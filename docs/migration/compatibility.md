# Keep, audit or replace? Claude configuration in Copilot CLI

Start with [your existing checkout](../start/use-copilot-in-your-repository.md), not a copied example. The table describes recognized surfaces, **not** a promise that every file is attached or that conflicting files have universal precedence. Review your own configuration before a trusted session. [Configuration map](../reference/configuration-map.md) has the fuller location list. [source:cli-config-reference]

| Your Claude artifact | Keep or audit | Copilot action / verification |
| --- | --- | --- |
| Root `CLAUDE.md`, `.claude/CLAUDE.md` | **Keep** your project's policy; avoid a duplicate root `AGENTS.md` just for migration | Check `/instructions` and `/env` in that checkout. Repository-relative `@` imports must stay within repository/custom-instruction boundaries; not absolute or `~` paths. |
| `.claude/rules/*.md`, nested `CLAUDE.md` | **Keep, test scope**; rules support is recorded in v1.0.89 | Compare attachment for matching and nonmatching files; do not infer precedence from mere presence. [claim:rules-added] |
| `.claude/skills/*/SKILL.md` | **Keep** canonical skill text | Check `/skills`, then request a relevant skill explicitly and inspect its result. Discovery alone does not prove invocation. |
| `.claude/commands/*.md` | **Audit** invocation, formatting and tool effects | Alternate skill source, not a guarantee that every Claude slash command has identical Copilot semantics. Check `/skills` and try only a reviewed command. |
| Claude agents | **Audit** each definition and tool list | Review CLI discovery and `/agent`. A custom subagent needs `include-custom-instructions: true` to inherit repository instructions; main-agent selection differs. [Agents](../customization/agents.md). |
| `.claude/settings.json` and private settings | **Audit key by key**, not whole-file translation | Shared settings have a documented subset; permissions, provider configuration and credentials require separate review. Keep personal settings private. |
| Hooks and `.mcp.json` | **Audit before reuse or activation** | Review event/payload compatibility, server definitions, credentials and permissions. Supported project MCP locations include `.mcp.json` and `.github/mcp.json`; discovery does not establish a working authenticated connection. |
| Claude conversation or memory | **Keep useful decisions as reviewed notes** | `copilot --resume` resumes a Copilot session, not a Claude transcript or imported auto-memory. Check cwd and current files. |

Copilot also recognizes `AGENTS.md`, `GEMINI.md`, GitHub custom instructions and path instructions; `GEMINI.md` and `.github/instructions/*.instructions.md` do not expand `@` imports. Don't assume universal priority between competing sources or that nested guidance loads for unrelated paths. Restart or resume, then inspect `/instructions` after changes; arbitrary hot reload is not promised. Claude's own `AGENTS.md` support is version-dependent (direct support at least 2.1.277 per supplied research), so migration to that filename is not mandatory. [source:instructions-reference]

If an agent or scoped rule appears to contradict your policy, reconcile the files yourself rather than betting on undocumented priority. [Inventory](configuration-inventory.md), [coexistence](coexistence.md) and [known discrepancies](../reference/known-discrepancies.md) separate observable attachment from assumptions. Authenticated runtime attachment was not verified in this repository.
