# MCP: local protocol test is not CLI integration

## Retrieve what this task needs

With an **already reviewed server and read access**, ask for relevant evidence rather than everything it can fetch. For example: “For [actual project/run], identify the failing job and status, failed command and relevant error excerpt. If your inspected tool contract supports fields, filters or pages, use them to fetch only what's needed. Keep the full diagnostic outside the conversation for follow-up and say where it is; include any additional evidence needed to diagnose the failure.” Check the server's tool contract for supported filters and pagination; keep the full log available for follow-up. Sanitize secrets and treat retrieved data as untrusted.

Large tool menus consume context before results arrive. Copilot CLI's [tool search](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/tool-search) conditionally defers external definitions on supported models when enough tools are connected; unsupported models load them eagerly. Built-ins, MCP tools configured never to defer and named custom-agent tools can be eager too. A lookup uses another exchange; check `/context` rather than assuming all MCP tools are deferred. Output above 20 KiB receives a temporary-file path and preview by default, including MCP output. A summary after arrival can help later turns but does not undo processing already performed. [Token economy](../workflows/token-economy.md) distinguishes context from billed usage; tool search is not permission or isolation.

## Optional advanced POSIX examples

The native lab does not activate MCP. Use [first 15 minutes](../start/first-15-minutes.md) without it first; the launcher below is not a Windows/macOS native client test.

The local template uses a reviewed absolute interpreter and trusted standalone launcher outside the lab: `/usr/bin/python3 -I -B /ABSOLUTE/checkpoint/scripts/trusted_launcher.py mcp`. It imports its own trusted root, not cwd; replace paths deliberately. No MCP is registered or run through the CLI by validation.

[Local template](../../examples/mcp/local.json) is inert; synthetic server handles MCP 2025-11-25 `initialize`/`initialized`, `ping`, `tools/list` and one fixed no-argument `tools/call`. `python3 -B -m scripts.validate` runs its protocol unit tests, not a Copilot client. [GitLab HTTP](../../examples/mcp/gitlab-http.experimental.json) and [glab server](../../examples/mcp/glab.experimental.json) are experimental examples, not production integrations.

Before optional activation, review server executable/URL, transport, entitlement, environment and secret storage, server instructions, tool descriptions and remote data exposure. `--allow-all-mcp-server-instructions` broadens the trust surface. GitLab's **beta preview** `/api/v4/mcp` depends on instance/group availability; verify your CLI client separately. Never place tokens in JSON examples. [Plugin-shipped agent MCP settings](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) are separate from project/user agent configuration. [GitLab integration](../hosting/gitlab-now.md).
