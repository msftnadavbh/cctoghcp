import json
import unittest

from scripts.generate_reference import MATRIX, OUTPUTS, ROOT, render, validate_rows


class ReferenceTests(unittest.TestCase):
    def test_references_are_generated_from_unique_habits(self):
        rows = json.loads(MATRIX.read_text())
        self.assertGreaterEqual(len(rows), 41)
        self.assertEqual(len(rows), len({r["habit"] for r in rows}))
        sources = {s["id"] for s in json.loads((ROOT / "evidence/sources.json").read_text())}
        validate_rows(rows, sources)
        for name in OUTPUTS:
            self.assertEqual((ROOT / "docs/reference" / name).read_text(), render(rows, name))

    def test_matrix_metadata_rejects_invalid_class_version_and_source(self):
        rows = json.loads(MATRIX.read_text())
        row = rows[0]
        sources = {s["id"] for s in json.loads((ROOT / "evidence/sources.json").read_text())}
        for changed in ({**row, "classification": "direct"},
                        {key: value for key, value in row.items() if key != "version_status"},
                        {**row, "source_ids": ["invented-source"]}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                validate_rows([changed, *rows[1:]], sources)

    def test_native_start_and_reference_have_no_legacy_setup(self):
        pages = [ROOT / "README.md", *(ROOT / "docs/start").glob("*.md"),
                 *(ROOT / "docs/reference" / name for name in OUTPUTS)]
        for page in pages:
            with self.subTest(page=page.name):
                text = page.read_text()
                self.assertNotIn("WSL", text)
                self.assertNotIn("/tmp/", text)
                self.assertNotIn("Generated from", text)
                self.assertNotIn("scripts.lab setup", text)

    def test_main_path_is_existing_repository_and_practice_is_optional(self):
        readme = (ROOT / "README.md").read_text()
        guide = (ROOT / "docs/start/use-copilot-in-your-repository.md").read_text()
        for heading in ("Get started in your repository", "Commands and muscle memory",
                        "Retain Claude configuration", "Daily workflows", "Model choices",
                        "Resources and troubleshooting", "Source integrations"):
            self.assertIn(heading, readme)
        self.assertIn("Optional practice", readme)
        self.assertIn("their own existing repository", readme)
        for command in ("git status --short", "git diff", "copilot --resume"):
            self.assertIn(command, guide)
        for text in ("practice.py", "sample-app", "python -", "python3 -"):
            self.assertNotIn(text, guide)
        self.assertIn("Start in [your own repository](../start/use-copilot-in-your-repository.md).",
                      render(json.loads(MATRIX.read_text()), "muscle-memory.md"))
