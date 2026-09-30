# B — Plan the stock filter

**Goal:** agree on a contract before editing. Use the repaired lab from [first hour](../start/first-hour.md), not a fresh validation copy. Its `validation` check should exit 0 and `in-stock` check should exit 1 using the platform commands on that page.

Start Copilot with `view,grep,glob` only; inspect `/env`, use `/permissions` to keep manual mode, then `/plan`. Ask: “Plan optional `in_stock=None|bool` for `list_products`, `handle_request` and CLI `--in-stock true|false`. Preserve `items,total,offset,limit` types, combine query and stock before pagination, preserve unfiltered output; reject ints, strings, lists, dicts and invalid CLI values with exit 2/stderr and no JSON stdout. Name callers, editable files, negative cases, checks and rollback. No edits.” Inspect the plan and adjust with Ctrl+Y where supported. **Expected:** `src/catalog.py` and focused `tests/test_catalog.py` only; a plan is not a passing feature. Next: [C implementation](C-plan-review-autopilot.md).

## Goal and prerequisites

Use the repaired lab, Python 3.12+ and an authorized Copilot session.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** plan as above. **Checkpoint:** reviewed contract. **Verification:** in-stock initially exits 1. **Permissions:** read tools. **External effects:** optional credits. **Escape:** stop on unrelated scope. **Claude analogy:** plan review is separate from implementation.
