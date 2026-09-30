# A — Explore before editing

**Goal:** find why `True` is accepted as an integer without changing code. Use the new validation lab and exact PowerShell/zsh `check` commands from [first 15 minutes](../start/first-15-minutes.md); initial check must exit 1.

Launch Copilot with the lesson's read-only `view,grep,glob` command. Check `/env`, `/instructions`, `/permissions`; ask: “Trace `integer()` through `Product`, `list_products`, `handle_request` and CLI; cite the guard and its callers by file and line. No edits or shell.” **Expected:** a citation to `not isinstance(value, int)` and an explanation that `bool` passes. Compare source yourself; a plausible answer is not a code change. The check should still fail afterward. Next: [M debug](M-debug.md) or finish the repair in [first 15 minutes](../start/first-15-minutes.md).

## Goal and prerequisites

Use the configured lab and Python 3.12+.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** use the investigation above. **Checkpoint:** source citations. **Verification:** validation still exits 1. **Permissions:** read tools only. **External effects:** optional model credits. **Escape:** stop on unexpected tools. **Claude analogy:** Explore before edit. [source:cli-reference]
