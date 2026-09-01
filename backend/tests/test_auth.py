import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import settings

client = TestClient(app)

def test_auth_dev_mode_fallback():
    """Verify backend returns developer payload when dev mode bypass header is supplied."""
    response = client.get("/api/auth/me?team_id=MO10", headers={"Authorization": "Bearer dummy-token-bypass"})
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] in settings.DEFAULT_COACH_EMAILS
    assert data["is_coach"] is True

def test_auth_header_parsing():
    """Verify authorization header processing."""
    response = client.get(
        "/api/auth/me?team_id=MO10",
        headers={"Authorization": "Bearer fake-token-for-test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "user" in data

def test_auth_missing_header_unauthorized():
    """Verify 401 response when Authorization header is missing."""
    response = client.get("/api/auth/me?team_id=MO10")
    assert response.status_code == 401
