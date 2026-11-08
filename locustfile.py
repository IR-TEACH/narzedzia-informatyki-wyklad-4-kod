"""Test obciążeniowy API: uv run locust (potem http://localhost:8089)"""
from locust import HttpUser, between, task


class Reader(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(0.5, 1.5)

    @task
    def search_last_book(self):
        # Ostatnia książka z scripts/make_catalog.py: wyszukiwanie przegląda cały katalog
        self.client.get("/books/9790001999991", name="/books/[isbn]")
