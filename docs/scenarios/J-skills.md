# J — Reuse a Claude skill

Use the configured [first-lesson lab](../start/first-15-minutes.md): it copies existing `.claude/skills`, not a second skill tree. Inspect `.claude/skills/repo-recon/SKILL.md` and `/skills` in the Copilot session. If visible, ask: “Use the discovered repo-recon skill to identify `integer()` callers and one negative test; cite current lab files; no edits.” **Expected:** a brief grounded in the same source as the first lesson; if the skill isn't visible, stop and check `/env` and workspace instead of assuming it ran. Validation stays failing until the fix. Optional plugin packaging and installation are separate from this skill reuse; [skills](../customization/skills.md).

## Goal and prerequisites

Use the configured lab and review skill text.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** request skill as above. **Checkpoint:** inspect discovery. **Verification:** check remains failing before fix. **Permissions:** read tools. **External effects:** optional credits. **Escape:** don't install a plugin to force discovery. **Claude analogy:** reuse project skills. [source:plugin-reference]
