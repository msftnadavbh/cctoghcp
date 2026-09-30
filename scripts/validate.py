"""Offline authoritative checks. Never invokes an assistant, hook or MCP CLI."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlsplit
import zipfile

from scripts.package_plugin import archive, contents
from scripts.safety import json_load, read_regular, safe_path
from scripts.secret_gate import gate

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".venv", "__pycache__", "build", ".private", "node_modules"}


def yaml_load(text):
    """JSON subset first; real YAML needs PyYAML, not a homemade parser."""
    try:
        return json_load(text)
    except ValueError:
        pass
    try:
        import yaml
    except ImportError:
        raise ValueError("PyYAML required; install requirements-validation.txt") from None

    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result:
                raise ValueError("invalid YAML mapping key")
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    try:
        # Reject aliases to avoid recursive/expanding structures at this boundary.
        if any(isinstance(token, yaml.tokens.AliasToken) for token in yaml.scan(text)):
            raise ValueError("YAML aliases unsupported in repository configuration")
        return yaml.load(text, Loader=UniqueLoader)
    except (yaml.YAMLError, TypeError, RecursionError, ValueError):
        raise ValueError("invalid YAML") from None


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError("unclosed frontmatter")
    data = yaml_load(parts[0][4:])
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be an object")
    return data, parts[1]


def anchors(text):
    result, counts = set(), {}
    _, text = frontmatter(text)
    text = re.sub(r"(?ms)^```.*?^```[^\n]*$", "", text)
    for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*\s*$", text):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        result.add(slug + (f"-{count}" if count else ""))
    result.update(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    return result


def markdown(path, root, source_ids=frozenset(), claim_ids=frozenset()):
    text = read_regular(path).decode()
    if not text.endswith("\n") or "\t" in text or any(line.rstrip() != line for line in text.splitlines()):
        raise ValueError("markdown formatting")
    meta, body = frontmatter(text)
    if path.name.endswith(".agent.md") or path.parent.name == "agents":
        if not {"name", "description", "tools"} <= meta.keys() or meta["tools"] != ["view", "grep", "glob"]:
            raise ValueError("agent contract")
        if path.name.endswith(".agent.md") and type(meta.get("include-custom-instructions")) is not bool:
            raise ValueError("agent inheritance must be explicit")
    if path.name == "SKILL.md" and (not isinstance(meta.get("name"), str) or not isinstance(meta.get("description"), str)):
        raise ValueError("skill frontmatter")
    fences = re.findall(r"(?m)^(`{3,}|~{3,})", body)
    if len(fences) % 2:
        raise ValueError("unclosed code fence")
    plain = re.sub(r"(?ms)^```.*?^```[^\n]*$|^~~~.*?^~~~[^\n]*$", "", body)
    references = {k.casefold(): v for k, v in re.findall(r"(?m)^\[([^\]]+)\]:\s*<?([^\s>]+)>?", plain)}
    targets = re.findall(r"\[[^\]]*\]\(([^)]+)\)", plain) + list(references.values())
    for label, ident in re.findall(r"\[([^\]]+)\]\[([^\]]*)\]", plain):
        key = (ident or label).casefold()
        if key not in references:
            raise ValueError("undefined markdown reference")
    targets += re.findall(r"(?m)^@([^\s]+)", plain)
    for target in targets:
        target = target.strip().strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme:
            if parsed.scheme not in {"https", "http", "mailto"}:
                raise ValueError("unreviewed link scheme")
            continue
        if parsed.netloc or parsed.path.startswith("/"):
            raise ValueError("absolute link refused")
        linked = safe_path(path.parent / unquote(parsed.path)) if parsed.path else path
        if not linked.is_relative_to(root) or not linked.exists():
            raise ValueError("missing or escaping markdown link")
        if parsed.fragment and linked.suffix == ".md":
            if unquote(parsed.fragment) not in anchors(read_regular(linked).decode()):
                raise ValueError("missing markdown anchor")
    for source_id in re.findall(r"\[source:([a-z0-9-]+)\]", body):
        if source_id not in source_ids:
            raise ValueError("unknown source id")
    for claim_id in re.findall(r"\[claim:([a-z0-9-]+)\]", body):
        if claim_id not in claim_ids:
            raise ValueError("unknown claim id")
    return meta


def schema_validate(value, schema):
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        raise ValueError("jsonschema required; install requirements-validation.txt") from None
    Draft202012Validator.check_schema(schema)
    if list(Draft202012Validator(schema).iter_errors(value)):
        raise ValueError("schema validation failed")


def hook_configs(configs):
    seen = set()
    for config in configs:
        if not isinstance(config, dict) or set(config) - {"version", "hooks"} or not isinstance(config.get("hooks"), dict):
            raise ValueError("invalid hook config")
        native = "version" in config
        if native and (type(config["version"]) is not int or config["version"] != 1):
            raise ValueError("invalid hook version")
        for event, entries in config["hooks"].items():
            if event not in {"preToolUse", "postToolUse", "PreToolUse", "PostToolUse"} or not isinstance(entries, list) or not entries:
                raise ValueError("invalid hook event")
            mode = "pre" if event.lower() == "pretooluse" else "post"
            expected_args = ["-I", "-B", "/REVIEW/checkpoint/scripts/trusted_launcher.py",
                             "hook", mode, "--lab", "/REVIEW/owned lab"]
            expected_command = ("/usr/bin/python3 -I -B '/REVIEW/checkpoint/scripts/trusted_launcher.py' "
                                f"hook {mode} --lab '/REVIEW/owned lab'")
            for entry in entries:
                if not isinstance(entry, dict):
                    raise ValueError("invalid hook entry")
                hooks = [entry] if native else entry.get("hooks")
                if not isinstance(hooks, list) or not hooks:
                    raise ValueError("invalid shared hooks")
                for hook in hooks:
                    if not isinstance(hook, dict) or hook.get("type") != "command":
                        raise ValueError("unreviewed hook type")
                    if native:
                        if (set(hook) != {"type", "exec", "args", "cwd", "timeoutSec"} or
                                hook["exec"] != "/usr/bin/python3" or hook["args"] != expected_args or
                                hook["cwd"] != "/REVIEW/checkpoint" or hook["timeoutSec"] != 15):
                            raise ValueError("native hook contract")
                    elif set(hook) != {"type", "command", "timeout"} or not isinstance(hook["command"], str) or hook["timeout"] != 15:
                        raise ValueError("shared hook contract")
                    elif hook["command"] != expected_command:
                        raise ValueError("shared trusted launcher contract")
                    identity = event.lower()
                    if identity in seen:
                        raise ValueError("duplicate registration; choose native OR shared")
                    seen.add(identity)


def files(root):
    result = []
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in dirs + names:
            if (Path(directory) / name).is_symlink():
                raise ValueError("repository symlink refused")
        dirs[:] = [d for d in dirs if d not in SKIP]
        result.extend(Path(directory) / n for n in names if not n.endswith(".pyc"))
    if len(result) > 2000:
        raise ValueError("repository file bound exceeded")
    return result


def static_checks(root=ROOT):
    root = safe_path(root)
    schema = json_load(read_regular(root / "schemas/evidence.schema.json"))
    from scripts.generate_reference import OUTPUTS, render, validate_rows
    rows = json_load(read_regular(root / "evidence/migration-matrix.json"))
    source_ids = {s["id"] for s in json_load(read_regular(root / "evidence/sources.json"))}
    validate_rows(rows, source_ids)
    for name in OUTPUTS:
        if read_regular(root / "docs/reference" / name).decode() != render(rows, name):
            raise ValueError("generated reference stale")
    scenarios = root / "docs/scenarios"
    names = tuple(f"{letter}-{suffix}.md" for letter, suffix in (
            ("A", "explore"), ("B", "plan"), ("C", "plan-review-autopilot"),
            ("D", "narrow-permission"), ("E", "disposable-broad"), ("F", "hydra-experiment"),
            ("G", "pin-model"), ("H", "fleet"), ("I", "reviewer"), ("J", "skills"),
            ("K", "existing-claude"), ("L", "mcp"), ("M", "debug"), ("N", "refactor"),
            ("O", "gitlab-mr"), ("P", "ci"), ("Q", "future-github"), ("R", "headless"),
            ("S", "resume"), ("T", "hooks")))
    if {p.name for p in scenarios.glob("[A-T]-*.md")} != set(names):
        raise ValueError("missing scenario")
    for name in names:
        scenario = read_regular(scenarios / name).decode()
        if any(f"## {heading}" not in scenario for heading in (
                "Goal and prerequisites", "Start and deterministic check", "Checkpoints, effects and exit")) or any(
                not re.search(r"\*\*(?:[^*]*\b)?" + term + r"\b", scenario, re.I) for term in (
                "prompt", "checkpoint", "verification", "permissions", "external effects", "escape", "Claude analogy")) or "```sh\n" not in scenario or "[source:" not in scenario:
            raise ValueError(f"scenario contract missing: {name}")
    data = {}
    required = {"sources": {"id", "url", "retrieved", "kind", "note"},
                "claims": {"id", "claim", "status", "source_ids", "preview", "limitations"},
                "commands": {"id", "argv", "tier", "status", "evidence"},
                "compatibility-cases": {"id", "fixture", "status", "source_ids", "expected"}}
    for name, keys in required.items():
        value = json_load(read_regular(root / f"evidence/{name}.json"))
        schema_validate(value, schema)
        if any(not keys <= item.keys() for item in value) or len({v["id"] for v in value}) != len(value):
            raise ValueError("evidence contract")
        data[name] = value
    sources = {s["id"] for s in data["sources"]}
    claims = {c["id"] for c in data["claims"]}
    for name in ("claims", "compatibility-cases"):
        if any(set(item["source_ids"]) - sources for item in data[name]):
            raise ValueError("unknown evidence source")
    for case in data["compatibility-cases"]:
        target = safe_path(root / case["fixture"])
        if not target.is_relative_to(root) or not target.is_file():
            raise ValueError("missing compatibility fixture")
    for command in data["commands"]:
        if command["evidence"] is not None:
            target = safe_path(root / command["evidence"])
            if not target.is_relative_to(root) or not target.is_file():
                raise ValueError("missing command evidence")
    for claim in data["claims"]:
        if claim["status"] == "untested" and not claim["limitations"]:
            raise ValueError("untested claim needs limitation")
    exceptions = json_load(read_regular(root / "evidence/validation-exceptions.json"))
    for path in files(root):
        relative = path.relative_to(root).as_posix()
        raw = read_regular(path, 1024 * 1024)
        if relative.startswith(("labs/sample-app/", "labs/fixtures/", "examples/")) and not gate([path]):
            raise ValueError("independent secret gate rejected distributable fixture")
        if path.suffix == ".json":
            json_load(raw, 1024 * 1024)
        if path.suffix in {".yaml", ".yml"}:
            if not isinstance(yaml_load(raw.decode()), dict):
                raise ValueError("configuration must be an object")
        if path.suffix == ".md":
            markdown(path, root, sources, claims)
            text = raw.decode()
            if re.search(r"\b(?:TODO|TBD|FIXME)\b", text) and relative not in exceptions["placeholder_paths"]:
                raise ValueError("unreviewed documentation placeholder")
            for claim in data["claims"]:
                if claim["preview"] and f'[claim:{claim["id"]}]' in text and "preview" not in text.lower():
                    raise ValueError("missing preview label")
        if relative.startswith("examples/") and b"/REVIEW/" in raw and relative not in exceptions["placeholder_paths"]:
            raise ValueError("unreviewed activation placeholder")
    for forbidden in (".github/hooks", ".mcp.json", ".claude/settings.json", ".claude/settings.local.json", ".github/copilot/settings.json"):
        if (root / forbidden).exists():
            raise ValueError("unexpected root activation")
    for name in ("native", "shared-settings"):
        hook_configs([json_load(read_regular(root / f"examples/hooks/{name}.json"))])
    for path in (root / "examples/mcp").glob("*.json"):
        value = json_load(read_regular(path))
        if path.name == "local.json":
            local = value.get("mcpServers", {}).get("checkpoint-synthetic", {})
            if local.get("command") != "/usr/bin/python3" or local.get("args") != ["-I", "-B", "/REVIEW/checkpoint/scripts/trusted_launcher.py", "mcp"]:
                raise ValueError("MCP trusted launcher contract")
        if set(value) != {"mcpServers"} or not isinstance(value["mcpServers"], dict):
            raise ValueError("MCP config envelope")
        for server in value["mcpServers"].values():
            if not isinstance(server, dict) or server.get("type") not in {"local", "http"} or not isinstance(server.get("tools"), list):
                raise ValueError("MCP config shape")
            if "env" in server or "headers" in server:
                raise ValueError("inert MCP examples must not contain credentials")
            if server["type"] == "local" and (set(server) != {"type", "command", "args", "tools"} or
                    not isinstance(server["command"], str) or not isinstance(server["args"], list) or
                    not all(isinstance(arg, str) for arg in server["args"])):
                raise ValueError("local MCP shape")
            if server["type"] == "http" and (set(server) != {"type", "url", "tools"} or
                    not isinstance(server["url"], str) or not server["url"].startswith("https://")):
                raise ValueError("HTTP MCP shape")
    schema_validate(json_load(read_regular(root / "examples/plugin/plugin.json")),
                    json_load(read_regular(root / "schemas/plugin.schema.json")))
    generated = archive(root)
    if generated != archive(root):
        raise ValueError("nondeterministic plugin")
    with zipfile.ZipFile(io.BytesIO(generated)) as bundle:
        if {name: bundle.read(name) for name in bundle.namelist()} != contents(root):
            raise ValueError("generated consistency")
    capture = root / "results/help/capture.json"
    if capture.exists():
        for command in json_load(read_regular(capture))["commands"]:
            raw = read_regular(capture.parent / (command["id"] + ".txt"), 1024 * 1024)
            if hashlib.sha256(raw).hexdigest() != command["sha256"]:
                raise ValueError("help evidence changed")
    return len(files(root))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    try:
        count = static_checks()
    except (ValueError, OSError, KeyError, TypeError, UnicodeError):
        print("offline static validation failed; run focused tests for details", file=sys.stderr)
        return 1
    if not args.static_only:
        suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
        outcome = unittest.TextTestRunner(verbosity=2).run(suite)
        if outcome.testsRun == 0 or not outcome.wasSuccessful():
            return 1
        result = subprocess.run([sys.executable, "-B", str(ROOT / "labs/sample-app/scripts/check_lab.py")],
                                cwd=ROOT, env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"})
        if result.returncode:
            return 1
        result = subprocess.run([sys.executable, "-B", str(ROOT / "labs/expected-results/acceptance.py"),
                                 str(ROOT / "labs/sample-app"), "baseline"], cwd=ROOT,
                                env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"})
        if result.returncode:
            return 1
    print(f"offline validation passed ({count} files); no assistant/auth/network integration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
