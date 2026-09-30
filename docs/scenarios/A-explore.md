# A — Explore before editing

## Goal and prerequisites

Trace why `True` is accepted as an integer offset before requesting a repair. Python 3 and repository root suffice for offline prep; an optional Copilot prompt needs an entitled developer. Host: local, no GitHub remote.

## Start and deterministic check

```sh
python3 -B -m scripts.lab setup /tmp/scenario-a --state /tmp/checkpoint-state --exercise validation
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-a validation
```

Record the expected failing oracle and ownership ID. Inspect `src/catalog.py` and `tests/test_catalog.py`. **Optional authorized start:** `copilot -C /tmp/scenario-a --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob`; inspect `/env` and `/permissions`. **Prompt:** “Trace `integer()` through `Product`, `list_products`, `handle_request` and CLI. Cite paths/lines; separate observed bug from hypothesis. No edits or shell.”

## Checkpoints, effects and exit

**Checkpoint:** cited shared boundary and negative-test gap; no edited file. **Verification:** rerun the external `validation` oracle: it remains failing until a human repairs the copy; a unchanged failure is not a pass. **Permissions:** actual read-only tool visibility and reviewed cwd, not prose; `--disallow-temp-dir` removes the automatic temp grant but does not deny approved cwd under `/tmp` or create OS isolation. **External effects:** private fixture and optional credits only. **Escape:** unexpected write, credential or network request → stop and clean only by recorded ID. **Claude analogy/difference:** Explore habit transfers, but Copilot tool visibility and path trust are separate. [source:cli-reference] [claim:selective-tools] Version 1.0.89 help/source reviewed; no authenticated run.
