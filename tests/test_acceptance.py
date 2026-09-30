import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.lab import ROOT, setup
from scripts.runner import Result

spec = importlib.util.spec_from_file_location("trusted_acceptance", ROOT / "labs/expected-results/acceptance.py")
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


class AcceptanceTests(unittest.TestCase):
    def test_baseline_refactor_and_feature_api_cli(self):
        oracle.check(ROOT / "labs/sample-app", "baseline")
        oracle.check(ROOT / "labs/sample-app", "refactor")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            setup(root / "lab", root / "state")
            path = root / "lab/src/catalog.py"
            text = path.read_text().replace('query="", offset=0, limit=20):', 'query="", offset=0, limit=20, in_stock=None):')
            text = text.replace('    matches = [p for p in products',
                '    if in_stock is not None and type(in_stock) is not bool:\n        raise ValueError("invalid stock")\n'
                '    products = [p for p in products if in_stock is None or p.in_stock is in_stock]\n    matches = [p for p in products')
            text = text.replace('{"query", "offset", "limit"}', '{"query", "offset", "limit", "in_stock"}')
            text = text.replace('    args = parser.parse_args(argv)',
                '    parser.add_argument("--in-stock", choices=["true", "false"])\n    args = parser.parse_args(argv)\n'
                '    args.in_stock = None if args.in_stock is None else args.in_stock == "true"')
            path.write_text(text)
            oracle.check(root / "lab", "in-stock")
            path.write_text(text.replace('"total": len(matches)', '"total": True'))
            with self.assertRaisesRegex(AssertionError, "schema, types, count or values"):
                oracle.check(root / "lab", "in-stock")

    def test_typed_comparison_rejects_bool_int_and_extra_keys(self):
        for actual, expected in ((True, 1), (0, False), ({"count": True}, {"count": 1}),
                                 ({"x": 1, "extra": 2}, {"x": 1}), ([1], [1, 2])):
            self.assertFalse(oracle.equal_typed(actual, expected))

    def test_exit_zero_hang_and_truncated_output_do_not_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            setup(root / "lab", root / "state")
            catalog = root / "lab/src/catalog.py"
            for source in ("import os; os._exit(0)", "import time; time.sleep(20)",
                           "print('{'); raise SystemExit(0)", "print('x'*100000); raise SystemExit(0)"):
                catalog.write_text(source)
                with patch.object(oracle, "TIMEOUT", 0.2), self.assertRaises(AssertionError):
                    oracle.check(root / "lab", "baseline")

    def test_bad_observations_and_fresh_empty_home(self):
        homes = []
        def observe(argv, **kwargs):
            home = Path(kwargs["env"]["HOME"])
            homes.append(home)
            self.assertEqual(list(home.iterdir()), [])
            self.assertNotIn("GITHUB_TOKEN", kwargs["env"])
            return Result("ok", 0, b'{"observations":[],"count":false}\n')
        with patch.object(oracle, "run", side_effect=observe):
            for _ in range(2):
                with self.assertRaisesRegex(AssertionError, "schema, types, count or values"):
                    oracle.check(ROOT / "labs/sample-app", "refactor")
        self.assertNotEqual(homes[0], homes[1])
        self.assertTrue(all(not home.exists() for home in homes))
