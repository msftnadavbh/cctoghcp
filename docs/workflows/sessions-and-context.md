# Resume the right conversation, not just the latest one

After the [validation repair](../start/first-15-minutes.md), note your lab path, the observed failing-then-passing check, changed files and any approvals before exiting with `/exit`. Later run `copilot --resume` to choose the intended session; `--continue` chooses the most recent one and might be for a different workspace. If you have a reviewed ID, `copilot --resume=ID` selects it. Recheck `/cwd`, `/env`, `/instructions`, `/permissions`, `/tasks` and current files before approving another edit. Session state is not a Git rollback.

| Action | What changes | What does not |
| --- | --- | --- |
| `/new` or `/clear` | Conversation | Files, branch, external effects |
| `/compact` | A lossy summary of context | Missing decisions; write them down first |
| `/fork` | Conversation branch | Existing workspace edits or credentials |
| `/rewind` | Supported recent turns/file changes | Pushes, network calls or every subprocess |
| Git worktree | Working files/history in a real Git repository | Network, identity or home-directory access |

For a handoff, record: (1) outcome/acceptance, (2) workspace and session ID, (3) baseline and initial/final check exits, (4) changed paths and edit owner, (5) commands actually run, (6) tool/path/URL grants, (7) external effects, (8) open question, (9) next safe action. Example: “Stock filter: validation=0, in-stock=1; `src/catalog.py` only; no remote action; next: review CLI parser diff before check.” Don't report a test as passed until you have its exit.

The lab has no `.git`, so worktree commands are for a **real repository**, not the first lesson. Session logs and exports can contain private prompts; `--no-remote-export` disables session export/control, not model traffic. [First real feature](../start/first-real-feature.md) shows the integration handoff.
