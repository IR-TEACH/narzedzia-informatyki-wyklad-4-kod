from fastapi.testclient import TestClient

from minilib.api import app

client = TestClient(app)
ANNA = {"Authorization": "Bearer token-anna"}
JAN = {"Authorization": "Bearer token-jan"}


def test_get_book():
    response = client.get("/books/978-0-13-235088-4")

    assert response.status_code == 200
    assert response.json()["title"] == "Clean Code"


def test_unknown_book_is_404():
    assert client.get("/books/978-0-00-000000-2").status_code == 404


def test_borrow_requires_token():
    assert client.post("/loans/978-0-13-475759-9").status_code == 401


def test_borrow_last_copy():
    response = client.post("/loans/978-0-13-475759-9", headers=ANNA)  # 1 egz.

    assert response.status_code == 200


def test_last_copy_is_gone_for_others():
    response = client.post("/loans/978-0-13-475759-9", headers=JAN)

    assert response.status_code == 409


def test_cannot_read_others_loans():
    response = client.get("/members/anna.nowak@example.com/loans", headers=JAN)

    assert response.status_code == 403
