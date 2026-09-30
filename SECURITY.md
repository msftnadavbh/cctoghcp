# Security boundaries

The optional teaching lab is not a production sandbox or a place for secrets. It needs no model, auth, remote or dependency installation. Python safety helpers are POSIX/Linux oriented and do not defend against a hostile same-user race or process escape. The ownership-ID cleanup checks recorded path/inode/device/owner/mount and refuses symlinks/special files; never share state or race cleanup with edits. [Artifact API](ARTIFACT-API.md).

An assistant may read untrusted repository content, shell output and CI logs. Keep credentials out of prompts, history, reports and repo; do not activate hooks/MCP/plugins during validation. Hook dispatcher timeouts can fail open; keep independent CI. Review MCP tool instructions, repository instructions and plugin contents before enabling them. `--allow-all` removes approval barriers for tools/paths/URLs but is no sandbox. Headless execution needs explicit paid consent, reviewed workspace/HOME, private output and human review. Raw GitLab CI logs must not be sent to an assistant; the bridge retains only allowlisted observations. Report vulnerabilities privately through a trusted channel rather than placing credentials in a public issue.

Optional headless forwards only explicitly selected `COPILOT_GITHUB_TOKEN` to
the child, with a fresh empty owned 0700 HOME. Other ambient credentials and
provider variables are excluded; interactive OAuth is unchanged. Never put a
token value in argv. Requested CLI secret redaction is not a guarantee: private
stdout/stderr may contain the token if the child prints it, and must not be
published automatically. No real credential or authentication probe is used by
tests. [Authentication source](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli).
