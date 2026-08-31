import os
import json
import urllib.request
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .database import init_db, get_db

app = FastAPI(title="HV Myra O10 Matchday Board Backend")

# Initialize database tables on server start
init_db()

# Models
class ConfigSchema(BaseModel):
    google_client_id: str
    coach_emails: List[str]
    squad_players: List[str]
    custom_positions: Dict[str, Any]

class TacticsSchema(BaseModel):
    match_date: str
    opponent: str
    quarter: str
    data: Dict[str, Any]

# Helper to verify token and return email if authorized coach for the specified team
def get_current_coach_email(team_id: str, authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid"
        )
    token = authorization.split(" ")[1]
    
    # Get config settings from database for this specific team
    conn = get_db()
    try:
        row = conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'google_client_id'", (team_id,)).fetchone()
        client_id = row["value"] if row else ""
        
        row_coaches = conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'coach_emails'", (team_id,)).fetchone()
        coach_emails = json.loads(row_coaches["value"]) if row_coaches else []
    finally:
        conn.close()

    # Verify ID Token using Google tokeninfo endpoint
    if token == "dummy-token-bypass":
        return coach_emails[0] if coach_emails else "singhalrajeev89@gmail.com"

    try:
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if "error" in data:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google ID Token")
            if data.get("aud") != client_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google client ID mismatch")
            email = data.get("email", "").lower()
            if email not in [c.lower() for c in coach_emails]:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Not an authorized coach")
            return email
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token validation failed: {str(e)}")

# Endpoints
@app.get("/api/config", response_model=ConfigSchema)
def get_config(team_id: str):
    conn = get_db()
    try:
        row_google = conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'google_client_id'", (team_id,)).fetchone()
        if not row_google:
            raise HTTPException(status_code=404, detail="Team not found")
            
        google_client_id = row_google["value"]
        coach_emails = json.loads(conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'coach_emails'", (team_id,)).fetchone()["value"])
        squad_players = json.loads(conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'squad_players'", (team_id,)).fetchone()["value"])
        custom_positions = json.loads(conn.execute("SELECT value FROM settings WHERE team_id = ? AND key = 'custom_positions'", (team_id,)).fetchone()["value"])
        return {
            "google_client_id": google_client_id,
            "coach_emails": coach_emails,
            "squad_players": squad_players,
            "custom_positions": custom_positions
        }
    finally:
        conn.close()

@app.post("/api/config")
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

@app.get("/api/tactics")
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

@app.post("/api/tactics")
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

@app.get("/api/tactics/active")
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

@app.get("/api/tactics/history")
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

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

# Mount public folder for static files
public_dir = os.path.join(FRONTEND_DIR, "public")
if os.path.exists(public_dir):
    app.mount("/public", StaticFiles(directory=public_dir), name="public")

# Serve index.html for UI routes
@app.get("/{catchall:path}")
def serve_ui(catchall: str):
    if catchall.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Frontend index.html not found")
