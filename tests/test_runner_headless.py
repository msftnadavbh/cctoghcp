import argparse
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from scripts.headless import command, consume, execute
from scripts import lab
from scripts.runner import environment, run, save

ROOT = Path(__file__).resolve().parents[1]
GOOD = b'{"type":"system"}\n{"type":"result","is_error":false,"result":"Reviewed synthetic catalog."}\n'


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="runner space ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = environment(self.root)

    def python(self, source, **kwargs):
        return run([sys.executable, "-c", source], cwd=self.root, env=self.env, **kwargs)

    def test_capture_private_exit_missing(self):
        result = self.python("import sys; print('out'); print('err',file=sys.stderr)")
        self.assertEqual((result.status, result.stdout, result.stderr), ("ok", b"out\n", b"err\n"))
        save(result, self.root / "private output")
        self.assertEqual((self.root / "private output/stdout.bin").stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.python("raise SystemExit(7)").status, "nonzero-exit")
        self.assertEqual(run(["/nonexistent-checkpoint-exe"], cwd=self.root, env=self.env).status, "missing-executable")

    def test_timeout_and_output_bounds(self):
        self.assertEqual(self.python("import time; time.sleep(20)", timeout=0.1).status, "timeout")
        result = self.python("import sys; sys.stdout.write('x'*100000)", limit=1234)
        self.assertEqual((result.status, len(result.stdout)), ("output-limit", 1234))
        result = self.python("import sys; sys.stderr.write('x'*100000)", limit=1234)
        self.assertEqual((result.status, len(result.stderr)), ("output-limit", 1234))
        result = self.python("import sys; print(len(sys.stdin.buffer.read()))", stdin=b"x" * 100000)
        self.assertEqual(result.stdout, b"100000\n")

    def test_kills_descendant_even_after_parent_exit(self):
        source = """import os, signal, time
pid = os.fork()
if pid == 0:
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    time.sleep(20)
else:
    print(pid, flush=True)
    os._exit(0)
"""
        result = self.python(source, timeout=0.2)
        self.assertEqual(result.status, "timeout")
        pid = int(result.stdout)
        try:
            for _ in range(50):
                status = Path(f"/proc/{pid}/stat")
                if not status.exists() or status.read_text().split()[2] == "Z":
                    break
                time.sleep(0.02)
            else:
                self.fail("descendant still running")
        finally:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

    def test_environment_and_argument_boundary(self):
        for extra in ({"BASH_ENV": "evil"}, {"COPILOT_GITHUB_TOKEN": "bad\nvalue"}, {"SECRET-CANARY": "value"}):
            with self.assertRaises(ValueError) as caught:
                environment(self.root, extra)
            self.assertNotIn("CANARY", str(caught.exception))
        self.assertNotIn("GITHUB_TOKEN", self.env)
        with self.assertRaises(ValueError):
            run("shell string", cwd=self.root, env=self.env)
        result = run([sys.executable, "-c", "import sys; print(sys.argv[1])", "a; $(false) b"],
                     cwd=self.root, env=self.env)
        self.assertEqual(result.stdout, b"a; $(false) b\n")
        for timeout in (float("nan"), float("inf"), 0, -1):
            with self.assertRaises(ValueError):
                self.python("pass", timeout=timeout)


class HeadlessTests(unittest.TestCase):
    def test_jsonl_contract(self):
        self.assertEqual(len(consume(GOOD)), 2)
        self.assertEqual(consume(b'{"type":"unknown.future","data":{}}\n')[0]["type"], "unknown.future")
        self.assertTrue(consume(b'{"type":"result","is_error":true}\n')[0]["is_error"])
        for raw in (b"", b"not-json\n", b"{}\n", GOOD.rstrip(),
                    GOOD + b"{}\n",
                    b'{"type":"result","type":"system"}\n'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                consume(raw)

    def test_permissions_not_widened(self):
        for mode in ("repo-summary", "diff-review", "test-fix", "gitlab-log-summary"):
            args = command("copilot", mode)
            self.assertIn("--no-remote", args)
            self.assertIn("--disallow-temp-dir", args)
            self.assertTrue(any(a.startswith("--available-tools=") for a in args))
            self.assertFalse(any(a in args for a in ("--allow-all", "--allow-all-tools", "--yolo")))
            self.assertNotIn("--allow-tool=shell", args)

    @patch.dict(os.environ, {"COPILOT_GITHUB_TOKEN": "synthetic-unit-value"})
    def test_fake_executable_and_postconditions(self):
        with tempfile.TemporaryDirectory(prefix="headless space ") as directory:
            root = Path(directory)
            prompt = root / "reviewed prompt.txt"
            prompt.write_text("Review the synthetic lab.")
            fake = root / "fake copilot"
            fake.write_text("#!" + sys.executable + "\nimport sys\nsys.stdout.buffer.write(" + repr(GOOD) + ")\n")
            fake.chmod(0o700)
            home = root / "credential-home"
            home.mkdir(mode=0o700)
            record = lab.setup(root / "bug lab", root / "state", "validation")
            args = argparse.Namespace(repo=Path(record["path"]), prompt_file=prompt,
                executable=str(fake), mode="repo-summary", execute=False, consent_paid=False,
                reviewed_workspace=False, home=home, output=root / "output", timeout=2,
                credential_env="COPILOT_GITHUB_TOKEN")
            self.assertEqual(execute(args)["status"], "dry-run")
            self.assertFalse(args.output.exists())
            args.execute = True
            with self.assertRaises(ValueError):
                execute(args)
            args.consent_paid = args.reviewed_workspace = True
            from scripts.runner import run as actual_run
            def checked_run(*argv, **kwargs):
                self.assertTrue(args.output.is_dir())
                self.assertEqual(args.output.stat().st_mode & 0o777, 0o700)
                return actual_run(*argv, **kwargs)
            with patch("scripts.headless.run", side_effect=checked_run):
                self.assertEqual(execute(args)["status"], "report-unverified")
            with patch("scripts.headless.run") as runner, self.assertRaises(ValueError):
                execute(args)
            runner.assert_not_called()
            args.repo, args.mode, args.output = Path(record["path"]), "test-fix", root / "output2"
            sentinel = root / "executed"
            (args.repo / "tests/test_catalog.py").write_text(f"from pathlib import Path\nPath({str(sentinel)!r}).touch()\n")
            self.assertEqual(execute(args)["status"], "validation-pending")
            self.assertFalse(sentinel.exists())
            (args.repo / "src/catalog.py").write_text("syntax broken !")
            args.output = root / "static failure"
            result = execute(args)
            self.assertEqual((result["status"], result["process_exit"]), ("static-check-failed", 0))
            args.mode, args.output = "repo-summary", root / "output3"
            fake.write_text("#!" + sys.executable + "\nprint('not json')\n")
            self.assertEqual(execute(args)["status"], "invalid-jsonl")
            args.mode = "gitlab-log-summary"
            with self.assertRaises(ValueError):
                execute(args)

    def test_preflight_known_config_refusal_and_paths(self):
        from scripts.preflight import ACTIVE, executable_path, preflight
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, home, output = root / "lab", root / "home", root / "output"
            repo.mkdir()
            home.mkdir(mode=0o700)
            preflight(repo, home, output)
            for base, name in ((repo, ".github/hooks"), (repo, ".vscode/mcp.json"), (root, ".claude/settings.json"),
                               (home, ".copilot/settings.json"), (home, ".copilot/installed-plugins"),
                               (home, ".copilot/extensions"), (home, ".copilot/lsp.json")):
                path = base / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("malformed CANARY permissions")
                with self.assertRaisesRegex(ValueError, "configuration refused"):
                    preflight(repo, home, output)
                path.unlink()
                while path.parent not in (repo, home, root):
                    path = path.parent
                    path.rmdir()
            with patch("scripts.preflight.POLICY", root / "policy"):
                (root / "policy").mkdir()
                with self.assertRaisesRegex(ValueError, "machine policy"):
                    preflight(repo, home, output)
            for selected_home, selected_output in ((repo, output), (home, repo / "output"), (home, home / "output")):
                with self.assertRaisesRegex(ValueError, "must be separate"):
                    preflight(repo, selected_home, selected_output)
            with self.assertRaises(ValueError):
                executable_path("./copilot")
            self.assertTrue(Path(executable_path(sys.executable)).is_absolute())
            home.chmod(0o755)
            with self.assertRaisesRegex(ValueError, "fresh empty owned private"):
                preflight(repo, home, output)
            home.chmod(0o700)
            (home / "unreviewed").touch()
            with self.assertRaisesRegex(ValueError, "fresh empty owned private"):
                preflight(repo, home, output)

    def test_selected_credential_only_stdin_and_private_capture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, home = root / "lab", root / "home"
            repo.mkdir()
            home.mkdir(mode=0o700)
            prompt = root / "prompt.txt"
            prompt.write_text("SYNTHETIC REVIEWED PROMPT")
            fake = root / "fake cli"
            fake.write_text("#!" + sys.executable + "\n" + '''import os, sys, json
assert 'GH_TOKEN' not in os.environ and 'GITHUB_TOKEN' not in os.environ
assert 'COPILOT_PROVIDER_API_KEY' not in os.environ
assert '--secret-env-vars=COPILOT_GITHUB_TOKEN' in sys.argv
assert 'SYNTHETIC REVIEWED PROMPT' not in str(sys.argv)
assert sys.stdin.read() == 'SYNTHETIC REVIEWED PROMPT'
value = os.environ['COPILOT_GITHUB_TOKEN']
assert value not in str(sys.argv)
print(json.dumps({'type':'synthetic.observation','content':value}))
print(value, file=sys.stderr)
open(os.path.join(os.environ['HOME'], 'cli-created-config'), 'w').close()
''')
            fake.chmod(0o700)
            args = argparse.Namespace(repo=repo, home=home, output=root / "out", prompt_file=prompt,
                executable=str(fake), mode="repo-summary", execute=False, consent_paid=True,
                reviewed_workspace=True, timeout=2, credential_env=None)
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(execute(args)["status"], "dry-run")
                args.execute = True
                with patch("scripts.headless.run") as runner, self.assertRaisesRegex(ValueError, "credential selection"):
                    execute(args)
                runner.assert_not_called()
                self.assertFalse(args.output.exists())
                args.credential_env = "COPILOT_GITHUB_TOKEN"
                for value in (None, "", "  ", "bad\nvalue", "bad\rvalue"):
                    with patch.dict(os.environ, {} if value is None else {"COPILOT_GITHUB_TOKEN": value}, clear=True):
                        with self.assertRaisesRegex(ValueError, "credential missing or invalid"):
                            execute(args)
                        self.assertFalse(args.output.exists())
            canary = "SYNTHETIC-CREDENTIAL-CANARY"
            with patch("scripts.headless.os.environ.get", return_value="bad\0value"), self.assertRaisesRegex(ValueError, "credential missing or invalid"):
                execute(args)
            self.assertFalse(args.output.exists())
            cli = [sys.executable, "-B", "-m", "scripts.headless", "repo-summary", "--repo", str(repo),
                   "--prompt-file", str(prompt), "--execute", "--consent-paid", "--reviewed-workspace",
                   "--credential-env", "COPILOT_GITHUB_TOKEN", "--home", str(home), "--output", str(args.output)]
            refused = run(cli, cwd=ROOT, env=environment(root))
            self.assertEqual(refused.returncode, 2)
            self.assertIn(b"selected credential", refused.stderr)
            self.assertFalse(args.output.exists())
            with patch.dict(os.environ, {"COPILOT_GITHUB_TOKEN": canary, "GH_TOKEN": "other", "GITHUB_TOKEN": "other",
                                         "COPILOT_PROVIDER_API_KEY": "other"}):
                report = execute(args)
                self.assertEqual(report["status"], "report-unverified")
                self.assertNotIn(canary, json.dumps(report))
                self.assertIn(canary.encode(), (args.output / "stdout.bin").read_bytes())
                self.assertEqual((args.output / "stderr.bin").stat().st_mode & 0o777, 0o600)
                args.output = root / "second-output"
                with self.assertRaisesRegex(ValueError, "fresh empty owned private"):
                    execute(args)
                self.assertFalse(args.output.exists())
