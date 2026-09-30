# G — Choose a model without changing the contract

In the [first-lesson validation lab](../start/first-15-minutes.md), record the failing check. Start Copilot with read tools and inspect `/env`, then `/model`; choose a named model **only if your account permits it**. Ask: “Locate the smallest shared guard causing boolean pagination inputs to pass; cite callers and tests. Do not edit.” Check the source citations and `/usage`; model choice does not turn an explanation into a repaired program. **Expected:** validation still exits 1 until you approve an edit, review diff and run the check. Use Auto in a separate trial if you want a comparison, not as an inferred model pin. [Model choices](../workflows/models-and-hydrafusion.md).

## Goal and prerequisites

Use the validation lab and an eligible account.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** find the shared guard above. **Checkpoint:** selected model noted. **Verification:** check still fails before repair. **Permissions:** read only. **External effects:** optional credits. **Escape:** don't force unavailable models. **Claude analogy:** selection does not certify correctness.
