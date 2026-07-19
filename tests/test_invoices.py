def test_create_invoice(invoice):
    assert invoice["status"] == "pending"
    assert invoice["customer_name"] == "Acme Ltd"
    assert invoice["amount_ngn"] == 150000.0
    assert invoice["id"]


def test_create_invoice_rejects_bad_payload(client):
    resp = client.post("/invoices", json={"customer_name": "", "amount_ngn": -5})
    assert resp.status_code == 422


def test_list_invoices(client, invoice):
    resp = client.get("/invoices")
    assert resp.status_code == 200
    assert [i["id"] for i in resp.json()] == [invoice["id"]]


def test_get_invoice(client, invoice):
    resp = client.get(f"/invoices/{invoice['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == invoice["id"]


def test_get_unknown_invoice_returns_404(client):
    resp = client.get("/invoices/does-not-exist")
    assert resp.status_code == 404
