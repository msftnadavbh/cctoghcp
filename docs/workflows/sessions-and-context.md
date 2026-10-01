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

## Chronicle: find and learn from previous work

Type these commands **inside Copilot CLI**, not directly in PowerShell or your macOS shell. Start with `/chronicle` to see the available options. Chronicle uses your Copilot session history; it does not import Claude conversations.

| Command | Use it to… | What to expect |
| --- | --- | --- |
| `/chronicle` | Browse history tools | A subcommand picker |
| `/chronicle standup` | Prepare a daily update | A report of recent work, normally the last 24 hours |
| `/chronicle standup for the last 3 days` | Change the reporting period | A summary covering the requested period |
| `/chronicle search authentication` | Find an earlier discussion | Matching session content; replace `authentication` with your topic |
| `/chronicle tips` | Improve how you use Copilot | Personalized suggestions based on recent sessions |
| `/chronicle tips for better prompting` | Focus the advice | Suggestions about your prompts |
| `/chronicle cost-tips` | Understand token spending | Usage patterns and ideas for reducing costs |
| `/chronicle improve` | Improve project instructions | Suggestions for this repository; choosing them creates or updates `.github/copilot-instructions.md` |
| `/chronicle skills create` | Turn repeated work into a skill | A repository skill proposal to review |
| `/chronicle skills review` | Inspect proposed skills | Review the proposed instructions and scripts before accepting |
| `/chronicle skills status` | Check proposal progress | Status of repository skill proposals |
| `/chronicle reindex` | Recover missing history entries | Rebuilds the local session store and syncs session data to your account |

**Retain your Claude assets:** review `improve` suggestions against the existing `CLAUDE.md`, and skill proposals against `.claude/skills`. Keep one copy of shared guidance rather than accepting duplicates.

History questions normally span repositories; `improve` is scoped to the current repository or working directory. History-based answers can send relevant session content to the model. Review summaries before sharing them, and check your session-data policy before reindexing. If a subcommand is missing, check the `/chronicle` picker and your CLI version.

### Nearby commands

| Command | When to use it |
| --- | --- |
| `/session` | Find the current session ID and details |
| `/rename Fix login validation` | Give this session a recognizable name |
| `/resume` | Reopen a conversation instead of searching its history |
| `/usage` | Inspect usage for the current session |
| `/rubber-duck` | Get a second opinion on the current problem, not a history report |
| `/skills` | Inspect available skills, not pending Chronicle proposals |

[Chronicle and session-history guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/chronicle) · [CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)
