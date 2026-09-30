# Q — Future GitHub-only capability decision

## Goal and prerequisites

Decide whether remote delegation applies without altering current GitLab source. Cloud operations require a separately approved GitHub target, entitlement and capable gh version; none are available in this local lab.

## Start and deterministic check

```sh
python3 -B -m scripts.validate --static-only
python3 -B labs/sample-app/scripts/check_lab.py
```

**Optional authorized prompt:** “Compare local `/review` and GitHub `/delegate` for the reviewed change; create no task/branch/PR.” The [gh manual](https://cli.github.com/manual/gh_agent-task) documents preview `gh agent-task create/list/view`; observed gh 2.45.0 is below the >=2.80 minimum in lead research. `.github/workflows/copilot-setup-steps.yml` with `copilot-setup-steps` job prepares a **GitHub** cloud environment only when on its default branch; no workflow or issue schedule is installed here. This is a discussion, not authorization to activate. [source:github-copilot-setup-steps]

## Checkpoints, effects and exit

**Checkpoint:** record target host, policy, versions and human approval *before* any `/delegate`. **Verification:** two offline commands pass but do not prove cloud task availability. **Permissions:** no GitHub remote write by default; PR approval is separate from local code review. **External effects:** none in lab; optional `/delegate` may checkpoint branch/open draft PR. **Escape:** GitLab remains source → follow [scenario O](O-gitlab-mr.md) instead. **Claude analogy/difference:** cloud delegation and remote-control service do not migrate GitLab source. [source:github-agent-tasks] Public preview unavailable in observed gh.
