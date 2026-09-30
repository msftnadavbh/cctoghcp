# R — Four-mode headless dry-run

## Goal and prerequisites

Inspect wrapper argv and prompt transport **without invoking Copilot**. Python 3, repository root; dry-run needs no auth. A separately approved paid integration has much stricter preflight, not supplied here.

## Start and deterministic check

```sh
python3 -B -m scripts.headless repo-summary --repo labs/sample-app --prompt-file examples/headless/repo-summary.txt
python3 -B -m scripts.headless diff-review --repo labs/sample-app --prompt-file examples/headless/diff-review.txt
python3 -B -m scripts.headless test-fix --repo labs/sample-app --prompt-file examples/headless/test-fix.txt
python3 -B -m scripts.headless gitlab-log-summary --repo labs/sample-app --prompt-file examples/headless/gitlab-log-summary.json
```

**Optional authorized prompt:** four prompt files respectively request a source overview, actual diff critique, bounded validation fix and sanitized GitLab log summary; review each file, do **not** treat a dry-run as paid consent. Paid mode requires a **bare owned copy**, fresh empty owned 0700 HOME disjoint from copy/output, selected privately provisioned `COPILOT_GITHUB_TOKEN` and all `--execute --consent-paid --reviewed-workspace --credential-env COPILOT_GITHUB_TOKEN --home FRESH_EMPTY_HOME --output NEW_PRIVATE_DIRECTORY` flags. Root/sample paths are dry-run only. [source:copilot-authentication]

## Checkpoints, effects and exit

**Checkpoint:** each dry-run returns JSON status and exit 0, no model. **Verification:** paid `test-fix` can return only static-only `validation-pending` (exit 17); reports `report-unverified` (18), JSONL framing error 15. Human reviews diff before separate oracle; no invented result event. **Permissions:** known config/policy preflight, only selected token forwarded, requested CLI secret redaction may still leave sensitive private child captures; no implicit temp grant, not a sandbox. **External effects:** dry-run none; paid runs can edit and consume credits. **Escape:** mismatched stdin/JSONL or token risk → stop, keep captures private, never broaden. **Claude analogy/difference:** Claude JSON/stream-json is not verified Copilot stdin/JSONL. [source:programmatic-reference] Fake tests only, no real CLI integration.
