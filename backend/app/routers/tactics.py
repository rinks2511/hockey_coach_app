import json
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..database import get_db
from .auth import get_current_coach_email

router = APIRouter(prefix="/api/tactics", tags=["tactics"])

class TacticsSchema(BaseModel):
    match_date: str
    opponent: str
    quarter: str
    data: Dict[str, Any]

@router.get("")
def get_tactics(team_id: str, match_date: str, opponent: str, quarter: str):
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT data FROM tactics WHERE team_id = ? AND match_date = ? AND opponent = ? AND quarter = ?",
            (team_id, match_date, opponent, quarter)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Tactics not found")
        return {"data": json.loads(row["data"])}
    finally:
        conn.close()

@router.post("")
def save_tactics(team_id: str, tactics: TacticsSchema, email: str = Depends(get_current_coach_email)):
    conn = get_db()
    try:
        conn.execute(
            """
            INSERT INTO tactics (team_id, match_date, opponent, quarter, data, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(team_id, match_date, opponent, quarter) 
            DO UPDATE SET data = excluded.data, updated_at = CURRENT_TIMESTAMP
            """,
            (team_id, tactics.match_date, tactics.opponent, tactics.quarter, json.dumps(tactics.data))
        )
        conn.commit()
        return {"status": "success", "message": "Tactics saved"}
    finally:
        conn.close()

@router.get("/active")
def get_active_tactics(team_id: str):
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT match_date, opponent, quarter, data FROM tactics WHERE team_id = ? ORDER BY updated_at DESC LIMIT 1",
            (team_id,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="No active tactics found")
        return {
            "match_date": row["match_date"],
            "opponent": row["opponent"],
            "quarter": row["quarter"],
            "data": json.loads(row["data"])
        }
    finally:
        conn.close()

@router.get("/history")
def get_tactics_history(team_id: str):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT match_date, opponent, quarter, updated_at FROM tactics WHERE team_id = ? ORDER BY updated_at DESC",
            (team_id,)
        ).fetchall()
        return [
            {
                "match_date": r["match_date"],
                "opponent": r["opponent"],
                "quarter": r["quarter"],
                "updated_at": r["updated_at"]
            }
            for r in rows
        ]
    finally:
        conn.close()
