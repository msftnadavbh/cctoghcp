"""Optional isolated help-only discovery. Not part of offline validation."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform

from scripts.runner import environment, run
from scripts.safety import private_write, safe_path

COMMANDS = {"version": ["--version"], "help": ["--help"],
            "commands": ["help", "commands"], "config": ["help", "config"],
            "environment": ["help", "environment"], "permissions": ["help", "permissions"],
            "plugin": ["plugin", "--help"], "plugin-install": ["plugin", "install", "--help"],
            "plugin-list": ["plugin", "list", "--help"],
            "plugin-enable": ["plugin", "enable", "--help"],
            "plugin-disable": ["plugin", "disable", "--help"],
            "plugin-uninstall": ["plugin", "uninstall", "--help"]}


def capture(executable, home, output):
    executable, home, output = safe_path(executable), safe_path(home), safe_path(output)
    # Reject symlink executable only at the caller boundary? npm's .bin entry
    # is a symlink; caller must supply the resolved, inspected loader instead.
    output.mkdir(mode=0o700, exist_ok=False)
    evidence = {"kind": "help-only", "captured_at": datetime.now(timezone.utc).isoformat(),
                "platform": platform.system(), "python": platform.python_version(),
                "auth_probes": False, "model_calls": False, "commands": []}
    for name, args in COMMANDS.items():
        result = run([str(executable), *args], cwd=home,
                     env={"PATH": "/usr/bin:/bin", "HOME": str(home)}, timeout=20, limit=1024 * 1024)
        # Only fixed help/version commands; no arbitrary diagnostic/env dumps.
        private_write(output / (name + ".txt"), result.stdout)
        private_write(output / (name + ".stderr.txt"), result.stderr)
        evidence["commands"].append({"id": name, "argv": ["copilot", *args],
                                    "status": result.status, "exit": result.returncode,
                                    "sha256": hashlib.sha256(result.stdout).hexdigest()})
    private_write(output / "capture.json", (json.dumps(evidence, indent=2) + "\n").encode())
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", required=True, type=Path)
    parser.add_argument("--home", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        evidence = capture(args.executable, args.home, args.output)
    except (ValueError, OSError):
        parser.exit(2, "help capture refused\n")
    print(json.dumps({"kind": evidence["kind"], "commands": len(evidence["commands"])}))
    return int(any(c["status"] != "ok" for c in evidence["commands"]))


if __name__ == "__main__":
    raise SystemExit(main())
