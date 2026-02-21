import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def get_user_performance_db_path(username: str) -> str:
    gui_dir = Path(__file__).resolve().parent
    user_dir = gui_dir / "users" / username
    user_dir.mkdir(parents=True, exist_ok=True)
    db_path = user_dir / "performance_history.db"

    if not db_path.exists():
        _initialize_performance_db(str(db_path))

    return str(db_path)


def _initialize_performance_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS power_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            peak_power REAL,
            average_power REAL,
            total_punches INTEGER,
            notes TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stamina_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            total_punches INTEGER,
            average_rate REAL,
            first_30_rate REAL,
            last_30_rate REAL,
            stamina_score INTEGER,
            fatigue_percentage REAL,
            duration INTEGER,
            notes TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reaction_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            reaction_time REAL,
            accuracy REAL,
            total_attempts INTEGER,
            successful_attempts INTEGER,
            notes TEXT
        )
    """
    )

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_power_time ON power_tests(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_stamina_time ON stamina_tests(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reaction_time ON reaction_tests(timestamp)")

    conn.commit()
    conn.close()


def save_power_result(username: str, peak_power: float, avg_power: float, total_punches: int):
    db_path = get_user_performance_db_path(username)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO power_tests (timestamp, peak_power, average_power, total_punches)
        VALUES (?, ?, ?, ?)
    """,
        (datetime.now().isoformat(), peak_power, avg_power, total_punches),
    )
    conn.commit()
    conn.close()


def save_stamina_result(username: str, results: Dict[str, Any]):
    db_path = get_user_performance_db_path(username)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO stamina_tests (
            timestamp, total_punches, average_rate, first_30_rate,
            last_30_rate, stamina_score, fatigue_percentage, duration
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            datetime.now().isoformat(),
            int(results.get("total_punches", 0)),
            float(results.get("average_rate", 0.0)),
            float(results.get("first_30_rate", 0.0)),
            float(results.get("last_30_rate", 0.0)),
            int(results.get("stamina_score", 0)),
            float(results.get("fatigue_percentage", 0.0)),
            int(results.get("duration", 120)),
        ),
    )
    conn.commit()
    conn.close()


def save_reaction_result(
    username: str,
    reaction_time: float,
    accuracy: float = 1.0,
    total_attempts: int = 1,
    successful_attempts: int = 1,
):
    db_path = get_user_performance_db_path(username)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO reaction_tests (timestamp, reaction_time, accuracy, total_attempts, successful_attempts)
        VALUES (?, ?, ?, ?, ?)
    """,
        (datetime.now().isoformat(), reaction_time, accuracy, total_attempts, successful_attempts),
    )
    conn.commit()
    conn.close()


def get_all_performance_history(username: str, limit: int = 50) -> List[Dict[str, Any]]:
    db_path = get_user_performance_db_path(username)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT timestamp, peak_power, average_power, total_punches, 'Power' AS test_type
        FROM power_tests
        ORDER BY timestamp DESC
        LIMIT ?
    """,
        (limit,),
    )
    power_tests = [dict(row) for row in cursor.fetchall()]

    cursor.execute(
        """
        SELECT timestamp, stamina_score, total_punches, average_rate, fatigue_percentage, 'Stamina' AS test_type
        FROM stamina_tests
        ORDER BY timestamp DESC
        LIMIT ?
    """,
        (limit,),
    )
    stamina_tests = [dict(row) for row in cursor.fetchall()]

    cursor.execute(
        """
        SELECT timestamp, reaction_time, accuracy, total_attempts, successful_attempts, 'Reaction' AS test_type
        FROM reaction_tests
        ORDER BY timestamp DESC
        LIMIT ?
    """,
        (limit,),
    )
    reaction_tests = [dict(row) for row in cursor.fetchall()]

    conn.close()

    all_tests: List[Dict[str, Any]] = []

    for test in power_tests:
        peak = float(test.get("peak_power") or 0.0)
        all_tests.append(
            {
                "timestamp": test["timestamp"],
                "test_type": "Power",
                "primary_value": peak,
                "display_value": f"{peak:.1f}g",
                "raw_data": test,
            }
        )

    for test in stamina_tests:
        punches = int(test.get("total_punches") or 0)
        score = int(test.get("stamina_score") or 0)
        all_tests.append(
            {
                "timestamp": test["timestamp"],
                "test_type": "Stamina",
                "primary_value": punches,
                "display_value": f"{punches} punches",
                "secondary_value": f"{score}/100",
                "raw_data": test,
            }
        )

    for test in reaction_tests:
        rt = float(test.get("reaction_time") or 0.0)
        all_tests.append(
            {
                "timestamp": test["timestamp"],
                "test_type": "Reaction",
                "primary_value": rt,
                "display_value": f"{rt:.3f}s",
                "raw_data": test,
            }
        )

    all_tests.sort(key=lambda x: x["timestamp"], reverse=True)
    return all_tests[:limit]


def get_latest_performance_summary(username: str) -> Dict[str, Dict[str, Any]]:
    db_path = get_user_performance_db_path(username)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    summary: Dict[str, Dict[str, Any]] = {}

    cursor.execute("SELECT peak_power FROM power_tests ORDER BY timestamp DESC LIMIT 1")
    latest_power = cursor.fetchone()
    cursor.execute("SELECT AVG(peak_power) FROM power_tests")
    avg_power = cursor.fetchone()[0]
    if latest_power and avg_power is not None:
        latest = float(latest_power[0])
        average = float(avg_power)
        diff = latest - average
        summary["power"] = {
            "latest": latest,
            "average": average,
            "difference": diff,
            "trend": "up" if diff > 0 else "down" if diff < 0 else "same",
        }

    cursor.execute("SELECT total_punches, stamina_score FROM stamina_tests ORDER BY timestamp DESC LIMIT 1")
    latest_stamina = cursor.fetchone()
    cursor.execute("SELECT AVG(total_punches) FROM stamina_tests")
    avg_stamina = cursor.fetchone()[0]
    if latest_stamina and avg_stamina is not None:
        latest = int(latest_stamina[0])
        latest_score = int(latest_stamina[1] or 0)
        average = float(avg_stamina)
        diff = latest - average
        summary["stamina"] = {
            "latest": latest,
            "latest_score": latest_score,
            "average": average,
            "difference": diff,
            "trend": "up" if diff > 0 else "down" if diff < 0 else "same",
        }

    cursor.execute("SELECT reaction_time FROM reaction_tests ORDER BY timestamp DESC LIMIT 1")
    latest_reaction = cursor.fetchone()
    cursor.execute("SELECT AVG(reaction_time) FROM reaction_tests")
    avg_reaction = cursor.fetchone()[0]
    if latest_reaction and avg_reaction is not None:
        latest = float(latest_reaction[0])
        average = float(avg_reaction)
        diff = average - latest
        summary["reaction"] = {
            "latest": latest,
            "average": average,
            "difference": diff,
            "trend": "up" if diff > 0 else "down" if diff < 0 else "same",
        }

    conn.close()
    return summary
