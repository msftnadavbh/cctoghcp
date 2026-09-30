# Troubleshooting: 21 stops and recoveries

Use diagnostics **before** granting another permission or reinstalling. Start with [your existing checkout](../start/use-copilot-in-your-repository.md); the separate [optional practice](../start/first-15-minutes.md) uses `practice.py` and requires Python 3.12+. Do not delete personal Copilot state as a default remedy or paste credentials/session logs into a report. [source:cli-reference]

| Symptom | Diagnostic / interpretation | Recovery and verification |
| --- | --- | --- |
| 1 `copilot` not found | Check `copilot --version` in your shell | Follow the [platform install steps](../start/use-copilot-in-your-repository.md#open-your-checkout), then open a new shell and recheck; optional practice checks work offline without login |
| 2 Login or entitlement fails | `copilot login` OAuth/browser/device, org policy, token type separate from GitLab | Check own entitlement and [auth boundary](../hosting/capability-boundaries.md) outside transcript; never try random token strings or classic `ghp_` |
| 3 GitLab read fails | `glab` absent, wrong host/project, job not in pipeline | Run bridge **dry plan** with `--hostname gitlab.example.com --project group/project --pipeline 12345 --job 67890`; review IDs then request authorized GET, no auto-retry |
| 4 `gh agent-task` absent | Observed gh 2.45.0 below public-preview >=2.80 | Continue local work; don't claim cloud task submitted; check gh version/entitlement if using a GitHub-hosted target |
| 5 Instructions not attached | Confirm your checkout's `CLAUDE.md` exists and its imports are reviewed | Check `/env`, `/instructions`, cwd and restart/resume; compare matching vs nonmatching paths afterward |
| 6 Contradictory instructions | Two root/nested files may both load; no universal priority | Inspect both and remove contradiction from reviewed sources, then verify effective attachment; don't add third copy |
| 7 `@` import missing | Unsupported GEMINI/path-instructions import or absolute/`~` escape | Use repository-relative import within supported boundary; recheck after restart without disclosing home |
| 8 Custom subagent misses repo policy | `include-custom-instructions` default differs for subagent/main selection | Review definition and set explicit true **only if required**; verify effective `/env` and task outcome |
| 9 “Read-only” agent writes | Text request doesn't remove tools or shell | Stop; use actual `view,grep,glob` tool set and inspect grants, diff and OS access |
| 10 Hook timeout appears to allow edit | Official dispatcher timeout can fail open; handler timeout unit test isn't dispatcher test | Keep CI independent; inspect captured event privately; never rely on hook as only gate |
| 11 Hook rejects/ignores expected edit | `cwd` must equal lab; native `toolArgs` vs compatible `tool_input`; nested path validated | Compare [payload fixture](../../examples/hooks/payloads/native.json), absolute launcher and trusted lab path; do not globally disable policy to pass |
| 12 MCP tool unavailable | Inert local config not installed; protocol tests don't enable client | Run `python3 -B -m unittest discover -s tests -p 'test_protocol_gitlab.py'`, then inspect transport/permissions before optional activation |
| 13 MCP adds unexpected instructions | Server instructions are untrusted independent source | Stop session/server, inspect instruction provenance and server access; do not enable `--allow-all-mcp-server-instructions` as a fix |
| 14 Plugin path rejected | Official local install docs vs 1.0.89 `plugin install --help` mismatch | Generate inert ZIP and schema check only; validate new help/lifecycle in separately approved environment |
| 15 Headless narrow grant stalls | Help says `--allow-all-tools` required for noninteractive but source describes selective grants | Preserve exit/output, stop; never fall back to `--allow-all`; consider interactive manual review |
| 16 JSONL unrecognized/incomplete | Wrapper accepts bounded *typed objects*, no terminal schema; code 15 means malformed framing | Keep private output, compare actual events with documented version; do not reinterpret unknown event as success |
| 17 `validation-pending` exit 17 | Advanced headless static checks passed, newly written code not executed | Human reviews all changed files, then uses `practice.py check LAB --exercise validation` from the native lesson; report actual exit |
| 18 Credit budget exceeded | `/limits` preview soft cap accounted after call | Stop prompts, inspect `/usage` and external timeout; never claim a hard spend ceiling |
| 19 `/compact` or resume loses a decision | Summary is lossy; `--continue` latest may be wrong workspace | Use nine-field handoff, `--resume` picker/ID, check cwd and current file; no guessed context |
| 20 CI trace may contain secrets | Raw log and MR text untrusted; gate alone is heuristic | Keep original private, use GET bridge's lossy allowlist, never fetch variables or give untrusted CI protected creds |
| 21 Practice check or cleanup fails | A failed check may indicate real behavior; `practice.py` never auto-cleans | Review diff and checker output before rerun; remove only your exact lab/artifact directory manually after stopping processes |

For a new failure, record **command, source/version, exact exit, observed output class (not secret values), hypothesis and next safe check**. [Known discrepancies](known-discrepancies.md) cover unresolved source differences; [security](../../SECURITY.md) governs untrusted code execution.
