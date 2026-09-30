# E — Broad permission only with independently verified isolation

## Goal and prerequisites

Observe why bypass is not a repair for a denied narrow grant. The CLI portion requires a **human-provisioned disposable VM/container** without host HOME, credentials, Docker socket, mounts or network egress. This repo supplies none of those conditions; otherwise **skip** the CLI portion.

## Start and deterministic check

```sh
python3 -B -m scripts.lab setup /tmp/scenario-e --state /tmp/checkpoint-state --exercise baseline
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-e baseline
```

**Optional authorized command only inside reviewed isolation:** `copilot -C /tmp/scenario-e --no-auto-update --no-remote-export --disable-builtin-mcps --allow-all`. **Prompt:** “Read `src/catalog.py`; report the baseline contract, do not change files.” No other scenario should inherit this grant.

## Checkpoints, effects and exit

**Checkpoint:** record actual mount/home/socket/egress isolation evidence, not merely a command flag. **Verification:** compare reviewed files before executing the baseline oracle again. **Permissions:** `--allow-all` combines tools, paths and URLs; no temp restriction is claimed here because broad access defeats that intent. Neither it nor an unverified container is a sandbox. **External effects:** may allow shell, network, paid calls and arbitrary paths; no live call was made for this repo. **Escape:** any isolation assumption fails → offline baseline only. **Claude analogy/difference:** Claude bypass and Copilot broad approval both need a real external boundary. [source:cli-reference] Help-observed v1.0.89, runtime untested.
