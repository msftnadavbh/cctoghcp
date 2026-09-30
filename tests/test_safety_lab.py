import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import lab
from scripts.inventory import inventory
from scripts.safety import LIMIT, has_secret, json_load, private_write, read_regular, sanitized_ci
from scripts.secret_gate import gate


class SafetyTests(unittest.TestCase):
    def test_jsonc_inventory_is_unparsed_and_value_free(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".vscode").mkdir()
            (root / ".vscode/mcp.jsonc").write_text('// CANARY\n{"secret":"CANARY",}')
            text = json.dumps(inventory(root))
            self.assertIn("found-unparsed-jsonc", text)
            self.assertNotIn("CANARY", text)

    def test_json_boundary(self):
        for raw in (b'{"a":1,"a":2}', b'{"x":{"a":1,"a":2}}', b"NaN", b"Infinity", b"[", b"\xff", b" " * (LIMIT + 1)):
            with self.subTest(raw=raw[:30]), self.assertRaises(ValueError):
                json_load(raw)

    def test_regular_private_symlink_fifo(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "private file"
            private_write(path, b"data")
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(read_regular(path), b"data")
            with self.assertRaises(FileExistsError):
                private_write(path, b"replace")
            (root / "link").symlink_to(path)
            with self.assertRaises(ValueError):
                read_regular(root / "link")
            os.mkfifo(root / "fifo")
            with self.assertRaises(ValueError):
                read_regular(root / "fifo")
            (root / "dirlink").symlink_to(root, target_is_directory=True)
            with self.assertRaises(ValueError):
                read_regular(root / "dirlink/../private file")

    def test_inventory_never_leaks(self):
        canary = "SECRET-CANARY-unknown-key-url-value"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".claude").mkdir()
            path = root / ".claude/settings.json"
            path.write_text(json.dumps({canary: canary, "env": {canary: canary}, "mcpServers": {
                canary: {"url": "https://" + canary, "headers": {canary: canary}}}}))
            result = inventory(root)
            text = json.dumps(result)
            self.assertNotIn(canary, text)
            self.assertIn("mcpServers", text)
            path.write_text('{"broken":"' + canary)
            self.assertNotIn(canary, json.dumps(inventory(root)))
            path.unlink()
            path.symlink_to(root / canary)
            self.assertNotIn(canary, json.dumps(inventory(root)))
            path.unlink()
            os.mkfifo(path)
            self.assertIn("skipped-special", json.dumps(inventory(root)))

    def test_lossy_sanitization(self):
        raw = b"FAIL: test_unknown\nsecret=CANARY https://private.invalid CANARY\nUNKNOWN-CANARY\n"
        self.assertTrue(has_secret(raw))
        clean = sanitized_ci(raw)
        self.assertNotIn(b"CANARY", clean)
        self.assertNotIn(b"https", clean)
        self.assertTrue(json_load(clean)["failure_observed"])

    def test_independent_secret_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.txt"
            path.write_text("synthetic safe content\n")
            self.assertTrue(gate([path]))
            path.write_text("token=" + "SYNTHETIC-CANARY\n")
            self.assertFalse(gate([path]))


class LabTests(unittest.TestCase):
    def test_config_is_exact_allowlist_with_import_closure(self):
        record = lab.setup(self.dest, self.state, with_config=True)
        self.assertTrue(record["with_config"])
        expected = set(lab.CONFIG_ASSETS) | {".checkpoint-owner", "src/catalog.py", "tests/test_catalog.py", "scripts/check_lab.py"}
        self.assertEqual({p.relative_to(self.dest).as_posix() for p in self.dest.rglob("*") if p.is_file()}, expected)
        for target, origin in lab.CONFIG_ASSETS.items():
            self.assertEqual((self.dest / target).read_bytes(), (lab.ROOT / origin).read_bytes())
        for line in (self.dest / "CLAUDE.md").read_text().splitlines():
            if line.startswith("@"):
                self.assertIn(line[1:], lab.CONFIG_ASSETS)
                self.assertTrue((self.dest / line[1:]).is_file())
        lab.cleanup(record["id"], self.state)
        record = lab.setup(self.dest, self.state)
        self.assertFalse(record["with_config"])
        self.assertFalse((self.dest / "CLAUDE.md").exists())
        self.assertFalse((self.dest / ".claude").exists())

    def test_config_partial_copy_cleanup(self):
        original = lab.private_write
        def failing(path, data):
            if Path(path) == self.dest / "guidance/shared.md":
                raise OSError("synthetic copy failure")
            return original(path, data)
        with patch("scripts.lab.private_write", side_effect=failing), self.assertRaises(OSError):
            lab.setup(self.dest, self.state, with_config=True)
        record = json.loads(next(self.state.glob("*.json")).read_text())
        self.assertEqual(self.dest.stat().st_mode & 0o777, 0o700)
        lab.cleanup(record["id"], self.state)
        self.assertFalse(self.dest.exists())

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="lab test ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = self.root / "ownership"
        self.dest = self.root / "owned lab"

    def test_roundtrip_spaces_no_remotes(self):
        record = lab.setup(self.dest, self.state)
        self.assertTrue((self.dest / "src/catalog.py").is_file())
        self.assertFalse((self.dest / ".git").exists())
        self.assertFalse((self.dest / "expected-results").exists())
        lab.cleanup(record["id"], self.state)
        self.assertFalse(self.dest.exists())
        self.assertFalse((self.state / (record["id"] + ".json")).exists())

    def test_baseline_and_introduced_bug(self):
        spec = importlib.util.spec_from_file_location("oracle", lab.ROOT / "labs/expected-results/acceptance.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.check(lab.ROOT / "labs/sample-app", "baseline")
        record = lab.setup(self.dest, self.state, "validation")
        with self.assertRaises(AssertionError):
            module.check(self.dest, "validation")
        with self.assertRaises(AssertionError):
            module.check(lab.ROOT / "labs/sample-app", "in-stock")
        lab.cleanup(record["id"], self.state)

    def test_nonempty_symlink_and_bad_paths(self):
        self.dest.mkdir()
        (self.dest / "keep").write_text("keep")
        with self.assertRaises(ValueError):
            lab.setup(self.dest, self.state)
        self.assertEqual((self.dest / "keep").read_text(), "keep")
        link = self.root / "link"
        link.symlink_to(self.dest, target_is_directory=True)
        with self.assertRaises(ValueError):
            lab.setup(link, self.state)
        for ident in ("../escape", "/", "", "a" * 31, "-rf"):
            with self.assertRaises(ValueError):
                lab.cleanup(ident, self.state)
        with self.assertRaises(ValueError):
            lab.setup(lab.ROOT, self.state)
        with self.assertRaises(ValueError):
            lab.setup(self.root / "new", self.root / "new/state")

    def test_cleanup_identity_symlink_mount(self):
        record = lab.setup(self.dest, self.state)
        (self.dest / "unsafe").symlink_to(self.root)
        with self.assertRaises(ValueError):
            lab.cleanup(record["id"], self.state)
        (self.dest / "unsafe").unlink()
        with patch("scripts.lab.os.path.ismount", return_value=True), self.assertRaises(ValueError):
            lab.cleanup(record["id"], self.state)
        original = self.root / "original"
        self.dest.rename(original)
        self.dest.mkdir()
        with self.assertRaises(ValueError):
            lab.cleanup(record["id"], self.state)
        self.assertTrue(original.exists())

    def test_private_ownership_state_and_parent_traversal(self):
        self.state.mkdir(mode=0o755)
        with self.assertRaises(ValueError):
            lab.setup(self.dest, self.state)
        self.state.chmod(0o700)
        with self.assertRaises(ValueError):
            lab.setup(self.root / "child/../lab", self.state)
        self.assertFalse(self.dest.exists())

    def test_partial_copy_owned_private_and_missing_marker(self):
        with patch("scripts.lab.shutil.copytree", side_effect=OSError("copy failed")):
            with self.assertRaises(OSError):
                lab.setup(self.dest, self.state)
        self.assertEqual(self.dest.stat().st_mode & 0o777, 0o700)
        record = json.loads(next(self.state.glob("*.json")).read_text())
        marker = self.dest / ".checkpoint-owner"
        marker.unlink()
        with self.assertRaises(FileNotFoundError):
            lab.cleanup(record["id"], self.state)
        marker.write_text("wrong-marker")
        with self.assertRaisesRegex(ValueError, "marker mismatch"):
            lab.cleanup(record["id"], self.state)
        marker.write_text(record["id"])
        lab.cleanup(record["id"], self.state)
        self.dest.mkdir()
        with self.assertRaisesRegex(ValueError, "must not exist"):
            lab.setup(self.dest, self.state)
        missing = self.root / "missing state"
        with self.assertRaises(FileNotFoundError):
            lab.cleanup("a" * 32, missing)
        self.assertFalse(missing.exists())
