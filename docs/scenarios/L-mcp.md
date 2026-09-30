# L — Inspect an MCP integration without enabling it

MCP activation isn't needed to learn Copilot CLI. Review the example [local config](../../examples/mcp/local.json) and [MCP guide](../customization/mcp.md) for its launcher, tool and permission boundaries. In a read-only Copilot session you may ask: “Explain how server instructions and tool output could affect a code review; do not register or call any MCP server.” **Expected:** an explanation, not a newly available tool. Static protocol tests, where supported, don't prove that Copilot connected. The bundled advanced server/test harness was developed as a POSIX workflow; don't run its scripts as a Windows-native integration. Only enable an independently reviewed server after separate authorization and transport/credential review.

## Goal and prerequisites

Review config only; no MCP activation.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** trust-boundary explanation above. **Checkpoint:** no server added. **Verification:** check `/env` for unexpected integration. **Permissions:** read tools. **External effects:** optional credits. **Escape:** stop on activation request. **Claude analogy:** MCP client trust differs. [source:mcp-spec]
