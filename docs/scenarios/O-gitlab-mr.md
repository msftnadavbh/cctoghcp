# O — GitLab MR after three human approvals

## Goal and prerequisites

Prepare an **existing authorized GitLab checkout** for a reviewable MR, without publishing from the fixture (it has no `.git`). Installed/authenticated `glab` needed only after local checks and human approval; absent at baseline.

## Start and deterministic check

```sh
python3 -B -m scripts.gitlab --hostname gitlab.example.com --project group/project --pipeline 12345 --job 67890
python3 -B -m scripts.validate
```

The GET plan and IDs are illustrative only. **Optional authorized prompt:** “Summarize reviewed local changes and proposed GitLab MR title; do not push or create an MR.” In the *real* clone, a human checks `glab repo view group/project --output json`, branch/target, `git status --short`, diff and project tests; do not print credential URLs.

## Checkpoints, effects and exit

**Checkpoint:** move only approved source/test diff to real clone and rerun its checks. Human separately approves (1) commit, (2) Git push to chosen branch, (3) `glab mr create --repo group/project --source-branch feature/catalog --target-branch main --title 'Catalog fix' --description 'Reviewed changes' --draft`; never use `--fill` or `--push` implicitly. **Verification:** local validation exit, real checkout checks and *actual* MR URL only if creation succeeds. **Permissions:** offline helper prints plan; push/MR are distinct remote writes. **External effects:** only separately approved human actions. **Escape:** wrong host/project/target → stop, no `/delegate` GitHub fallback. **Claude analogy/difference:** local Copilot review doesn't change GitLab source host. [source:gitlab-mr-create] glab absent, no authenticated publish.
