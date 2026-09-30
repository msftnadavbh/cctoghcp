"""Paid integration adapter, dry-run by default. Never widens tool permissions."""
import argparse
import json
import math
import os
from pathlib import Path

from scripts.runner import environment, run, save, reserve
from scripts.preflight import executable_path, preflight
from scripts.safety import has_secret, json_load, read_regular, safe_path, static_python

MODES = {"repo-summary", "diff-review", "test-fix", "gitlab-log-summary"}
EXIT = {"ok": 0, "dry-run": 0, "missing-executable": 10, "launch-error": 11,
        "timeout": 12, "output-limit": 13, "nonzero-exit": 14,
        "invalid-jsonl": 15, "static-check-failed": 16,
        "validation-pending": 17, "report-unverified": 18}


def consume(raw):
    """Structural JSONL only. No invented terminal event or task-success claim.

    Unknown typed objects are retained verbatim in private output. A process
    exit of zero and well-formed events do not establish semantic completion.
    """
    if not raw.endswith(b"\n"):
        raise ValueError("incomplete JSONL")
    events = [json_load(line) for line in raw.splitlines() if line.strip()]
    if not events or len(events) > 4096:
        raise ValueError("invalid events")
    for event in events:
        if not isinstance(event, dict) or not isinstance(event.get("type"), str) or not event["type"]:
            raise ValueError("invalid event")
    return events


def command(executable, mode):
    if mode not in MODES:
        raise ValueError("invalid mode")
    tools = ["view", "grep", "glob"]
    if mode == "test-fix":
        tools += ["edit", "create"]
    permissions = ["read"]
    if mode == "test-fix":
        permissions += ["write(src/catalog.py)", "write(tests/test_catalog.py)"]
    return [str(executable), "--no-auto-update", "--no-remote", "--no-remote-export",
            "--disable-builtin-mcps", "--no-custom-instructions", "--no-bash-env", "--disallow-temp-dir",
            "--secret-env-vars=COPILOT_GITHUB_TOKEN",
            "--no-ask-user", "--output-format", "json", "--available-tools=" + ",".join(tools),
            *("--allow-tool=" + permission for permission in permissions)]


def execute(args):
    root = safe_path(args.repo)
    if not root.is_dir():
        raise ValueError("repository directory required")
    prompt_path = safe_path(args.prompt_file)
    prompt = read_regular(prompt_path)
    if not prompt.strip() or has_secret(prompt):
        raise ValueError("prompt rejected")
    if args.mode == "gitlab-log-summary":
        content = json_load(prompt)
        if (not isinstance(content, dict) or content.get("kind") != "sanitized-ci" or
                set(content) != {"kind", "synthetic", "failure_observed", "success_observed", "detail"} or
                any(type(content[k]) is not bool for k in ("synthetic", "failure_observed", "success_observed")) or
                content["detail"] != "Raw log omitted; inspect locally before proposing a fix."):
            raise ValueError("sanitized log required")
    argv = command(args.executable, args.mode)
    if not args.execute:
        return {"status": "dry-run", "mode": args.mode, "argv": argv,
                "prompt_transport": "reviewed file bytes via stdin; real CLI untested"}
    if not args.consent_paid or not args.reviewed_workspace or not args.home or not args.output:
        raise ValueError("explicit paid consent, reviewed workspace, HOME and output required")
    if getattr(args, "credential_env", None) != "COPILOT_GITHUB_TOKEN":
        raise ValueError("explicit supported credential selection required")
    credential = os.environ.get("COPILOT_GITHUB_TOKEN")
    if (not isinstance(credential, str) or not credential.strip() or
            any(char in credential for char in ("\0", "\n", "\r"))):
        raise ValueError("selected credential missing or invalid")
    root, home, output = preflight(root, args.home, args.output)
    child_env = environment(home, {"COPILOT_GITHUB_TOKEN": credential})
    if not isinstance(args.timeout, (int, float)) or not math.isfinite(args.timeout) or not 0 < args.timeout <= 3600:
        raise ValueError("invalid timeout")
    try:
        argv[0] = executable_path(args.executable)
    except FileNotFoundError:
        return {"status": "missing-executable", "process_exit": None, "mode": args.mode}
    if Path(argv[0]).is_relative_to(root):
        raise ValueError("executable must be outside editable workspace")
    reserve(output)
    # Forward only the explicitly selected variable, never the ambient environment.
    result = run(argv, cwd=root, env=child_env, stdin=prompt, timeout=args.timeout)
    save(result, output, reserved=True)
    status = result.status
    if status == "ok":
        try:
            consume(result.stdout)
        except ValueError:
            status = "invalid-jsonl"
    if status == "ok" and args.mode == "test-fix":
        try:
            for path in (root / "src/catalog.py", root / "tests/test_catalog.py"):
                static_python(path)
        except (ValueError, OSError):
            status = "static-check-failed"
    if status == "ok":
        status = "validation-pending" if args.mode == "test-fix" else "report-unverified"
    return {"status": status, "process_exit": result.returncode, "mode": args.mode,
            "integration": "Task completion unverified. Review private output and diff; run acceptance separately only after human code review."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=sorted(MODES))
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--executable", default="copilot")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--consent-paid", action="store_true")
    parser.add_argument("--reviewed-workspace", action="store_true")
    parser.add_argument("--home", type=Path)
    parser.add_argument("--credential-env", choices=["COPILOT_GITHUB_TOKEN"],
                        help="explicit environment variable selection; required only for execution")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--timeout", type=float, default=120)
    args = parser.parse_args()
    try:
        result = execute(args)
    except (ValueError, OSError):
        parser.exit(2, "headless request refused; check consent, selected credential, fresh private HOME and paths; no values logged\n")
    print(json.dumps(result, sort_keys=True))
    return EXIT[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
