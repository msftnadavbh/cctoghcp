# CLI Cheat Sheet

Find the familiar task, try the Copilot action, then check the difference before approving tools. Start in [your own repository](../start/use-copilot-in-your-repository.md).

| Goal from Claude | Exact move | Boundary |
| --- | --- | --- |
| claude interactive | copilot | Copilot entitlement distinct from Git source hosting |
| claude -c / continue | copilot --continue | Most recent, not guaranteed current-directory filter |
| claude --resume | copilot --resume | Use --resume=ID for explicit identity |
| Claude plan mode | /plan or copilot --plan | Plan is not OS read-only; inspect plan.md before implementation |
| Claude /goal | /autopilot; record acceptance, limits and handoff | Autopilot continues turns; keep an explicit written acceptance and stop condition |
| Claude permissions | --available-tools=view,grep,glob --allow-tool=read | Availability, approval, paths, URLs and sandbox are separate |
| Claude danger bypass | --allow-all | Grants tools, paths and URLs; only consider in approved disposable isolation |
| root CLAUDE.md | CLAUDE.md | Do not duplicate; inspect actual attachment |
| AGENTS.md | AGENTS.md | Check both clients' versions before relying on discovery |
| GEMINI.md | GEMINI.md | Repository-relative @ imports are not expanded in GEMINI.md |
| Claude settings.json | .claude/settings.json | Only documented keys, not blanket permission/provider conversion |
| project skills | .claude/skills/name/SKILL.md | Also .github/skills and .agents/skills; inspect /skills in session |
| personal skills | ~/.copilot/skills/name/SKILL.md | Personal and project locations differ; inspect private HOME |
| .claude/commands | .claude/commands/name.md | Inspect /skills before relying on command invocation |
| Claude custom agents | .github/agents/name.agent.md | Subagent needs explicit include-custom-instructions true to receive repo policy |
| Claude built-in agents | /tasks; /rubber-duck | Use explicit role selection; inspect tasks |
| Claude teams | /fleet or copilot --fleet | Parallelism separate from permission and autonomy; one integrator owns edits |
| Claude hooks | .github/hooks/*.json or shared settings hooks | Timeout may fail open; choose one registration and keep CI independent |
| project MCP | .github/mcp.json; review existing .mcp.json for reusable server definitions | Review server instructions and credentials before enabling; audit both config locations |
| user MCP | ~/.copilot/mcp-config.json | Review private HOME and server before enabling |
| Claude plugins | plugin.json plus skills/ | Check installed CLI options and review archive before installation |
| Claude model selection | /model or --model MODEL | Choose a model available to your account and policy |
| switch model mid-session | /model | Pinning is not deterministic; inspect context and credits |
| Copilot Auto routing | /model auto | Auto routing is not HydraFusion research preview or fleet parallelism |
| Claude context inspection | /context | Context usage is not conversation durability |
| Claude compact | /compact | Summarization is lossy; keep a written handoff |
| Claude new conversation | /new | Does not reset files or Git branch |
| Claude rewind | /rewind | Does not guarantee rollback of shell/network effects |
| conversation branch | /fork | Conversation fork does not isolate filesystem |
| Git branch | git switch -c feature/catalog | Use only in a real reviewed Git checkout, not disposable first lab |
| Claude worktrees | /fork worktree or /new worktree | Separate directory, not identity/network sandbox; check base/uncommitted changes |
| Claude background tasks | /tasks | Shell-process tasks differ from agent tasks; inspect pending work before exit |
| Claude web lookup | ask for source links; approve URL per host | Remote content untrusted; a URL grant is not blanket network permission |
| Claude local review | /diff then /review | Neither substitutes for tests or independent human review |
| GitLab merge request | glab mr create --repo group/project --source-branch feature/catalog --target-branch main --title 'Catalog fix' --description 'Reviewed changes' --draft | Local Copilot doesn't publish; human approves push and MR separately |
| Claude JSON output | --output-format json | JSONL is not Claude text/json/stream-json; validate actual event handling |

Detailed classifications and supporting sources: [migration matrix](../../evidence/migration-matrix.json). Check your installed CLI and organization policy before relying on a version-dependent action. [Versions](versions.md).
