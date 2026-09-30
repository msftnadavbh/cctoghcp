# B — Plan the in-stock feature

## Goal and prerequisites

Agree on filter semantics before editing; Python 3, repository root, **fresh** baseline copy. No Git remote needed. This copy does not contain the prior repaired validation exercise.

## Start and deterministic check

```sh
python3 -B -m scripts.lab setup /tmp/scenario-b --state /tmp/checkpoint-state --exercise in-stock
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-b baseline
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-b in-stock
```

Baseline passes; `in-stock` fails before implementation. **Optional authorized start:** `copilot -C /tmp/scenario-b --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob`; inspect `/env`, then `/plan`. **Prompt:** “Plan optional `in_stock=None|bool` for `list_products` and `handle_request`, CLI `--in-stock true|false`, filter before offset/limit, preserve totals, reject ints/strings. Cite source/tests, produce plan only with acceptance and rollback, no edits.” Edit plan via Ctrl+Y where supported.

## Checkpoints, effects and exit

**Checkpoint:** human-reviewed [twelve fields](../workflows/planning.md), negative cases, owner of `src/catalog.py` and `tests/test_catalog.py`; plan does not imply success. **Verification:** before edits, feature oracle still fails and baseline passes; compare actual exits. **Permissions:** only read tools; plan mode itself is not OS read-only and temp flag is not isolation. **External effects:** owned copy and optional credits. **Escape:** unexpected network/storage scope or write request → stop and revise plan. **Claude analogy/difference:** Claude planning maps to Copilot plan review, not `/goal` persistence. [source:cli-reference] Version 1.0.89 help only, no product runtime test.
