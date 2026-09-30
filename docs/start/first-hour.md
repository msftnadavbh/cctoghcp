# Optional practice: first hour, plan and build a stock filter

**Optional exercise, not a prerequisite for [your own checkout](use-copilot-in-your-repository.md).** Continue the **same repaired lab** and shell variables (`$Lab`, `$Practice` in PowerShell or `Lab`, `Practice` in zsh) from [first 15 minutes](first-15-minutes.md). Don't set up another lab: this feature builds on the validation fix. Your task is optional `in_stock=None|bool` filtering in `list_products`, `handle_request` and CLI `--in-stock true|false`. Keep the response keys `items,total,offset,limit` and their existing types; `None` preserves unfiltered output, `True`/`False` select exact booleans. Reject integer, string, list and dict API values; filter by query **and** stock before pagination and count filtered matches in `total`. CLI invalid stock values exit 2 with an error on stderr, not JSON on stdout.

## Establish the before state

In PowerShell 7+:

```powershell
python -I -B $Practice check $Lab --exercise validation
$LASTEXITCODE
python -I -B $Practice check $Lab --exercise in-stock
$LASTEXITCODE
```

In macOS zsh:

```zsh
python3 -I -B "$Practice" check "$Lab" --exercise validation
echo $?
python3 -I -B "$Practice" check "$Lab" --exercise in-stock
echo $?
```

Validation must exit 0; **stop** if it doesn't. The stock feature must initially exit 1; stop if it exits 0 or 2 instead. The checker runs app tests **and** independent acceptance. Review the code before running these checks; its child processes can execute code from your lab. Retained check artifacts are private until inspected. If a new shell was opened, reset the variables and `COPILOT_ALLOW_ALL` guard from the first lesson before launching Copilot.

## Plan, inspect, implement

Start Copilot with read tools only (choose the command for your shell):

```powershell
copilot -C $Lab --no-remote-export --disable-builtin-mcps --disallow-temp-dir '--available-tools=view,grep,glob'
```

```zsh
copilot -C "$Lab" --no-remote-export --disable-builtin-mcps --disallow-temp-dir '--available-tools=view,grep,glob'
```

Check `/env`, `/instructions` and `/skills`. Use `/permissions` to check or select **manual** approvals; the command changes mode, it isn't a read-only status command. If `reproduction-brief` appears in `/skills`, you may ask Copilot to use it for the brief; if not, use the prompt below without installing anything. Skill discovery is not permission to write. Switch to `/plan` and submit:

> Plan `in_stock=None|bool` in `list_products` and `handle_request`, and CLI `--in-stock true|false` in this lab. Preserve `items,total,offset,limit` and their types. Combine query and stock filters before pagination; `None` changes nothing; reject ints, strings, lists, dicts and invalid CLI values (exit 2, stderr error, no JSON stdout). Identify callers, the two editable files (`src/catalog.py`, `tests/test_catalog.py`), negative tests, check commands, rollback and stop conditions. Plan only; no edits or code execution.

Inspect the plan; Ctrl+Y edits it where supported. Compare it with the [planning checklist](../workflows/planning.md). If restricted tools prevent saving a `plan.md` or Ctrl+Y isn't available, keep the approved plan in the conversation or a human-owned note; do not grant writes just to persist it. For a second perspective inspect `/agent`: the copied repository reviewer can be requested to **read** and critique filter order and invalid inputs, but it cannot run tests with `view,grep,glob`. Check whether its instructions attach when invoked as a subagent; don't mistake a review for independent acceptance. Exit with `/exit` after approving the plan.

Resume **that lab's plan session** with edit available, keeping manual approvals:

```powershell
copilot -C $Lab --resume --no-remote-export --disable-builtin-mcps --disallow-temp-dir '--available-tools=view,grep,glob,edit'
```

```zsh
copilot -C "$Lab" --resume --no-remote-export --disable-builtin-mcps --disallow-temp-dir '--available-tools=view,grep,glob,edit'
```

Select the plan session and recheck its cwd, `/env` and manual `/permissions` mode. If resume is unavailable, start a fresh lab session without `--resume` and paste the approved contract above before requesting edits; don't assume a new session recalls your plan. First ask: “Implement the approved `list_products` and `handle_request` API contract and focused tests only. Edit `src/catalog.py` and `tests/test_catalog.py`; do not run code or shell. Present the diff.” Review the edits. Next ask for the CLI parsing seam in the **same two files**; recheck approval mode on every new session and approve only those paths. If using `/autopilot` instead, set a bounded completion condition and leave shell unavailable; [Autopilot](../workflows/autopilot.md) explains why continuation isn't test certification.

## Verify and hand off

After `/exit`, run **only diff** (PowerShell or zsh):

```powershell
python -I -B $Practice diff $Lab
```

```zsh
python3 -I -B "$Practice" diff "$Lab"
```

**STOP AND REVIEW** all changed/added/deleted source, test and instruction files. If `diff` refuses a file or shows only a byte-count summary for it, inspect that file separately; don't run code based on a summary. Only after approving executable changes, run both checks; stop if either does not exit 0. Then, and only then, run the CLI example:

```powershell
python -I -B $Practice check $Lab --exercise validation
if ($LASTEXITCODE -ne 0) { throw 'Validation failed; stop before the next check.' }
python -I -B $Practice check $Lab --exercise in-stock
if ($LASTEXITCODE -ne 0) { throw 'In-stock failed; stop before running the CLI.' }
```

```zsh
python3 -I -B "$Practice" check "$Lab" --exercise validation
echo $?
```

Stop unless the displayed validation exit is 0; then run:

```zsh
python3 -I -B "$Practice" check "$Lab" --exercise in-stock
echo $?
```

After **both** check exits are 0, the following executes the reviewed lab app directly, with your ordinary shell environment (unlike the checker’s fresh child environment):

```powershell
python -I -B (Join-Path $Lab 'src/catalog.py') --in-stock true --offset 1 --limit 1
```

```zsh
python3 -I -B "$Lab/src/catalog.py" --in-stock true --offset 1 --limit 1
```

Both checks should exit 0. The CLI should output JSON with `total: 2` and the single second in-stock product (`sku: "C3"`). If it does not, inspect the failing assertion and code rather than broadening access. Write down changed paths, actual exits, permissions and unresolved decisions; use `copilot --resume` to choose a session and verify the lab before continuing. The lab has no Git remote: [first real feature](first-real-feature.md) shows how to transfer **reviewed** work to an authorized checkout, not how to publish the lab.
