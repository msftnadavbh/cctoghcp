# Configuration map: carry outcomes, not raw JSON

Start with [your repository inventory](../migration/configuration-inventory.md). Audit repository, user home, ancestor directories and machine policy separately before a paid session; avoid printing personal files or tokens. The optional `scripts.inventory` reports *known path and field names*, not whether a CLI loaded them. This repo has **no root active hook, MCP, plugin or duplicate `copilot-instructions.md`**.

| Claude or Copilot surface | Recognized locations / migration intent | Scope and verification boundary |
| --- | --- | --- |
| Always-on instructions | Root `CLAUDE.md`, `.claude/CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md` | Retain your project's own CLAUDE; use `/instructions` and `/env` to confirm attachment |
| Narrow instruction | Nested `CLAUDE.md`, `.claude/rules/*.md`, `.github/instructions/*.instructions.md` | v1.0.89 rules support; validate matching/nonmatching path and attachment, not inferred precedence |
| Shared settings | `.claude/settings.json` documented subset; `.github/copilot/settings.json` Copilot repo settings | `companyAnnouncements`, `disableAllHooks`, `enabledPlugins`, `extraKnownMarketplaces`, `hooks` need key-by-key review; no blanket permissions/provider translation |
| Private settings | `.claude/settings.local.json`, `~/.copilot/config.json`, private HOME | Never commit; persisted grants/secret-bearing settings can change trust. Review source without outputting values |
| Skills and commands | `.claude/skills/*/SKILL.md`, `.github/skills`, `.agents/skills`; `.claude/commands/*.md` alternate | Keep your canonical `.claude/skills`; inspect `/skills` and command behavior before claiming use |
| Agents | `.github/agents/*.agent.md`, supported `.claude`/personal variants | Name collision descriptions differ; custom subagent default does not include repository instructions unless enabled; main selection differs |
| Hooks | `.github/hooks/*.json` or documented shared settings `hooks` | Choose **one** registration; inert examples only; hook timeout may fail open, CI independent |
| MCP | Audit existing Claude `.mcp.json` first; Copilot project `.github/mcp.json` or user `~/.copilot/mcp-config.json` | Review reusable server definitions, transport, OAuth and server instructions before activation; templates are inert |
| Plugin | Root `plugin.json` in packaged artifact | Inspect package contents and installed `plugin install --help` before approving installation |
| Sessions | `~/.copilot/session-state` and logs | Private, not portable source-of-truth and not safe to export casually |

Relative `@` imports inside supported instructions stay within repository/custom boundaries; `GEMINI.md` and path instructions do not expand them. Check your installed Claude version before assuming whether it reads `AGENTS.md`. [Compatibility](../migration/compatibility.md) and [inventory workflow](../migration/configuration-inventory.md) give an inspection plan. Don't use an instruction file as a substitute for actual tool/path permission controls.
