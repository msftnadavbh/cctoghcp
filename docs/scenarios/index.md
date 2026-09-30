# Optional practice and examples

For the main path, [work in your existing repository](../start/use-copilot-in-your-repository.md); no sample app, Python or lab setup is required. These optional exercises use a **separate** known-result Python lab, not your project's acceptance checks. If you choose one, start with [first 15 minutes](../start/first-15-minutes.md) to set up a private lab outside this book and observe a reproducible validation failure. Continue on that same lab for [first hour](../start/first-hour.md). Each scenario below gives an additional question; use the shared lab unless a page explicitly needs a fresh one. The native `practice.py setup/diff/check` commands in those lessons are for practice only. Inspect the entire diff before executing edited lab code; the checker retains private artifacts and never deletes the lab. Paid Copilot actions require your login and approval; offline checks do not.

| Want to practice… | Start here |
| --- | --- |
| Understand before editing | [A explore](A-explore.md), [B plan](B-plan.md), [C plan then Autopilot](C-plan-review-autopilot.md) |
| Permission boundaries | [D narrow permissions](D-narrow-permission.md), [E broad grants in external isolation](E-disposable-broad.md) |
| Model selection | [F Hydra comparison](F-hydra-experiment.md), [G model pinning](G-pin-model.md) |
| Parallelism and review | [H fleet](H-fleet.md), [I reviewer](I-reviewer.md) |
| Customize | [J skills](J-skills.md), [K retained Claude instructions](K-existing-claude.md), [L MCP](L-mcp.md), [T hooks](T-hooks.md) |
| Build | [M debug](M-debug.md), [N refactor](N-refactor.md) |
| Hosting (optional) | [O GitLab MR](O-gitlab-mr.md), [P CI](P-ci.md), [Q GitHub delegation](Q-future-github.md) |
| Automation/continuation | [R headless](R-headless.md), [S resume](S-resume.md) |

Some advanced pages describe POSIX-only automation helpers: **do not run their POSIX setup/cleanup commands in PowerShell or treat them as native practice commands**. Use the interactive lab and native checks first; only run those helpers in a separately reviewed POSIX environment. External integrations, hooks and MCP are never necessary for the first task. [Platform verification](../maintainers/native-platform-verification.md) records the native lab results and remaining limits.
