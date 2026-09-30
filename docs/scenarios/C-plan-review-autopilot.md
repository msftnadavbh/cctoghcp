# C — Reviewed plan, then bounded continuation

Use [B's](B-plan.md) human-reviewed plan in the **same repaired lab**. Recheck: `validation` exits 0, `in-stock` exits 1, using [first-hour commands](../start/first-hour.md). With manual permissions and `view,grep,glob,edit` available, inspect `/env` and `/permissions` before enabling `/autopilot`.

Ask: “Implement only the approved `in_stock` contract in `src/catalog.py` and `tests/test_catalog.py`. Filter before pagination, preserve prior behavior, and reject invalid values. No shell, network or other files. Finish by showing a diff and naming tests for a human to run; stop on unexpected requests.” Inspect `/tasks` and every requested edit. After `/exit`, review `practice.py diff` before running **both** checks from first hour. **Expected:** zero exits only after valid implementation. Esc interrupts but doesn't undo edits; do not widen a refused grant. [Autopilot details](../workflows/autopilot.md).

## Goal and prerequisites

Use B's reviewed plan in the same lab.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** bounded task above. **Checkpoint:** inspected diff. **Verification:** two passing checks after review. **Permissions:** manual edits only. **External effects:** credits and lab edits. **Escape:** stop on new paths. **Claude analogy:** autonomy and permission are separate. [source:cli-reference]
