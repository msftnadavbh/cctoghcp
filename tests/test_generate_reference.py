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
