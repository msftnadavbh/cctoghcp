# Hooks: optional defense, never the only gate

Config validation binds each pre/post event to the entire exact native argv or
shared launcher command. Event/mode swaps and appended arguments/commands fail.
Native payloads do not reliably identify their event; `toolResult` is not used
to infer it. Correct registration remains essential.

Compare [native hooks](../../examples/hooks/native.json) with [shared settings](../../examples/hooks/shared-settings.json). They remain inert alternatives: register **one**, not both, only after approval. Both use `/usr/bin/python3 -I -B /ABSOLUTE/checkpoint/scripts/trusted_launcher.py hook pre|post --lab ABSOLUTE_LAB`. Review the interpreter and launcher outside the editable lab. The launcher imports only its own trusted root regardless of process cwd; payload cwd must equal LAB. Optional `--event-log PRIVATE_FILE`; JSON on stdin. Native `toolArgs` accepts object or JSON string; compatible `tool_input` requires matching event name. Mixed formats, missing fields and duplicate keys reject. This targeted demo pre-policy denies unknown tools and shell/patch tools, not a promise of full runtime usability. Neutral is `{}`, never unconditional allow. [source:hooks-reference]

Python edits under `src/`, including nested paths, receive bounded regular-file AST syntax and secret checks on the actual accepted path. Nothing is imported or executed. Post success is `static-check-passed`, not full validation. Handled failures (including malformed payloads and logging failure) exit 0 with `additionalContext`; review the diff before separately executing acceptance. Tests exercise the handler, not Copilot dispatch. **SOURCE REVIEW ONLY:** dispatcher command-hook timeouts can fail open, so independent reviewed CI remains authoritative. No hook is registered. [claim:hook-timeout] [Scenario T](../scenarios/T-hooks.md).
