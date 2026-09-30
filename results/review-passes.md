# Final implementation review — 2026-09-30

These are separate review passes over the actual implementation, not seven
authenticated product tests. The lead owns the conclusions. An independent
Claude-family reviewer inspected the OpenAI-written security implementation;
an additional repository audit covered onboarding, hosting and duplication.
Reviewers reported code-reading evidence, not execution they could not perform.
The lead subsequently ran the deterministic checks described below.

## Pass 1 — Technical accuracy

Compared isolated Copilot 1.0.89 help with current official sources, the supplied
research and shipped assets. Corrected the baseline's older `.claude/rules`
assumption using the stable release notes; changed the cloud setup filename to
`copilot-setup-steps.yml`; updated the deprecated experimental-mode entry point;
kept CLI tool identifiers distinct from editor/cloud aliases. The 46-row
migration matrix now uses all eight required compatibility classes, independent
hosting/availability fields, and per-row version/source evidence. The generated
references passed `--check`. Product runtime and collision semantics remain
unverified where the ledgers say so.

## Pass 2 — Claude Code expert usability

Read all three onboarding pages against real artifact interfaces. Replaced an
offline-only introduction with the intended authenticated CLI walkthrough, plus
an honestly labeled offline alternative. The configured disposable copy retains
the existing fixture `CLAUDE.md`, relative import, three canonical skills and
restricted reviewer. Investigation starts without an edit tool; an explicit
resume adds it only after scope approval. The first hour continues the same
catalog task rather than restarting an unrelated lesson. The 15-minute target
was not timed with a representative developer.

## Pass 3 — GitLab compatibility

The workspace has no Git repository or remote. Tests create local copies without
a remote; no GitHub source host is needed. Examined the first-feature and MR
paths: local checks precede separately human-approved push and draft MR creation.
The GitLab helper uses an explicit hostname, project, pipeline and job, and
fixed GET requests only. Lead-ran dry-run output contained no executed network
operation. GitHub Issues, cloud delegation and `gh agent-task` remain a separate
future lane. No live GitLab read or write was performed.

## Pass 4 — Security

Independent review found and prompted fixes for two high-severity design faults:
post-edit hooks executing freshly edited Python, and automatic headless
validation with a credential HOME and exit-code-only acceptance. Hooks now do
static AST/secret checks only. Headless reports pending human validation, never
automatic test-fix success. A trusted parent compares bounded child-probe
observations for separately human-reviewed code; premature exit-zero output
fails. This is not hostile-code containment.

Also fixed event/mode hook registration swaps, cwd-dependent launchers, delayed
output reservation, partial-copy ownership, temp-directory grants in examples,
and ambiguous GitLab host selection. The optional paid wrapper now forwards
only an explicitly selected credential into a fresh empty private HOME; fake
tests demonstrate that private captures can still contain a secret printed by a
child. The final cross-family re-review found no remaining high-severity issue;
its medium temp-grant documentation finding was then fixed. Approval is limited
to offline teaching artifacts, not activating integrations or production use.

## Pass 5 — Links, commands and configurations

The lead ran `python3 -B -m scripts.validate`: **50 repository tests, 3 app tests,
external baseline acceptance and static validation passed**. Coverage includes
malformed payloads, no secret-value inventory output, subprocess timeout/child
cleanup, missing executable, nonzero exit, JSONL framing, static hook behavior,
exact registration binding, private lab ownership and non-destructive cleanup,
real YAML/frontmatter parsing, plugin schema and deterministic packaging,
scenario contracts, relative Markdown links/anchors and generated drift.

The lead also ran the reference generator's `--check`, the headless repository
summary dry run, and the explicit-host GitLab dry run. Twelve isolated CLI
help/version captures have stored hashes. The optional source-link check first
found one redirect; after content review and a canonical-URL update, all
**24 source entries returned HTTP 200**. See [link results](links.json).
Hosted CI, Windows/macOS, authenticated smoke tests and every external Markdown
URL were not tested. JSONC is inventoried as unparsed; no JSONC asset is shipped.

## Pass 6 — Duplication and editing

README remains within the requested 500–800-word range. The migration matrix is
canonical for two generated references. Three skill definitions are authored
once; lab/plugin packaging copies them deterministically. Reorganized all 20
scenarios into scannable sections and added an enforced scenario contract.
Reconciled stale test counts and false runtime-evidence flags. Kept small topic
guides linked rather than duplicating the entire workflow into README.

## Pass 7 — Senior-developer usefulness

Checked that guidance leads to an action: a call-path investigation, reviewable
plan, narrow permission decision, failing reproduction, real acceptance oracle,
GitLab GET plan, explicit publishing boundary or evidence-qualified diagnostic.
Tests prove the deliberately broken fixture fails and the known fixes/features
pass independently of assistant assertions. HydraFusion comparisons have no
invented outcome. The lab's refactor is deliberately a small behavior-preserving
serialization extraction; multi-module coordination is taught as a workflow,
not presented as a tested large refactor.

## Remaining boundaries and deliberate deviations

- No authenticated Copilot/Claude/GitLab session, HydraFusion comparison, hook
  dispatcher, MCP client or plugin lifecycle was run. Copilot was checked only
  through isolated help/version; Claude and glab were absent globally.
- Headless output is structurally checked JSONL, not a presumed stable terminal
  event schema. Reports return unverified/pending statuses and executable checks
  require a separate human approval. Fake subprocess tests are not product tests.
- Full-repository validation uses optional PyYAML/jsonschema for correct parsers;
  the first lab is stdlib-only. CI dependency pins differ from locally installed
  validator versions, and hosted CI was not run.
- Evidence is organized as `evidence/` and `results/`, rather than a nested
  verification directory. No website or mandatory plugin framework was added.
- Broad-permission execution requires an independently provisioned disposable
  environment. No container/VM deployment or security-isolation claim is made.
- Existing repository JSONC is reported, not semantically migrated; active
  settings and credentials are never loaded by the inventory.
- No commits, pushes, merges, deployments, global upgrades or publication were
  performed. The files are delivered in the previously empty workspace.
