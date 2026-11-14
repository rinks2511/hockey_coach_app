import pytest
import json
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import get_db, init_db, execute_query, upsert_setting

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_db()

def test_database_helper_upsert():
    conn = get_db()
    try:
        upsert_setting(conn, "TestTeam", "custom_situations", json.dumps({"S1": "Pressing"}))
        conn.commit()

        cur = execute_query(conn, "SELECT value FROM settings WHERE team_id = ? AND key = 'custom_situations'", ("TestTeam",))
        row = cur.fetchone()
        assert row is not None
        data = json.loads(row["value"])
        assert data.get("S1") == "Pressing"
    finally:
        conn.close()

def test_config_endpoint_custom_situations_and_sub_roles():
    payload = {
        "google_client_id": "test-client-id",
        "coach_emails": ["singhalrajeev89@gmail.com", "coach2@example.com"],
        "squad_players": ["Player A", "Player B"],
        "custom_positions": {"Pos1": "Striker"},
        "custom_situations": {"Situation1": "Overload Left"},
        "custom_sub_roles": {"Player A": "Striker"}
    }
    response = client.post(
        "/api/config?team_id=MO10",
        json=payload,
        headers={"Authorization": "Bearer dummy-token-bypass"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

    # Fetch config back
    get_res = client.get("/api/config?team_id=MO10")
    assert get_res.status_code == 200
    res_data = get_res.json()
    assert res_data["custom_situations"] == {"Situation1": "Overload Left"}
    assert res_data["custom_sub_roles"] == {"Player A": "Striker"}

def test_auth_me_authorized_teams_classification():
    # Register coach2@example.com for Trimmers
    conn = get_db()
    try:
        upsert_setting(conn, "Trimmers", "coach_emails", json.dumps(["coach2@example.com"]))
        conn.commit()
    finally:
        conn.close()

    res = client.get(
        "/api/auth/me?team_id=Trimmers",
        headers={"Authorization": "Bearer dummy-token-bypass"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "user" in data
    assert "authorized_teams" in data
    assert isinstance(data["authorized_teams"], list)

def test_tactics_database_persistence():
    tactics_payload = {
        "match_date": "2026-09-10",
        "opponent": "Rivals HC",
        "quarter": "Q1",
        "title": "Matchday 1 Setup",
        "data": {"formation": "1-2-3-2", "notes": "Press high"}
    }
    post_res = client.post(
        "/api/tactics?team_id=MO10",
        json=tactics_payload,
        headers={"Authorization": "Bearer dummy-token-bypass"}
    )
    assert post_res.status_code == 200
    assert post_res.json()["status"] == "success"

    # Fetch active tactics from database
    active_res = client.get("/api/tactics/active?team_id=MO10")
    assert active_res.status_code == 200
    active_data = active_res.json()
    assert active_data["opponent"] == "Rivals HC"
    assert active_data["data"]["formation"] == "1-2-3-2"

def test_create_team_and_check_access():
    team_payload = {
        "team_id": "U12_Girls",
        "display_name": "U12 Girls Team",
        "coach_emails": ["singhalrajeev89@gmail.com", "assistant@example.com"],
        "squad_players": ["Player 1", "Player 2"],
        "custom_positions": {}
    }
    create_res = client.post(
        "/api/teams",
        json=team_payload,
        headers={"Authorization": "Bearer dummy-token-bypass"}
    )
    assert create_res.status_code == 201

    # Verify new team appears in list
    list_res = client.get("/api/teams")
    assert list_res.status_code == 200
    team_ids = [t["team_id"] for t in list_res.json()]
    assert "U12_Girls" in team_ids

