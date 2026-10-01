# Use the GitHub Copilot app as a visual workbench

The CLI is the closest fit for terminal-first Claude Code muscle memory, but some teams need a visual surface for sessions, branches, pull requests and review. Use the GitHub Copilot app when you want one place to coordinate agent work while still preserving human approval.

Use the app to make the workflow visible:

1. Sign in with the GitHub account that has Copilot entitlement.
2. Add the existing project from a GitHub repository, local folder, or repository URL.
3. Start a **Plan** or **Interactive** session first; avoid Autopilot until the task boundary and review expectations are clear.
4. Ask for a read-oriented trace before approving edits.
5. Review the changes, checks and PR evidence yourself.

The app can help a team see issue/branch/PR flow more easily than a terminal. It does not remove the need to inspect instructions, permissions, changed files and actual checks. If the checkout is from GitLab, the app can still work with local code, but GitLab MR/CI publishing remains a separate integration decision. See [GitLab integration](../hosting/gitlab-now.md).

## First safe app prompt

Use this in a Copilot app session opened on the repository:

```text
Analyze this repository.
Do not modify files.

Return:
1. What this repository appears to do
2. Main folders and components
3. How tests seem to be organized
4. Any existing agent instructions, skills, hooks or MCP configuration you notice
5. A recommended first low-risk task for a pilot
```

Success means the app can read the project and produce a grounded summary without changing files. It does not mean the workflow is ready to scale.

