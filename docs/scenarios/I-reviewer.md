# I — Reviewer cannot bless its own patch

## Goal and prerequisites

Critique a human-reviewed fix in the owned [scenario A](A-explore.md) copy (or refactor in scenario N). The scenario copy is bare: the example reviewer agent is **not preinstalled**. No GitLab publication.

## Start and deterministic check

```sh
python3 -I -B labs/expected-results/acceptance.py /tmp/scenario-a validation
python3 -B -m scripts.validate --static-only
```

If copy A remains broken, preserve the failing status. **Optional authorized start:** `copilot -C /tmp/scenario-a --no-auto-update --no-remote-export --disable-builtin-mcps --disallow-temp-dir --available-tools=view,grep,glob`. **Prompt inspired by [inert reviewer definition](../../examples/agents/repository-reviewer.agent.md):** “Inspect the shared guard for caller coverage, negative inputs, data exposure and missing tests; cite file/line, no edit/shell/approval.” If testing the custom agent itself, review/copy **one** agent into a recognized location and confirm `/agent`; `/review` is another *local* critique.

## Checkpoints, effects and exit

**Checkpoint:** distinguish observations, hypotheses, actual oracle exit and human disposition. **Verification:** a reviewer statement doesn't make a failed oracle pass; independently inspect diff then rerun check. **Permissions:** CLI `view,grep,glob` only, no agent shell; temp flag doesn't confine approved cwd. **External effects:** optional credits, no publish. **Escape:** unexpected edit or executable access → stop and return to integrator. **Claude analogy/difference:** a review agent is useful critique, not independent human or test authority. [source:cli-reference] Source/help reviewed 1.0.89, runtime untested.
