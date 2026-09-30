# Optional external patterns

Upstream [awesome-copilot](https://github.com/github/awesome-copilot) offers optional examples, not configuration to install wholesale. Check each item's content, license and version before copying it into your project. The upstream repository lists MIT at root, but contributed items can require additional attribution. [Upstream index](https://awesome-copilot.github.com/llms.txt).

| Example | What it covers | Before using it |
| --- | --- | --- |
| [refactor-plan skill](https://github.com/github/awesome-copilot/blob/main/skills/refactor-plan/SKILL.md) — broad refactors | Phase gates and rollback idea; task skill | Compare with the [refactor exercise](../scenarios/N-refactor.md); review shell steps, attribution and edit scope before adapting |
| [create-implementation-plan skill](https://github.com/github/awesome-copilot/blob/main/skills/create-implementation-plan/SKILL.md) — complex plans | Named plan files/IDs; skill | Review file writes, dependencies and version before use |
| [bug-reproduction-brief skill](https://github.com/github/awesome-copilot/blob/main/skills/bug-reproduction-brief/SKILL.md) — reproduce a bug | Separates the failing behavior from suspected causes | Check the skill's license and commands before adapting |
| [debug agent](https://github.com/github/awesome-copilot/blob/main/agents/debug.agent.md) — guided debugging | Structured steps; agent | Editor tool names may differ from CLI `view,grep,glob`; review tools and MCP before adapting |
| [hooks instructions](https://github.com/github/awesome-copilot/blob/main/instructions/hooks.instructions.md) — hook authoring | Checklist for lifecycle hooks; instructions | Compare every payload and failure statement against [official current hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference); inherited text could affect all tool calls, so no auto-load |
| [tool-guardian script](https://github.com/github/awesome-copilot/blob/main/hooks/tool-guardian/guard-tool.sh) — tool allowlist example | Shows a regex policy; executable hook | Compare payload fields with your hook format; shell/regex checks are not a sandbox |
| [MCP implementation security review](https://github.com/github/awesome-copilot/blob/main/skills/mcp-implementation-security-review/SKILL.md) — server threat review | Checklist for credentials, server prompts and tool descriptions; skill | Review dependencies and permissions; a checklist does not certify GitLab transport |
| [structured-autonomy plugin](https://github.com/github/awesome-copilot/blob/main/plugins/structured-autonomy/plugin.json) — packaged workflow | Manifest example; plugin | Verify its referenced skill files exist in the distributable archive before installing |
| [Creating Effective Skills](https://awesome-copilot.github.com/learning-hub/creating-effective-skills/) — skill authorship | Focused descriptions, task boundaries, tests and assets | Adapt ideas only; review code that may write or commit before use |
| [daily issues report workflow](https://github.com/github/awesome-copilot/blob/main/workflows/daily-issues-report.md) — scheduled issues | GitHub gh-aw job design; workflow | Creates external GitHub issues and may require Actions credentials, permissions and scheduler. Applies only to a separately authorized GitHub-hosted project; never schedule from the local lab; verify upstream file/version before reuse |

These links are optional, not installed integrations. The [local skills](../../.claude/skills) are the only skills in this repo's plugin ZIP. [Official references](../../SOURCES.md).

Related optional projects: [Copilot SDK](https://github.com/github/copilot-sdk) for programmatic lifecycle needs, [spec-kit](https://github.com/github/spec-kit) for specification workflows and [gh-aw](https://github.com/github/gh-aw) for GitHub Actions agents. Review installation, credentials and permissions separately.
