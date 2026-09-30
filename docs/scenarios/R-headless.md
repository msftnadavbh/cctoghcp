# R — Headless is not the first interactive lesson

Complete [first 15 minutes](../start/first-15-minutes.md) interactively before automation. In a read-only session ask: “Which approvals and observations would a headless version of the validation exercise need? Don't launch one.” **Expected:** workspace, reviewed inputs, narrowly granted tools, artifact handling and a separate post-diff check—not an assumption that a noninteractive success exit means tests passed.

The bundled [headless helper](../workflows/headless-and-ci.md) is advanced POSIX automation with dry-run and separately approved paid modes. Its CLI stdin/JSONL behavior has not been confirmed with an authenticated Copilot run. Do not copy POSIX commands into PowerShell or use a dry-run as permission to send prompts. For Windows/macOS practice keep the native `practice.py` check and manual diff review.

## Goal and prerequisites

Finish the interactive native lesson first.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** ask for preconditions above. **Checkpoint:** no automation run. **Verification:** manual diff and check. **Permissions:** no headless grant. **External effects:** optional credits only. **Escape:** stop on unverified event schema. **Claude analogy:** output formats differ. [source:programmatic-reference]
