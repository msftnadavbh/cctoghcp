# T — Keep hooks inert during the first task

The first-lesson `--with-config` lab copies no hooks. Review the example [native hook config](../../examples/hooks/native.json), [payload](../../examples/hooks/payloads/native.json) and [hook guide](../customization/hooks.md). In a read-only Copilot session ask: “Compare hook pre/post behavior and failure cases; do not register any hook.” **Expected:** no hook runs and `practice.py check` remains the independent validation step after diff review. The bundled hook handlers and launcher are advanced POSIX workflows; a passing local handler unit test does not establish Windows-native Copilot dispatcher behavior. Do not activate hooks as a way around manual review or a failing check.

## Goal and prerequisites

Use inert examples; no hook registration.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** compare hooks above. **Checkpoint:** no registration. **Verification:** independent practice check. **Permissions:** read tools. **External effects:** optional credits. **Escape:** stop on activation request. **Claude analogy:** hooks don't replace validation.
