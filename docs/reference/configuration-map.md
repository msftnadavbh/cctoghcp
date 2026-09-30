# Configuration map: carry outcomes, not raw JSON

`python3 -B -m scripts.inventory .` reports *known path and field names*, not whether a CLI loaded them. Audit repository, user home, ancestor directories and machine policy separately before a paid session; avoid printing personal files or tokens. This repo intentionally has **no root active hook, MCP, plugin or duplicate `copilot-instructions.md`**. [source:cli-config-reference]

| Claude or Copilot surface | Recognized locations / migration intent | Scope and verification boundary |
| --- | --- | --- |
| Always-on instructions | Root `CLAUDE.md`, `.claude/CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md` | Root CLAUDE stays; *bare* lab copies none. First-15-minute `--with-config` copies one reviewed fixture CLAUDE/import. Use `/instructions`/`/env` to inspect actual attachment |
| Narrow instruction | Nested `CLAUDE.md`, `.claude/rules/*.md`, `.github/instructions/*.instructions.md` | v1.0.89 rules support; validate matching/nonmatching path and attachment, not inferred precedence |
| Shared settings | `.claude/settings.json` documented subset; `.github/copilot/settings.json` Copilot repo settings | `companyAnnouncements`, `disableAllHooks`, `enabledPlugins`, `extraKnownMarketplaces`, `hooks` need key-by-key review; no blanket permissions/provider translation |
| Private settings | `.claude/settings.local.json`, `~/.copilot/config.json`, private HOME | Never commit; persisted grants/secret-bearing settings can change trust. Review source without outputting values |
| Skills and commands | `.claude/skills/*/SKILL.md`, `.github/skills`, `.agents/skills`; `.claude/commands/*.md` alternate | Canonical text under `.claude/skills`; bare lab copies none, `--with-config` copies exactly three. Inspect `/skills` before claiming attachment |
| Agents | `.github/agents/*.agent.md`, supported `.claude`/personal variants | Name collision descriptions differ; custom subagent default does not include repository instructions unless enabled; main selection differs |
| Hooks | `.github/hooks/*.json` or documented shared settings `hooks` | Choose **one** registration; inert examples only; hook timeout may fail open, CI independent |
| MCP | Audit existing Claude `.mcp.json` first; Copilot project `.github/mcp.json` or user `~/.copilot/mcp-config.json` | No automatic activation equivalence for Claude file; templates inert, transport/OAuth/server instructions reviewed separately |
| Plugin | Root `plugin.json` in packaged artifact | Schema/generator tested; install help lacks local path, lifecycle untested |
| Sessions | `~/.copilot/session-state` and logs | Private, not portable source-of-truth and not safe to export casually |

Relative `@` imports inside supported instructions stay within repository/custom boundaries; `GEMINI.md` and path instructions do not expand them. Current Claude versions (direct AGENTS.md support at least 2.1.277, per supplied research; verify locally) must not be described as universally unable to read `AGENTS.md`. [Compatibility](../migration/compatibility.md) and [inventory workflow](../migration/configuration-inventory.md) give an inspection plan. Don't use an instruction file as a substitute for actual tool/path permission controls. [source:instructions-reference]
