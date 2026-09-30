# P — Diagnose CI without sending raw trace

## Goal and prerequisites

Observe only sanitized success/failure and verify job-to-pipeline identity. Python 3 for offline fixture; real `glab`, exact host/project/IDs and approved separate credential HOME needed for optional GET.

## Start and deterministic check

```sh
python3 -B -m scripts.secret_gate labs/fixtures/ci-sanitized.log
python3 -B -m scripts.gitlab --hostname gitlab.example.com --project group/project --pipeline 12345 --job 67890
```

Illustrative IDs are **not** fetched. **Optional authorized prompt:** “Given only the sanitized CI observation, distinguish failure from root-cause hypothesis and propose a local repro. No retry, no variables.” A separately approved `--execute-read --home REVIEWED_HOME --output NEW_FILE` performs explicit-host GET in neutral cwd after human checks that real job belongs to real pipeline. Raw trace stays private.

## Checkpoints, effects and exit

**Checkpoint:** gate exit 0, verified host/project/job relation and local repro proposal. **Verification:** fake glab tests cover sanitization; real network result remains **not-run**. **Permissions:** only GET; no variable retrieval, CI retry or assistant with protected credentials. **External effects:** dry run none; approved read contacts GitLab and stores private lossy JSON. **Escape:** if diagnosis requires raw secrets, stop and ask a human privately. **Claude analogy/difference:** CI triage transfers but lossily sanitized evidence is not full trace. [source:gitlab-api-host] No authenticated GitLab test.
