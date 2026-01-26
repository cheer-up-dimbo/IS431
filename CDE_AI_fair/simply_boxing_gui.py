"""
Simplified Boxing Training GUI with Combo and Blocking modes - INTEGRATED VERSION

Features:
- Combo Mode: Countdown → Display combo → Show results → Play video → Return home
- Blocking Mode: Countdown → Numpad interface with recording → Return home
- Backend integration with combo_detector and blocking_detector modules
"""

import sys
import json
import os
from typing import Optional
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, 
    QLabel, QStackedWidget, QGridLayout
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread, QObject
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl

# Backend detection modules
sys.path.insert(0, str(Path(__file__).parent))
from CV import combo_detector
from Arms import blocking_detector

# ============================================================================
# PAGE INDICES
# ============================================================================

class PageIndex:
    HOMEPAGE = 0
    COMBO_COUNTDOWN = 1
    COMBO_DISPLAY = 2
    COMBO_RESULTS = 3
    COMBO_VIDEO = 4
    BLOCKING_COUNTDOWN = 5
    BLOCKING_NUMPAD = 6


# ============================================================================
# BUTTON STYLES
# ============================================================================

class ButtonStyle:
    """Centralized button style management."""

    @staticmethod
    def _create_style(font_size, padding, min_width, min_height, bg_color, 
                     hover_color, pressed_color, border_radius=8):
        """Internal helper to generate button stylesheet."""
        return f"""
            QPushButton {{
                font-size: {font_size}px;
                padding: {padding}px;
                min-width: {min_width}px;
                min-height: {min_height}px;
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: {border_radius}px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """

    # Green buttons (Primary actions)
    PRIMARY_LARGE = _create_style.__func__(
        font_size=28, padding=40, min_width=500, min_height=50,
        bg_color="#4CAF50", hover_color="#45a049", pressed_color="#3d8b40",
    )

    PRIMARY_MEDIUM = _create_style.__func__(
        font_size=20, padding=25, min_width=250, min_height=40,
        bg_color="#4CAF50", hover_color="#45a049", pressed_color="#3d8b40",
    )

    # Red buttons (Back/Exit)
    BACK_LARGE = _create_style.__func__(
        font_size=20, padding=25, min_width=500, min_height=40,
        bg_color="#f44336", hover_color="#da190b", pressed_color="#c41504",
    )

    BACK_MEDIUM = _create_style.__func__(
        font_size=20, padding=25, min_width=250, min_height=40,
        bg_color="#f44336", hover_color="#da190b", pressed_color="#c41504",
    )

    # Blue buttons (Numpad)
    NUMPAD_BUTTON = _create_style.__func__(
        font_size=40, padding=30, min_width=120, min_height=80,
        bg_color="#2196F3", hover_color="#1976D2", pressed_color="#0D47A1",
        border_radius=12
    )


# ============================================================================
# HOMEPAGE
# ============================================================================

class HomePage(QWidget):
    """Main menu with Combo and Blocking mode options."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Boxing Training")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 30px;")

        combo_btn = QPushButton("Combo")
        blocking_btn = QPushButton("Blocking")

        combo_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        blocking_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)

        combo_btn.clicked.connect(self.on_combo_clicked)
        blocking_btn.clicked.connect(self.on_blocking_clicked)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(combo_btn)
        layout.addStretch()
        layout.addWidget(blocking_btn)
        layout.addStretch()

        self.setLayout(layout)

    def on_combo_clicked(self):
        """Start Combo mode."""
        print(json.dumps({"mode": "Combo", "action": "start"}))
        countdown_page = self.stacked_widget.widget(PageIndex.COMBO_COUNTDOWN)
        countdown_page.start_countdown()
        self.stacked_widget.setCurrentIndex(PageIndex.COMBO_COUNTDOWN)

    def on_blocking_clicked(self):
        """Start Blocking mode."""
        print(json.dumps({"mode": "Blocking", "action": "start"}))
        countdown_page = self.stacked_widget.widget(PageIndex.BLOCKING_COUNTDOWN)
        countdown_page.start_countdown()
        self.stacked_widget.setCurrentIndex(PageIndex.BLOCKING_COUNTDOWN)


# ============================================================================
# COMBO MODE PAGES
# ============================================================================

class ComboCountdownPage(QWidget):
    """10-second countdown before combo display with camera initialization."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.countdown_value = 10
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self._init_thread: Optional[QThread] = None
        self._init_complete = False

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Get Ready!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold;")

        self.countdown_label = QLabel(str(self.countdown_value))
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; color: #666;")

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.countdown_label)
        layout.addWidget(self.status_label)
        layout.addStretch()

        self.setLayout(layout)

    def start_countdown(self):
        """Start the 10-second countdown and initialize camera."""
        self.countdown_value = 10
        self._init_complete = False
        self.countdown_label.setText(str(self.countdown_value))
        self.status_label.setText("Initializing camera...")
        
        # Start camera initialization in background
        self._start_initialization()
        
        self.timer.start(1000)
        print(json.dumps({"action": "countdown_start", "duration": 10}))

    def _start_initialization(self):
        """Initialize camera and model in worker thread."""
        class _InitWorker(QObject):
            finished = Signal(bool, str)  # success, error_message

            def run(self):
                try:
                    # Use Windows-compatible path
                    video_dir = Path.home() / "Videos" / "BoxingTraining"
                    video_dir.mkdir(parents=True, exist_ok=True)
                    video_path = str(video_dir / "combo_recording.mp4")
                    
                    print(json.dumps({"debug": "Starting camera initialization", "video_path": video_path}))
                    
                    success, error_msg = combo_detector.initialize_camera_and_model(
                        camera_index=0,
                        video_path=video_path
                    )
                    
                    print(json.dumps({"debug": "Camera initialization complete", "success": success, "error": error_msg}))
                    self.finished.emit(success, error_msg or "")
                except Exception as ex:
                    error_detail = f"Initialization error: {str(ex)}"
                    print(json.dumps({"debug": "Camera initialization exception", "error": error_detail}))
                    self.finished.emit(False, error_detail)

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
        """Handle initialization completion."""
        print(json.dumps({"debug": "Combo init finished", "success": success, "error": error_message}))
        self._init_complete = success
        if success:
            self.status_label.setText("Camera ready!")
            print(json.dumps({"status": "Combo camera ready"}))
        else:
            self.status_label.setText(f"Error: {error_message}")
            print(json.dumps({"status": "Combo camera failed", "error": error_message}))

    def update_countdown(self):
        """Update countdown display."""
        if self.countdown_value > 1:
            self.countdown_value -= 1
            self.countdown_label.setText(str(self.countdown_value))
        else:
            self.timer.stop()
            if self._init_complete:
                print(json.dumps({"action": "countdown_complete"}))
                display_page = self.stacked_widget.widget(PageIndex.COMBO_DISPLAY)
                display_page.start_display()
                self.stacked_widget.setCurrentIndex(PageIndex.COMBO_DISPLAY)
            else:
                self.status_label.setText("Camera initialization failed. Returning to home...")
                QTimer.singleShot(2000, lambda: self.stacked_widget.setCurrentIndex(PageIndex.HOMEPAGE))


class ComboDisplayPage(QWidget):
    """Display '1-1-2' combo for 15 seconds with detection."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.display_time = 15
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self._detection_thread: Optional[QThread] = None

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)

        self.combo_label = QLabel("1-1-2")
        self.combo_label.setAlignment(Qt.AlignCenter)
        self.combo_label.setStyleSheet(
            "font-size: 80px; font-weight: bold; color: #2196F3;"
        )

        self.timer_label = QLabel("15")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 48px; color: #666;")

        layout.addStretch()
        layout.addWidget(self.combo_label)
        layout.addStretch()
        layout.addWidget(self.timer_label)
        layout.addStretch()

        self.setLayout(layout)

    def start_display(self):
        """Start displaying the combo and recording."""
        self.display_time = 15
        self.timer_label.setText(str(self.display_time))
        
        # Start recording and detection in background
        self._start_detection()
        
        self.timer.start(1000)
        print(json.dumps({"action": "combo_display", "combo": "1-1-2", "duration": 15}))

    def _start_detection(self):
        """Start combo detection in worker thread."""
        class _DetectionWorker(QObject):
            finished = Signal(object)  # ComboResult

            def run(self):
                try:
                    # Start recording
                    success, error = combo_detector.start_recording()
                    if not success:
                        result = combo_detector.ComboResult(
                            success=False, status="error",
                            error_message=f"Recording failed: {error}"
                        )
                        self.finished.emit(result)
                        return
                    
                    # Detect combo for 15 seconds
                    result = combo_detector.detect_combo(duration_seconds=15.0, expected_punches=5)
                    self.finished.emit(result)
                except Exception as ex:
                    result = combo_detector.ComboResult(
                        success=False, status="error",
                        error_message=f"Detection error: {str(ex)}"
                    )
                    self.finished.emit(result)

        self._detection_thread = QThread(self)
        self._detection_worker = _DetectionWorker()
        self._detection_worker.moveToThread(self._detection_thread)
        self._detection_thread.started.connect(self._detection_worker.run)
        self._detection_worker.finished.connect(self._on_detection_finished)
        self._detection_worker.finished.connect(self._detection_thread.quit)
        self._detection_worker.finished.connect(self._detection_worker.deleteLater)
        self._detection_thread.finished.connect(self._detection_thread.deleteLater)
        self._detection_thread.start()

    def _on_detection_finished(self, result):
        """Handle detection completion."""
        # Store result for results page
        results_page = self.stacked_widget.widget(PageIndex.COMBO_RESULTS)
        if result.success:
            results_page.set_results(result.successful_punches, result.video_path)
        else:
            results_page.set_error(result.error_message)

    def update_timer(self):
        """Update timer display."""
        if self.display_time > 1:
            self.display_time -= 1
            self.timer_label.setText(str(self.display_time))
        else:
            self.timer.stop()
            print(json.dumps({"action": "combo_complete"}))
            # Move to results page
            self.stacked_widget.setCurrentIndex(PageIndex.COMBO_RESULTS)


class ComboResultsPage(QWidget):
    """Display results: X out of 5 punches correct."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.successful_punches = 0
        self.video_path = None

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Results")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold;")

        self.results_label = QLabel("0 / 5")
        self.results_label.setAlignment(Qt.AlignCenter)
        self.results_label.setStyleSheet(
            "font-size: 80px; font-weight: bold; color: #4CAF50;"
        )

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 24px; color: #666;")

        next_btn = QPushButton("Next")
        next_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        next_btn.clicked.connect(self.on_next_clicked)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.results_label)
        layout.addWidget(self.message_label)
        layout.addStretch()
        layout.addWidget(next_btn)
        layout.addStretch()

        self.setLayout(layout)

    def set_results(self, successful_punches: int, video_path: str):
        """Set results from combo detection."""
        self.successful_punches = successful_punches
        self.video_path = video_path
        
        self.results_label.setText(f"{self.successful_punches} / 5")
        
        if self.successful_punches >= 4:
            self.message_label.setText("Excellent! 🥊")
        elif self.successful_punches >= 3:
            self.message_label.setText("Good job! 💪")
        else:
            self.message_label.setText("Keep practicing! 🥋")
        
        print(json.dumps({
            "action": "results_displayed",
            "successful_punches": self.successful_punches,
            "total_punches": 5
        }))

    def set_error(self, error_message: str):
        """Display error message."""
        self.results_label.setText("Error")
        self.message_label.setText(error_message)
        self.video_path = None

    def on_next_clicked(self):
        """Show video replay."""
        print(json.dumps({"action": "show_video"}))
        video_page = self.stacked_widget.widget(PageIndex.COMBO_VIDEO)
        video_page.load_video(self.video_path)
        self.stacked_widget.setCurrentIndex(PageIndex.COMBO_VIDEO)


class ComboVideoPage(QWidget):
    """Play recorded video of CV detecting punches."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Video Replay")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")

        # Video widget
        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)

        # Placeholder for when no video is loaded
        self.placeholder_label = QLabel("Video will play here")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet(
            "font-size: 24px; color: #999; background-color: #f0f0f0; "
            "min-height: 400px; border-radius: 8px;"
        )

        back_btn = QPushButton("Back to Home")
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(self.video_widget)
        layout.addWidget(self.placeholder_label)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)
        
        # Initially hide video widget and show placeholder
        self.video_widget.hide()
        self.placeholder_label.show()

    def load_video(self, video_path: Optional[str] = None):
        """Load and play the recorded video."""
        print(json.dumps({"action": "load_video"}))
        
        if video_path is None:
            video_dir = Path.home() / "Videos" / "BoxingTraining"
            video_path = str(video_dir / "combo_recording.mp4")
        
        # Check if video file exists
        if not Path(video_path).exists():
            print(json.dumps({"action": "video_not_found", "path": video_path}))
            self.placeholder_label.setText(f"Video not found at:\n{video_path}")
            self.placeholder_label.show()
            self.video_widget.hide()
            return
        
        try:
            self.media_player.setSource(QUrl.fromLocalFile(video_path))
            self.video_widget.show()
            self.placeholder_label.hide()
            self.media_player.play()
        except Exception as e:
            print(json.dumps({"action": "video_load_error", "error": str(e)}))
            self.placeholder_label.setText(f"Error loading video:\n{str(e)}")
            self.placeholder_label.show()
            self.video_widget.hide()

    def on_media_status_changed(self, status):
        """Handle media player status changes."""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            print(json.dumps({"action": "video_complete"}))

    def on_back_clicked(self):
        """Return to homepage."""
        self.media_player.stop()
        combo_detector.cleanup()
        print(json.dumps({"action": "return_home"}))
        self.stacked_widget.setCurrentIndex(PageIndex.HOMEPAGE)


# ============================================================================
# BLOCKING MODE PAGES
# ============================================================================

class BlockingCountdownPage(QWidget):
    """10-second countdown before blocking mode with camera initialization."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.countdown_value = 10
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self._init_thread: Optional[QThread] = None
        self._init_complete = False

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Get Ready!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold;")

        self.countdown_label = QLabel(str(self.countdown_value))
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; color: #666;")

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.countdown_label)
        layout.addWidget(self.status_label)
        layout.addStretch()

        self.setLayout(layout)

    def start_countdown(self):
        """Start the 10-second countdown and initialize camera."""
        self.countdown_value = 10
        self._init_complete = False
        self.countdown_label.setText(str(self.countdown_value))
        self.status_label.setText("Initializing camera...")
        
        # Start camera initialization in background
        self._start_initialization()
        
        self.timer.start(1000)
        print(json.dumps({"action": "countdown_start", "duration": 10}))

    def _start_initialization(self):
        """Initialize camera and model in worker thread."""
        class _InitWorker(QObject):
            finished = Signal(bool, str)  # success, error_message

            def run(self):
                try:
                    # Use Windows-compatible path
                    video_dir = Path.home() / "Videos" / "BoxingTraining"
                    video_dir.mkdir(parents=True, exist_ok=True)
                    video_path = str(video_dir / "blocking_recording.mp4")
                    
                    print(json.dumps({"debug": "Starting blocking camera initialization", "video_path": video_path}))
                    
                    success, error_msg = blocking_detector.initialize_camera_and_model(
                        camera_index=0,
                        video_path=video_path
                    )
                    
                    print(json.dumps({"debug": "Blocking camera initialization complete", "success": success, "error": error_msg}))
                    self.finished.emit(success, error_msg or "")
                except Exception as ex:
                    error_detail = f"Initialization error: {str(ex)}"
                    print(json.dumps({"debug": "Blocking camera initialization exception", "error": error_detail}))
                    self.finished.emit(False, error_detail)

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
        """Handle initialization completion."""
        print(json.dumps({"debug": "Blocking init finished", "success": success, "error": error_message}))
        self._init_complete = success
        if success:
            self.status_label.setText("Camera ready!")
            print(json.dumps({"status": "Blocking camera ready"}))
        else:
            self.status_label.setText(f"Error: {error_message}")
            print(json.dumps({"status": "Blocking camera failed", "error": error_message}))

    def update_countdown(self):
        """Update countdown display."""
        if self.countdown_value > 1:
            self.countdown_value -= 1
            self.countdown_label.setText(str(self.countdown_value))
        else:
            self.timer.stop()
            if self._init_complete:
                print(json.dumps({"action": "countdown_complete", "next": "blocking_numpad"}))
                print(json.dumps({"command": "record"}))
                
                # Start recording
                numpad_page = self.stacked_widget.widget(PageIndex.BLOCKING_NUMPAD)
                numpad_page.start_recording()
                self.stacked_widget.setCurrentIndex(PageIndex.BLOCKING_NUMPAD)
            else:
                self.status_label.setText("Camera initialization failed. Returning to home...")
                QTimer.singleShot(2000, lambda: self.stacked_widget.setCurrentIndex(PageIndex.HOMEPAGE))


class BlockingNumpadPage(QWidget):
    """Numpad interface (1-6) with Exit button for blocking mode."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self._recording = False
        self._frame_timer = QTimer()
        self._frame_timer.timeout.connect(self._process_frame)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Blocking Mode")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 20px;")

        # Create numpad grid (2 rows x 3 columns)
        numpad_grid = QGridLayout()
        numpad_grid.setSpacing(20)

        for i in range(6):
            btn = QPushButton(str(i + 1))
            btn.setStyleSheet(ButtonStyle.NUMPAD_BUTTON)
            btn.clicked.connect(lambda checked=False, num=i+1: self.on_number_clicked(num))
            row = i // 3
            col = i % 3
            numpad_grid.addWidget(btn, row, col)

        # Exit button
        exit_btn = QPushButton("Exit")
        exit_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        exit_btn.clicked.connect(self.on_exit_clicked)

        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addLayout(numpad_grid)
        main_layout.addStretch()
        main_layout.addWidget(exit_btn)

        self.setLayout(main_layout)

    def start_recording(self):
        """Start recording and frame processing."""
        try:
            success, error = blocking_detector.start_recording()
            if success:
                self._recording = True
                # Process frames at 30 fps
                self._frame_timer.start(33)  # ~30fps
            else:
                print(json.dumps({"error": "Failed to start recording", "message": error}))
        except Exception as e:
            print(json.dumps({"error": "Recording exception", "message": str(e)}))

    def _process_frame(self):
        """Process a frame in the background."""
        if self._recording:
            try:
                blocking_detector.process_frame()
            except Exception as e:
                print(json.dumps({"error": "Frame processing error", "message": str(e)}))

    def on_number_clicked(self, number: int):
        """Handle numpad button click."""
        print(json.dumps({"action": "button_press", "number": number}))
        
        # Register button press with pose data
        if self._recording:
            blocking_detector.register_button_press(number)

    def on_exit_clicked(self):
        """Return to homepage and stop recording."""
        self._recording = False
        self._frame_timer.stop()
        
        print(json.dumps({"command": "stop_recording"}))
        
        # Stop recording and get results
        result = blocking_detector.stop_recording()
        if result.success:
            print(json.dumps({
                "action": "exit_blocking_mode",
                "total_presses": result.total_presses,
                "video_path": result.video_path
            }))
        
        # Cleanup
        blocking_detector.cleanup()
        
        self.stacked_widget.setCurrentIndex(PageIndex.HOMEPAGE)


# ============================================================================
# MAIN WINDOW
# ============================================================================

class MainWindow(QWidget):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boxing Training - Integrated GUI")
        self.setFixedSize(1024, 600)

        self.stacked_widget = QStackedWidget()

        # Create pages
        self.homepage = HomePage(self.stacked_widget)
        self.combo_countdown = ComboCountdownPage(self.stacked_widget)
        self.combo_display = ComboDisplayPage(self.stacked_widget)
        self.combo_results = ComboResultsPage(self.stacked_widget)
        self.combo_video = ComboVideoPage(self.stacked_widget)
        self.blocking_countdown = BlockingCountdownPage(self.stacked_widget)
        self.blocking_numpad = BlockingNumpadPage(self.stacked_widget)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.homepage)               # 0
        self.stacked_widget.addWidget(self.combo_countdown)        # 1
        self.stacked_widget.addWidget(self.combo_display)          # 2
        self.stacked_widget.addWidget(self.combo_results)          # 3
        self.stacked_widget.addWidget(self.combo_video)            # 4
        self.stacked_widget.addWidget(self.blocking_countdown)     # 5
        self.stacked_widget.addWidget(self.blocking_numpad)        # 6

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Initialize and run the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
