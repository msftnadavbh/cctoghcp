# MCP: local protocol test is not CLI integration

**Optional advanced POSIX examples:** the native lab does not activate MCP. Use [first 15 minutes](../start/first-15-minutes.md) without it first; the launcher below is not a Windows/macOS native client test.

The local template uses a reviewed absolute interpreter and trusted standalone launcher outside the lab: `/usr/bin/python3 -I -B /ABSOLUTE/checkpoint/scripts/trusted_launcher.py mcp`. It imports its own trusted root, not cwd; replace paths deliberately. No MCP is registered or run through the CLI by validation.

[Local template](../../examples/mcp/local.json) is inert; synthetic server handles MCP 2025-11-25 `initialize`/`initialized`, `ping`, `tools/list` and one fixed no-argument `tools/call`. `python3 -B -m scripts.validate` runs its protocol unit tests, not a Copilot client. [GitLab HTTP](../../examples/mcp/gitlab-http.experimental.json) and [glab server](../../examples/mcp/glab.experimental.json) are experimental examples, not production integrations.

Before optional activation, review server executable/URL, transport, entitlement, environment and secret storage, server instructions, tool descriptions and remote data exposure. `--allow-all-mcp-server-instructions` broadens the trust surface. GitLab's **beta preview** `/api/v4/mcp` depends on instance/group availability; verify your CLI client separately. Never place tokens in JSON examples. [Plugin-shipped agent MCP settings](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) are separate from project/user agent configuration. [GitLab integration](../hosting/gitlab-now.md).
