# Fleet and subagents: parallel investigation, one editor

For a small shared guard, skip fleet and fix it once. Use `/fleet` only when several **independent read tasks** will save time; parallel agents can consume credits and do not settle conflicting product semantics for you. The [first-hour stock filter](../start/first-hour.md) is a concrete split after `in-stock` initially fails:

1. Read worker A: trace `integer()` and callers; report path:line, observation and missing negative test.
2. Read worker B: inspect `list_products` and `PRODUCTS`; report a filter-before-pagination example and what `total` should count.
3. Read worker C: inspect `handle_request`, CLI and tests; report accepted/rejected inputs and missing regression.

Ask each for assumptions, citations, consequence, proposed check and uncertainty. Start the CLI with `view,grep,glob` available (see [first hour](../start/first-hour.md)); verify worker tool grants rather than assuming the word “read” enforces them. In the interactive CLI, `/fleet` toggles the mode and `/tasks` shows work. If workers disagree about whether `1` means `True`, stop and settle the shared `None|bool` contract. One integrator then owns the edits to `src/catalog.py` and `tests/test_catalog.py`; review the combined diff and run the checks yourself.

For a focused reviewer, inspect the copied `.github/agents/repository-reviewer.agent.md` and `/agent`. Selecting an agent as the main agent and spawning it as a subagent can attach instructions differently; `include-custom-instructions: true` is required in a custom subagent when repository instructions must be inherited. Check the active environment and the definition's tool list. `/review` offers critique, not independent acceptance or a human sign-off.

Inspect `/tasks` before leaving: `a` expands nested agents, `f` shows finished tasks and `X` stops an active task. Interrupting is not rollback. Built-in roles and picker options can differ by installed version; [agent definitions](../customization/agents.md) and [permissions](permissions.md) explain how to check the actual boundary.
