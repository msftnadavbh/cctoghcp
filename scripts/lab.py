"""Disposable copies; ownership state must live outside the lab. Never commits."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import stat
import uuid

from scripts.safety import json_load, private_write, read_regular, safe_path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_ASSETS = {
    "CLAUDE.md": "examples/coexistence/CLAUDE.md",
    "guidance/shared.md": "examples/coexistence/guidance/shared.md",
    ".github/agents/repository-reviewer.agent.md": "examples/agents/repository-reviewer.agent.md",
    **{f".claude/skills/{name}/SKILL.md": f".claude/skills/{name}/SKILL.md" for name in
       ("repo-recon", "reproduction-brief", "verification-handoff")},
}


def state_dir(path, create=True):
    path = safe_path(path)
    if create:
        path.mkdir(mode=0o700, parents=False, exist_ok=True)
    info = path.stat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError("state must be private and owned")
    return path


def inspect_tree(path):
    device = path.stat().st_dev
    count = 0
    # ismount alone misses Linux bind mounts on the same device.
    mounts = set()
    if Path("/proc/self/mountinfo").exists():
        for line in Path("/proc/self/mountinfo").read_text().splitlines():
            mounts.add(re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), line.split()[4]))
    for parent, dirs, files in os.walk(path, followlinks=False):
        for item in [Path(parent), *(Path(parent) / n for n in dirs + files)]:
            count += 1
            if count > 10_000:
                raise ValueError("tree bound exceeded")
            info = item.lstat()
            if (stat.S_ISLNK(info.st_mode) or info.st_dev != device or
                    str(item) in mounts or os.path.ismount(item) or
                    info.st_uid != os.getuid() or
                    not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode))):
                raise ValueError("unsafe tree")


def setup(dest, state, exercise="baseline", with_config=False):
    if type(with_config) is not bool:
        raise ValueError("invalid config option")
    if exercise not in {"baseline", "validation", "in-stock", "refactor"}:
        raise ValueError("unknown exercise")
    if ".." in Path(dest).parts or ".." in Path(state).parts:
        raise ValueError("parent traversal refused")
    dest, state = safe_path(dest), safe_path(state)
    if dest == ROOT or dest in ROOT.parents or dest.is_relative_to(ROOT):
        raise ValueError("lab must be outside repository")
    if state == dest or state.is_relative_to(dest) or dest.is_relative_to(state):
        raise ValueError("state must be separate")
    if dest.exists():
        raise ValueError("destination must not exist")
    if not dest.parent.is_dir():
        raise ValueError("destination parent missing")
    state = state_dir(state)
    source = ROOT / "labs/sample-app"
    inspect_tree(source)
    # Fixed files only: never copy a whole customization/conflict fixture tree.
    assets = {target: read_regular(ROOT / origin) for target, origin in CONFIG_ASSETS.items()} if with_config else {}
    dest.mkdir(mode=0o700, exist_ok=False)
    dest.chmod(0o700)
    inspect_tree(dest)
    ident = uuid.uuid4().hex
    info = dest.stat()
    record = {"id": ident, "path": str(dest), "device": info.st_dev,
              "inode": info.st_ino, "uid": info.st_uid, "exercise": exercise, "with_config": with_config}
    private_write(state / (ident + ".json"), json.dumps(record).encode())
    private_write(dest / ".checkpoint-owner", ident.encode())
    try:
        # Copy children, not source-root metadata, preserving private root even
        # during partial failure. Ownership is established before bulk copying.
        for child in source.iterdir():
            if child.is_dir():
                shutil.copytree(child, dest / child.name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            else:
                shutil.copyfile(child, dest / child.name)
        if exercise == "validation":
            catalog = dest / "src/catalog.py"
            catalog.write_text(catalog.read_text().replace("type(value) is not int", "not isinstance(value, int)"))
        for target, data in assets.items():
            path = dest / target
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            private_write(path, data)
    finally:
        dest.chmod(0o700)
    return record


def cleanup(ident, state):
    if not re.fullmatch(r"[0-9a-f]{32}", ident):
        raise ValueError("invalid ownership id")
    state = state_dir(state, create=False)
    record_path = state / (ident + ".json")
    record = json_load(read_regular(record_path))
    dest = safe_path(record["path"])
    if (record["id"] != ident or dest == ROOT or dest in ROOT.parents or
            dest.is_relative_to(ROOT) or state == dest or state.is_relative_to(dest)):
        raise ValueError("invalid ownership record")
    info = dest.stat()
    if (info.st_dev, info.st_ino, info.st_uid) != (record["device"], record["inode"], record["uid"]):
        raise ValueError("identity changed")
    if read_regular(dest / ".checkpoint-owner") != ident.encode():
        raise ValueError("ownership marker mismatch")
    inspect_tree(dest)
    if not shutil.rmtree.avoids_symlink_attacks:
        raise ValueError("safe deletion unavailable")
    shutil.rmtree(dest)
    record_path.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["setup", "cleanup"])
    parser.add_argument("target", help="destination for setup; ownership ID for cleanup")
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--exercise", default="baseline", choices=["baseline", "validation", "in-stock", "refactor"])
    parser.add_argument("--with-config", action="store_true", help="copy only reviewed instructions, three skills and reviewer agent")
    args = parser.parse_args()
    try:
        if args.action == "setup":
            print(json.dumps(setup(args.target, args.state, args.exercise, args.with_config), sort_keys=True))
        else:
            cleanup(args.target, args.state)
            print("owned lab removed")
    except (OSError, ValueError, KeyError, TypeError):
        parser.exit(2, "lab operation refused; inspect ownership and paths locally\n")


if __name__ == "__main__":
    main()
