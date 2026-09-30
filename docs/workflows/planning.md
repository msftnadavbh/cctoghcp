# Planning: a reviewed contract before autonomy

Planning depth follows **uncertainty and risk**, not file count. A single validation guard whose callers are known may need only a short reproduction note. `in_stock` changes API, pagination, CLI and tests, so use `/plan`, `copilot --plan` or Shift+Tab in an authorized session; inspect the proposed `plan.md`, edit it via Ctrl+Y where supported and obtain human agreement before implementation. Plan mode can still discover/request tools; it is **not** an OS read-only sandbox. A checklist measures steps, not completed acceptance. [source:cli-reference]

## The twelve-field contract, filled in

| Field | `in_stock` reviewed example |
| --- | --- |
| 1. Outcome | Optional product stock filter through domain API, request and CLI, no persistence |
| 2. Baseline | Owned validation copy already repaired; `validation` passes, `in-stock` oracle initially fails |
| 3. Files/owner | One integrator edits `src/catalog.py`, `tests/test_catalog.py` only; no parallel writers |
| 4. I/O | `in_stock=None` leaves results unchanged; `True`/`False` selects exact bool; same `items,total,offset,limit` shape |
| 5. Callers | `list_products`, `handle_request`, `main` and existing test callers; trace current interfaces first |
| 6. Boundaries | Reject `0`, `1`, strings and unsupported CLI flags; empty filtered page and offset past end retain filtered total |
| 7. Order | Add filter validation and predicate before slice, update request allowed keys, then CLI parser and tests |
| 8. Acceptance | After reviewing the diff, use the `practice.py check` commands for `validation` and `in-stock` in [first hour](../start/first-hour.md); first passed before feature, second failed before and passes after |
| 9. Non-goals | No database, HTTP service, external dependency, deployment, GitHub remote, model experiment |
| 10. Permission/effects | Approve reviewed edits only to two copy paths; no agent shell/network; optional paid credits; no push |
| 11. Rollback | Compare copy against frozen baseline and recorded repair; reverse only owned feature changes after inspecting diff |
| 12. Review/stop | Stop on unexpected instruction/permission, ambiguous semantics, new file, failed negative case or oracle mismatch; independent human reviews code before execution |

**Prompt to `/plan`:** “In the catalog lab, inspect current `list_products`, `handle_request`, CLI and tests. Plan `None|bool`, filter before pagination, unchanged unfiltered behavior; show negative cases and the check commands in first hour. Do not edit, run code, fetch external data or install tools.” Review the output against the [exercise contract](../../labs/exercises.json). If it says “run tests until green” but omits *which inputs, files and reviewed execution boundary*, revise it.

Approve implementation separately, one seam at a time; inspect diff **before** trusted execution of newly generated code. A failed check returns to diagnosis, never to broad permission grants. `/autopilot` changes turn continuation after the plan, not the underlying permission contract. [First hour](../start/first-hour.md) and [scenario C](../scenarios/C-plan-review-autopilot.md).
