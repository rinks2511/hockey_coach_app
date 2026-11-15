import json
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..database import get_db, execute_query, upsert_setting
from .auth import get_current_coach_email

router = APIRouter(prefix="/api/config", tags=["config"])

class ConfigSchema(BaseModel):
    google_client_id: str
    coach_emails: List[str]
    squad_players: List[Any]
    custom_positions: Dict[str, Any]
    custom_situations: Optional[Dict[str, Any]] = None
    custom_sub_roles: Optional[Dict[str, Any]] = None

@router.get("", response_model=ConfigSchema)
def get_config(team_id: str):
    conn = get_db()
    try:
        row_google = execute_query(conn, "SELECT value FROM settings WHERE team_id = ? AND key = 'google_client_id'", (team_id,)).fetchone()
        if not row_google:
            raise HTTPException(status_code=404, detail=f"Team '{team_id}' not found")
            
        google_client_id = row_google["value"]
        
        row_coaches = execute_query(conn, "SELECT value FROM settings WHERE team_id = ? AND key = 'coach_emails'", (team_id,)).fetchone()
        coach_emails = json.loads(row_coaches["value"]) if row_coaches else []

        row_squad = execute_query(conn, "SELECT value FROM settings WHERE team_id = ? AND key = 'squad_players'", (team_id,)).fetchone()
        squad_players = json.loads(row_squad["value"]) if row_squad else []

        # Sanitize cross-team data leaks if present
        squad_str = json.dumps(squad_players)
        if team_id == "Trimmers" and ("Sai Jiya" in squad_str or "Defne" in squad_str or "Shanaya" in squad_str):
            from ..config import settings
            squad_players = settings.DEFAULT_TRIMMERS_SQUAD_PLAYERS
            upsert_setting(conn, team_id, 'squad_players', json.dumps(squad_players))
            conn.commit()
        elif team_id == "MO10":
            if "Sander Duivesteijn" in squad_str or "Rajeev Singhal" in squad_str:
                from ..config import settings
                squad_players = settings.DEFAULT_SQUAD_PLAYERS
                upsert_setting(conn, team_id, 'squad_players', json.dumps(squad_players))
                conn.commit()
            else:
                updated = False
                for p in squad_players:
                    if isinstance(p, dict) and p.get("name", "").lower() == "ayana" and p.get("gender") != "F":
                        p["gender"] = "F"
                        updated = True
                if not any("ayana" in (p if isinstance(p, str) else p.get("name", "")).lower() for p in squad_players):
                    squad_players.append("Ayana")
                    updated = True
                if updated:
                    upsert_setting(conn, team_id, 'squad_players', json.dumps(squad_players))
                    conn.commit()
        
        row_positions = execute_query(conn, "SELECT value FROM settings WHERE team_id = ? AND key = 'custom_positions'", (team_id,)).fetchone()
        custom_positions = json.loads(row_positions["value"]) if row_positions else {}

        row_situations = execute_query(conn, "SELECT value FROM settings WHERE team_id = ? AND key = 'custom_situations'", (team_id,)).fetchone()
        custom_situations = json.loads(row_situations["value"]) if row_situations else {}

        row_sub_roles = execute_query(conn, "SELECT value FROM settings WHERE team_id = ? AND key = 'custom_sub_roles'", (team_id,)).fetchone()
        custom_sub_roles = json.loads(row_sub_roles["value"]) if row_sub_roles else {}

        return {
            "google_client_id": google_client_id,
            "coach_emails": coach_emails,
            "squad_players": squad_players,
            "custom_positions": custom_positions,
            "custom_situations": custom_situations,
            "custom_sub_roles": custom_sub_roles
        }
    finally:
        conn.close()

@router.post("")
def save_config(team_id: str, config: ConfigSchema, email: str = Depends(get_current_coach_email)):
    conn = get_db()
    try:
        upsert_setting(conn, team_id, 'google_client_id', config.google_client_id)
        upsert_setting(conn, team_id, 'coach_emails', json.dumps(config.coach_emails))
        upsert_setting(conn, team_id, 'squad_players', json.dumps(config.squad_players))
        upsert_setting(conn, team_id, 'custom_positions', json.dumps(config.custom_positions))
        if config.custom_situations is not None:
            upsert_setting(conn, team_id, 'custom_situations', json.dumps(config.custom_situations))
        if config.custom_sub_roles is not None:
            upsert_setting(conn, team_id, 'custom_sub_roles', json.dumps(config.custom_sub_roles))
        conn.commit()
        return {"status": "success", "message": "Settings updated"}
    finally:
        conn.close()

