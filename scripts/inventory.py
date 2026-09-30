"""Passive, bounded inventory. Found is never a claim of product support."""
import argparse
import json
import os
from pathlib import Path
import stat

from scripts.safety import json_load, read_regular, safe_path

STANDARD = ["CLAUDE.md", "AGENTS.md", ".claude/CLAUDE.md", ".claude/settings.json",
            ".claude/settings.local.json", ".claude/rules", ".claude/skills",
            ".claude/agents", ".claude/commands", ".mcp.json", ".github/agents",
            ".github/skills", ".github/hooks", ".github/instructions",
            ".github/copilot-instructions.md", ".copilot/mcp-config.json",
            ".github/copilot/settings.json", ".github/copilot/settings.local.json",
            ".agents/skills", "plugin.json", ".claude-plugin/plugin.json",
            ".vscode/mcp.json", ".vscode/mcp.jsonc"]
FIELDS = {"hooks", "mcpServers", "permissions", "env", "model", "tools",
          "include-custom-instructions", "enabledPlugins", "command", "args",
          "type", "url", "headers", "PreToolUse", "PostToolUse", "preToolUse",
          "postToolUse", "allow", "deny", "ask", "matcher", "timeout", "bash",
          "exec", "cwd", "timeoutSec"}


def known_fields(value, depth=0):
    if depth > 12:
        return set()
    found = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FIELDS:
                found.add(key)
            found.update(known_fields(child, depth + 1))
    elif isinstance(value, list):
        for child in value[:256]:
            found.update(known_fields(child, depth + 1))
    return found


def inventory(root):
    root = safe_path(root)
    if not root.is_dir() or root == Path.home() or root == Path("/"):
        raise ValueError("explicit repository root required")
    results = []
    for name in STANDARD:
        path = root / name
        category = ("skills" if "skills" in name else "agents" if "agents" in name else
                    "hooks" if "hooks" in name else "mcp" if "mcp" in name else
                    "plugin" if "plugin" in name else "settings" if "settings" in name else
                    "commands" if "commands" in name else "instructions")
        entry = {"path": name, "category": category, "status": "absent", "known_fields": []}
        try:
            safe_path(path)
            info = path.lstat()
            if stat.S_ISREG(info.st_mode):
                data = read_regular(path)
                entry["status"] = "found"
                if path.suffix == ".json":
                    entry["known_fields"] = sorted(known_fields(json_load(data)))
                elif path.suffix == ".jsonc":
                    entry["status"] = "found-unparsed-jsonc"
            elif stat.S_ISDIR(info.st_mode):
                entry["status"] = "found-directory"
                # Never emit arbitrary child names: names themselves may be secrets.
                with os.scandir(path) as children:
                    entry["bounded_entries"] = sum(1 for _, _item in zip(range(256), children))
            else:
                entry["status"] = "skipped-special"
        except FileNotFoundError:
            pass
        except (OSError, ValueError):
            entry["status"] = "unreadable-or-unsafe"
        results.append(entry)
    return {"meaning": "found != supported; values and arbitrary names omitted",
            "scope": "explicit root; no home recursion; no execution", "entries": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = inventory(args.root)
    except (OSError, ValueError):
        parser.exit(2, "inventory refused\n")
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(result["meaning"])
        for entry in result["entries"]:
            print(entry["path"], entry["status"], ",".join(entry["known_fields"]))


if __name__ == "__main__":
    main()
