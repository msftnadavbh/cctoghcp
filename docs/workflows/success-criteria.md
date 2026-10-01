# What good looks like

Use these criteria to decide whether a Copilot workflow is ready to reuse. A confident answer is not enough.

## Planning quality

- The plan cites actual files, functions, commands or configuration.
- It distinguishes observed facts from hypotheses.
- It names assumptions and open questions.
- It proposes the smallest safe change.

## Implementation quality

- The diff is small and reviewable.
- The change stays within approved scope.
- Public API or behavior changes are explicit.
- Generated tests are reviewed before execution.

## Evidence quality

- The assistant lists files inspected and files changed.
- Commands/checks are recorded with actual observed results.
- If a check cannot be run, the limitation is stated.
- Review focus is clear for the human reviewer.

## Governance quality

- No secrets appear in prompts, outputs or files.
- The run respects approved tools, paths and permissions.
- Branch, PR, CI and review boundaries are explicit.
- The handoff records branch, changed paths, checks, approvals and next decision.

## Useful pilot outcome

A pilot is useful if it answers:

1. Does the workflow produce better or comparable output to the current process?
2. Is the output easier to review?
3. Does it reduce repeated manual prompting or handoff work?
4. Are cost, model choice and permissions visible enough to govern?
5. Can the workflow be repeated safely on another similar task?

If the answer is unclear, keep the workflow in pilot and refine the instructions before scaling.

