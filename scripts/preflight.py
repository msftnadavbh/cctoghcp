"""Conservative wrapper profile, not a complete Copilot policy resolver/sandbox.

Refuse any known configuration source, even benign or malformed configuration.
Use a fresh empty owned 0700 HOME; ordinary configured CLI homes are unsupported.
No credential values are read. Existence checks never execute configuration.
"""
import os
from pathlib import Path
import shutil
import stat

from scripts.safety import safe_path

POLICY = Path("/etc/github-copilot")
ACTIVE = (".github/hooks", ".github/copilot", ".github/agents", ".github/skills",
          ".github/instructions", ".github/copilot-instructions.md", ".claude",
          ".agents", ".copilot", ".mcp.json", "AGENTS.md", "CLAUDE.md",
          "plugin.json", ".plugin", ".claude-plugin", "lsp.json", ".github/lsp.json",
          ".github/extensions", ".github/mcp.json", ".github/plugin", ".vscode/mcp.json")


def disjoint(left, right):
    return not (left == right or left.is_relative_to(right) or right.is_relative_to(left))


def executable_path(value):
    path = Path(value)
    if not path.is_absolute():
        if "/" in value or value in {".", ".."}:
            raise ValueError("absolute executable or trusted PATH name required")
        found = shutil.which(value, path="/usr/bin:/bin")
        if not found:
            raise FileNotFoundError("executable unavailable")
        path = Path(found)
    path = path.resolve(strict=True)
    if not path.is_file() or not os.access(path, os.X_OK):
        raise ValueError("executable unavailable")
    return str(path)


def preflight(root, home, output):
    root, home, output = map(safe_path, (root, home, output))
    if not root.is_dir() or not home.is_dir():
        raise ValueError("existing workspace and designated HOME required")
    if not all(disjoint(a, b) for a, b in ((root, home), (root, output), (home, output))):
        raise ValueError("workspace HOME and output must be separate")
    if POLICY.exists() or POLICY.is_symlink():
        raise ValueError("machine policy location present; wrapper refuses execution")
    for ancestor in (root, *root.parents):
        for name in ACTIVE:
            candidate = ancestor / name
            if candidate.exists() or candidate.is_symlink():
                raise ValueError("workspace or ancestor configuration refused")
    # Known roots give a generic configuration diagnostic; remaining content is
    # refused too. This does not assert every location is loaded by Copilot.
    for name in (*ACTIVE, ".config/copilot", ".config/github-copilot", ".config/claude"):
        candidate = home / name
        if candidate.exists() or candidate.is_symlink():
            raise ValueError("designated HOME configuration refused")
    info = home.stat()
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700 or any(home.iterdir()):
        raise ValueError("HOME must be fresh empty owned private 0700")
    if output.exists() or not output.parent.is_dir():
        raise ValueError("new private output directory required")
    return root, home, output
