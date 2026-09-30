import io
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
import zipfile

from scripts.check_links import check, classify, reviewed
from scripts.package_plugin import archive, contents
from scripts.safety import json_load
from scripts.validate import ROOT, anchors, frontmatter, hook_configs, markdown, schema_validate, static_checks, yaml_load


class ValidationTests(unittest.TestCase):
    def test_yaml_frontmatter_real_parser_duplicates(self):
        self.assertEqual(yaml_load("name: test\ntools: [view, grep, glob]\n")["name"], "test")
        self.assertEqual(frontmatter('---\n{"name":"test"}\n---\n# Body\n')[0]["name"], "test")
        for value in ("name: test\nname: again", "thing: [", "x: &x [*x]", '{"name":1,"name":2}'):
            with self.assertRaises(ValueError):
                yaml_load(value)
        with self.assertRaises(ValueError):
            frontmatter("---\nname: test\n")

    def test_links_anchors_references_and_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.md"
            target.write_text("# Target\n\n## Same\n\n## Same\n")
            path = root / "index.md"
            path.write_text("# Index\n\n[ok](target.md#same-1)\n\n[link][ref]\n\n[ref]: target.md#target\n")
            markdown(path, root)
            for text in ("[bad](target.md#missing)\n", "[bad](missing.md)\n", "[bad](../escape.md)\n",
                          "[bad][missing]\n", "# Heading \n", "```python\npass\n",
                          "[" + "source:internal]\n", "[" + "claim:internal]\n"):
                path.write_text(text)
                with self.subTest(text=text), self.assertRaises(ValueError):
                    markdown(path, root)

    def test_plugin_real_schema_and_deterministic_archive(self):
        schema = json_load((ROOT / "schemas/plugin.schema.json").read_bytes())
        manifest = json_load((ROOT / "examples/plugin/plugin.json").read_bytes())
        schema_validate(manifest, schema)
        for broken in ({**manifest, "skills": "./skills"}, {**manifest, "name": "bad--name"},
                       {**manifest, "$schema": "https://wrong.invalid"}):
            with self.assertRaises(ValueError):
                schema_validate(broken, schema)
        self.assertEqual(archive(), archive())
        with zipfile.ZipFile(io.BytesIO(archive())) as bundle:
            self.assertEqual({name: bundle.read(name) for name in bundle.namelist()}, contents())
            self.assertEqual(len(bundle.namelist()), 4)
            self.assertIn("plugin.json", bundle.namelist())
            self.assertFalse(any("hooks" in name or "mcp" in name for name in bundle.namelist()))

    def test_banner_and_readme_opening(self):
        banner = ROOT / "assets/claude-code-to-github-copilot-banner.png"
        self.assertEqual(hashlib.sha256(banner.read_bytes()).hexdigest(),
                         "a2c13ff14d86c870436f2fc26747c8d63d685d10ec78248770b3e7189561649c")
        self.assertEqual((ROOT / "README.md").read_text(encoding="utf-8").splitlines()[:3], [
            "![Claude Code to GitHub Copilot banner with Copilot Octocat](assets/claude-code-to-github-copilot-banner.png)",
            "", "# Claude Code → GitHub Copilot"])

    def test_negative_config_and_evidence_contracts(self):
        for config in ({}, {"version": True, "hooks": {}}, {"version": 1, "hooks": {"preToolUse": {}}},
                       {"version": 1, "hooks": {"preToolUse": [{"type": "http"}]}}):
            with self.subTest(config=config), self.assertRaises(ValueError):
                hook_configs([config])
        schema = json_load((ROOT / "schemas/evidence.schema.json").read_bytes())
        for value in ([{"id": "has space"}], [{"id": "test", "status": "runtime-proven"}],
                      [{"id": "test", "preview": "yes"}], [{"id": "test", "secret": "CANARY"}]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                schema_validate(value, schema)

    def test_static_validator_detects_source_and_generated_drift(self):
        static_checks()
        from scripts.safety import read_regular

        def changed(path, *args, **kwargs):
            raw = read_regular(path, *args, **kwargs)
            if Path(path).name == "claims.json":
                claims = json.loads(raw)
                claims[0]["source_ids"] = ["missing-source"]
                return json.dumps(claims).encode()
            return raw

        with patch("scripts.validate.read_regular", side_effect=changed), self.assertRaisesRegex(ValueError, "^unknown evidence source$"):
            static_checks()
        with patch("scripts.validate.archive", side_effect=[b"first", b"second"]), self.assertRaisesRegex(ValueError, "^nondeterministic plugin$"):
            static_checks()

    def test_unlisted_example_activation_placeholder_rejected(self):
        from scripts.safety import read_regular
        from scripts.secret_gate import gate
        from scripts.validate import files

        example = ROOT / "examples/unlisted.json"

        def injected(path, *args, **kwargs):
            return b'{"path":"/REVIEW/unlisted"}' if Path(path) == example else read_regular(path, *args, **kwargs)

        with patch("scripts.validate.files", side_effect=lambda root: [*files(root), example]), \
                patch("scripts.validate.read_regular", side_effect=injected), \
                patch("scripts.validate.gate", side_effect=lambda paths: True if paths == [example] else gate(paths)), \
                self.assertRaisesRegex(ValueError, "^unreviewed activation placeholder$"):
            static_checks()

    def test_scenario_contract_rejects_missing_field(self):
        from scripts.safety import read_regular

        def missing_prompt(path, *args, **kwargs):
            raw = read_regular(path, *args, **kwargs)
            if Path(path).name == "A-explore.md":
                return raw.replace(b"**Prompt:**", b"**Question:**", 1)
            return raw

        with patch("scripts.validate.read_regular", side_effect=missing_prompt), self.assertRaisesRegex(
                ValueError, "^scenario contract missing: A-explore.md$"):
            static_checks()

    def test_network_classification_retry_exceptions(self):
        for code, expected in ((200, "ok"), (301, "moved-review"), (403, "auth-or-forbidden"),
                               (429, "rate-limited"), (503, "transient"), (404, "broken")):
            self.assertEqual(classify(code), expected)
        calls = []

        def request(*args, **kwargs):
            calls.append(1)
            raise HTTPError("https://example.invalid", 429, "CANARY", {}, None)

        result = check("https://example.invalid", request=request, sleep=lambda _: None)
        self.assertEqual(len(calls), 2)
        self.assertEqual(result["status"], "rate-limited")
        self.assertNotIn("CANARY", str(result))
        self.assertFalse(reviewed(result, "test", []))
        self.assertTrue(reviewed(result, "test", [{"source_id": "test", "status": "rate-limited",
            "reason": "Public endpoint rate limit reviewed", "reviewed": "2026-01-01", "expires": "2099-01-01"}]))
        self.assertFalse(reviewed(result, "test", [{"source_id": "test", "status": "rate-limited",
            "reason": "Expired", "reviewed": "2020-01-01", "expires": "2020-01-02"}]))
        with self.assertRaises(ValueError):
            check("https://user:secret@example.invalid")
