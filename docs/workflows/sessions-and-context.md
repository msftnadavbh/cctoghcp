# Resume the right conversation, not just the latest one

Before leaving a task in your existing repository, note its path, branch/revision, changed files, checks actually run and approvals. Later use `copilot --resume` to choose the intended session; `--continue` chooses the most recent one, possibly from a different workspace. If you have a reviewed ID, `copilot --resume=ID` selects it. Recheck `/cwd`, `/env`, `/instructions`, `/permissions`, `/tasks`, `git status --short` and current files before another edit. Session state is not a Git rollback.

| Action | What changes | What does not |
| --- | --- | --- |
| `/new` or `/clear` | Conversation | Files, branch, external effects |
| `/compact` | A lossy summary of context | Missing decisions; write them down first |
| `/fork` | Conversation branch | Existing workspace edits or credentials |
| `/rewind` | Supported recent turns/file changes | Pushes, network calls or every subprocess |
| Git worktree | Working files/history in a real Git repository | Network, identity or home-directory access |

For a handoff, record: outcome/acceptance; workspace, revision and session ID; baseline and observed check exits; changed paths and owner; grants/external effects; open question and next safe action. Do not report a test as passed until you have its exit. Session logs and exports can contain private prompts; `--no-remote-export` disables session export/control, **not** model traffic. [Review](review-and-validation.md) covers independent verification.
