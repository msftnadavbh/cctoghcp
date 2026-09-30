# First 15 minutes: investigate and repair a local task with Copilot

**Primary path:** an entitled, authenticated developer with an installed Copilot CLI; Python 3 and Git installed. This local exercise requires no source remote. The lead's isolated 1.0.89 installation captured help only; the steps below are an **operator walkthrough**, not a transcript or authenticated test. Reserve enough time for login beforehand; 15 minutes describes the exercise, not account provisioning. Never run the assistant against this repository's original sample. [source:cli-reference]

## 1. Prepare and inspect the copy

From the repository root, run the stdlib baseline and create a **nonexistent** private destination. Keep the ownership ID for cleanup. `--with-config` explicitly copies only the reviewed canonical fixture `CLAUDE.md`, its relative import, three canonical skills and the repository reviewer agent; no `.git`, settings, hooks, MCP, plugins or conflict rules. Review these assets before using the flag. A partial setup has an external ownership record and `.checkpoint-owner` marker. Bare setup remains the default for headless scenarios.

```sh
python3 -B labs/sample-app/scripts/check_lab.py
python3 -B -m scripts.inventory .
python3 -B -m scripts.lab setup '/tmp/my catalog lab' --state /tmp/checkpoint-state --exercise validation --with-config
python3 -I -B labs/expected-results/acceptance.py '/tmp/my catalog lab' validation
```

The final check **must initially fail**: the copy's `integer()` erroneously accepts a boolean. Stop if the copy does not match this failure. Before trusting a live CLI, inspect personal and workspace configuration and machine policy for unexpected instructions, grants, MCP, hooks, plugins and credentials. `scripts.inventory` only lists known repository paths; it cannot audit your home or prove runtime behavior. Do not paste that home inventory or tokens into a prompt. Check `copilot --version` against [observed 1.0.89 help](../../results/help/capture.json); optional `copilot login` or interactive `/login` invokes OAuth and stores credentials (possibly plaintext fallback). Approve it separately and keep login distinct from source-host credentials. If no entitlement, follow the **offline sidebar** below. [source:cli-reference]

## 2. Investigate with read tools only

Start interactive Copilot on the owned copy in **manual** permission mode. Inspect `/env`, `/instructions` and `/permissions` before a paid prompt. Check discovery/attachment of the existing fixture `CLAUDE.md` and `guidance/shared.md`; do not generate replacement instructions or assume discovery proves inheritance. Stop if unexpected configuration loads. No hook/plugin/MCP setup is part of this lesson. For an existing trusted checkout instead, audit and retain its own `CLAUDE.md` and imports; do not overwrite them with this synthetic fixture.

```sh
copilot -C '/tmp/my catalog lab' --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob
```

In the CLI, use `/env`, `/instructions`, `/permissions`, then submit this exact bounded task. If the environment requests repo trust, review what it would load and **do not** assume path access has been granted solely by the `-C` option:

> Trace `integer()` through `Product`, `list_products`, `handle_request` and CLI in this copy. Cite file and line for the boolean-as-int defect and name the smallest regression check. First report findings **without edits**. Do not access other directories, network, credentials or remotes.

Compare the answer with actual code; `/exit` this read-oriented session. Record its ID and **explicitly** resume that same session, adding the edit tool only after a human approves the two owned files:

```sh
copilot -C '/tmp/my catalog lab' --resume=REVIEWED_SESSION_ID --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob,edit
```

Recheck `/cwd`, `/env` and permissions on resume. Ask: “Fix the shared `integer()` guard to reject bool while preserving valid integers. Change only `src/catalog.py` and, if needed, `tests/test_catalog.py`. Do not run code or write outside those files; stop on a permission mismatch.” Approve **only** reviewed edit requests; `--available-tools` limits visibility, but CLI permission matching, path verification and OS isolation remain separate. No agent shell tool is offered. `--disallow-temp-dir` removes the CLI's *automatic temp-directory grant*; this fixture itself is under `/tmp`, so verify cwd trust/path access independently. Its runtime effect on this lab was **not** tested here, and the flag is no sandbox. [claim:selective-tools]

Exit with `/exit`. From a trusted terminal **at the original repository root**, review the copy against the frozen baseline with `git diff --no-index labs/sample-app/src/catalog.py '/tmp/my catalog lab/src/catalog.py'` (exit 1 means a diff exists, not a test failure). Also inspect the test diff if changed. Do not run newly written code until the diff has been reviewed. This diff is against the original *passing* sample, so a correct repaired copy may have **no source diff**; compare the previously recorded broken line and both before/after oracle exits to prove that the exercise was actually fixed. Then:

```sh
python3 -I -B labs/expected-results/acceptance.py '/tmp/my catalog lab' validation
python3 -I -B labs/expected-results/acceptance.py '/tmp/my catalog lab' baseline
```

Both should pass **after** a correct fix; the trusted oracle parent does not import lab code, but its child probes execute reviewed code with a fresh HOME. It is not a hostile-code sandbox. For continuity, `--continue` selects the most recent session, **not necessarily** one for this directory; use `copilot --resume` to select or the reviewed ID with the same `-C`, privacy and temp flags shown above, then recheck `/env` and workspace. Don't mistake resume for Git rollback. [source:cli-reference]

**Offline sidebar (no login/model call):** run the same setup, read `src/catalog.py`, make the shared repair manually and use the same diff/oracles. This verifies the lab, not Copilot. Cleanup is `python3 -B -m scripts.lab cleanup OWNERSHIP_ID --state /tmp/checkpoint-state` from the original repo root, after leaving the lab and stopping tasks. It accepts only the recorded ID; don't share state or race cleanup. Proceed on the **same copy** to [first hour](first-hour.md), or clean when done.
