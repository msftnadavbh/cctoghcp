# Claude Code → GitHub Copilot

**Make your first change with Copilot without rebuilding your Claude setup.**

Already comfortable in Claude Code? Keep the `CLAUDE.md` and `.claude/skills` that work in your existing repository. Learn the few Copilot CLI controls that change how you investigate, approve, and resume a task. This book works with a local checkout regardless of whether its source is hosted on GitLab or GitHub; a GitHub repository is not needed to practice. Copilot model calls still require an entitled account and network access.

## Start on your machine

Use **Windows PowerShell 7+** or **macOS Terminal (zsh)**. Install Copilot with [GitHub's installation instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli):

| Windows PowerShell 7+ | macOS Terminal |
| --- | --- |
| `winget install GitHub.Copilot` | `brew install --cask copilot-cli` |
| `copilot --version` | `copilot --version` |
| `copilot login` | `copilot login` |

Install [PowerShell 7](https://learn.microsoft.com/powershell/scripting/install/installing-powershell) if needed. Login opens an account authorization flow; do it only on a device and account you intend to use. Check organization policy and any personal/workspace instructions before a model call. Python **3.12+** is needed for the offline practice app ([python.org](https://www.python.org/downloads/)); verify `python --version` on Windows or `python3 --version` on macOS. If Windows `python` is missing, opens a Store alias, or reports an older version, check `py -3.12 --version` and substitute `py -3.12` for **every** Windows `python` command in the lessons. Otherwise install/select Python 3.12+ before continuing. On macOS, select an installed Python 3.12+ if `python3` is older. No Node/npm installation is required for the install choices above.

The fastest useful exercise is [**First 15 minutes: find and fix a boolean validation bug**](docs/start/first-15-minutes.md). It creates a private lab outside this book, copies a `CLAUDE.md` with its import and three skills, asks Copilot to trace the defect with read tools, then has you approve a single repair. Expect a failing check before the fix and a passing check afterward; the lab never overwrites or automatically deletes a destination. You can also run the lab offline without Copilot.

Keep **both the book checkout and the lab in ordinary local directories**, not OneDrive, other cloud-managed folders, symlink paths or Windows junctions. All Windows reparse points are refused; OneDrive is not supported. Check the actual checkout location—Documents may be redirected to OneDrive even when your home directory is local.

Want to start in **your existing checkout** instead? Keep its own `CLAUDE.md`; from that checkout, after inspecting its instructions and permissions, run `copilot`, then `/env` and `/instructions`. Try: “Trace the callers of the validation function in this repository; cite file and line, propose the smallest regression check, and do not edit yet.” Inspect the answer against source before allowing edits. The lab below is safer when you want a known expected result.

## Translate your workflow

| Familiar Claude habit | Copilot CLI action | Check before moving on |
| --- | --- | --- |
| Keep repository guidance | Retain `CLAUDE.md`; inspect `/instructions` | Correct file and imports attached, no contradictory duplicate policy |
| Explore before editing | Start with `--available-tools='view,grep,glob'` | Citations match actual code; no shell or edit tools visible |
| Plan a multi-seam change | `/plan`, inspect/edit the plan with Ctrl+Y | Inputs, owned files, checks and stop conditions are explicit |
| Approve a write | Resume with the `edit` tool available; check `/permissions` mode | Keep manual approvals; approve only the requested file and action |
| Reuse a skill or reviewer | Inspect `/skills` or `/agent` in the active workspace | Definition and instruction inheritance match the task |
| Continue yesterday's work | `copilot --resume` opens a session picker | Confirm session, cwd, files, grants and pending tasks first |

Follow [first hour](docs/start/first-hour.md) for a stock-filter feature in the **same** lab; [first real feature](docs/start/first-real-feature.md) takes a reviewed change into your real checkout. For individual controls use [planning](docs/workflows/planning.md), [permissions](docs/workflows/permissions.md), [Autopilot](docs/workflows/autopilot.md), [sessions](docs/workflows/sessions-and-context.md), [skills](docs/customization/skills.md) or [troubleshooting](docs/reference/troubleshooting.md). [Scenarios A–T](docs/scenarios/index.md) offer optional exercises; advanced automation is separate from the native interactive path.

The native lab uses Python 3.12+ and the standard library. For maintainers, `python3 -B -m scripts.validate` runs the Linux full suite (optional dependencies in [requirements-validation.txt](requirements-validation.txt)); native CI runs `python -B -m unittest discover -s tests -p test_practice.py -v` with platform Python. See [platform verification](docs/maintainers/native-platform-verification.md) for observed results and pending native CI; Copilot itself was not authenticated or exercised by these tests. Nothing here requires a push, commit, hook, plugin, MCP server or remote integration.
