import sqlite3
import json
from .config import settings

def get_db():
    conn = sqlite3.connect(settings.DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        # Check if legacy settings table exists and lacks team_id column
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings'")
        if cur.fetchone():
            cur_info = conn.execute("PRAGMA table_info(settings)")
            cols = [row["name"] for row in cur_info.fetchall()]
            if "team_id" not in cols:
                # Dropping legacy tables to recreate with multi-team structure
                conn.execute("DROP TABLE settings")
                conn.execute("DROP TABLE tactics")

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
        # Create an index for unique matching per team
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_tactics_period_team 
            ON tactics(team_id, match_date, opponent, quarter)
        """)
        
        # Seed both teams: MO10 and Trimmers
        teams = ["MO10", "Trimmers"]
        for team in teams:
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
        # MO10
        cur = conn.execute("SELECT 1 FROM settings WHERE team_id = 'MO10' AND key = 'squad_players'")
        if not cur.fetchone():
            conn.execute(
                "INSERT INTO settings (team_id, key, value) VALUES (?, ?, ?)",
                ("MO10", "squad_players", json.dumps(settings.DEFAULT_SQUAD_PLAYERS))
            )
            
        # Trimmers (Adult roster of parents)
        cur = conn.execute("SELECT 1 FROM settings WHERE team_id = 'Trimmers' AND key = 'squad_players'")
        if not cur.fetchone():
            trimmers_roster = ["Rajeev", "Anchal", "Jatin", "Meenakshi", "Mustafa", "Michelle", "Marjolein", "Daniel", "Zeliha", "Dinesh", "Mine"]
            conn.execute(
                "INSERT INTO settings (team_id, key, value) VALUES (?, ?, ?)",
                ("Trimmers", "squad_players", json.dumps(trimmers_roster))
            )
            
        conn.commit()
