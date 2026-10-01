# Secrets and shared tokens are re-provisioned, not migrated

Do not copy tokens, API keys, database credentials, PATs or private keys from Claude Code configuration into GitHub Copilot prompts, repository files or documentation.

If a workflow depends on a shared token, migrate the **requirement**, not the value.

Capture:

| Field | Example |
| --- | --- |
| Workflow | Review Jira-linked incident bug |
| Secret requirement | Jira read token |
| Scope | Read-only project issues |
| Owner | Platform/security |
| Runtime | MCP server, GitHub Actions, local CLI, internal gateway |
| Storage target | Approved secret store, GitHub Actions secret, MCP server environment or organization secret manager |

Preferred patterns:

- Put shared tool credentials behind an MCP server or internal gateway.
- Give Copilot access to approved operations, not raw token values.
- Use read-only scopes first.
- Split broad shared tokens into narrower scopes where practical.
- Keep personal settings and local auth private.

Example handoff text:

```text
This workflow requires Jira issue lookup through an approved MCP server.
Secret required: JIRA_READ_TOKEN
Scope: read-only project issue metadata
Owner: platform/security
Do not expose the token to the assistant or commit it to the repository.
```

See [MCP configuration](../customization/mcp.md), [hosting boundaries](../hosting/capability-boundaries.md) and [GitLab integration](../hosting/gitlab-now.md) for related authentication boundaries.

