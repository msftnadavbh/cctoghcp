# Sessions and context: conversation is not filesystem

`copilot --continue` resumes the **most recent** session, not necessarily one scoped to current cwd. `copilot --resume` opens the picker; `copilot --resume=ID` selects a particular session; `/resume` switches in the UI. Record session ID/name and re-inspect `/cwd` and `/env` before approving tools. `/new` starts a new conversation, `/context` shows context-window usage, `/compact` summarizes (lossily), `/rewind` can undo recent turn/file changes but not external effects, and `/fork` copies conversation state. [source:cli-reference]

| Boundary | What it changes | What it does **not** change |
| --- | --- | --- |
| `/new` or `/clear` | Conversation context | Files, Git branch, remote publication; credit-limit setting may remain |
| `/compact` | Context-token pressure via summary | Exact forgotten decisions; write them down before compacting |
| `/fork` | Conversation branch | Working-directory edits or credentials |
| Git branch | Version-control history | OS access and running background tasks |
| `/new worktree` or `/fork worktree` | Separate Git working directory (different conversation behavior) | Network/credential isolation or approved branch protection |
| `/rewind` | Last turn and supported file edits | Shell side effects, push, MR, web requests or all child processes |

Use `/worktree` only in a real Git repo after checking base ref and uncommitted changes; the [disposable fixture](../start/first-15-minutes.md) has no `.git`. Git worktrees isolate files, **not** identities, HOME or network; a VM/container needs an actual credential/mount/egress threat review. `~/.copilot/session-state`, logs and exported reports can contain private prompts and tool output. `--no-remote` disables remote control only, while `--no-remote-export` disables both export and control. Remote control can technically operate from a non-GitHub source directory because it is a service, not proof that the source remote moved. [source:cli-reference]

## Handoff card before compact, exit or another operator

1. Objective and exact acceptance (e.g. `in_stock=None|bool`, filter before slicing).
2. Workspace path, owning lab ID and current CLI session ID/name; check selected cwd.
3. Baseline revision or copy origin plus observed initial/final oracle status.
4. Changed paths and sole edit owner; identify any unreviewed file.
5. Executed commands **with actual exits**, separating reviewed code runs from static checks.
6. Granted tools, paths, URLs and instructions attached; never paste secret values.
7. External effects: files, subprocesses, network, push/MR, credit spend; write “none” only when verified.
8. Unresolved hypothesis, failed check or human decision pending.
9. Next action and stop/rollback boundary (which specific check/reviewer comes first).

Before `/exit`, inspect `/tasks`: `a` toggles nested tasks, `f` includes finished tasks, `X` stops an active task, `B` backgrounds a synchronous task. Child cleanup and external process effects are not a generic “session saved” guarantee. The current official CLI reference documents `COPILOT_TASK_WAIT_TIMEOUT_SECONDS` as the **maximum seconds** `-p` or `-p --autopilot` waits for pending background agents or shell commands before exit; default `600`, `0` exits without waiting. Captured 1.0.89 `help environment` omits it: this is a **source-reviewed, not runtime-verified** setting, not an unsupported setting or an OS process-kill deadline. Inspect actual tasks and use an independently reviewed external deadline. [Scenario S](../scenarios/S-resume.md). [claim:background-wait]
