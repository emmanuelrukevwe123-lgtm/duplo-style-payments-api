import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import store


@pytest.fixture(autouse=True)
def clean_store():
    store.reset()
    yield
    store.reset()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def invoice(client):
    resp = client.post(
        "/invoices",
        json={"customer_name": "Acme Ltd", "amount_ngn": 150000.0, "due_date": "2026-08-01"},
    )
    assert resp.status_code == 201
    return resp.json()
