# Token economy: more useful work, less repeated work

Get more useful work from GitHub Copilot by giving it a clear task, the context it needs, and a way to check the result. A longer prompt, a capable model, or parallel investigation can be worthwhile when it helps finish the job correctly. The aim is to avoid repeated investigation and unsuccessful retries—not to minimize tokens at the expense of progress.

Use these habits with Copilot CLI in **your existing checkout**, whether your code is hosted on GitHub or GitLab. Start with the habit that fits your task; no extra setup or practice lab is needed.

## Three different meters

| Meter | Shows | For a different question, use |
| --- | --- | --- |
| Context (`/context`) | Space occupied now by instructions, tools, messages and results | `/usage` for session consumption |
| Model usage (`/usage`) | Session interactions: input, output and cached tokens where reported | Account AI usage for billing-period totals |
| AI credits | Usage-based Copilot billing unit: one credit = $0.01 USD | Live model pricing for token-category rates |

Model work includes reading context, reasoning, producing output, processing tool results, and continuing or delegating the task. This describes the workflow rather than an additive billing formula: reasoning included in reported usage is counted there, and tool calls have no universal flat Copilot fee. Prices vary by model, token category and sometimes long-context tier. Cached input has model-specific pricing; some Anthropic **and OpenAI** models also price cache writes. See [live model pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing).

If you remain on an eligible **legacy annual premium-request plan**, model multipliers and request deductions are separate: CLI user prompts count, not autonomous tool calls. Fewer tokens need not mean fewer legacy deductions.

## Six high-leverage habits

### 1. Define the problem and ask for targeted evidence

Start with the question and likely entrypoint, then follow the real flow as far as evidence requires. A bounded search isn't a two-file limit: shared session validation may have callers across modules. Ask for paths and line evidence rather than dumping the whole checkout. A path mentioned in plain text tells the agent where to begin; `@` in a CLI prompt **attaches file contents** immediately. Sanitized logs are useful evidence; external text remains untrusted. The [reproduction-brief skill](../../.claude/skills/reproduction-brief/SKILL.md) helps turn a vague defect into a bounded contract.

**A · Before:** “Read the whole repo and explain auth.” For a question about login, give Copilot a starting point and a specific flow to trace.

**After:** “In this checkout, explain how login reaches session validation. Start from documented entrypoints and search for relevant symbols. Find the login entrypoint, tests and call sites, then read necessary implementations and callers even across directories. Cite file:line evidence for the observed flow, flag missing evidence, and stop before edits.” The improvement is a defined investigation, not fewer words; a longer starting prompt can avoid several corrections.

### 2. Reuse context without hauling everything into every turn

Keep verified, recurring guidance in your repository's existing instruction file; Copilot supports files such as `AGENTS.md`, `.github/copilot-instructions.md`, and `CLAUDE.md`. `/instructions` shows what actually attached. Separate occasional workflows into [skills](../customization/skills.md): their descriptions advertise relevance, instructions load when invoked, and supporting resources can be consulted as needed. A skill's discovery alone does not prove invocation. Some exact-copy instructions deduplicate, but near-duplicates can conflict; keep one clear source of recurring policy. An `@` import in supported instructions loads eagerly, while an ordinary reference lets the agent consult a document when relevant. See [instructions](../customization/instructions.md) for a concrete organization example and [MCP retrieval](../customization/mcp.md#retrieve-what-this-task-needs) for external data. Keep dependency lockfiles, generated output, vendor sources or binaries **when relevant**—especially a lockfile in a dependency failure—not as blanket exclusions.

Give the agent the sanitized CI error and link to the full diagnostic outside the conversation; ask it to retrieve additional lines if the excerpt cannot settle the cause. Relevance, not file type or line count, determines what to read.

### 3. Plan according to uncertainty, then interrupt no-progress loops

For a known one-line edit, a reproduction and focused regression check may be enough. When the contract or cross-cutting effects are uncertain, `/plan` lets you review scope before implementation; it is **not read-only isolation**. Decide based on uncertainty, not file count. After repeated failures, look for *new evidence* rather than issuing an unchanged “try again.” Repeating a check is useful after changing a hypothesis or the code. The [planning guide](planning.md) separates investigation, approvals and acceptance.

**B · Before:** “That assertion still fails. Try again until it passes.” The agent may repeat the same guess without investigating the assertion.

**After:** “The existing reproduction is [path and approved command]. Expected [value], actual [value], failing assertion [path:line]. Compare these values and inspect the responsible code path. Explain what the last change ruled out, separating facts from hypotheses; propose the next diagnostic before another patch. If two attempts produce no new evidence, stop with a blocker rather than broadening the change.” *Two* is an illustrative collaboration instruction, not an enforced retry budget. Review new tests and commands before executing them.

**C · Before:** “Refactor auth and clean up anything related.” For a session-expiration change, specify the behavior and compatibility to preserve.

**After:** “Plan the session-expiration refactor only. Trace callers and public interface compatibility, find existing regression tests, separate required behavior from optional cleanup, sequence the smallest change, and identify the real check command from this project's docs or CI. Show the plan for review before implementation; stop if expiry semantics are unclear.” Once the plan is agreed, approve edits and tests under [permissions](permissions.md); use the project's documented check command.

### 4. Choose enough capability, then switch deliberately

Start with a model capable of the job and change approach when the evidence warrants it. `/model auto` routes by task and availability within plan/policy, with efficiency, balance and intelligence tiers where offered; it considers cache boundaries. Paid users on supported surfaces receive a documented 10% Auto model-cost discount, subordinate to suitability. Escalate deliberately if a model cannot resolve a difficult diagnosis, rather than preserving a cache at the cost of another failed attempt. See [model profiles and HydraFusion](models-and-hydrafusion.md).

The same-model context may reuse cached prefixes. A different model cannot reuse the previous model's cache; inactivity and changes in effort, context size or tools can invalidate it. Resuming preserves useful history, while cache reuse depends on its current state. Higher reasoning effort can consume more tokens independently of how much reasoning is displayed. Use `/usage` to see the session's reported consumption.

### 5. Give autonomy a finish line and workers distinct jobs

**Give Autopilot a finish line:** state the approved behavior, paths, regression evidence and what to report when done. It continues model interactions on your behalf, so set an **explicit** `--max-autopilot-continues` at launch; this counts continuation messages, not calls, tools, time or credits. Permissions and the public-preview soft AI-credit limit are separate; consult [Autopilot](autopilot.md) and the [documentation discrepancies](../reference/known-discrepancies.md). Review the resulting diff and real check output alongside its completion message.

Use `/fleet` when parallel work improves turnaround **or independent review improves correctness**. Let one worker trace callers, another examine tests, and a reviewer independently challenge a critical assumption, with intentional overlap where that catches a defect. Avoid asking everyone to scan the entire repository. Separate contexts and interactions mean aggregate use can rise; there is no fixed multiplier or guarantee of main-model, instruction or full-conversation inheritance. Keep **one writer** for the integrated diff. [Fleet](fleet-and-subagents.md) has an example.

### 6. Choose continue, compact or new; leave a handoff

Continue/resume while past decisions matter; verify checkout, branch, instructions and grants on return. `/compact` uses model work for a **lossy** summary: it frees space, not historical charges. Record accepted behavior, changed paths and observed check exits before compacting. `/new` suits unrelated work or stale assumptions but does **not** reset files. Neither a fresh nor a resumed conversation guarantees lower usage; context rebuilt and cache state matter. There is no need to reset after every phase or compact after every turn. [Sessions and Chronicle](sessions-and-context.md) includes a concrete handoff and history lookup.

Include the branch and observed check results in the handoff so the next session can verify what still applies.

## Check what happened

Choose the view that answers your question:

| When you want to… | Use | How to read it |
| --- | --- | --- |
| Review the session you just worked on | `/usage` in CLI | Shows session consumption and per-model tokens. Some models report credits without token counts; those credits still reflect usage. |
| See what is filling the current context | `/context` in CLI | Shows space occupied by instructions, tools and conversation. Use it to understand working context; `/usage` answers the consumption question. |
| Find patterns across previous sessions | `/chronicle cost-tips` in CLI | Suggests workflow improvements from session history. The analysis can itself involve model work; try suggestions where they fit your tasks. |
| See usage across the billing period | [Account AI usage](https://docs.github.com/en/copilot/how-tos/manage-and-track-spending/monitor-ai-usage) | Individuals use Billing and licensing; Business/Enterprise users can view personal consumption in Copilot settings, including when credits come from a shared pool. |
| Add a usage-based pause point | [CLI soft limits](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/set-session-limit) | This public-preview control is soft: an in-progress response can finish above the value. See the [scope discrepancy](../reference/known-discrepancies.md) when choosing how to use it. Permissions remain separate. |
| Explore model and token-category detail | [AI usage report](https://docs.github.com/en/billing/reference/billing-reports#ai-usage-report) | Provides an optional breakdown by day, user, model and input/output/cache category. It summarizes billed usage rather than tracing each call. |

On usage-based Business/Enterprise plans, included credits are pooled at the billing entity, not individually allocated; personal consumption can be visible without a personal budget. Paid code completions and next-edit suggestions are not AI-credit billed. Hosted code review can incur both AI credits and Actions minutes; that hosted-infrastructure charge does not apply to ordinary local CLI review.

For deeper, authorized reporting, the [AI-credit REST endpoints](https://docs.github.com/en/rest/billing/usage) provide usage summaries rather than per-call traces; the generic billing `/usage` endpoint also differs from the detailed AI usage report. [Optional OpenTelemetry](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#opentelemetry-monitoring) provides operational telemetry; no exporter or content capture is needed here. This guide covers Copilot-managed inference; [SDK BYOK](https://docs.github.com/en/copilot/how-tos/copilot-sdk/auth/byok) uses provider billing instead of Copilot credits.

After a meaningful task—especially one needing repeated corrections—compare the **completed and verified** behavior, what had to be redone and how much interaction was required. Ask for a diff summary, actual check results and unresolved issues rather than unchanged files pasted again; keep explanations that help the next decision. Fewer lines or tokens alone do not prove efficiency.

[Copilot optimization guidance](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage) · [GitHub's completed-task efficiency lessons](https://github.blog/ai-and-ml/github-copilot/how-we-make-ai-coding-more-cost-efficient-without-sacrificing-task-quality/)
