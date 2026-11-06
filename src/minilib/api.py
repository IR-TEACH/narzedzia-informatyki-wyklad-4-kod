"""HTTP API MiniLib. Start: uv run uvicorn minilib.api:app --reload"""
import os

from fastapi import Depends, FastAPI, HTTPException

from minilib.auth import current_member
from minilib.book import Book
from minilib.library import Library, LoanError
from minilib.member import Member

app = FastAPI(title="MiniLib")
library = Library.from_file(os.environ.get("MINILIB_BOOKS", "data/books.json"))


@app.get("/books/{isbn}")
def get_book(isbn: str) -> Book:
    book = library.find_by_isbn(isbn)
    if book is None:
        raise HTTPException(404, "Nie ma takiej książki")
    return book


@app.post("/loans/{isbn}")
def borrow(isbn: str, member: Member = Depends(current_member)) -> list[str]:
    try:
        library.borrow(member, isbn)
    except LoanError as e:
        raise HTTPException(409, str(e)) from e
    return library.loans[member.email]


@app.get("/members/{email}/loans")
def member_loans(email: str, member: Member = Depends(current_member)) -> list[str]:
    return library.loans.get(email, [])
