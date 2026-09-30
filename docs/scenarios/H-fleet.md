# H — Fleet of independent read-only investigators

## Goal and prerequisites

Compare three independent findings without overlapping edits. Fresh `in-stock` copy, optional authorized CLI fleet; no Git host.

## Start and deterministic check

```sh
python3 -B -m scripts.lab setup /tmp/scenario-h --state /tmp/checkpoint-state --exercise in-stock
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-h in-stock
```

The initial feature failure is expected. **Optional prompt via `/fleet` or `--fleet`:** “Assume `None|bool`, filter before slicing, preserve totals. Three **read-only** reports: A `integer()` callers; B filter/pagination order; C request/CLI plus missing tests. Each gives assumption, file:line evidence, observed vs hypothesis, consequence, proposed check and uncertainty. One integrator owns all later edits; no worker shell.” [Fleet contract](../../labs/exercises.json).

## Checkpoints, effects and exit

**Checkpoint:** A/B/C independent reads → integrator reconciles → one editor → human diff → separate oracle. `/tasks`: `a` nested levels, `f` finished, `X` kill, `B` background sync. **Verification:** before integration, no changed files and feature oracle still fails; afterward run oracle only on reviewed edit. **Permissions:** verify actual tool binding `view,grep,glob`, not prose; shell tasks and agent tasks differ. **External effects:** optional parallel credits. **Escape:** uncertain shared contract or two editors → stop fleet and serialize. **Claude analogy/difference:** Claude teams and Copilot fleet share delegation intent, not automatic consensus or a known picker. [source:cli-reference] 1.0.89 help, no fleet execution.
