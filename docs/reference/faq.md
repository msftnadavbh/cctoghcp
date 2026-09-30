# FAQ

**Must I host on GitHub?** No. Local Copilot usage and GitLab source/CI are distinct from GitHub-only cloud delegation. [Hosting boundaries](../hosting/capability-boundaries.md).

**Must I delete `CLAUDE.md`?** No. Keep it in the first lab; verify actual instruction attachment in any later CLI session. [Coexistence](../migration/coexistence.md).

**Is planning a read-only sandbox?** No. Use permission/tool and OS controls independently. [Planning](../workflows/planning.md).

**Does `--allow-tool='write(src/catalog.py)'` stop shell writes?** No; shell permissions are independent, and relative write matching may cover trailing path components. [Permissions](../workflows/permissions.md).

**Does a passing validator prove Copilot runtime support?** No. It proves offline syntax, tests and fixture behavior; no login, paid run, dispatcher or MCP client was exercised. [Versions](versions.md).

**Is JSON output Claude JSON?** No, Copilot help specifies JSONL; adapter's conservative fake-tested event profile is not a guaranteed real schema. [Headless](../workflows/headless-and-ci.md).

**How do I clean the lab?** Use its ownership ID with `scripts.lab cleanup` and original private state. Never pass a deletion path or race edits. [First 15 minutes](../start/first-15-minutes.md).

**Can a reviewer approve without tests?** It can critique code but cannot establish deterministic acceptance. Use external oracle and human review. [Validation](../workflows/review-and-validation.md).
