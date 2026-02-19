from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_auth_login_returns_url():
    response = client.get("/api/auth/login")
    assert response.status_code == 200


def test_auth_me_requires_token():
    response = client.get("/api/auth/me")
    assert response.status_code == 403
