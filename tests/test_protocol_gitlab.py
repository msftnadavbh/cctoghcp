import json
import io
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from scripts.gitlab import fetch, plan
from scripts.mcp_server import Server, VERSION, main


class ProtocolTests(unittest.TestCase):
    def request(self, server, method, params=None, ident=1):
        message = {"jsonrpc": "2.0", "id": ident, "method": method}
        if params is not None:
            message["params"] = params
        return server.receive(json.dumps(message).encode())

    def test_handshake_list_call(self):
        server = Server()
        self.assertIn("error", self.request(server, "tools/list"))
        result = self.request(server, "initialize", {"protocolVersion": "older", "capabilities": {},
                                                     "clientInfo": {"name": "unit-test", "version": "1"}})
        self.assertEqual(result["result"]["protocolVersion"], VERSION)
        self.assertIsNone(server.receive(b'{"jsonrpc":"2.0","method":"notifications/initialized"}'))
        tool = self.request(server, "tools/list")["result"]["tools"][0]
        result = self.request(server, "tools/call", {"name": tool["name"], "arguments": {}})
        self.assertIn("4 products", result["result"]["content"][0]["text"])
        self.assertIn("error", self.request(server, "tools/call", {"name": tool["name"], "arguments": {"path": "secret"}}))
        self.assertEqual(self.request(server, "unknown")["error"]["code"], -32601)

    def test_malformed_no_input_reflection(self):
        server = Server()
        for raw in (b"CANARY", b"[]", b'{"jsonrpc":"2.0","id":true,"method":"ping"}',
                    b'{"jsonrpc":"2.0","id":1,"id":2,"method":"ping"}'):
            response = server.receive(raw)
            self.assertIn("error", response)
            self.assertNotIn("CANARY", json.dumps(response))

    def test_protocol_framing_in_process_only(self):
        payload = b'{"jsonrpc":"2.0","id":1,"method":"ping"}\n'
        output = io.StringIO()
        with patch("scripts.mcp_server.sys.stdin", SimpleNamespace(buffer=io.BytesIO(payload))), patch("scripts.mcp_server.sys.stdout", output):
            self.assertEqual(main(), 0)
        self.assertEqual(json.loads(output.getvalue()), {"jsonrpc": "2.0", "id": 1, "result": {}})


class GitLabTests(unittest.TestCase):
    def test_explicit_ids_and_no_write(self):
        result = plan("group/project", 3, 5, "gitlab.example.com")
        for key in ("pipeline", "job", "trace"):
            self.assertEqual(result[key][-2:], ["--method", "GET"])
        self.assertIn("--draft", result["human_only_publish_argv"])
        for project in ("-bad/project", "../project", "https://secret.invalid/p", "group/project;whoami"):
            with self.assertRaises(ValueError):
                plan(project, 3, 5, "gitlab.example.com")
        for number in (True, 0, -1, "3"):
            with self.assertRaises(ValueError):
                plan("group/project", number, 5, "gitlab.example.com")
        for host in ("https://gitlab.com", "-bad", "user@host", "host/path", "host:443"):
            with self.assertRaises(ValueError):
                plan("group/project", 3, 5, host)

    def test_fake_glab_sanitizes_and_checks_pipeline(self):
        with tempfile.TemporaryDirectory(prefix="glab space ") as directory:
            root = Path(directory)
            fake = root / "fake glab"
            source = """import sys, json, os
assert sys.argv[-2:] == ['--method', 'GET']
assert sys.argv[3:5] == ['--hostname', 'gitlab.example.com']
assert os.getcwd() != os.environ['HOME']
path = sys.argv[2]
if path.endswith('/trace'):
    print('FAIL: synthetic test\\nunknown CANARY token=CANARY')
elif '/jobs/' in path:
    print(json.dumps({'id':5,'pipeline':{'id':3}}))
else:
    print(json.dumps({'id':3}))
"""
            fake.write_text("#!" + sys.executable + "\n" + source)
            fake.chmod(0o700)
            result = fetch(fake, "group/project", 3, 5, root, "gitlab.example.com")
            self.assertNotIn(b"CANARY", result)
            self.assertTrue(json.loads(result)["failure_observed"])
            fake.write_text("#!" + sys.executable + "\n" + source.replace("'pipeline':{'id':3}", "'pipeline':{'id':4}"))
            with self.assertRaises(ValueError):
                fetch(fake, "group/project", 3, 5, root, "gitlab.example.com")
            fake.write_text("#!" + sys.executable + "\n" + source.replace("'pipeline':{'id':3}", "'pipeline':None"))
            with self.assertRaisesRegex(ValueError, "pipeline mismatch"):
                fetch(fake, "group/project", 3, 5, root, "gitlab.example.com")
