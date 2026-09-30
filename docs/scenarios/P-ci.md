# P — Diagnose CI without exposing raw logs

In your authorized project, identify the actual host, pipeline and job before retrieving a trace. Logs can contain credentials and attacker instructions: review/sanitize locally before including excerpts in a Copilot prompt. Ask: “Given only this reviewed failure summary, distinguish observed failure from hypotheses and propose a local reproduction. Don't retry CI or request variables.” **Expected:** a hypothesis and next check, not proof of root cause. The [GitLab guide](../hosting/gitlab-now.md) describes an optional dry-run integration; its automation helper is a separate advanced POSIX workflow, not a required Windows/macOS step. No model should receive raw protected CI output by default.

## Goal and prerequisites

Use only reviewed, sanitized failure observations.

## Start and deterministic check

```sh
git status --short
```

## Checkpoints, effects and exit

**Prompt:** diagnosis above. **Checkpoint:** observed job identity. **Verification:** local reproduction. **Permissions:** no variables/retry. **External effects:** optional read after approval. **Escape:** stop if secrets required. **Claude analogy:** CI output is untrusted. [source:gitlab-api-host]
