"""Minimal newline-delimited stdio MCP 2025-11-25 subset; unit-tested only.

No filesystem, network, auth, resources, prompts, subscriptions or model access.
"""
import json
import sys

from scripts.safety import LIMIT, json_load

VERSION = "2025-11-25"
TOOL = {"name": "synthetic_catalog_count", "description": "Return a fixed synthetic product count.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}}


class Server:
    def __init__(self):
        self.initialized = False
        self.ready = False

    def receive(self, raw):
        ident = None
        try:
            request = json_load(raw)
        except ValueError:
            return self.error(None, -32700)
        if not isinstance(request, dict) or request.get("jsonrpc") != "2.0":
            return self.error(None, -32600)
        ident = request.get("id")
        if "id" in request and (type(ident) not in (str, int) or isinstance(ident, bool)):
            return self.error(None, -32600)
        method = request.get("method")
        params = request.get("params", {})
        if not isinstance(method, str) or not isinstance(params, dict):
            return self.error(ident, -32600)
        if "id" not in request:
            if method == "notifications/initialized" and self.initialized:
                self.ready = True
            return None
        if method == "initialize":
            client = params.get("clientInfo")
            if (self.initialized or not isinstance(params.get("protocolVersion"), str) or
                    not isinstance(params.get("capabilities"), dict) or not isinstance(client, dict) or
                    not all(isinstance(client.get(k), str) for k in ("name", "version"))):
                return self.error(ident, -32602)
            self.initialized = True
            result = {"protocolVersion": VERSION, "capabilities": {"tools": {}},
                      "serverInfo": {"name": "checkpoint-synthetic", "version": "1.0.0"}}
        elif method == "ping":
            result = {}
        elif not self.ready:
            return self.error(ident, -32000)
        elif method == "tools/list":
            if params:
                return self.error(ident, -32602)
            result = {"tools": [TOOL]}
        elif method == "tools/call":
            if params.get("name") != TOOL["name"] or params.get("arguments", {}) != {}:
                return self.error(ident, -32602)
            result = {"content": [{"type": "text", "text": "Synthetic catalog contains 4 products."}],
                      "isError": False}
        else:
            return self.error(ident, -32601)
        return {"jsonrpc": "2.0", "id": ident, "result": result}

    @staticmethod
    def error(ident, code):
        return {"jsonrpc": "2.0", "id": ident, "error": {"code": code, "message": "Request rejected"}}


def main():
    server = Server()
    while True:
        line = sys.stdin.buffer.readline(LIMIT + 1)
        if not line:
            return 0
        if len(line) > LIMIT or not line.endswith(b"\n"):
            print(json.dumps(server.error(None, -32700)), flush=True)
            return 2
        response = server.receive(line)
        if response is not None:
            print(json.dumps(response), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
