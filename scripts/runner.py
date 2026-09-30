"""POSIX subprocess runner: bounded capture, private outputs, process-group cleanup."""
from dataclasses import dataclass
import os
from pathlib import Path
import selectors
import math
import signal
import subprocess
import time

from scripts.safety import LIMIT, private_write, safe_path


@dataclass
class Result:
    status: str
    returncode: int | None
    stdout: bytes = b""
    stderr: bytes = b""


def environment(home, extra=None):
    home = safe_path(home)
    if not home.is_dir():
        raise ValueError("explicit HOME must exist")
    result = {"HOME": str(home), "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
              "NO_COLOR": "1"}
    allowed = {"COPILOT_GITHUB_TOKEN", "GITLAB_TOKEN"}
    for key, value in (extra or {}).items():
        if key not in allowed or not isinstance(value, str) or not value or "\0" in value or "\n" in value:
            raise ValueError("invalid environment entry")
        result[key] = value
    return result


def run(argv, *, cwd, env, stdin=b"", timeout=20, limit=LIMIT):
    if (not isinstance(argv, list) or not argv or
            any(not isinstance(a, str) or not a or "\0" in a for a in argv) or
            not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or
            not 0 < timeout <= 3600 or type(limit) is not int or not 0 < limit <= 16 * LIMIT or
            not isinstance(stdin, bytes) or len(stdin) > LIMIT):
        raise ValueError("invalid execution request")
    if not isinstance(env, dict) or any(not isinstance(k, str) or not isinstance(v, str)
                                        or "\0" in k + v or "=" in k for k, v in env.items()):
        raise ValueError("invalid environment")
    try:
        proc = subprocess.Popen(argv, cwd=safe_path(cwd), env=env,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, start_new_session=True)
    except FileNotFoundError:
        return Result("missing-executable", None)
    except OSError:
        return Result("launch-error", None)
    selector = selectors.DefaultSelector()
    output = {"stdout": bytearray(), "stderr": bytearray()}
    status = "ok"
    started = time.monotonic()
    pending = memoryview(stdin)
    for stream, name in ((proc.stdout, "stdout"), (proc.stderr, "stderr")):
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ, name)
    if pending:
        os.set_blocking(proc.stdin.fileno(), False)
        selector.register(proc.stdin, selectors.EVENT_WRITE, "stdin")
    else:
        proc.stdin.close()
    try:
        while selector.get_map() or proc.poll() is None:
            if time.monotonic() - started >= timeout:
                status = "timeout"
                break
            for key, _ in selector.select(0.03):
                stream, name = key.fileobj, key.data
                if name == "stdin":
                    try:
                        pending = pending[os.write(stream.fileno(), pending[:8192]):]
                    except BrokenPipeError:
                        pending = memoryview(b"")
                    if not pending:
                        selector.unregister(stream)
                        stream.close()
                    continue
                chunk = os.read(stream.fileno(), 8192)
                if not chunk:
                    selector.unregister(stream)
                    stream.close()
                elif len(output[name]) + len(chunk) > limit:
                    output[name].extend(chunk[:limit - len(output[name])])
                    status = "output-limit"
                    break
                else:
                    output[name].extend(chunk)
            if status != "ok":
                break
    finally:
        # Always signal the group, even when its leader has already exited.
        # Descendants that intentionally setsid() escape this: not a sandbox.
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        time.sleep(0.05)
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()
        selector.close()
        for stream in (proc.stdin, proc.stdout, proc.stderr):
            stream.close()
    if status == "ok" and proc.returncode != 0:
        status = "nonzero-exit"
    return Result(status, proc.returncode, bytes(output["stdout"]), bytes(output["stderr"]))


def reserve(directory):
    directory = safe_path(directory)
    directory.mkdir(mode=0o700, exist_ok=False)
    directory.chmod(0o700)
    return directory


def save(result, directory, *, reserved=False):
    directory = safe_path(directory)
    if not reserved:
        reserve(directory)
    elif (not directory.is_dir() or directory.stat().st_uid != os.getuid() or
          directory.stat().st_mode & 0o077):
        raise ValueError("unsafe reserved output")
    private_write(directory / "stdout.bin", result.stdout)
    private_write(directory / "stderr.bin", result.stderr)
