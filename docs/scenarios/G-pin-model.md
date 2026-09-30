# G — Pin a model for a reason

## Goal and prerequisites

Distinguish available model selection from behavioral correctness. Python 3 and an owned validation copy; optional account entitlement, no source remote.

## Start and deterministic check

```sh
python3 -B -m scripts.lab setup /tmp/scenario-g --state /tmp/checkpoint-state --exercise validation
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-g validation
```

**Optional authorized start:** `copilot -C /tmp/scenario-g --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob`. Inspect `/env`, then `/model`; select an account-permitted named model, or Auto in a *separate* trial. **Prompt:** “Identify the smallest shared guard for boolean pagination; cite tests, do not edit.”

## Checkpoints, effects and exit

**Checkpoint:** record visible model/context/credits without exposing enterprise allowlists. **Verification:** failing oracle remains before an edit; if a later human-approved repair occurs, inspect diff then both `validation` and `baseline` oracles must pass. **Permissions:** read tools only; switching models adds no write/shell grant; temp flag does not isolate cwd. **External effects:** optional credits only. **Escape:** unsupported model/tenant policy → offline investigation, not forced Hydra toggle. **Claude analogy/difference:** explicit pin resembles Claude selection; Auto and Hydra differ and a pin doesn't produce deterministic text. [source:cli-reference] Version 1.0.89 help, no model call.
