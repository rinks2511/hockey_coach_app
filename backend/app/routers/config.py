import json
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..database import get_db
from .auth import get_current_coach_email

router = APIRouter(prefix="/api/config", tags=["config"])

class ConfigSchema(BaseModel):
    google_client_id: str
    coach_emails: List[str]
    squad_players: List[Any]
    custom_positions: Dict[str, Any]

@router.get("", response_model=ConfigSchema)
def get_config(team_id: str):
    conn = get_db()
    try:
        row_google = conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'google_client_id'", (team_id,)).fetchone()
        if not row_google:
            raise HTTPException(status_code=404, detail=f"Team '{team_id}' not found")
            
        google_client_id = row_google["value"]
        coach_emails = json.loads(conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'coach_emails'", (team_id,)).fetchone()["value"])
        squad_players = json.loads(conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'squad_players'", (team_id,)).fetchone()["value"])
        
        row_positions = conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'custom_positions'", (team_id,)).fetchone()
        custom_positions = json.loads(row_positions["value"]) if row_positions else {}

        return {
            "google_client_id": google_client_id,
            "coach_emails": coach_emails,
            "squad_players": squad_players,
            "custom_positions": custom_positions
        }
    finally:
        conn.close()

@router.post("")
def save_config(team_id: str, config: ConfigSchema, email: str = Depends(get_current_coach_email)):
    conn = get_db()
    try:
        conn.execute("INSERT OR REPLACE INTO settings (team_id, key, value) VALUES (?, 'google_client_id', ?)", (team_id, config.google_client_id))
        conn.execute("INSERT OR REPLACE INTO settings (team_id, key, value) VALUES (?, 'coach_emails', ?)", (team_id, json.dumps(config.coach_emails)))
        conn.execute("INSERT OR REPLACE INTO settings (team_id, key, value) VALUES (?, 'squad_players', ?)", (team_id, json.dumps(config.squad_players)))
        conn.execute("INSERT OR REPLACE INTO settings (team_id, key, value) VALUES (?, 'custom_positions', ?)", (team_id, json.dumps(config.custom_positions)))
        conn.commit()
        return {"status": "success", "message": "Settings updated"}
    finally:
        conn.close()
