# O — A GitLab review is a separate decision

After [first real feature](../start/first-real-feature.md), inspect the reviewed changes in your **real authorized GitLab checkout**, not the lab. Run that project's tests and inspect `git status --short` and `git diff --check` in your chosen terminal. Confirm host, project and target branch privately; remote URLs may include credentials. Ask Copilot with read tools: “Summarize this reviewed diff and propose a merge-request title; do not commit, push or create anything.” **Expected:** a proposed summary, not an MR URL. If you use `glab`, follow [GitLab integration](../hosting/gitlab-now.md) only after separately approving commit, push and MR creation; never use `--fill` assuming it is a read. GitHub `/delegate` is not a GitLab substitute.

## Goal and prerequisites

Use an authorized GitLab checkout, not the lab.

## Start and deterministic check

```sh
git status --short
```

## Checkpoints, effects and exit

**Prompt:** propose an MR title above. **Checkpoint:** host and branch verified. **Verification:** real project tests. **Permissions:** remote writes need approvals. **External effects:** commit/push/MR only with consent. **Escape:** stop on wrong host. **Claude analogy:** local work need not move hosts.
