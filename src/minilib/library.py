"""Biblioteka: katalog książek i wypożyczenia."""
import json
from pathlib import Path

from minilib.book import Book
from minilib.member import Member


class LoanError(Exception):
    """Wypożyczenie jest niemożliwe."""


class Library:
    def __init__(self, books: list[Book]) -> None:
        self.books = books
        self.loans: dict[str, list[str]] = {}  # e-mail -> ISBN-y
        self._by_isbn = {book.isbn.replace("-", ""): book for book in books}

    @classmethod
    def from_file(cls, path: str = "data/books.json") -> "Library":
        with Path(path).open(encoding="utf-8") as f:
            return cls([Book.from_dict(item) for item in json.load(f)])

    def find_by_isbn(self, isbn: str) -> Book | None:
        return self._by_isbn.get(isbn.replace("-", ""))

    def borrow(self, member: Member, isbn: str) -> None:
        book = self.find_by_isbn(isbn)
        if book is None or book.copies == 0:
            raise LoanError(f"Brak wolnych egzemplarzy: {isbn}")
        loans = self.loans.setdefault(member.email, [])
        if len(loans) >= member.max_loans:
            raise LoanError(f"Limit wypożyczeń: {member.max_loans}")
        book.copies -= 1
        loans.append(isbn)

    def return_book(self, member: Member, isbn: str) -> None:
        book = self.find_by_isbn(isbn)
        if book is None:
            raise LoanError(f"Nie ma takiej książki: {isbn}")
        loans = self.loans.get(member.email, [])
        if isbn not in loans:
            raise LoanError(f"{member.name} nie wypożycza {isbn}")
        loans.remove(isbn)
        book.copies += 1
