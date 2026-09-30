# T — Inert hook and independent gate

## Goal and prerequisites

Test local handler parsing without registering Copilot dispatcher hooks. Python 3; validator libraries for static check, no auth or plugin.

## Start and deterministic check

```sh
python3 -B -m unittest discover -s tests -p 'test_hooks.py'
python3 -B -m scripts.validate --static-only
```

Review [native](../../examples/hooks/native.json), [shared](../../examples/hooks/shared-settings.json), [payload](../../examples/hooks/payloads/native.json) and absolute trusted launcher. **Optional read-oriented prompt for an authorized separate session:** “Compare native `toolArgs`, compatible `tool_input`, required cwd/event and dispatcher timeout. Do not register a hook.”

## Checkpoints, effects and exit

**Checkpoint:** handler tests pass; post-edit check parses accepted nested Python path and scans secrets, **never executes it**. **Verification:** unit-test exit plus independent CI, not a Copilot dispatcher test. Handled post errors exit 0 with context; static success is not acceptance. **Permissions:** pre demo policy denies malformed/unknown/shell/patch; choose native **or** shared only after explicit approval. **External effects:** local offline tests only, no dispatcher integration. **Escape:** on unexpected payload/log failure deny or annotate, inspect diff then independent CI; dispatcher timeout can fail open. **Claude analogy/difference:** hooks share lifecycle concept but native/compatible payload and failure semantics differ. [source:hooks-reference] [claim:hook-timeout] Source review and local unit tests only.
