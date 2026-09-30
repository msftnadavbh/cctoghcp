# S — Resume without trusting old context

In the [first-lesson lab](../start/first-15-minutes.md), record the actual validation exit and your lab path, changed files, approvals and open decision. Exit Copilot and run `copilot --resume` to select the correct session; don't assume `--continue` is scoped to this lab. Once resumed, inspect `/cwd`, `/env`, `/permissions`, `/tasks` and current source. Ask: “Restate the agreed validation task and remaining check from current files; do not edit until it matches the handoff.” **Expected:** either matching state or a reason to stop and re-plan; a resume doesn't change code or pass the checker. [Nine-field handoff](../workflows/sessions-and-context.md).

## Goal and prerequisites

Use an existing Copilot lab session and handoff.

## Start and deterministic check

```sh
copilot --resume
```

## Checkpoints, effects and exit

**Prompt:** restate handoff above. **Checkpoint:** verify cwd and files. **Verification:** run check separately. **Permissions:** inspect grants anew. **External effects:** optional credits. **Escape:** pick correct session. **Claude analogy:** latest needn't match cwd. [source:cli-reference]
