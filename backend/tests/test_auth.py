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

def test_request_and_approve_access():
    """Verify sign-up access request creation and admin approval flow."""
    # 1. User submits access request
    req_res = client.post(
        "/api/auth/request-access",
        json={"team_id": "Trimmers", "requested_role": "coach", "user_email": "applicant@example.com", "user_name": "Test Applicant"}
    )
    assert req_res.status_code == 200
    assert req_res.json()["status"] == "success"

    # 2. Coach lists access requests
    list_res = client.get(
        "/api/auth/access-requests?team_id=Trimmers",
        headers={"Authorization": "Bearer dummy-token-bypass"}
    )
    assert list_res.status_code == 200
    requests = list_res.json()
    req = next((r for r in requests if r["user_email"] == "applicant@example.com"), None)
    assert req is not None
    assert req["status"] == "pending"

    # 3. Coach approves request
    app_res = client.post(
        "/api/auth/access-requests/approve",
        json={"request_id": req["id"]},
        headers={"Authorization": "Bearer dummy-token-bypass"}
    )
    assert app_res.status_code == 200
    assert app_res.json()["status"] == "success"

def test_parent_player_instant_access():
    """Verify Parent/Player access requests get instant approved status on registration."""
    req_res = client.post(
        "/api/auth/request-access",
        json={"team_id": "Trimmers", "requested_role": "parent_player", "user_email": "parentplayer@example.com", "user_name": "Test Parent Player"}
    )
    assert req_res.status_code == 200

    list_res = client.get(
        "/api/auth/access-requests?team_id=Trimmers",
        headers={"Authorization": "Bearer dummy-token-bypass"}
    )
    assert list_res.status_code == 200
    requests = list_res.json()
    req = next((r for r in requests if r["user_email"] == "parentplayer@example.com"), None)
    assert req is not None
    assert req["status"] == "approved"

def test_direct_email_approval_link():
    """Verify clicking 1-click email approval link approves the user instantly."""
    req_res = client.post(
        "/api/auth/request-access",
        json={"team_id": "MO10", "requested_role": "coach", "user_email": "emailcoach@example.com", "user_name": "Email Coach"}
    )
    assert req_res.status_code == 200
    request_id = req_res.json()["request_id"]

    approve_res = client.get(f"/api/auth/approve-request-direct?request_id={request_id}")
    assert approve_res.status_code == 200
    assert "Coach Access Approved" in approve_res.text




