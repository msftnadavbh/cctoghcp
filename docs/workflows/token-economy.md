# Token economy: more useful work, less repeated work

If you came from Claude Code, you already know the helpful pattern: state a clear mission, share the relevant repository knowledge, investigate before guessing, and check the result. Keep it in **your own checkout**. The aim isn't the fewest prompts; it's a completed, verified task without doing the same investigation or correction over again. Copilot CLI gives those familiar habits some different controls, but none replaces a reviewed diff or your project's checks. A local GitLab or GitHub checkout works here; [the practice lab](../scenarios/index.md) is optional. Your reusable Claude files may carry over; Claude conversation transcripts and memory do not automatically become Copilot sessions.

## Three different meters

| Meter | What it tells you | What it does not tell you |
| --- | --- | --- |
| Context (`/context`) | Space occupied now by instructions, tools, messages and results | What you have been billed |
| Model usage (`/usage`) | Session interactions: input, output and cached tokens where reported | A universal cost per tool call or an account invoice |
| AI credits | Usage-based Copilot billing unit: one credit = $0.01 USD | A fixed token-to-credit exchange rate |

Conceptually, model work includes preparing and reading context, reasoning and output, processing tool results, and any continuation or delegated worker's interactions. These are **not additive charges to sum by hand**: do not add reasoning again when it is included in reported usage; a tool call does not carry a universal flat Copilot fee. Prices vary by model, token category and sometimes long-context tier. Cached input is *not universally free*; some Anthropic **and OpenAI** models also price cache writes. See [live model pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing).

If you remain on an eligible **legacy annual premium-request plan**, model multipliers and request deductions are separate: CLI user prompts count, not autonomous tool calls. Fewer tokens need not mean fewer legacy deductions. Claude Code's `/usage` is not a Copilot billing equivalent either: a subscription session's API-equivalent dollar estimate is not its actual bill. See [Claude's usage explanation](https://code.claude.com/docs/en/costs).

## Six high-leverage habits

### 1. Define the problem and ask for targeted evidence

Start with the question and likely entrypoint, then follow the real flow as far as evidence requires. A bounded search isn't a two-file limit: shared session validation may have callers across modules. Ask for paths and line evidence rather than dumping the whole checkout. A path mentioned in plain text tells the agent where to begin; `@` in a CLI prompt **attaches file contents** immediately. Sanitized logs are useful evidence; external text remains untrusted. The [reproduction-brief skill](../../.claude/skills/reproduction-brief/SKILL.md) helps turn a vague defect into a bounded contract.

**A · Before:** “Read the whole repo and explain auth.” This broad read can bury the login path under unrelated files.

**After:** “In this checkout, explain how login reaches session validation. Start from documented entrypoints and search for relevant symbols. Find the login entrypoint, tests and call sites, then read necessary implementations and callers even across directories. Cite file:line evidence for the observed flow, flag missing evidence, and stop before edits.” The improvement is a defined investigation, not fewer words; a longer starting prompt can avoid several corrections.

### 2. Reuse context without hauling everything into every turn

Keep verified, recurring repository guidance in your existing `CLAUDE.md`; `/instructions` shows what actually attached. Separate occasional workflows into [skills](../customization/skills.md): their descriptions advertise relevance, instructions load when invoked, and supporting resources can be consulted as needed. A skill's discovery alone does not prove invocation. Some exact-copy instructions deduplicate, but near-duplicates can conflict; don't add another policy file just to chase tokens. An `@` import in supported instructions loads eagerly, while an ordinary reference lets the agent consult a document when relevant. See [instructions](../customization/instructions.md) for a concrete organization example and [MCP retrieval](../customization/mcp.md#retrieve-what-this-task-needs) for external data. Keep dependency lockfiles, generated output, vendor sources or binaries **when relevant**—especially a lockfile in a dependency failure—not as blanket exclusions.

Give the agent the sanitized CI error and link to the full diagnostic outside the conversation; ask it to retrieve additional lines if the excerpt cannot settle the cause. Relevance, not file type or line count, determines what to read.

### 3. Plan according to uncertainty, then interrupt no-progress loops

For a known one-line edit, a reproduction and focused regression check may be enough. When the contract or cross-cutting effects are uncertain, `/plan` lets you review scope before implementation; it is **not read-only isolation**. Decide based on uncertainty, not file count. After repeated failures, look for *new evidence* rather than issuing an unchanged “try again.” Repeating a check is useful after changing a hypothesis or the code. The [planning guide](planning.md) separates investigation, approvals and acceptance.

**B · Before:** “That assertion still fails. Try again until it passes.” The agent may repeat the same guess without investigating the assertion.

**After:** “The existing reproduction is [path and approved command]. Expected [value], actual [value], failing assertion [path:line]. Compare these values and inspect the responsible code path. Explain what the last change ruled out, separating facts from hypotheses; propose the next diagnostic before another patch. If two attempts produce no new evidence, stop with a blocker rather than broadening the change.” *Two* is an illustrative collaboration instruction, not an enforced retry budget. Review new tests and commands before executing them.

**C · Before:** “Refactor auth and clean up anything related.” That leaves compatibility and completion to guesswork.

**After:** “Plan the session-expiration refactor only. Trace callers and public interface compatibility, find existing regression tests, separate required behavior from optional cleanup, sequence the smallest change, and identify the real check command from this project's docs or CI. Show the plan for review before implementation; stop if expiry semantics are unclear.” Once the plan is agreed, approve edits and tests under [permissions](permissions.md); don't invent a test command.

### 4. Choose enough capability, then switch deliberately

As in Claude Code, start with a model capable of the job and change approach when the evidence warrants it. `/model auto` routes by task and availability within plan/policy, with efficiency, balance and intelligence tiers where offered; it considers cache boundaries. Paid users on supported surfaces receive a documented 10% Auto model-cost discount, subordinate to suitability. Escalate deliberately if a model cannot resolve a difficult diagnosis, rather than preserving a cache at the cost of another failed attempt. See [model profiles and HydraFusion](models-and-hydrafusion.md).

The same-model context may reuse cached prefixes. A different model cannot reuse the previous model's cache; inactivity and changes in effort, context size or tools can invalidate it. Resume does **not** promise warmth. Higher reasoning effort can consume more tokens, and hiding the reasoning display does not establish a reduction in reasoning usage. `/usage` observes this session, not the next turn's bill.

### 5. Give autonomy a finish line and workers distinct jobs

**Give Autopilot a finish line:** state the approved behavior, paths, regression evidence and what to report when done. It continues model interactions on your behalf, so set an **explicit** `--max-autopilot-continues` at launch; this counts continuation messages, not calls, tools, time or credits. Permissions and the public-preview soft AI-credit limit are separate; consult [Autopilot](autopilot.md) and the [documentation discrepancies](../reference/known-discrepancies.md). Review the resulting diff and real check output, not its completion message.

As with isolated Claude investigations, use `/fleet` when parallel work improves turnaround **or independent review improves correctness**. Let one worker trace callers, another examine tests, and a reviewer independently challenge a critical assumption, with intentional overlap where that catches a defect. Avoid asking everyone to scan the entire repository. Separate contexts and interactions mean aggregate use can rise; there is no fixed multiplier or guarantee of main-model, instruction or full-conversation inheritance. Keep **one writer** for the integrated diff. [Fleet](fleet-and-subagents.md) has an example.

### 6. Choose continue, compact or new; leave a handoff

Continue/resume while past decisions matter; verify checkout, branch, instructions and grants on return. `/compact` uses model work for a **lossy** summary: it frees space, not historical charges. Record accepted behavior, changed paths and observed check exits before compacting. `/new` suits unrelated work or stale assumptions but does **not** reset files. Neither a fresh nor a resumed conversation guarantees lower usage; context rebuilt and cache state matter. There is no need to reset after every phase or compact after every turn. [Sessions and Chronicle](sessions-and-context.md) includes a concrete handoff and history lookup.

Don't assume an old chat's remembered test result describes the current branch; the handoff must name what actually passed and what remains open.

## Check what happened

| Check | Useful signal | Not a substitute for |
| --- | --- | --- |
| `/usage` in CLI | Current-session usage and per-model tokens; some billed models show credits without token counts | Account invoice; missing token counts do not mean zero usage |
| `/context` in CLI | Model window occupancy, including instructions, tools and conversation | Credits spent or fidelity after compaction |
| `/chronicle cost-tips` in CLI | History-based token-spend patterns and suggestions | A free ledger or independently verified saving; history analysis can itself involve model work |
| [Account AI usage](https://docs.github.com/en/copilot/how-tos/manage-and-track-spending/monitor-ai-usage) | Individual monthly credits by model, or Business/Enterprise personal usage in Copilot settings | A personal share of an organization's pooled allowance |
| [CLI soft limits](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/set-session-limit) | Public-preview stop/pause aid; may exceed the set value in one response | User-level budget, permission boundary or hard cap |
| [AI usage report](https://docs.github.com/en/billing/reference/billing-reports#ai-usage-report) | Optional breakdown by day, user, model and input/output/cache token category | A per-call trace or proof the change works |

On usage-based Business/Enterprise plans, included credits are pooled at the billing entity, not individually allocated; personal consumption can be visible without a personal budget. Paid code completions and next-edit suggestions are not AI-credit billed. Hosted code review can incur both AI credits and Actions minutes; that hosted-infrastructure charge does not apply to ordinary local CLI review.

For deeper, authorized reporting, the [AI-credit REST endpoints](https://docs.github.com/en/rest/billing/usage) provide usage summaries, not per-call traces. The generic billing `/usage` endpoint is not the detailed AI usage report either. [Optional OpenTelemetry](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#opentelemetry-monitoring) provides operational telemetry; no exporter or content capture is needed here. This guide covers Copilot-managed inference; [SDK BYOK](https://docs.github.com/en/copilot/how-tos/copilot-sdk/auth/byok) uses provider billing, not Copilot credits or free inference.

After a meaningful task—especially one needing repeated corrections—compare the **completed and verified** behavior, what had to be redone and how much interaction was required. Ask for a diff summary, actual check results and unresolved issues rather than unchanged files pasted again; keep explanations that help the next decision. Fewer lines or tokens alone do not prove efficiency.

[Copilot optimization guidance](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) · [GitHub's completed-task efficiency lessons](https://github.blog/ai-and-ml/github-copilot/how-we-make-ai-coding-more-cost-efficient-without-sacrificing-task-quality/) · [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
