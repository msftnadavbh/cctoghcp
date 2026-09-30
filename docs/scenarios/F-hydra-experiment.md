# F — Optional HydraFusion research-preview comparison

## Goal and prerequisites

Measure acceptance, latency and credits rather than guess which underlying model ran. Two clean copies, explicit paid approval and preview eligibility are required; no GitHub source remote.

## Start and deterministic check

```sh
python3 -B -m scripts.lab setup /tmp/scenario-f-one --state /tmp/checkpoint-state --exercise in-stock
python3 -B -m scripts.lab setup /tmp/scenario-f-two --state /tmp/checkpoint-state --exercise in-stock
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-f-one in-stock
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-f-two in-stock
```

Both initially fail; neither has the injected validation defect, so don't compare against a previously repaired *different* exercise. **Optional authorized setup:** approve `/update` **separately** if needed (changes install); prefer `/settings experimental on` over deprecated `/experimental on`, inspect `/model`, select a supported pinned comparison versus visible Hydra *only if available*. **Prompt for both copies:** “Add optional `in_stock=None|bool` through list, request and CLI, filter before pagination, preserve totals and invalid-input behavior. Edit source/tests only; present diff before human-run oracle.” Use identical reviewed permissions on separate copies. [source:hydrafusion-announcement]

## Checkpoints, effects and exit

**Checkpoint:** record actual version, eligible mode, equal task revision, elapsed time, human corrections, oracle exits and `/usage` credits; **leave cells blank until measured**. Internal Single/Cascade/Critique route remains unknown from user-visible text. **Verification:** human reviews both diffs before running each oracle; equal acceptance, no prefilled winner. **Permissions:** bounded edits and no remote writes; temp access, account and soft credit budget need independent review. **External effects:** preview model calls can consume credits/time. **Escape:** if preview missing or budget unapproved, record unavailable and do only offline prep. **Claude analogy/difference:** pin/Auto/fleet are different from research-preview multi-model routing. [claim:hydrafusion-preview] v1.0.89 help and announcement, no preview run.
