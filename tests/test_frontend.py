def test_root_redirects_to_dashboard(client):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 307
    assert resp.headers["location"] == "/app/"


def test_dashboard_is_served(client):
    resp = client.get("/app/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_dashboard_assets_are_served(client):
    assert client.get("/app/app.js").status_code == 200
    assert client.get("/app/styles.css").status_code == 200
