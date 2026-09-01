from backend.app.main import app
from backend.app.routers.auth import get_current_coach_email

def test_list_teams(client):
    res = client.get("/api/teams")
    assert res.status_code == 200
    data = res.json()
    team_ids = [t["team_id"] for t in data]
    assert "MO10" in team_ids
    assert "Trimmers" in team_ids

def test_create_team(client, mock_coach):
    app.dependency_overrides[get_current_coach_email] = mock_coach
    try:
        new_team = {
            "team_id": "Heren1",
            "coach_emails": ["singhalrajeev89@gmail.com"],
            "squad_players": ["Player 1", "Player 2", "Player 3"]
        }
        res = client.post("/api/teams", json=new_team, headers={"Authorization": "Bearer dummy-token"})
        assert res.status_code == 201
        
        # Verify team is listed
        list_res = client.get("/api/teams")
        data = list_res.json()
        team_ids = [t["team_id"] for t in data]
        assert "Heren1" in team_ids

        # Check config for Heren1
        cfg_res = client.get("/api/config?team_id=Heren1")
        assert cfg_res.status_code == 200
        cfg_data = cfg_res.json()
        assert cfg_data["squad_players"] == ["Player 1", "Player 2", "Player 3"]
    finally:
        app.dependency_overrides.clear()
