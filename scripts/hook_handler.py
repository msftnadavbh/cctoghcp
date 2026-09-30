"""Inert until explicitly registered. Defense in depth, never a sandbox."""
import argparse
import json
import os
from pathlib import Path
import stat
import sys

from scripts.safety import LIMIT, has_secret, json_load, safe_path, static_python

ALIASES = {"Read": "view", "Grep": "grep", "Glob": "glob", "Write": "create",
           "Edit": "edit", "Bash": "bash"}
READ = {"view", "grep", "glob"}
EDIT = {"edit", "create"}


def normalize(raw, event):
    value = json_load(raw)
    if not isinstance(value, dict):
        raise ValueError("invalid payload")
    native = "toolName" in value or "toolArgs" in value
    compatible = "tool_name" in value or "tool_input" in value
    if native == compatible:
        raise ValueError("ambiguous payload")
    if native:
        name, args = value.get("toolName"), value.get("toolArgs")
        if "hook_event_name" in value:
            raise ValueError("mixed payload")
    else:
        name, args = value.get("tool_name"), value.get("tool_input")
        if value.get("hook_event_name") != {"pre": "PreToolUse", "post": "PostToolUse"}[event]:
            raise ValueError("invalid event")
    if isinstance(args, str):
        args = json_load(args)
    if not isinstance(name, str) or not name or not isinstance(args, dict):
        raise ValueError("missing tool fields")
    cwd = value.get("cwd")
    if not isinstance(cwd, str) or not Path(cwd).is_absolute():
        raise ValueError("missing cwd")
    return ALIASES.get(name, name), args, safe_path(cwd)


def edit_path(args, root):
    keys = set(args) & {"path", "file_path", "filePath"}
    if len(keys) != 1:
        raise ValueError("ambiguous edit path")
    value = args[next(iter(keys))]
    if not isinstance(value, str) or not value or ".." in Path(value).parts:
        raise ValueError("invalid edit path")
    path = safe_path(root / value)
    if not path.is_relative_to(root / "src") or path.suffix != ".py":
        raise ValueError("protected path")
    if path.exists() and not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("special edit target")
    return path


def handle(raw, event, root):
    root = safe_path(root)
    if not root.is_dir():
        raise ValueError("missing lab")
    name, args, cwd = normalize(raw, event)
    if cwd != root:
        raise ValueError("unexpected cwd")
    if has_secret(raw):
        raise ValueError("secret gate")
    if name in READ:
        return {}, "neutral"
    if name not in EDIT:
        raise ValueError("unreviewed tool")
    path = edit_path(args, root)
    if event == "post":
        static_python(path)
        return {"additionalContext": "Static syntax/secret checks passed only; review diff before separate acceptance."}, "static-check-passed"
    return {}, "neutral"


def event_log(path, event, outcome):
    if event not in {"pre", "post"} or outcome not in {"neutral", "denied", "static-check-passed", "static-check-failed"}:
        raise ValueError("invalid log enum")
    path = safe_path(path)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    with os.fdopen(fd, "wb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077 or info.st_size > LIMIT:
            raise ValueError("unsafe log")
        stream.write(json.dumps({"event": event, "outcome": outcome}).encode() + b"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event", choices=["pre", "post"])
    parser.add_argument("--lab", required=True, type=Path)
    parser.add_argument("--event-log", type=Path)
    args = parser.parse_args()
    code = 0
    try:
        response, outcome = handle(sys.stdin.buffer.read(LIMIT + 1), args.event, args.lab)
    except (ValueError, OSError, TypeError, KeyError):
        response = ({"permissionDecision": "deny", "permissionDecisionReason": "Lab policy rejected the request."}
                    if args.event == "pre" else {"additionalContext": "Static check failed or input was unsafe; inspect locally. No code was executed."})
        outcome, code = ("denied", 2) if args.event == "pre" else ("static-check-failed", 0)
    if args.event_log:
        try:
            event_log(args.event_log, args.event, outcome)
        except (ValueError, OSError):
            response = ({"permissionDecision": "deny", "permissionDecisionReason": "Lab event logging failed."}
                        if args.event == "pre" else {"additionalContext": "Lab event logging failed."})
            code = 2 if args.event == "pre" else 0
    print(json.dumps(response, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
