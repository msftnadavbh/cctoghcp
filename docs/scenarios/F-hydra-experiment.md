# F — Compare model modes only when eligible

HydraFusion is a research preview, not a synonym for Auto or fleet. First complete the [first-lesson lab](../start/first-15-minutes.md) offline. For an optional comparison use **two new, different lab paths** outside the book, each created with `practice.py setup PATH --exercise in-stock --with-config` using the PowerShell `python -I -B $Practice` or zsh `python3 -I -B "$Practice"` prefix from the lesson. Check each with `practice.py check PATH --exercise in-stock`: expect exit 1 before implementation. Never reuse or overwrite an existing path.

If `/model` exposes the preview and you have approved credits, use identical read/edit permissions and the same feature prompt on both copies: “Implement `in_stock=None|bool` in list, request and CLI; filter before pagination, preserve defaults, edit source/tests only and show the diff before running code.” Choose an available pinned model in one and Hydra in the other. Review **each** diff before separate checks; record actual exits, elapsed time and `/usage`. If preview isn't present, stop at the offline comparison setup. [Model guide](../workflows/models-and-hydrafusion.md).

## Goal and prerequisites

Two new labs, preview eligibility and explicit credit approval.

## Start and deterministic check

```sh
copilot --version
```

## Checkpoints, effects and exit

**Prompt:** identical feature request above. **Checkpoint:** record measured conditions. **Verification:** check each lab after diff review. **Permissions:** same scoped tools. **External effects:** model credits. **Escape:** skip if preview unavailable. **Claude analogy:** model comparison, not deterministic routing.
