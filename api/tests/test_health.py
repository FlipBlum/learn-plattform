from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_news_endpoint():
    response = client.get("/api/news/")
    assert response.status_code == 200


def test_videos_endpoint():
    response = client.get("/api/videos/")
    assert response.status_code == 200


def test_auth_endpoint():
    response = client.get("/api/auth/")
    assert response.status_code == 200
