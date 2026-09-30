# K — Existing CLAUDE.md and conflicting scope

## Goal and prerequisites

Compare discovered vs attached instructions; repo root contains maintenance CLAUDE.md, while [coexistence fixtures](../../examples/coexistence/CLAUDE.md) deliberately conflict. Python 3 for passive inspection; optional authorized Copilot, no Git remote.

## Start and deterministic check

```sh
python3 -B -m scripts.inventory . --json
python3 -B -m scripts.validate --static-only
```

**Optional authorized start:** `copilot -C examples/coexistence --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob` only after reviewing parent/fixture instructions. **Prompt:** “Report instruction files actually attached at fixture root and `packages/catalog`; compare a nonmatching path, identify contradictions, make no edits.” Inspect `/instructions` and `/env`; a second session with different cwd may be needed to test nested scope.

## Checkpoints, effects and exit

**Checkpoint:** record version, exact attached paths, matching/nonmatching result; static inventory alone establishes *nothing* about precedence. **Verification:** offline check only validates fixtures/links, not runtime attachment. **Permissions:** read tools only, temp flag no OS isolation. **External effects:** optional credits, no plugin/hooks. **Escape:** human resolves conflicts, not guessed priority. **Claude analogy/difference:** CLAUDE.md remains useful; modern Claude versions may also support AGENTS.md, so renaming isn't mandatory. [source:instructions-reference] [claim:rules-added] Release support v1.0.89, precedence untested.
