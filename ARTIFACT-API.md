# Foundation artifact API

Run commands from the repository root, except the standalone lab checker.
This is the advanced POSIX automation contract. For native Windows PowerShell 7+ or macOS zsh practice, use [first 15 minutes](docs/start/first-15-minutes.md) and `scripts/practice.py` instead of the legacy setup/cleanup commands below.

## Offline commands

| Command | Contract |
| --- | --- |
| `python3 -B -m scripts.validate` | Static checks, repository unittests, standalone app tests, external baseline oracle. No network or assistant CLI. Exit 0 passes; 1 fails. Requires optional validator libraries already installed. |
| `python3 -B labs/sample-app/scripts/check_lab.py` | First lab, stdlib only. No installation, registry, credentials, Git or network required. |
| `python3 -B -m scripts.validate --static-only` | Documentation/config/evidence/package checks, no test processes. |
| `python3 -B -m scripts.inventory . --json` | Passive bounded inventory, known path/field names and categories only. Found does not mean supported. Human output omits `--json`. |
| `python3 -B -m scripts.lab setup '/tmp/my catalog lab' --state /tmp/checkpoint-state --exercise validation` | Requires a nonexistent destination. Creates a private 0700 fixture with external ownership record and matching marker before copying. Parent directories must exist. No Git init/remotes/commits. Partial failures remain identifiable by the external record. |
| `python3 -B -m scripts.lab cleanup OWNERSHIP_ID --state /tmp/checkpoint-state` | Deletes only recorded path after ID, owner, inode, device, mount, symlink and special-file checks. Never accepts a deletion path. |
| `python3 -I -B labs/expected-results/acceptance.py '/tmp/my catalog lab' validation` | Human-reviewed Python only. Trusted parent never imports lab code; bounded child probes use fresh empty HOME and neutral cwd. Parent checks exact observations, schema/count/types/values and CLI output, not just exit 0. Not a malicious-code sandbox: same-user code can forge observations or access the host. |
| `python3 -B -m scripts.package_plugin /tmp/checkpoint-skills.zip` | Exclusive-create deterministic ZIP, root `plugin.json` plus three skill files. Add `--directory` for a new unpacked directory instead. |
| `python3 -B -m scripts.secret_gate labs/fixtures/ci-sanitized.log` | Independent bounded heuristic secret gate, never prints matches or input. Exit 1 rejects. |

Setup exercise names: `baseline`, `validation`, `in-stock`, `refactor`. Only
`validation` injects a defect. Fix that copy, then implement the `in-stock`
acceptance on the same app for the first-hour progression. A fresh `in-stock`
copy starts from the passing baseline without the feature. `refactor` starts
passing and must stay passing. See [exercise contracts](labs/exercises.json).
The fleet tasks are read-only investigations, not automatic model execution.

Setup `--with-config` is explicit and off by default. It copies only the six
files in `scripts.lab.CONFIG_ASSETS`: canonical coexistence `CLAUDE.md` plus
`guidance/shared.md`, three canonical skill files and the reviewer agent at
`.github/agents/repository-reviewer.agent.md`. No settings/hooks/MCP/conflict
rules or whole fixture trees are copied. The configured interactive tutorial
inspects these existing instructions; a trusted GitLab clone retains its own
audited instructions instead. Headless scenarios stay bare.

## Python seams

- `labs/sample-app/src/catalog.py`: frozen `Product(sku, name, price_cents,
  in_stock)`, `integer(value, name, low, high)`, `list_products(products=PRODUCTS,
  *, query='', offset=0, limit=20)`, `handle_request(params)`, `main(argv=None)`.
  Request output keys: `items`, `total`, `offset`, `limit`. Item keys are the
  Product fields. Booleans are not integers. Invalid inputs raise `ValueError`.
- `scripts.lab.setup(dest, state, exercise='baseline', with_config=False) -> ownership dict`;
  `cleanup(id, state) -> None`. Ownership records are trusted local state:
  do not share the state directory or run cleanup concurrently with edits.
- `scripts.runner.run(argv, *, cwd, env, stdin=b'', timeout=20, limit=262144)`
  returns `Result(status, returncode, stdout, stderr)`. Separate bounded bytes;
  no shell. `save(result, new_directory)` creates private output files.
- `scripts.safety.sanitized_ci(raw) -> bytes`: lossy JSON allowlist, retaining
  only success/failure observations and fixed explanatory text. Unknown lines,
  URLs, names, paths and values are discarded, not merely regex-redacted.

## Explicit integration boundaries

`python3 -B -m scripts.headless MODE --repo LAB --prompt-file REVIEWED_FILE`
is a dry run. Modes: `repo-summary`, `diff-review`, `test-fix`,
`gitlab-log-summary`. Execution additionally requires **all** of `--execute`,
`--consent-paid`, `--reviewed-workspace`, `--credential-env COPILOT_GITHUB_TOKEN`,
`--home FRESH_EMPTY_HOME`, and `--output NEW_PRIVATE_DIRECTORY`.
Optional `--executable` and `--timeout`. Dry-run may omit the credential flag.
Only that selected token variable is forwarded, after checking presence,
nonblank value and no NUL/newline; other token/provider variables are excluded.
No token goes in argv or the public report. Use an entitled personal account's
fine-grained PAT with **Copilot Requests** account permission. This is source
review only, not a tested login/model flow; interactive OAuth is unchanged and
BYOK is unsupported here. [source:copilot-authentication]
HOME must be fresh, empty, owned and exactly 0700 outside the
lab; use a fresh HOME again if the CLI writes configuration. Preflight refuses known active config
locations in the workspace and every ancestor, HOME `.copilot`, shared Claude
settings, plugins/extensions/LSP/grants and other known configuration roots,
including malformed configurations. Presence of `/etc/github-copilot` refuses
execution without bypass. This is a conservative fixed-location profile, not a
complete runtime-policy resolver. Credentials embedded in settings are refused.
`.vscode/mcp.json` is also conservatively refused, not claimed as a supported
Copilot runtime source. The wrapper supplies `--secret-env-vars=COPILOT_GITHUB_TOKEN`,
but does not guarantee that child stdout/stderr were redacted: private captures
can contain a token if a child prints it. Never publish them automatically.
The absolute executable resolves through trusted `/usr/bin:/bin` or an explicit
absolute path. Output is atomically reserved 0700 outside both lab and HOME
before spawning. `--disallow-temp-dir` removes implicit temp access; permission
matching and flags still are not a sandbox.
Prompt bytes use stdin, not argv; real Copilot stdin and JSONL integration have
**not** been tested. JSONL validation is structural only: nonempty typed objects,
bounded output, complete lines and no duplicate keys. Unknown event types are
retained privately; no terminal event or semantic completion is assumed.
No fallback to broad permissions. `test-fix` performs syntax/secret checks only,
never imports or runs generated code, and returns `validation-pending`. Review
the diff before running the separate acceptance CLI. Other modes return
`report-unverified`, even on process exit 0; humans assess report semantics.

Headless exit codes: 0 dry-run only; 2 rejected request; 10 missing executable;
11 launch error; 12 timeout; 13 output limit; 14 nonzero child exit; 15 invalid or
incomplete JSONL; 16 failed static check; 17 validation pending; 18 report unverified. Private stdout/stderr
may contain sensitive model content; never publish them automatically.

`python3 -B -m scripts.gitlab --hostname gitlab.example.com --project group/project --pipeline 3 --job 5`
prints a read plan and human-only draft MR argv. `--execute-read --home HOME
--output NEW_FILE` explicitly permits GET requests only; `--executable` defaults
to `glab`. Every GET carries explicit `--hostname` and runs in a neutral temporary
cwd, not a Git checkout. HOME and atomically reserved output must be outside the
calling workspace and separate from each other. Checks job-to-pipeline identity, sanitizes trace before storage, never
fetches variables or publishes. Fake glab only has been tested. No token values
belong in arguments, templates, reports or documentation.

## Inert examples and optional discovery

- [Native hooks](examples/hooks/native.json) and
  [shared settings](examples/hooks/shared-settings.json) are alternatives:
  register **one**, not both, after replacing the reviewed paths. Shared commands
  use a reviewed absolute launcher outside the lab, independent of process cwd:
  `/usr/bin/python3 -I -B /ABSOLUTE/checkpoint/scripts/trusted_launcher.py hook pre|post --lab ABSOLUTE_LAB` (JSON stdin),
  optional `--event-log PRIVATE_FILE`. Native `toolArgs` accepts object or JSON
  string; compatible `tool_input` requires matching `hook_event_name`. Mixed
  formats, duplicate keys, missing tool/cwd, malformed inputs and unknown tools
  reject. Neutral response is `{}`, never unconditional allow. Only edits to
  `src/*.py` (including nested paths) are considered; arbitrary shell and patch
  tools reject. This is a targeted demo policy, not a fully usable runtime tool
  policy. Reads remain subject to normal CLI permissions. Post-edit checks parse
  only the actual accepted file (including nested paths) with bounded AST/secret
  checks and never execute code. Handled post failures, malformed inputs and log
  failures exit 0 with `additionalContext`; static success is not full validation.
  Payload cwd remains LAB even when process cwd differs. Handler tests are not dispatcher
  tests. **SOURCE REVIEW:** Copilot command hook timeouts fail open; CI is the
  independent authoritative gate. [source:hooks-reference]
  Config validation binds each pre/post event to its entire exact launcher argv
  or shared command; swaps/suffixes reject. Native payload event identity cannot
  be inferred from `toolResult`; it depends on correct registration.
- [MCP templates](examples/mcp/local.json) are not installed. The synthetic
  local template uses the same absolute trusted launcher with `-I -B`, mode `mcp`.
  server implements newline JSON-RPC MCP 2025-11-25 initialize/initialized, ping,
  tools/list, tools/call, one fixed no-argument tool. Unit protocol checks only.
  GitLab HTTP/glab templates are experimental, inert, credential-free and not
  CLI-integration-tested. Do not infer glab server-command availability.
- Canonical skill text exists only in `.claude/skills/*/SKILL.md`; build outputs
  copy it mechanically. Agents use `view`, `grep`, `glob`; compatibility fixtures
  live under `examples/coexistence`. Fixtures do not establish precedence.
- `python3 -B -m scripts.capture_help --executable RESOLVED_LOADER --home
  ISOLATED_HOME --output NEW_DIRECTORY` executes a fixed allowlist of help and
  version commands only. [Captures](results/help/capture.json) contain hashes,
  exit statuses and timestamps. Plugin lifecycle was not run: install help omits
  local paths despite official documentation including them.
- `python3 -B -m scripts.check_links` is dry-run; `--network` explicitly enables
  bounded HEAD checks of source URLs. Redirects need review; 401/403 are
  auth/forbidden, 429 rate limits, 5xx/timeouts transient. No automatic redirects,
  credentials, proxies or logged URL values. Exceptions require source ID,
  status, reason, review date and expiry in the exception ledger.

## Documentation and evidence contract

Use [sources](evidence/sources.json), [claims](evidence/claims.json),
[commands](evidence/commands.json), and
[compatibility cases](evidence/compatibility-cases.json). IDs are unique kebab
case. Sources record retrieval date and provenance. Claims require source IDs,
status, preview boolean, limitations. Use `[source:ID]` and `[claim:ID]` markers;
preview claims require a visible preview label. New Markdown files are checked
automatically for relative links, anchors, reference links, frontmatter, fence
balance, whitespace and unreviewed placeholders. The checker supports ordinary
Markdown links, not every CommonMark extension; keep documentation conservative.
Real YAML uses PyYAML; JSON-as-YAML is the canonical config/frontmatter subset.
No canonical JSONC assets are validated; passive inventory reports known JSONC
files as unparsed without exposing contents. No general JSONC parser is claimed.
Plugin validation uses real jsonschema against the vendored Agent Plugins 1.0
schema. No custom full-YAML parser or pretend schema validator.

Optional repository validators: [pinned dependencies](requirements-validation.txt).
CI installs these before offline checks; that dependency bootstrap uses a package
registry, while the first standalone Python lab does not. Local observed versions
are recorded separately from CI pins. No root hook/MCP activation is present.
No global installation, authentication probe, model call, commit or publish was
performed by this foundation. Safety helpers are POSIX/Linux-oriented and not a
hostile same-user race or process-escape sandbox. Lead must arrange independent
Opus 5.5 `alternative-reviewer` review before activation or release.

The acceptance child imports the single `src/catalog.py` file in isolation.
The refactor exercise means pure-function extraction within that file, not
arbitrary package/module restructuring; larger refactors need a reviewed probe
contract change.
