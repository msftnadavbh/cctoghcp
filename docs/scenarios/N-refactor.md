# N — Refactor without changing observable behavior

Create a **fresh** lab path outside the book using `practice.py setup PATH --exercise refactor --with-config` (PowerShell `python -I -B $Practice`, macOS zsh `python3 -I -B "$Practice"`; see [first-lesson variables](../start/first-15-minutes.md)). It must not exist already. `practice.py check PATH --exercise refactor` should exit 0 before editing.

In Copilot with `view,grep,glob,edit` and manual approvals ask: “Extract item serialization to one pure function in `src/catalog.py`; preserve `items,total,offset,limit`, request and CLI output; focused tests only; no new modules or shell.” Check the current file and approve scoped edits. Inspect `practice.py diff PATH` **before** executing revised code, then run `practice.py check PATH --exercise refactor`. **Expected:** exit 0 both before and after; a change in JSON fields or ordering is a regression. Keep the new path in a separate shell variable so it cannot overwrite the first lesson's `$Lab`/`Lab`.

## Goal and prerequisites

Create a new refactor lab; don't overwrite the first.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** pure serializer above. **Checkpoint:** review full diff. **Verification:** refactor check exits 0 before and after. **Permissions:** two editable files. **External effects:** lab edit and credits. **Escape:** revert owned regression. **Claude analogy:** preserve observed behavior.
