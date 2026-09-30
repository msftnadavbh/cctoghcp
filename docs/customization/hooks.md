# Hooks: optional defense, never the only gate

**The bundled handlers require a POSIX environment.** They are optional; use [your normal project workflow](../start/use-copilot-in-your-repository.md) without them on Windows. Review each hook's command and payload before registering it.

Match `preToolUse` to the handler's `pre` mode and `postToolUse` to `post`.
Copying a command under the wrong event changes its effect. Register either
the native format or the compatible format, not both.

Compare [native hooks](../../examples/hooks/native.json) with [shared settings](../../examples/hooks/shared-settings.json). They remain inert alternatives: register **one**, not both, only after approval. Both use `/usr/bin/python3 -I -B /ABSOLUTE/checkpoint/scripts/trusted_launcher.py hook pre|post --lab ABSOLUTE_LAB`. Review the interpreter and launcher outside the editable lab. The launcher imports only its own trusted root regardless of process cwd; payload cwd must equal LAB. Optional `--event-log PRIVATE_FILE`; JSON on stdin. Native `toolArgs` accepts object or JSON string; compatible `tool_input` requires matching event name. Mixed formats, missing fields and duplicate keys reject. This targeted demo pre-policy denies unknown tools and shell/patch tools; it is not a full runtime policy. Neutral is `{}`, never unconditional allow.

Python edits under `src/`, including nested paths, receive bounded regular-file AST syntax and secret checks on the actual accepted path. Nothing is imported or executed. Post success is `static-check-passed`, not full validation. Handled failures (including malformed payloads and logging failure) exit 0 with `additionalContext`; review the diff before separately executing acceptance. [Copilot command hook timeouts can fail open](https://docs.github.com/en/copilot/reference/hooks-reference), so keep independent CI. No hook is registered. [Hook exercise](../scenarios/T-hooks.md).
