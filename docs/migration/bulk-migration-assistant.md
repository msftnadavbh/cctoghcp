# Bulk migration assistant: scan first, apply in batches

You do not need to migrate each item manually. Use Copilot as a migration assistant: let it scan the repository, classify assets, generate a migration plan and prepare proposed artifacts. Humans review and approve before anything is committed or enabled.

The safe sequence is:

```text
Scan all → generate migration plan → review → prepare low-risk artifacts → apply in batches
```

Do not ask Copilot to apply everything automatically. Bulk scan is useful; bulk apply is risky.

## Where to run it

Run from the repository root in Copilot CLI:

```sh
cd /path/to/your/repository
copilot
```

Or start a Copilot Desktop app session on the repository project. If important workflow guidance lives outside the repo, paste the reviewed excerpt from Confluence, a runbook, a shared prompt or a session handoff into the prompt. Do not paste secrets, raw private transcripts or credential-bearing logs.

## Run 1: scan only

```text
Act as a GitHub Copilot migration assistant.

Scan this repository for existing agent workflow assets:
- CLAUDE.md / AGENTS.md
- .claude/rules
- .claude/skills
- .claude/commands
- hooks
- MCP configs
- LiteLLM/model routing configs
- scripts and runbooks used by agent workflows

Do not modify files yet.

Return:
1. Inventory of all assets found
2. Recommended GitHub Copilot target for each asset
3. Which items can be migrated automatically
4. Which items require human review
5. Which items should stay external
6. Proposed migration batches: low-risk first, medium-risk second, high-risk/manual last
7. Draft GitHub Copilot artifacts for low-risk items only
8. Open questions for the owner
```

Review the result with the workflow owners before moving on. Discovery does not prove attachment or correct invocation.

## Run 2: prepare proposal only

After humans approve the low-risk batch, ask Copilot to draft proposed artifacts without changing files:

```text
Using the migration plan above, prepare proposed GitHub Copilot artifacts for the approved low-risk items only.

Do not modify files yet.

Return:
1. Proposed repo instructions
2. Proposed skill definitions
3. Proposed slash commands or prompt templates
4. Proposed PR checklists
5. Items that require manual review before migration
6. Items that should stay external

Keep everything concise and reviewable.
```

## Run 3: create a proposal branch only after approval

Only after a human approves the proposed artifacts should you allow file creation:

```text
Create a migration proposal branch for the approved low-risk items only.

Constraints:
- Do not delete or modify existing workflow files.
- Do not touch production code.
- Create proposed GitHub Copilot artifacts only.
- Add a MIGRATION_SUMMARY.md explaining what was created, what stayed external and what still requires review.

Return:
1. Files created
2. Files changed
3. Rationale
4. Review checklist
5. Open questions
```

The agent drafts. Humans approve.

