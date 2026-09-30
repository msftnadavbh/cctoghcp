# First 15 minutes: trace and fix a validation bug

**Outcome:** Copilot identifies a shared boolean-as-integer defect, you approve one scoped change, and an independent check changes from failure to success. Install and log in to Copilot first using the [README](../../README.md). The practice path requires Python 3.12+ (`python --version` in PowerShell 7+, `python3 --version` in macOS zsh). On Windows, if `python` is missing, is a Store alias, or is too old, use `py -3.12 --version`; if that reports 3.12+, substitute `py -3.12` for **every** Windows `python` invocation below. Otherwise install/select Python 3.12+ before continuing. You may instead make the fix manually and still use the offline checks.

The commands below assume your terminal is **at this book's root**. Before setup, review what will be copied: `examples/coexistence/CLAUDE.md`, `examples/coexistence/guidance/shared.md`, `examples/agents/repository-reviewer.agent.md` and `.claude/skills/{repo-recon,reproduction-brief,verification-handoff}/SKILL.md`. The lab receives these as `CLAUDE.md`, `guidance/shared.md`, `.github/agents/repository-reviewer.agent.md` and `.claude/skills/...`; your existing project's guidance stays untouched. Set the variables once per shell and use the same shell throughout. The lab path must not already exist. It is outside the book so edits target a copy; CLI flags and prompts are not filesystem isolation.

Keep **both this book checkout and the lab in ordinary local directories**, outside OneDrive or other cloud-managed folders, symlink paths and Windows junctions. All Windows reparse points are refused; this is not a OneDrive-supported workflow. Check the actual checkout location: Documents may be cloud-redirected even when `$HOME` is local. Use absolute paths as shown, without a trailing separator.

**Windows PowerShell 7+:** set paths, then run the passing baseline. Stop if it does not exit 0.

```powershell
$Book = (Get-Location).Path
$Lab = Join-Path $HOME 'Copilot catalog practice'
$Practice = Join-Path $Book 'scripts/practice.py'
python -I -B (Join-Path $Book 'labs/sample-app/scripts/check_lab.py')
if ($LASTEXITCODE -ne 0) { throw 'Baseline failed; stop before creating a lab.' }
```

**macOS Terminal (zsh):** set paths, then run the same baseline. Stop if it does not exit 0.

```zsh
Book="$(pwd -P)"
Lab="$HOME/Copilot catalog practice"
Practice="$Book/scripts/practice.py"
python3 -I -B "$Book/labs/sample-app/scripts/check_lab.py"
echo $?
```

Expect three passing app tests; on macOS stop unless the displayed baseline exit is 0. **Stop** if setup fails: do not run `check` on an old or partially created lab. Run only the setup command for your shell:

```powershell
python -I -B $Practice setup $Lab --exercise validation --with-config
if ($LASTEXITCODE -ne 0) { throw 'Setup failed; inspect the destination and stop.' }
```

```zsh
python3 -I -B "$Practice" setup "$Lab" --exercise validation --with-config
echo $?
```

Setup must print `Practice lab created: ...` and exit 0. On macOS stop if the displayed exit is not 0. **Only after successful setup**, run the deliberately failing check:

```powershell
python -I -B $Practice check $Lab --exercise validation
$LASTEXITCODE
```

```zsh
python3 -I -B "$Practice" check "$Lab" --exercise validation
echo $?
```

The first check runs three app tests and separate acceptance checks: it **must exit 1**, with an `Independent acceptance failed:` message containing `validation fails: boolean value accepted or wrong rejection`. If setup refuses an existing path (exit 2), inspect that directory rather than overwriting it; choose a fresh lab name and update `$Lab` or `Lab`. Do not continue if the check exits 0 or 2. A check prints a retained artifact directory; keep its path private and review it before manual removal. This is not a malicious-code sandbox; only check code you have reviewed.

## Ask Copilot to investigate, then approve an edit

Before launching, ensure `COPILOT_ALLOW_ALL` is **unset** in this shell; a truthy value can autoapprove tools. Do not print its value or bypass organization policy. In PowerShell run `if ($env:COPILOT_ALLOW_ALL) { throw 'Open a shell without COPILOT_ALLOW_ALL before continuing.' }`; in zsh run `[[ -z "${COPILOT_ALLOW_ALL:-}" ]]` and stop unless its exit is 0. Launch from the book's terminal; `-C` selects the **lab** workspace, not your home or this book. If asked to trust it, review what will load; trust only this reviewed lab, for this session if offered, and stop on unexpected configuration. Do not assume `-C` alone grants path access.

```powershell
copilot -C $Lab --no-remote-export --disable-builtin-mcps --disallow-temp-dir '--available-tools=view,grep,glob'
```

```zsh
copilot -C "$Lab" --no-remote-export --disable-builtin-mcps --disallow-temp-dir '--available-tools=view,grep,glob'
```

Inspect `/env` and `/instructions`. Open `/permissions` to check the mode; it **switches modes**, so select manual approvals if needed, never broad approval. Verify the copied `CLAUDE.md` and its import are attached, workspace and grants are expected; stop if unexpected personal configuration loads. `--disallow-temp-dir` removes an automatic grant, not permission to the lab or an OS sandbox. At the Copilot prompt:

> Trace `integer()` through `Product`, `list_products`, `handle_request` and the CLI in this lab. Cite file and line for why a boolean is accepted as an integer and name a regression check. Report findings only: no edits, shell, network, or other directories.

Check the cited guard in `src/catalog.py` yourself. Python considers `bool` an `int` subclass here. Exit with `/exit`. To retain context, resume the lab session using `--resume` (select the session you just left) with the **edit** tool added only when ready to approve its requested writes:

```powershell
copilot -C $Lab --resume --no-remote-export --disable-builtin-mcps --disallow-temp-dir '--available-tools=view,grep,glob,edit'
```

```zsh
copilot -C "$Lab" --resume --no-remote-export --disable-builtin-mcps --disallow-temp-dir '--available-tools=view,grep,glob,edit'
```

Recheck the selected session's cwd and `/env`; use `/permissions` to keep manual approvals. If resume is unavailable, start a new lab session with the same flags **without** `--resume` and restate the confirmed defect before editing. Ask:

> Change the shared `integer()` guard in `src/catalog.py` to reject bool but accept actual integers. Only edit `src/catalog.py` and, if needed, `tests/test_catalog.py`. Do not run tests or shell commands. Present the diff; stop on any other path or permission request.

Approve only the reviewed file edits, then `/exit`. Back in the book terminal, run **only diff** first:

```powershell
python -I -B $Practice diff $Lab
```

```zsh
python3 -I -B "$Practice" diff "$Lab"
```

**STOP AND REVIEW** the full lab diff, including tests, new/deleted files and copied instructions. If `diff` refuses a file or summarizes binary/control content, inspect that file separately; a byte count is not code review. `diff` compares against the already-correct source, so no differences is expected **only** if your repaired source, tests and config all match the canonical files; confirm the recorded initial failure too. Only after you have reviewed the code it will execute, run the final check:

```powershell
python -I -B $Practice check $Lab --exercise validation
$LASTEXITCODE
```

```zsh
python3 -I -B "$Practice" check "$Lab" --exercise validation
echo $?
```

The correct guard is `type(value) is not int` instead of `not isinstance(value, int)`. An unchanged copied test/config plus the correct repair prints `No differences from canonical files (the canonical validation bug is already fixed).` Final check exits 0, runs three app tests and prints `Independent acceptance passed: validation`. If it fails, inspect the diff and error; don't widen permissions to make it pass.

To resume this work later use `copilot --resume` to choose the session, then check its cwd and grants; `--continue` may select an unrelated recent session. Keep the **same lab** for [first hour](first-hour.md). When finished, leave Copilot, stop any remaining processes, and remove **only the specific lab directory you created**, manually in Explorer or Finder after inspecting its contents. There is no automatic cleanup or reset. Review each `Check artifacts retained:` path before removing its specific directory too.
