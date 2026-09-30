# E — Why broad permissions are not a fix

`--allow-all` combines tool, path and URL approvals. The native lab **does not isolate Copilot from your host**, so do not try this flag there. Instead run the [first-lesson read-only command](../start/first-15-minutes.md) and inspect `/permissions`; ask why an edit requires separate approval. **Expected:** the initial validation check still fails, and no file changes. The next action is the lesson's reviewed edit grant, not broad access.

If you independently provision a disposable, isolated environment, review credential, home, mount, socket and egress exposure before considering broad grants there. The book does not provide that isolation. [Permission boundaries](../workflows/permissions.md).

## Goal and prerequisites

Use a read-only lab; broad mode requires external isolation not provided here.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** ask why broad access is unnecessary. **Checkpoint:** no edits. **Verification:** initial check still fails. **Permissions:** read only in lab. **External effects:** optional credits. **Escape:** skip broad mode without isolation. **Claude analogy:** bypass needs a real external boundary. [source:cli-reference]
