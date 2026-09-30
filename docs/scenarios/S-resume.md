# S — Resume with a nine-field handoff

## Goal and prerequisites

Avoid confusing saved conversation with current filesystem or Git remote. New owned validation copy, private handoff note and optional entitled CLI; no Git repository in copy.

## Start and deterministic check

```sh
python3 -B -m scripts.lab setup /tmp/scenario-s --state /tmp/checkpoint-state --exercise validation
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-s validation
```

Record expected failure and [nine handoff fields](../workflows/sessions-and-context.md): objective, copy/ownership and session ID, baseline, files, checks/exits, grants, external effects, unresolved decision, next action. **Optional authorized resume:** `copilot -C /tmp/scenario-s --resume=REVIEWED_SESSION_ID --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob` after confirming the selected ID; `/resume` picker is alternative. **Prompt:** “Restate the handoff and inspect the current files first; no edit until state matches.”

## Checkpoints, effects and exit

**Checkpoint:** `/cwd`, `/env`, mode, task list and actual file match note. **Verification:** oracle remains failing until separately reviewed repair; `/compact`, `/new`, `/fork` do not change code, and `/fork worktree` needs a real Git repo. **Permissions:** read tools; `--no-remote-export` disables export/control, temp flag removes automatic temp access not approved cwd. **External effects:** optional credits/session state, no remote. **Escape:** wrong session → stop/select explicit ID; `/rewind` cannot undo remote actions. **Claude analogy/difference:** Claude continue/resume habit transfers, but `--continue` means latest, not implicit cwd filter. [source:cli-reference] 1.0.89 help, no resumed runtime test.
