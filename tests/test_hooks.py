import json
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.hook_handler import event_log, handle, normalize
from scripts.lab import ROOT, setup
from scripts.runner import Result, environment, run
from scripts.safety import LIMIT
from scripts.validate import hook_configs


class HookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hook lab space ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.lab = self.root / "sample lab"
        setup(self.lab, self.root / "state")

    def payload(self, tool="edit", args=None, compatible=False):
        args = args if args is not None else {"path": "src/catalog.py"}
        if compatible:
            return json.dumps({"hook_event_name": "PreToolUse", "cwd": str(self.lab),
                               "tool_name": tool, "tool_input": args}).encode()
        return json.dumps({"cwd": str(self.lab), "toolName": tool, "toolArgs": args}).encode()

    def test_valid_native_object_string_compatible_neutral(self):
        for raw in (self.payload(), self.payload(args='{"path":"src/catalog.py"}'),
                    self.payload("Edit", {"file_path": "src/catalog.py"}, True), self.payload("view")):
            self.assertEqual(handle(raw, "pre", self.lab), ({}, "neutral"))

    def test_denied_and_malformed_matrix(self):
        cases = [b"", b"[]", b"{}", b"{", b"x" * (LIMIT + 1),
                 b'{"toolName":"edit","toolName":"view"}',
                 self.payload(args='{"path":"src/a.py","path":"src/b.py"}'),
                 self.payload(args={}), self.payload(args={"path": "../escape.py"}),
                 self.payload(args={"path": "tests/test_catalog.py"}),
                 self.payload(args={"path": "/tmp/escape.py"}),
                 self.payload(args={"path": "src/a.py", "file_path": "src/a.py"}),
                 self.payload("bash", {"command": "rm -rf /"}),
                 self.payload("apply_patch", {"patch": "anything"}),
                 self.payload("unknown"), self.payload(args={"path": "src/a.py", "content": "token=" + "CANARY"}),
                 json.dumps({"cwd": str(self.lab), "toolName": "edit", "toolArgs": {}, "tool_input": {}}).encode()]
        for raw in cases:
            with self.subTest(raw=raw[:100]), self.assertRaises((ValueError, OSError)):
                handle(raw, "pre", self.lab)
        (self.lab / "src/link.py").symlink_to(self.root / "outside.py")
        with self.assertRaises(ValueError):
            handle(self.payload(args={"path": "src/link.py"}), "pre", self.lab)

    def test_post_static_never_executes_nested_code_or_tests(self):
        target = self.lab / "src/nested space/new.py"
        target.parent.mkdir()
        sentinel = self.root / "EXECUTED"
        code = f"from pathlib import Path\nPath({str(sentinel)!r}).touch()\n"
        target.write_text(code)
        (self.lab / "tests/test_catalog.py").write_text(code)
        for alias in ("Write", "Edit"):
            raw = json.loads(self.payload(alias, {"file_path": "src/nested space/new.py"}, True))
            raw["hook_event_name"] = "PostToolUse"
            self.assertEqual(handle(json.dumps(raw).encode(), "post", self.lab)[1], "static-check-passed")
        self.assertFalse(sentinel.exists())
        self.assertEqual(handle(self.payload("Read"), "post", self.lab), ({}, "neutral"))
        for code in ("syntax broken !", "token=" + "'CANARY'"):
            target.write_text(code)
            with self.assertRaises(ValueError):
                handle(self.payload(args={"path": "src/nested space/new.py"}), "post", self.lab)

    def test_post_exit_zero_malformed_log_failure_and_untrusted_cwd(self):
        (self.lab / "scripts").mkdir(exist_ok=True)
        (self.lab / "scripts/__init__.py").write_text("raise RuntimeError('UNTRUSTED IMPORT')")
        for raw in (b"malformed CANARY", self.payload()):
            result = run([sys.executable, "-I", "-B", str(ROOT / "scripts/trusted_launcher.py"),
                          "hook", "post", "--lab", str(self.lab), "--event-log", str(self.lab)],
                         cwd=self.lab, env=environment(self.root), stdin=raw)
            self.assertEqual(result.returncode, 0)
            self.assertIn("additionalContext", json.loads(result.stdout))
            self.assertNotIn(b"CANARY", result.stdout + result.stderr)
            self.assertNotIn(b"UNTRUSTED", result.stdout + result.stderr)
        (self.lab / "src/catalog.py").write_text("syntax broken !")
        result = run([sys.executable, "-I", "-B", str(ROOT / "scripts/trusted_launcher.py"),
                      "hook", "post", "--lab", str(self.lab)],
                     cwd=self.lab, env=environment(self.root), stdin=self.payload())
        self.assertEqual(result.returncode, 0)
        self.assertIn("Static check failed", json.loads(result.stdout)["additionalContext"])

    def test_compatible_event_and_cwd_required(self):
        value = json.loads(self.payload("Edit", compatible=True))
        for field in ("hook_event_name", "cwd", "tool_name", "tool_input"):
            changed = dict(value)
            del changed[field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                normalize(json.dumps(changed).encode(), "pre")
        value["hook_event_name"] = "PostToolUse"
        with self.assertRaises(ValueError):
            normalize(json.dumps(value).encode(), "pre")

    def test_command_nonzero_sanitized_and_enum_log(self):
        canary = b"SECRET-CANARY-DO-NOT-ECHO"
        result = run([sys.executable, "-B", "-m", "scripts.hook_handler", "pre", "--lab", str(self.lab)],
                     cwd=ROOT, env=environment(self.root), stdin=canary)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["permissionDecision"], "deny")
        self.assertNotIn(canary, result.stdout + result.stderr)
        log = self.root / "event log.jsonl"
        event_log(log, "pre", "denied")
        self.assertEqual(json.loads(log.read_text()), {"event": "pre", "outcome": "denied"})
        with self.assertRaises(ValueError):
            event_log(log, "pre", canary.decode())

    def test_duplicate_registration_rejected(self):
        native = json.loads((ROOT / "examples/hooks/native.json").read_text())
        shared = json.loads((ROOT / "examples/hooks/shared-settings.json").read_text())
        hook_configs([native])
        hook_configs([shared])
        with self.assertRaises(ValueError):
            hook_configs([native, shared])
        with self.assertRaises(ValueError):
            hook_configs([native, native])

    def test_event_mode_binding_and_no_suffixes(self):
        native = json.loads((ROOT / "examples/hooks/native.json").read_text())
        shared = json.loads((ROOT / "examples/hooks/shared-settings.json").read_text())
        for event, mode in (("preToolUse", "post"), ("postToolUse", "pre")):
            changed = copy.deepcopy(native)
            changed["hooks"][event][0]["args"][4] = mode
            with self.assertRaisesRegex(ValueError, "native hook contract"):
                hook_configs([changed])
        changed = copy.deepcopy(native)
        changed["hooks"]["preToolUse"][0]["args"].append("--arbitrary")
        with self.assertRaisesRegex(ValueError, "native hook contract"):
            hook_configs([changed])
        for event, original, wrong in (("PreToolUse", "pre", "post"), ("PostToolUse", "post", "pre")):
            changed = copy.deepcopy(shared)
            hook = changed["hooks"][event][0]["hooks"][0]
            hook["command"] = hook["command"].replace(f"hook {original} ", f"hook {wrong} ")
            with self.assertRaisesRegex(ValueError, "shared trusted launcher contract"):
                hook_configs([changed])
        for suffix in ("; true", " --arbitrary", " && /bin/true"):
            changed = copy.deepcopy(shared)
            changed["hooks"]["PreToolUse"][0]["hooks"][0]["command"] += suffix
            with self.assertRaisesRegex(ValueError, "shared trusted launcher contract"):
                hook_configs([changed])

    def test_pre_launcher_from_poisoned_cwd_still_denies(self):
        (self.lab / "scripts/__init__.py").write_text("raise RuntimeError('POISONED')")
        result = run([sys.executable, "-I", "-B", str(ROOT / "scripts/trusted_launcher.py"),
                      "hook", "pre", "--lab", str(self.lab)],
                     cwd=self.lab, env=environment(self.root), stdin=self.payload("bash"))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["permissionDecision"], "deny")
        self.assertNotIn(b"POISONED", result.stdout + result.stderr)
