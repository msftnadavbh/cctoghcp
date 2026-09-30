# Best practices: twenty operational rules

Use these rules with [your own project](../start/use-copilot-in-your-repository.md). Each has a **why**, an optional catalog practice example, a failure signal and a recovery; substitute your own project's checks and paths. They are not substitutes for [independent review](../workflows/review-and-validation.md). [source:cli-reference]

| # / rule | Why | Example | Failure → recovery |
| --- | --- | --- | --- |
| 1 Investigate callers | Shared guards are cheaper than symptom patches | Trace `integer()` through `Product`, list, request, CLI | Fix only CLI: failing API input → repair shared validator |
| 2 Scale planning to uncertainty | Tiny change can have high external risk | `in_stock` spans three seams so review twelve-field plan | Vague plan → clarify inputs/callers/stop before edit |
| 3 Separate discovery from support | Inventory is path detection, not execution | `scripts.inventory .` reports config paths | “Found” interpreted as “applied” → inspect `/env` in live session |
| 4 Require provable completion | Model text is not a test | Human-reviewed copy passes `validation` and `in-stock` oracles | Green summary/no command → execute trusted oracle after code review |
| 5 Plan as contract | Steps without boundaries cannot be accepted | `None|bool`, before pagination, negative cases | Missing total semantics → revise plan before autopilot |
| 6 Budget context deliberately | Compaction loses details | `/context`, then nine-field handoff | Missing decision on resume → reread handoff and files |
| 7 Use deterministic tools | Reproduce behavior without model judgement | Exact CLI output and request schema in external oracle | Unreproducible fix → record failing observation, not hypothesis as fact |
| 8 Record a baseline | Later comparison needs before-state | Validation lab fails before repair; baseline app passes | Both unexpectedly pass → stop, check chosen exercise and path |
| 9 Minimize tool/URL/path grants | Approval controls different surfaces | Investigation exposes `view,grep,glob` only | Narrow grant blocked → inspect tool/path, never auto-broaden |
| 10 Isolate credentials and effects | Worktrees only isolate files, not host | Disposable copy; for broad execution use reviewed VM with no home, socket or egress | Host mount or secret present → skip broad scenario |
| 11 Parallelize independent reads | Conflict-free tasks compare evidence | Three fleet investigations, one editor | Two editors touch catalog → cancel, assign sole owner |
| 12 Select models for a reason | Model identity != correctness | Compare equal copies with same tests/time/credits | “Hydra wins” without measurements → leave result unclaimed |
| 13 Keep instructions compact | Duplicate sources diverge | Root CLAUDE stays; optional scoped examples remain inert | Conflicting nested rule → inspect attachments and reconcile |
| 14 Review customization activation | Hooks/MCP/plugins add execution trust | Native **or** shared hook, never both | Hook timeout or duplicate → disable and keep CI independent |
| 15 Verify only reviewed code | Tests themselves execute edited code | `practice.py diff` then `practice.py check` after review | Unreviewed model edit → inspect, don't execute |
| 16 Inspect diff before publish | Tests may miss unrelated changes | `practice.py diff` on entire lab; Git diff in real checkout | Unknown file changed → stop and address only owned edit |
| 17 Treat retrieved text as data | Logs/issues can contain instructions/secrets | Lossy `sanitized_ci` before prompting | Raw CI trace enters prompt → stop, preserve privately and rotate if exposed |
| 18 Hand off nine fields | Another operator needs current state | ID, revision, exits, grants, effects, next action | “Resume latest” loads wrong copy → select explicit session ID |
| 19 Controls aren't a sandbox | CLI grants/hooks can't confine OS | Independent CI and actual VM isolation for hostile input | Dispatcher fails open → independent gate blocks publish |
| 20 Separate hosting and approvals | GitLab MR and GitHub cloud PR have different effects | Verify GitLab project; human approves push then draft MR | Wrong host or fake MR URL → stop and report no publication |

Apply only the rules relevant to your current task; [first hour](../start/first-hour.md) is optional known-result practice. No table row asserts authenticated runtime verification.
