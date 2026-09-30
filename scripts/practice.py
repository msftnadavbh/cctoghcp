"""Native, offline practice for reviewed local code; not a sandbox or deletion tool."""
import sys

if sys.version_info < (3, 12):
    print("practice requires Python 3.12 or newer; select a Python 3.12+ executable", file=sys.stderr)
    raise SystemExit(2)

import argparse
import difflib
import importlib.util
import os
from pathlib import Path, PureWindowsPath
import re
import stat
import subprocess
import tempfile
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
# With -I, only the explicitly trusted book is added, never cwd or the lab.
sys.path.insert(0, str(ROOT))
from scripts.lab import CONFIG_ASSETS
from scripts.runner import Result

APP_FILES = ("src/catalog.py", "tests/test_catalog.py", "scripts/check_lab.py")
EXERCISES = ("validation", "baseline", "in-stock", "refactor")
LIMIT = 256 * 1024
OUTPUT_LIMIT = 65536
TREE_LIMIT = 1000
TOTAL_LIMIT = 8 * 1024 * 1024
GUARD = b"type(value) is not int"
BROKEN_GUARD = b"not isinstance(value, int)"


def windows_spelling(raw):
    """Pure lexical Windows checks, also testable on non-Windows hosts."""
    path = PureWindowsPath(raw)
    if raw.startswith(("\\", "/")) or (path.drive and not path.root):
        raise ValueError("use a local drive-absolute or ordinary relative path, not UNC/device paths")
    tail = raw[len(path.anchor):] if path.anchor else raw
    for part in re.split(r"[\\/]", tail):
        if (not part or part in {".", ".."} or part.endswith((" ", ".")) or
                any(ord(c) < 32 or c in '<>:"|?*' for c in part) or
                re.fullmatch(r"CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|(?:COM|LPT)[1-9¹²³]",
                             part.split(".", 1)[0].rstrip(" ").upper())):
            raise ValueError("ambiguous or reserved Windows path refused")


def ordinary(path):
    raw = os.fspath(path)
    if not raw or "\0" in raw or ".." in Path(raw).parts:
        raise ValueError("empty path or parent traversal refused")
    if os.name == "nt":
        windows_spelling(raw)
    path = Path(raw).absolute()
    for part in (*reversed(path.parents), path):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        # Windows junctions and other reparse points need not be symlinks.
        reparse = os.name == "nt" and info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
        if stat.S_ISLNK(info.st_mode) or reparse:
            raise ValueError("symlink or reparse point refused")
        if part != path and not stat.S_ISDIR(info.st_mode):
            raise ValueError("ancestor is not a directory")
    return path


def read_file(path):
    path = ordinary(path)
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > LIMIT:
        raise ValueError("not a bounded regular file")
    # lstat then open is for stable, trusted local trees, not adversarial races.
    with path.open("rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("not a regular file")
        data = stream.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError("file size bound exceeded")
    return data


def assets(with_config):
    result = {name: read_file(ROOT / "labs/sample-app" / name) for name in APP_FILES}
    if with_config:
        result.update({name: read_file(ROOT / source) for name, source in CONFIG_ASSETS.items()})
    return result


def outside_book(path):
    path = ordinary(path)
    if (path == ROOT or path in ROOT.parents or path.is_relative_to(ROOT) or
            any(part.exists() and os.path.samefile(part, ROOT) for part in (path, *path.parents)) or
            (path.exists() and any(os.path.samefile(path, part) for part in ROOT.parents))):
        raise ValueError("lab must be outside the book, not the book or an ancestor")
    return path


def setup(dest, exercise="validation", with_config=False):
    if exercise not in EXERCISES or type(with_config) is not bool:
        raise ValueError("invalid setup option")
    dest = outside_book(dest)
    if dest.exists() or not dest.parent.is_dir():
        raise ValueError("destination must not exist; its parent must already exist")
    files = assets(with_config)
    if exercise == "validation":
        if files["src/catalog.py"].count(GUARD) != 1:
            raise ValueError("canonical validation guard must occur exactly once")
        files["src/catalog.py"] = files["src/catalog.py"].replace(GUARD, BROKEN_GUARD, 1)
    dest.mkdir(mode=0o700)
    try:
        for name, data in files.items():
            path = ordinary(dest / name)
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(data)
    except (OSError, ValueError):
        raise ValueError("partial setup retained; inspect it manually and choose another destination name") from None
    return dest


def tree(root):
    root = outside_book(root)
    if not root.is_dir():
        raise ValueError("lab must be an existing directory")
    files, pending, count, total = {}, [root], 0, 0
    while pending:
        with os.scandir(pending.pop()) as entries:
            for entry in entries:
                count += 1
                if count > TREE_LIMIT:
                    raise ValueError("tree entry bound exceeded")
                path = ordinary(entry.path)
                info = path.lstat()
                if stat.S_ISDIR(info.st_mode):
                    pending.append(path)
                else:
                    data = read_file(path)
                    total += len(data)
                    if total > TOTAL_LIMIT:
                        raise ValueError("tree byte bound exceeded")
                    files[path.relative_to(root).as_posix()] = data
    return files


def diff(root):
    current = tree(root)
    # Missing optional configs are reported too; there is no hidden setup state.
    canonical = assets(True)
    changed = False
    for name in sorted(canonical.keys() | current.keys()):
        before, after = canonical.get(name), current.get(name)
        if before == after:
            continue
        changed = True
        label = (name.encode("unicode_escape").decode("ascii") if
                 any(unicodedata.category(c) in {"Cc", "Cf"} for c in name) else name)
        print(f"{'added' if before is None else 'deleted' if after is None else 'changed'}: {label}")
        try:
            texts = [(data or b"").decode("utf-8") for data in (before, after)]
            if any(unicodedata.category(c) in {"Cc", "Cf"} and c not in "\t\n"
                   for text in texts for c in text):
                raise ValueError("binary content")
        except (UnicodeError, ValueError):
            print(f"Binary content differs ({len(before or b'')} -> {len(after or b'')} bytes); content omitted.")
            continue
        print("".join(difflib.unified_diff(
            texts[0].splitlines(keepends=True), texts[1].splitlines(keepends=True),
            fromfile="canonical/" + label, tofile="lab/" + label)), end="\n")
    if not changed:
        print("No differences from canonical files (the canonical validation bug is already fixed).")
    return changed


def load_oracle():
    spec = importlib.util.spec_from_file_location("practice_acceptance", ROOT / "labs/expected-results/acceptance.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class _Observer:
    """Private fixed-Python observer, deliberately not a general command runner."""
    def __init__(self, root, scratch, oracle):
        self.root, self.scratch, self.oracle = root, scratch, oracle

    def __call__(self, argv, stdin=b""):
        prefix = [sys.executable, "-I", "-B"]
        checker = prefix + [str(self.root / "scripts/check_lab.py")]
        probe = prefix + [str(self.oracle.PROBE), str(self.root)]
        cli = prefix + [str(self.root / "src/catalog.py")]
        if (argv != checker and argv != probe and not (
                argv[:4] == cli and len(argv[4:]) % 2 == 0 and len(argv) <= 12 and
                all(argv[i] in {"--query", "--offset", "--limit", "--in-stock"} for i in range(4, len(argv), 2)))):
            raise ValueError("only fixed practice probes are supported")
        if not isinstance(stdin, bytes) or len(stdin) > OUTPUT_LIMIT:
            raise ValueError("probe input bound exceeded")
        work = Path(tempfile.mkdtemp(prefix="probe-", dir=self.scratch))
        home = work / "home"
        home.mkdir()
        env = {key: str(home) for key in ("HOME", "USERPROFILE", "TMP", "TEMP", "TMPDIR")}
        env.update({"LANG": "C.UTF-8", "NO_COLOR": "1"})
        if os.name == "nt":
            env.update({key: os.environ[key] for key in ("SystemRoot", "WINDIR") if key in os.environ})
        # Keep handles open and read at most limit+1 after exit. Disk output is
        # not quota-limited. No pipe writes, communicate(), or recursive cleanup.
        with (work / "stdin.bin").open("x+b") as source, (work / "stdout.bin").open("x+b") as out, (work / "stderr.bin").open("x+b") as err:
            source.write(stdin)
            source.seek(0)
            try:
                proc = subprocess.Popen(argv, cwd=work, env=env, stdin=source, stdout=out, stderr=err)
            except OSError:
                return Result("launch-error", None)
            status = "ok"
            try:
                proc.wait(timeout=20 if argv == checker else self.oracle.TIMEOUT)
            except subprocess.TimeoutExpired:
                status = "timeout"
                proc.kill()  # Direct child only; descendants are not contained.
                proc.wait()
            out.seek(0)
            err.seek(0)
            stdout, stderr = out.read(OUTPUT_LIMIT + 1), err.read(OUTPUT_LIMIT + 1)
        if max(len(stdout), len(stderr)) > OUTPUT_LIMIT:
            status = "output-limit"
        elif status == "ok" and proc.returncode:
            status = "nonzero-exit"
        return Result(status, proc.returncode, stdout[:OUTPUT_LIMIT], stderr[:OUTPUT_LIMIT])


def check(root, exercise="validation"):
    if exercise not in EXERCISES:
        raise ValueError("unknown exercise")
    root = outside_book(root)
    files = tree(root)
    if any(name not in files for name in APP_FILES):
        raise ValueError("required app file missing")
    if files["scripts/check_lab.py"] != read_file(ROOT / "labs/sample-app/scripts/check_lab.py"):
        raise ValueError("check_lab.py must match the trusted canonical checker; review diff")
    oracle = load_oracle()
    scratch = Path(tempfile.mkdtemp(prefix="checkpoint-practice-")).resolve()
    print(f"Check artifacts retained: {scratch}", flush=True)
    observe = _Observer(root, scratch, oracle)
    result = observe([sys.executable, "-I", "-B", str(root / "scripts/check_lab.py")])
    print(f"App tests: {result.status}")
    for data in (result.stdout, result.stderr):
        if data:
            print(data.decode("utf-8", "replace"), end="\n")
    passed = result.status == "ok"
    try:
        oracle.check(root, exercise, observe=observe)
        print(f"Independent acceptance passed: {exercise}")
    except AssertionError as error:
        print(f"Independent acceptance failed: {error}")
        passed = False
    print("Review artifacts locally; remove manually only after all child processes have stopped.")
    return passed


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("setup", "diff", "check"):
        child = sub.add_parser(command)
        child.add_argument("path")
        if command != "diff":
            child.add_argument("--exercise", choices=EXERCISES, default="validation")
        if command == "setup":
            child.add_argument("--with-config", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "setup":
            print(f"Practice lab created: {setup(args.path, args.exercise, args.with_config)}")
        elif args.command == "diff":
            diff(args.path)
        else:
            return 0 if check(args.path, args.exercise) else 1
    except (OSError, ValueError) as error:
        parser.exit(2, f"Practice operation refused: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
