from hypothesis import given
from hypothesis import strategies as st

from minilib.library import Library, LoanError
from minilib.member import Member

MEMBERS = [
    Member("Anna Nowak", "anna.nowak@example.com"),
    Member("Jan Kowalski", "jan.kowalski@example.com"),
]
ISBNS = ["978-0-13-235088-4", "978-0-13-475759-9"]
OPERATION = st.tuples(
    st.sampled_from(["borrow", "return_book"]),
    st.sampled_from(MEMBERS),
    st.sampled_from(ISBNS),
)


@given(st.lists(OPERATION))
def test_books_do_not_disappear_or_multiply(operations):
    library = Library.from_file()
    before = {book.isbn: book.copies for book in library.books}
    for name, member, isbn in operations:
        try:
            getattr(library, name)(member, isbn)
        except LoanError:
            pass
    for book in library.books:
        on_loan = sum(loans.count(book.isbn) for loans in library.loans.values())
        assert book.copies + on_loan == before[book.isbn]
