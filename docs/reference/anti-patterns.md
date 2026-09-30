# Fifteen anti-patterns and recoveries

| Anti-pattern | Consequence | Recovery |
| --- | --- | --- |
| “Implement everything” with no success criteria | Cannot tell when done | Define inputs, files, tests, stop gate |
| Autopilot before plan review | Unbounded work | Inspect plan before allowing edits |
| “Read-only” in prose with shell tool | Can mutate | Restrict visible tools and review OS access |
| `--allow-all` after narrow denial | Broad host/network access | Stop and diagnose exact denied invocation |
| Treat deny rules as sandbox | Shell/process can escape intent | Add independent isolation and CI gate |
| Two hooks for same event | Duplicate tests/actions | Choose native or shared registration |
| Hook as sole secret check | Timeout may fail open | Independent CI secret gate |
| Installing a plugin from schema pass | Lifecycle unverified | Keep artifact inert pending reviewed install test |
| Loading MCP server instructions blindly | Untrusted prompt authority | Review server and explicit allowlist |
| Pasting raw CI trace | Secret/injection risk | Lossy sanitized bridge and private original |
| Turning GitLab MR into GitHub PR | Wrong hosting action | Use the selected host's review workflow; GitHub cloud delegation requires a GitHub-hosted target |
| Claiming model experiment outcome in advance | False evidence | Record measured exits/time/credits only after run |
| Equating sample checks with Copilot runtime | Portability overclaim | Report offline and authenticated checks separately |
| Compact without handoff | Missing decisions | Write nine-field handoff first |
| Using `/rewind` as external rollback | Leaves remote/shell effects | Inspect effects, reverse only with approval |

The antidote is a [small verified feature](../start/first-real-feature.md), not more configuration. [source:hooks-reference]
