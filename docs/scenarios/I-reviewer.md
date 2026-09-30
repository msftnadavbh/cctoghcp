# I — Ask a reviewer for findings, not certification

The `--with-config` [first-lesson lab](../start/first-15-minutes.md) includes `.github/agents/repository-reviewer.agent.md`. Inspect its definition and `/agent` before invoking it; confirm its read tools and whether repository instructions attach when used as a subagent. Ask: “Review the `integer()` guard and its callers for boolean inputs, negative-test gaps and unintended changes; cite file:line and severity; no edits or shell.” **Expected:** actionable findings or explicitly none, not a passing test report. It cannot run checks with `view,grep,glob`. A human reviews `practice.py diff` and runs the check; a reviewer's approval never overrides a failing validation check. [Agent guide](../customization/agents.md).

## Goal and prerequisites

Use the configured validation lab.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** review callers above. **Checkpoint:** cited findings. **Verification:** human-run check remains authoritative. **Permissions:** read tools. **External effects:** optional credits. **Escape:** stop on write requests. **Claude analogy:** reviewer is not test runner. [source:cli-reference]
