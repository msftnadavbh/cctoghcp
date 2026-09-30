"""Render compact reference tables from the reviewed migration matrix; --check is read-only."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "evidence/migration-matrix.json"
OUTPUTS = {"muscle-memory.md": ("Claude habit", "Copilot move", "Caution"),
           "cli-cheat-sheet.md": ("Goal from Claude", "Exact move", "Boundary")}
CLASSES = frozenset({
    "Directly reusable", "Same concept, different syntax", "Similar outcome, different architecture",
    "Copilot-specific opportunity", "No clean equivalent", "GitHub-hosted capability",
    "Preview or experimental", "Unclear or requires a version-specific test",
})
REQUIRED = {"habit", "outcome", "mechanism", "syntax", "classification", "hosting", "availability",
            "version_status", "source_ids", "difference"}


def validate_rows(rows, sources):
    if (not isinstance(rows, list) or len(rows) < 41 or
            len({r.get("habit") for r in rows if isinstance(r, dict)}) != len(rows)):
        raise ValueError("migration matrix incomplete or duplicate habits")
    for row in rows:
        if (not isinstance(row, dict) or not REQUIRED <= row.keys() or
                row["classification"] not in CLASSES or
                row["hosting"] not in {"host-independent", "gitlab-required", "github-required"} or
                not all(isinstance(row[key], str) and row[key].strip() for key in REQUIRED - {"source_ids"}) or
                not isinstance(row["source_ids"], list) or not row["source_ids"] or
                any(not isinstance(s, str) or s not in sources for s in row["source_ids"])):
            raise ValueError("migration matrix metadata invalid")


def render(rows, name):
    a, b, c = OUTPUTS[name]
    lines = [f"# {name.removesuffix('.md').replace('-', ' ').title()}", "",
             "Generated from [migration matrix](../../evidence/migration-matrix.json) by `python3 -B -m scripts.generate_reference`; do not edit this table manually.",
             "", f"| {a} | {b} | {c} |", "| --- | --- | --- |"]
    for row in rows:
        if name == "cli-cheat-sheet.md" and row["classification"] in {
                "No clean equivalent", "GitHub-hosted capability", "Preview or experimental",
                "Unclear or requires a version-specific test"}:
            continue
        cells = (row["habit"], row["syntax"], row["difference"])
        lines.append("| " + " | ".join(str(x).replace("|", "\\|").replace("`", "\\`") for x in cells) + " |")
    lines.extend(["", "Per-row classification, version/status, source IDs and hosting: [migration matrix](../../evidence/migration-matrix.json). Entries are source/help observations, not authenticated runtime proof. [Versions](versions.md).", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rows = json.loads(MATRIX.read_text())
    try:
        validate_rows(rows, {s["id"] for s in json.loads((ROOT / "evidence/sources.json").read_text())})
    except ValueError as error:
        parser.error(str(error))
    for name in OUTPUTS:
        target = ROOT / "docs/reference" / name
        content = render(rows, name)
        if args.check:
            if not target.is_file() or target.read_text() != content:
                parser.error(f"generated reference stale: {target}")
        else:
            target.write_text(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
