import sqlite3
import json
import os
import logging
from typing import List, Dict, Any, Optional
from .config import settings

logger = logging.getLogger("database")

def get_db():
    database_url = settings.DATABASE_URL
    if database_url and (database_url.startswith("postgresql://") or database_url.startswith("postgres://")):
        try:
            import psycopg2
            import psycopg2.extras
            conn = psycopg2.connect(database_url, cursor_factory=psycopg2.extras.DictCursor)
            return conn
        except ImportError as e:
            logger.debug("psycopg2 not available: %s", e)

    conn = sqlite3.connect(settings.DATABASE_FILE, timeout=30.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA busy_timeout = 30000")
        conn.execute("PRAGMA journal_mode = WAL")
    except Exception as e:
        logger.debug("WAL mode could not be set: %s", e)
    return conn

def execute_query(conn, sql: str, params: tuple = ()):
    """Unified query execution supporting both SQLite (?) and PostgreSQL (%s) syntax."""
    is_postgres = not isinstance(conn, sqlite3.Connection)
    if is_postgres:
        sql = sql.replace("?", "%s")
        sql = sql.replace("INSERT OR REPLACE INTO", "INSERT INTO")
    
    cur = conn.cursor()
    cur.execute(sql, params)
    return cur

def upsert_setting(conn, team_id: str, key: str, value: str):
    """Upsert setting key-value pair across SQLite and PostgreSQL."""
    is_postgres = not isinstance(conn, sqlite3.Connection)
    if is_postgres:
        sql = """
            INSERT INTO settings (team_id, key, value) VALUES (%s, %s, %s)
            ON CONFLICT (team_id, key) DO UPDATE SET value = EXCLUDED.value
        """
        cur = conn.cursor()
        cur.execute(sql, (team_id, key, value))
    else:
        sql = "INSERT OR REPLACE INTO settings (team_id, key, value) VALUES (?, ?, ?)"
        cur = conn.cursor()
        cur.execute(sql, (team_id, key, value))

def init_db():
    conn = get_db()
    is_postgres = not isinstance(conn, sqlite3.Connection)
    try:
        if not is_postgres:
            # SQLite non-destructive migration checks
            cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings'")
            if cur.fetchone():
                cur_info = conn.execute("PRAGMA table_info(settings)")
                cols = [row["name"] for row in cur_info.fetchall()]
                if "team_id" not in cols:
                    conn.execute("ALTER TABLE settings ADD COLUMN team_id TEXT DEFAULT 'MO10'")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    team_id TEXT,
                    key TEXT,
                    value TEXT,
                    PRIMARY KEY (team_id, key)
                )
            """)

            cur_tactics = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tactics'")
            if cur_tactics.fetchone():
                cur_info = conn.execute("PRAGMA table_info(tactics)")
                cols = [row["name"] for row in cur_info.fetchall()]
                if "title" not in cols:
                    conn.execute("ALTER TABLE tactics ADD COLUMN title TEXT DEFAULT ''")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS tactics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_id TEXT,
                    match_date TEXT,
                    opponent TEXT,
                    quarter TEXT,
                    title TEXT,
                    data TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_tactics_period_team 
                ON tactics(team_id, match_date, opponent, quarter)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS access_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_email TEXT,
                    user_name TEXT,
                    team_id TEXT,
                    requested_role TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Data migration: Clean old drawn arrows from saved tactic payloads
            cur = conn.execute("SELECT id, data FROM tactics")
            rows = cur.fetchall()
            for r in rows:
                if r["data"]:
                    try:
                        d = json.loads(r["data"])
                        if "drawings" in d and len(d["drawings"]) > 0:
                            d["drawings"] = []
                            conn.execute("UPDATE tactics SET data = ? WHERE id = ?", (json.dumps(d), r["id"]))
                    except Exception as e:
                        logger.debug("Tactic drawing data migration skipped for id %s: %s", r["id"], e)
        else:
            # PostgreSQL table initialization
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    team_id TEXT,
                    key TEXT,
                    value TEXT,
                    PRIMARY KEY (team_id, key)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tactics (
                    id SERIAL PRIMARY KEY,
                    team_id TEXT,
                    match_date TEXT,
                    opponent TEXT,
                    quarter TEXT,
                    title TEXT,
                    data TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_tactics_period_team 
                ON tactics(team_id, match_date, opponent, quarter)
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS access_requests (
                    id SERIAL PRIMARY KEY,
                    user_email TEXT,
                    user_name TEXT,
                    team_id TEXT,
                    requested_role TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

        # Seed initial teams dynamically if database is empty
        cur_teams = execute_query(conn, "SELECT DISTINCT team_id FROM settings").fetchall()
        existing_teams = [r["team_id"] for r in cur_teams]

        initial_teams = ["MO10", "Trimmers"]
        for team in initial_teams:
            # Seed coach emails
            cur = execute_query(conn, "SELECT 1 FROM settings WHERE team_id = ? AND key = 'coach_emails'", (team,))
            if not cur.fetchone():
                upsert_setting(conn, team, "coach_emails", json.dumps(settings.DEFAULT_COACH_EMAILS))
            
            # Seed Google client ID
            cur = execute_query(conn, "SELECT 1 FROM settings WHERE team_id = ? AND key = 'google_client_id'", (team,))
            if not cur.fetchone():
                upsert_setting(conn, team, "google_client_id", settings.DEFAULT_GOOGLE_CLIENT_ID)

            # Seed custom positions
            cur = execute_query(conn, "SELECT 1 FROM settings WHERE team_id = ? AND key = 'custom_positions'", (team,))
            if not cur.fetchone():
                upsert_setting(conn, team, "custom_positions", json.dumps({}))

            # Seed custom situations
            cur = execute_query(conn, "SELECT 1 FROM settings WHERE team_id = ? AND key = 'custom_situations'", (team,))
            if not cur.fetchone():
                upsert_setting(conn, team, "custom_situations", json.dumps({}))

            # Seed custom sub roles
            cur = execute_query(conn, "SELECT 1 FROM settings WHERE team_id = ? AND key = 'custom_sub_roles'", (team,))
            if not cur.fetchone():
                upsert_setting(conn, team, "custom_sub_roles", json.dumps({}))

        # Seed squad players specifically and sanitize cross-team contamination if present
        cur_mo10 = execute_query(conn, "SELECT value FROM settings WHERE team_id = 'MO10' AND key = 'squad_players'").fetchone()
        if not cur_mo10:
            upsert_setting(conn, "MO10", "squad_players", json.dumps(settings.DEFAULT_SQUAD_PLAYERS))
        else:
            val_mo10_str = cur_mo10["value"]
            if "Sander Duivesteijn" in val_mo10_str or "Rajeev Singhal" in val_mo10_str:
                upsert_setting(conn, "MO10", "squad_players", json.dumps(settings.DEFAULT_SQUAD_PLAYERS))
            elif "Ayana" not in val_mo10_str:
                try:
                    players = json.loads(val_mo10_str)
                    if isinstance(players, list) and not any("ayana" in (p if isinstance(p, str) else p.get("name", "")).lower() for p in players):
                        players.append("Ayana")
                        upsert_setting(conn, "MO10", "squad_players", json.dumps(players))
                except Exception as e:
                    logger.debug(f"Failed to migrate squad players for Ayana: {e}")

        cur_trimmers = execute_query(conn, "SELECT value FROM settings WHERE team_id = 'Trimmers' AND key = 'squad_players'").fetchone()
        if not cur_trimmers:
            upsert_setting(conn, "Trimmers", "squad_players", json.dumps(settings.DEFAULT_TRIMMERS_SQUAD_PLAYERS))
        else:
            val_trim_str = cur_trimmers["value"]
            if "Sai Jiya" in val_trim_str or "Defne" in val_trim_str or "Shanaya" in val_trim_str:
                upsert_setting(conn, "Trimmers", "squad_players", json.dumps(settings.DEFAULT_TRIMMERS_SQUAD_PLAYERS))

        conn.commit()
    finally:
        conn.close()


