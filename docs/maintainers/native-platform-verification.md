# Native practice API and verification handoff

This is the implementation contract for the next documentation writer, not an
assertion that Windows or macOS CI has already run. Local evidence below is from
Linux with Python 3.12.3. Native Windows PowerShell 7+ and macOS zsh jobs are
configured in [the workflow](../../.github/workflows/validate.yml); their results
must be checked after the lead publishes the authorized branch.

## Commands and first-lesson outcomes

Use a trusted absolute path to `scripts/practice.py` and Python 3.12 or newer.
All commands work independently of cwd; invoke with isolation and no bytecode:

```text
python -I -B BOOK/scripts/practice.py setup LAB --exercise validation --with-config
python -I -B BOOK/scripts/practice.py diff LAB
python -I -B BOOK/scripts/practice.py check LAB --exercise validation
```

`BOOK` and `LAB` above are placeholders, not literal paths. Quote paths containing
spaces. In PowerShell use `python` with a quoted script path (or `&` before a
quoted absolute Python executable). In zsh, use the installed Python 3.12+
executable, commonly `python3`. Windows PowerShell 5 is not the supported shell.

- `setup`: exit 0, prints `Practice lab created: PATH`. Default exercise is
  `validation`; explicit choices are `validation`, `baseline`, `in-stock`,
  `refactor`. No config is copied unless `--with-config` is supplied.
- `diff`: exit 0 whether differences exist or not; exit 2 for refusal. It prints
  added/deleted/changed paths and UTF-8 text unified diffs without running lab code.
  Binary content (invalid UTF-8 or control/format characters other than tab/newlines)
  gets a byte-count summary, not replacement characters or raw binary output.
  Filename control/format characters are escaped in displayed paths. A byte-count
  summary requires separate inspection before executing that lab file.
  It compares against the fixed canonical app plus all six optional config
  assets. Without config, the six missing configs appear as deletions. This is
  intentionally stateless: even deletion of all six configs remains visible.
- `check`: exit 0 only when app tests and independent acceptance both pass;
  exit 1 for observed test/acceptance failure; exit 2 for invalid paths, options,
  missing files, modified checker, or other refused operations.
- Initial validation check is an **expected exit 1**, not a setup failure. The
  app runs three tests; boolean validation subtests fail. Independent acceptance
  includes `validation fails: boolean value accepted or wrong rejection`.
- Fix the single guard in `src/catalog.py` from `not isinstance(value, int)` to
  `type(value) is not int`. Check then exits 0 and prints
  `Independent acceptance passed: validation`. With unchanged copied config,
  diff prints `No differences from canonical files (the canonical validation
  bug is already fixed).` Diff is against the fixed source, not the broken setup.
- Baseline and refactor initially pass. In-stock initially fails until its API
  and CLI feature is implemented. Its oracle checks typed filtering, combined
  query/stock filtering, pagination, totals, invalid inputs, and CLI behavior.

## Files, paths, and retained results

Setup creates only `src/catalog.py`, `tests/test_catalog.py`, and
`scripts/check_lab.py`. Config adds the six exact byte-copied assets defined by
`CONFIG_ASSETS` in [scripts/lab.py](../../scripts/lab.py): `CLAUDE.md`,
`guidance/shared.md`, the repository-reviewer agent, and three skills. The
`CLAUDE.md` import target is included. No cache, whole test tree, ownership state,
Git metadata, hooks, MCP settings, plugins, credentials, or model activation is
copied. Canonical files are read only. Validation changes exactly one byte-string
guard occurrence; an unexpected canonical guard count refuses setup.

Both the book checkout and the lab must be ordinary local directories, not
OneDrive, other cloud-managed folders, symlink paths or Windows junctions. All
Windows reparse points remain refused; OneDrive is not supported. Check the
actual checkout location: Documents may be redirected even when HOME is local.

The destination must not exist, its parent must exist, and it must be outside
the book, not the book or an ancestor. Ordinary local absolute or relative paths
are supported, including spaces and Unicode. Parent traversal, symlink ancestors
or leaves, Windows reparse points/junctions, UNC/device paths, drive-relative or
root-relative Windows paths, alternate data streams, reserved names, trailing
dots/spaces, and other ambiguous Windows spellings are refused. Use absolute
Windows paths without a trailing separator, as in the first lesson. Existing
directory identities are also compared to reject aliases of the book or its
ancestors (including case aliases and Windows short names). On macOS, avoid
symlink aliases such as `/var` when supplying a path; use the physical path or an
ordinary directory under your home. Setup errors retain any partial copy: inspect
it manually and choose another destination name. There is no overwrite, reset,
cleanup command, or deletion authority.

Diff and check inspect the entire lab without following links. Limits are 1,000
entries, 256 KiB per regular file, and 8 MiB total file data. Added and deleted
files, including test and config changes, are visible to diff. Nonregular files
and links fail closed. Diff is a local review tool, **not a secret redactor**.

Each check prints `Check artifacts retained: PATH`. The path is a new
`checkpoint-practice-*` directory in the OS temporary directory. Each child has
a separate `probe-*` directory containing `stdin.bin`, `stdout.bin`, `stderr.bin`,
and an initially empty `home/`. Nothing recursively deletes this child-writable
tree. Review artifacts locally, stop any remaining descendants, then remove the
specific directory manually. Output may contain reviewed lab test diagnostics;
do not publish it without inspection. There is no result JSON schema.

## Execution boundary and limitations

Only use stable, trusted local trees and human-reviewed app/test code. This is
not a malicious-code sandbox or a defense against a same-user filesystem race.
The parent imports only trusted book modules, never lab code. A private observer
uses fixed Python argv with `-I -B`, never a general shell. It verifies the lab
checker is byte-identical to the canonical checker before execution. Modified
tests cannot bypass independent acceptance, which runs even after test failure.

Each child receives a neutral fresh cwd and fresh HOME/USERPROFILE/TMP/TEMP/TMPDIR.
Only these redirects, LANG, NO_COLOR, and Windows SystemRoot/WINDIR (when present)
are supplied. No inherited tokens, PATH, Python startup variables, or assistant
configuration is forwarded. This does **not** prevent reviewed code from reading
the host, accessing the network, writing elsewhere, or forging observations.

Input is file-backed and bounded to 64 KiB. Stdout/stderr are file-backed; the
parent reads at most 64 KiB plus one byte each after exit and returns at most
64 KiB each. Larger output fails with `output-limit`. Disk output is not quota
limited. Probe timeout is five seconds; the app-test child timeout is twenty
seconds; the nested sample CLI test timeout is five seconds. Timeout kills the
direct child only: descendant termination and disk containment are not
guaranteed. No automatic recursive cleanup runs against child-writable scratch.

Existing POSIX lab ownership/deletion helpers and POSIX runner security behavior
are unchanged. Headless execution, GitLab automation, secret inventory, hooks,
and MCP/plugin activation remain advanced POSIX workflows, not native practice
features.

## Verification commands and evidence

```text
python -B -m unittest discover -s tests -p test_practice.py -v
python -I -B labs/sample-app/scripts/check_lab.py
python -B -m scripts.validate
```

The first two are the native CI test commands (stdlib-only, no pip). Each native
job also runs the first-lesson shell commands in PowerShell 7 or zsh, checking
setup exit 0, broken check exit 1, diff exit 0, then copying the trusted canonical
source as a CI-only repair and checking exit 0. No model participates. The portable
suite includes an exact subprocess first lesson from outside the book, with
spaces and Unicode: setup succeeds, broken check fails, diff shows the guard,
fixed check passes. It also checks six config assets/import closure, no overwrite,
path refusals, partial-copy retention, unchanged canonical hashes, all-file diff
bounds, environment canaries, retained capture, checker tampering, fake tests,
malformed/no result, timeout/output limits, and known-good feature fixtures.
Windows lexical cases run on Linux too, but that is not native Windows evidence.
The junction test runs only on Windows; the native symlink test skips only when
Windows denies the symlink creation privilege.

Version-guard coverage simulates Python 3.9's version tuple in a subprocess and
checks the friendly message before project imports; it is not an older-interpreter
execution claim. Non-timeout probe tests use five seconds; only the deliberate
30-second sleep fixture uses a two-second timeout. CLI test subprocess temporary
directories stay under the test-owned tree and are verified before test cleanup.

Linux rerun after the display and lesson changes: portable suite 16 tests,
15 passed and one Windows junction test skipped. Full offline validation ran
67 tests, 66 passed and that same skip, plus three sample-app tests and
independent baseline acceptance. Reference generation `--check` and
`git diff --check` also passed. These are local Linux results, **not** hosted Windows or
macOS evidence. The last command remains the Ubuntu/full-suite job and is not
run in native jobs.
Raw help captures use `-text` in `.gitattributes` to preserve evidence hashes;
other files retain normal Git text handling. Copy and checker comparisons use
checkout bytes, including any checkout line endings.

Before merge, the lead must obtain native CI results and the required independent
Opus 5.5 `alternative-reviewer` review. No native execution, publication, commit,
or review is claimed by this handoff.
