# M — Debug bool-as-int at the shared boundary

## Goal and prerequisites

Fix root cause rather than only a CLI symptom. New owned validation copy, Python 3; optional entitled Copilot, no remote.

## Start and deterministic check

```sh
python3 -B -m scripts.lab setup /tmp/scenario-m --state /tmp/checkpoint-state --exercise validation
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-m validation
```

Record expected initial failure. **Optional authorized start:** `copilot -C /tmp/scenario-m --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob,edit`; inspect `/env` and manual `/permissions`. **Prompt:** “Trace every `integer()` caller, repair shared bool guard only as needed, add regression for `True`/valid integers, preserve pagination; present diff and do not run code.”

## Checkpoints, effects and exit

**Checkpoint:** one owner, only `src/catalog.py`/focused test change. **Verification:** human reviews actual diff first, then external `validation` and `baseline` oracles exit 0; failing-before and passing-after recorded separately. **Permissions:** reviewed edit requests, no agent shell/network; temp flag does not deny approved `/tmp` cwd. **External effects:** local edit and optional credits. **Escape:** unreproduced bug or unexpected file → stop, don't speculative-refactor. **Claude analogy/difference:** same debug loop, independent external oracle outranks model assertion. [source:cli-reference] v1.0.89 source only, no runtime invocation.
