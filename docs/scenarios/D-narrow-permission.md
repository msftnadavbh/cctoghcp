# D — Narrow permission and an expected block

## Goal and prerequisites

Demonstrate read-tool visibility versus approval; optional entitled **interactive** CLI on owned validation copy. No Git remote or privileged environment.

## Start and deterministic check

```sh
python3 -B -m scripts.lab setup /tmp/scenario-d --state /tmp/checkpoint-state --exercise validation
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-d validation
```

**Optional authorized start:** `copilot -C /tmp/scenario-d --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob --allow-tool=read`. **Prompt:** “Identify the boolean-offset defect and cite a caller; no edits. Explain why an edit request requires another visible tool.” Then request a proposed edit *without changing visibility* and observe; stop before any additional grant. The `read` permission kind is in the programmatic reference but omitted from the captured permissions-help list; no CLI block was runtime verified. [claim:selective-tools]

## Checkpoints, effects and exit

**Checkpoint:** findings and untouched file. **Verification:** initial oracle remains failing; edit should be blocked by unavailable tools, but this **expected block is UNTESTED**, not an observed result. **Permissions:** visible tools, invocation, cwd and temp access are different; flag does not sandbox a cwd under `/tmp`. **External effects:** local copy and optional credits only. **Escape:** if UI requests a grant or differs, stop, never switch to `--allow-all`. **Claude analogy/difference:** same least-privilege intent as Claude, different relative `write(path)` and shell rules. [source:programmatic-reference] 1.0.89 source/help; no paid test.
