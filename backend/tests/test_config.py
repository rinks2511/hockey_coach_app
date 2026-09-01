from backend.app.main import app
from backend.app.routers.auth import get_current_coach_email

def test_get_config(client):
    response = client.get("/api/config?team_id=MO10")
    assert response.status_code == 200
    data = response.json()
    assert "google_client_id" in data
    assert "coach_emails" in data
    assert "squad_players" in data
    assert "custom_positions" in data
    assert "singhalrajeev89@gmail.com" in data["coach_emails"]

def test_get_config_not_found(client):
    response = client.get("/api/config?team_id=InvalidTeam")
    assert response.status_code == 404

def test_post_config_unauthorized(client):
    payload = {
        "google_client_id": "new-google-id",
        "coach_emails": ["singhalrajeev89@gmail.com"],
        "squad_players": ["Player A"],
        "custom_positions": {}
    }
    response = client.post("/api/config?team_id=MO10", json=payload)
    assert response.status_code == 401

def test_post_config_authorized(client, mock_coach):
    # Override coach validation dependency
    app.dependency_overrides[get_current_coach_email] = mock_coach
    try:
        payload = {
            "google_client_id": "new-google-id",
            "coach_emails": ["singhalrajeev89@gmail.com", "coach2@gmail.com"],
            "squad_players": ["Player A", "Player B"],
            "custom_positions": {"gk": {"en": {"code": "G", "label": "GK", "circle": "G"}, "nl": {"code": "K", "label": "K", "circle": "K"}}}
        }
        response = client.post("/api/config?team_id=MO10", json=payload, headers={"Authorization": "Bearer dummy-token"})
        assert response.status_code == 200
        
        # Verify changes took effect
        get_res = client.get("/api/config?team_id=MO10")
        data = get_res.json()
        assert data["google_client_id"] == "new-google-id"
        assert "coach2@gmail.com" in data["coach_emails"]
        assert "Player A" in data["squad_players"]
    finally:
        app.dependency_overrides.clear()
