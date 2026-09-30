# Model decisions, Auto and HydraFusion research preview

`/model` or `--model MODEL` selects from models **available to your account and enterprise policy**. `/model auto` selects Auto routing, with an `efficiency`, `balance` or `intelligence` profile where supported. [HydraFusion](https://github.blog/ai-and-ml/github-copilot/project-hydrafusion-frontier-quality-via-multi-model-orchestration/) is a **research preview**, separate from Auto. Its Single, Cascade and Critique modes may use different underlying work, cost and latency; the final answer does not reveal its internal route.

| Option | Choose it when | Check |
| --- | --- | --- |
| Pinned model | You want a specific available model | Use `/model`, then check its context and `/usage` |
| Auto | You prefer routing among eligible models | Choose `/model auto` and, where offered, a profile |
| HydraFusion (research preview) | You explicitly want a paid trial and the preview appears in `/model` | If needed, enable `/settings experimental on`; watch `/usage` |

`/rubber-duck` requests critique and `/fleet` distributes work across agents; neither selects HydraFusion's internal mode.

## Try a model comparison

1. Use separate clean copies of the same task and run their baseline checks first. Keep the prompt, permissions, file boundary and acceptance check identical.
2. Check `/model` and your credit budget. Only if you choose to try the preview, enable it through `/settings experimental on` where supported and check `/model` again. If unavailable, skip it. `/update` changes your installation and requires separate approval.
3. Compare a pinned model or Auto against the preview in separate copies. Review each diff and run the same local checks. Record model choice, elapsed time, corrections and `/usage`; budget for underlying work and stop if cost or latency exceeds your limit.

Return to an available pinned model when the preview is absent or unsuitable. [Optional comparison exercise](../scenarios/F-hydra-experiment.md).
