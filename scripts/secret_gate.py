"""Independent offline gate. Heuristic, not complete secret detection."""
import argparse
from pathlib import Path

from scripts.safety import has_secret, read_regular


def gate(paths):
    for path in paths:
        if has_secret(read_regular(path)):
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        ok = gate(args.paths)
    except (OSError, ValueError):
        ok = False
    print("secret gate passed" if ok else "secret gate rejected input; inspect locally")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
