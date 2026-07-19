def test_pay_invoice(client, invoice):
    resp = client.post(f"/invoices/{invoice['id']}/pay")
    assert resp.status_code == 200
    body = resp.json()
    assert body["invoice_id"] == invoice["id"]
    assert body["amount_ngn"] == invoice["amount_ngn"]

    assert client.get(f"/invoices/{invoice['id']}").json()["status"] == "paid"


def test_pay_unknown_invoice_returns_404(client):
    resp = client.post("/invoices/nope/pay")
    assert resp.status_code == 404


def test_double_payment_returns_409(client, invoice):
    assert client.post(f"/invoices/{invoice['id']}/pay").status_code == 200
    resp = client.post(f"/invoices/{invoice['id']}/pay")
    assert resp.status_code == 409


def test_transactions_recorded(client, invoice):
    client.post(f"/invoices/{invoice['id']}/pay")
    resp = client.get("/transactions")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["invoice_id"] == invoice["id"]


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_metrics_exposes_business_counter(client, invoice):
    client.post(f"/invoices/{invoice['id']}/pay")
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "invoices_paid_total" in resp.text
