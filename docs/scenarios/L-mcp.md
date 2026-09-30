# L — MCP protocol only, no Copilot client

## Goal and prerequisites

Separate synthetic server protocol from authenticated client integration. Python 3, no creds, host or server activation.

## Start and deterministic check

```sh
python3 -B -m unittest discover -s tests -p 'test_protocol_gitlab.py'
python3 -B -m scripts.validate --static-only
```

Review [inert config](../../examples/mcp/local.json): absolute trusted launcher, fixed no-argument tool, no credential env. **Optional prompt for later read-only authorized CLI:** “Describe synthetic tool output and trust boundaries; do not register MCP or enable server instructions.” It does **not** invoke the server in Copilot.

## Checkpoints, effects and exit

**Checkpoint:** protocol initialize/ping/list/call tests pass; no CLI client result. **Verification:** unit test exit and config validation, not `copilot mcp` discovery. **Permissions:** none beyond local Python; activation would require new process and server-instruction review. **External effects:** offline local process only. **Escape:** if real client tool absent, inspect transport/auth separately; never allow all MCP instructions reflexively. **Claude analogy/difference:** MCP concepts transfer, but client config, OAuth and instruction trust differ. [source:mcp-spec] [claim:mcp-subset] Protocol fake-tested, no service test.
