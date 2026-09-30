# L — Inspect an MCP integration without enabling it

Review the [local config](../../examples/mcp/local.json) and [MCP guide](../customization/mcp.md) before enabling a server. Ask Copilot: “Explain which tools this server exposes and what data they can access. Do not register or call it.” **Expected:** a description of tools and access, with no new server connection. The bundled launcher requires a POSIX environment. Approve the server, transport and credentials separately before activation.

## Goal and prerequisites

Review config only; no MCP activation.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** trust-boundary explanation above. **Checkpoint:** no server added. **Verification:** check `/env` for unexpected integration. **Permissions:** read tools. **External effects:** optional credits. **Escape:** stop on activation request. **Claude analogy:** MCP client trust differs.
