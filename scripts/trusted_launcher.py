"""Standalone launcher; invoke via reviewed absolute Python with -I -B.

The launcher and its repository must remain outside the editable lab. The only
added import path is the launcher's own trusted root, never payload/process cwd.
"""
from pathlib import Path
import sys


def main():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    if len(sys.argv) < 2 or sys.argv[1] not in {"hook", "mcp"}:
        raise SystemExit("usage: trusted_launcher.py hook|mcp [arguments]")
    mode = sys.argv.pop(1)
    if mode == "hook":
        from scripts.hook_handler import main as entry
    else:
        from scripts.mcp_server import main as entry
    return entry()


if __name__ == "__main__":
    raise SystemExit(main())
