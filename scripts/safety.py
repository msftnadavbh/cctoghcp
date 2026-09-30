"""Small shared trust-boundary helpers. Error messages never include input."""
import ast
import json
import os
from pathlib import Path
import re
import stat

LIMIT = 256 * 1024


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def json_load(raw, limit=LIMIT):
    if len(raw) > limit:
        raise ValueError("input too large")
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError, RecursionError):
        raise ValueError("invalid JSON") from None


def safe_path(path):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError("symlink refused")
    return Path(os.path.abspath(path))


def read_regular(path, limit=LIMIT):
    path = safe_path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError("not a bounded regular file")
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("input too large")
    return data


def private_write(path, data):
    """Create only, never clobber or follow a preexisting output."""
    path = safe_path(path)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)


SECRET = re.compile(
    rb"(?:gh[pousr]_[A-Za-z0-9]{12,}|github_pat_[A-Za-z0-9_]{12,}|"
    rb"glpat-[A-Za-z0-9_-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    rb"(?i:authorization\s*[:=]|(?:token|password|secret|api[_-]?key)\s*[:=])\s*\S+)")


def has_secret(data):
    return bool(SECRET.search(data))


def static_python(path):
    """Bounded syntax/secret inspection only: never import or execute input."""
    data = read_regular(path)
    if has_secret(data):
        raise ValueError("static secret check failed")
    try:
        ast.parse(data, filename="reviewed-source", mode="exec")
    except (SyntaxError, ValueError, UnicodeError, RecursionError):
        raise ValueError("static syntax check failed") from None


def sanitized_ci(raw):
    """Lossy allowlist, not a promise to redact arbitrary logs correctly.

    No raw lines, paths, URLs, variable names, or exception messages survive.
    """
    if len(raw) > LIMIT:
        raise ValueError("input too large")
    text = raw.decode("utf-8", errors="replace")
    return json.dumps({"kind": "sanitized-ci", "synthetic": False,
                       "failure_observed": bool(re.search(r"(?m)^(?:FAIL:|FAILED\b|ERROR:)", text)),
                       "success_observed": bool(re.search(r"(?m)^OK$", text)),
                       "detail": "Raw log omitted; inspect locally before proposing a fix."},
                      sort_keys=True).encode()
