"""Deterministic skill-only ZIP built from the single canonical skill tree."""
import argparse
import io
from pathlib import Path
import zipfile

from scripts.safety import private_write, read_regular, safe_path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("repo-recon", "reproduction-brief", "verification-handoff")


def contents(root=ROOT):
    files = {"plugin.json": read_regular(root / "examples/plugin/plugin.json")}
    for skill in SKILLS:
        files[f"skills/{skill}/SKILL.md"] = read_regular(root / f".claude/skills/{skill}/SKILL.md")
    return files


def archive(root=ROOT):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as output:
        for name, data in sorted(contents(root).items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            output.writestr(info, data)
    return buffer.getvalue()


def build(path, directory=False):
    path = safe_path(path)
    if directory:
        path.mkdir(mode=0o700, exist_ok=False)
        for name, data in contents().items():
            target = path / name
            target.parent.mkdir(parents=True, exist_ok=True)
            private_write(target, data)
    else:
        private_write(path, archive())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--directory", action="store_true")
    args = parser.parse_args()
    try:
        build(args.output, args.directory)
    except (OSError, ValueError):
        parser.exit(2, "plugin output refused\n")
    print("skill-only package created")


if __name__ == "__main__":
    main()
