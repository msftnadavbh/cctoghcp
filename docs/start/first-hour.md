# First hour: plan, implement, review and resume

**Continue the repaired `/tmp/my catalog lab`** from [first 15 minutes](first-15-minutes.md); do not reset it with `--exercise in-stock` (that produces a different baseline). The goal is optional `in_stock=None|bool` through `list_products`, `handle_request` and CLI `--in-stock true|false`. Filter before pagination, preserve the filtered total and existing unfiltered output; reject integer/string filter values. The [contract](../../labs/exercises.json) and [API](../../ARTIFACT-API.md) define exact seams. The separate external `in-stock` oracle should fail before implementation, while `validation` now passes.

```sh
python3 -I -B labs/expected-results/acceptance.py '/tmp/my catalog lab' validation
python3 -I -B labs/expected-results/acceptance.py '/tmp/my catalog lab' in-stock
copilot -C '/tmp/my catalog lab' --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir
```

The last command is an optional **authorized interactive** session, not an offline check; it can expose shell/write tools and must remain in manual permissions. Inspect `/env`, `/permissions`, `/skills` and `/instructions`. The first-15-minute `--with-config` copy already includes exactly `.claude/skills/{repo-recon,reproduction-brief,verification-handoff}/SKILL.md` and the existing `CLAUDE.md` import closure. Inspect discovery before claiming these instructions loaded. Use the reproduction-brief skill for the defect/feature brief if discovered, or use the prompt below; do not manually duplicate skills or install a plugin. If you chose a bare copy, it has none of this configuration. Skill text is guidance, not permission enforcement.

Run `/plan` (or Shift+Tab to plan mode) and submit:

> In this copy, produce an implementation plan **without coding** for `in_stock=None|bool` in `list_products` and `handle_request`, and CLI `--in-stock true|false`. Filter before slicing; preserve totals and unfiltered output; reject `1`, `0`, strings and invalid CLI values. Identify affected callers, the two editable files, regression tests, exact independent acceptance commands, non-goals, rollback and stop conditions. No network, commits or dependencies.

Inspect the plan and edit it using Ctrl+Y where supported; compare the [twelve-field contract](../workflows/planning.md). Have another person or the read-oriented [repository reviewer agent](../../examples/agents/repository-reviewer.agent.md) challenge filter order and invalid inputs. The configured copy already has `.github/agents/repository-reviewer.agent.md`; review its `view,grep,glob` frontmatter/inheritance and inspect `/agent` and `/env` before use, without another copy step. Do not label self-review independent human review. `/review` can critique a diff, not certify acceptance. [source:cli-reference]

After approval, request **one part at a time**: first change the domain/API plus focused tests; inspect the diff; next add CLI parsing. Approve writes only to `src/catalog.py` and `tests/test_catalog.py`; approve no shell/network/remote action by default. If opting into `/autopilot` for this medium task, use the bounded objective and stop protocol in [autopilot](../workflows/autopilot.md); it does not inherit the reviewed plan as a security policy. `/tasks` shows any agent or shell work; don't start background jobs just to look busy. Exit and inspect **all** edits before running the new tests from the trusted root:

```sh
git diff --no-index labs/sample-app/src/catalog.py '/tmp/my catalog lab/src/catalog.py'
python3 -I -B labs/expected-results/acceptance.py '/tmp/my catalog lab' validation
python3 -I -B labs/expected-results/acceptance.py '/tmp/my catalog lab' in-stock
```

`git diff --no-index` normally exits 1 when differences exist. If new test files were edited, inspect them against the original too; after review run `python3 -B -m unittest discover -s '/tmp/my catalog lab/tests'` only on code you trust. Record observed exits and remaining questions. Use `/exit`, then `copilot -C '/tmp/my catalog lab' --resume=REVIEWED_SESSION_ID --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir` to resume; compare the written [handoff](../workflows/sessions-and-context.md) and current files first. The flag does not deny the approved cwd solely because the lab lives under `/tmp`; check path trust separately, not as a sandbox claim. No GitHub remote, `/delegate`, Hydra preview, push or commit is part of this hour. The offline route is the same plan and independent checks with a human editor instead of a model. Continue to [first real feature](first-real-feature.md).
