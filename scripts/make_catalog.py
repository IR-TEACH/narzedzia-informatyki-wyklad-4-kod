"""Duży katalog do testu obciążeniowego: uv run python scripts/make_catalog.py"""
import json
import sys


def isbn13(n: int) -> str:
    digits = f"979{n:09d}"
    total = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(digits))
    return digits + str(-total % 10)


count = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
books = [
    {"isbn": isbn13(n), "title": f"Książka {n}", "author": "Autor, Anonim"}
    for n in range(count)
]
with open("data/catalog-big.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False)
print(f"Zapisano {count} książek do data/catalog-big.json")
