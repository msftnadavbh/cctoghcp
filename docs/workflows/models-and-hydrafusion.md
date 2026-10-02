# Model decisions, Auto and HydraFusion research preview

`/model` or `--model MODEL` selects from models **available to your account and enterprise policy**. `/model auto` selects Auto routing, with an `efficiency`, `balance` or `intelligence` profile where supported. [HydraFusion](https://github.blog/ai-and-ml/github-copilot/project-hydrafusion-frontier-quality-via-multi-model-orchestration/) is a **research preview**, separate from Auto. Its Single, Cascade and Critique modes may use different underlying work, cost and latency; the final answer does not reveal its internal route.

Do not hard-code model names into durable workflow instructions. Model names, release status and org availability change frequently. Define task profiles first, then map those profiles to the models currently available to your users and policy. It is still useful to name the current candidate models in a pilot plan so reviewers know what you tested.

| Option | Choose it when | Check |
| --- | --- | --- |
| Pinned model | You want a specific available model | Use `/model`, then check its context and `/usage` |
| Auto | You prefer routing among eligible models | Choose `/model auto` and, where offered, a profile |
| HydraFusion (research preview) | You explicitly choose to try the preview and it appears in `/model` | If needed, enable `/settings experimental on`; watch `/usage` |

`/rubber-duck` requests critique and `/fleet` distributes work across agents; neither selects HydraFusion's internal mode.

## Use task profiles, not fixed model names

| Profile | Use when | Example current mapping |
| --- | --- | --- |
| Default / Auto | The task is a normal planning, editing or review workflow | Start with `/model auto` where available |
| Efficient / cost-optimized | The task is repetitive, medium-complexity or cache-heavy | Consider a low-cost approved model such as GPT Luna, if visible and quality is acceptable |
| Reasoning-heavy | The task involves hard debugging, architecture, legacy code or security planning | Consider a stronger approved reasoning model such as GPT Sol or Claude Opus/Sonnet, depending on availability |
| Orchestration / preview | The task is an explicit experiment with multi-step orchestration | Consider HydraFusion only when visible, approved and budgeted |

These examples are intentionally current-state examples, not permanent routing rules. This keeps the workflow stable when new models appear or old names change. If a model you expect is absent, treat it as an availability/policy issue first, not as a prompt problem.

## Model, cache and effort for completed work

Compare **completed reviewed tasks** as well as per-prompt prices. Auto considers task complexity, availability, account policy and natural cache boundaries; on supported surfaces a paid plan qualifies for a documented 10% model-cost discount. Choose for task fit first. A model switch cannot reuse the earlier model's cache; inactivity, a change of reasoning effort or context size, and changes to enabled tools/MCP may also invalidate it. Resuming a session does not promise a warm cache. Configure tools and supported effort before a focused phase when practical, but escalate when the task needs more capability despite cache loss. More effort can consume more tokens without changing answer length; the reasoning display alone cannot measure reasoning usage. Cached input has model-specific pricing; some OpenAI and Anthropic models charge for cache writes. Check [live model pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing), [token economy](token-economy.md) and `/usage` against actual results before changing a team workflow.

HydraFusion's Single (one model), Cascade (draft then possibly escalate) and Critique (draft, independent critic, revise) patterns aggregate model and stage usage. The announcement's cost/quality comparisons are **vendor-controlled offline evaluations**; results in another checkout can differ. If you choose to compare it, the optional exercise below covers approval and validation. HydraFusion orchestrates models within its preview; Auto selects a model, `/rubber-duck` requests critique, and `/fleet` runs parallel subagents.

## Try a model comparison

1. Use separate clean copies of the same task and run their baseline checks first. Keep the prompt, permissions, file boundary and acceptance check identical.
2. Check `/model` and your credit budget. Only if you choose to try the preview, enable it through `/settings experimental on` where supported and check `/model` again. If unavailable, skip it. `/update` changes your installation and requires separate approval.
3. Compare a pinned model or Auto against the preview in separate copies. Review each diff and run the same local checks. Record model choice, elapsed time, corrections and `/usage`; budget for underlying work and stop if cost or latency exceeds your limit.

Return to an available pinned model when the preview is absent or unsuitable. [Optional comparison exercise](../scenarios/F-hydra-experiment.md).
