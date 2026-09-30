# GitLab integration: credentials, CI and merge requests

For a project hosted on GitLab, Copilot CLI authentication grants access to an assistant, **not** to your GitLab project; `glab` has its own host and token. The first lab has no Git remote or `.git`. Start remote operations **only** in an existing, authorized GitLab clone after [reviewing the feature](../start/first-real-feature.md) and its checks. Never print a credential-bearing Git remote URL in a transcript.

## Read before write

Confirm expected GitLab host and project **outside** untrusted output. In the approved clone, `git status --short`, `git branch --show-current` and `glab repo view group/project --output json` let you inspect branch and host/project identity. For a known real MR or job, `glab mr view 123 --output json`, `glab ci get --pipeline-id 12345 --output json` or `glab ci trace 67890` need their IDs replaced with verified ones; raw traces may contain secrets or instructions, so do **not** paste them into a prompt. GitLab's `ci view` can be interactive/mutating, and `mr create --fill` implies push; neither is a harmless read.

The fixed [bridge](../../scripts/gitlab.py) defaults to **dry-run**:

```sh
python3 -B -m scripts.gitlab --hostname gitlab.example.com --project group/project --pipeline 12345 --job 67890
```

`gitlab.example.com` and numbers are *illustrations*, not fetched data. Every GET it plans passes `--hostname`, `--method GET`, runs in a neutral temporary cwd (not checkout-derived host), checks that job belongs to pipeline and stores only a **lossy sanitized** trace. For a separately authorized read, append `--execute-read --home REVIEWED_HOME --output NEW_FILE` with private credential HOME **outside calling workspace**, output separately reserved and a trusted executable. The helper does not fetch variables, retry CI, push, create MR or expose token values. If access fails, report no read and stop, don't switch project or host automatically.

## Human-approved publishing sequence in the real clone

1. Review the source and test changes in your checkout, including new files. Run your project's checks, then inspect `git diff`, `git diff --check` and `git status --short`. Keep assistant logs and credentials out of the commit.
2. Human approves **commit** of only intended files/branch; then separately approves `git push` to the *reviewed* GitLab remote and source branch. This documentation **does not** perform either action. Verify GitLab branch now exists; branch protection/CI rules take precedence.
3. Human separately approves draft MR on correct target: `glab mr create --repo group/project --source-branch feature/catalog --target-branch main --title 'Catalog fix' --description 'Reviewed changes and checks' --draft`. The [create reference](https://docs.gitlab.com/cli/mr/create/) confirms explicit flags; omit `--fill` (it pushes) and `--push`. The helper's printed draft argv is human-only and does not supply branches. Give an MR URL only if actual creation returns it; inspect MR target/diff and request human review. A failed push or MR creation is not completion.

GitLab MCP is [beta preview](https://docs.gitlab.com/user/model_context_protocol/mcp_server/) with instance/group enablement and OAuth. Confirm Copilot CLI client compatibility before trying the experimental server; the default path above needs neither. GitLab CI's pinned dependency bootstrap contacts a registry, then runs offline tests **without models**. Untrusted MRs must not receive protected secrets. [Hosting boundaries](capability-boundaries.md).
