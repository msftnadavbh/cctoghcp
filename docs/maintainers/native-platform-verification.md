# Native practice: platforms and limits

Use Python 3.12+ with PowerShell 7+ on Windows or Terminal zsh on macOS. The
[first lesson](../start/first-15-minutes.md) provides shell-specific commands.
The native practice is stdlib-only; full repository validation additionally
requires [validator dependencies](../../requirements-validation.txt).

The practice passed on Windows Server 2025 (PowerShell 7, Python 3.12.10) and
macOS 26.6.2 arm64 (zsh, Python 3.12.10) in
[CI run 36757869730](https://github.com/msftnadavbh/cctoghcp/actions/runs/36757869730).
The run also checked the first lesson's failing baseline, diff and repaired
check. [Dated test counts](../../results/native-platform.json) identify the
revision and the Windows-only junction-test skip on macOS. These hosted runs
do not cover Microsoft Store Python or authenticated Copilot use.

## Practice commands

From any working directory, use the absolute path to your trusted book copy:

```text
python -I -B BOOK/scripts/practice.py setup LAB --exercise validation --with-config
python -I -B BOOK/scripts/practice.py diff LAB
python -I -B BOOK/scripts/practice.py check LAB --exercise validation
```

Replace `BOOK` and `LAB` and quote paths with spaces. Use `python` in PowerShell
or your installed Python 3.12+ executable (usually `python3`) in zsh. For a
quoted Python executable in PowerShell, prefix the command with `&`.

- `setup` creates a new lab; it never overwrites. Exercises are `validation`
  (default), `baseline`, `in-stock` and `refactor`. `--with-config` copies
  `CLAUDE.md`, its import, three skills and one agent; no hooks, MCP, plugins,
  credentials or Git remote are copied.
- `diff` displays added, changed and deleted files without running them. Exit 0
  does not mean the files match. Binary/control content is summarized by byte
  count: inspect it separately before executing it. Without `--with-config`,
  the six optional config files appear as deletions against the canonical copy.
- `check` runs the app tests and separate acceptance checks. Exit 0 passes;
  exit 1 means a failing check; exit 2 means a refused path, modified checker
  or invalid input. A new `validation` lab **should fail** its first check (exit 1).
  Fix `src/catalog.py` to reject boolean inputs to `integer()`, inspect the
  diff, then check again. `baseline` and `refactor` start passing; `in-stock`
  needs its feature implemented to pass.

## Paths and execution

Both book and lab must be ordinary local directories: OneDrive and other
cloud-managed/reparse directories, symlinks and junctions are unsupported.
Check for redirected Documents folders. The lab's parent must exist; the lab
itself must not exist or contain the book. Windows UNC/device, drive-relative,
root-relative, alternate-stream and reserved-name paths are refused. Use a
normal absolute Windows path without a trailing separator; on macOS use a
physical path rather than a symlink alias such as `/var`. Failed setup can
leave a partial copy: inspect it and choose a new name. There is no automatic
cleanup or overwrite command.

Diff and check refuse links and nonregular files. The lab is bounded to 1,000
entries, 256 KiB per file and 8 MiB of file data. Diff is **not** a secret
redactor. Each check prints `Check artifacts retained: PATH` for a new
`checkpoint-practice-*` directory in the OS temporary directory. Inspect
private output, stop remaining child processes, then remove that exact
directory manually. Do not publish captures without inspection.

Run only trusted, human-reviewed app and test code: the checker is **not an OS
sandbox**. Children run with fresh HOME, cwd and temporary directories and no
inherited token or Python startup variables; code can still access the host
or network. Output read into memory is bounded to 64 KiB per stream, but disk
output has no quota. Timeouts stop the direct child, not necessarily its
descendants. The checker itself must match the trusted book copy before use.
Advanced POSIX headless, GitLab and hook/MCP helpers are not Windows/macOS
native-practice commands.
