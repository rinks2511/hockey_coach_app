import json
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from ..database import get_db, execute_query
from .auth import get_current_coach_email

router = APIRouter(prefix="/api/tactics", tags=["tactics"])

class TacticsSchema(BaseModel):
    match_date: str
    opponent: Optional[str] = ""
    quarter: Optional[str] = "Q1"
    title: Optional[str] = None
    data: Dict[str, Any]

@router.get("")
def get_tactics(team_id: str, match_date: str, opponent: Optional[str] = "", quarter: Optional[str] = "Q1"):
    conn = get_db()
    try:
        row = execute_query(
            conn,
            "SELECT data, title FROM tactics WHERE team_id = ? AND match_date = ? AND opponent = ? AND quarter = ?",
            (team_id, match_date, opponent or "", quarter or "Q1")
        ).fetchone()
        if not row:
            # Fallback by team_id and match_date
            row = execute_query(
                conn,
                "SELECT data, title FROM tactics WHERE team_id = ? AND match_date = ? ORDER BY updated_at DESC LIMIT 1",
                (team_id, match_date)
            ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Tactics not found")
        return {"data": json.loads(row["data"]), "title": row["title"] or ""}
    finally:
        conn.close()

@router.get("/by-id")
def get_tactic_by_id(id: int = Query(...)):
    conn = get_db()
    try:
        row = execute_query(conn, "SELECT id, team_id, match_date, opponent, quarter, title, data, updated_at FROM tactics WHERE id = ?", (id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Tactic file not found")
        return {
            "id": row["id"],
            "team_id": row["team_id"],
            "match_date": row["match_date"],
            "opponent": row["opponent"],
            "quarter": row["quarter"],
            "title": row["title"],
            "data": json.loads(row["data"]),
            "updated_at": row["updated_at"]
        }
    finally:
        conn.close()

@router.post("")
def save_tactics(team_id: str, tactics: TacticsSchema, email: str = Depends(get_current_coach_email)):
    conn = get_db()
    try:
        title_val = tactics.title or f"{tactics.match_date} - {tactics.opponent or 'Match'}"
        opponent_val = tactics.opponent or ""
        quarter_val = tactics.quarter or "Q1"

        # Check if record exists for this team, date, opponent, quarter
        existing = execute_query(
            conn,
            "SELECT id FROM tactics WHERE team_id = ? AND match_date = ? AND opponent = ? AND quarter = ?",
            (team_id, tactics.match_date, opponent_val, quarter_val)
        ).fetchone()

        if existing:
            execute_query(
                conn,
                "UPDATE tactics SET title = ?, data = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (title_val, json.dumps(tactics.data), existing["id"])
            )
        else:
            execute_query(
                conn,
                "INSERT INTO tactics (team_id, match_date, opponent, quarter, title, data, updated_at) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (team_id, tactics.match_date, opponent_val, quarter_val, title_val, json.dumps(tactics.data))
            )
        conn.commit()
        return {"status": "success", "message": "Tactics saved"}
    finally:
        conn.close()

@router.delete("")
def delete_tactic(id: int = Query(...), team_id: Optional[str] = Query(default=None), email: str = Depends(get_current_coach_email)):
    conn = get_db()
    try:
        if team_id:
            execute_query(conn, "DELETE FROM tactics WHERE id = ? AND team_id = ?", (id, team_id))
        else:
            execute_query(conn, "DELETE FROM tactics WHERE id = ?", (id,))
        conn.commit()
        return {"status": "success", "message": "File deleted"}
    finally:
        conn.close()

@router.get("/active")
def get_active_tactics(team_id: str):
    conn = get_db()
    try:
        rows = execute_query(
            conn,
            "SELECT id, match_date, opponent, quarter, title, data FROM tactics WHERE team_id = ? ORDER BY updated_at DESC",
            (team_id,)
        ).fetchall()
        
        for row in rows:
            data = json.loads(row["data"])
            # Validate that data payload isn't a cross-team mismatched legacy save
            opp = (row["opponent"] or "").lower()
            title = (row["title"] or "").lower()
            data_str = json.dumps(data)
            formation = data.get("activeFormation", "")

            if team_id == "Trimmers" and (formation in ("1-2-3-2", "1-3-3-1") or "Sai Jiya" in data_str or "Defne" in data_str or "mo10" in opp or "mo10" in title):
                continue
            if team_id == "MO10" and (formation in ("4-3-3", "4-4-2", "3-1-3-3") or "Sander Duivesteijn" in data_str or "trimmers" in opp or "trimmers" in title):
                continue

            return {
                "id": row["id"],
                "match_date": row["match_date"],
                "opponent": row["opponent"],
                "quarter": row["quarter"],
                "title": row["title"],
                "data": data
            }

        raise HTTPException(status_code=404, detail="No active tactics found")
    finally:
        conn.close()

@router.get("/history")
def get_tactics_history(team_id: str):
    conn = get_db()
    try:
        rows = execute_query(
            conn,
            "SELECT id, match_date, opponent, quarter, title, updated_at FROM tactics WHERE team_id = ? ORDER BY updated_at DESC",
            (team_id,)
        ).fetchall()
        return [
            {
                "id": r["id"],
                "match_date": r["match_date"],
                "opponent": r["opponent"],
                "quarter": r["quarter"],
                "title": r["title"] or f"{r['match_date']} - {r['opponent'] or 'Match'}",
                "updated_at": r["updated_at"]
            }
            for r in rows
        ]
    finally:
        conn.close()

@router.delete("/clean-history")
def clean_tactics_history(team_id: str, email: str = Depends(get_current_coach_email)):
    conn = get_db()
    try:
        execute_query(conn, "DELETE FROM tactics WHERE team_id = ?", (team_id,))
        conn.commit()
        return {"status": "success", "message": f"Cleared tactics history for team '{team_id}'"}
    finally:
        conn.close()

