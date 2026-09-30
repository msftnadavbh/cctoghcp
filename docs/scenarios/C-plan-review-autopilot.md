# C — Reviewed plan then bounded autopilot

## Goal and prerequisites

Implement [scenario B](B-plan.md)'s *human-approved* `in_stock` plan in its existing `/tmp/scenario-b` copy. No remote; prior feature acceptance fails and baseline passes. Do not run setup again.

## Start and deterministic check

```sh
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-b in-stock
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-b baseline
```

**Optional authorized start:** `copilot -C /tmp/scenario-b --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob,edit,create`; inspect `/env` and manual `/permissions`, review `/plan` with Ctrl+Y, then toggle `/autopilot`. **Prompt:** “Implement only the approved `in_stock` contract in `src/catalog.py` and `tests/test_catalog.py`. Preserve existing behavior, stop on other files/network. Present diff and proposed checks for human review **before any code execution**.” A headless `--no-ask-user` variant is a separate untested recipe, not implied here.

## Checkpoints, effects and exit

**Checkpoint:** one integrator owns two paths; `/tasks` and `/diff` inspected. **Verification:** human reviews actual diff, *then* independently executes both oracles and records exits; only final zero/zero meets acceptance. **Permissions:** explicitly reviewed edit requests, no agent shell; temp flag and continuation cap do not constrain OS or credits. **External effects:** local edits, optional paid calls; no commit/push. **Escape:** Ctrl+Q can queue a correction; Esc twice stops turns, not changes; never widen a denied rule, reverse only owned edits. **Claude analogy/difference:** Copilot planning, autonomy and permissions are separate. [source:cli-reference] Source-only 1.0.89; no authenticated invocation.
