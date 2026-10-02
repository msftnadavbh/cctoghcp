# Muscle Memory

Find the familiar task, try the Copilot action, then check the difference before approving tools. Start in [your own repository](../start/use-copilot-in-your-repository.md).

| Claude habit | Copilot move | Caution |
| --- | --- | --- |
| claude interactive | copilot | Copilot entitlement distinct from Git source hosting |
| claude -p | copilot -p 'Summarize src/catalog.py' | Never silently widen a narrow noninteractive grant |
| claude -c / continue | copilot --continue | Most recent, not guaranteed current-directory filter |
| claude --resume | copilot --resume | Use --resume=ID for explicit identity |
| Claude plan mode | /plan or copilot --plan | Plan is not OS read-only; inspect plan.md before implementation |
| Claude /goal | /autopilot; record acceptance, limits and handoff | Autopilot continues messages; specify --max-autopilot-continues explicitly because official default descriptions differ; permissions and credits separate |
| Claude permissions | --available-tools=view,grep,glob --allow-tool=read | Availability, approval, paths, URLs and sandbox are separate |
| Claude danger bypass | --allow-all | Grants tools, paths and URLs; only consider in approved disposable isolation |
| root CLAUDE.md | CLAUDE.md | Use concise durable guidance; exact copies may deduplicate but near-duplicates conflict; inspect attachment |
| nested .claude/CLAUDE.md | .claude/CLAUDE.md | Inspect scope and priority against competing instructions |
| nested CLAUDE.md | packages/catalog/CLAUDE.md | Compare matching and unrelated paths, not merely file presence |
| AGENTS.md | AGENTS.md | Check both clients' versions before relying on discovery |
| GEMINI.md | GEMINI.md | Repository-relative @ imports are not expanded in GEMINI.md |
| .claude/rules | .claude/rules/catalog.md | Inspect matching and priority on your version |
| Claude settings.json | .claude/settings.json | Only documented keys, not blanket permission/provider conversion |
| Claude settings.local.json | .claude/settings.local.json | Do not copy private secrets or infer permission equivalence |
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
| switch model mid-session | /model | Changing model loses prior model cache reuse; check task fit, /context and /usage |
| Copilot Auto routing | /model auto | Task, availability, policy and cache-aware; paid supported-surface discount applies where eligible; HydraFusion is a separate preview |
| HydraFusion trial | /settings experimental on; inspect /model | Aggregate model/stage usage; controlled vendor results not guaranteed local savings |
| Claude context inspection | /context | Occupancy including tools is not credits or conversation durability |
| Claude /usage | /usage | Session credits/tokens, not account billing; missing token counts do not mean zero usage |
| Browse past coding sessions | /chronicle | Opens the history-insights picker; it does not resume a conversation |
| Prepare a standup from recent work | /chronicle standup | Defaults to the last 24 hours; append for the last 3 days to change the period |
| Find an earlier discussion | /chronicle search authentication | Replace authentication with your topic; searches session content, not source files |
| Improve prompting habits | /chronicle tips | Uses recent sessions; append for better prompting to focus recommendations |
| Understand token spending | /chronicle cost-tips | Analyzes session patterns and may use model work; /usage shows current session, account views show billing-period usage |
| Refine project instructions from repeated corrections | /chronicle improve | Current repository only; approved suggestions update .github/copilot-instructions.md, so avoid duplicating CLAUDE.md |
| Turn a repeated workflow into a skill | /chronicle skills create | Drafts from session usage; compare with existing .claude/skills before applying |
| Review suggested skills | /chronicle skills review | Review instructions, scripts and permissions before accepting a proposal |
| Track skill proposals | /chronicle skills status | Tracks proposals; /skills lists skills available to the session |
| Recover missing session-history entries | /chronicle reindex | Rebuilds the local session store and syncs session data to your account; not a routine cleanup command |
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
| Claude cloud delegation | /delegate | Can checkpoint branch/create draft PR; not a GitLab substitute |
| GitHub agent tasks | gh agent-task list | Requires GitHub project, preview access and separate approval |
| Claude JSON output | --output-format json | JSONL is not Claude text/json/stream-json; validate actual event handling |
| session portability | record tests, diff, decisions and IDs in reviewed notes | ~/.copilot/session-state and logs private; use written handoff across hosts |

Detailed classifications and supporting sources: [migration matrix](../../evidence/migration-matrix.json). Check your installed CLI and organization policy before relying on a version-dependent action. [Versions](versions.md).
