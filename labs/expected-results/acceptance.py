"""Independent oracle for HUMAN-REVIEWED Python, not a malicious-code sandbox.

Only child probes import lab code. The parent compares exact, typed observations
against trusted expectations. Arbitrary same-user code can still forge output
or access the host: an empty HOME and process timeout are not isolation.
"""
import json
from pathlib import Path
import sys
import tempfile

TRUSTED_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TRUSTED_ROOT))
from scripts.runner import environment, run
from scripts.safety import json_load, safe_path

PROBE = Path(__file__).with_name("probe.py")
TIMEOUT = 5
PRODUCTS = [
    {"sku": "A1", "name": "Amber mug", "price_cents": 1200, "in_stock": True},
    {"sku": "B2", "name": "Blue mug", "price_cents": 1500, "in_stock": False},
    {"sku": "C3", "name": "Canvas bag", "price_cents": 2200, "in_stock": True},
    {"sku": "D4", "name": "Desk pad", "price_cents": 3000, "in_stock": False}]


def page(items, total, offset=0, limit=20):
    return {"items": items, "total": total, "offset": offset, "limit": limit}


def equal_typed(actual, expected):
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(equal_typed(actual[k], v) for k, v in expected.items())
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(equal_typed(a, b) for a, b in zip(actual, expected))
    return actual == expected


def observed(argv, stdin=b""):
    # A new empty HOME and neutral cwd for every process, never credential HOME.
    with tempfile.TemporaryDirectory(prefix="acceptance-probe-") as home:
        result = run(argv, cwd=home, env=environment(home), stdin=stdin, timeout=TIMEOUT, limit=65536)
    return result


def check(root, exercise, *, observe=None):
    if exercise not in {"baseline", "validation", "in-stock", "refactor"}:
        raise ValueError("unknown exercise")
    root = safe_path(root)
    observe = observed if observe is None else observe
    cases, expected, labels = [], [], []

    def add(kind, params, value=None, rejected=False):
        cases.append({"kind": kind, "params": params})
        expected.append({"outcome": "ValueError"} if rejected else {"outcome": "returned", "value": value})
        boolean = type(params) is bool or (isinstance(params, dict) and any(type(v) is bool for v in params.values()))
        labels.append("validation fails: boolean value accepted or wrong rejection" if rejected and boolean else
                      "validation fails: invalid input not rejected" if rejected else
                      "returned page differs: check filtering, pagination, totals and types")

    for value in (True, False, "1", 1.5, -1):
        add("product", value, rejected=True)
    for field in ("limit", "offset"):
        for value in (True, False, "1", 1.5):
            add("request", {field: value}, rejected=True)
    for params in ({"limit": 0}, {"limit": 101}, {"offset": -1}, {"query": 1}, {"unknown": 1}):
        add("request", params, rejected=True)
    for kind in ("request", "domain"):
        add(kind, {}, page(PRODUCTS, 4))
        add(kind, {"query": "MUG", "offset": 1, "limit": 1}, page([PRODUCTS[1]], 2, 1, 1))
        add(kind, {"offset": 100}, page([], 4, 100))
    if exercise == "in-stock":
        for kind in ("request", "domain"):
            for value, items in ((True, [PRODUCTS[0], PRODUCTS[2]]), (False, [PRODUCTS[1], PRODUCTS[3]]), (None, PRODUCTS)):
                add(kind, {"in_stock": value}, page(items, len(items)))
            add(kind, {"in_stock": True, "offset": 1, "limit": 1}, page([PRODUCTS[2]], 2, 1, 1))
            add(kind, {"query": "MUG", "in_stock": False, "offset": 0, "limit": 1}, page([PRODUCTS[1]], 1, 0, 1))
            add(kind, {"query": "MUG", "in_stock": True, "offset": 1, "limit": 1}, page([], 1, 1, 1))
            for value in (0, 1, "true", [], {}):
                add(kind, {"in_stock": value}, rejected=True)
    result = observe([sys.executable, "-I", "-B", str(PROBE), str(root)], json.dumps(cases).encode())
    if result.status != "ok" or result.stderr:
        raise AssertionError("probe process failed")
    try:
        actual = json_load(result.stdout)
    except ValueError:
        raise AssertionError("probe observations missing or malformed") from None
    if not equal_typed(actual, {"observations": expected, "count": len(cases)}):
        if isinstance(actual, dict) and isinstance(actual.get("observations"), list):
            for observation, wanted, label in zip(actual["observations"], expected, labels):
                if not equal_typed(observation, wanted):
                    raise AssertionError("probe observation schema, types, count or values differ; " + label)
        raise AssertionError("probe observation schema, types, count or values differ")
    cli_cases = [([], page(PRODUCTS, 4)), (["--query", "MUG", "--offset", "1", "--limit", "1"], page([PRODUCTS[1]], 2, 1, 1))]
    if exercise == "in-stock":
        cli_cases += [(["--in-stock", value, "--limit", "1"], page([PRODUCTS[index]], 2, 0, 1)) for value, index in (("true", 0), ("false", 1))]
        cli_cases += [(["--query", "MUG", "--in-stock", "false", "--offset", "0", "--limit", "1"], page([PRODUCTS[1]], 1, 0, 1)),
                      (["--query", "MUG", "--in-stock", "true", "--offset", "1", "--limit", "1"], page([], 1, 1, 1))]
    for args, expected_page in cli_cases:
        result = observe([sys.executable, "-I", "-B", str(root / "src/catalog.py"), *args])
        try:
            valid = result.status == "ok" and not result.stderr and equal_typed(json_load(result.stdout), expected_page)
        except ValueError:
            valid = False
        if not valid:
            raise AssertionError("CLI output or process failed")
    invalid = [["--limit", "0"], ["--offset", "-1"]]
    if exercise == "in-stock":
        invalid.append(["--in-stock", "1"])
    for args in invalid:
        result = observe([sys.executable, "-I", "-B", str(root / "src/catalog.py"), *args])
        if result.status != "nonzero-exit" or result.returncode != 2 or result.stdout or not result.stderr:
            raise AssertionError("CLI invalid-input contract failed")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: acceptance.py LAB baseline|validation|in-stock|refactor")
    try:
        check(*sys.argv[1:])
    except (ValueError, OSError, AssertionError):
        raise SystemExit("acceptance failed; inspect reviewed code locally") from None
    print("acceptance passed")
