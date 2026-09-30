"""Read-only GitLab bridge: dry-run by default; publishing never implemented."""
import argparse
import json
from pathlib import Path
import re
import tempfile
import os
from urllib.parse import quote

from scripts.runner import environment, run
from scripts.preflight import disjoint, executable_path
from scripts.safety import private_write, sanitized_ci, safe_path


def plan(project, pipeline, job, hostname):
    if (not isinstance(hostname, str) or len(hostname) > 253 or
            not all(re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", part) for part in hostname.split("."))):
        raise ValueError("explicit bare hostname required")
    if (not re.fullmatch(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+", project) or
            any(part in {".", ".."} or part.startswith("-") for part in project.split("/")) or
            type(pipeline) is not int or pipeline <= 0 or type(job) is not int or job <= 0):
        raise ValueError("explicit project and positive IDs required")
    prefix = "projects/" + quote(project, safe="")
    return {"pipeline": ["api", f"{prefix}/pipelines/{pipeline}", "--hostname", hostname, "--method", "GET"],
            "job": ["api", f"{prefix}/jobs/{job}", "--hostname", hostname, "--method", "GET"],
            "trace": ["api", f"{prefix}/jobs/{job}/trace", "--hostname", hostname, "--method", "GET"],
            "human_only_publish_argv": ["glab", "mr", "create", "--repo", "https://" + hostname + "/" + project,
                                        "--draft", "--title", "Review catalog fix",
                                        "--description-file", "REVIEWED_REPORT.md"],
            "publishing": "outside helper; human must review branches and report"}


def fetch(executable, project, pipeline, job, home, hostname):
    from scripts.safety import json_load
    commands = plan(project, pipeline, job, hostname)
    executable = executable_path(str(executable))
    for kind in ("pipeline", "job", "trace"):
        with tempfile.TemporaryDirectory(prefix="gitlab-read-") as neutral:
            result = run([executable, *commands[kind]], cwd=neutral, env=environment(home), timeout=20)
        if result.status != "ok":
            raise ValueError("GitLab read failed")
        if kind != "trace":
            value = json_load(result.stdout)
            if not isinstance(value, dict) or type(value.get("id")) is not int or value["id"] != (pipeline if kind == "pipeline" else job):
                raise ValueError("resource mismatch")
            if kind == "job":
                parent = value.get("pipeline")
                if not isinstance(parent, dict) or type(parent.get("id")) is not int or parent["id"] != pipeline:
                    raise ValueError("job pipeline mismatch")
    return sanitized_ci(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--hostname", required=True)
    parser.add_argument("--pipeline", required=True, type=int)
    parser.add_argument("--job", required=True, type=int)
    parser.add_argument("--execute-read", action="store_true")
    parser.add_argument("--executable", default="glab")
    parser.add_argument("--home", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = plan(args.project, args.pipeline, args.job, args.hostname)
        if args.execute_read:
            if not args.home or not args.output:
                raise ValueError("HOME and output required")
            output = safe_path(args.output)
            home, workspace = safe_path(args.home), safe_path(Path.cwd())
            if not all(disjoint(a, b) for a, b in ((home, workspace), (output, workspace), (output, home))):
                raise ValueError("credential HOME and output must be separate from workspace")
            if output.exists() or not output.parent.is_dir():
                raise ValueError("new output required before network read")
            fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, "wb") as stream:
                stream.write(fetch(args.executable, args.project, args.pipeline,
                                   args.job, home, args.hostname))
            print("sanitized GitLab read saved; no writes performed")
        else:
            print(json.dumps({"status": "dry-run", **result}, sort_keys=True))
    except (ValueError, OSError, TypeError, AttributeError):
        parser.exit(2, "GitLab operation refused; inspect locally\n")


if __name__ == "__main__":
    main()
