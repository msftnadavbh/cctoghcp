# First real feature: start in your own checkout

You do not need to finish a lab or transfer a sample-app patch. Follow [use Copilot in your repository](use-copilot-in-your-repository.md) with a real task and your existing `CLAUDE.md`, imports and skills. Read them before trusting project configuration, then inspect `/env` and `/instructions` in-session.

1. **Define your outcome.** Identify the actual behavior, affected callers and a check your project already uses; record current changes with `git status --short`. Ask for citations before edits. If semantics are ambiguous, [plan](../workflows/planning.md) and agree on files, negative cases and stop conditions.
2. **Approve a bounded change.** Make `edit` available separately, keep manual permissions and review requested paths. A plan, a skill or Autopilot does not authorize extra tools or external effects.
3. **Review then test.** Inspect `/diff`, `git status --short`, `git diff` and any new untracked files. Review generated tests before running your project's real test command. Record its observed exit; `git diff --check` checks whitespace only. A passing lab or model summary does not prove the feature works here.
4. **Hand off.** Record outcome, workspace/revision, changed files, checks and exits, grants, external effects and next human decision. No commit, push or review publication is implied; approve each separately. [Sessions](../workflows/sessions-and-context.md) explains what to check when resuming.

If you chose the [optional practice lab](first-15-minutes.md), its separate checks remain practice results, not prerequisites or integration evidence for your real checkout.
