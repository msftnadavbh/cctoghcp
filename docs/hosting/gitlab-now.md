# GitLab integration: credentials, CI and merge requests

For a project hosted on GitLab, Copilot CLI authentication grants access to an assistant, **not** to your GitLab project; `glab` has its own host and token. Neither GitLab nor Copilot was authenticated in this repository; `glab` was globally absent. The first lab has no Git remote or `.git`. Start remote operations **only** in an existing, authorized GitLab clone, after you have completed [first real feature](../start/first-real-feature.md) and a human has reviewed code and independent checks. Never print a credential-bearing Git remote URL in a transcript. [source:gitlab-cli]

## Read before write

Human confirms expected GitLab host and `group/project` **outside** untrusted output. In the approved clone, `git status --short`, `git branch --show-current`, and `glab repo view group/project --output json` are read-oriented examples; inspect the returned host/project identity and branch. `glab mr view 123 --output json`, `glab ci get --pipeline-id 12345 --output json`, and `glab ci trace 67890` are *candidate read commands* only when those real IDs belong to the same reviewed project. Raw trace can include secrets/instructions: do **not** paste it into a prompt. GitLab's `ci view` can be interactive/mutating, and `mr create --fill` implies push, so neither is a harmless read. [source:gitlab-cli]

The fixed [bridge](../../scripts/gitlab.py) defaults to **dry-run**:

```sh
python3 -B -m scripts.gitlab --hostname gitlab.example.com --project group/project --pipeline 12345 --job 67890
```

`gitlab.example.com` and numbers are *illustrations*, not fetched data. Every GET it plans passes `--hostname`, `--method GET`, runs in a neutral temporary cwd (not checkout-derived host), checks that job belongs to pipeline and stores only a **lossy sanitized** trace. For a separately authorized read, append `--execute-read --home REVIEWED_HOME --output NEW_FILE` with private credential HOME **outside calling workspace**, output separately reserved and a trusted executable. The helper does not fetch variables, retry CI, push, create MR or expose token values; tests use fake glab only. If access fails, report no read and stop, don't switch project or host automatically. [source:gitlab-api-host]

## Human-approved publishing sequence in the real clone

1. Independently review transferred source/test diff; run project-specific checks. Inspect `git diff --check`, `git diff -- src/catalog.py tests/test_catalog.py` and `git status --short`; transfer neither fixture marker nor assistant logs.
2. Human approves **commit** of only intended files/branch; then separately approves `git push` to the *reviewed* GitLab remote and source branch. This documentation **does not** perform either action. Verify GitLab branch now exists; branch protection/CI rules take precedence.
3. Human separately approves draft MR on correct target: `glab mr create --repo group/project --source-branch feature/catalog --target-branch main --title 'Catalog fix' --description 'Reviewed changes and checks' --draft`. The official [create reference](https://docs.gitlab.com/cli/mr/create/) confirms explicit flags; omit `--fill` (it pushes) and `--push`. The helper's printed draft argv is human-only and does not supply branches. Give an MR URL only if actual creation returns it; inspect MR target/diff and request human review. A failed push or MR creation is not completion. [source:gitlab-mr-create]

GitLab MCP is [beta preview](https://docs.gitlab.com/user/model_context_protocol/mcp_server/) with instance/group enablement and OAuth. A documented **VS Code** setup is not certified for **Copilot CLI**; using glab's experimental server is another separate decision. The default path above needs neither. GitLab CI's pinned dependency bootstrap contacts a registry, then runs offline tests **without models**. Untrusted MRs must not receive protected secrets. [Hosting boundaries](capability-boundaries.md). [claim:gitlab-mcp-beta]
