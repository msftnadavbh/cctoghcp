# Scenario lab: A–T

Every scenario includes a reviewed local prep and deterministic check. **CLI prompts are proposed paid/operator exercises, not transcripts or authenticated proof.** `copilot`, `claude` and `glab` were globally absent at baseline; if your CLI is not authorized, execute only offline prep/check. Documentation was written without installing hooks/MCP/plugins, making model calls, pushing or committing. Human-directed optional scenarios can involve external effects **only after separate approval**. For a local copy: setup requires a nonexistent destination; keep its printed ownership ID and use `python3 -B -m scripts.lab cleanup OWNERSHIP_ID --state /tmp/checkpoint-state` only after stopping tasks. The oracle's current trusted command is `python3 -I -B labs/expected-results/acceptance.py LAB EXERCISE` after reviewing any modified code. Never use an ID from another run. [Versions](../reference/versions.md).

| Track | Scenario |
| --- | --- |
| Understand | [A explore](A-explore.md), [B plan](B-plan.md), [C plan → review → autopilot](C-plan-review-autopilot.md) |
| Control | [D narrow permission](D-narrow-permission.md), [E disposable broad permission](E-disposable-broad.md) |
| Model | [F Hydra experiment](F-hydra-experiment.md), [G pin model](G-pin-model.md) |
| Parallel/review | [H fleet](H-fleet.md), [I reviewer](I-reviewer.md) |
| Customize | [J skills](J-skills.md), [K existing CLAUDE](K-existing-claude.md), [L MCP](L-mcp.md), [T hooks](T-hooks.md) |
| Build/host | [M debug](M-debug.md), [N refactor](N-refactor.md), [O GitLab MR](O-gitlab-mr.md), [P CI](P-ci.md), [Q future GitHub](Q-future-github.md) |
| Automate/continue | [R headless](R-headless.md), [S resume](S-resume.md) |

Each page has goal/prerequisites, exact local start/check, a specific optional prompt, checkpoints, permission/external effects, an escape and Claude analogy with evidence tier. An **initial expected oracle failure is a verified reproduction, not a passing feature**. No optional paid/client action was executed for this guide. For a real CLI session verify installation, `/env`, selected cwd and policies first; never substitute an invented transcript for a recorded result. Interactive examples narrow visible CLI tools, suppress remote export and automatic temp access; `--disallow-temp-dir` does not revoke permission to a separately approved `/tmp` cwd and was not runtime validated here. The broad-permission isolation exercise deliberately does **not** claim that flag makes `--allow-all` safe.
