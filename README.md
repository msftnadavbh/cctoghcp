# Claude Code → GitHub Copilot

**Keep the Claude Code assets that already work. Learn the Copilot-specific controls. Complete useful work without changing your Git host.**

This repository is for developers who already use Claude Code confidently and want to become productive with **GitHub Copilot CLI**. It translates familiar workflows—investigation, planning, implementation, delegation and review—without reteaching agentic coding or assuming that similarly named features behave identically.

The starting point is an existing **GitLab clone**, or a disposable local lab with no remote. You do not need a GitHub-hosted repository, GitHub Issues, Actions, a pull request or a plugin framework to begin.

## GitLab today, GitHub only when needed

| Work | Runtime and integration | Source-host requirement |
| --- | --- | --- |
| Analyze code, edit files and run checks | Local Copilot CLI tools and shell | No move from GitLab required |
| Read GitLab MRs or investigate pipelines | Separately authenticated `glab`, APIs or optional MCP | GitLab access |
| Delegate to Copilot cloud agent | GitHub-hosted agent workflow | GitHub-hosted target repository |

Local execution does **not** mean local model inference or that no data leaves your machine. The default workflow uses your Copilot entitlement and permitted models; GitHub authentication, organization policy and session-data settings remain separate from GitLab credentials and source hosting. See [capability boundaries](docs/hosting/capability-boundaries.md).

## Retain first; adapt selectively

Start by keeping your useful `CLAUDE.md` and compatible `.claude/skills` in place. Inventory existing configuration before adding or activating anything. Copilot-specific instructions or agents should address a real difference—not duplicate the same repository guidance.

Reuse is selective: discovery does not establish identical scope, instruction inheritance, permission semantics or hook behavior. Review shared settings and MCP definitions individually; do not copy user state or assume session portability. The [compatibility guide](docs/migration/compatibility.md) and [46-row migration matrix](evidence/migration-matrix.json) make those distinctions explicit.

## Quickstart: establish a local baseline

From this repository's root, with Python 3 available (verified on Python 3.12.3/Linux), run:

```sh
python3 -B labs/sample-app/scripts/check_lab.py
python3 -B labs/sample-app/src/catalog.py --query mug --limit 1
python3 -B -m scripts.inventory .
```

Expect three passing app tests, then a JSON page containing one mug with a matching total of two. The inventory reports known configuration paths and field names without printing credential values or executing discovered scripts. **Found does not mean supported.** These commands need no account, remote, network access or dependency installation.

Then follow the progressive path:

1. **[First 15 minutes](docs/start/first-15-minutes.md):** inspect retained instructions, investigate a deliberately introduced validation bug, approve a bounded repair, review the diff, check behavior and resume the session.
2. **[First hour](docs/start/first-hour.md):** continue on the same copy; plan an optional stock filter, reuse a skill, request a repository-aware review and consider narrowly scoped Autopilot.
3. **[First real feature](docs/start/first-real-feature.md):** take reviewed changes into a GitLab checkout, validate there, then explicitly approve publication.

The Copilot walkthrough assumes an entitled, authenticated developer. Offline alternatives exercise the lab, not the product. Installation and account provisioning are separate from the unmeasured 15-minute usability target.

## Choose your next task

| Need | Guide |
| --- | --- |
| Translate a Claude habit | [Muscle memory](docs/reference/muscle-memory.md) · [CLI cheat sheet](docs/reference/cli-cheat-sheet.md) |
| Control scope and continuation | [Planning](docs/workflows/planning.md) · [Autopilot](docs/workflows/autopilot.md) · [Permissions](docs/workflows/permissions.md) |
| Coordinate workers or evaluate models | [Fleet and subagents](docs/workflows/fleet-and-subagents.md) · [Models and HydraFusion research preview](docs/workflows/models-and-hydrafusion.md) |
| Reuse configuration | [Inventory](docs/migration/configuration-inventory.md) · [Instructions](docs/customization/instructions.md) · [Skills](docs/customization/skills.md) |
| Manage longer tasks or automation | [Sessions and context](docs/workflows/sessions-and-context.md) · [Headless and CI](docs/workflows/headless-and-ci.md) |
| Work with your source host | [GitLab now](docs/hosting/gitlab-now.md) · [GitHub later](docs/hosting/github-later.md) |
| Practice or diagnose a problem | [20 scenarios](docs/scenarios/index.md) · [Troubleshooting](docs/reference/troubleshooting.md) |

## Validate the repository

The lab is standard-library-only. Full repository validation additionally needs the packages in [requirements-validation.txt](requirements-validation.txt), installed in your own validation environment. That optional bootstrap contacts a package registry; the check itself is offline:

```sh
python3 -B -m scripts.validate
```

It covers tests, baseline acceptance, internal Markdown links and anchors, configuration parsing, plugin packaging and generated-reference consistency. [GitLab CI](.gitlab-ci.yml) and [GitHub Actions](.github/workflows/validate.yml) use this command without paid models or Copilot credentials. Hook/MCP examples remain inert; GitLab helpers are dry-run by default. Review [SECURITY.md](SECURITY.md) before activation and [CONTRIBUTING.md](CONTRIBUTING.md) before changing claims or assets.

## Verification and limits

The implementation baseline is **September 30, 2026**: **50 repository tests, 3 app tests and external baseline acceptance passed**. Copilot CLI **1.0.89** received isolated help/version checks only; this is not proof of authenticated behavior.

No authenticated Copilot or GitLab integration, HydraFusion comparison, hook dispatch, MCP client connection, plugin lifecycle or hosted CI run was exercised. Real CLI stdin/JSONL behavior and version-dependent configuration semantics remain qualified. Fake-process tests are not product tests, and permission controls are not an OS sandbox.

Consult [versions](docs/reference/versions.md), [sources](SOURCES.md), the [claim ledger](evidence/claims.json) and [review findings](results/review-passes.md) for evidence and remaining boundaries. No default validation step publishes, pushes, merges or deploys.
