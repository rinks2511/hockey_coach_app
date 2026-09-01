import sqlite3
import json
from .config import settings

def get_db():
    conn = sqlite3.connect(settings.DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        # Non-destructive migration checks
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings'")
        if cur.fetchone():
            cur_info = conn.execute("PRAGMA table_info(settings)")
            cols = [row["name"] for row in cur_info.fetchall()]
            if "team_id" not in cols:
                # Add team_id column non-destructively if needed
                conn.execute("ALTER TABLE settings ADD COLUMN team_id TEXT DEFAULT 'MO10'")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                team_id TEXT,
                key TEXT,
                value TEXT,
                PRIMARY KEY (team_id, key)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tactics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id TEXT,
                match_date TEXT,
                opponent TEXT,
                quarter TEXT,
                data TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_tactics_period_team 
            ON tactics(team_id, match_date, opponent, quarter)
        """)
        
        # Seed initial teams dynamically if database is empty
        cur_teams = conn.execute("SELECT DISTINCT team_id FROM settings").fetchall()
        existing_teams = [r["team_id"] for r in cur_teams]

        initial_teams = ["MO10", "Trimmers"]
        for team in initial_teams:
            # Seed coach emails
            cur = conn.execute("SELECT 1 FROM settings WHERE team_id = ? AND key = 'coach_emails'", (team,))
            if not cur.fetchone():
                conn.execute(
                    "INSERT INTO settings (team_id, key, value) VALUES (?, ?, ?)",
                    (team, "coach_emails", json.dumps(settings.DEFAULT_COACH_EMAILS))
                )
            
            # Seed Google client ID
            cur = conn.execute("SELECT 1 FROM settings WHERE team_id = ? AND key = 'google_client_id'", (team,))
            if not cur.fetchone():
                conn.execute(
                    "INSERT INTO settings (team_id, key, value) VALUES (?, ?, ?)",
                    (team, "google_client_id", settings.DEFAULT_GOOGLE_CLIENT_ID)
                )

            # Seed custom positions
            cur = conn.execute("SELECT 1 FROM settings WHERE team_id = ? AND key = 'custom_positions'", (team,))
            if not cur.fetchone():
                conn.execute(
                    "INSERT INTO settings (team_id, key, value) VALUES (?, ?, ?)",
                    (team, "custom_positions", json.dumps({}))
                )

        # Seed squad players specifically
        cur_mo10 = conn.execute("SELECT 1 FROM settings WHERE team_id = 'MO10' AND key = 'squad_players'")
        if not cur_mo10.fetchone():
            conn.execute(
                "INSERT INTO settings (team_id, key, value) VALUES (?, ?, ?)",
                ("MO10", "squad_players", json.dumps(settings.DEFAULT_SQUAD_PLAYERS))
            )
            
        cur_trimmers = conn.execute("SELECT 1 FROM settings WHERE team_id = 'Trimmers' AND key = 'squad_players'")
        if not cur_trimmers.fetchone():
            conn.execute(
                "INSERT INTO settings (team_id, key, value) VALUES (?, ?, ?)",
                ("Trimmers", "squad_players", json.dumps(settings.DEFAULT_TRIMMERS_SQUAD_PLAYERS))
            )

        conn.commit()
