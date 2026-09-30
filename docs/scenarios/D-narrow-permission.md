# D — See what a read-only tool set actually allows

Use the [first-lesson validation lab](../start/first-15-minutes.md) before the repair (initial check exits 1). Start with that page's `view,grep,glob` Copilot command. Inspect `/permissions`, then ask: “Identify the boolean defect; cite a caller. Propose—but do not perform—a repair.” Request an edit proposal without restarting with edit available. **Expected:** the tool set has no edit or shell tool; compare actual client behavior instead of assuming a specific denial message. The defect and failing check should remain. To make the repair, explicitly restart with edit available as in [first 15 minutes](../start/first-15-minutes.md), approve only the requested path and review diff before check. [Permissions](../workflows/permissions.md).

## Goal and prerequisites

Use the unrepaired validation lab.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** propose without edits. **Checkpoint:** no changed files. **Verification:** check still fails. **Permissions:** read tools. **External effects:** optional credits. **Escape:** don't broaden denied tools. **Claude analogy:** least privilege, different controls. [source:cli-reference]
