# Inventory your configuration before migrating

In **your existing checkout**, inspect the files you already rely on: root and nested `CLAUDE.md`, relative imports, `.claude/rules`, `.claude/skills`, `.claude/commands`, agents, settings, hooks and `.mcp.json`. Look for user-only settings and ancestor guidance separately. Opening files is an audit, not permission to execute anything in them. Keep credentials and private HOME content out of prompts. [source:cli-config-reference]

| What to record for each surface | Why |
| --- | --- |
| Path, owner and intended behavior | Distinguish project policy from personal settings and examples |
| Any command, import, server, secret or grant | Decide whether activation is appropriate before a trusted Copilot session |
| Keep / adapt / leave disabled | Do not translate a whole settings file as if the schemas were identical |
| Observed `/instructions`, `/skills`, `/agent` or `/env` result | A path on disk is not proof of attachment or execution |

Native directory inspection works without this book's scripts: from the checkout, PowerShell `Get-ChildItem .claude -Force` or macOS zsh `ls -a .claude` if that directory exists. Read relevant files privately; missing directories are normal. For settings such as `companyAnnouncements`, `disableAllHooks`, `enabledPlugins`, `extraKnownMarketplaces` or `hooks`, decide **per key**. Claude `.mcp.json` does not automatically become Copilot `.github/mcp.json`. Avoid creating a second root policy when the existing `CLAUDE.md` works. [Compatibility](compatibility.md) gives the short artifact-by-artifact answer; [configuration map](../reference/configuration-map.md) lists recognized destinations.

The optional offline `scripts.inventory` report belongs to **this guide's checkout**, not your application and not the first step in using Copilot. It reports names, not whether anything loaded; never paste its private output without review.
