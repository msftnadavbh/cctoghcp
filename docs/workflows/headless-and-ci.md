# Headless/CI: structurally valid is not task complete

**Advanced POSIX workflow only.** The commands below describe the existing automation helper, not native Windows PowerShell or macOS first-lesson setup. Use [first 15 minutes](../start/first-15-minutes.md) for a cross-platform interactive lab and `practice.py` checks. A dry run is not an authenticated Copilot task.

Claude Code's text/json/stream-json is **not** Copilot `--output-format json` JSONL. Installed help documents `-p 'prompt'` for a noninteractive task, but this repo's [headless wrapper](../../scripts/headless.py) sends reviewed file bytes on stdin **without `-p`**. Whether the real CLI accepts those bytes and what event types it emits has **not** been tested. Never assume Claude `-p` + stdin translates directly, or that a fake event with `type=result` models Copilot success. Unknown typed JSONL events remain private; even exit 0 and structurally complete JSON lines do not establish task completion. SDK-backed integration is optional if a human-validated CLI wrapper proves insufficient for lifecycle/events. [source:programmatic-reference]

## Four reviewed prompt modes

| Dry-run mode | Exact command from repository root | Intended report / boundary |
| --- | --- | --- |
| `repo-summary` | `python3 -B -m scripts.headless repo-summary --repo labs/sample-app --prompt-file examples/headless/repo-summary.txt` | Human verifies cited source paths, not an oracle |
| `diff-review` | `python3 -B -m scripts.headless diff-review --repo labs/sample-app --prompt-file examples/headless/diff-review.txt` | Human compares actual diff, no automatic approval |
| `test-fix` | `python3 -B -m scripts.headless test-fix --repo labs/sample-app --prompt-file examples/headless/test-fix.txt` | Static syntax/secret check **only**; never run generated code here |
| `gitlab-log-summary` | `python3 -B -m scripts.headless gitlab-log-summary --repo labs/sample-app --prompt-file examples/headless/gitlab-log-summary.json` | Requires fixed-shape sanitized JSON; never feed a raw trace |

All four commands are **dry runs**; exit 0 means no model invocation. Execution requires **all** `--execute --consent-paid --reviewed-workspace --credential-env COPILOT_GITHUB_TOKEN --home FRESH_EMPTY_HOME --output NEW_PRIVATE_DIRECTORY`, plus a reviewed bare disposable workspace. The selected variable must contain a nonblank supported token without NUL/newlines; only that secret is forwarded, never `GH_TOKEN`, `GITHUB_TOKEN` or BYOK variables. Provision it privately using your approved secret mechanism, not command arguments or documentation. Official authentication docs describe a personal-account fine-grained PAT with **Copilot Requests** account permission; account entitlement and policy must allow use. Interactive OAuth remains the default interactive path, unchanged. This token path is source-reviewed and fake-executable-tested, not authentication/integration-tested. [source:copilot-authentication]

HOME must be empty, owned and exactly 0700, outside lab/output. Use a fresh HOME on every invocation; CLI-created settings make reuse fail preflight. Known workspace/ancestor configuration, machine policy and `.vscode/mcp.json` cause conservative refusal, not a claim that all these sources load in Copilot. A configured `--with-config` tutorial copy is intentionally not suitable for this headless profile. Absolute executable resolution, atomic private output reservation, `--disallow-temp-dir`, disabled builtin MCP and remote export are guards **not a sandbox**. `--secret-env-vars=COPILOT_GITHUB_TOKEN` requests CLI redaction, but private captures may still contain secrets printed by a child. Public wrapper reports never include child output or token values. [Artifact API](../../ARTIFACT-API.md).

| Exit | Interpretation; next human action |
| --- | --- |
| 0 | Dry-run only: inspect plan, no task outcome |
| 2 | Refused request/preflight; do not weaken defaults reflexively |
| 10–14 | Missing executable, launch error, timeout, output limit or nonzero child; preserve private evidence and stop |
| 15 | Invalid/incomplete JSONL framing: review actual schema in private, don't invent a terminal result |
| 16 | `test-fix` static check failed; no execution/acceptance |
| 17 | `validation-pending`: syntax/secret checks passed; review diff, then separately run independent acceptance on human-reviewed code |
| 18 | `report-unverified`: human must compare text with sources and objective |

Never publish private stdout/stderr automatically; a generated explanation may contain sensitive material. The separately trusted oracle `python3 -I -B labs/expected-results/acceptance.py LAB validation` uses isolated parent and fresh-home child probes but is not a same-user hostile-code sandbox. Review new code **before** using it. The wrapper does not run the oracle and never claims `test-fix` success. [Review](review-and-validation.md).

GitLab CI runs [offline validation](../../.gitlab-ci.yml) without assistant/auth. Pinned optional [PyYAML/jsonschema](../../requirements-validation.txt) bootstrap uses a package registry; the standalone app is stdlib-only. Untrusted MR code and CI traces must not receive protected tokens or an autonomous privileged runner; identify exact pipeline/job, retain raw output privately and pass only the [lossy sanitized allowlist](../../scripts/safety.py) into a reviewed prompt. [GitLab bridge](../hosting/gitlab-now.md) uses GET only and has fake-glab tests, not an authenticated integration. [source:gitlab-api-host]
