import pytest

def test_quarter_referees_in_tactics(client, mock_coach):
    """Test saving and retrieving tactics containing quarterReferees data."""
    tactics_payload = {
        "match_date": "2026-09-07",
        "opponent": "HV Abcoude Trimmers",
        "quarter": "Q1",
        "data": {
            "assignments": {
                "gk": "Sander Duivesteijn",
                "lb": "Marije Koelink",
                "cb": "Norbert van Haaften"
            },
            "quarterReferees": {
                "Q1": "Rajeev Singhal",
                "Q2": "Tom Weller",
                "Q3": "",
                "Q4": ""
            },
            "subMatrixState": {
                "Rajeev Singhal": [False, False, True, True, True, True, True, True]
            }
        }
    }

    # Save tactics for Trimmers
    save_res = client.post(
        "/api/tactics?team_id=Trimmers",
        json=tactics_payload,
        headers={"Authorization": "Bearer dummy-token"}
    )
    assert save_res.status_code == 200

    # Retrieve saved tactics
    get_res = client.get(
        "/api/tactics?team_id=Trimmers&match_date=2026-09-07&opponent=HV%20Abcoude%20Trimmers&quarter=Q1"
    )
    assert get_res.status_code == 200
    data = get_res.json()["data"]

    assert "quarterReferees" in data
    assert data["quarterReferees"]["Q1"] == "Rajeev Singhal"
    assert data["quarterReferees"]["Q2"] == "Tom Weller"
