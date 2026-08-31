from backend.app.main import get_current_coach_email, app

def test_get_tactics_not_found(client):
    response = client.get("/api/tactics?team_id=MO10&match_date=2026-08-30&opponent=NonExistent&quarter=H1")
    assert response.status_code == 404

def test_save_and_get_tactics(client, mock_coach):
    app.dependency_overrides[get_current_coach_email] = mock_coach
    try:
        tactics_payload = {
            "match_date": "2026-08-30",
            "opponent": "Pinoke O10",
            "quarter": "H1",
            "data": {
                "assignments": {"gk": "Kyra"},
                "notes": "Some match notes here"
            }
        }
        
        # Save tactics
        save_res = client.post("/api/tactics?team_id=MO10", json=tactics_payload, headers={"Authorization": "Bearer dummy-token"})
        assert save_res.status_code == 200
        
        # Retrieve tactics
        get_res = client.get("/api/tactics?team_id=MO10&match_date=2026-08-30&opponent=Pinoke%20O10&quarter=H1")
        assert get_res.status_code == 200
        data = get_res.json()
        assert data["data"]["assignments"]["gk"] == "Kyra"
        assert data["data"]["notes"] == "Some match notes here"
    finally:
        app.dependency_overrides.clear()

def test_get_active_tactics(client, mock_coach):
    app.dependency_overrides[get_current_coach_email] = mock_coach
    try:
        # First check that active tactics returns 404 since it's a new match
        res = client.get("/api/tactics/active?team_id=MO10")
        assert res.status_code == 404

        # Save some tactics
        tactics_payload = {
            "match_date": "2026-08-30",
            "opponent": "Hurley O10",
            "quarter": "H2",
            "data": {"assignments": {}, "notes": "Active match test"}
        }
        client.post("/api/tactics?team_id=MO10", json=tactics_payload, headers={"Authorization": "Bearer dummy-token"})

        # Retrieve active tactics
        active_res = client.get("/api/tactics/active?team_id=MO10")
        assert active_res.status_code == 200
        data = active_res.json()
        assert data["opponent"] == "Hurley O10"
        assert data["quarter"] == "H2"
        assert data["data"]["notes"] == "Active match test"
    finally:
        app.dependency_overrides.clear()

def test_get_tactics_history_and_isolation(client, mock_coach):
    app.dependency_overrides[get_current_coach_email] = mock_coach
    try:
        # Save tactics for MO10
        client.post("/api/tactics?team_id=MO10", json={
            "match_date": "2026-08-28",
            "opponent": "Match MO10",
            "quarter": "H1",
            "data": {}
        }, headers={"Authorization": "Bearer dummy"})

        # Save tactics for Trimmers
        client.post("/api/tactics?team_id=Trimmers", json={
            "match_date": "2026-08-29",
            "opponent": "Match Trimmers",
            "quarter": "H2",
            "data": {}
        }, headers={"Authorization": "Bearer dummy"})

        # Get history list for MO10
        history_mo10 = client.get("/api/tactics/history?team_id=MO10").json()
        opponents_mo10 = [h["opponent"] for h in history_mo10]
        assert "Match MO10" in opponents_mo10
        assert "Match Trimmers" not in opponents_mo10

        # Get history list for Trimmers
        history_trimmers = client.get("/api/tactics/history?team_id=Trimmers").json()
        opponents_trimmers = [h["opponent"] for h in history_trimmers]
        assert "Match Trimmers" in opponents_trimmers
        assert "Match MO10" not in opponents_trimmers
    finally:
        app.dependency_overrides.clear()
