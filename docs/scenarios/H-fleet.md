# H — Three read-only investigations, one editor

Use the repaired lab from [first hour](../start/first-hour.md); its in-stock check should exit 1. Launch Copilot with `view,grep,glob` and inspect permissions. If `/fleet` is available, ask for three **read-only** reports: A validation callers, B filtering/pagination semantics, C request/CLI negative cases. Require each to cite path:line, state uncertainty and propose a check. Inspect `/tasks` and compare findings with source; the reports should not edit files or make `in-stock` pass. Reconcile disagreements before assigning a *single* editor; inspect the resulting diff before running first-hour checks. For a two-line repair, skip fleet. [Fleet guide](../workflows/fleet-and-subagents.md).

## Goal and prerequisites

Use the repaired lab with failing in-stock check.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** three read tasks above. **Checkpoint:** reconcile reports. **Verification:** no edits before integration. **Permissions:** read tools. **External effects:** parallel credits. **Escape:** serialize uncertain work. **Claude analogy:** teams need one editor.
