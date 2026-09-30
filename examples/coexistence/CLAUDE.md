# Catalog repository guidance

@guidance/shared.md

For the catalog exercise, inspect `src/catalog.py` and its callers before edits.
Keep changes bounded to the requested domain/API/CLI behavior and tests. Preserve
stdlib-only offline operation; no dependencies, network, commits or publishing.
After changes, hand the diff to a human before executing any generated Python.
Use the external acceptance oracle only after that review; never call a static
syntax check a passing behavioral test. Instructions are guidance, not a sandbox.
