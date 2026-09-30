import json
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from catalog import Product, handle_request, list_products


class CatalogTests(unittest.TestCase):
    def test_validation(self):
        for value in (True, False, "2", 1.2, None, -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                Product("x", "name", value, True)
        for params in ({"limit": True}, {"offset": False}, {"limit": 0},
                       {"limit": 101}, {"offset": -1}, {"query": 2},
                       {"unknown": 1}, {"query": "x" * 101}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                handle_request(params)

    def test_filter_page_serialization(self):
        result = list_products(query="MUG", offset=1, limit=1)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["items"][0]["sku"], "B2")
        self.assertIs(result["items"][0]["in_stock"], False)
        self.assertEqual(json.loads(json.dumps(result)), result)
        self.assertEqual(list_products(offset=100)["items"], [])

    def test_cli(self):
        path = Path(__file__).resolve().parents[1] / "src/catalog.py"
        proc = subprocess.run([sys.executable, "-I", "-B", str(path), "--query", "bag"],
                              capture_output=True, text=True, timeout=5)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout)["items"][0]["sku"], "C3")
