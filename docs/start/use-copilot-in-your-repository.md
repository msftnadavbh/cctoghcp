# Use Copilot in your existing repository

Start with a checkout you already own and a small real task. You do **not** need to clone this guide, create a sample app, install Python or move your repository to GitHub. A Copilot entitlement and network access are required for model calls; review your organization's policy before signing in. Never paste secrets into a prompt.

## Open your checkout

Install the CLI using [GitHub's instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli). These are separate shell choices, not commands to run in this guide's checkout:

| Windows PowerShell 7+ | macOS Terminal (zsh) |
| --- | --- |
| `winget install GitHub.Copilot` | `brew install --cask copilot-cli` |
| `copilot --version` | `copilot --version` |
| `copilot login` | `copilot login` |

If needed, [install PowerShell 7](https://learn.microsoft.com/powershell/scripting/install/installing-powershell). Login opens an account authorization flow; use only an account and device you intend to authorize. In **your own terminal**, replace the example path with the location of your existing checkout (not a path into this guide):

```powershell
Set-Location 'C:\src\your-project'
git status --short
```

```zsh
cd "$HOME/src/your-project"
git status --short
```

Note any pre-existing changes; don't ask Copilot to overwrite them. Read your project's `CLAUDE.md` and any referenced repository files, relevant `.claude/rules`, skills, agent definitions, settings, hooks and MCP configuration **before trusting or activating them**. Do not execute a hook, plugin or MCP server to perform this audit. If something is unfamiliar, pause and inspect its source. [Configuration inventory](../migration/configuration-inventory.md) lists the surfaces; don't replace working instructions with a new `AGENTS.md` just to start.

## Trace one real task, then decide whether to edit

From that checkout, start a read-oriented session (PowerShell and zsh use the same command):

```text
copilot --no-remote-export --disable-builtin-mcps --disallow-temp-dir '--available-tools=view,grep,glob'
```

`--no-remote-export` disables session export/control, **not** model traffic. These flags limit the CLI tools offered to the model and disable built-in MCPs; they do not isolate the OS or automatically disable trusted project configuration. Check `/env`, `/instructions` and `/skills` for cwd and attached guidance; use `/permissions` to select manual approvals if necessary (it changes mode). Don't approve unexpected activation or extra tools.

Pick an actual function and task in your checkout. For example, replace **[function or behavior]** with the real name in this prompt; the brackets are a prompt placeholder, not a command:

> Trace the callers of [function or behavior] in this repository. Cite the actual files and lines, explain the observed behavior and propose the smallest regression check. Report only; do not edit, run commands or fetch external content.

Verify its citations in your source. If the change is nontrivial, use `/plan` and review the proposed files, behavior, tests and stop conditions first; a plan does not enforce read-only access. [Planning](../workflows/planning.md) and [permissions](../workflows/permissions.md) explain the controls.

## Make the approved change

Exit with `/exit`. From the same checkout, open the session picker with editing available (the command works in both shells):

```text
copilot --resume --no-remote-export --disable-builtin-mcps --disallow-temp-dir '--available-tools=view,grep,glob,edit'
```

Select the session for your task. Recheck `/env` and keep manual approvals in `/permissions`. Replace the bracketed text below with the behavior and file paths you just reviewed:

> Implement [approved behavior] in [implementation path], and add the agreed regression test in [existing test path]. Preserve [existing interface or behavior]. Change only those files. Do not run commands, install dependencies or publish. Show the diff and stop if the scope is insufficient.

Approve only the expected edits. This tool list can modify existing files; it does not include file creation or shell execution. If the task needs another capability, revise the scope and approve that separately rather than enabling every tool. Expect a source/test diff matching the request—not a claim that tests already passed.

## Verify and hand off

Inspect `/diff` and, in your checkout, `git status --short` and `git diff` (also inspect new untracked files separately). Review generated test code **before running it**. Identify the test or build command already used by *your* project from its existing scripts/CI/readme; don't invent a universal `npm test` or Python command. Run that approved command yourself and record its real exit and output. If the repository has no suitable check, say so; do not report the change as tested. Finish with `git diff --check`, which checks whitespace, not correctness. No commit or push is implied.

For later work, use `copilot --resume` to choose the session, then recheck cwd, files, instructions and grants; `--continue` can pick a different recent task. Record changed paths, actual checks, approvals and the next decision. [Sessions](../workflows/sessions-and-context.md) and [review](../workflows/review-and-validation.md) go deeper.
