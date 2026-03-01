import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def get_user_sparring_db_path(username: str) -> str:
    """Return path to the user's performance_history.db, ensuring sparring tables exist."""
    gui_dir = Path(__file__).resolve().parent.parent
    user_dir = gui_dir / "users" / username
    user_dir.mkdir(parents=True, exist_ok=True)
    db_path = user_dir / "performance_history.db"

    _ensure_sparring_tables(str(db_path))

    return str(db_path)


def _ensure_sparring_tables(db_path: str) -> None:
    """Create sparring tables and indexes if they don't already exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sparring_sessions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp       TEXT    NOT NULL,
            style           TEXT    NOT NULL,
            total_rounds    INTEGER NOT NULL,
            round_duration  INTEGER NOT NULL,
            rest_duration   INTEGER NOT NULL,
            cv_raw_output   TEXT,
            punch_counts    TEXT,
            notes           TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sparring_weakness_profile (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            username         TEXT    NOT NULL UNIQUE,
            jab_freq         REAL    DEFAULT 0.0,
            cross_freq       REAL    DEFAULT 0.0,
            lead_hook_freq   REAL    DEFAULT 0.0,
            rear_hook_freq   REAL    DEFAULT 0.0,
            lead_upper_freq  REAL    DEFAULT 0.0,
            rear_upper_freq  REAL    DEFAULT 0.0,
            sessions_count   INTEGER DEFAULT 0,
            last_updated     TEXT
        )
    """
    )

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sparring_time ON sparring_sessions(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sparring_user ON sparring_weakness_profile(username)")

    conn.commit()
    conn.close()


def _parse_cv_output(cv_raw: str) -> Dict[str, int]:
    """Parse a comma-separated CV output string into a punch counts dictionary.

    Maps common variations:
        "hook"      -> "lead_hook"
        "uppercut"  -> "lead_upper"
    """
    if not cv_raw:
        return {}

    # Map common variations to canonical names
    variation_map = {
        "hook": "lead_hook",
        "uppercut": "lead_upper",
    }

    counts: Dict[str, int] = {}
    for punch in cv_raw.split(","):
        punch = punch.strip().lower()
        if not punch:
            continue
        punch = variation_map.get(punch, punch)
        counts[punch] = counts.get(punch, 0) + 1

    return counts


def save_sparring_session(
    username: str,
    style: str,
    total_rounds: int,
    round_duration: int,
    rest_duration: int,
    cv_raw_output: str,
) -> int:
    """Save a sparring session and return the new session row id."""
    db_path = get_user_sparring_db_path(username)
    punch_counts = _parse_cv_output(cv_raw_output)
    punch_counts_json = json.dumps(punch_counts)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO sparring_sessions (
            timestamp, style, total_rounds, round_duration,
            rest_duration, cv_raw_output, punch_counts
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            datetime.now().isoformat(),
            style,
            total_rounds,
            round_duration,
            rest_duration,
            cv_raw_output,
            punch_counts_json,
        ),
    )
    row_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return row_id


def update_weakness_profile(username: str, punch_counts: Dict[str, int]) -> None:
    """Update the rolling weakness profile for a user based on the latest session's punch counts.

    Converts punch counts to frequencies (normalised by total punches).
    If no profile exists yet, inserts with sessions_count = 1.
    If a profile exists, applies a rolling weighted average:
        alpha    = min(0.4, sessions_count * 0.05)
        new_freq = (1 - alpha) * old_freq + alpha * current_session_freq
    """
    total_punches = sum(punch_counts.values())
    if total_punches == 0:
        return

    # Normalise punch counts to frequencies for this session
    freq_keys = ["jab", "cross", "lead_hook", "rear_hook", "lead_upper", "rear_upper"]
    current_freqs: Dict[str, float] = {}
    for key in freq_keys:
        current_freqs[key] = punch_counts.get(key, 0) / total_punches

    db_path = get_user_sparring_db_path(username)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM sparring_weakness_profile WHERE username = ?",
        (username,),
    )
    existing = cursor.fetchone()

    if existing is None:
        # First session — insert directly
        cursor.execute(
            """
            INSERT INTO sparring_weakness_profile (
                username, jab_freq, cross_freq, lead_hook_freq,
                rear_hook_freq, lead_upper_freq, rear_upper_freq,
                sessions_count, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                username,
                current_freqs["jab"],
                current_freqs["cross"],
                current_freqs["lead_hook"],
                current_freqs["rear_hook"],
                current_freqs["lead_upper"],
                current_freqs["rear_upper"],
                1,
                datetime.now().isoformat(),
            ),
        )
    else:
        # Apply rolling weighted average
        sessions_count = int(existing["sessions_count"])
        alpha = min(0.4, sessions_count * 0.05)

        new_freqs: Dict[str, float] = {}
        for key in freq_keys:
            db_col = f"{key}_freq"
            old_val = float(existing[db_col])
            new_freqs[db_col] = (1 - alpha) * old_val + alpha * current_freqs[key]

        cursor.execute(
            """
            UPDATE sparring_weakness_profile
            SET jab_freq = ?, cross_freq = ?, lead_hook_freq = ?,
                rear_hook_freq = ?, lead_upper_freq = ?, rear_upper_freq = ?,
                sessions_count = ?, last_updated = ?
            WHERE username = ?
        """,
            (
                new_freqs["jab_freq"],
                new_freqs["cross_freq"],
                new_freqs["lead_hook_freq"],
                new_freqs["rear_hook_freq"],
                new_freqs["lead_upper_freq"],
                new_freqs["rear_upper_freq"],
                sessions_count + 1,
                datetime.now().isoformat(),
                username,
            ),
        )

    conn.commit()
    conn.close()


def get_weakness_profile(username: str) -> Dict[str, Any]:
    """Return the full weakness profile as a dict, or empty dict if none exists."""
    db_path = get_user_sparring_db_path(username)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM sparring_weakness_profile WHERE username = ?",
        (username,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {}

    return dict(row)


def get_sparring_history(username: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Return list of sparring session dicts, newest first."""
    db_path = get_user_sparring_db_path(username)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM sparring_sessions
        ORDER BY timestamp DESC
        LIMIT ?
    """,
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()

    sessions: List[Dict[str, Any]] = []
    for row in rows:
        session = dict(row)
        # Deserialise punch_counts JSON back to dict
        raw = session.get("punch_counts")
        if raw:
            session["punch_counts"] = json.loads(raw)
        else:
            session["punch_counts"] = {}
        sessions.append(session)

    return sessions
