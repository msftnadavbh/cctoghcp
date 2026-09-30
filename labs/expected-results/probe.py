"""Child observer only. Expectations and verdict remain in trusted parent."""
import importlib.util
import json
from pathlib import Path
import sys


def main():
    cases = json.loads(sys.stdin.buffer.read(65537))
    spec = importlib.util.spec_from_file_location("observed_catalog", Path(sys.argv[1]) / "src/catalog.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    observations = []
    for case in cases:
        try:
            if case["kind"] == "product":
                value = module.Product("S1", "Synthetic", case["params"], True)
                value = vars(value)
            elif case["kind"] == "domain":
                value = module.list_products(**case["params"])
            else:
                value = module.handle_request(case["params"])
            observations.append({"outcome": "returned", "value": value})
        except ValueError:
            observations.append({"outcome": "ValueError"})
        except Exception:
            observations.append({"outcome": "unexpected-error"})
    print(json.dumps({"observations": observations, "count": len(observations)}, allow_nan=False))


if __name__ == "__main__":
    main()
