# J — Package existing skills without installing

## Goal and prerequisites

Test canonical `.claude/skills` reuse and deterministic plugin packaging. Python 3 and optional validator libraries; no hosting or plugin lifecycle.

## Start and deterministic check

```sh
python3 -B -m scripts.package_plugin /tmp/scenario-j-skills.zip
python3 -B -m scripts.validate --static-only
```

Use a **new** archive path (exclusive create); inspect [manifest](../../examples/plugin/plugin.json) and [canonical skills](../../.claude/skills). **Optional prompt in a separately authorized read-only CLI:** “Which existing skill fits reviewing `src/catalog.py`? Summarize minimum task boundary; do not invoke or install.”

## Checkpoints, effects and exit

**Checkpoint:** ZIP has root manifest and three mechanically copied skills; schema check is local. **Verification:** static check and deterministic package tests pass; no CLI discovery/lifecycle inference. **Permissions:** offline packaging only; optional paid read call separately authorized. **External effects:** one local archive, no activation. **Escape:** 1.0.89 install help omits documented local paths—keep ZIP inert; future human can review unpacked directory and documented local-install candidate separately. **Claude analogy/difference:** project skills remain canonical without duplicating live instruction trees. [source:plugin-reference] [claim:plugin-portability] Version 1.0.89, runtime untested.
