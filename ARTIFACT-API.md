# Optional POSIX helper reference

Run these commands from the book root. For native Windows PowerShell 7+ or
macOS zsh practice use [the first lesson](docs/start/first-15-minutes.md) and
`scripts/practice.py` instead. The POSIX helpers do not provide a hostile-code
sandbox.

## Offline commands

| Command | Action |
| --- | --- |
| `python3 -B -m scripts.validate` | Static checks, repository tests, app tests and baseline acceptance; optional [validator dependencies](requirements-validation.txt) required. |
| `python3 -B -m scripts.validate --static-only` | Static docs, configuration, evidence and package checks. |
| `python3 -B labs/sample-app/scripts/check_lab.py` | Stdlib-only app check. |
| `python3 -B -m scripts.inventory . --json` | Reports known configuration paths and field names, not file contents or effective CLI settings. |
| `python3 -B -m scripts.lab setup '/tmp/my catalog lab' --state /tmp/checkpoint-state --exercise validation` | Creates a private 0700 lab at a nonexistent path with a separate ownership record. Parent directories must exist. |
| `python3 -B -m scripts.lab cleanup OWNERSHIP_ID --state /tmp/checkpoint-state` | Deletes only the recorded lab after identity, inode, device, mount, symlink and special-file checks. Do not race edits or share state. |
| `python3 -I -B labs/expected-results/acceptance.py '/tmp/my catalog lab' validation` | Runs independent acceptance after reviewing lab code; child probes execute that code, not in a sandbox. |
| `python3 -B -m scripts.package_plugin /tmp/checkpoint-skills.zip` | Creates a deterministic ZIP at a new path; `--directory` creates an unpacked directory. Neither installs a plugin. |
| `python3 -B -m scripts.secret_gate labs/fixtures/ci-sanitized.log` | Bounded heuristic secret check; exit 1 rejects without printing matched values. |

Exercises: `baseline` and `refactor` start passing, `validation` has a boolean
guard defect, and `in-stock` needs an API/CLI feature. See
[exercise contracts](labs/exercises.json). `scripts.lab setup --with-config`
copies only `CLAUDE.md`, its import, three skills and one reviewer agent. It
does not copy hooks, MCP, plugins or a Git remote. Setup never overwrites an
existing path; after partial failure use the ownership ID for cleanup only
after inspecting state.

For Python callers: `scripts.lab.setup(dest, state, exercise='baseline',
with_config=False)` returns an ownership record; `cleanup(id, state)` uses that
record, not a deletion path. `scripts.runner.run(argv, *, cwd, env, stdin=b'',
timeout=20, limit=262144)` returns separate bounded `status`, `returncode`,
`stdout` and `stderr`; `save(result, new_directory)` creates private output.
`scripts.safety.sanitized_ci(raw)` returns a lossy allowlist, discarding names,
URLs, paths and unknown lines. The catalog API has `Product(sku, name,
price_cents, in_stock)`, `list_products(*, query='', offset=0, limit=20)` and
`handle_request(params)`; request output uses `items`, `total`, `offset` and
`limit`. Invalid inputs raise `ValueError`, including booleans where integers
are required.

## Optional external integrations

`python3 -B -m scripts.headless MODE --repo LAB --prompt-file REVIEWED_FILE`
dry-runs `repo-summary`, `diff-review`, `test-fix` or `gitlab-log-summary`.
Execution requires **all** `--execute`, `--consent-paid`,
`--reviewed-workspace`, `--credential-env COPILOT_GITHUB_TOKEN`,
`--home FRESH_EMPTY_HOME` and `--output NEW_PRIVATE_DIRECTORY`, plus a reviewed bare disposable lab. Use an entitled
personal fine-grained token with **Copilot Requests** permission; see
[authentication](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli).
The token must be nonblank without NUL/newline; only the selected variable is
forwarded, never a token in argv or a public report. BYOK is unsupported here.

HOME must be fresh, empty, owned, 0700 and outside lab/output. Preflight
refuses known active configuration in the workspace, ancestors and HOME, and
refuses `/etc/github-copilot`; this is not a complete policy resolver.
Output is reserved privately before spawning. `--disallow-temp-dir` and tool
grants are not OS isolation. Private stdout/stderr may contain a token printed
by a child despite requested CLI redaction: never publish them automatically.
The helper passes prompt bytes on stdin without `-p`; confirm real CLI stdin
support before relying on it. It checks only bounded JSONL framing, **not task
completion**. Unknown events remain private; `test-fix` returns
`validation-pending` after static checks, and other modes return
`report-unverified`. Review the diff, then separately run acceptance on
reviewed code. No permission fallback to `--allow-all`.

Headless exits: 0 dry run, 2 rejected request, 10 missing executable,
11 launch error, 12 timeout, 13 output limit, 14 child failure,
15 invalid/incomplete JSONL, 16 static check failure, 17 validation pending,
18 report unverified.

`python3 -B -m scripts.gitlab --hostname gitlab.example.com --project group/project --pipeline 3 --job 5`
prints a GET plan and a draft MR command; it does not read or publish. For an authorized read,
add `--execute-read --home HOME --output NEW_FILE`. Supply real host, project, pipeline and job IDs.
The helper uses explicit `--hostname` and GET, checks job/pipeline identity,
and saves only a lossy sanitized trace to new private output outside the
workspace and credential HOME. It never fetches variables, pushes or creates
an MR. Review raw CI traces privately; do not give them to a model.

## Inert examples

- [Native hooks](examples/hooks/native.json) and
  [shared hooks](examples/hooks/shared-settings.json) are alternatives, not
  registrations. Choose **one** after reviewing the absolute interpreter,
  launcher and target lab. `/usr/bin/python3 -I -B /ABSOLUTE/checkpoint/scripts/trusted_launcher.py hook pre|post --lab ABSOLUTE_LAB`
  reads JSON on stdin; native `toolArgs` and compatible
  `tool_input` require their respective payload forms. Unknown tools and
  malformed payloads reject; post-edit static checks do **not** execute edited
  Python or pass behavioral tests. Handled post failures can exit 0 with
  `additionalContext`. [Hook timeouts can fail open](https://docs.github.com/en/copilot/reference/hooks-reference): keep independent CI.
- [Local MCP template](examples/mcp/local.json) starts the trusted launcher in
  `mcp` mode with `/usr/bin/python3 -I -B`; the synthetic server implements
  `initialize`, `ping`, `tools/list` and one fixed `tools/call`. Protocol checks
  do not activate a Copilot MCP client. [GitLab templates](examples/mcp/gitlab-http.experimental.json)
  are experimental and require separate transport, permission and credential
  review.
- [Help capture](results/help/capture.json) stores hashes and exit statuses for
  a fixed allowlist of help/version commands. Before a plugin install, inspect
  your own CLI's `plugin install --help` and the package contents.
- `python3 -B -m scripts.check_links` is a dry run; `--network` enables bounded
  HEAD checks of source URLs, with redirects and exceptions requiring review.

The [source](evidence/sources.json), [claim](evidence/claims.json),
[command](evidence/commands.json) and [compatibility](evidence/compatibility-cases.json)
records support the generated [migration reference](docs/reference/muscle-memory.md).
`scripts.validate` checks source IDs, preview labels, relative links, Markdown
anchors and the vendored Agent Plugins schema. Full validation uses PyYAML and
jsonschema; the standalone lab remains stdlib-only. JSONC discovered by the
inventory is not parsed or activated.

The acceptance oracle loads only the single `src/catalog.py` module. The
`refactor` exercise covers pure-function extraction in that file; larger
reorganizations need a separately reviewed acceptance contract.
