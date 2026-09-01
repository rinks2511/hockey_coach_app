import json
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from ..database import get_db
from .auth import get_current_coach_email, get_current_user_email

router = APIRouter(prefix="/api/teams", tags=["teams"])

class CreateTeamSchema(BaseModel):
    team_id: str
    display_name: Optional[str] = None
    coach_emails: List[str]
    squad_players: List[str]
    custom_positions: Optional[Dict[str, Any]] = None

@router.get("", response_model=List[Dict[str, Any]])
def list_teams():
    conn = get_db()
    try:
        rows = conn.execute("SELECT DISTINCT team_id FROM settings").fetchall()
        teams = []
        for r in rows:
            tid = r["team_id"]
            coach_row = conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'coach_emails'", (tid,)).fetchone()
            squad_row = conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'squad_players'", (tid,)).fetchone()
            teams.append({
                "team_id": tid,
                "coach_emails": json.loads(coach_row["value"]) if coach_row else [],
                "player_count": len(json.loads(squad_row["value"])) if squad_row else 0
            })
        return teams
    finally:
        conn.close()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_team(team: CreateTeamSchema, email: str = Depends(get_current_user_email)):
    conn = get_db()
    try:
        cur = conn.execute("SELECT 1 FROM settings WHERE team_id = ?", (team.team_id,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail=f"Team '{team.team_id}' already exists")

        # Set default google client ID if not provided
        google_client_row = conn.execute("SELECT value FROM settings WHERE key = 'google_client_id' LIMIT 1").fetchone()
        client_id = google_client_row["value"] if google_client_row else ""

        conn.execute("INSERT INTO settings (team_id, key, value) VALUES (?, 'google_client_id', ?)", (team.team_id, client_id))
        conn.execute("INSERT INTO settings (team_id, key, value) VALUES (?, 'coach_emails', ?)", (team.team_id, json.dumps(team.coach_emails)))
        conn.execute("INSERT INTO settings (team_id, key, value) VALUES (?, 'squad_players', ?)", (team.team_id, json.dumps(team.squad_players)))
        conn.execute("INSERT INTO settings (team_id, key, value) VALUES (?, 'custom_positions', ?)", (team.team_id, json.dumps(team.custom_positions or {})))
        conn.commit()
        return {"status": "success", "message": f"Team '{team.team_id}' created successfully"}
    finally:
        conn.close()
