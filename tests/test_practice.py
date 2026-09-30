"""Portable-only suite: no POSIX runner, hooks, assistants, network or pip."""
import contextlib
import hashlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import practice
from test_acceptance import feature_source


class PracticeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)  # Test-owned, synthetic code only.
        self.base = Path(self.temp.name).resolve()
        self.lab = self.base / "practice space café 東京"
        self.canonical = practice.assets(True)
        self.digest = {name: hashlib.sha256(raw).hexdigest() for name, raw in self.canonical.items()}
        # Production retains scratch. Tests own and remove their synthetic trees.
        self.make_temp = tempfile.mkdtemp
        def scratch(*args, **kwargs):
            kwargs.setdefault("dir", self.base)
            return self.make_temp(*args, **kwargs)
        self.patcher = patch.object(practice.tempfile, "mkdtemp", side_effect=scratch)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def tearDown(self):
        self.assertEqual(self.digest, {name: hashlib.sha256(raw).hexdigest()
                                     for name, raw in practice.assets(True).items()})

    def check(self, exercise="validation"):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            passed = practice.check(self.lab, exercise)
        return passed, output.getvalue()

    def test_fixed_copy_configs_and_exact_mutation(self):
        practice.setup(self.lab, with_config=True)
        self.assertEqual(len(practice.CONFIG_ASSETS), 6)
        self.assertEqual(set(practice.tree(self.lab)), set(self.canonical))
        for name, data in self.canonical.items():
            wanted = data.replace(practice.GUARD, practice.BROKEN_GUARD, 1) if name == "src/catalog.py" else data
            self.assertEqual((self.lab / name).read_bytes(), wanted)
        for line in (self.lab / "CLAUDE.md").read_text(encoding="utf-8").splitlines():
            if line.startswith("@"):
                self.assertIn(line[1:], practice.CONFIG_ASSETS)
                self.assertTrue((self.lab / line[1:]).is_file())
        self.assertNotIn(b"settings.json", b"\n".join(name.encode() for name in practice.CONFIG_ASSETS))
        with patch.object(practice, "assets", return_value={"src/catalog.py": b"no guard"}):
            with self.assertRaisesRegex(ValueError, "exactly once"):
                practice.setup(self.base / "no mutation")
        self.assertFalse((self.base / "no mutation").exists())

    def test_no_overwrite_book_ancestor_traversal_or_missing_parent(self):
        practice.setup(self.lab, "baseline")
        self.assertEqual(set(practice.tree(self.lab)), set(practice.APP_FILES))
        for path in (self.lab, practice.ROOT, practice.ROOT.parent, practice.ROOT / "new-lab",
                     self.base / "missing" / "child", self.base / ".." / "escape"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                practice.setup(path)

    def test_book_alias_identity_refused(self):
        alias = self.base / "book alias"
        alias.mkdir()
        samefile = os.path.samefile
        def same_book(left, right):
            return (left == alias and right == practice.ROOT) or samefile(left, right)
        with patch.object(practice.os.path, "samefile", side_effect=same_book):
            for path in (alias, alias / "new lab"):
                with self.assertRaisesRegex(ValueError, "outside the book"):
                    practice.outside_book(path)
        def same_ancestor(left, right):
            return (left == alias and right == practice.ROOT.parent) or samefile(left, right)
        with patch.object(practice.os.path, "samefile", side_effect=same_ancestor):
            with self.assertRaisesRegex(ValueError, "outside the book"):
                practice.outside_book(alias)
        # Real case-alias check on case-insensitive filesystems, not a Linux claim.
        case_alias = practice.ROOT.with_name(practice.ROOT.name.swapcase())
        if case_alias.exists() and samefile(case_alias, practice.ROOT):
            with self.assertRaisesRegex(ValueError, "outside the book"):
                practice.outside_book(case_alias / "new lab")

    def test_version_guard_precedes_project_imports_simulated(self):
        result = subprocess.run([sys.executable, "-I", "-B", "-c",
                                 "import runpy, sys; sys.version_info = (3, 9); "
                                 "runpy.run_path(sys.argv[1], run_name='__main__')",
                                 str(practice.ROOT / "scripts/practice.py")],
                                capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"practice requires Python 3.12 or newer", result.stderr)
        self.assertNotIn(b"Traceback", result.stderr)

    def test_partial_copy_is_retained(self):
        original = Path.open
        def opening(path, *args, **kwargs):
            if path == self.lab / "tests/test_catalog.py" and args == ("xb",):
                raise OSError("synthetic write failure")
            return original(path, *args, **kwargs)
        with patch.object(Path, "open", opening), self.assertRaisesRegex(ValueError, "partial setup retained"):
            practice.setup(self.lab)
        self.assertTrue((self.lab / "src/catalog.py").is_file())
        with self.assertRaises(ValueError):
            practice.setup(self.lab)

    def test_windows_path_spelling_on_every_platform(self):
        for path in (r"C:\labs\space café", r"lab\child", "lab/child"):
            practice.windows_spelling(path)
        for path in (r"\\host\share\lab", r"\\?\C:\lab", r"\\.\C:\lab", r"C:lab", r"\lab", "/lab",
                     r"C:\lab:stream", "lab.", "lab ", "NUL", "COM1.txt", "COM¹.txt", "LPT³", "aux .txt",
                     "CONIN$", "CONOUT$.txt", "lab/../child", "lab//child", "lab/./child"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                practice.windows_spelling(path)

    def test_symlinks_rejected_at_leaf_ancestor_and_inside_tree(self):
        link = self.base / "link"
        target = self.base / "real"
        target.mkdir()
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError as error:
            if os.name == "nt" and error.winerror == 1314:
                self.skipTest("Windows symlink creation privilege unavailable")
            raise
        for path in (link, link / "new"):
            with self.assertRaises(ValueError):
                practice.setup(path)
        practice.setup(self.lab)
        (self.lab / "linked").symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            practice.tree(self.lab)

    @unittest.skipUnless(os.name == "nt", "native Windows junction test")
    def test_native_junction_rejected(self):
        target, link = self.base / "real", self.base / "junction"
        target.mkdir()
        subprocess.run([os.environ["COMSPEC"], "/d", "/c", "mklink", "/J", str(link), str(target)],
                       check=True, capture_output=True, timeout=5)
        self.addCleanup(link.rmdir)
        for path in (link, link / "child"):
            with self.assertRaises(ValueError):
                practice.setup(path)

    def test_baseline_broken_validation_fix_and_refactor(self):
        practice.setup(self.lab, "baseline", True)
        self.assertTrue(self.check("baseline")[0])
        catalog = self.lab / "src/catalog.py"
        catalog.write_bytes(catalog.read_bytes().replace(practice.GUARD, practice.BROKEN_GUARD))
        passed, output = self.check()
        self.assertFalse(passed)
        self.assertIn("Ran 3 tests", output)
        self.assertIn("boolean value accepted", output)
        catalog.write_bytes(self.canonical["src/catalog.py"])
        self.assertTrue(self.check()[0])
        self.assertTrue(self.check("refactor")[0])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertFalse(practice.diff(self.lab))
        self.assertIn("already fixed", output.getvalue())

    def test_feature_absent_then_fixture_passes_combined_filters(self):
        practice.setup(self.lab, "in-stock")
        self.assertFalse(self.check("in-stock")[0])
        catalog = self.lab / "src/catalog.py"
        source = feature_source(catalog.read_text(encoding="utf-8"))
        catalog.write_text(source, encoding="utf-8")
        self.assertTrue(self.check("in-stock")[0])
        # Broken only when query and stock are combined: the extra oracle case catches it.
        catalog.write_text(source.replace('if in_stock is None or p.in_stock is in_stock',
                                         'if query or in_stock is None or p.in_stock is in_stock'), encoding="utf-8")
        self.assertFalse(self.check("in-stock")[0])

    def test_fake_tests_cannot_bypass_oracle_checker_must_match(self):
        practice.setup(self.lab)
        (self.lab / "tests/test_catalog.py").write_text("import unittest\n", encoding="utf-8")
        passed, output = self.check()
        self.assertFalse(passed)
        self.assertIn("App tests: ok", output)
        self.assertIn("Independent acceptance failed", output)
        (self.lab / "scripts/check_lab.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "canonical checker"):
            self.check()

    def test_observer_rejects_no_result_malformed_timeout_and_large_output(self):
        practice.setup(self.lab, "baseline")
        oracle = practice.load_oracle()
        observer = practice._Observer(self.lab, self.base, oracle)
        catalog = self.lab / "src/catalog.py"
        for code, status in (("raise SystemExit(0)", "ok"), ("print('{'); raise SystemExit(0)", "ok"),
                             ("import time; time.sleep(30)", "timeout"),
                             ("print('x' * 100000); raise SystemExit(0)", "output-limit")):
            catalog.write_text(code, encoding="utf-8")
            oracle.TIMEOUT = 2 if status == "timeout" else 5
            result = observer([sys.executable, "-I", "-B", str(catalog)])
            self.assertEqual(result.status, status)
            self.assertLessEqual(len(result.stdout), practice.OUTPUT_LIMIT)
            observed_statuses = []
            def observe(argv, stdin=b""):
                result = observer(argv, stdin)
                observed_statuses.append(result.status)
                return result
            message = "observations missing or malformed" if status == "ok" else "probe process failed"
            with self.assertRaisesRegex(AssertionError, message):
                oracle.check(self.lab, "baseline", observe=observe)
            self.assertEqual(observed_statuses, [status])
        with self.assertRaises(ValueError):
            observer([sys.executable, "-c", "print('not allowed')"])
        with self.assertRaises(ValueError):
            observer([sys.executable, "-I", "-B", str(catalog)], b"x" * (practice.OUTPUT_LIMIT + 1))
        with patch.object(practice.subprocess, "Popen", side_effect=OSError):
            self.assertEqual(observer([sys.executable, "-I", "-B", str(catalog)]).status, "launch-error")

    def test_environment_is_minimal_home_fresh_and_artifacts_retained(self):
        practice.setup(self.lab, "baseline")
        oracle = practice.load_oracle()
        observer = practice._Observer(self.lab, self.base, oracle)
        real_popen = subprocess.Popen
        homes = []
        def launch(argv, **kwargs):
            env = kwargs["env"]
            home = Path(env["HOME"])
            homes.append(home)
            self.assertEqual(list(home.iterdir()), [])
            self.assertNotEqual(Path(kwargs["cwd"]), self.lab)
            self.assertEqual(set(env) - {"SystemRoot", "WINDIR"},
                             {"HOME", "USERPROFILE", "TMP", "TEMP", "TMPDIR", "LANG", "NO_COLOR"})
            return real_popen(argv, **kwargs)
        with patch.dict(os.environ, {"GITHUB_TOKEN": "synthetic-canary", "PYTHONPATH": str(self.lab)}), \
                patch.object(practice.subprocess, "Popen", side_effect=launch):
            oracle.check(self.lab, "baseline", observe=observer)
        self.assertEqual(len(homes), len(set(homes)))
        self.assertTrue(all((home.parent / "stdout.bin").exists() for home in homes))

    def test_diff_all_files_added_deleted_configs_and_bounds_never_executes(self):
        practice.setup(self.lab, "baseline", True)
        (self.lab / "tests/test_catalog.py").unlink()
        (self.lab / "CLAUDE.md").write_bytes(b"changed config\n")
        (self.lab / "added.py").write_bytes(b"raise RuntimeError('must never execute')\n")
        (self.lab / "invalid-utf8.bin").write_bytes(b"\xff\xfe")
        (self.lab / "null-byte.bin").write_bytes(b"hidden\x00payload")
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch.object(subprocess, "Popen", side_effect=AssertionError):
            self.assertTrue(practice.diff(self.lab))
        for text in ("added: added.py", "deleted: tests/test_catalog.py", "changed: CLAUDE.md"):
            self.assertIn(text, output.getvalue())
        self.assertEqual(output.getvalue().count("Binary content differs"), 2)
        self.assertNotIn("\ufffd", output.getvalue())
        self.assertNotIn("hidden", output.getvalue())
        with patch.object(practice, "TREE_LIMIT", 1), self.assertRaises(ValueError):
            practice.tree(self.lab)
        with patch.object(practice, "TOTAL_LIMIT", 1), self.assertRaises(ValueError):
            practice.tree(self.lab)
        (self.lab / "big").write_bytes(b"x" * (practice.LIMIT + 1))
        with self.assertRaises(ValueError):
            practice.tree(self.lab)

    def test_diff_displays_crlf_source_without_hiding_bare_carriage_returns(self):
        practice.setup(self.lab, "baseline", True)
        path = self.lab / "src/catalog.py"
        source = path.read_bytes().replace(b"\r\n", b"\n").replace(practice.GUARD, practice.BROKEN_GUARD)
        path.write_bytes(source.replace(b"\n", b"\r\n"))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertTrue(practice.diff(self.lab))
        self.assertIn(practice.BROKEN_GUARD.decode(), output.getvalue())
        self.assertNotIn("Binary content differs", output.getvalue())
        self.assertNotIn("\r", output.getvalue())

    def test_diff_escapes_invisible_filenames_and_omits_control_content(self):
        practice.setup(self.lab, "baseline", True)
        (self.lab / "src/catalog.py").write_bytes("line\rhidden\u202e".encode("utf-8"))
        (self.lab / "invisible\u202e.py").write_text("safe\n", encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertTrue(practice.diff(self.lab))
        text = output.getvalue()
        self.assertIn("changed: src/catalog.py", text)
        self.assertIn("added: invisible\\u202e.py", text)
        self.assertIn("Binary content differs", text)
        self.assertNotIn("\r", text)
        self.assertNotIn("\u202e", text)
        self.assertNotIn("hidden", text)

    def test_exact_first_lesson_cli_outside_book(self):
        command = [sys.executable, "-I", "-B", str(practice.ROOT / "scripts/practice.py")]
        env = dict(os.environ, **{key: str(self.base) for key in ("TMP", "TEMP", "TMPDIR")})
        def run(*args):
            result = subprocess.run(command + list(args), cwd=self.base, env=env, capture_output=True, timeout=30)
            if args[0] == "check":
                paths = [Path(line.split(": ", 1)[1]) for line in result.stdout.decode("utf-8").splitlines()
                         if line.startswith("Check artifacts retained: ")]
                self.assertEqual(len(paths), 1, result.stdout + result.stderr)
                self.assertTrue(paths[0].is_relative_to(self.base))
                self.assertTrue(paths[0].is_dir())
            return result
        result = run("setup", str(self.lab), "--exercise", "validation", "--with-config")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = run("check", str(self.lab), "--exercise", "validation")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(b"boolean value accepted", result.stdout)
        result = run("diff", str(self.lab))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(practice.BROKEN_GUARD, result.stdout)
        (self.lab / "src/catalog.py").write_bytes(self.canonical["src/catalog.py"])
        result = run("check", str(self.lab), "--exercise", "validation")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
