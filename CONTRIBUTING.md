# Contributing without activating integrations

1. Read [artifact API](ARTIFACT-API.md) and inspect affected code and tests first.
2. Record source/provenance and observation tier in [evidence](evidence/claims.json) before a new capability claim.
3. Keep the sample lab stdlib-only and the repository root free of active hooks, MCP and plugins.
4. For scenarios, provide an executable offline prep and deterministic check, permission boundary, effect and stop path; don't invent outcomes.
5. For migration mappings, edit [matrix](evidence/migration-matrix.json) then run `python3 -B -m scripts.generate_reference` and `--check`; never hand-edit generated tables.
6. Run `python3 -B labs/sample-app/scripts/check_lab.py` for standalone lab and `python3 -B -m scripts.validate` for full offline checks (pinned optional validators required).
7. Review diff, links, instructions and secret exposure before activation or release.
8. Do not commit, authenticate, publish, install plugins or invoke a model without explicit human approval. Report test results and unresolved risk separately.

## Changes to product claims

For behavior changes, link a primary source, record the relevant version,
update the example and regression check, and preserve preview labels and
GitLab/GitHub hosting boundaries. Rebuild generated summaries from the matrix.
An offline parser or test does not establish authenticated CLI behavior.

For full validation on a fresh machine, install `requirements-validation.txt` in
your own virtual environment first; this optional maintainer bootstrap contacts a
package registry. It is not required by the stdlib lab. Default CI never invokes
a model.
