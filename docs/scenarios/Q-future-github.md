# Q — When GitHub cloud delegation applies

The first-lesson lab has no remote; stay with local `/review` and the independent check. If your **real** target repository is hosted on GitHub, ask in a read-only session: “Compare local `/review` with `/delegate` for this reviewed feature; do not create a task, branch or PR.” **Expected:** a decision, no cloud side effects. `/delegate` requires separate entitlement, target and approval; it does not publish a GitLab merge request. For public-preview `gh agent-task`, check the installed command and [GitHub-hosted guide](../hosting/github-later.md) before use. Copilot CLI in a GitLab checkout does not move your repository to GitHub.

## Goal and prerequisites

GitHub-hosted target only for cloud delegation.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** compare delegation above. **Checkpoint:** identify target. **Verification:** no remote change in lab. **Permissions:** cloud approval separate. **External effects:** none by default. **Escape:** use local review if GitLab-hosted. **Claude analogy:** host is independent of CLI.
