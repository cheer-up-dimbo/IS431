"""
GUI page classes for the sparring flow.

Flow:
    SparPage (existing, PageIndex.SPAR = 12)
      -> SparStyleSelectPage     (SPAR_STYLE_SELECT = 34)
      -> SparRoundConfigPage     (SPAR_ROUND_CONFIG  = 35)
      -> SparCountdownPage       (SPAR_COUNTDOWN     = 36)
      -> SparSessionPage         (SPAR_SESSION       = 37)
      -> SparRestPage            (SPAR_REST          = 38)
      -> (repeat countdown -> session -> rest for each round)
      -> SparProcessingPage      (SPAR_PROCESSING    = 39)
      -> SparResultPage          (SPAR_RESULT        = 40)
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

from PySide6.QtCore import Qt, QThread, QTimer, QObject, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget,
    QSizePolicy,
)

from core.constants import PageIndex, ButtonStyle
from sparring.combo_pools import STYLE_TRANSITION_MATRICES
from sparring.sequence_generator import generate_session_sequence
from sparring.robot_interface import (
    send_punch, send_round_start, send_round_stop,
    INTRA_COMBO_GAP_S, INTER_COMBO_GAP_S,
)
from sparring import sparring_database as spar_db

# ---------------------------------------------------------------------------
# Import ButtonNavigationMixin from main_gui — fallback stub for safety
# ---------------------------------------------------------------------------
from core.navigation import ButtonNavigationMixin


# ============================================================================
# Shared session state
# ============================================================================

class SparSessionState:
    """Mutable session state shared across all sparring pages."""

    def __init__(self) -> None:
        self.style: str = "Random"
        self.rounds: int = 3
        self.round_duration: int = 120
        self.rest_duration: int = 60
        self.current_round: int = 0
        self.session_sequence: List[List[str]] = []
        self.username: str = ""
        self.session_id: Optional[int] = None

    def reset(self) -> None:
        self.__init__()


_spar_state = SparSessionState()


# ============================================================================
# Helper — resolve users/ directory
# ============================================================================

def _users_dir() -> Path:
    """Return the GUI/users directory."""
    return Path(__file__).resolve().parent.parent / "users"


# ============================================================================
# Page 1 — SparStyleSelectPage
# ============================================================================

class SparStyleSelectPage(ButtonNavigationMixin, QWidget):
    """Allows the user to pick a fighting style for the sparring session."""

    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        # Title
        title = QLabel("Choose Fighting Style")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # One button per style from the transition matrices
        nav_buttons: List[QPushButton] = []
        for style_name in STYLE_TRANSITION_MATRICES.keys():
            btn = QPushButton(style_name)
            btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
            btn.clicked.connect(lambda checked=False, s=style_name: self._select_style(s))
            layout.addWidget(btn, alignment=Qt.AlignCenter)
            nav_buttons.append(btn)

        layout.addStretch()

        # Back button
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        back_btn.clicked.connect(self.on_back_clicked)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        nav_buttons.append(back_btn)

        self.setLayout(layout)
        self.setup_navigation(nav_buttons)

    # -- actions --

    def _select_style(self, style_name: str) -> None:
        """Store the chosen style and navigate to round config."""
        _spar_state.style = style_name
        self.navigate_to(PageIndex.SPAR_ROUND_CONFIG)

    def on_back_clicked(self) -> None:
        self.navigate_to(PageIndex.SPAR)


# ============================================================================
# Page 2 — SparRoundConfigPage
# ============================================================================

class _SequenceWorker(QObject):
    """Worker that generates the punch sequence on a background thread."""
    finished = Signal(list)  # emits List[List[str]]

    def __init__(
        self,
        style: str,
        weakness_profile: Dict,
        rounds: int,
        round_duration: int,
    ) -> None:
        super().__init__()
        self._style = style
        self._weakness = weakness_profile
        self._rounds = rounds
        self._duration = round_duration

    def run(self) -> None:
        sequence = generate_session_sequence(
            self._style,
            self._weakness,
            self._rounds,
            self._duration,
        )
        self.finished.emit(sequence)


class SparRoundConfigPage(ButtonNavigationMixin, QWidget):
    """Configure rounds, round duration, and rest duration before starting."""

    _DURATION_VALUES = [30, 60, 90, 120, 150, 180]
    _DURATION_LABELS = [
        "30 sec", "1 min", "1 min 30 sec", "2 min", "2 min 30 sec", "3 min",
    ]

    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super().__init__()
        self.stacked_widget = stacked_widget

        # Internal indices for spinners
        self._rounds_val: int = 3
        self._round_dur_idx: int = 3   # default = 120 s
        self._rest_dur_idx: int = 1    # default = 60 s

        # Worker references (prevent GC)
        self._thread: Optional[QThread] = None
        self._worker: Optional[_SequenceWorker] = None

        # -- build UI --
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(18)
        layout.setContentsMargins(50, 40, 50, 40)

        title = QLabel("Configure Session")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Spinner rows
        self._rounds_label = QLabel()
        self._round_dur_label = QLabel()
        self._rest_dur_label = QLabel()

        rounds_row, rounds_left, rounds_right = self._make_spinner_row(
            "Rounds", self._rounds_label,
        )
        round_dur_row, rd_left, rd_right = self._make_spinner_row(
            "Round Duration", self._round_dur_label,
        )
        rest_dur_row, rest_left, rest_right = self._make_spinner_row(
            "Rest Duration", self._rest_dur_label,
        )

        rounds_left.clicked.connect(lambda: self._change_rounds(-1))
        rounds_right.clicked.connect(lambda: self._change_rounds(1))
        rd_left.clicked.connect(lambda: self._change_round_dur(-1))
        rd_right.clicked.connect(lambda: self._change_round_dur(1))
        rest_left.clicked.connect(lambda: self._change_rest_dur(-1))
        rest_right.clicked.connect(lambda: self._change_rest_dur(1))

        layout.addLayout(rounds_row)
        layout.addLayout(round_dur_row)
        layout.addLayout(rest_dur_row)

        layout.addStretch()

        # Start Session button
        self.start_btn = QPushButton("Start Session")
        self.start_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        self.start_btn.clicked.connect(self._on_start)
        layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)

        # Back button
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        back_btn.clicked.connect(self.on_back_clicked)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Collect navigable buttons (arrows are not included — only action buttons)
        nav_buttons: List[QPushButton] = [
            rounds_left, rounds_right,
            rd_left, rd_right,
            rest_left, rest_right,
            self.start_btn, back_btn,
        ]
        self.setup_navigation(nav_buttons)

        # Refresh labels
        self._refresh_labels()

    # -- spinner helpers --

    @staticmethod
    def _make_spinner_row(
        label_text: str, value_label: QLabel,
    ) -> tuple:
        """Create a horizontal spinner row: ◀ [label: value] ▶."""
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignCenter)
        row.setSpacing(12)

        header = QLabel(label_text)
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.setFixedWidth(180)
        header.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        left_btn = QPushButton("◀")
        left_btn.setFixedSize(50, 50)
        left_btn.setStyleSheet(ButtonStyle.INFO_SMALL)

        right_btn = QPushButton("▶")
        right_btn.setFixedSize(50, 50)
        right_btn.setStyleSheet(ButtonStyle.INFO_SMALL)

        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFixedWidth(160)
        value_label.setStyleSheet("font-size: 22px; font-weight: bold;")

        row.addWidget(header)
        row.addWidget(left_btn)
        row.addWidget(value_label)
        row.addWidget(right_btn)

        return row, left_btn, right_btn

    def _refresh_labels(self) -> None:
        self._rounds_label.setText(str(self._rounds_val))
        self._round_dur_label.setText(self._DURATION_LABELS[self._round_dur_idx])
        self._rest_dur_label.setText(self._DURATION_LABELS[self._rest_dur_idx])

    def _change_rounds(self, delta: int) -> None:
        self._rounds_val = max(1, min(12, self._rounds_val + delta))
        self._refresh_labels()

    def _change_round_dur(self, delta: int) -> None:
        self._round_dur_idx = max(0, min(len(self._DURATION_VALUES) - 1, self._round_dur_idx + delta))
        self._refresh_labels()

    def _change_rest_dur(self, delta: int) -> None:
        self._rest_dur_idx = max(0, min(len(self._DURATION_VALUES) - 1, self._rest_dur_idx + delta))
        self._refresh_labels()

    # -- start session --

    def _on_start(self) -> None:
        """Commit values, resolve user, generate sequence in background thread."""
        _spar_state.rounds = self._rounds_val
        _spar_state.round_duration = self._DURATION_VALUES[self._round_dur_idx]
        _spar_state.rest_duration = self._DURATION_VALUES[self._rest_dur_idx]
        _spar_state.current_round = 1

        # Resolve username
        main_window = self.window()
        username = ""
        if main_window and hasattr(main_window, "get_current_user"):
            username = main_window.get_current_user() or ""
        _spar_state.username = username

        # Fetch weakness profile for this user
        weakness_profile: Dict = {}
        if username:
            try:
                weakness_profile = spar_db.get_weakness_profile(username)
            except Exception:
                weakness_profile = {}

        # Disable button while generating
        self.start_btn.setEnabled(False)
        self.start_btn.setText("Generating…")

        # Generate sequence in background (QThread + QObject pattern)
        self._thread = QThread()
        self._worker = _SequenceWorker(
            _spar_state.style,
            weakness_profile,
            _spar_state.rounds,
            _spar_state.round_duration,
        )
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_sequence_ready)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def _on_sequence_ready(self, sequence: List[List[str]]) -> None:
        """Called when the background worker has produced the sequence."""
        _spar_state.session_sequence = sequence

        # Re-enable button
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Start Session")

        # Navigate to countdown
        countdown_page = self.stacked_widget.widget(PageIndex.SPAR_COUNTDOWN)
        if hasattr(countdown_page, "start_countdown"):
            countdown_page.start_countdown()
        self.navigate_to(PageIndex.SPAR_COUNTDOWN)

    def on_back_clicked(self) -> None:
        self.navigate_to(PageIndex.SPAR_STYLE_SELECT)


# ============================================================================
# Page 3 — SparCountdownPage
# ============================================================================

class SparCountdownPage(ButtonNavigationMixin, QWidget):
    """3-2-1-GO! countdown before each round begins."""

    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setStyleSheet("background-color: #1a1a2e;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        # Round + style info
        self._info_label = QLabel()
        self._info_label.setAlignment(Qt.AlignCenter)
        self._info_label.setStyleSheet("font-size: 22px; color: #94A3B8; background-color: transparent;")
        layout.addWidget(self._info_label)

        layout.addStretch()

        # Large countdown number
        self._countdown_label = QLabel("3")
        self._countdown_label.setAlignment(Qt.AlignCenter)
        self._countdown_label.setStyleSheet(
            "font-size: 120px; font-weight: bold; color: white;"
        )
        layout.addWidget(self._countdown_label)

        layout.addStretch()
        self.setLayout(layout)

        # Timer for the countdown ticks
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)
        self._count = 3

    def start_countdown(self) -> None:
        """Called externally to begin the 3-2-1-GO sequence."""
        self._info_label.setText(
            f"Round {_spar_state.current_round} of {_spar_state.rounds}  —  {_spar_state.style}"
        )
        self._count = 3
        self._countdown_label.setText("3")
        self._countdown_label.setStyleSheet(
            "font-size: 120px; font-weight: bold; color: white;"
        )
        self._timer.start()

    def _tick(self) -> None:
        self._count -= 1
        if self._count > 0:
            self._countdown_label.setText(str(self._count))
        elif self._count == 0:
            self._countdown_label.setText("GO!")
            self._countdown_label.setStyleSheet(
                "font-size: 120px; font-weight: bold; color: #22C55E; background-color: transparent;"
            )
        else:
            # count < 0 → transition after "GO!" display
            self._timer.stop()
            # Short delay then navigate to session
            QTimer.singleShot(600, self._go_to_session)

    def _go_to_session(self) -> None:
        session_page = self.stacked_widget.widget(PageIndex.SPAR_SESSION)
        if hasattr(session_page, "start_round"):
            session_page.start_round()
        self.navigate_to(PageIndex.SPAR_SESSION)


# ============================================================================
# Page 4 — SparSessionPage
# ============================================================================

class _PunchWorker(QObject):
    """Sends punches to the robot on a background thread."""
    finished = Signal()
    punch_sent = Signal(str)  # emits the punch string for UI feedback

    def __init__(self, punches: List[str]) -> None:
        super().__init__()
        self._punches = punches
        self._running = True

    def stop(self) -> None:
        self._running = False

    def run(self) -> None:
        """Iterate through punches continuously until stopped by the round timer."""
        if not self._punches:
            return

        idx = 0
        while self._running:
            punch = self._punches[idx % len(self._punches)]
            idx += 1

            send_punch(punch)
            self.punch_sent.emit(punch)

            # Determine gap: combo boundary every 3rd punch
            if idx % 3 == 0:
                gap = INTER_COMBO_GAP_S
            else:
                gap = INTRA_COMBO_GAP_S

            # Sleep in small increments so we can check _running
            elapsed = 0.0
            while elapsed < gap and self._running:
                step = min(0.05, gap - elapsed)
                time.sleep(step)
                elapsed += step

        self.finished.emit()


class SparSessionPage(ButtonNavigationMixin, QWidget):
    """Active sparring round — shows timer and sends punches to robot."""

    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setStyleSheet("background-color: #0d1117;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        # Style + round info
        self._info_label = QLabel()
        self._info_label.setAlignment(Qt.AlignCenter)
        self._info_label.setStyleSheet("font-size: 22px; color: #94A3B8; background-color: transparent;")
        layout.addWidget(self._info_label)

        layout.addStretch()

        # Large countdown timer
        self._timer_label = QLabel("0:00")
        self._timer_label.setAlignment(Qt.AlignCenter)
        self._timer_label.setStyleSheet(
            "font-size: 100px; font-weight: bold; color: #f44336;"
        )
        layout.addWidget(self._timer_label)

        # Current punch feedback
        self._punch_label = QLabel("")
        self._punch_label.setAlignment(Qt.AlignCenter)
        self._punch_label.setStyleSheet("font-size: 28px; color: #22C55E; background-color: transparent;")
        layout.addWidget(self._punch_label)

        layout.addStretch()

        # Stop Round button
        self._stop_btn = QPushButton("Stop Round")
        self._stop_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        self._stop_btn.clicked.connect(self._stop_round)
        layout.addWidget(self._stop_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setup_navigation([self._stop_btn])

        # Internal state
        self._remaining: int = 0
        self._tick_timer = QTimer(self)
        self._tick_timer.setInterval(1000)
        self._tick_timer.timeout.connect(self._tick)

        self._punch_thread: Optional[QThread] = None
        self._punch_worker: Optional[_PunchWorker] = None

    def start_round(self) -> None:
        """Begin the current round: start timer and robot punches."""
        self._info_label.setText(
            f"{_spar_state.style}  —  Round {_spar_state.current_round} of {_spar_state.rounds}"
        )
        self._remaining = _spar_state.round_duration
        self._update_timer_display()
        self._punch_label.setText("")

        # Signal robot
        send_round_start()

        # Start countdown timer
        self._tick_timer.start()

        # Start punch worker
        round_idx = _spar_state.current_round - 1
        if round_idx < len(_spar_state.session_sequence):
            punches = _spar_state.session_sequence[round_idx]
        else:
            punches = []

        self._punch_thread = QThread()
        self._punch_worker = _PunchWorker(punches)
        self._punch_worker.moveToThread(self._punch_thread)
        self._punch_thread.started.connect(self._punch_worker.run)
        self._punch_worker.punch_sent.connect(self._on_punch_sent)
        self._punch_worker.finished.connect(self._punch_thread.quit)
        self._punch_worker.finished.connect(self._punch_worker.deleteLater)
        self._punch_thread.finished.connect(self._punch_thread.deleteLater)
        self._punch_thread.start()

    def _on_punch_sent(self, punch: str) -> None:
        """Update the UI with the latest punch sent."""
        punch_names = {
            "1": "Jab", "2": "Cross", "3": "Lead Hook", "4": "Rear Hook",
            "5": "Lead Uppercut", "6": "Rear Uppercut",
            "3b": "Lead Hook (Body)", "2b": "Cross (Body)",
        }
        self._punch_label.setText(punch_names.get(punch, punch))

    def _update_timer_display(self) -> None:
        mins = self._remaining // 60
        secs = self._remaining % 60
        self._timer_label.setText(f"{mins}:{secs:02d}")

    def _tick(self) -> None:
        self._remaining -= 1
        self._update_timer_display()
        if self._remaining <= 0:
            self._end_round()

    def _stop_round(self) -> None:
        """User pressed Stop Round."""
        self._end_round()

    def _end_round(self) -> None:
        """Clean up and decide: rest or processing."""
        self._tick_timer.stop()

        # Stop punch worker
        if self._punch_worker is not None:
            self._punch_worker.stop()

        # Signal robot
        send_round_stop()

        if _spar_state.current_round < _spar_state.rounds:
            # More rounds remain — go to rest
            rest_page = self.stacked_widget.widget(PageIndex.SPAR_REST)
            if hasattr(rest_page, "start_rest"):
                rest_page.start_rest()
            self.navigate_to(PageIndex.SPAR_REST)
        else:
            # Final round done — write trigger and go to processing
            self._write_trigger_file()
            self.navigate_to(PageIndex.SPAR_PROCESSING)

    def _write_trigger_file(self) -> None:
        """Write spar_trigger.json so the CV pipeline knows a session ended."""
        user_dir = _users_dir() / _spar_state.username
        user_dir.mkdir(parents=True, exist_ok=True)
        trigger_path = user_dir / "spar_trigger.json"
        trigger_data = {
            "username": _spar_state.username,
            "session_id": _spar_state.session_id,
            "timestamp": datetime.now().isoformat(),
        }
        trigger_path.write_text(json.dumps(trigger_data, indent=2), encoding="utf-8")
        print(f"[Spar] Trigger written to {trigger_path}")


# ============================================================================
# Page 5 — SparRestPage
# ============================================================================

class SparRestPage(ButtonNavigationMixin, QWidget):
    """Rest period between sparring rounds."""

    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setStyleSheet("background-color: #1b2a1b;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        # Title
        title = QLabel("Rest")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        layout.addWidget(title)

        layout.addStretch()

        # Large green countdown
        self._timer_label = QLabel("0:00")
        self._timer_label.setAlignment(Qt.AlignCenter)
        self._timer_label.setStyleSheet(
            "font-size: 100px; font-weight: bold; color: #F97316; background-color: transparent;"
        )
        layout.addWidget(self._timer_label)

        # Next round info
        self._next_label = QLabel("")
        self._next_label.setAlignment(Qt.AlignCenter)
        self._next_label.setStyleSheet("font-size: 20px; color: #94A3B8; background-color: transparent;")
        layout.addWidget(self._next_label)

        layout.addStretch()

        # Skip Rest button
        self._skip_btn = QPushButton("Skip Rest")
        self._skip_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        self._skip_btn.clicked.connect(self._skip_rest)
        layout.addWidget(self._skip_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setup_navigation([self._skip_btn])

        # Internal timer
        self._remaining: int = 0
        self._tick_timer = QTimer(self)
        self._tick_timer.setInterval(1000)
        self._tick_timer.timeout.connect(self._tick)

    def start_rest(self) -> None:
        """Called externally to begin the rest countdown."""
        self._remaining = _spar_state.rest_duration
        next_round = _spar_state.current_round + 1
        self._next_label.setText(
            f"Next: Round {next_round} of {_spar_state.rounds}"
        )
        self._update_timer_display()
        self._tick_timer.start()

    def _update_timer_display(self) -> None:
        mins = self._remaining // 60
        secs = self._remaining % 60
        self._timer_label.setText(f"{mins}:{secs:02d}")

    def _tick(self) -> None:
        self._remaining -= 1
        self._update_timer_display()
        if self._remaining <= 0:
            self._transition_to_next_round()

    def _skip_rest(self) -> None:
        """User pressed Skip Rest."""
        self._tick_timer.stop()
        self._transition_to_next_round()

    def _transition_to_next_round(self) -> None:
        """Increment round and go to countdown."""
        self._tick_timer.stop()
        _spar_state.current_round += 1

        countdown_page = self.stacked_widget.widget(PageIndex.SPAR_COUNTDOWN)
        if hasattr(countdown_page, "start_countdown"):
            countdown_page.start_countdown()
        self.navigate_to(PageIndex.SPAR_COUNTDOWN)


# ============================================================================
# Page 6 — SparProcessingPage
# ============================================================================

class SparProcessingPage(ButtonNavigationMixin, QWidget):
    """Waits for CV output file after the session ends."""

    _POLL_INTERVAL_MS = 1000
    _TIMEOUT_S = 120

    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        # Title
        self._title_label = QLabel("Analysing Your Session...")
        self._title_label.setAlignment(Qt.AlignCenter)
        self._title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(self._title_label)

        layout.addStretch()

        # Status text
        self._status_label = QLabel("Waiting for CV pipeline…")
        self._status_label.setAlignment(Qt.AlignCenter)
        self._status_label.setStyleSheet("font-size: 18px; color: #888;")
        layout.addWidget(self._status_label)

        layout.addStretch()

        # Skip Analysis button
        self._skip_btn = QPushButton("Skip Analysis")
        self._skip_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        self._skip_btn.clicked.connect(self._skip_analysis)
        layout.addWidget(self._skip_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setup_navigation([self._skip_btn])

        # Polling timer
        self._poll_timer = QTimer(self)
        self._poll_timer.setInterval(self._POLL_INTERVAL_MS)
        self._poll_timer.timeout.connect(self._poll)
        self._elapsed_s: int = 0

    # -- lifecycle --

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._start_processing()

    def hideEvent(self, event) -> None:
        super().hideEvent(event)
        self._poll_timer.stop()

    # -- logic --

    def _start_processing(self) -> None:
        """Decide whether to poll for CV output or skip directly."""
        self._elapsed_s = 0

        # Check cv_enabled from AppState
        cv_enabled = False
        main_window = self.window()
        if main_window and hasattr(main_window, "app_state"):
            cv_enabled = getattr(main_window.app_state, "cv_enabled", False)

        if not cv_enabled:
            # No CV — skip after a brief pause
            self._status_label.setText("CV disabled — skipping analysis.")
            QTimer.singleShot(1000, lambda: self._finish_with_cv_data(""))
        else:
            self._status_label.setText("Waiting for CV pipeline…")
            self._poll_timer.start()

    def _poll(self) -> None:
        """Check for the CV output file once per second."""
        self._elapsed_s += 1
        user_dir = _users_dir() / _spar_state.username
        output_path = user_dir / "spar_cv_output.txt"

        if output_path.exists():
            self._poll_timer.stop()
            cv_raw = output_path.read_text(encoding="utf-8").strip()

            # Clean up files
            try:
                output_path.unlink()
            except Exception:
                pass
            trigger_path = user_dir / "spar_trigger.json"
            try:
                trigger_path.unlink()
            except Exception:
                pass

            self._finish_with_cv_data(cv_raw)
            return

        # Timeout
        if self._elapsed_s >= self._TIMEOUT_S:
            self._poll_timer.stop()
            self._status_label.setText("Timeout — no CV data received.")
            QTimer.singleShot(1000, lambda: self._finish_with_cv_data(""))

    def _skip_analysis(self) -> None:
        """User pressed Skip Analysis."""
        self._poll_timer.stop()
        self._finish_with_cv_data("")

    def _finish_with_cv_data(self, cv_raw: str) -> None:
        """Save session & weakness data, then navigate to results."""
        # Save to DB
        if _spar_state.username:
            try:
                session_id = spar_db.save_sparring_session(
                    username=_spar_state.username,
                    style=_spar_state.style,
                    total_rounds=_spar_state.rounds,
                    round_duration=_spar_state.round_duration,
                    rest_duration=_spar_state.rest_duration,
                    cv_raw_output=cv_raw,
                )
                _spar_state.session_id = session_id

                # Update weakness profile from parsed punch counts
                punch_counts = spar_db._parse_cv_output(cv_raw)
                if punch_counts:
                    spar_db.update_weakness_profile(_spar_state.username, punch_counts)
            except Exception as e:
                print(f"[Spar] DB save error: {e}")

        # Pass data to result page
        result_page = self.stacked_widget.widget(PageIndex.SPAR_RESULT)
        if hasattr(result_page, "set_results"):
            result_page.set_results(cv_raw)

        self.navigate_to(PageIndex.SPAR_RESULT)


# ============================================================================
# Page 7 — SparResultPage
# ============================================================================

class SparResultPage(ButtonNavigationMixin, QWidget):
    """Displays session results and feedback."""

    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(18)
        layout.setContentsMargins(50, 40, 50, 40)

        # Title
        title = QLabel("Session Complete")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Stats label — total punches + per-punch breakdown
        self._stats_label = QLabel("")
        self._stats_label.setAlignment(Qt.AlignCenter)
        self._stats_label.setWordWrap(True)
        self._stats_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(self._stats_label)

        # Feedback label
        self._feedback_label = QLabel("")
        self._feedback_label.setAlignment(Qt.AlignCenter)
        self._feedback_label.setWordWrap(True)
        self._feedback_label.setStyleSheet("font-size: 16px; color: #94A3B8; margin-top: 10px; background-color: transparent;")
        layout.addWidget(self._feedback_label)

        layout.addStretch()

        # Buttons
        restart_btn = QPushButton("Restart")
        restart_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        restart_btn.clicked.connect(self._on_restart)

        history_btn = QPushButton("History")
        history_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        history_btn.clicked.connect(self._on_history)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(restart_btn, alignment=Qt.AlignCenter)
        layout.addWidget(history_btn, alignment=Qt.AlignCenter)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setup_navigation([restart_btn, history_btn, back_btn])

    def set_results(self, cv_raw: str) -> None:
        """Populate the results page with punch data and feedback."""
        punch_counts: Dict[str, int] = spar_db._parse_cv_output(cv_raw)
        total = sum(punch_counts.values())

        # Build stats text
        if total > 0:
            breakdown_parts = [f"{name}: {count}" for name, count in sorted(punch_counts.items())]
            breakdown_str = "  |  ".join(breakdown_parts)
            stats_text = f"Total Punches Thrown: {total}\n\n{breakdown_str}"
        else:
            stats_text = "No punch data recorded for this session."
        self._stats_label.setText(stats_text)

        # Determine feedback prefix based on AI chat toggle
        ai_chat_enabled = False
        main_window = self.window()
        if main_window and hasattr(main_window, "app_state"):
            ai_chat_enabled = getattr(main_window.app_state, "ai_chat_enabled", False)

        prefix = "🤖 Coach Feedback:" if ai_chat_enabled else "🥊 Feedback:"

        # Build feedback text
        if total > 0:
            most_common = max(punch_counts, key=punch_counts.get)  # type: ignore[arg-type]
            most_common_count = punch_counts[most_common]

            # Determine which side the robot should target next session
            left_punches = sum(punch_counts.get(p, 0) for p in ["jab", "lead_hook", "lead_upper"])
            right_punches = sum(punch_counts.get(p, 0) for p in ["cross", "rear_hook", "rear_upper"])
            if left_punches > right_punches:
                target_side = "your right side"
            elif right_punches > left_punches:
                target_side = "your left side"
            else:
                target_side = "both sides equally"

            feedback = (
                f"{prefix} Your most used punch was '{most_common}' ({most_common_count} times). "
                f"Total punches: {total}. "
                f"Next session the robot will target {target_side} more to challenge your defence."
            )
        else:
            feedback = f"{prefix} No CV data was available for analysis this session."

        self._feedback_label.setText(feedback)

    # -- navigation --

    def _on_restart(self) -> None:
        _spar_state.reset()
        self.navigate_to(PageIndex.SPAR_STYLE_SELECT)

    def _on_history(self) -> None:
        # Placeholder — will be linked to sparring history page in future
        print("[Spar] History view placeholder — not yet implemented")

    def on_back_clicked(self) -> None:
        _spar_state.reset()
        self.navigate_to(PageIndex.SPAR)
