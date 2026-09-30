# N — Single-file refactor with unchanged behavior

## Goal and prerequisites

Extract a named pure serializer *inside `src/catalog.py`*, not a package split; the acceptance child imports that one file in isolation. Python 3, new passing refactor copy, optional entitled Copilot.

## Start and deterministic check

```sh
python3 -B -m scripts.lab setup /tmp/scenario-n --state /tmp/checkpoint-state --exercise refactor
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-n refactor
```

**Optional authorized start:** `copilot -C /tmp/scenario-n --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob,edit`; inspect `/env` and manual `/permissions`. **Prompt:** “Extract item serialization to one named pure function in `src/catalog.py`, preserve `items,total,offset,limit` and CLI/request behavior, add only focused tests. Present diff before execution, no new modules or deps.”

## Checkpoints, effects and exit

**Checkpoint:** initial oracle passes; integration remains in one importable file. **Verification:** human inspects changed file and tests, then same refactor oracle passes after; compare serialized fields. **Permissions:** reviewed source/test edit requests, no agent shell; temp flag not a sandbox. **External effects:** owned copy and optional credits. **Escape:** changed observable behavior or abstraction hierarchy → revert owned refactor, not broaden probe contract. **Claude analogy/difference:** same minimal refactor intent, external acceptance independent of agent confidence. [source:cli-reference] v1.0.89 help only; offline oracle is real.
