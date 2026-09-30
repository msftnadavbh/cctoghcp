"""Synthetic in-memory catalog: no network, persistence, or dependencies."""
import argparse
from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price_cents: int
    in_stock: bool

    def __post_init__(self):
        if not isinstance(self.sku, str) or not self.sku.strip():
            raise ValueError("invalid sku")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("invalid name")
        integer(self.price_cents, "price_cents", 0, 1_000_000)
        if type(self.in_stock) is not bool:
            raise ValueError("invalid in_stock")


def integer(value, name, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("invalid " + name)
    return value


PRODUCTS = (Product("A1", "Amber mug", 1200, True),
            Product("B2", "Blue mug", 1500, False),
            Product("C3", "Canvas bag", 2200, True),
            Product("D4", "Desk pad", 3000, False))


def list_products(products=PRODUCTS, *, query="", offset=0, limit=20):
    if not isinstance(query, str) or len(query) > 100:
        raise ValueError("invalid query")
    integer(offset, "offset", 0, 10_000)
    integer(limit, "limit", 1, 100)
    matches = [p for p in products if query.casefold() in p.name.casefold()]
    return {"items": [asdict(p) for p in matches[offset:offset + limit]],
            "total": len(matches), "offset": offset, "limit": limit}


def handle_request(params):
    if not isinstance(params, dict) or set(params) - {"query", "offset", "limit"}:
        raise ValueError("invalid request")
    return list_products(**params)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(handle_request(vars(args)), sort_keys=True))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
