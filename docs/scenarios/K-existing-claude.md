# K — Retain your existing CLAUDE.md

In the `--with-config` [first-lesson lab](../start/first-15-minutes.md), inspect `CLAUDE.md` and the file referenced by its `@` import. Start Copilot with read tools and check `/instructions` and `/env`; ask: “Which repository instructions are attached? Cite only the paths; do not edit.” **Expected:** existing guidance attached if discovery works for your version; if not, inspect workspace and policy rather than writing a duplicate file. A static file check cannot establish instruction precedence. For a nested-scope example, read the [coexistence sample](../../examples/coexistence/CLAUDE.md) and compare how a matching `packages/catalog` task differs from a nonmatching one in a separately reviewed session. [Instructions](../customization/instructions.md).

## Goal and prerequisites

Use the configured lab with reviewed instructions.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** report attachment above. **Checkpoint:** note paths. **Verification:** compare attached files, not mere presence. **Permissions:** read tools. **External effects:** credits. **Escape:** stop on contradictory policy. **Claude analogy:** retain CLAUDE.md. [source:instructions-reference]
