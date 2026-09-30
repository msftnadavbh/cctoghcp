# Fleet and subagents: work graph, not six simultaneous editors

The six named built-in roles serve different *intentions*. Installed 1.0.89 help exposes `/fleet`, `--fleet`, `/tasks`, `/rubber-duck`, `/subagents` and `/agent`, but not a guaranteed six-item picker or every built-in's exact default tool permissions. Describe allowed tools in your task **and** enforce tool availability/approval in the actual client; an agent saying “read only” is not an OS boundary. The custom [investigator](../../examples/agents/focused-investigator.agent.md) deliberately specifies `view`, `grep`, `glob` and explicit instruction inheritance; that fixture does not document all built-ins. [source:cli-reference]

| Role | Suitable request/context | Tools, inheritance and output boundary | When not to use |
| --- | --- | --- | --- |
| Explore | Trace `integer()` callers in copied catalog | Ask for cited path/line evidence, read tools only; confirm actual built-in availability/permissions | Don't ask it to patch or certify tests |
| Task | Execute a single approved independent unit | Give owned paths, acceptance, stop; verify actual tool set and whether repository instructions attached | Don't delegate an undefined product decision |
| General Purpose | Integrate a bounded feature after decisions settle | Main integrator owns edits; subagent instructions are not inherited by default in custom definitions | Don't make it a second editor on same file |
| Code Review | Challenge a final diff against input/output contract | Read-only request, cite missed negative tests; don't confuse with authoritative human review | Don't accept “LGTM” without tests |
| Research | Investigate external versions/documentation | Sources and date required; URL/network approvals separate from local file access | Don't use for a local bug already reproducible offline |
| Rubber Duck | Critique assumptions with `/rubber-duck` | Ask “What is wrong with filter-before-pagination plan?”; no claim of automatic picker routing | Don't treat critique as implementation or sign-off |

For custom subagents choose `include-custom-instructions: true` **if** repository policy must attach. Selecting a definition as the main agent and spawning it as a subagent have different instruction behavior. Review collisions between `.github`, `.claude` and personal definitions; current source descriptions disagree on priority. Configure per-agent models through `/subagents` only when the actual environment supports them and a cost reason exists. [Agents](../customization/agents.md).

## Concrete dependency graph: copied `in_stock` exercise

The [fleet exercise](../../labs/exercises.json) specifies **read-only** investigations. After checking an owned passing baseline and expected failing `in-stock` oracle, the integrator writes one shared assumption: inputs `None|bool`, filter before slicing, preserve count and CLI behavior. Then fan out **independent** reports:

1. Investigator A owns evidence about `integer()`, `Product` and validation callers in `src/catalog.py`; report path:line, observed defect vs hypothesis, one negative test.
2. Investigator B owns filter/pagination semantics for `list_products` and `PRODUCTS`; report total/offset example, observed current behavior and an oracle assertion.
3. Investigator C owns API/CLI contract and tests (`handle_request`, `main`, `tests/test_catalog.py`); report accepted vs rejected inputs and missing regression.

All three may *read* the same file; none owns writes. Each output must state **assumption, evidence citation, consequence, proposed check, uncertainty**. Dependency graph: A/B/C independent read → integrator reconciles disagreements and reviews plan → **one** owner edits `src/catalog.py`/`tests/test_catalog.py` → human inspects diff → separate trusted oracle executes. If workers disagree whether strings are valid, stop at the shared contract instead of asking parallel writers to resolve it by racing edits. A short sequential change or uncertain central-file ownership is a reason to **skip fleet**. Fleet changes concurrency and credits, not tool/path authorization. [source:cli-reference]

## Monitor, steer, stop

In an authorized CLI, `/fleet` toggles fleet mode; inspect `/tasks` before assigning work. The tasks dialog uses `Enter` for details/teleport, `a` to toggle **nested subagent levels**, `f` to show **finished** subagents and shells, `X` to kill an active task, `B` to promote a synchronous task to background, and `R` to remove a finished task. A queued Ctrl+Q message can steer later work; while inside a subagent view, you can send it a direct correction. None of these retroactively undoes an edit. Shell-process list/read/write/stop APIs are distinct from agent tasks and may have separate tool permissions; do not conflate a shell log with a worker finding. Esc twice can stop active/background work but inspect cleanup and private output before resuming or leaving the CLI. [source:cli-reference]

The integrator records worker attribution and the final acceptance exits. No fleet run occurred in this repository: only the read-only exercise contract and offline checks exist. [Scenario H](../scenarios/H-fleet.md) provides a task prompt; [permissions](permissions.md) explain enforcement.
