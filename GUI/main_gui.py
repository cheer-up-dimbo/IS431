import sys
import json
import csv
import os
import hashlib
import sqlite3
from pathlib import Path
from functools import partial
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Set
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, 
                               QStackedWidget, QGridLayout, QSizePolicy, QHBoxLayout,
                               QLineEdit, QMessageBox, QScrollArea, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QAbstractItemView, QTextEdit,
                               QComboBox, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QObject, QEvent
from PySide6.QtGui import QTextCursor, QKeyEvent, QCloseEvent, QColor

try:
    import serial
    from serial.tools import list_ports
except Exception:
    serial = None
    list_ports = None

import random
import time
from datetime import datetime
from power import power_runner
from reaction_time import reaction_time_runner as rt_runner
from stamina.stamina_runner import StaminaRunner, USE_ARDUINO
from combo_curriculum import ComboCurriculum
from placeholders import format_feedback_data, get_performance_score
from sparring.spar_pages import (
    SparStyleSelectPage,
    SparRoundConfigPage,
    SparCountdownPage,
    SparSessionPage,
    SparRestPage,
    SparProcessingPage,
    SparResultPage,
)

# Import from new compartmentalized modules
from core import TrainingConfig, AppState, PageIndex, ButtonStyle
from utils import (
    get_users_csv_path, hash_password, load_users, save_users,
    get_user_level, set_user_level, get_user_progress, update_user_progress,
    calculate_user_progress_from_combos, get_training_csv_path
)

GUI_DIR = os.path.dirname(__file__)
SHARED_DB_PATH = os.path.join(GUI_DIR, 'data', 'combos.db')
GUI_ENV_PATH = os.path.join(GUI_DIR, ".env")


def _load_env_file(path: str):
    """Load KEY=VALUE pairs from a simple .env file into os.environ."""
    if not os.path.exists(path):
        return

    try:
        with open(path, "r", encoding="utf-8") as env_file:
            for raw_line in env_file:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key:
                    os.environ.setdefault(key, value)
    except Exception as e:
        print(f"WARNING: Failed to load env file {path}: {e}")


def _set_env_key(path: str, key: str, value: str):
    """Set or append KEY=VALUE in a simple .env file and runtime env."""
    normalized_line = f"{key}={value}"
    lines: List[str] = []

    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as env_file:
                lines = env_file.read().splitlines()
        except Exception:
            lines = []

    updated = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(f"{key}="):
            lines[index] = normalized_line
            updated = True
            break

    if not updated:
        lines.append(normalized_line)

    with open(path, "w", encoding="utf-8") as env_file:
        env_file.write("\n".join(lines).strip() + "\n")

    os.environ[key] = value


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except Exception:
        return default


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except Exception:
        return default


_load_env_file(os.path.join(os.path.dirname(GUI_DIR), ".env"))
_load_env_file(os.path.join(GUI_DIR, ".env"))


def _widget_navigate_to(self, page_index: int):
    """Shared navigation helper for page widgets.

    Delegates to MainWindow.navigate_to when available; otherwise falls back
    to direct stacked widget navigation.
    """
    main_window = self.window()
    if hasattr(main_window, "navigate_to"):
        main_window.navigate_to(page_index)
    elif hasattr(self, "stacked_widget") and self.stacked_widget is not None:
        self.stacked_widget.setCurrentIndex(page_index)


if not hasattr(QWidget, "navigate_to"):
    QWidget.navigate_to = _widget_navigate_to


def _initialize_user_combo_database(user_db_path: Path) -> bool:
    """Create and populate a user's combo database if missing."""
    try:
        import importlib.util

        setup_script_path = Path(GUI_DIR) / 'setup' / 'setup_combo_database.py'
        if not setup_script_path.exists():
            print(f"WARNING: Setup script not found at {setup_script_path}")
            return False

        spec = importlib.util.spec_from_file_location("setup_combo_database", str(setup_script_path))
        if not spec or not spec.loader:
            print("WARNING: Unable to load setup_combo_database module")
            return False

        setup_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(setup_module)

        setup_module.create_schema(str(user_db_path))
        setup_module.populate_combos(str(user_db_path))
        success, result = setup_module.verify_database(str(user_db_path))
        if not success:
            print(f"WARNING: User DB verification failed: {result}")
            return False

        return True
    except Exception as e:
        print(f"WARNING: Failed to initialize user combo database at {user_db_path}: {e}")
        return False


def get_user_db_path(username: str) -> str:
    """Get a user-specific combos DB path and initialize it on first use."""
    if not username:
        print("WARNING: No username provided, using shared DB")
        return SHARED_DB_PATH

    user_dir = Path(GUI_DIR) / 'users' / username
    user_dir.mkdir(parents=True, exist_ok=True)
    user_db_path = user_dir / 'combos.db'

    if not user_db_path.exists():
        print(f"Creating fresh combo database for user: {username}")
        initialized = _initialize_user_combo_database(user_db_path)
        if initialized:
            print(f"✓ Initialized database at: {user_db_path}")
        else:
            print("WARNING: Falling back to shared DB due to initialization failure")
            return SHARED_DB_PATH

    return str(user_db_path)


DB_PATH = SHARED_DB_PATH


class ArduinoButtonListener(QThread):
    """Background serial listener for physical navigation buttons."""

    button_pressed = Signal(str)
    status = Signal(str)

    def __init__(
        self,
        port: Optional[str] = None,
        baudrate: int = 115200,
        debounce_ms: int = 120,
        serial_timeout_s: float = 0.05,
        startup_delay_s: float = 1.2,
        reconnect_interval_s: float = 2.0,
        parent: Optional[QObject] = None,
    ):
        super().__init__(parent)
        self.port = port or os.getenv("ARDUINO_BUTTON_PORT", "")
        self.baudrate = baudrate
        self.debounce_ms = debounce_ms
        self.serial_timeout_s = serial_timeout_s
        self.startup_delay_s = startup_delay_s
        self.reconnect_interval_s = reconnect_interval_s
        self._running = True
        self._ser = None
        self._last_emit_ms: Dict[str, int] = {}
        self._last_status_msg: str = ""
        self._last_status_ts: float = 0.0

    def stop(self):
        self._running = False

    def _emit_status_throttled(self, message: str, min_interval_s: float = 2.0):
        now = time.time()
        if message != self._last_status_msg or (now - self._last_status_ts) >= min_interval_s:
            self.status.emit(message)
            self._last_status_msg = message
            self._last_status_ts = now

    def _resolve_port(self) -> Optional[str]:
        if self.port:
            return self.port
        if list_ports is None:
            return None
        for candidate in list_ports.comports():
            desc = (candidate.description or "").lower()
            if "arduino" in desc or "ch340" in desc or "usb serial" in desc:
                return candidate.device
        return None

    def _connect(self) -> bool:
        if serial is None:
            self._emit_status_throttled("pyserial not installed - Arduino button input disabled", min_interval_s=10.0)
            return False

        port = self._resolve_port()
        if not port:
            self._emit_status_throttled("No Arduino serial port detected", min_interval_s=5.0)
            return False

        try:
            self._ser = serial.Serial(port, self.baudrate, timeout=self.serial_timeout_s)
            self._ser.reset_input_buffer()
            self._ser.reset_output_buffer()
            if self.startup_delay_s > 0:
                time.sleep(self.startup_delay_s)
                self._ser.reset_input_buffer()
            self._emit_status_throttled(f"Arduino buttons connected on {port} @ {self.baudrate}", min_interval_s=0.0)
            return True
        except Exception as e:
            self._emit_status_throttled(f"Arduino connect failed on {port}: {e}", min_interval_s=3.0)
            self._ser = None
            return False

    def _close_serial(self):
        try:
            if self._ser and self._ser.is_open:
                self._ser.close()
        except Exception:
            pass
        finally:
            self._ser = None

    def run(self):
        command_aliases = {
            "BTN1_PRESS": "BTN1_PRESS",
            "BTN2_PRESS": "BTN2_PRESS",
            "BTN3_PRESS": "BTN3_PRESS",
            "BTN1": "BTN1_PRESS",
            "BTN2": "BTN2_PRESS",
            "BTN3": "BTN3_PRESS",
        }

        while self._running:
            if self._ser is None or not self._ser.is_open:
                if not self._connect():
                    self.msleep(int(self.reconnect_interval_s * 1000))
                    continue

            try:
                raw_line = self._ser.readline()
                if not raw_line:
                    continue

                cmd_raw = raw_line.decode("utf-8", errors="ignore").replace("\x00", "").strip().upper()
                cmd = command_aliases.get(cmd_raw)
                if not cmd:
                    continue

                now_ms = int(time.time() * 1000)
                last_ms = self._last_emit_ms.get(cmd, 0)
                if now_ms - last_ms < self.debounce_ms:
                    continue

                self._last_emit_ms[cmd] = now_ms
                self.button_pressed.emit(cmd)
            except Exception as e:
                self._emit_status_throttled(f"Arduino read error: {e}", min_interval_s=3.0)
                self._close_serial()
                self.msleep(int(self.reconnect_interval_s * 1000))

        self._close_serial()



# ============================================================================
# Page Classes
# ============================================================================

class ButtonNavigationMixin:
    """Provides consistent button styling and keyboard navigation."""

    BUTTON_STYLE = """
        QPushButton {
            font-size: 20px;
            padding: 20px;
            background-color: #f5f5f5;
            border: 3px solid #cccccc;
            border-radius: 10px;
            min-width: 360px;
            max-width: 420px;
            min-height: 65px;
            color: #111111;
        }
        QPushButton:focus {
            border: 6px solid #00ff00;
            background-color: #2d5016;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e8e8e8;
        }
    """

    def setup_navigation(self, buttons: List[QPushButton]):
        nav_buttons = [button for button in buttons if isinstance(button, QPushButton)]
        self._nav_buttons = nav_buttons
        self._focused_button_index = 0
        nav_style = getattr(self, "NAV_BUTTON_STYLE", self.BUTTON_STYLE)
        nav_autosize = getattr(self, "NAV_BUTTON_AUTOSIZE", False)
        nav_min_width = getattr(self, "NAV_BUTTON_MIN_WIDTH", 360)
        nav_max_width = getattr(self, "NAV_BUTTON_MAX_WIDTH", 420)
        nav_min_height = getattr(self, "NAV_BUTTON_MIN_HEIGHT", 65)

        if not nav_buttons:
            return

        if hasattr(self, "setFocusPolicy"):
            self.setFocusPolicy(Qt.StrongFocus)

        for button in nav_buttons:
            button.setFocusPolicy(Qt.StrongFocus)
            button.setStyleSheet(nav_style)

            if nav_autosize:
                button.setMinimumWidth(nav_min_width)
                button.setMaximumWidth(16777215)
                button.setMinimumHeight(nav_min_height)
                button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            else:
                button.setMinimumWidth(nav_min_width)
                button.setMaximumWidth(nav_max_width)
                button.setMinimumHeight(nav_min_height)
                button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            parent_widget = button.parentWidget()
            parent_layout = parent_widget.layout() if parent_widget is not None else None
            if parent_layout is not None:
                parent_layout.setAlignment(button, Qt.AlignHCenter)

            button.installEventFilter(self)

        QTimer.singleShot(0, lambda: self._set_focus_index(0))

    def _set_focus_index(self, index: int):
        if not getattr(self, "_nav_buttons", None):
            return
        self._focused_button_index = index % len(self._nav_buttons)
        self._nav_buttons[self._focused_button_index].setFocus(Qt.TabFocusReason)
        self._update_focus_glow()

    def _move_focus(self, step: int):
        self._set_focus_index(self._focused_button_index + step)

    def _activate_focused_button(self):
        if not getattr(self, "_nav_buttons", None):
            return
        self._nav_buttons[self._focused_button_index].click()

    def _update_focus_glow(self):
        if not getattr(self, "_nav_buttons", None):
            return
        for idx, button in enumerate(self._nav_buttons):
            if idx == self._focused_button_index:
                glow = QGraphicsDropShadowEffect(self)
                glow.setBlurRadius(36)
                glow.setColor(QColor(0, 255, 0, 230))
                glow.setOffset(0, 0)
                button.setGraphicsEffect(glow)
            else:
                button.setGraphicsEffect(None)

    def eventFilter(self, obj, event):
        nav_buttons = getattr(self, "_nav_buttons", [])
        if obj in nav_buttons:
            idx = nav_buttons.index(obj)
            if event.type() == QEvent.FocusIn:
                self._focused_button_index = idx
                self._update_focus_glow()
                return False
            if event.type() == QEvent.KeyPress:
                key = event.key()
                if key == Qt.Key_Up:
                    self._move_focus(-1)
                    return True
                if key == Qt.Key_Down:
                    self._move_focus(1)
                    return True
                if key in (Qt.Key_Return, Qt.Key_Enter):
                    self._activate_focused_button()
                    return True

        parent_event_filter = getattr(super(), "eventFilter", None)
        if callable(parent_event_filter):
            return parent_event_filter(obj, event)
        return False

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            self._move_focus(-1)
            event.accept()
            return
        if key == Qt.Key_Down:
            self._move_focus(1)
            event.accept()
            return
        if key in (Qt.Key_Return, Qt.Key_Enter):
            self._activate_focused_button()
            event.accept()
            return
        super_key_press = getattr(super(), "keyPressEvent", None)
        if callable(super_key_press):
            super_key_press(event)

    def handle_arduino_up(self) -> bool:
        if not getattr(self, "_nav_buttons", None):
            return False
        self._move_focus(-1)
        return True

    def handle_arduino_down(self) -> bool:
        if not getattr(self, "_nav_buttons", None):
            return False
        self._move_focus(1)
        return True

    def handle_arduino_enter(self) -> bool:
        if not getattr(self, "_nav_buttons", None):
            return False
        self._activate_focused_button()
        return True


PARAMETER_SELECTION_BUTTON_STYLE = """
    QPushButton {
        font-size: 17px;
        padding: 10px 20px;
        background-color: #f5f5f5;
        border: 3px solid #cccccc;
        border-radius: 10px;
        min-width: 280px;
        min-height: 55px;
        color: #111111;
    }
    QPushButton:focus {
        border: 6px solid #00ff00;
        background-color: #2d5016;
        color: white;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #e8e8e8;
    }
"""

def get_users_csv_path():
    """Get the path to the users CSV file."""
    return os.path.join(os.path.dirname(__file__), "users.csv")


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> dict:
    """Load users from CSV file. Returns dict of {username: {"password_hash": ..., "level": ..., "progress": ...}}."""
    users = {}
    csv_path = get_users_csv_path()
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    users[row['username']] = {
                        'password_hash': row['password_hash'],
                        'level': row.get('level', 'Beginner'),
                        'progress': float(row.get('progress', '0.0'))
                    }
        except Exception as e:
            print(f"Error loading users: {e}")
    return users


def save_users(users: dict) -> bool:
    """Save users dict to CSV file. Returns True on success."""
    csv_path = get_users_csv_path()
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['username', 'password_hash', 'level', 'progress'])
            writer.writeheader()
            for username, user_data in users.items():
                if isinstance(user_data, dict):
                    writer.writerow({
                        'username': username,
                        'password_hash': user_data['password_hash'],
                        'level': user_data.get('level', 'Beginner'),
                        'progress': user_data.get('progress', 0.0)
                    })
                else:
                    # Backward compatibility for old format
                    writer.writerow({
                        'username': username,
                        'password_hash': user_data,
                        'level': 'Beginner',
                        'progress': 0.0
                    })
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False


def get_user_level(username: str) -> str:
    """Get the current level of a user. Returns 'Beginner', 'Intermediate', or 'Advanced'."""
    users = load_users()
    if username in users:
        user_data = users[username]
        if isinstance(user_data, dict):
            return user_data.get('level', 'Beginner')
        return 'Beginner'
    return 'Beginner'


def set_user_level(username: str, level: str) -> bool:
    """Set the level of a user. Returns True on success."""
    if level not in ['Beginner', 'Intermediate', 'Advanced']:
        print(f"Invalid level: {level}")
        return False
    users = load_users()
    if username in users:
        users[username]['level'] = level
        return save_users(users)
    return False


def get_user_progress(username: str) -> float:
    """Get the current progress percentage of a user (0.0-100.0)."""
    users = load_users()
    if username in users:
        user_data = users[username]
        if isinstance(user_data, dict):
            return user_data.get('progress', 0.0)
        return 0.0
    return 0.0


def update_user_progress(username: str, progress: float) -> bool:
    """
    Update user's progress percentage and auto-level up if thresholds met.
    
    Progress thresholds:
    - Beginner -> Intermediate: 80% progress at Beginner level
    - Intermediate -> Advanced: 80% progress at Intermediate level
    
    Args:
        username: Username to update
        progress: Progress percentage (0.0-100.0)
    
    Returns:
        bool: True on success
    """
    users = load_users()
    if username not in users:
        return False
    
    # Clamp progress to 0-100
    progress = max(0.0, min(100.0, progress))
    
    current_level = users[username].get('level', 'Beginner')
    users[username]['progress'] = progress
    
    # Auto level-up logic
    if current_level == 'Beginner' and progress >= 80.0:
        users[username]['level'] = 'Intermediate'
        users[username]['progress'] = 0.0  # Reset progress for new level
        print(f"User {username} leveled up to Intermediate!")
    elif current_level == 'Intermediate' and progress >= 80.0:
        users[username]['level'] = 'Advanced'
        users[username]['progress'] = 0.0  # Reset progress for new level
        print(f"User {username} leveled up to Advanced!")
    
    return save_users(users)


def calculate_user_progress_from_combos(username: str, db_path: str) -> float:
    """
    Calculate user's progress based on combo mastery from database.
    
    Progress = (Average mastery score of all combos at current level) * 100
    
    Args:
        username: Username to calculate progress for
        db_path: Path to combos.db database
    
    Returns:
        float: Progress percentage (0.0-100.0)
    """
    try:
        import sys
        import os
        # Add combo_curriculum to path if not already there
        curriculum_path = os.path.join(os.path.dirname(__file__), 'combo_curriculum')
        if curriculum_path not in sys.path:
            sys.path.insert(0, curriculum_path)
        
        from combo_curriculum import ComboCurriculum
        
        # Get user's current level
        level = get_user_level(username)
        
        # Query combos at that level
        with ComboCurriculum(db_path) as curriculum:
            combos = curriculum.get_combos_by_difficulty(level)
            
            if not combos:
                return 0.0
            
            # Calculate average mastery score
            total_mastery = sum(combo.get('mastery_score', 0.0) for combo in combos)
            avg_mastery = total_mastery / len(combos)
            
            # Convert to percentage (mastery_score is 0.0-1.0)
            progress = avg_mastery * 100.0
            
            return progress
    
    except Exception as e:
        print(f"Error calculating progress from combos: {e}")
        return 0.0


def get_training_csv_path(username: str):
    """Get the path to a user's training history CSV file."""
    gui_dir = os.path.dirname(__file__)
    training_dir = os.path.join(gui_dir, "training_history")
    os.makedirs(training_dir, exist_ok=True)

    new_path = os.path.join(training_dir, f"training_{username}.csv")
    legacy_path = os.path.join(gui_dir, f"training_{username}.csv")

    # Migrate old files from GUI root to dedicated folder on first access.
    if os.path.exists(legacy_path) and not os.path.exists(new_path):
        try:
            os.replace(legacy_path, new_path)
        except Exception as e:
            print(f"Error migrating training CSV for user {username}: {e}")

    return new_path


class LoginPage(ButtonNavigationMixin, QWidget):
    """Login/Signup page shown on application startup."""

    NAV_BUTTON_AUTOSIZE = True
    NAV_BUTTON_MIN_WIDTH = 280
    NAV_BUTTON_MIN_HEIGHT = 70
    NAV_BUTTON_STYLE = """
        QPushButton {
            font-size: 20px;
            padding: 15px 30px;
            background-color: #f5f5f5;
            border: 3px solid #cccccc;
            border-radius: 10px;
            min-width: 280px;
            min-height: 70px;
            color: #111111;
        }
        QPushButton:focus {
            border: 6px solid #00ff00;
            background-color: #2d5016;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e8e8e8;
        }
    """
    
    def __init__(self, stacked_widget, app_state):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        self.current_user = None
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(60, 40, 60, 40)
        
        # Title
        title = QLabel("Boxing Training App")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        title.setFixedHeight(50)

        
        # Username field
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        username_label.setFixedHeight(25)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFixedHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 8px;
                min-width: 350px;
                background-color: white;
                color: black;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        password_label.setFixedHeight(25)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 8px;
                min-width: 350px;
                background-color: white;
                color: black;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        
        # Status label for error messages
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
        self.status_label.setFixedHeight(20)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        login_btn = QPushButton("Login")
        signup_btn = QPushButton("Sign Up")
        manage_users_btn = QPushButton("Manage Users")
        
        login_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        signup_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        manage_users_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        
        login_btn.setMinimumHeight(70)
        signup_btn.setMinimumHeight(70)
        manage_users_btn.setMinimumHeight(70)
        login_btn.setMinimumWidth(280)
        signup_btn.setMinimumWidth(280)
        manage_users_btn.setMinimumWidth(280)
        login_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        signup_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        manage_users_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        login_btn.clicked.connect(self.on_login)
        signup_btn.clicked.connect(self.on_signup)
        manage_users_btn.clicked.connect(self.on_manage_users)
        
        # Enable login on Enter key press
        self.password_input.returnPressed.connect(self.on_login)
        self.username_input.returnPressed.connect(lambda: self.password_input.setFocus())
        
        button_layout.addStretch()
        button_layout.addWidget(login_btn)
        button_layout.addWidget(signup_btn)
        button_layout.addStretch()
        
        # Layout assembly - compact spacing
        layout.addStretch(1)
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addSpacing(15)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addSpacing(5)
        layout.addWidget(self.status_label)
        layout.addSpacing(15)
        layout.addLayout(button_layout)
        layout.addSpacing(10)
        layout.addWidget(manage_users_btn, alignment=Qt.AlignCenter)
        layout.addStretch(1)
        
        self.setLayout(layout)
    
    def on_login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.status_label.setText("Please enter both username and password")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        users = load_users()
        password_hash = hash_password(password)
        
        if username in users and isinstance(users[username], dict) and users[username]['password_hash'] == password_hash:
            self.current_user = username
            self.status_label.setText(f"Welcome back, {username}!")
            self.status_label.setStyleSheet("font-size: 14px; color: #4CAF50;")
            # Clear inputs
            self.username_input.clear()
            self.password_input.clear()
            # Navigate to homepage
            QTimer.singleShot(500, lambda: self.navigate_to(PageIndex.HOMEPAGE))
        else:
            self.status_label.setText("Invalid username or password")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
    
    def on_signup(self):
        """Handle signup button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.status_label.setText("Please enter both username and password")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        if len(username) < 3:
            self.status_label.setText("Username must be at least 3 characters")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        if len(password) < 4:
            self.status_label.setText("Password must be at least 4 characters")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        users = load_users()
        
        if username in users:
            self.status_label.setText("Username already exists")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        # Add new user with Beginner level and 0% progress
        users[username] = {
            'password_hash': hash_password(password),
            'level': 'Beginner',
            'progress': 0.0
        }
        if save_users(users):
            self.current_user = username
            self.status_label.setText(f"Account created! Welcome, {username}!")
            self.status_label.setStyleSheet("font-size: 14px; color: #4CAF50;")
            # Clear inputs
            self.username_input.clear()
            self.password_input.clear()
            # Navigate to homepage
            QTimer.singleShot(500, lambda: self.navigate_to(PageIndex.HOMEPAGE))
        else:
            self.status_label.setText("Error creating account. Please try again.")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
    
    def on_manage_users(self):
        """Navigate to user management page."""
        self.navigate_to(PageIndex.USER_MANAGEMENT)
    
    def get_current_user(self):
        """Return the currently logged in user."""
        return self.current_user


class UserManagementPage(ButtonNavigationMixin, QWidget):
    """Page to view and delete users."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 30, 50, 30)
        
        # Title
        title = QLabel("User Management")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px; color: white;")
        
        # User table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(["Username", "Level", "Progress", "Training Sessions", "Combo Progress", "Delete"])
        self.user_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.user_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.user_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.user_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.user_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.user_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.user_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.user_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.user_table.setStyleSheet("""
            QTableWidget {
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: white;
                color: black;
            }
            QTableWidget::item {
                padding: 10px;
                color: black;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
        """)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        refresh_btn = QPushButton("Refresh")
        back_btn = QPushButton("Back to Login")
        
        refresh_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        back_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        
        refresh_btn.setFixedSize(200, 50)
        back_btn.setFixedSize(200, 50)
        
        refresh_btn.clicked.connect(self.refresh_users)
        back_btn.clicked.connect(self.on_back)
        
        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        
        # Layout assembly
        layout.addWidget(title)
        layout.addWidget(self.user_table)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def showEvent(self, event):
        """Refresh user list when page is shown."""
        super().showEvent(event)
        self.refresh_users()
    
    def refresh_users(self):
        """Load and display all users."""
        users = load_users()
        self.user_table.setRowCount(len(users))
        for row, username in enumerate(users.keys()):
            # Username
            username_item = QTableWidgetItem(username)
            username_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 0, username_item)

            # Level
            user_data = users[username]
            level = user_data.get('level', 'Beginner') if isinstance(user_data, dict) else 'Beginner'
            level_item = QTableWidgetItem(level)
            level_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 1, level_item)

            # Progress
            progress = user_data.get('progress', 0.0) if isinstance(user_data, dict) else 0.0
            progress_item = QTableWidgetItem(f"{progress:.1f}%")
            progress_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 2, progress_item)

            # Training sessions count (aligned to per-user combo attempts)
            session_count = 0
            try:
                user_db_path = get_user_db_path(username)
                with sqlite3.connect(user_db_path) as conn:
                    result = conn.execute(
                        "SELECT COALESCE(SUM(total_attempts), 0) FROM combos"
                    ).fetchone()
                    session_count = int(result[0] or 0) if result else 0
            except Exception as e:
                print(f"Error reading attempts for user {username}: {e}")
            sessions_item = QTableWidgetItem(str(session_count))
            sessions_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 3, sessions_item)
            
            # View Combo Progress button
            view_combo_btn = QPushButton("View Combos")
            view_combo_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            view_combo_btn.clicked.connect(partial(self.view_user_combos, username))
            self.user_table.setCellWidget(row, 4, view_combo_btn)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
                QPushButton:pressed {
                    background-color: #c41504;
                }
            """)
            delete_btn.clicked.connect(partial(self.delete_user, username))
            self.user_table.setCellWidget(row, 5, delete_btn)
        
        self.user_table.resizeRowsToContents()
    
    def delete_user(self, username: str):
        """Delete a user after confirmation."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete user '{username}'?\nThis will also delete their training history.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            users = load_users()
            if username in users:
                del users[username]
                if save_users(users):
                    # Delete user's training file if exists
                    training_csv = get_training_csv_path(username)
                    if os.path.exists(training_csv):
                        try:
                            os.remove(training_csv)
                        except:
                            pass
                    QMessageBox.information(self, "Success", f"User '{username}' deleted successfully.")
                    self.refresh_users()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete user.")
    
    def view_user_combos(self, username: str):
        """Navigate to user combo progress page."""
        # Find and update the UserComboProgressPage with the selected user
        for i in range(self.stacked_widget.count()):
            page = self.stacked_widget.widget(i)
            if hasattr(page, '__class__') and page.__class__.__name__ == 'UserComboProgressPage':
                page.set_user(username, return_to_page=PageIndex.USER_MANAGEMENT)
                self.stacked_widget.setCurrentIndex(i)
                break
    
    def on_back(self):
        """Return to login page."""
        self.navigate_to(PageIndex.LOGIN)


class Homepage(ButtonNavigationMixin, QWidget):
    NAV_BUTTON_AUTOSIZE = True
    NAV_BUTTON_MIN_WIDTH = 320
    NAV_BUTTON_MIN_HEIGHT = 65
    NAV_BUTTON_STYLE = """
        QPushButton {
            font-size: 18px;
            padding: 12px 20px;
            background-color: #f5f5f5;
            border: 3px solid #cccccc;
            border-radius: 10px;
            min-width: 320px;
            min-height: 65px;
            color: #111111;
        }
        QPushButton:focus {
            border: 6px solid #00ff00;
            background-color: #2d5016;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e8e8e8;
        }
    """

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        title = QLabel("Homepage")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        training_btn = QPushButton("Training")
        performance_btn = QPushButton("Performance")
        combo_progress_btn = QPushButton("Combo Progress")
        others_btn = QPushButton("Others")
        back_btn = QPushButton("Back to Login")

        training_btn.setStyleSheet(ButtonStyle.HOME_LARGE)
        performance_btn.setStyleSheet(ButtonStyle.HOME_LARGE)
        combo_progress_btn.setStyleSheet(ButtonStyle.HOME_LARGE)
        others_btn.setStyleSheet(ButtonStyle.HOME_LARGE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        training_btn.clicked.connect(self.on_training_clicked)
        performance_btn.clicked.connect(self.on_performance_clicked)
        combo_progress_btn.clicked.connect(self.on_combo_progress_clicked)
        others_btn.clicked.connect(self.on_others_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(training_btn)
        layout.addStretch()
        layout.addWidget(performance_btn)
        layout.addStretch()
        layout.addWidget(combo_progress_btn)
        layout.addStretch()
        layout.addWidget(others_btn)
        layout.addStretch()
        layout.addWidget(back_btn)
        layout.addStretch()

        self.setLayout(layout)

    def on_training_clicked(self):
        print("Training button clicked")
        self.navigate_to(PageIndex.TRAINING)

    def on_performance_clicked(self):
        print("Performance button clicked")
        self.navigate_to(PageIndex.PERFORMANCE)

    def on_combo_progress_clicked(self):
        """Navigate to combo progress page for current user."""
        print("Combo Progress button clicked")
        # Set current user immediately so page always refreshes with latest data
        try:
            main_window = self.window()
            if main_window and hasattr(main_window, 'get_current_user'):
                current_user = main_window.get_current_user()
                if current_user:
                    page = self.stacked_widget.widget(PageIndex.USER_COMBO_PROGRESS)
                    if page and hasattr(page, 'set_user'):
                        page.set_user(current_user, return_to_page=PageIndex.HOMEPAGE)
        except Exception as e:
            print(f"Error preparing combo progress page: {e}")
        self.navigate_to(PageIndex.USER_COMBO_PROGRESS)

    def on_others_clicked(self):
        print("Others button clicked")
        self.navigate_to(PageIndex.OTHERS)

    def on_back_clicked(self):
        """Navigate back to login page."""
        self.navigate_to(PageIndex.LOGIN)


class OthersPage(ButtonNavigationMixin, QWidget):
    """Others page with stable layout and explicit focus navigation."""

    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        self.setFocusPolicy(Qt.StrongFocus)

        self.history_btn = QPushButton("History")
        self.stance_btn = QPushButton("Orthodox")
        self.ai_chat_btn = QPushButton("AI Chat: Off")
        self.arduino_port_combo = QComboBox()
        self.arduino_port_apply_btn = QPushButton("Apply Arduino Port")
        self.back_btn = QPushButton("Back")
        self.arduino_port_status = QLabel("")
        self.arduino_listener_status = QLabel("Listener: initializing")

        self._nav_buttons: List[QPushButton] = [
            self.history_btn,
            self.stance_btn,
            self.ai_chat_btn,
            self.arduino_port_apply_btn,
            self.back_btn,
        ]
        self._focused_button_index = 0

        self._setup_widgets()
        self._setup_layout()
        self._setup_connections()
        self.setup_navigation(self._nav_buttons)

        if self.app_state:
            self.ai_chat_btn.setText("AI Chat: On" if self.app_state.ai_chat_enabled else "AI Chat: Off")

        self._refresh_arduino_ports()
        self._refresh_listener_status()

    def _setup_widgets(self):
        for button in self._nav_buttons:
            button.setFocusPolicy(Qt.StrongFocus)

        self.arduino_port_combo.setFixedWidth(360)
        self.arduino_port_combo.setFocusPolicy(Qt.NoFocus)
        self.arduino_port_apply_btn.setFixedWidth(320)
        self.arduino_port_status.setAlignment(Qt.AlignCenter)
        self.arduino_port_status.setStyleSheet("color: #666; font-size: 13px;")
        self.arduino_listener_status.setAlignment(Qt.AlignCenter)
        self.arduino_listener_status.setStyleSheet("color: #666; font-size: 13px;")

    def _setup_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 28, 40, 28)
        main_layout.setSpacing(14)

        title = QLabel("Others")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")

        button_stack = QVBoxLayout()
        button_stack.setSpacing(12)
        button_stack.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        button_stack.addWidget(self.history_btn, alignment=Qt.AlignCenter)
        button_stack.addWidget(self.stance_btn, alignment=Qt.AlignCenter)
        button_stack.addWidget(self.ai_chat_btn, alignment=Qt.AlignCenter)

        serial_stack = QVBoxLayout()
        serial_stack.setSpacing(8)
        serial_stack.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        serial_stack.addWidget(self.arduino_port_combo, alignment=Qt.AlignCenter)
        serial_stack.addWidget(self.arduino_port_apply_btn, alignment=Qt.AlignCenter)
        serial_stack.addWidget(self.arduino_port_status, alignment=Qt.AlignCenter)
        serial_stack.addWidget(self.arduino_listener_status, alignment=Qt.AlignCenter)

        main_layout.addWidget(title, alignment=Qt.AlignCenter)
        main_layout.addSpacing(8)
        main_layout.addLayout(button_stack)
        main_layout.addSpacing(10)
        main_layout.addLayout(serial_stack)
        main_layout.addStretch(1)
        main_layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def _setup_connections(self):
        self.history_btn.clicked.connect(self.on_history_clicked)
        self.stance_btn.clicked.connect(self.on_stance_clicked)
        self.ai_chat_btn.clicked.connect(self.on_ai_chat_clicked)
        self.arduino_port_apply_btn.clicked.connect(self.on_apply_arduino_port)
        self.back_btn.clicked.connect(self.on_back_clicked)

    def _refresh_listener_status(self):
        main_window = self.window()
        if main_window and hasattr(main_window, "get_arduino_button_runtime_status"):
            self.arduino_listener_status.setText(
                f"Listener: {main_window.get_arduino_button_runtime_status()}"
            )
        else:
            self.arduino_listener_status.setText("Listener: unavailable")

    def _refresh_arduino_ports(self):
        self.arduino_port_combo.clear()
        self.arduino_port_combo.addItem("Auto Detect", "")

        ports: List[str] = []
        arduino_like_ports: List[str] = []
        if list_ports is not None:
            try:
                for port_info in list_ports.comports():
                    ports.append(port_info.device)
                    desc = (port_info.description or "").lower()
                    if "arduino" in desc or "ch340" in desc or "usb serial" in desc:
                        arduino_like_ports.append(port_info.device)
            except Exception:
                ports = []
                arduino_like_ports = []

        for port in sorted(set(ports)):
            self.arduino_port_combo.addItem(port, port)

        configured_port = os.getenv("ARDUINO_BUTTON_PORT", "").strip()
        if configured_port:
            idx = self.arduino_port_combo.findData(configured_port)
            if idx < 0:
                self.arduino_port_combo.addItem(f"{configured_port} (configured)", configured_port)
                idx = self.arduino_port_combo.findData(configured_port)
            self.arduino_port_combo.setCurrentIndex(max(idx, 0))
            self.arduino_port_status.setText(f"Current: {configured_port}")
        else:
            self.arduino_port_combo.setCurrentIndex(0)
            self.arduino_port_status.setText("Current: Auto Detect")

        unique_arduino_like = sorted(set(arduino_like_ports))
        if not configured_port and len(unique_arduino_like) == 1:
            self._apply_arduino_port(unique_arduino_like[0], user_initiated=False)

        self._refresh_listener_status()

    def on_history_clicked(self):
        try:
            main_window = self.window()
            username = main_window.get_current_user() if hasattr(main_window, "get_current_user") else None
            history_page = self.stacked_widget.widget(PageIndex.PERFORMANCE_HISTORY)
            if username and hasattr(history_page, "load_history"):
                history_page.load_history(username)
            self.navigate_to(PageIndex.PERFORMANCE_HISTORY)
        except Exception:
            self.navigate_to(PageIndex.HOMEPAGE)

    def on_stance_clicked(self):
        current = self.stance_btn.text().strip()
        new_stance = "Southpaw" if current == "Orthodox" else "Orthodox"
        self.stance_btn.setText(new_stance)
        try:
            print(json.dumps({"stance": new_stance}))
        except Exception as e:
            print(f"Error sending stance message: {e}")

    def on_ai_chat_clicked(self):
        if self.app_state is None:
            return
        self.app_state.ai_chat_enabled = not self.app_state.ai_chat_enabled
        new_label = "AI Chat: On" if self.app_state.ai_chat_enabled else "AI Chat: Off"
        self.ai_chat_btn.setText(new_label)
        print(f"AI Chat {'enabled' if self.app_state.ai_chat_enabled else 'disabled'}")

    def _apply_arduino_port(self, selected_port: str, user_initiated: bool):
        _set_env_key(GUI_ENV_PATH, "ARDUINO_BUTTON_PORT", selected_port)
        main_window = self.window()
        if hasattr(main_window, "restart_arduino_button_listener"):
            main_window.restart_arduino_button_listener()

        label = selected_port if selected_port else "Auto Detect"
        self.arduino_port_status.setText(f"Current: {label}")
        if user_initiated:
            print(f"[ArduinoButtons] Port updated to: {label}")
        else:
            print(f"[ArduinoButtons] Auto-applied detected port: {label}")

    def on_apply_arduino_port(self):
        selected_port = (self.arduino_port_combo.currentData() or "").strip()
        try:
            self._apply_arduino_port(selected_port, user_initiated=True)
            self._refresh_listener_status()
        except Exception as e:
            self.arduino_port_status.setText(f"Port update failed: {e}")

    def on_back_clicked(self):
        self.navigate_to(PageIndex.HOMEPAGE)

class PerformancePage(ButtonNavigationMixin, QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        title = QLabel("Performance")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        power_btn = QPushButton("Power")
        stamina_btn = QPushButton("Stamina")
        reaction_time_btn = QPushButton("Reaction Time")
        back_btn = QPushButton("Back")

        power_btn.setStyleSheet(ButtonStyle.HOME_LARGE)
        stamina_btn.setStyleSheet(ButtonStyle.HOME_LARGE)
        reaction_time_btn.setStyleSheet(ButtonStyle.HOME_LARGE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        power_btn.clicked.connect(self.on_power_clicked)
        stamina_btn.clicked.connect(self.on_stamina_clicked)
        reaction_time_btn.clicked.connect(self.on_reaction_time_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(power_btn)
        layout.addStretch()
        layout.addWidget(stamina_btn)
        layout.addStretch()
        layout.addWidget(reaction_time_btn)
        layout.addStretch()
        layout.addWidget(back_btn)
        layout.addStretch()

        self.setLayout(layout)

    def on_power_clicked(self):
        print("Power button clicked")
        # Navigate to Power Instructions page (index 15)
        self.navigate_to(PageIndex.POWER_INSTRUCTIONS)

    def on_stamina_clicked(self):
        print("Stamina button clicked")
        # Navigate to Stamina Instructions page (index 18)
        self.navigate_to(PageIndex.STAMINA_INSTRUCTIONS)

    def on_reaction_time_clicked(self):
        print("Reaction Time button clicked")
        # Navigate to Reaction Instructions page (index 19)
        self.navigate_to(PageIndex.REACTION_INSTRUCTIONS)

    def on_back_clicked(self):
        self.navigate_to(PageIndex.HOMEPAGE)


class StaminaInstructionsPage(ButtonNavigationMixin, QWidget):
    """Instructions page for the Stamina mode."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold;")

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw as many punches to the head.\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 28px; font-weight: bold;")

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        back_btn = QPushButton("Back")
        history_btn = QPushButton("History")
        start_btn = QPushButton("Start")

        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        history_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        start_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)

        back_btn.setFixedWidth(250)
        history_btn.setFixedWidth(250)
        start_btn.setFixedWidth(250)

        back_btn.clicked.connect(self.on_back_clicked)
        history_btn.clicked.connect(self.show_history)
        start_btn.clicked.connect(self.on_start_clicked)

        button_layout.addWidget(back_btn)
        button_layout.addWidget(history_btn)
        button_layout.addWidget(start_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(instructions)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_back_clicked(self):
        self.navigate_to(PageIndex.PERFORMANCE)

    def on_start_clicked(self):
        try:
            countdown_page = self.stacked_widget.widget(PageIndex.COUNTDOWN)
            countdown_page.on_finished = self.launch_stamina_test_page
            countdown_page.return_page_index = PageIndex.STAMINA_INSTRUCTIONS  # back should return to stamina instructions
            countdown_page.start_countdown()
        except Exception:
            pass
        self.navigate_to(PageIndex.COUNTDOWN)

    def launch_stamina_test_page(self):
        try:
            stamina_page = self.stacked_widget.widget(PageIndex.STAMINA_TEST)
            if hasattr(stamina_page, "start_test"):
                stamina_page.start_test()
            self.navigate_to(PageIndex.STAMINA_TEST)
        except Exception:
            self.navigate_to(PageIndex.PERFORMANCE)

    def show_history(self):
        try:
            main_window = self.window()
            username = main_window.get_current_user() if hasattr(main_window, "get_current_user") else None
            history_page = self.stacked_widget.widget(PageIndex.PERFORMANCE_HISTORY)
            if username and hasattr(history_page, "load_history"):
                history_page.load_history(username)
            self.navigate_to(PageIndex.PERFORMANCE_HISTORY)
        except Exception:
            self.navigate_to(PageIndex.PERFORMANCE)


class StaminaTestPage(ButtonNavigationMixin, QWidget):
    """Runs a 2-minute stamina test with simulated or hardware-backed punch detection."""

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.duration_seconds = 120
        self._runner: Optional[StaminaRunner] = None
        self._worker_thread: Optional[QThread] = None
        self._is_running = False

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        self.title_label = QLabel("Stamina Test (2 Minutes)")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 34px; font-weight: bold;")

        mode_text = "Arduino" if USE_ARDUINO else "Simulation"
        self.mode_label = QLabel(f"Mode: {mode_text}")
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.mode_label.setStyleSheet("font-size: 18px; color: #FFC107; font-weight: bold;")

        self.timer_label = QLabel("Time: 120s")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 44px; font-weight: bold;")

        self.punch_label = QLabel("Punches: 0")
        self.punch_label.setAlignment(Qt.AlignCenter)
        self.punch_label.setStyleSheet("font-size: 36px; font-weight: bold;")

        self.rate_label = QLabel("Current Rate: 0.0 punches/min")
        self.rate_label.setAlignment(Qt.AlignCenter)
        self.rate_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        quit_btn = QPushButton("Quit")
        quit_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        quit_btn.setFixedWidth(250)
        quit_btn.clicked.connect(self.on_quit_clicked)

        layout.addStretch()
        layout.addWidget(self.title_label)
        layout.addWidget(self.mode_label)
        layout.addStretch()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.punch_label)
        layout.addWidget(self.rate_label)
        layout.addStretch()
        layout.addWidget(quit_btn, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    def start_test(self):
        if self._is_running:
            return

        self._is_running = True
        self.timer_label.setText(f"Time: {self.duration_seconds}s")
        self.punch_label.setText("Punches: 0")
        self.rate_label.setText("Current Rate: 0.0 punches/min")

        class _Worker(QObject):
            progress = Signal(int, int, float)
            finished = Signal(dict)

            def __init__(self, runner: StaminaRunner, parent=None):
                super().__init__(parent)
                self.runner = runner

            def run(self):
                def on_progress(elapsed: int, punches: int, rate: float):
                    self.progress.emit(elapsed, punches, rate)

                def on_result(result: dict):
                    self.finished.emit(result)

                self.runner.measure_stamina_with_callback(on_progress, on_result)

        self._runner = StaminaRunner(duration_seconds=self.duration_seconds, use_arduino=USE_ARDUINO)
        self._worker_thread = QThread(self)
        self._worker = _Worker(self._runner)
        self._worker.moveToThread(self._worker_thread)
        self._worker_thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.finished.connect(self._worker_thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker_thread.finished.connect(self._worker_thread.deleteLater)
        self._worker_thread.start()

    def _on_progress(self, elapsed: int, punches: int, rate: float):
        remaining = max(0, self.duration_seconds - elapsed)
        self.timer_label.setText(f"Time: {remaining}s")
        self.punch_label.setText(f"Punches: {punches}")
        self.rate_label.setText(f"Current Rate: {rate:.1f} punches/min")

    def _on_finished(self, results: dict):
        self._is_running = False
        result_page = self.stacked_widget.widget(PageIndex.STAMINA_RESULT)
        if hasattr(result_page, "set_results"):
            result_page.set_results(results)
        self.navigate_to(PageIndex.STAMINA_RESULT)

    def on_quit_clicked(self):
        if self._runner:
            self._runner.stop()
        self._is_running = False
        self.navigate_to(PageIndex.PERFORMANCE)


class StaminaResultPage(ButtonNavigationMixin, QWidget):
    """Displays stamina metrics, stores test data, and generates coaching feedback."""

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_results: Optional[dict] = None

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("Stamina Results")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 34px; font-weight: bold;")

        self.score_label = QLabel("Stamina Score: --/100")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("font-size: 30px; font-weight: bold; color: #4CAF50;")

        self.metrics_label = QLabel("")
        self.metrics_label.setAlignment(Qt.AlignCenter)
        self.metrics_label.setStyleSheet("font-size: 20px; color: white; font-weight: bold;")
        self.metrics_label.setWordWrap(True)

        self.ai_feedback_label = QLabel("")
        self.ai_feedback_label.setWordWrap(True)
        self.ai_feedback_label.setStyleSheet(
            """
            font-size: 16px;
            padding: 16px;
            background-color: #f0f0f0;
            border-radius: 10px;
            color: black;
            """
        )

        button_row = QHBoxLayout()
        history_btn = QPushButton("History")
        restart_btn = QPushButton("Restart")
        quit_btn = QPushButton("Quit")
        history_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        restart_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        quit_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        history_btn.clicked.connect(self.on_history_clicked)
        restart_btn.clicked.connect(self.on_restart_clicked)
        quit_btn.clicked.connect(self.on_quit_clicked)
        button_row.addStretch()
        button_row.addWidget(history_btn)
        button_row.addWidget(restart_btn)
        button_row.addWidget(quit_btn)
        button_row.addStretch()

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.score_label)
        layout.addWidget(self.metrics_label)
        layout.addWidget(self.ai_feedback_label)
        layout.addStretch()
        layout.addLayout(button_row)

        self.setLayout(layout)

    def set_results(self, results: dict):
        self.current_results = results
        self.score_label.setText(f"Stamina Score: {results.get('stamina_score', 0)}/100")
        self.metrics_label.setText(
            f"Total Punches: {results.get('total_punches', 0)}\n"
            f"Average Rate: {results.get('average_rate', 0):.1f} punches/min\n"
            f"First 30s: {results.get('first_30_rate', 0):.1f} | Last 30s: {results.get('last_30_rate', 0):.1f}\n"
            f"Fatigue: {results.get('fatigue_percentage', 0):.1f}%"
        )

        main_window = self.get_main_window()
        username = main_window.get_current_user() if main_window else None

        if username:
            try:
                from performance_database import save_stamina_result, get_latest_performance_summary
                save_stamina_result(username, results)
                stats = get_latest_performance_summary(username)
            except Exception as e:
                stats = None
                print(f"Error saving stamina result: {e}")
        else:
            stats = None

        self._generate_feedback(results, stats)

    def _generate_feedback(self, results: dict, stats: Optional[dict]):
        score = results.get("stamina_score", 0)
        fatigue = results.get("fatigue_percentage", 0.0)
        punches = results.get("total_punches", 0)
        trend_text = ""
        if stats and isinstance(stats, dict) and "stamina" in stats:
            trend = stats["stamina"].get("difference", 0.0)
            trend_text = f" Recent trend: {'+' if trend > 0 else ''}{trend:.1f} punches vs avg."

        if score >= 80:
            opening = f"Excellent endurance today: {punches} punches with strong pacing."
        elif score >= 60:
            opening = f"Good stamina session with {punches} punches completed."
        else:
            opening = f"Solid effort with {punches} punches; this is a good base to build on."

        if fatigue <= 15:
            detail = "You maintained output very consistently through the full duration."
        elif fatigue >= 30:
            detail = "You started fast but faded; focus on pace control in the first minute."
        else:
            detail = "Your pace dropped moderately; aim for steadier breathing and rhythm."

        app_state = getattr(self.get_main_window(), "app_state", None)
        ai_prefix = "🤖 Coach Feedback:" if app_state and getattr(app_state, "ai_chat_enabled", False) else "💪 Feedback:"
        self.ai_feedback_label.setText(f"{ai_prefix}\n\n{opening} {detail}{trend_text}")

    def on_history_clicked(self):
        main_window = self.get_main_window()
        username = main_window.get_current_user() if main_window else None
        history_page = self.stacked_widget.widget(PageIndex.PERFORMANCE_HISTORY)
        if username and hasattr(history_page, "load_history"):
            history_page.load_history(username)
        self.navigate_to(PageIndex.PERFORMANCE_HISTORY)

    def on_restart_clicked(self):
        self.navigate_to(PageIndex.STAMINA_INSTRUCTIONS)

    def on_quit_clicked(self):
        self.navigate_to(PageIndex.PERFORMANCE)

    def get_main_window(self):
        window = self.window()
        return window if hasattr(window, "get_current_user") else None


class PerformanceHistoryPage(ButtonNavigationMixin, QWidget):
    """Unified performance history page for Power, Stamina, and Reaction tests."""

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_filter = 'All'
        self.all_history: List[dict] = []
        self.return_to_page: Optional[int] = None

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(24, 16, 24, 16)

        self.title_label = QLabel("Performance History")
        self.title_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)

        summary_group = QWidget()
        summary_group.setStyleSheet("background-color: #1f1f1f; border-radius: 10px;")
        summary_layout = QVBoxLayout()
        summary_layout.setContentsMargins(15, 12, 15, 12)

        summary_title = QLabel("LATEST PERFORMANCE SUMMARY")
        summary_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50;")

        self.power_summary_label = QLabel("Power: No data yet")
        self.stamina_summary_label = QLabel("Stamina: No data yet")
        self.reaction_summary_label = QLabel("Reaction Time: No data yet")
        self.trend_label = QLabel("Overall Trend: --")

        for lbl in [self.power_summary_label, self.stamina_summary_label, self.reaction_summary_label]:
            lbl.setStyleSheet("font-size: 16px; color: white;")
        self.trend_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50;")

        summary_layout.addWidget(summary_title)
        summary_layout.addWidget(self.power_summary_label)
        summary_layout.addWidget(self.stamina_summary_label)
        summary_layout.addWidget(self.reaction_summary_label)
        summary_layout.addWidget(self.trend_label)
        summary_group.setLayout(summary_layout)

        table_group = QWidget()
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(0, 0, 0, 0)

        filter_row = QHBoxLayout()
        self.all_btn = QPushButton("All")
        self.power_btn = QPushButton("Power")
        self.stamina_btn = QPushButton("Stamina")
        self.reaction_btn = QPushButton("Reaction")

        for btn in [self.all_btn, self.power_btn, self.stamina_btn, self.reaction_btn]:
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton { font-size: 14px; padding: 8px 14px; }
                QPushButton:checked { background-color: #3498db; color: white; }
            """)
            filter_row.addWidget(btn)

        self.all_btn.setChecked(True)
        self.all_btn.clicked.connect(lambda: self.apply_filter('All'))
        self.power_btn.clicked.connect(lambda: self.apply_filter('Power'))
        self.stamina_btn.clicked.connect(lambda: self.apply_filter('Stamina'))
        self.reaction_btn.clicked.connect(lambda: self.apply_filter('Reaction'))

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Time", "Type", "Result", "Trend"])
        for i in range(5):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { font-size: 14px; background-color: white; color: black; }
            QHeaderView::section { background-color: #4CAF50; color: white; font-weight: bold; }
        """)

        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        self.back_button.clicked.connect(self.go_back)

        table_layout.addLayout(filter_row)
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)

        layout.addWidget(self.title_label)
        layout.addWidget(summary_group)
        layout.addWidget(table_group)
        layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def load_history(self, username: str, return_to: Optional[int] = None):
        from performance_database import get_all_performance_history, get_latest_performance_summary

        self.return_to_page = return_to
        self.title_label.setText(f"Performance History - {username}")
        summary = get_latest_performance_summary(username)
        self._update_summary(summary)
        self.all_history = get_all_performance_history(username, limit=100)
        self.apply_filter(self.current_filter)

    def _update_summary(self, summary: dict):
        if 'power' in summary:
            p = summary['power']
            icon = '↑' if p['trend'] == 'up' else '↓' if p['trend'] == 'down' else '→'
            sign = '+' if p['difference'] > 0 else ''
            self.power_summary_label.setText(f"Power: {p['latest']:.1f}g ({icon} {sign}{p['difference']:.1f} vs avg)")
        else:
            self.power_summary_label.setText("Power: No data yet")

        if 'stamina' in summary:
            s = summary['stamina']
            icon = '↑' if s['trend'] == 'up' else '↓' if s['trend'] == 'down' else '→'
            sign = '+' if s['difference'] > 0 else ''
            self.stamina_summary_label.setText(
                f"Stamina: {int(s['latest'])} punches ({icon} {sign}{s['difference']:.0f} vs avg)"
            )
        else:
            self.stamina_summary_label.setText("Stamina: No data yet")

        if 'reaction' in summary:
            r = summary['reaction']
            icon = '↑' if r['trend'] == 'up' else '↓' if r['trend'] == 'down' else '→'
            sign = '+' if r['difference'] > 0 else ''
            self.reaction_summary_label.setText(
                f"Reaction Time: {r['latest']:.3f}s ({icon} {sign}{r['difference']:.3f}s vs avg)"
            )
        else:
            self.reaction_summary_label.setText("Reaction Time: No data yet")

        if summary:
            improving = sum(1 for key in summary if summary[key]['trend'] == 'up')
            declining = sum(1 for key in summary if summary[key]['trend'] == 'down')
            if improving > declining:
                self.trend_label.setText("Overall Trend: Improving ✓")
            elif declining > improving:
                self.trend_label.setText("Overall Trend: Needs Work ⚠")
            else:
                self.trend_label.setText("Overall Trend: Stable →")
        else:
            self.trend_label.setText("Overall Trend: --")

    def apply_filter(self, filter_type: str):
        self.current_filter = filter_type
        self.all_btn.setChecked(filter_type == 'All')
        self.power_btn.setChecked(filter_type == 'Power')
        self.stamina_btn.setChecked(filter_type == 'Stamina')
        self.reaction_btn.setChecked(filter_type == 'Reaction')

        if filter_type == 'All':
            filtered_data = self.all_history
        else:
            filtered_data = [item for item in self.all_history if item.get('test_type') == filter_type]
        self._populate_table(filtered_data)

    def _populate_table(self, data: List[dict]):
        self.table.setRowCount(len(data))
        for row, test in enumerate(data):
            dt = datetime.fromisoformat(test['timestamp'])
            self.table.setItem(row, 0, QTableWidgetItem(dt.strftime('%Y-%m-%d')))
            self.table.setItem(row, 1, QTableWidgetItem(dt.strftime('%H:%M')))
            type_item = QTableWidgetItem(test['test_type'])
            type_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, type_item)
            result = test['display_value']
            if 'secondary_value' in test:
                result = f"{result} ({test['secondary_value']})"
            self.table.setItem(row, 3, QTableWidgetItem(result))
            trend_item = QTableWidgetItem(self._calculate_trend(data, row, test['test_type']))
            trend_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, trend_item)

    def _calculate_trend(self, data: List[dict], current_index: int, test_type: str) -> str:
        for j in range(current_index + 1, len(data)):
            if data[j]['test_type'] != test_type:
                continue
            current = float(data[current_index]['primary_value'])
            previous = float(data[j]['primary_value'])
            diff = (previous - current) if test_type == 'Reaction' else (current - previous)
            if abs(diff) < 1e-6:
                return '→ same'
            return f"↑ +{abs(diff):.1f}" if diff > 0 else f"↓ -{abs(diff):.1f}"
        return 'First test'

    def go_back(self):
        main_window = self.window()
        if self.return_to_page is not None and hasattr(main_window, "navigate_to"):
            main_window.navigate_to(self.return_to_page)
        elif hasattr(main_window, "navigate_back"):
            main_window.navigate_back()
        else:
            self.navigate_to(PageIndex.OTHERS)


class ReactionInstructionsPage(ButtonNavigationMixin, QWidget):
    """Instructions page for the Reaction Time mode."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.skip_countdown = False  # Flag to skip countdown on restart

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold;")

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Wait until the screen turns green.\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 28px; font-weight: bold;")

        # Buttons at the bottom
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        back_btn = QPushButton("Back")
        history_btn = QPushButton("History")
        start_btn = QPushButton("Start")

        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        history_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        start_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)

        back_btn.setFixedWidth(250)
        history_btn.setFixedWidth(250)
        start_btn.setFixedWidth(250)

        back_btn.clicked.connect(self.on_back_clicked)
        history_btn.clicked.connect(self.show_history)
        start_btn.clicked.connect(self.on_start_clicked)

        button_layout.addWidget(back_btn)
        button_layout.addWidget(history_btn)
        button_layout.addWidget(start_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(instructions)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_back_clicked(self):
        self.skip_countdown = False
        self.navigate_to(PageIndex.PERFORMANCE)

    def on_start_clicked(self):
        if self.skip_countdown:
            # Skip countdown and go directly to test
            self.skip_countdown = False
            self.launch_reaction_test_page()
        else:
            # Show countdown normally
            try:
                countdown_page = self.stacked_widget.widget(PageIndex.COUNTDOWN)
                countdown_page.on_finished = self.launch_reaction_test_page
                countdown_page.return_page_index = PageIndex.REACTION_INSTRUCTIONS  # back should return to reaction instructions
                countdown_page.start_countdown()
            except Exception:
                pass
            self.navigate_to(PageIndex.COUNTDOWN)

    def launch_reaction_test_page(self):
        try:
            reaction_test_page = self.stacked_widget.widget(PageIndex.REACTION_TEST)
            reaction_test_page.start_test()
            self.navigate_to(PageIndex.REACTION_TEST)
        except Exception:
            self.navigate_to(PageIndex.PERFORMANCE)

    def show_history(self):
        try:
            main_window = self.window()
            username = main_window.get_current_user() if hasattr(main_window, "get_current_user") else None
            history_page = self.stacked_widget.widget(PageIndex.PERFORMANCE_HISTORY)
            if username and hasattr(history_page, "load_history"):
                history_page.load_history(username, return_to=PageIndex.PERFORMANCE)
            self.navigate_to(PageIndex.PERFORMANCE_HISTORY)
        except Exception:
            self.navigate_to(PageIndex.PERFORMANCE)

class PowerInstructionsPage(ButtonNavigationMixin, QWidget):
    """Instructions page for the Power mode."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        instructions_1 = QLabel(
            "Instructions"
        )
        instructions_1.setAlignment(Qt.AlignCenter)
        instructions_1.setStyleSheet("font-size: 40px; font-weight: bold;")

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 28px; font-weight: bold;")

        # Buttons at the bottom
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        back_btn = QPushButton("Back")
        history_btn = QPushButton("History")
        start_btn = QPushButton("Start")

        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        history_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        start_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)

        back_btn.setFixedWidth(250)
        history_btn.setFixedWidth(250)
        start_btn.setFixedWidth(250)

        back_btn.clicked.connect(self.on_back_clicked)
        history_btn.clicked.connect(self.show_history)
        start_btn.clicked.connect(self.on_start_clicked)

        button_layout.addWidget(back_btn)
        button_layout.addWidget(history_btn)
        button_layout.addWidget(start_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(instructions_1)
        layout.addStretch()
        layout.addWidget(instructions)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_back_clicked(self):
        # Return to Performance page
        self.navigate_to(PageIndex.PERFORMANCE)

    def on_start_clicked(self):
        # Start the existing countdown flow then show CountdownPage (index 9)
        try:
            countdown_page = self.stacked_widget.widget(PageIndex.COUNTDOWN)
            # When countdown finishes, go to Power Punch page
            countdown_page.on_finished = self.launch_power_punch_page
            countdown_page.return_page_index = PageIndex.POWER_INSTRUCTIONS  # back should return to instructions
            countdown_page.start_countdown()
        except Exception:
            pass
        self.navigate_to(PageIndex.COUNTDOWN)

    def launch_power_punch_page(self):
        """Switch to the punch counting page after countdown."""
        try:
            punch_page = self.stacked_widget.widget(PageIndex.POWER_PUNCH)
            punch_page.reset_counter()
            self.navigate_to(PageIndex.POWER_PUNCH)
        except Exception:
            # If page not available, fall back to Performance page
            self.navigate_to(PageIndex.PERFORMANCE)

    def show_history(self):
        try:
            main_window = self.window()
            username = main_window.get_current_user() if hasattr(main_window, "get_current_user") else None
            history_page = self.stacked_widget.widget(PageIndex.PERFORMANCE_HISTORY)
            if username and hasattr(history_page, "load_history"):
                history_page.load_history(username, return_to=PageIndex.PERFORMANCE)
            self.navigate_to(PageIndex.PERFORMANCE_HISTORY)
        except Exception:
            self.navigate_to(PageIndex.PERFORMANCE)

class PowerPunchPage(ButtonNavigationMixin, QWidget):
    """Page to count power punches after countdown."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.target = 10
        self.count = 0
        self._worker_thread: Optional[QThread] = None
        self._measuring = False

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50,50,50,50)

        self.counter_label = QLabel(self.counter_text())
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet("font-size: 32px; font-weight: bold;")

        self.instruction_label = QLabel("Throw 10 Powerful Body Hooks")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        # Quit button at bottom
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        quit_btn = QPushButton("Quit")
        quit_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        quit_btn.setFixedWidth(250)
        quit_btn.clicked.connect(self.on_quit_clicked)

        button_layout.addWidget(quit_btn)
        button_layout.addStretch()

        main_layout.addStretch()
        main_layout.addWidget(self.counter_label)
        main_layout.addStretch()
        main_layout.addWidget(self.instruction_label)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def counter_text(self):
        return f"Punch Count: {self.count}/{self.target}"

    def reset_counter(self):
        # Reset UI and begin measurement run
        self.count = 0
        self.counter_label.setText(self.counter_text())
        if not self._measuring:
            self.start_measurement()

    def mousePressEvent(self, event):
        """Increment punch count on screen press until target reached."""
        # Manual taps no longer drive the flow; measurement is from sensor
        # Keep tap to give user feedback count if desired
        if self.count < self.target:
            self.count += 1
            self.counter_label.setText(self.counter_text())
        super().mousePressEvent(event)
    
    def on_completed(self, punches_data: List[tuple]):
        """Called when measurement completes; shows the result page."""
        try:
            # Calculate peak g-force from punches
            peak_g_force = max([g for _, g in punches_data], default=0.0) if punches_data else 0.0
            avg_g_force = (sum(g for _, g in punches_data) / len(punches_data)) if punches_data else 0.0
            total_punches = len(punches_data)
            result_page = self.stacked_widget.widget(PageIndex.POWER_RESULT)
            if hasattr(result_page, "set_results"):
                result_page.set_results(peak_g_force, avg_g_force, total_punches)
            elif hasattr(result_page, "set_power_output"):
                result_page.set_power_output(f"Peak: {peak_g_force:.2f} g")
            self.navigate_to(PageIndex.POWER_RESULT)
        except Exception:
            self.navigate_to(PageIndex.PERFORMANCE)

    def on_quit_clicked(self):
        # Abort and return to Performance page
        self.navigate_to(PageIndex.PERFORMANCE)

    def start_measurement(self):
        """Start background measurement using serial to detect 10 punches."""
        class _Worker(QObject):
            finished = Signal(list)  # Emit list of (punch_number, g_force) tuples
            punch_detected = Signal(int, float)  # Emit (punch_count, g_force) in real-time

            def __init__(self, parent=None):
                super().__init__(parent)

            def run(self):
                try:
                    # Use the callback version for real-time updates
                    punches = power_runner.measure_punches_with_callback(
                        port="COM10",  # Changed from COM10 to match your other script
                        baud=115200,
                        punch_threshold_ms2=100.0,
                        max_punches=10,
                        debounce_ms=300,
                        max_duration_s=120.0,
                        callback=self._on_punch_callback  # Real-time callback
                    )
                except Exception as ex:
                    print(f"Error during measurement: {ex}")
                    punches = []
                self.finished.emit(punches)
            
            def _on_punch_callback(self, punch_num: int, g_force: float):
                """Called immediately when a punch is detected by the serial reader."""
                self.punch_detected.emit(punch_num, g_force)

        # Set UI state
        self._measuring = True
        self.instruction_label.setText("Measuring... Throw 10 Powerful Body Hooks")

        # Spin worker thread
        self._worker_thread = QThread(self)
        self._worker = _Worker()
        self._worker.moveToThread(self._worker_thread)
        self._worker_thread.started.connect(self._worker.run)
        self._worker.punch_detected.connect(self._on_punch_detected)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.finished.connect(self._worker_thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker_thread.finished.connect(self._worker_thread.deleteLater)
        self._worker_thread.start()

    def _on_punch_detected(self, punch_count: int, g_force: float):
        """Update UI when a punch is detected - called in real-time via signal."""
        self.count = punch_count
        self.counter_label.setText(self.counter_text())
        # Optional: Show visual feedback
        self.instruction_label.setText(f"💥 {g_force:.1f}g! Keep going...")
        # Reset instruction text after a moment
        QTimer.singleShot(500, lambda: self.instruction_label.setText("Throw 10 Powerful Body Hooks"))

    def _on_worker_finished(self, punches_data: list):
        self._measuring = False
        self.on_completed(punches_data)

class PowerResultPage(ButtonNavigationMixin, QWidget):
    """Result page shown after completing the Power punches."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_peak_power = 0.0
        self.current_avg_power = 0.0
        self.current_total_punches = 0

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        # Center message
        self.result_label = QLabel("Punches Thrown in a Minute: 100")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        self.ai_feedback_label = QLabel("")
        self.ai_feedback_label.setWordWrap(True)
        self.ai_feedback_label.setStyleSheet(
            """
            font-size: 16px;
            padding: 16px;
            background-color: #f0f0f0;
            border-radius: 10px;
            color: black;
            """
        )

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        history_btn = QPushButton("History")
        restart_btn = QPushButton("Restart")
        quit_btn = QPushButton("Quit")

        history_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        restart_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        quit_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        history_btn.setFixedWidth(250)
        restart_btn.setFixedWidth(250)
        quit_btn.setFixedWidth(250)

        history_btn.clicked.connect(self.on_history_clicked)
        restart_btn.clicked.connect(self.on_restart_clicked)
        quit_btn.clicked.connect(self.on_quit_clicked)

        button_layout.addWidget(history_btn)
        button_layout.addWidget(restart_btn)
        button_layout.addWidget(quit_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(self.result_label)
        layout.addWidget(self.ai_feedback_label)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_power_output(self, value_str: str):
        self.result_label.setText(f"G-Force Output: {value_str}")

    def set_results(self, peak_power: float, avg_power: float, total_punches: int):
        self.current_peak_power = peak_power
        self.current_avg_power = avg_power
        self.current_total_punches = total_punches
        self.result_label.setText(
            f"Peak: {peak_power:.2f}g | Avg: {avg_power:.2f}g | Punches: {total_punches}"
        )

        main_window = self.window()
        username = main_window.get_current_user() if hasattr(main_window, "get_current_user") else None
        summary = None
        if username:
            try:
                from performance_database import save_power_result, get_latest_performance_summary
                save_power_result(username, peak_power, avg_power, total_punches)
                summary = get_latest_performance_summary(username)
            except Exception as e:
                print(f"Error saving power result: {e}")

        self._generate_feedback(peak_power, avg_power, total_punches, summary)

    def _generate_feedback(self, peak_power: float, avg_power: float, total_punches: int, summary: Optional[dict]):
        if peak_power >= 4.0:
            opening = f"Excellent power output with a {peak_power:.2f}g peak."
        elif peak_power >= 3.0:
            opening = f"Good power session with a {peak_power:.2f}g peak."
        else:
            opening = f"Solid effort today; {peak_power:.2f}g is a good base to build from."

        if avg_power >= 3.0:
            detail = "Your average power stayed strong across punches."
        else:
            detail = "Focus on transferring force consistently through each punch."

        count_detail = f" You completed {total_punches} recorded punches this round."

        trend_text = ""
        if summary and isinstance(summary, dict) and "power" in summary:
            diff = summary["power"].get("difference", 0.0)
            if diff > 0:
                trend_text = f" Recent trend: +{diff:.2f}g vs average."
            elif diff < 0:
                trend_text = f" Recent trend: {diff:.2f}g vs average; keep pressing for consistency."

        app_state = getattr(self.get_main_window(), "app_state", None)
        ai_prefix = "🤖 Coach Feedback:" if app_state and getattr(app_state, "ai_chat_enabled", False) else "💪 Feedback:"
        self.ai_feedback_label.setText(f"{ai_prefix}\n\n{opening} {detail}{count_detail}{trend_text}")

    def on_history_clicked(self):
        try:
            main_window = self.window()
            username = main_window.get_current_user() if hasattr(main_window, "get_current_user") else None
            history_page = self.stacked_widget.widget(PageIndex.PERFORMANCE_HISTORY)
            if username and hasattr(history_page, "load_history"):
                history_page.load_history(username, return_to=PageIndex.PERFORMANCE)
            self.navigate_to(PageIndex.PERFORMANCE_HISTORY)
        except Exception:
            self.navigate_to(PageIndex.PERFORMANCE)

    def on_restart_clicked(self):
        # Return to the Power Instructions to restart the flow
        self.navigate_to(PageIndex.POWER_INSTRUCTIONS)

    def on_quit_clicked(self):
        # Return to Performance menu
        self.navigate_to(PageIndex.PERFORMANCE)

    def get_main_window(self):
        window = self.window()
        return window if hasattr(window, "get_current_user") else None

class ReactionTestPage(ButtonNavigationMixin, QWidget):
    """Red/green screen to measure reaction time using camera after countdown."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.state = "red"
        self._init_thread: Optional[QThread] = None
        self._measurement_thread: Optional[QThread] = None
        self._init_in_progress = False
        self._measuring = False

        # Allow style sheets to paint the entire widget background
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        self.green_timer = QTimer()
        self.green_timer.setSingleShot(True)
        self.green_timer.timeout.connect(self.go_green)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.status_label = QLabel("Do Not Punch")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 48px; font-weight: bold; color: white; background: transparent;")

        layout.addStretch()
        layout.addWidget(self.status_label)
        layout.addStretch()

        self.setLayout(layout)
        self.set_red_state()

    def set_red_state(self):
        self.state = "red"
        self.setStyleSheet("background-color: #b71c1c;")
        self.status_label.setText("Do Not Punch")

    def schedule_green(self):
        delay_ms = random.randint(5, 8) * 1000
        self.green_timer.stop()
        self.green_timer.start(delay_ms)

    def start_test(self):
        """Start test: show setup screen and initialize camera/model."""
        self.set_red_state()
        self.status_label.setText("Setting up camera...")
        self._init_in_progress = True
        
        # Start initialization in background thread
        self._start_initialization()

    def _start_initialization(self):
        """Initialize camera and model in a worker thread."""
        class _InitWorker(QObject):
            finished = Signal(bool, str)  # success, error_message

            def __init__(self, parent=None):
                super().__init__(parent)

            def run(self):
                try:
                    success, error_msg = rt_runner.initialize_camera_and_model()
                    self.finished.emit(success, error_msg or "")
                except Exception as ex:
                    self.finished.emit(False, f"Initialization error: {str(ex)}")

        # Spin worker thread
        self._init_thread = QThread(self)
        self._init_worker = _InitWorker()
        self._init_worker.moveToThread(self._init_thread)
        self._init_thread.started.connect(self._init_worker.run)
        self._init_worker.finished.connect(self._on_init_finished)
        self._init_worker.finished.connect(self._init_thread.quit)
        self._init_worker.finished.connect(self._init_worker.deleteLater)
        self._init_thread.finished.connect(self._init_thread.deleteLater)
        self._init_thread.start()

    def _on_init_finished(self, success: bool, error_message: str):
        """Called when initialization completes."""
        self._init_in_progress = False
        
        if success:
            # Schedule green light
            self.schedule_green()
        else:
            # Show error
            self.status_label.setText(f"Error: {error_message}")
            QTimer.singleShot(2000, lambda: self.navigate_to(PageIndex.PERFORMANCE))

    def flash_text(self):
        self.status_label.setText("")
        QTimer.singleShot(150, lambda: self.status_label.setText("Do Not Punch"))

    def go_green(self):
        """Signal to punch and start reaction measurement."""
        self.state = "green"
        self.setStyleSheet("background-color: #2e7d32;")
        self.status_label.setText("Punch Now!")
        
        # Start background measurement when green appears
        if not self._measuring:
            self.start_measurement()

    def mousePressEvent(self, event):
        if self.state == "red" and not self._init_in_progress:
            self.flash_text()
            self.schedule_green()
        super().mousePressEvent(event)

    def start_measurement(self):
        """Start background measurement using camera to detect punch."""
        class _MeasurementWorker(QObject):
            finished = Signal(object)  # ReactionResult

            def __init__(self, parent=None):
                super().__init__(parent)

            def run(self):
                try:
                    result = rt_runner.measure_reaction_time()
                    self.finished.emit(result)
                except Exception as ex:
                    from reaction_time.reaction_time_runner import ReactionResult
                    result = ReactionResult(success=False, status="error", 
                                          error_message=f"Measurement error: {str(ex)}")
                    self.finished.emit(result)

        # Set UI state
        self._measuring = True
        self.status_label.setText("Measuring... Punch Now!")

        # Spin worker thread
        self._measurement_thread = QThread(self)
        self._measurement_worker = _MeasurementWorker()
        self._measurement_worker.moveToThread(self._measurement_thread)
        self._measurement_thread.started.connect(self._measurement_worker.run)
        self._measurement_worker.finished.connect(self._on_measurement_finished)
        self._measurement_worker.finished.connect(self._measurement_thread.quit)
        self._measurement_worker.finished.connect(self._measurement_worker.deleteLater)
        self._measurement_thread.finished.connect(self._measurement_thread.deleteLater)
        self._measurement_thread.start()

    def _on_measurement_finished(self, result):
        """Called when camera measurement completes."""
        self._measuring = False
        self.green_timer.stop()
        
        try:
            result_page = self.stacked_widget.widget(PageIndex.REACTION_RESULT)
            if result.success and result.reaction_ms is not None:
                # Convert milliseconds to seconds for display
                reaction_seconds = result.reaction_ms / 1000.0
                if hasattr(result_page, "set_reaction_time"):
                    result_page.set_reaction_time(reaction_seconds)
            else:
                # Show error/status
                status_text = result.status or "unknown"
                if result.status == "too_soon":
                    status_text = "Too Soon!"
                elif result.status == "timeout":
                    status_text = "No Punch Detected"
                if hasattr(result_page, "set_error_message"):
                    result_page.set_error_message(status_text)
            
            self.navigate_to(PageIndex.REACTION_RESULT)
        except Exception:
            self.navigate_to(PageIndex.PERFORMANCE)

class ReactionResultPage(ButtonNavigationMixin, QWidget):
    """Shows measured reaction time after the test."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_reaction_time = 0.0
        self.current_accuracy = 0.0
        self.current_total_attempts = 0
        self.current_successful_attempts = 0

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        self.result_label = QLabel("Reaction Time: -- s")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        self.ai_feedback_label = QLabel("")
        self.ai_feedback_label.setWordWrap(True)
        self.ai_feedback_label.setStyleSheet(
            """
            font-size: 16px;
            padding: 16px;
            background-color: #f0f0f0;
            border-radius: 10px;
            color: black;
            """
        )

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        history_btn = QPushButton("History")
        restart_btn = QPushButton("Restart")
        back_btn = QPushButton("Back")

        history_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        restart_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        history_btn.setFixedWidth(250)
        restart_btn.setFixedWidth(250)
        back_btn.setFixedWidth(250)

        history_btn.clicked.connect(self.on_history_clicked)
        restart_btn.clicked.connect(self.on_restart_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        button_layout.addWidget(history_btn)
        button_layout.addWidget(restart_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(self.result_label)
        layout.addWidget(self.ai_feedback_label)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_reaction_time(self, seconds: float):
        self.current_reaction_time = seconds
        self.current_accuracy = 1.0
        self.current_total_attempts = 1
        self.current_successful_attempts = 1
        self.result_label.setText(f"Reaction Time: {seconds:.3f} s")
        main_window = self.window()
        username = main_window.get_current_user() if hasattr(main_window, "get_current_user") else None
        summary = None
        if username:
            try:
                from performance_database import save_reaction_result, get_latest_performance_summary
                save_reaction_result(username, seconds, accuracy=1.0, total_attempts=1, successful_attempts=1)
                summary = get_latest_performance_summary(username)
            except Exception as e:
                print(f"Error saving reaction result: {e}")

        self._generate_feedback(seconds, 1.0, summary)

    def set_error_message(self, message: str):
        """Display error or status message instead of reaction time."""
        self.result_label.setText(message)
        self.ai_feedback_label.setText("")

    def _generate_feedback(self, reaction_time: float, accuracy: float, summary: Optional[dict]):
        if reaction_time < 0.4:
            opening = f"Lightning-fast reaction at {reaction_time:.3f}s."
        elif reaction_time < 0.6:
            opening = f"Good reflexes shown with a {reaction_time:.3f}s reaction time."
        else:
            opening = f"Nice effort today; {reaction_time:.3f}s is a solid baseline to improve from."

        if accuracy >= 0.9:
            detail = "Your strike timing and precision were excellent."
        elif accuracy >= 0.7:
            detail = "Accuracy is decent; target cleaner timing on each cue."
        else:
            detail = "Focus on clean target confirmation before committing each punch."

        trend_text = ""
        if summary and isinstance(summary, dict) and "reaction" in summary:
            diff = summary["reaction"].get("difference", 0.0)
            if diff < 0:
                trend_text = f" Recent trend: {diff:.3f}s faster than average."
            elif diff > 0:
                trend_text = f" Recent trend: +{diff:.3f}s slower than average; keep practicing timing drills."

        app_state = getattr(self.get_main_window(), "app_state", None)
        ai_prefix = "🤖 Coach Feedback:" if app_state and getattr(app_state, "ai_chat_enabled", False) else "⚡ Feedback:"
        self.ai_feedback_label.setText(f"{ai_prefix}\n\n{opening} {detail}{trend_text}")

    def on_history_clicked(self):
        try:
            main_window = self.window()
            username = main_window.get_current_user() if hasattr(main_window, "get_current_user") else None
            history_page = self.stacked_widget.widget(PageIndex.PERFORMANCE_HISTORY)
            if username and hasattr(history_page, "load_history"):
                history_page.load_history(username, return_to=PageIndex.PERFORMANCE)
            self.navigate_to(PageIndex.PERFORMANCE_HISTORY)
        except Exception:
            self.navigate_to(PageIndex.PERFORMANCE)

    def on_restart_clicked(self):
        # Set flag to skip countdown and go directly to test
        try:
            reaction_instructions_page = self.stacked_widget.widget(PageIndex.REACTION_INSTRUCTIONS)
            reaction_instructions_page.skip_countdown = True
        except Exception:
            pass
        self.navigate_to(PageIndex.REACTION_INSTRUCTIONS)

    def on_back_clicked(self):
        self.navigate_to(PageIndex.PERFORMANCE)

    def get_main_window(self):
        window = self.window()
        return window if hasattr(window, "get_current_user") else None

class TrainingPage(ButtonNavigationMixin, QWidget):
    """
    TrainingPage class for displaying training options in a GUI application.
    This class extends QWidget and provides a user interface for selecting different
    training activities. It displays a centered layout with buttons for accessing
    techniques and sparring features, along with a back button for navigation.
    Attributes:
        stacked_widget (QStackedWidget): Reference to the parent stacked widget for
            managing page navigation between different sections of the application.
        main_window: Reference to the MainWindow to get current user and check level.
    Methods:
        __init__(stacked_widget, main_window): Initializes the TrainingPage with UI components
            including title, buttons, and layout configuration.
        on_techniques_clicked(): Handles the techniques button click event and
            navigates to the Techniques page (index 2).
        on_spar_clicked(): Handles the spar button click event and navigates to
            the SparPage (index 12) if user is Intermediate or Advanced.
        on_back_clicked(): Handles the back button click event and returns to
            the main page (index 0).
    """
    def __init__(self, stacked_widget, main_window=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Training")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        techniques_btn = QPushButton("Techniques")
        self.spar_btn = QPushButton("Spar")
        back_btn = QPushButton("Back")

        techniques_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        self.spar_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        techniques_btn.clicked.connect(self.on_techniques_clicked)
        self.spar_btn.clicked.connect(self.on_spar_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(techniques_btn)
        layout.addWidget(self.spar_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_techniques_clicked(self):
        print("Techniques button clicked")
        self.navigate_to(PageIndex.TECHNIQUES)

    def on_spar_clicked(self):
        print("Spar button clicked")
        # SparPage is now at index 12 after removing DefenseTechniquePage
        self.navigate_to(PageIndex.SPAR)

    def on_back_clicked(self):
        self.navigate_to(PageIndex.HOMEPAGE)

class TechniquesPage(ButtonNavigationMixin, QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Training Options")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        punch_lib_btn = QPushButton("Punch Combination Library")
        back_btn = QPushButton("Back")

        punch_lib_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        punch_lib_btn.clicked.connect(self.on_punch_combination_library_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(punch_lib_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_punch_combination_library_clicked(self):
        print("Punch Combination Library button clicked")
        self.navigate_to(PageIndex.PUNCH_COMBINATIONS)

    def on_back_clicked(self):
        self.navigate_to(PageIndex.TRAINING)

class PunchCombinationPage(ButtonNavigationMixin, QWidget):
    NAV_BUTTON_MIN_WIDTH = 300
    NAV_BUTTON_MAX_WIDTH = 360
    NAV_BUTTON_MIN_HEIGHT = 55
    LAYOUT_SPACING = 18
    LAYOUT_MARGINS = (50, 30, 50, 30)
    NAV_BUTTON_STYLE = """
        QPushButton {
            font-size: 18px;
            padding: 12px 20px;
            background-color: #f5f5f5;
            border: 3px solid #cccccc;
            border-radius: 10px;
            min-width: 300px;
            min-height: 55px;
            color: #111111;
        }
        QPushButton:focus {
            border: 6px solid #00ff00;
            background-color: #2d5016;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e8e8e8;
        }
    """

    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(self.LAYOUT_SPACING)
        layout.setContentsMargins(*self.LAYOUT_MARGINS)

        title = QLabel("Punch Combinations")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        self.beginner_btn = QPushButton("Beginner")
        self.intermediate_btn = QPushButton("Intermediate")
        self.advanced_btn = QPushButton("Advanced")
        self.self_select_btn = QPushButton("Self-Select")
        back_btn = QPushButton("Back")

        self.beginner_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.intermediate_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.advanced_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.self_select_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        self.beginner_btn.clicked.connect(self.on_difficulty_clicked("Beginner"))
        self.intermediate_btn.clicked.connect(self.on_difficulty_clicked("Intermediate"))
        self.advanced_btn.clicked.connect(self.on_difficulty_clicked("Advanced"))
        self.self_select_btn.clicked.connect(self.on_difficulty_clicked("Self-Select"))
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        # center the buttons horizontally
        layout.addWidget(self.beginner_btn)
        layout.addWidget(self.intermediate_btn)
        layout.addWidget(self.advanced_btn)
        layout.addWidget(self.self_select_btn)
        # layout.addStretch()

        # Create horizontal layout for back and continue buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()  # Add space on the left
        
        back_btn = QPushButton("Back")
        self.continue_btn = QPushButton("Continue")  # Initialize continue_btn here
        
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        # Continue button should be green like Start actions
        self.continue_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        
        back_btn.clicked.connect(self.on_back_clicked)
        self.continue_btn.clicked.connect(self.on_continue_clicked)
        
        button_layout.addWidget(back_btn)
        button_layout.addWidget(self.continue_btn)
        button_layout.addStretch()  # Add space on the right

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Initialize button displays from state and update continue availability
        self.update_button_displays()

    def update_button_displays(self):
        """Refresh parameter buttons from app_state config and labels."""
        if self.app_state:
            config = self.app_state.get_config()
            self.beginner_btn.setText(f"Round\n{config.rounds}")
            self.speed_btn.setText(f"Speed\n{config.speed}")

            time_text = self.app_state.time_label or config.get_time_str()
            rest_text = self.app_state.rest_label or config.get_rest_str()
            self.time_btn.setText(f"Time\n{time_text}")
            self.rest_btn.setText(f"Rest\n{rest_text}")

        self.update_continue_button()

    def is_parameter_selected(self, btn):
        """Check if a parameter button has been selected (has more than just the label)."""
        text = btn.text()
        return "\n" in text  # Selected buttons have format "Label\nValue"

    def update_continue_button(self):
        """Enable continue button only if all parameters are selected."""
        all_selected = (
            self.is_parameter_selected(self.beginner_btn) and
            self.is_parameter_selected(self.intermediate_btn) and
            self.is_parameter_selected(self.advanced_btn) and
            self.is_parameter_selected(self.self_select_btn)
        )
        self.continue_btn.setEnabled(all_selected)

    def on_difficulty_clicked(self, difficulty):
        print(f"{difficulty} button clicked")
        # Store difficulty via app_state
        if self.app_state:
            self.app_state.update_difficulty(difficulty)
            self.app_state.previous_page = PageIndex.PUNCH_COMBINATIONS
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.selected_difficulty = difficulty
                basic_page.previous_page = PageIndex.PUNCH_COMBINATIONS
            except Exception:
                pass
        
        if difficulty == "Self-Select":
            self_select_page = self.stacked_widget.widget(PageIndex.SELF_SELECT_SEQUENCE)
            self_select_page.previous_page = PageIndex.PUNCH_COMBINATIONS
            self.navigate_to(PageIndex.SELF_SELECT_SEQUENCE)
        else:
            self.navigate_to(PageIndex.BASIC_PARAMETERS)

    def on_back_clicked(self):
        self.navigate_to(PageIndex.TECHNIQUES)

class BasicParametersPage(ButtonNavigationMixin, QWidget):
    """Page for basic parameters (index 4)."""
    NAV_BUTTON_MIN_WIDTH = 280
    NAV_BUTTON_MAX_WIDTH = 340
    NAV_BUTTON_MIN_HEIGHT = 55
    NAV_BUTTON_STYLE = PARAMETER_SELECTION_BUTTON_STYLE
    LAYOUT_SPACING = 15
    LAYOUT_MARGINS = (50, 25, 50, 25)

    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        self.previous_page = PageIndex.PUNCH_COMBINATIONS  # Fallback for when no app_state

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(self.LAYOUT_SPACING)
        layout.setContentsMargins(*self.LAYOUT_MARGINS)

        title = QLabel("Basic Parameters")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        # store as instance attribute so other pages can update it
        self.round_btn = QPushButton("Round")
        self.speed_btn = QPushButton("Speed")
        self.time_btn = QPushButton("Time")
        self.rest_btn = QPushButton("Rest")
        
        self.round_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.speed_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.time_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.rest_btn.setStyleSheet(ButtonStyle.INFO_SMALL)

        self.round_btn.clicked.connect(self.on_round_clicked)
        self.speed_btn.clicked.connect(self.on_speed_clicked)
        self.time_btn.clicked.connect(self.on_time_clicked)
        self.rest_btn.clicked.connect(self.on_rest_clicked)

        layout.addWidget(title)
        # center the buttons horizontally
        layout.addWidget(self.round_btn)
        layout.addWidget(self.speed_btn)
        layout.addWidget(self.time_btn)
        layout.addWidget(self.rest_btn)
        # layout.addStretch()

        # Create horizontal layout for back and continue buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()  # Add space on the left
        
        back_btn = QPushButton("Back")
        self.continue_btn = QPushButton("Continue")  # Initialize continue_btn here
        
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        # Continue button should be green like Start actions
        self.continue_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        
        back_btn.clicked.connect(self.on_back_clicked)
        self.continue_btn.clicked.connect(self.on_continue_clicked)
        
        button_layout.addWidget(back_btn)
        button_layout.addWidget(self.continue_btn)
        button_layout.addStretch()  # Add space on the right

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Initialize button displays from state and update continue availability
        self.update_button_displays()

    def update_button_displays(self):
        """Refresh parameter buttons from app_state config and labels."""
        if self.app_state:
            config = self.app_state.get_config()
            self.round_btn.setText(f"Round\n{config.rounds}")
            self.speed_btn.setText(f"Speed\n{config.speed}")

            time_text = self.app_state.time_label or config.get_time_str()
            rest_text = self.app_state.rest_label or config.get_rest_str()
            self.time_btn.setText(f"Time\n{time_text}")
            self.rest_btn.setText(f"Rest\n{rest_text}")

        self.update_continue_button()

    def is_parameter_selected(self, btn):
        """Check if a parameter button has been selected (has more than just the label)."""
        text = btn.text()
        return "\n" in text  # Selected buttons have format "Label\nValue"

    def update_continue_button(self):
        """Enable continue button only if all parameters are selected."""
        all_selected = (
            self.is_parameter_selected(self.round_btn) and
            self.is_parameter_selected(self.speed_btn) and
            self.is_parameter_selected(self.time_btn) and
            self.is_parameter_selected(self.rest_btn)
        )
        self.continue_btn.setEnabled(all_selected)

    def on_round_clicked(self):
        self.navigate_to(PageIndex.ROUND_SELECTION)

    def on_speed_clicked(self):
        self.navigate_to(PageIndex.SPEED_SELECTION)

    def on_time_clicked(self):
        self.navigate_to(PageIndex.TIME_SELECTION)

    def on_rest_clicked(self):
        self.navigate_to(PageIndex.REST_SELECTION)

    def on_back_clicked(self):
        prev_page = self.app_state.previous_page if self.app_state else self.previous_page
        self.stacked_widget.setCurrentIndex(prev_page)

    def on_continue_clicked(self):
        print("Continue button clicked")
        # Start countdown and move to CountdownPage
        countdown_page = self.stacked_widget.widget(PageIndex.COUNTDOWN)
        # Ensure training flow uses the training session start callback
        parent_window = self.stacked_widget.parent()
        if parent_window and hasattr(parent_window, "start_training_session"):
            countdown_page.on_finished = parent_window.start_training_session
        # Back from countdown should return to Basic Parameters during training flow
        countdown_page.return_page_index = PageIndex.BASIC_PARAMETERS
        countdown_page.start_countdown()
        self.navigate_to(PageIndex.COUNTDOWN)

class RoundSelectionPage(ButtonNavigationMixin, QWidget):
    """Page showing 12 numbered round buttons and a back button."""
    NAV_BUTTON_MIN_WIDTH = 90
    NAV_BUTTON_MAX_WIDTH = 120
    NAV_BUTTON_MIN_HEIGHT = 55
    NAV_BUTTON_STYLE = """
        QPushButton {
            font-size: 18px;
            padding: 10px 20px;
            background-color: #f5f5f5;
            border: 3px solid #cccccc;
            border-radius: 10px;
            min-width: 90px;
            max-width: 120px;
            min-height: 55px;
            color: #111111;
        }
        QPushButton:focus {
            border: 6px solid #00ff00;
            background-color: #2d5016;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e8e8e8;
        }
    """
    LAYOUT_SPACING = 15
    LAYOUT_MARGINS = (50, 25, 50, 25)

    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(self.LAYOUT_SPACING)
        main_layout.setContentsMargins(*self.LAYOUT_MARGINS)

        title = QLabel("Select Round")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(15)
        grid.setContentsMargins(30, 30, 30, 30)

        self.round_buttons: List[QPushButton] = []
        for idx in range(12):
            n = idx + 1
            btn = QPushButton(str(n))
            btn.setStyleSheet(ButtonStyle.ROUND_SELECTION)
            btn.clicked.connect(partial(self.select_round, n))
            row = idx // 4
            col = idx % 4
            grid.addWidget(btn, row, col)
            self.round_buttons.append(btn)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.setMinimumWidth(280)
        back_btn.setMaximumWidth(360)
        # go back to BasicParametersPage (index 4)
        back_btn.clicked.connect(lambda: self.navigate_to(PageIndex.BASIC_PARAMETERS))
        self.back_btn = back_btn
        self.navigation_buttons = [*self.round_buttons]

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def select_round(self, n: int):
        """Set the chosen round on BasicParametersPage and switch back."""
        if self.app_state:
            self.app_state.update_rounds(n)
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.update_button_displays()
            except Exception:
                pass
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.round_btn.setText(f"Round\n{n}")
                basic_page.update_continue_button()
            except Exception:
                pass
        self.navigate_to(PageIndex.BASIC_PARAMETERS)

class SpeedSelectionPage(ButtonNavigationMixin, QWidget):
    """Page offering speed choices (25, 50, 75, 100)."""
    NAV_BUTTON_MIN_WIDTH = 280
    NAV_BUTTON_MAX_WIDTH = 340
    NAV_BUTTON_MIN_HEIGHT = 55
    NAV_BUTTON_STYLE = PARAMETER_SELECTION_BUTTON_STYLE
    LAYOUT_SPACING = 15
    LAYOUT_MARGINS = (50, 25, 50, 25)

    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(self.LAYOUT_SPACING)
        main_layout.setContentsMargins(*self.LAYOUT_MARGINS)

        title = QLabel("Select Speed")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        options_layout = QVBoxLayout()
        options_layout.setSpacing(self.LAYOUT_SPACING)
        options_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        speeds = [("Slow", "25%"), ("Medium", "50%"), ("Fast", "75%")]
        for label, value in speeds:
            btn = QPushButton(label)
            btn.setStyleSheet(ButtonStyle.SPEED_SELECTION)
            btn.clicked.connect(partial(self.select_speed, value))
            options_layout.addWidget(btn, alignment=Qt.AlignCenter)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.navigate_to(PageIndex.BASIC_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(options_layout)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_speed(self, n: int):
        """Update BasicParametersPage speed button text and return."""
        if self.app_state:
            self.app_state.update_speed(n)
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.update_button_displays()
            except Exception:
                pass
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.speed_btn.setText(f"Speed\n{n}")
                basic_page.update_continue_button()
            except Exception:
                pass
        self.navigate_to(PageIndex.BASIC_PARAMETERS)

class TimeSelectionPage(ButtonNavigationMixin, QWidget):
    """Page offering time choices (30sec, 1min, 1min30sec, 2min, 2min30sec, 3min)."""
    NAV_BUTTON_MIN_WIDTH = 280
    NAV_BUTTON_MAX_WIDTH = 340
    NAV_BUTTON_MIN_HEIGHT = 55
    NAV_BUTTON_STYLE = PARAMETER_SELECTION_BUTTON_STYLE
    LAYOUT_SPACING = 15
    LAYOUT_MARGINS = (50, 25, 50, 25)

    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(self.LAYOUT_SPACING)
        main_layout.setContentsMargins(*self.LAYOUT_MARGINS)

        title = QLabel("Select Time")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        options_layout = QVBoxLayout()
        options_layout.setSpacing(self.LAYOUT_SPACING)
        options_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        times = [
            ("30s", 30),
            ("1min", 60),
            ("2min", 90),
            ("3min", 120),
        ]
        for label, seconds in times:
            btn = QPushButton(label)
            btn.setStyleSheet(ButtonStyle.TIME_SELECTION)
            btn.clicked.connect(partial(self.select_time, seconds, label))
            options_layout.addWidget(btn, alignment=Qt.AlignCenter)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.navigate_to(PageIndex.BASIC_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(options_layout)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_time(self, seconds: int, label: str):
        """Update BasicParametersPage time button text and return."""
        if self.app_state:
            self.app_state.time_label = label
            self.app_state.config.time_minutes = seconds // 60
            self.app_state.config.time_seconds = seconds % 60
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.update_button_displays()
            except Exception:
                pass
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.time_btn.setText(f"Time\n{label}")
                basic_page.update_continue_button()
            except Exception:
                pass
        self.navigate_to(PageIndex.BASIC_PARAMETERS)

class RestSelectionPage(ButtonNavigationMixin, QWidget):
    """Page offering rest choices (10sec to 60sec in 10sec increments)."""
    NAV_BUTTON_MIN_WIDTH = 280
    NAV_BUTTON_MAX_WIDTH = 340
    NAV_BUTTON_MIN_HEIGHT = 55
    NAV_BUTTON_STYLE = PARAMETER_SELECTION_BUTTON_STYLE
    LAYOUT_SPACING = 15
    LAYOUT_MARGINS = (50, 25, 50, 25)

    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(self.LAYOUT_SPACING)
        main_layout.setContentsMargins(*self.LAYOUT_MARGINS)

        title = QLabel("Select Rest Time")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        options_layout = QVBoxLayout()
        options_layout.setSpacing(self.LAYOUT_SPACING)
        options_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        rest_times = [
            ("10s", 10),
            ("30s", 30),
            ("1min", 60),
            ("1min 30s", 90),
        ]
        for label, seconds in rest_times:
            btn = QPushButton(label)
            btn.setStyleSheet(ButtonStyle.TIME_SELECTION)
            btn.clicked.connect(partial(self.select_rest, seconds, label))
            options_layout.addWidget(btn, alignment=Qt.AlignCenter)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.navigate_to(PageIndex.BASIC_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(options_layout)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_rest(self, seconds: int, label: str):
        """Update BasicParametersPage rest button text and return."""
        if self.app_state:
            self.app_state.rest_label = label
            self.app_state.config.rest_minutes = seconds // 60
            self.app_state.config.rest_seconds = seconds % 60
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.update_button_displays()
            except Exception:
                pass
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.rest_btn.setText(f"Rest\n{label}")
                basic_page.update_continue_button()
            except Exception:
                pass
        self.navigate_to(PageIndex.BASIC_PARAMETERS)

class CountdownPage(ButtonNavigationMixin, QWidget):
    """Page with 20 second countdown and pause button."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.countdown_value = 20
        self.is_paused = False
        self.on_finished = None  # callback to start training session
        # Where to return if user presses Back during countdown
        self.return_page_index = PageIndex.BASIC_PARAMETERS
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Wear Your Gloves")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 20px;")

        self.countdown_label = QLabel(str(self.countdown_value))
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")

        # Create horizontal layout for pause and back buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        self.pause_btn = QPushButton("Pause")
        back_btn = QPushButton("Back")

        self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        self.pause_btn.setFixedWidth(250)
        back_btn.setFixedWidth(250)

        self.pause_btn.clicked.connect(self.toggle_pause)
        back_btn.clicked.connect(self.on_back_clicked)

        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()

        main_layout.addStretch()
        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addWidget(self.countdown_label)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def start_countdown(self):
        """Start the countdown timer."""
        self.countdown_value = 3
        self.is_paused = False
        self.countdown_label.setText(str(self.countdown_value))
        self.pause_btn.setText("Pause")
        # Ensure Pause button starts in red style
        self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        self.timer.start(1000)  # Update every 1 second

    def update_countdown(self):
        """Update countdown display."""
        if self.countdown_value > 0:
            self.countdown_value -= 1
            self.countdown_label.setText(str(self.countdown_value))
        else:
            self.timer.stop()
            if callable(self.on_finished):
                self.on_finished()

    def toggle_pause(self):
        """Pause or resume the countdown."""
        if self.is_paused:
            self.timer.start(1000)
            self.pause_btn.setText("Pause")
            # Back to red when resuming (showing "Pause")
            self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
            self.is_paused = False
        else:
            self.timer.stop()
            self.pause_btn.setText("Resume")
            # Green while paused (showing "Resume")
            self.pause_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
            self.is_paused = True

    def on_back_clicked(self):
        """Stop timer and go back to BasicParametersPage."""
        self.timer.stop()
        self.stacked_widget.setCurrentIndex(self.return_page_index)

class TrainingSessionPage(ButtonNavigationMixin, QWidget):
    """Page showing the actual training session with round counter and timer."""
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        self.current_round = 1
        self.total_rounds = 1
        self.work_time = 60  # in seconds
        self.rest_time = 30  # in seconds
        self.time_remaining = self.work_time
        self.is_resting = False
        self.is_paused = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Training mode attributes
        self.difficulty = None
        self.battle_style = None

        # Combo curriculum state
        self.curriculum = None
        self.current_difficulty = None
        self.current_combo_id = None
        self.current_combo_name = ""
        self.current_combo_sequence = ""
        self.last_combo_id = None
        self.current_combo = None  # Stores combo dict from database
        self.combo_display_text = ""  # Text to display on screen
        self.combo_score = 0  # Score for the current combo (0-5, whole numbers)
        self.current_username = None  # Track current user for database updates

        # self-select state
        self.is_self_select_mode = False
        self.sequences = []
        self.sequence_index = 0
        self.sequence_cycle_seconds = 6  # each sequence shows for 6 seconds
        self.sequence_time_remaining = 0

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)

        # Round counter at the top
        self.round_label = QLabel(f"Round {self.current_round}/{self.total_rounds}")
        self.round_label.setAlignment(Qt.AlignCenter)
        self.round_label.setStyleSheet("font-size: 40px; font-weight: bold; margin-bottom: 20px;")

        # Rest indicator (hidden during work periods)
        self.rest_label = QLabel("Rest")
        self.rest_label.setAlignment(Qt.AlignCenter)
        self.rest_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #FF9800; margin-bottom: 10px;")
        self.rest_label.hide()

        # Sequence display (visible for combo/self-select modes during work)
        self.sequence_label = QLabel("")
        self.sequence_label.setAlignment(Qt.AlignCenter)
        self.sequence_label.setStyleSheet("font-size: 40px; font-weight: bold; color: #2196F3; margin-bottom: 20px;")
        self.sequence_label.hide()

        # Timer in the middle
        self.timer_label = QLabel(self.format_time(self.time_remaining))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")

        # Create horizontal layout for pause and back buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        self.pause_btn = QPushButton("Pause")
        stop_btn = QPushButton("Stop")

        self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        stop_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        self.pause_btn.setFixedWidth(250)
        stop_btn.setFixedWidth(250)

        self.pause_btn.clicked.connect(self.toggle_pause)
        stop_btn.clicked.connect(self.on_stop_clicked)

        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(stop_btn)
        button_layout.addStretch()

        main_layout.addStretch()
        main_layout.addWidget(self.round_label)
        main_layout.addStretch()
        main_layout.addWidget(self.rest_label)
        main_layout.addStretch()
        main_layout.addWidget(self.sequence_label)  # combo display above timer
        main_layout.addWidget(self.timer_label)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def format_time(self, seconds):
        """Format seconds as MM:SS."""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def parse_time_to_seconds(self, time_str):
        """Convert time string to seconds."""
        time_map = {
            "30sec": 30,
            "1min": 60,
            "1min30sec": 90,
            "2min": 120,
            "2min30sec": 150,
            "3min": 180,
            "10sec": 10,
            "20sec": 20,
            "40sec": 40,
            "50sec": 50
        }
        return time_map.get(time_str, 60)

    def _get_curriculum_db_path(self):
        """Get user-specific curriculum database path."""
        if hasattr(self, 'current_username') and self.current_username:
            return get_user_db_path(self.current_username)
        print("WARNING: No current_username in TrainingSessionPage")
        return SHARED_DB_PATH

    def _init_curriculum(self):
        """Initialize curriculum manager for Punch Combination mode."""
        if self.difficulty not in ["Beginner", "Intermediate", "Advanced"]:
            self.curriculum = None
            return

        try:
            db_path = self._get_curriculum_db_path()
            self.curriculum = ComboCurriculum(db_path)
            if not hasattr(self, '_db_init_notified'):
                if f"{os.sep}users{os.sep}" in db_path:
                    print(f"✓ Using personal progress database for: {self.current_username}")
                self._db_init_notified = True
        except Exception as e:
            print(f"Error initializing curriculum: {e}")
            self.curriculum = None

    def _select_curriculum_combo(self, previous_combo_id=None):
        """Select next combo based on curriculum progression."""
        if not self.curriculum or self.current_difficulty not in ["Beginner", "Intermediate", "Advanced"]:
            return False

        try:
            combo = self.curriculum.get_next_combo(self.current_difficulty, previous_combo_id)
            if not combo:
                next_level = self.curriculum.get_next_difficulty(self.current_difficulty)
                if next_level:
                    reply = QMessageBox.question(
                        self,
                        "Level Complete",
                        f"Congratulations! You've mastered all {self.current_difficulty} combos!\n"
                        f"Switch to {next_level} now?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.Yes,
                    )
                    if reply == QMessageBox.Yes:
                        self.current_difficulty = next_level
                        combo = self.curriculum.get_next_combo(self.current_difficulty, None)
                        if combo:
                            self.difficulty = self.current_difficulty
                        else:
                            QMessageBox.information(
                                self,
                                "No Combo Available",
                                f"No available combos found for {self.current_difficulty}.",
                            )
                            return False
                    else:
                        return False
                else:
                    QMessageBox.information(
                        self,
                        "All Combos Mastered",
                        f"Congratulations! You've mastered all {self.current_difficulty} combos!",
                    )
                    return False

            self.current_combo = combo
            self.current_combo_id = combo.get('combo_id')
            self.current_combo_name = combo.get('combo_name', '')
            self.current_combo_sequence = combo.get('combo_sequence', '')
            self.combo_display_text = self.current_combo_sequence
            return True
        except Exception as e:
            print(f"Error selecting curriculum combo: {e}")
            return False

    def _update_combo_display(self):
        """Update the on-screen combo label for curriculum modes."""
        if self.current_difficulty in ["Beginner", "Intermediate", "Advanced"] and self.current_combo_sequence:
            self.sequence_label.show()
            self.sequence_label.setText(self.current_combo_sequence)
        elif self.is_self_select_mode:
            self.sequence_label.show()
            self.update_sequence_display()
        else:
            self.sequence_label.hide()

    def _score_and_update_curriculum(self):
        """Score current combo and persist curriculum progress."""
        if not self.curriculum or not self.current_combo_id:
            return

        try:
            score = get_performance_score(video_path=None, combo_id=self.current_combo_id)
            self.combo_score = score
            self.curriculum.update_score(self.current_combo_id, score)

            combo_stats = self.curriculum.get_combo_stats(self.current_combo_id) or {}
            level_progress = self.curriculum.get_level_progress(self.current_difficulty) or {}
            feedback_data = format_feedback_data(combo_stats, level_progress, score)

            if self.current_username:
                try:
                    progress = calculate_user_progress_from_combos(self.current_username, self._get_curriculum_db_path())
                    update_user_progress(self.current_username, progress)
                except Exception as progress_error:
                    print(f"Error syncing user progress: {progress_error}")

            print(f"[TrainingSession] Combo score updated: {self.current_combo_id} -> {score}/5")
            group_name = feedback_data.get('current_group_name', 'N/A')
            group_progress = feedback_data.get('current_group_progress', '0/0 combos mastered')
            print(f"[TrainingSession] Progress: {group_name} ({group_progress})")
        except Exception as e:
            print(f"Error updating curriculum score: {e}")

    def _check_level_up_eligibility(self):
        """Check and display level-up eligibility at session end."""
        if not self.curriculum or self.current_difficulty not in ["Beginner", "Intermediate", "Advanced"]:
            return

        try:
            can_level_up = self.curriculum.check_progression_eligibility(self.current_difficulty)
            if can_level_up:
                next_level = self.curriculum.get_next_difficulty(self.current_difficulty)
                if next_level:
                    QMessageBox.information(
                        self,
                        "Level Up Ready",
                        f"Congratulations! You are ready to level up from {self.current_difficulty} to {next_level}.",
                    )
                else:
                    QMessageBox.information(
                        self,
                        "Mastery Complete",
                        f"Congratulations! You've mastered all {self.current_difficulty} combos!",
                    )
        except Exception as e:
            print(f"Error checking level-up eligibility: {e}")

    def send_round_start_message(self):
        """Send JSON message at the start of each round for non-Self-Select modes."""
        if self.is_self_select_mode:
            return  # Skip for Self-Select mode
        
        try:
            if self.difficulty == "Battle":
                # For Battle mode, send both mode and battle_style
                payload = {
                    "mode": self.difficulty,
                    "battle_style": self.battle_style,
                }
            elif self.difficulty in ["Beginner", "Intermediate", "Advanced"]:
                # For Punch Combination modes
                mode_str = f"Punch-Combination {self.difficulty}"
                payload = {
                    "mode": mode_str,
                }
                # Add combo info if available
                if self.current_combo:
                    payload["combo_id"] = self.current_combo.get("combo_id", "")
                    payload["combo_name"] = self.current_combo.get("combo_name", "")
                    payload["combo_sequence"] = self.current_combo.get("combo_sequence", "")
            else:
                # For other modes (Stamina, Reaction Time, Power, etc.)
                payload = {
                    "mode": self.difficulty,
                }
            print(json.dumps(payload))
        except Exception as e:
            print(f"Error sending round start message: {e}")

    def start_session(self, rounds, time_str, rest_str, difficulty=None, sequences=None, battle_style=None, username=None):
        """Start the training session with the given parameters."""
        self.current_round = 1
        self.total_rounds = rounds
        config_difficulty = None
        if self.app_state:
            try:
                config_difficulty = self.app_state.get_config().difficulty
            except Exception:
                config_difficulty = None

        self.difficulty = config_difficulty or difficulty
        self.current_difficulty = self.difficulty
        self.battle_style = battle_style
        self.current_username = username
        self.last_combo_id = None

        # Convert time strings to seconds
        self.work_time = self.parse_time_to_seconds(time_str)
        self.rest_time = self.parse_time_to_seconds(rest_str)

        # Self-select setup
        self.is_self_select_mode = (difficulty == "Self-Select") and sequences and len(sequences) > 0
        self.sequences = sequences if self.is_self_select_mode else []
        self.sequence_index = 0
        self.sequence_time_remaining = self.sequence_cycle_seconds if self.sequences else 0

        # Fetch combo from database for Beginner/Intermediate/Advanced modes
        self.current_combo = None
        self.combo_display_text = ""
        self.current_combo_id = None
        self.current_combo_name = ""
        self.current_combo_sequence = ""
        self._init_curriculum()

        if self.current_difficulty in ["Beginner", "Intermediate", "Advanced"]:
            selected = self._select_curriculum_combo(previous_combo_id=None)
            if selected and self.current_combo:
                self.combo_display_text = self.current_combo.get('combo_sequence', '')
                print(f"[TrainingSession] Selected combo: {self.current_combo.get('combo_name', 'Unknown')} ({self.combo_display_text})")
            else:
                self.combo_display_text = ""

        self.time_remaining = self.work_time
        self.is_resting = False
        self.is_paused = False

        self.round_label.setText(f"Round {self.current_round}/{self.total_rounds}")
        self.rest_label.hide()
        self.timer_label.setText(self.format_time(self.time_remaining))
        self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")
        self.pause_btn.setText("Pause")
        # Ensure Pause button starts in red style
        self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        # Show sequence/combo for Self-Select and Punch Combination modes
        self._update_combo_display()

        # Send round start message for non-Self-Select modes
        self.send_round_start_message()

        self.timer.start(1000)  # Update every 1 second

    def update_sequence_display(self):
        """Show the current sequence text."""
        if self.is_self_select_mode and self.sequences:
            current_sequence = self.sequences[self.sequence_index]
            self.sequence_label.setText(current_sequence)
            try:
                payload = {
                    "mode": self.difficulty,
                    "sequence": current_sequence,
                    "sequence_index": self.sequence_index,
                }
                print(json.dumps(payload))
            except Exception:
                pass
        else:
            self.sequence_label.setText("")

    def update_timer(self):
        """Update the timer display."""
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.setText(self.format_time(self.time_remaining))

            # Cycle self-select sequences every 6s during work
            if self.is_self_select_mode and not self.is_resting and self.sequences:
                if self.sequence_time_remaining > 0:
                    self.sequence_time_remaining -= 1
                if self.sequence_time_remaining <= 0 and self.time_remaining > 0:
                    self.sequence_index = (self.sequence_index + 1) % len(self.sequences)
                    self.sequence_time_remaining = self.sequence_cycle_seconds
                    self.update_sequence_display()
        else:
            if self.is_resting:
                # Rest finished -> next round
                self.current_round += 1
                self.is_resting = False
                self.time_remaining = self.work_time
                self.round_label.setText(f"Round {self.current_round}/{self.total_rounds}")
                self.rest_label.hide()
                self.timer_label.setText(self.format_time(self.time_remaining))
                self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")

                # reset sequence cycling for new round
                if self.is_self_select_mode and self.sequences:
                    self.sequence_index = 0
                    self.sequence_time_remaining = self.sequence_cycle_seconds
                elif self.current_difficulty in ["Beginner", "Intermediate", "Advanced"]:
                    self.last_combo_id = self.current_combo_id
                    if not self._select_curriculum_combo(previous_combo_id=self.last_combo_id):
                        self.timer.stop()
                        self.navigate_to(PageIndex.BASIC_PARAMETERS)
                        return
                self._update_combo_display()

                # Send round start message after combo has been selected/displayed
                self.send_round_start_message()
            else:
                # Work finished
                if self.current_difficulty in ["Beginner", "Intermediate", "Advanced"]:
                    self._score_and_update_curriculum()

                if self.current_round < self.total_rounds:
                    # start rest
                    self.is_resting = True
                    self.time_remaining = self.rest_time
                    self.rest_label.show()
                    self.timer_label.setText(self.format_time(self.time_remaining))
                    self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #FF9800;")
                    self.sequence_label.hide()
                    # Send Rest JSON message
                    try:
                        print(json.dumps({"action": "Rest"}))
                    except Exception as e:
                        print(f"Error sending rest message: {e}")
                else:
                    # final round done
                    self.timer.stop()
                    self.sequence_label.hide()
                    # Send Log Training Session JSON message
                    try:
                        print(json.dumps({"action": "Log Training Session"}))
                    except Exception as e:
                        print(f"Error sending log training session message: {e}")

                    # Persist session history for User Management session counts
                    self.log_user_training_session()
                    self._check_level_up_eligibility()
                    
                    # If combo mode, update database and show results
                    if self.difficulty in ["Beginner", "Intermediate", "Advanced"] and self.current_combo:
                        self.show_combo_results()
                    else:
                        self.navigate_to(PageIndex.BASIC_PARAMETERS)

    def toggle_pause(self):
        """Pause or resume the timer."""
        if self.is_paused:
            self.timer.start(1000)
            self.pause_btn.setText("Pause")
            # Back to red when resuming (showing "Pause")
            self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
            self.is_paused = False
            if not self.is_resting:
                # Send Resume JSON message
                try:
                    print(json.dumps({"action": "Resume"}))
                except Exception as e:
                    print(f"Error sending resume message: {e}")
                
                # Resend mode-specific information after resume
                try:
                    if self.is_self_select_mode and self.sequences:
                        # For Self-Select mode, send current sequence info
                        current_sequence = self.sequences[self.sequence_index]
                        payload = {
                            "mode": "Self-Select",
                            "sequence": current_sequence,
                            "sequence_index": self.sequence_index,
                        }
                        print(json.dumps(payload))
                    elif self.difficulty == "Battle":
                        # For Battle mode, send mode and battle_style
                        payload = {
                            "mode": self.difficulty,
                            "battle_style": self.battle_style,
                        }
                        print(json.dumps(payload))
                    elif self.difficulty in ["Beginner", "Intermediate", "Advanced"]:
                        # For Punch Combination modes
                        mode_str = f"Punch-Combination {self.difficulty}"
                        payload = {
                            "mode": mode_str,
                        }
                        print(json.dumps(payload))
                except Exception as e:
                    print(f"Error resending mode info after resume: {e}")
        else:
            self.timer.stop()
            self.pause_btn.setText("Resume")
            # Green while paused (showing "Resume")
            self.pause_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
            self.is_paused = True
            if not self.is_resting:
                # Send Pause JSON message
                try:
                    print(json.dumps({"action": "Pause"}))
                except Exception as e:
                    print(f"Error sending pause message: {e}")

    def on_stop_clicked(self):
        """Stop timer and go back to BasicParametersPage."""
        self.timer.stop()
        # Send Stop JSON message
        try:
            print(json.dumps({"action": "Stop"}))
        except Exception as e:
            print(f"Error sending stop message: {e}")
        self.navigate_to(PageIndex.BASIC_PARAMETERS)

    def log_user_training_session(self):
        """Append one completed session to the current user's training history CSV."""
        if not self.current_username:
            return

        try:
            training_csv = get_training_csv_path(self.current_username)
            file_exists = os.path.exists(training_csv)

            with open(training_csv, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow([
                        'timestamp', 'mode', 'difficulty', 'rounds', 'score', 'combo_id', 'combo_name'
                    ])

                combo_id = self.current_combo.get('combo_id', '') if self.current_combo else ''
                combo_name = self.current_combo.get('combo_name', '') if self.current_combo else ''
                score = self.combo_score if self.difficulty in ["Beginner", "Intermediate", "Advanced"] else ''

                writer.writerow([
                    time.strftime('%Y-%m-%d %H:%M:%S'),
                    self.difficulty or '',
                    self.difficulty or '',
                    self.total_rounds,
                    score,
                    combo_id,
                    combo_name,
                ])
        except Exception as e:
            print(f"Error logging user training session: {e}")
    
    def update_combo_database(self):
        """Update the combo database with the score."""
        if not self.current_combo:
            return
        
        try:
            curriculum = self.curriculum
            if not curriculum:
                curriculum = ComboCurriculum(self._get_curriculum_db_path())

            combo_id = self.current_combo.get('combo_id')
            # Update score in database
            result = curriculum.update_score(combo_id, self.combo_score)
            print(f"[TrainingSession] Stored combo score: {combo_id} -> {self.combo_score}/5")

            # Sync user progress into users.csv so User Management table stays updated
            if result and self.current_username:
                try:
                    progress = calculate_user_progress_from_combos(self.current_username, self._get_curriculum_db_path())
                    update_user_progress(self.current_username, progress)
                except Exception as progress_error:
                    print(f"Error syncing user progress: {progress_error}")

            if curriculum is not self.curriculum:
                curriculum.close()
        except Exception as e:
            print(f"[ERROR] Error updating combo database: {e}")
            import traceback
            traceback.print_exc()
    
    def show_combo_results(self):
        """Navigate to results page with combo performance (via AI chat if enabled)."""
        try:
            combo_name = self.current_combo.get('combo_name', 'Unknown')
            combo_sequence = self.current_combo.get('combo_sequence', '')
            score = self.combo_score
            difficulty = self.difficulty
            rounds = self.total_rounds
            
            # Check if AI chat is enabled
            if self.app_state and self.app_state.ai_chat_enabled:
                # Go to LLM chat page first
                chat_page = self.stacked_widget.widget(PageIndex.COMBO_LLM_CHAT)
                if chat_page:
                    chat_page.set_combo_data(combo_name, combo_sequence, score, difficulty, rounds)
                    self.navigate_to(PageIndex.COMBO_LLM_CHAT)
                    print("[TrainingSession] Routed to combo feedback chat")
                    return
            
            # AI chat disabled or not found - go directly to results page
            results_page = self.stacked_widget.widget(PageIndex.COMBO_RESULTS)
            if results_page:
                results_page.set_results(combo_name, combo_sequence, score, difficulty, rounds)
                self.navigate_to(PageIndex.COMBO_RESULTS)
                print("[TrainingSession] Routed to combo results page")
                return
        except Exception as e:
            print(f"[ERROR] Error showing results: {e}")
            import traceback
            traceback.print_exc()
        # Fallback to basic parameters if pages not found
        print("[TrainingSession] Results unavailable; returning to parameters")
        self.navigate_to(PageIndex.BASIC_PARAMETERS)

class SelfSelectSequencePage(ButtonNavigationMixin, QWidget):
    """Page for creating custom punch sequences."""
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        self.current_sequence = []  # Current sequence being built
        self.sequence_list = []  # List of confirmed sequences (max 5)
        self.editing_index = None  # Track which sequence is being edited
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # LEFT SIDE - Sequence List
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        list_title = QLabel("Sequence List")
        list_title.setAlignment(Qt.AlignCenter)
        list_title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 10px;")

        # Container for sequence buttons
        self.sequence_buttons_layout = QVBoxLayout()
        self.sequence_buttons_layout.setSpacing(10)
        self.sequence_buttons = []
        
        # Create 5 sequence slots
        for i in range(5):
            h_layout = QHBoxLayout()
            h_layout.setSpacing(10)
            
            # Sequence button (clickable to edit)
            seq_btn = QPushButton(f"{i+1}) ")
            seq_btn.setFocusPolicy(Qt.StrongFocus)
            seq_btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    padding: 8px 12px;
                    background-color: #f0f0f0;
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    text-align: left;
                    color: black;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border: 2px solid #2196F3;
                }
                QPushButton:focus {
                    border: 6px solid #00ff00;
                    background-color: #2d5016;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
            seq_btn.clicked.connect(lambda checked, idx=i: self.edit_sequence(idx))
            
            # Up button
            up_btn = QPushButton("▲")
            up_btn.setFocusPolicy(Qt.StrongFocus)
            up_btn.setFixedSize(38, 50)
            up_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: 2px solid #2f7f32;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:focus {
                    border: 3px solid #00ff00;
                    background-color: #2d5016;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                }
            """)
            up_btn.clicked.connect(lambda checked, idx=i: self.move_sequence_up(idx))
            
            # Down button
            down_btn = QPushButton("▼")
            down_btn.setFocusPolicy(Qt.StrongFocus)
            down_btn.setFixedSize(38, 50)
            down_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: 2px solid #2f7f32;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:focus {
                    border: 3px solid #00ff00;
                    background-color: #2d5016;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                }
            """)
            down_btn.clicked.connect(lambda checked, idx=i: self.move_sequence_down(idx))
            
            # Delete button
            del_btn = QPushButton("✖")
            del_btn.setFocusPolicy(Qt.StrongFocus)
            del_btn.setFixedSize(38, 50)
            del_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    background-color: #f44336;
                    color: white;
                    border: 2px solid #9e1f17;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
                QPushButton:focus {
                    border: 3px solid #00ff00;
                    background-color: #a52a2a;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                }
            """)
            del_btn.clicked.connect(lambda checked, idx=i: self.delete_sequence(idx))
            
            h_layout.addWidget(seq_btn, stretch=1)
            h_layout.addWidget(up_btn)
            h_layout.addWidget(down_btn)
            h_layout.addWidget(del_btn)
            
            self.sequence_buttons_layout.addLayout(h_layout)
            self.sequence_buttons.append({
                'button': seq_btn,
                'up': up_btn,
                'down': down_btn,
                'delete': del_btn
            })

        # Back and Next buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        back_btn = QPushButton("Back")
        self.next_btn = QPushButton("Next")
        
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        self.next_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        
        back_btn.setFixedWidth(150)
        self.next_btn.setFixedWidth(150)
        
        back_btn.clicked.connect(self.on_back_clicked)
        self.next_btn.clicked.connect(self.on_next_clicked)
        
        button_layout.addWidget(back_btn)
        button_layout.addWidget(self.next_btn)

        # Add left and right layouts to main layout
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        self.setLayout(main_layout)
        
        # Initial state
        self.update_sequence_buttons()
        self.update_buttons()

    def update_sequence_buttons(self):
        """Update all sequence button displays and states."""
        for i in range(5):
            if i < len(self.sequence_list):
                self.sequence_buttons[i]['button'].setText(f"{i+1}) {self.sequence_list[i]}")
                self.sequence_buttons[i]['button'].setEnabled(True)
                self.sequence_buttons[i]['delete'].setEnabled(True)
                # Enable up button if not first
                self.sequence_buttons[i]['up'].setEnabled(i > 0)
                # Enable down button if not last in list
                self.sequence_buttons[i]['down'].setEnabled(i < len(self.sequence_list) - 1)
            else:
                self.sequence_buttons[i]['button'].setText(f"{i+1}) ")
                self.sequence_buttons[i]['button'].setEnabled(False)
                self.sequence_buttons[i]['up'].setEnabled(False)
                self.sequence_buttons[i]['down'].setEnabled(False)
                self.sequence_buttons[i]['delete'].setEnabled(False)

    def edit_sequence(self, index):
        """Load a sequence for editing."""
        if index < len(self.sequence_list):
            self.editing_index = index
            # Load the sequence into current_sequence
            self.current_sequence = self.sequence_list[index].split()
            self.sequence_input.setText(" ".join(self.current_sequence))
            self.update_buttons()

    def move_sequence_up(self, index):
        """Move sequence up in the list."""
        if index > 0 and index < len(self.sequence_list):
            self.sequence_list[index], self.sequence_list[index - 1] = \
                self.sequence_list[index - 1], self.sequence_list[index]
            self.update_sequence_buttons()

    def move_sequence_down(self, index):
        """Move sequence down in the list."""
        if index < len(self.sequence_list) - 1:
            self.sequence_list[index], self.sequence_list[index + 1] = \
                self.sequence_list[index + 1], self.sequence_list[index]
            self.update_sequence_buttons()

    def delete_sequence(self, index):
        """Delete a sequence from the list."""
        if index < len(self.sequence_list):
            self.sequence_list.pop(index)
            # Clear editing if we're editing this sequence
            if self.editing_index == index:
                self.editing_index = None
                self.current_sequence = []
                self.sequence_input.setText("")
            elif self.editing_index is not None and self.editing_index > index:
                # Adjust editing index if needed
                self.editing_index -= 1
            self.update_sequence_buttons()
            self.update_buttons()

    def add_to_sequence(self, value):
        """Add a move to the current sequence."""
        if len(self.current_sequence) < 9:
            self.current_sequence.append(value)
            self.sequence_input.setText(" ".join(self.current_sequence))
            self.update_buttons()

    def backspace_sequence(self):
        """Remove the last item from current sequence."""
        if self.current_sequence:
            self.current_sequence.pop()
            self.sequence_input.setText(" ".join(self.current_sequence))
            self.update_buttons()

    def confirm_sequence(self):
        """Add current sequence to the sequence list or update existing."""
        if 1 <= len(self.current_sequence) <= 9:
            sequence_str = " ".join(self.current_sequence)
            
            if self.editing_index is not None:
                # Update existing sequence
                self.sequence_list[self.editing_index] = sequence_str
                self.editing_index = None
            elif len(self.sequence_list) < 5:
                # Add new sequence
                self.sequence_list.append(sequence_str)
            
            self.current_sequence = []
            self.sequence_input.setText("")
            self.update_sequence_buttons()
            self.update_buttons()

    def update_buttons(self):
        """Update button states based on current input."""
        # Confirm button: enabled if 1-9 items
        sequence_valid = 1 <= len(self.current_sequence) <= 9
        
        if self.editing_index is not None:
            # Editing mode - always allow confirm
            self.confirm_btn.setEnabled(sequence_valid)
        else:
            # Adding mode - check if we can add more
            can_add_more = len(self.sequence_list) < 5
            self.confirm_btn.setEnabled(sequence_valid and can_add_more)
        
        # Next button: enabled if at least one sequence exists
        self.next_btn.setEnabled(len(self.sequence_list) >= 1)

    def on_back_clicked(self):
        """Go back to Punch Combination page."""
        # Reset state
        self.current_sequence = []
        self.sequence_list = []
        self.editing_index = None
        self.sequence_input.setText("")
        self.update_sequence_buttons()
        self.update_buttons()
        self.navigate_to(PageIndex.PUNCH_COMBINATIONS)

    def on_next_clicked(self):
        """Go to Basic Parameters page."""
        if len(self.sequence_list) >= 1:
            # Store sequences via app_state
            if self.app_state:
                self.app_state.set_sequences(self.sequence_list.copy())
                try:
                    basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                    basic_page.update_button_displays()
                except Exception:
                    pass
            else:
                try:
                    basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                    basic_page.custom_sequences = self.sequence_list.copy()
                except Exception:
                    pass
            self.navigate_to(PageIndex.BASIC_PARAMETERS)

class SparPage(ButtonNavigationMixin, QWidget):
    """Page with Spar options."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Spar")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        sparring_btn = QPushButton("Sparring")
        battle_btn = QPushButton("Battle")
        back_btn = QPushButton("Back")

        sparring_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        battle_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        sparring_btn.clicked.connect(self.on_sparring_clicked)
        battle_btn.clicked.connect(self.on_battle_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(sparring_btn, alignment=Qt.AlignCenter)
        layout.addWidget(battle_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setup_navigation([sparring_btn, battle_btn, back_btn])

    def on_sparring_clicked(self):
        self.navigate_to(PageIndex.SPAR_STYLE_SELECT)

    def on_battle_clicked(self):
        # BattlePage index moved to 13 after removing defense page
        self.navigate_to(PageIndex.BATTLE)

    def on_back_clicked(self):
        self.navigate_to(PageIndex.TRAINING)

class BattlePage(ButtonNavigationMixin, QWidget):
    NAV_BUTTON_MIN_WIDTH = 225
    NAV_BUTTON_MAX_WIDTH = 420
    NAV_BUTTON_MIN_HEIGHT = 65
    NAV_BUTTON_STYLE = """
        QPushButton {
            font-size: 18px;
            padding: 15px;
            background-color: #f5f5f5;
            border: 3px solid #cccccc;
            border-radius: 10px;
            min-height: 65px;
            color: #111111;
        }
        QPushButton:focus {
            border: 6px solid #00ff00;
            background-color: #2d5016;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e8e8e8;
        }
    """

    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        title = QLabel("Battle")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold;")

        pressure_btn = QPushButton("Pressure Fighter")
        counter_btn = QPushButton("Counter Puncher")
        infighter_btn = QPushButton("Infighter")
        outboxer_btn = QPushButton("Out Boxer")
        random_btn = QPushButton("Random")
        back_btn = QPushButton("Back")

        style_buttons = [pressure_btn, counter_btn, infighter_btn, outboxer_btn, random_btn]
        for button in style_buttons:
            button.setStyleSheet(self.NAV_BUTTON_STYLE)
            button.setFocusPolicy(Qt.StrongFocus)

        back_btn.setStyleSheet(self.NAV_BUTTON_STYLE)
        back_btn.setFocusPolicy(Qt.StrongFocus)

        self.navigation_buttons = style_buttons + [back_btn]
        self.setup_navigation(self.navigation_buttons)

        for button in style_buttons:
            button.setFixedSize(225, 65)

        back_btn.setMinimumWidth(200)
        back_btn.setMinimumHeight(60)

        # --- Alternative approach: Use HBoxLayouts for both rows ---
        # Row 0: Pressure Fighter, Counter Puncher, Infighter
        row0_layout = QHBoxLayout()
        row0_layout.setSpacing(15)
        row0_layout.addWidget(pressure_btn)
        row0_layout.addWidget(counter_btn)
        row0_layout.addWidget(infighter_btn)

        # Row 1: Out Boxer, Random (centered)
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(15)
        row1_layout.addStretch()
        row1_layout.addWidget(outboxer_btn)
        row1_layout.addWidget(random_btn)
        row1_layout.addStretch()

        # wire clicks
        pressure_btn.clicked.connect(lambda: self.on_style_clicked("Pressure Fighter"))
        counter_btn.clicked.connect(lambda: self.on_style_clicked("Counter Puncher"))
        infighter_btn.clicked.connect(lambda: self.on_style_clicked("Infighter"))
        outboxer_btn.clicked.connect(lambda: self.on_style_clicked("Out Boxer"))
        random_btn.clicked.connect(lambda: self.on_style_clicked("Random"))
        back_btn.clicked.connect(self.on_back_clicked)

        # Layout assembly
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)
        main_layout.addStretch(1)  # Top stretch
        main_layout.addWidget(title)
        main_layout.addSpacing(30)
        main_layout.addLayout(row0_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(row1_layout)
        main_layout.addSpacing(30)
        main_layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)  # Bottom stretch

        self.setLayout(main_layout)

    def on_style_clicked(self, style):
        """Navigate to style description page."""
        print(f"{style} selected")
        desc_page = self.stacked_widget.widget(PageIndex.BATTLE_STYLE_DESC)
        if isinstance(desc_page, BattleStyleDescriptionPage):
            desc_page.set_style_info(style)
        self.navigate_to(PageIndex.BATTLE_STYLE_DESC)

    def on_back_clicked(self):
        self.navigate_to(PageIndex.SPAR)


class BattleStyleDescriptionPage(ButtonNavigationMixin, QWidget):
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        self.selected_style = ""

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        self.style_title = QLabel("")
        self.style_title.setAlignment(Qt.AlignCenter)
        self.style_title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 10px;")

        self.description_label = QLabel("")
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("""
            font-size: 18px;
            padding: 25px;
            background-color: #f5f5f5;
            border: 2px solid #cccccc;
            border-radius: 10px;
            line-height: 1.6;
            color: #000000;
            text-align: center;
            max-width: 900px;
            min-width: 800px;
        """)

        continue_btn = QPushButton("Continue to Training")
        back_btn = QPushButton("Back")

        continue_btn.setMinimumSize(250, 60)
        back_btn.setMinimumSize(200, 60)

        continue_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        continue_btn.clicked.connect(self.on_continue_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addWidget(back_btn)
        button_layout.addWidget(continue_btn)

        layout.addWidget(self.style_title)
        layout.addSpacing(15)
        layout.addWidget(self.description_label, alignment=Qt.AlignCenter)
        layout.addSpacing(25)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def set_style_info(self, style):
        """Set the fighting style and show description."""
        self.selected_style = style
        self.style_title.setText(style)

        descriptions = {
            "Pressure Fighter": "Aggressive style that constantly moves forward, applying pressure with high-volume punches. Wears down opponents through relentless attacks and cuts off the ring.",
            "Counter Puncher": "Defensive style that waits for opponents to attack, then counters with precise punches. Relies on timing, reflexes, and exploiting openings.",
            "Infighter": "Close-range specialist who fights inside, using hooks and uppercuts. Excels at close-quarters combat with head movement and body shots.",
            "Out Boxer": "Technical style using footwork and reach advantage. Maintains distance with jabs and straight punches, avoiding close exchanges.",
            "Random": "Unpredictable mixed style that randomly combines elements from all fighting styles. Keeps you guessing!",
        }

        self.description_label.setText(descriptions.get(style, "Select your fighting style."))

    def on_continue_clicked(self):
        if self.app_state:
            self.app_state.update_battle_style(self.selected_style)
            self.app_state.update_difficulty("Battle")
            self.app_state.previous_page = PageIndex.BATTLE_STYLE_DESC
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.selected_battle_style = self.selected_style
                basic_page.selected_difficulty = "Battle"
                basic_page.previous_page = PageIndex.BATTLE_STYLE_DESC
            except Exception:
                pass
        self.navigate_to(PageIndex.BASIC_PARAMETERS)

    def on_back_clicked(self):
        self.navigate_to(PageIndex.BATTLE)


class ComboLLMChatPage(ButtonNavigationMixin, QWidget):
    """Simplified LLM chat page for post-training combo feedback."""
    
    def __init__(self, stacked_widget, app_state):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        self._worker = None
        self._current_reply_cursor = None
        self.combo_data = {}
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("AI Coach Feedback")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #4CAF50;")
        
        # Score and combo info (compact)
        info_layout = QHBoxLayout()
        self.combo_info_label = QLabel("Combo: - | Score: -/5")
        self.combo_info_label.setAlignment(Qt.AlignCenter)
        self.combo_info_label.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")
        info_layout.addWidget(self.combo_info_label)
        
        # Chat display area
        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        self.chat_view.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #e6e6e6;
                font-size: 14px;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.chat_view.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Input row
        input_row = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ask the AI coach about the combo...")
        self.user_input.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: white;
                font-size: 14px;
                padding: 10px;
                border: 1px solid #444;
                border-radius: 6px;
            }
        """)
        self.user_input.returnPressed.connect(self._send_user_message)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        self.send_btn.clicked.connect(self._send_user_message)
        
        input_row.addWidget(self.user_input, stretch=4)
        input_row.addWidget(self.send_btn, stretch=1)
        
        # Buttons row
        buttons_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear Chat")
        self.clear_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        self.clear_btn.clicked.connect(self._clear_chat)
        
        continue_btn = QPushButton("Continue")
        continue_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        continue_btn.clicked.connect(self._continue_to_results)
        
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(continue_btn)
        
        # Assembly
        main_layout.addWidget(title)
        main_layout.addLayout(info_layout)
        main_layout.addWidget(self.chat_view, stretch=1)
        main_layout.addLayout(input_row)
        main_layout.addSpacing(10)
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
    
    def set_combo_data(self, combo_name, combo_sequence, score, difficulty, rounds):
        """Set the combo data and trigger initial AI feedback."""
        print(f"[DEBUG] ComboLLMChatPage.set_combo_data called: {combo_name}, score={score}")
        self.combo_data = {
            'combo_name': combo_name,
            'combo_sequence': combo_sequence,
            'score': score,
            'difficulty': difficulty,
            'rounds': rounds
        }
        
        # Update info label
        self.combo_info_label.setText(f"Combo: {combo_name} | Score: {score}/5")
        print(f"[DEBUG] Updated info label, clearing chat...")
        
        # Clear chat and send initial prompt
        self.chat_view.clear()
        self._send_initial_prompt()
        print(f"[DEBUG] Initial prompt sent")
    
    def _send_initial_prompt(self):
        """Send initial AI prompt about the combo performance."""
        combo_name = self.combo_data.get('combo_name', 'Unknown')
        combo_sequence = self.combo_data.get('combo_sequence', '')
        score = self.combo_data.get('score', 0)
        difficulty = self.combo_data.get('difficulty', 'Beginner')
        
        # Create initial prompt
        prompt = (f"User just completed {combo_name} ({combo_sequence}) combo "
                  f"at {difficulty} difficulty and scored {score}/5. "
                  f"Give them brief encouraging feedback and one practical tip in 2-3 sentences.")
        
        self._append_chat("System", f"Analyzing your {combo_name} performance...")
        self._generate_ai_response(prompt)
    
    def _send_user_message(self):
        """Handle user sending a custom question."""
        text = self.user_input.text().strip()
        if not text:
            return
        
        self.user_input.clear()
        self._append_chat("You", text)
        
        # Build context-aware prompt
        combo_name = self.combo_data.get('combo_name', '')
        combo_sequence = self.combo_data.get('combo_sequence', '')
        score = self.combo_data.get('score', 0)
        
        prompt = (f"Context: User trained {combo_name} ({combo_sequence}) and scored {score}/5. "
                  f"User question: {text}. "
                  f"Provide a concise, helpful answer as a boxing coach in 2-3 sentences.")
        
        self._generate_ai_response(prompt)
    
    def _generate_ai_response(self, prompt):
        """Generate AI response (placeholder - prints to chat)."""
        # Placeholder implementation: Generate a simple response without using actual LLM
        # In a real implementation, this would call the LLM model
        
        combo_name = self.combo_data.get('combo_name', 'this combo')
        score = self.combo_data.get('score', 0)
        
        # Generate contextual response based on score
        if score >= 4:
            responses = [
                f"Excellent work on {combo_name}! Your technique is solid. Focus on increasing speed while maintaining this accuracy.",
                f"Great score! You've mastered the basics of {combo_name}. Try mixing it with other combos to improve flow.",
                f"Outstanding performance! Keep practicing {combo_name} at higher speeds to build muscle memory.",
            ]
        elif score >= 3:
            responses = [
                f"Good effort on {combo_name}! You're on the right track. Focus on clean transitions between punches.",
                f"Decent score! For {combo_name}, remember to keep your guard up between punches. Practice slowly first.",
                f"You're improving! With {combo_name}, focus on hip rotation and weight transfer for more power.",
            ]
        else:
            responses = [
                f"Keep practicing {combo_name}! Break it down into individual punches first, then combine them slowly.",
                f"Don't worry, {combo_name} takes time. Focus on form over speed. Watch your footwork.",
                f"Good try! For {combo_name}, practice each punch separately, then gradually increase combo speed.",
            ]
        
        import random
        response = random.choice(responses)
        
        # Simulate typing delay
        QTimer.singleShot(500, lambda: self._append_chat("AI Coach", response))
    
    def _append_chat(self, who, text):
        """Append a message to the chat view."""
        cursor = self.chat_view.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        if who == "System":
            cursor.insertHtml(f"<p style='color:#888;'><i>{text}</i></p>")
        elif who == "You":
            cursor.insertHtml(f"<p><b style='color:#2196F3;'>You:</b> {text}</p>")
        else:  # AI Coach
            cursor.insertHtml(f"<p><b style='color:#4CAF50;'>AI Coach:</b> {text}</p>")
        
        self.chat_view.ensureCursorVisible()
    
    def _clear_chat(self):
        """Clear the chat and restart with initial prompt."""
        self.chat_view.clear()
        self._send_initial_prompt()
    
    def _continue_to_results(self):
        """Move to the combo results page."""
        # Pass data to results page
        results_page = self.stacked_widget.widget(PageIndex.COMBO_RESULTS)
        if results_page:
            results_page.set_results(
                self.combo_data['combo_name'],
                self.combo_data['combo_sequence'],
                self.combo_data['score'],
                self.combo_data['difficulty'],
                self.combo_data['rounds']
            )
        self.navigate_to(PageIndex.COMBO_RESULTS)


class ComboResultsPage(ButtonNavigationMixin, QWidget):
    """Page showing combo training results with score and progress."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(30, 20, 30, 20)
        
        # Title
        title = QLabel("Training Complete!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #4CAF50;")
        
        # Combo info
        self.combo_name_label = QLabel("Combo: -")
        self.combo_name_label.setAlignment(Qt.AlignCenter)
        self.combo_name_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        
        self.combo_sequence_label = QLabel("Sequence: -")
        self.combo_sequence_label.setAlignment(Qt.AlignCenter)
        self.combo_sequence_label.setStyleSheet("font-size: 20px; color: white;")
        
        # Score display
        self.score_label = QLabel("Score: 0.0/5.0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #2196F3;")
        
        # Status message
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; color: #FFC107;")
        
        # Details
        self.details_label = QLabel("")
        self.details_label.setAlignment(Qt.AlignCenter)
        self.details_label.setStyleSheet("font-size: 16px; color: white;")
        
        # Continue button
        continue_btn = QPushButton("Continue Training")
        continue_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        continue_btn.clicked.connect(lambda: self.navigate_to(PageIndex.BASIC_PARAMETERS))
        
        # Assembly
        main_layout.addStretch()
        main_layout.addWidget(title)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.combo_name_label)
        main_layout.addWidget(self.combo_sequence_label)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.score_label)
        main_layout.addSpacing(5)
        main_layout.addWidget(self.status_label)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.details_label)
        main_layout.addSpacing(15)
        main_layout.addWidget(continue_btn)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def set_results(self, combo_name, combo_sequence, score, difficulty, rounds):
        """Display the training results."""
        self.combo_name_label.setText(f"Combo: {combo_name}")
        self.combo_sequence_label.setText(f"Sequence: {combo_sequence}")
        self.score_label.setText(f"Score: {score}/5")
        
        # Determine performance message
        if difficulty == "Beginner":
            threshold = 3
            threshold_text = "3"
        else:  # Intermediate or Advanced
            threshold = 4
            threshold_text = "4"
        
        if score >= threshold:
            self.status_label.setText("✓ Great Job! Combo performance recorded!")
            self.status_label.setStyleSheet("font-size: 18px; color: #4CAF50; font-weight: bold;")
        else:
            self.status_label.setText(f"Keep practicing! Target: {threshold_text}/5")
            self.status_label.setStyleSheet("font-size: 18px; color: #FFC107; font-weight: bold;")
        
        self.details_label.setText(f"{difficulty} Level • {rounds} Rounds Completed")


class UserComboProgressPage(ButtonNavigationMixin, QWidget):
    """Page showing a user's combo progress and mastery status."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_user = None
        self.return_to_page = PageIndex.HOMEPAGE  # Track where to return to
        self.db_path = SHARED_DB_PATH
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(50, 30, 50, 30)
        
        # Title
        title_layout = QHBoxLayout()
        self.title_label = QLabel("Combo Progress")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        title_layout.addWidget(self.title_label)
        
        # Difficulty tabs
        tab_layout = QHBoxLayout()
        tab_layout.setSpacing(10)
        tab_layout.addStretch()
        
        self.difficulty_buttons = {}
        for difficulty in ["Beginner", "Intermediate", "Advanced"]:
            btn = QPushButton(difficulty)
            btn.setStyleSheet(ButtonStyle.TRACK_MEDIUM)
            btn.setFixedSize(150, 40)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, d=difficulty: self.show_difficulty(d))
            self.difficulty_buttons[difficulty] = btn
            tab_layout.addWidget(btn)
        
        tab_layout.addStretch()
        
        # Combo progress table
        self.combo_table = QTableWidget()
        self.combo_table.setColumnCount(5)
        self.combo_table.setHorizontalHeaderLabels(["Combo", "Sequence", "Mastery", "Attempts", "Status"])
        self.combo_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.combo_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.combo_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.combo_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.combo_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.combo_table.setColumnWidth(2, 120)
        self.combo_table.setColumnWidth(3, 90)
        self.combo_table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: white;
                color: black;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
        """)
        
        # Progress summary
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(30)
        
        self.total_label = QLabel("Total: 0")
        self.mastered_label = QLabel("Mastered: 0")
        self.in_progress_label = QLabel("In Progress: 0")
        self.struggling_label = QLabel("Struggling: 0")
        
        for label in [self.total_label, self.mastered_label, self.in_progress_label, self.struggling_label]:
            label.setStyleSheet("font-size: 14px; color: white; font-weight: bold;")
        
        summary_layout.addWidget(self.total_label)
        summary_layout.addWidget(self.mastered_label)
        summary_layout.addWidget(self.in_progress_label)
        summary_layout.addWidget(self.struggling_label)
        summary_layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        refresh_btn = QPushButton("Refresh")
        back_btn = QPushButton("Back to Home")
        
        refresh_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        back_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        
        refresh_btn.setFixedSize(150, 45)
        back_btn.setFixedSize(150, 45)
        
        refresh_btn.clicked.connect(self.refresh_progress)
        back_btn.clicked.connect(self.on_back_clicked)
        
        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        
        # Assembly
        main_layout.addLayout(title_layout)
        main_layout.addLayout(tab_layout)
        main_layout.addWidget(self.combo_table)
        main_layout.addLayout(summary_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        self.current_difficulty = "Beginner"
    
    def set_user(self, username, return_to_page=None):
        """Set the user to display progress for."""
        self.current_user = username
        self.db_path = get_user_db_path(username)
        if return_to_page is not None:
            self.return_to_page = return_to_page
        self.title_label.setText(f"Combo Progress - {username}")
        self.refresh_progress()
    
    def show_difficulty(self, difficulty):
        """Show combos for selected difficulty."""
        self.current_difficulty = difficulty
        # Update button states
        for d, btn in self.difficulty_buttons.items():
            btn.setChecked(d == difficulty)
        self.load_difficulty_data(difficulty)
    
    def refresh_progress(self):
        """Refresh progress data."""
        if self.current_user:
            self.show_difficulty(self.current_difficulty)
    
    def on_back_clicked(self):
        """Return to the page we came from."""
        self.stacked_widget.setCurrentIndex(self.return_to_page)
    
    def load_difficulty_data(self, difficulty):
        """Load and display combo data for a difficulty."""
        try:
            from combo_curriculum import ComboCurriculum
            
            with ComboCurriculum(self.db_path) as curriculum:
                # Get all combos with progress
                all_combos = curriculum.get_all_combos_with_progress()
                combos = all_combos.get(difficulty, [])
                
                # Get progress summary
                progress = curriculum.get_level_progress(difficulty)
                
                # Update summary labels
                self.total_label.setText(f"Total: {progress['total_combos']}")
                self.mastered_label.setText(f"Mastered: {progress['mastered_combos']}")
                self.in_progress_label.setText(f"In Progress: {progress['in_progress_combos']}")
                self.struggling_label.setText(f"Struggling: {progress['struggling_combos']}")
                
                # Populate table
                self.combo_table.setRowCount(len(combos))
                for row, combo in enumerate(combos):
                    # Combo name
                    name_item = QTableWidgetItem(combo['combo_name'])
                    name_item.setTextAlignment(Qt.AlignCenter)
                    self.combo_table.setItem(row, 0, name_item)
                    
                    # Sequence
                    seq_item = QTableWidgetItem(str(combo['combo_sequence']))
                    seq_item.setTextAlignment(Qt.AlignCenter)
                    self.combo_table.setItem(row, 1, seq_item)
                    
                    # Mastery score is already on 0-5 scale
                    mastery = combo['mastery_score'] if combo['mastery_score'] else 0.0
                    mastery_display = mastery
                    mastery_item = QTableWidgetItem(f"{mastery_display:.1f}/5.0")
                    mastery_item.setTextAlignment(Qt.AlignCenter)
                    self.combo_table.setItem(row, 2, mastery_item)
                    
                    # Attempts
                    attempts_item = QTableWidgetItem(str(combo['total_attempts'] or 0))
                    attempts_item.setTextAlignment(Qt.AlignCenter)
                    self.combo_table.setItem(row, 3, attempts_item)
                    
                    # Status
                    if combo['is_mastered']:
                        status = "✓ Mastered"
                        status_item = QTableWidgetItem(status)
                        status_item.setBackground(Qt.green)
                    elif combo['total_attempts'] == 0:
                        status = "Not Started"
                        status_item = QTableWidgetItem(status)
                    else:
                        status = "Learning"
                        status_item = QTableWidgetItem(status)
                    status_item.setTextAlignment(Qt.AlignCenter)
                    self.combo_table.setItem(row, 4, status_item)
                    
                self.combo_table.resizeRowsToContents()
                
        except Exception as e:
            print(f"Error loading combo progress: {e}")
            self.combo_table.setRowCount(0)


class UserProgressOverviewPage(ButtonNavigationMixin, QWidget):
    """Page showing all users' combo progress overview from user management."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db_path = SHARED_DB_PATH
        self.selected_user = None
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 30, 50, 30)
        
        # Title
        title = QLabel("User Combo Progress Overview")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        
        # User selection table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(["Username", "Beginner", "Intermediate", "Advanced", "Overall", "View Details"])
        for i in range(6):
            self.user_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        self.user_table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: white;
                color: black;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
        """)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        refresh_btn = QPushButton("Refresh")
        back_btn = QPushButton("Back to Users")
        
        refresh_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        back_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        
        refresh_btn.setFixedSize(150, 45)
        back_btn.setFixedSize(150, 45)
        
        refresh_btn.clicked.connect(self.refresh_users)
        back_btn.clicked.connect(lambda: self.navigate_to(PageIndex.USER_MANAGEMENT))
        
        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        
        # Assembly
        main_layout.addWidget(title)
        main_layout.addWidget(self.user_table)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def showEvent(self, event):
        """Refresh when page is shown."""
        super().showEvent(event)
        self.refresh_users()
    
    def refresh_users(self):
        """Load and display all users with their combo progress."""
        try:
            from combo_curriculum import ComboCurriculum
            
            users = load_users()
            self.user_table.setRowCount(len(users))

            for row, username in enumerate(users.keys()):
                # Username
                user_item = QTableWidgetItem(username)
                user_item.setTextAlignment(Qt.AlignCenter)
                self.user_table.setItem(row, 0, user_item)

                user_db_path = get_user_db_path(username)
                with ComboCurriculum(user_db_path) as curriculum:
                    # Get progress for each difficulty
                    col = 1
                    for difficulty in ["Beginner", "Intermediate", "Advanced"]:
                        progress = curriculum.get_level_progress(difficulty)
                        total = progress['total_combos']
                        mastered = progress['mastered_combos']
                        pct = (mastered / total * 100) if total > 0 else 0
                        progress_text = f"{mastered}/{total} ({pct:.0f}%)"

                        progress_item = QTableWidgetItem(progress_text)
                        progress_item.setTextAlignment(Qt.AlignCenter)
                        if mastered == total and total > 0:
                            progress_item.setBackground(Qt.darkGreen)
                            progress_item.setForeground(Qt.white)
                        elif mastered > 0:
                            progress_item.setBackground(Qt.darkYellow)
                            progress_item.setForeground(Qt.white)
                        self.user_table.setItem(row, col, progress_item)
                        col += 1

                    total_all = 0
                    mastered_all = 0
                    for difficulty in ["Beginner", "Intermediate", "Advanced"]:
                        progress = curriculum.get_level_progress(difficulty)
                        total_all += progress['total_combos']
                        mastered_all += progress['mastered_combos']

                    overall_pct = (mastered_all / total_all * 100) if total_all > 0 else 0
                    overall_item = QTableWidgetItem(f"{overall_pct:.1f}%")
                    overall_item.setTextAlignment(Qt.AlignCenter)
                    self.user_table.setItem(row, 4, overall_item)

                # View details button
                view_btn = QPushButton("View")
                view_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 8px 16px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                """)
                view_btn.clicked.connect(lambda checked, u=username: self.view_user_details(u))
                self.user_table.setCellWidget(row, 5, view_btn)
            
            self.user_table.resizeRowsToContents()
        
        except Exception as e:
            print(f"Error refreshing users: {e}")
    
    def view_user_details(self, username):
        """Navigate to detailed user combo progress."""
        # Find the UserComboProgressPage and set user
        for i in range(self.stacked_widget.count()):
            page = self.stacked_widget.widget(i)
            if hasattr(page, '__class__') and page.__class__.__name__ == 'UserComboProgressPage':
                page.set_user(username, return_to_page=PageIndex.USER_PROGRESS_OVERVIEW)
                self.stacked_widget.setCurrentIndex(i)
                break


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boxing Training App")
        self.setFixedSize(1024, 600)
        self.setFocusPolicy(Qt.StrongFocus)

        self.arduino_button_listener: Optional[ArduinoButtonListener] = None
        self._arduino_buttons_suspended = False
        self._arduino_runtime_status = "starting"
        self._serial_exclusive_pages: Set[int] = {
            PageIndex.POWER_INSTRUCTIONS,
            PageIndex.POWER_PUNCH,
            PageIndex.STAMINA_INSTRUCTIONS,
            PageIndex.STAMINA_TEST,
        }

        self._arduino_watchdog_timer = QTimer(self)
        watchdog_ms = _env_int("ARDUINO_BUTTON_WATCHDOG_MS", 5000)
        self._arduino_watchdog_timer.setInterval(max(1000, watchdog_ms))
        self._arduino_watchdog_timer.timeout.connect(self._watchdog_arduino_button_listener)

        # Auto-setup database on first run
        self._ensure_database_setup()
        
        self.previous_page = PageIndex.LOGIN  # Track the previous page
        self.navigation_stack: List[int] = []
        self._navigating_back = False

        self.stacked_widget = QStackedWidget()
        self.app_state = AppState(initial_page=PageIndex.HOMEPAGE)

        # Create pages
        self.homepage = Homepage(self.stacked_widget)
        self.training_page = TrainingPage(self.stacked_widget)
        self.techniques_page = TechniquesPage(self.stacked_widget)
        self.punch_combinations_page = PunchCombinationPage(self.stacked_widget, self.app_state)
        self.basic_parameters_page = BasicParametersPage(self.stacked_widget, self.app_state)
        self.round_selection_page = RoundSelectionPage(self.stacked_widget, self.app_state)
        self.speed_selection_page = SpeedSelectionPage(self.stacked_widget, self.app_state)
        self.time_selection_page = TimeSelectionPage(self.stacked_widget, self.app_state)
        self.rest_selection_page = RestSelectionPage(self.stacked_widget, self.app_state)
        self.countdown_page = CountdownPage(self.stacked_widget)
        self.training_session_page = TrainingSessionPage(self.stacked_widget, self.app_state)
        self.self_select_sequence_page = SelfSelectSequencePage(self.stacked_widget, self.app_state)
        self.spar_page = SparPage(self.stacked_widget)
        self.battle_page = BattlePage(self.stacked_widget, self.app_state)
        self.battle_style_description_page = BattleStyleDescriptionPage(self.stacked_widget, self.app_state)
        self.spar_style_select_page = SparStyleSelectPage(self.stacked_widget)
        self.spar_round_config_page = SparRoundConfigPage(self.stacked_widget)
        self.spar_countdown_page    = SparCountdownPage(self.stacked_widget)
        self.spar_session_page      = SparSessionPage(self.stacked_widget)
        self.spar_rest_page         = SparRestPage(self.stacked_widget)
        self.spar_processing_page   = SparProcessingPage(self.stacked_widget)
        self.spar_result_page       = SparResultPage(self.stacked_widget)

        # Login and User Management pages
        self.login_page = LoginPage(self.stacked_widget, self.app_state)
        self.user_management_page = UserManagementPage(self.stacked_widget)
        self.user_combo_progress_page = UserComboProgressPage(self.stacked_widget)
        self.user_progress_overview_page = UserProgressOverviewPage(self.stacked_widget)
        self.combo_results_page = ComboResultsPage(self.stacked_widget)
        self.combo_llm_chat_page = ComboLLMChatPage(self.stacked_widget, self.app_state)

        # Wire countdown completion to start the training session
        self.countdown_page.on_finished = self.start_training_session

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.homepage)                    # 0
        self.stacked_widget.addWidget(self.training_page)               # 1
        self.stacked_widget.addWidget(self.techniques_page)             # 2
        self.stacked_widget.addWidget(self.punch_combinations_page)     # 3
        self.stacked_widget.addWidget(self.basic_parameters_page)       # 4
        self.stacked_widget.addWidget(self.round_selection_page)        # 5
        self.stacked_widget.addWidget(self.speed_selection_page)        # 6
        self.stacked_widget.addWidget(self.time_selection_page)         # 7
        self.stacked_widget.addWidget(self.rest_selection_page)         # 8
        self.stacked_widget.addWidget(self.countdown_page)              # 9
        self.stacked_widget.addWidget(self.training_session_page)       # 10
        self.stacked_widget.addWidget(self.self_select_sequence_page)   # 11
        self.stacked_widget.addWidget(self.spar_page)                   # 12
        self.stacked_widget.addWidget(self.battle_page)                 # 13
        self.stacked_widget.addWidget(self.performance_page)            # 14
        self.stacked_widget.addWidget(self.power_instructions_page)     # 15
        self.stacked_widget.addWidget(self.power_punch_page)            # 16
        self.stacked_widget.addWidget(self.power_result_page)           # 17
        self.stacked_widget.addWidget(self.stamina_instructions_page)   # 18
        self.stacked_widget.addWidget(self.reaction_instructions_page)  # 19
        self.stacked_widget.addWidget(self.reaction_test_page)          # 20
        self.stacked_widget.addWidget(self.reaction_result_page)        # 21
        self.stacked_widget.addWidget(self.others_page)                 # 22
        self.stacked_widget.addWidget(self.login_page)                  # 23
        self.stacked_widget.addWidget(self.user_management_page)        # 24
        self.stacked_widget.addWidget(self.user_combo_progress_page)    # 25
        self.stacked_widget.addWidget(self.user_progress_overview_page) # 26
        self.stacked_widget.addWidget(self.combo_results_page)          # 27
        self.stacked_widget.addWidget(self.combo_llm_chat_page)         # 28
        self.stacked_widget.addWidget(self.stamina_test_page)           # 29
        self.stacked_widget.addWidget(self.stamina_result_page)         # 30
        self.stacked_widget.addWidget(QWidget())                        # 31 reserved (STAMINA_HISTORY)
        self.stacked_widget.addWidget(self.performance_history_page)    # 32
        self.stacked_widget.addWidget(self.battle_style_description_page) # 33
        self.stacked_widget.addWidget(self.spar_style_select_page)      # 34
        self.stacked_widget.addWidget(self.spar_round_config_page)      # 35
        self.stacked_widget.addWidget(self.spar_countdown_page)         # 36
        self.stacked_widget.addWidget(self.spar_session_page)           # 37
        self.stacked_widget.addWidget(self.spar_rest_page)              # 38
        self.stacked_widget.addWidget(self.spar_processing_page)        # 39
        self.stacked_widget.addWidget(self.spar_result_page)            # 40

        # Connect stack widget page changes to update user references
        self.stacked_widget.currentChanged.connect(self.on_page_changed)

        # Start on the login page
        self.stacked_widget.setCurrentIndex(PageIndex.LOGIN)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self._normalize_page_layouts()
        self._setup_page_button_navigation()
        self.update_back_button_visibility()
        self._start_arduino_button_listener()
        self._arduino_watchdog_timer.start()

    def _normalize_page_layouts(self):
        """Apply consistent spacing and margins for balanced 1024x600 button layouts."""
        for index in range(self.stacked_widget.count()):
            page = self.stacked_widget.widget(index)
            if page is None:
                continue

            page_layout = page.layout()
            if page_layout is None:
                continue

            spacing = getattr(page, "LAYOUT_SPACING", 20)
            margins = getattr(page, "LAYOUT_MARGINS", (60, 40, 60, 40))

            page_layout.setSpacing(spacing)
            if isinstance(margins, tuple) and len(margins) == 4:
                page_layout.setContentsMargins(*margins)
            else:
                page_layout.setContentsMargins(60, 40, 60, 40)

    def _setup_page_button_navigation(self):
        """Apply mixin navigation setup to all pages with QPushButtons."""
        for index in range(self.stacked_widget.count()):
            page = self.stacked_widget.widget(index)
            if not isinstance(page, ButtonNavigationMixin):
                continue

            if isinstance(page, OthersPage):
                continue

            if isinstance(page, SelfSelectSequencePage):
                continue

            if isinstance(page, BattlePage):
                continue

            explicit_buttons = getattr(page, "navigation_buttons", None)
            if explicit_buttons is None:
                explicit_buttons = getattr(page, "_nav_buttons", None)

            if explicit_buttons:
                buttons = [button for button in explicit_buttons if isinstance(button, QPushButton)]
            else:
                buttons = [button for button in page.findChildren(QPushButton)]

            if buttons:
                page.setup_navigation(buttons)

    def _start_arduino_button_listener(self):
        """Start background listener for Arduino button commands."""
        if not _env_bool("ARDUINO_BUTTONS_ENABLED", True):
            self._arduino_runtime_status = "disabled"
            self._notify_arduino_status_change("Disabled by ARDUINO_BUTTONS_ENABLED")
            return

        self._arduino_runtime_status = "starting"

        port = os.getenv("ARDUINO_BUTTON_PORT", "").strip() or None
        baudrate = _env_int("ARDUINO_BUTTON_BAUD", 115200)
        debounce_ms = _env_int("ARDUINO_BUTTON_DEBOUNCE_MS", 120)
        serial_timeout_s = _env_float("ARDUINO_BUTTON_TIMEOUT_SEC", 0.05)
        startup_delay_s = _env_float("ARDUINO_BUTTON_STARTUP_DELAY_SEC", 1.2)
        reconnect_interval_s = _env_float("ARDUINO_BUTTON_RECONNECT_SEC", 2.0)

        self.arduino_button_listener = ArduinoButtonListener(
            port=port,
            baudrate=baudrate,
            debounce_ms=debounce_ms,
            serial_timeout_s=serial_timeout_s,
            startup_delay_s=startup_delay_s,
            reconnect_interval_s=reconnect_interval_s,
            parent=self,
        )
        self.arduino_button_listener.button_pressed.connect(self._handle_arduino_button_command)
        self.arduino_button_listener.status.connect(self._on_arduino_button_status)
        self.arduino_button_listener.start()

    def restart_arduino_button_listener(self):
        """Restart button listener after runtime config changes."""
        if self.arduino_button_listener and self.arduino_button_listener.isRunning():
            self.arduino_button_listener.stop()
            self.arduino_button_listener.wait(1000)
        self.arduino_button_listener = None
        if not self._arduino_buttons_suspended:
            self._start_arduino_button_listener()

    def _suspend_arduino_button_listener(self):
        if self._arduino_buttons_suspended:
            return
        self._arduino_buttons_suspended = True
        if self.arduino_button_listener and self.arduino_button_listener.isRunning():
            self.arduino_button_listener.stop()
            self.arduino_button_listener.wait(1000)
        self.arduino_button_listener = None
        self._arduino_runtime_status = "suspended"
        self._notify_arduino_status_change("Suspended during serial-exclusive test page")

    def _resume_arduino_button_listener(self):
        if not self._arduino_buttons_suspended:
            return
        self._arduino_buttons_suspended = False
        self._start_arduino_button_listener()
        self._notify_arduino_status_change("Resumed after leaving serial-exclusive test page")

    def _watchdog_arduino_button_listener(self):
        """Auto-recover listener if it unexpectedly stops."""
        if self._arduino_buttons_suspended:
            return
        if not _env_bool("ARDUINO_BUTTONS_ENABLED", True):
            return
        if self.arduino_button_listener is None or not self.arduino_button_listener.isRunning():
            self._notify_arduino_status_change("Watchdog restarting listener")
            self.restart_arduino_button_listener()

    def _on_arduino_button_status(self, message: str):
        lower_msg = message.lower()
        if "connected" in lower_msg:
            self._arduino_runtime_status = "connected"
        elif "disabled" in lower_msg:
            self._arduino_runtime_status = "disabled"
        elif "no arduino" in lower_msg or "failed" in lower_msg or "error" in lower_msg:
            self._arduino_runtime_status = "reconnecting"
        elif "suspended" in lower_msg:
            self._arduino_runtime_status = "suspended"
        elif "resumed" in lower_msg:
            self._arduino_runtime_status = "starting"
        self._notify_arduino_status_change(message)

    def _notify_arduino_status_change(self, message: str):
        print(f"[ArduinoButtons] {message}")
        if hasattr(self, "others_page") and hasattr(self.others_page, "_refresh_listener_status"):
            self.others_page._refresh_listener_status()

    def get_arduino_button_runtime_status(self) -> str:
        return self._arduino_runtime_status

    def _simulate_key(self, key: int):
        """Simulate a keyboard key press/release on the focused widget."""
        target = QApplication.focusWidget()
        if target is None:
            target = self.stacked_widget.currentWidget()
        if target is None:
            target = self

        press_event = QKeyEvent(QKeyEvent.KeyPress, key, Qt.NoModifier)
        release_event = QKeyEvent(QKeyEvent.KeyRelease, key, Qt.NoModifier)
        QApplication.postEvent(target, press_event)
        QApplication.postEvent(target, release_event)

    def _handle_arduino_button_command(self, command: str):
        """Map Arduino commands to existing GUI keyboard navigation."""
        current_page = self.stacked_widget.currentWidget()
        if isinstance(current_page, ButtonNavigationMixin):
            if command == "BTN1_PRESS" and current_page.handle_arduino_up():
                return
            if command == "BTN3_PRESS" and current_page.handle_arduino_down():
                return
            if command == "BTN2_PRESS" and current_page.handle_arduino_enter():
                return

        if command == "BTN1_PRESS":
            self.focusPreviousChild()
            self._simulate_key(Qt.Key_Up)
        elif command == "BTN3_PRESS":
            self.focusNextChild()
            self._simulate_key(Qt.Key_Down)
        elif command == "BTN2_PRESS":
            focused = QApplication.focusWidget()
            if isinstance(focused, QPushButton):
                focused.click()
            else:
                self._simulate_key(Qt.Key_Return)
                self._simulate_key(Qt.Key_Enter)

    def navigate_to(self, page_index: int):
        """Navigate to a page and refresh back-button visibility."""
        self.stacked_widget.setCurrentIndex(page_index)
        self.update_back_button_visibility()

    def navigate_back(self):
        """Navigate back to previous page using navigation stack."""
        if self.navigation_stack:
            previous_page = self.navigation_stack.pop()
            self._navigating_back = True
            self.stacked_widget.setCurrentIndex(previous_page)
        else:
            self.stacked_widget.setCurrentIndex(PageIndex.MAIN_MENU)

        self.update_back_button_visibility()

    def update_back_button_visibility(self):
        """Show back button only if there is navigation history."""
        current_page = self.stacked_widget.currentWidget()
        if current_page is not None and hasattr(current_page, "back_button"):
            current_page.back_button.setVisible(bool(self.navigation_stack))
    
    def _ensure_database_setup(self):
        """Ensure the combo database exists and has tables. If not, set it up automatically."""
        db_path = DB_PATH
        
        try:
            # Check if database exists and has tables
            needs_setup = False
            
            if not os.path.exists(db_path):
                needs_setup = True
                print("Database file not found, running setup...")
            else:
                # Check if tables exist
                try:
                    import sqlite3
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='combos'")
                    if cursor.fetchone() is None:
                        needs_setup = True
                        print("Database tables not found, running setup...")
                    conn.close()
                except Exception as e:
                    print(f"Error checking database: {e}")
                    needs_setup = True
            
            # Run setup if needed
            if needs_setup:
                setup_script = os.path.join(GUI_DIR, 'setup', 'setup_combo_database.py')
                if os.path.exists(setup_script):
                    print(f"Running database setup from: {setup_script}")
                    import subprocess
                    try:
                        db_path = DB_PATH
                        result = subprocess.run(
                            [sys.executable, setup_script, '--db-path', db_path, '--force'],
                            cwd=GUI_DIR,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        if result.returncode == 0:
                            print("✓ Database setup completed successfully!")
                        else:
                            print(f"✗ Database setup failed: {result.stderr}")
                    except subprocess.TimeoutExpired:
                        print("✗ Database setup timed out (30 seconds)")
                else:
                    print(f"Setup script not found at: {setup_script}")
        
        except Exception as e:
            print(f"Error in database setup: {e}")
            import traceback
            traceback.print_exc()
    
    def get_current_user(self):
        """Get the currently logged in user."""
        return self.login_page.get_current_user()
    
    def on_page_changed(self, index):
        """Handle page changes to update user-specific pages."""
        if index != self.previous_page:
            if self._navigating_back:
                self._navigating_back = False
            else:
                self.navigation_stack.append(self.previous_page)

        if index == PageIndex.OTHERS and hasattr(self.others_page, "_refresh_arduino_ports"):
            self.others_page._refresh_arduino_ports()

        if _env_bool("ARDUINO_BUTTONS_SUSPEND_DURING_TESTS", True):
            if index in self._serial_exclusive_pages:
                self._suspend_arduino_button_listener()
            else:
                self._resume_arduino_button_listener()

        if index == PageIndex.USER_COMBO_PROGRESS:
            current_user = self.get_current_user()
            # Set return_to_page based on where we came from
            return_to = self.previous_page if self.previous_page not in [PageIndex.USER_COMBO_PROGRESS, PageIndex.USER_PROGRESS_OVERVIEW] else PageIndex.HOMEPAGE
            if current_user:
                self.user_combo_progress_page.set_user(current_user, return_to_page=return_to)
        # Track previous page for next navigation
        self.previous_page = index
        self.update_back_button_visibility()

    def start_training_session(self):
        """Extract parameters and start the training session."""
        try:
            config = self.app_state.get_config()
            rounds = config.rounds

            time_str = self.app_state.time_label or config.get_time_str()
            rest_str = self.app_state.rest_label or config.get_rest_str()

            difficulty = config.difficulty
            sequences = config.custom_sequences
            battle_style = config.battle_style

            # Emit payload when countdown ends (battle or punch-library flows)
            # Skip emission for Self-Select; it will emit per-sequence refresh instead
            # if (difficulty != "Self-Select") and (difficulty or battle_style):
            #     payload = {
            #         "mode": difficulty,
            #         "battle_style": battle_style,
            #         "sequences": sequences,
            #     }
            #     print(json.dumps(payload))

            training_page = self.stacked_widget.widget(PageIndex.TRAINING_SESSION)
            current_user = self.get_current_user()
            training_page.start_session(rounds, time_str, rest_str, difficulty, sequences, battle_style, current_user)
            self.navigate_to(PageIndex.TRAINING_SESSION)
        except Exception as e:
            print(f"Error starting training session: {e}")

    def closeEvent(self, event: QCloseEvent):
        """Ensure background serial listener is stopped when app closes."""
        if hasattr(self, "_arduino_watchdog_timer"):
            self._arduino_watchdog_timer.stop()
        if self.arduino_button_listener and self.arduino_button_listener.isRunning():
            self.arduino_button_listener.stop()
            self.arduino_button_listener.wait(1000)
        super().closeEvent(event)

def main():
    """
    Initialize and run the PyQt application.

    Creates a QApplication instance, instantiates the main window,
    displays it, and starts the application event loop.

    Returns:
        None
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
