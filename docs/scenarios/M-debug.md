# M — Fix the shared boundary once

Start at the [first-lesson validation lab](../start/first-15-minutes.md): record initial check exit 1 and identify all `integer()` callers with read tools. Then restart Copilot with `edit` available and ask: “Replace the shared boolean-accepting guard with exact integer validation; only edit `src/catalog.py` and focused `tests/test_catalog.py`. Preserve valid offsets/limits; no shell or code execution.” Approve specific writes. Before executing code, inspect `practice.py diff` for **all** files. Run `practice.py check` for `validation` and record exit 0 plus `Independent acceptance passed: validation`; if it still exits 1, diagnose the shared guard rather than patching one CLI caller. Next: [first hour](../start/first-hour.md).

## Goal and prerequisites

Use the broken validation lab with recorded failing check.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** repair shared guard above. **Checkpoint:** inspect all diffs. **Verification:** validation exits 0. **Permissions:** reviewed edit only. **External effects:** local edits and optional credits. **Escape:** stop on unexpected path. **Claude analogy:** debug the root cause. [source:cli-reference]
