import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QGridLayout, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt, QTimer

# Define shared button styles at module level
BUTTON_STYLE = """
    QPushButton {
        font-size: 28px;
        padding: 40px;
        min-width: 500px;
        min-height: 50px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QPushButton:pressed {
        background-color: #3d8b40;
    }
"""

BACK_BUTTON_STYLE = """
    QPushButton {
        font-size: 20px;
        padding: 25px;
        min-width: 500px;
        min-height: 40px;
        background-color: #f44336;
        color: white;
        border: none;
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: #da190b;
    }
    QPushButton:pressed {
        background-color: #c41504;
    }
"""

BACK_BUTTON_STYLE_2 = """
    QPushButton {
        font-size: 20px;
        padding: 25px;
        min-width: 250px;
        min-height: 40px;
        background-color: #f44336;
        color: white;
        border: none;
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: #da190b;
    }
    QPushButton:pressed {
        background-color: #c41504;
    }
"""

BACK_CONTINUE_BUTTON_STYLE = """
    QPushButton {
        font-size: 20px;
        padding: 25px;
        min-width: 200px;
        min-height: 40px;
        background-color: #f44336;
        color: white;
        border: none;
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: #da190b;
    }
    QPushButton:pressed {
        background-color: #c41504;
    }
"""

# Adjusted SMALL_BUTTON_STYLE to a smaller size (change values here to tune)
SMALL_BUTTON_STYLE = """
    QPushButton {
        font-size: 20px;
        padding: 12px;
        min-width: 240px;
        min-height: 50px;
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: #1976D2;
    }
    QPushButton:pressed {
        background-color: #155A8A;
    }
"""

# Button style used specifically for the 12 round-selection buttons (smaller)
ROUND_SELECTION_BUTTON_STYLE = """
    QPushButton {
        font-size: 20px;
        padding: 8px;
        min-width: 80px;
        min-height: 90px;
        background-color: #1976D2;
        color: white;
        border: none;
        border-radius: 6px;
    }
    QPushButton:hover {
        background-color: #1565C0;
    }
    QPushButton:pressed {
        background-color: #0D47A1;
    }
"""

# Button style used specifically for the 12 speed-selection buttons (smaller)
SPEED_SELECTION_BUTTON_STYLE = """
    QPushButton {
        font-size: 40px;
        padding: 8px;
        min-width: 80px;
        min-height: 300px;
        background-color: #1976D2;
        color: white;
        border: none;
        border-radius: 6px;
    }
    QPushButton:hover {
        background-color: #1565C0;
    }
    QPushButton:pressed {
        background-color: #0D47A1;
    }
"""

# Button style used specifically for the 12 time-selection buttons (smaller)
TIME_SELECTION_BUTTON_STYLE = """
    QPushButton {
        font-size: 18px;
        padding: 8px;
        background-color: #1976D2;
        color: white;
        border: none;
        border-radius: 6px;
    }
    QPushButton:hover {
        background-color: #1565C0;
    }
    QPushButton:pressed {
        background-color: #0D47A1;
    }
"""

class Homepage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Homepage")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        training_btn = QPushButton("Training")
        performance_btn = QPushButton("Performance")
        others_btn = QPushButton("Others")

        training_btn.setStyleSheet(BUTTON_STYLE)
        performance_btn.setStyleSheet(BUTTON_STYLE)
        others_btn.setStyleSheet(BUTTON_STYLE)

        training_btn.clicked.connect(self.on_training_clicked)
        performance_btn.clicked.connect(self.on_performance_clicked)
        others_btn.clicked.connect(self.on_others_clicked)

        layout.addWidget(title)
        layout.addWidget(training_btn)
        layout.addWidget(performance_btn)
        layout.addWidget(others_btn)
        layout.addStretch()

        self.setLayout(layout)

    def on_training_clicked(self):
        print("Training button clicked")
        self.stacked_widget.setCurrentIndex(1)

    def on_performance_clicked(self):
        print("Performance button clicked")

    def on_others_clicked(self):
        print("Others button clicked")

class TrainingPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Training")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        techniques_btn = QPushButton("Techniques")
        spar_btn = QPushButton("Spar")
        back_btn = QPushButton("Back")

        techniques_btn.setStyleSheet(BUTTON_STYLE)
        spar_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

        techniques_btn.clicked.connect(self.on_techniques_clicked)
        spar_btn.clicked.connect(self.on_spar_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(techniques_btn)
        layout.addWidget(spar_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_techniques_clicked(self):
        print("Techniques button clicked")
        self.stacked_widget.setCurrentIndex(2)

    def on_spar_clicked(self):
        print("Spar button clicked")
        self.stacked_widget.setCurrentIndex(13)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(0)

class TechniquesPage(QWidget):
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
        defense_btn = QPushButton("Defense Technique")
        back_btn = QPushButton("Back")

        punch_lib_btn.setStyleSheet(BUTTON_STYLE)
        defense_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

        punch_lib_btn.clicked.connect(self.on_punch_combination_library_clicked)
        defense_btn.clicked.connect(self.on_defense_technique_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(punch_lib_btn)
        layout.addWidget(defense_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_punch_combination_library_clicked(self):
        print("Punch Combination Library button clicked")
        self.stacked_widget.setCurrentIndex(3)

    def on_defense_technique_clicked(self):
        print("Defense Technique button clicked")
        self.stacked_widget.setCurrentIndex(12)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(1)

class PunchCombinationPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Punch Combinations")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        beginner_btn = QPushButton("Beginner")
        intermediate_btn = QPushButton("Intermediate")
        advanced_btn = QPushButton("Advanced")
        self_select_btn = QPushButton("Self-Select")
        back_btn = QPushButton("Back")

        beginner_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        intermediate_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        advanced_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        self_select_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

        beginner_btn.clicked.connect(lambda: self.on_difficulty_clicked("Beginner"))
        intermediate_btn.clicked.connect(lambda: self.on_difficulty_clicked("Intermediate"))
        advanced_btn.clicked.connect(lambda: self.on_difficulty_clicked("Advanced"))
        self_select_btn.clicked.connect(lambda: self.on_difficulty_clicked("Self-Select"))
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(beginner_btn)
        layout.addWidget(intermediate_btn)
        layout.addWidget(advanced_btn)
        layout.addWidget(self_select_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_difficulty_clicked(self, difficulty):
        print(f"{difficulty} button clicked")
        # Store difficulty in BasicParametersPage
        basic_page = self.stacked_widget.widget(4)
        basic_page.selected_difficulty = difficulty
        basic_page.previous_page = 3  # Set to Punch Combinations
        
        if difficulty == "Self-Select":
            self_select_page = self.stacked_widget.widget(11)
            self_select_page.previous_page = 3
            self.stacked_widget.setCurrentIndex(11)
        else:
            self.stacked_widget.setCurrentIndex(4)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(2)

class BasicParametersPage(QWidget):
    """Page for basic parameters (index 4)."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.previous_page = 3  # Default to Punch Combinations

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Basic Parameters")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        # store as instance attribute so other pages can update it
        self.round_btn = QPushButton("Round")
        self.speed_btn = QPushButton("Speed")
        self.time_btn = QPushButton("Time")
        self.rest_btn = QPushButton("Rest")
        
        self.round_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        self.speed_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        self.time_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        self.rest_btn.setStyleSheet(SMALL_BUTTON_STYLE)

        self.round_btn.clicked.connect(self.on_round_clicked)
        self.speed_btn.clicked.connect(self.on_speed_clicked)
        self.time_btn.clicked.connect(self.on_time_clicked)
        self.rest_btn.clicked.connect(self.on_rest_clicked)

        layout.addWidget(title)
        layout.addWidget(self.round_btn)
        layout.addWidget(self.speed_btn)
        layout.addWidget(self.time_btn)
        layout.addWidget(self.rest_btn)
        layout.addStretch()

        # Create horizontal layout for back and continue buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()  # Add space on the left
        
        back_btn = QPushButton("Back")
        self.continue_btn = QPushButton("Continue")  # Initialize continue_btn here
        
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        self.continue_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        
        back_btn.clicked.connect(self.on_back_clicked)
        self.continue_btn.clicked.connect(self.on_continue_clicked)
        
        button_layout.addWidget(back_btn)
        button_layout.addWidget(self.continue_btn)
        button_layout.addStretch()  # Add space on the right

        layout.addLayout(button_layout)

        self.setLayout(layout)
        
        # Disable continue button initially
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
        self.stacked_widget.setCurrentIndex(5)

    def on_speed_clicked(self):
        self.stacked_widget.setCurrentIndex(6)

    def on_time_clicked(self):
        self.stacked_widget.setCurrentIndex(7)

    def on_rest_clicked(self):
        self.stacked_widget.setCurrentIndex(8)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(self.previous_page)

    def on_continue_clicked(self):
        print("Continue button clicked")
        # Start countdown and move to CountdownPage
        countdown_page = self.stacked_widget.widget(9)
        countdown_page.start_countdown()
        self.stacked_widget.setCurrentIndex(9)

class RoundSelectionPage(QWidget):
    """Page showing 12 numbered round buttons and a back button."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Round")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)

        # Create 12 numbered buttons (1..12)
        for idx in range(12):
            n = idx + 1
            btn = QPushButton(str(n))
            btn.setStyleSheet(ROUND_SELECTION_BUTTON_STYLE)
            # call select_round with the selected number and return to BasicParametersPage
            btn.clicked.connect(lambda checked, val=n: self.select_round(val))
            row = idx // 4
            col = idx % 4
            grid.addWidget(btn, row, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        # go back to BasicParametersPage (index 4)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_round(self, n: int):
        """Set the chosen round on BasicParametersPage and switch back."""
        try:
            basic_page = self.stacked_widget.widget(4)
            if hasattr(basic_page, "round_btn"):
                basic_page.round_btn.setText(f"Round\n{n}")
                basic_page.update_continue_button()
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(4)

class SpeedSelectionPage(QWidget):
    """Page offering speed choices (25, 50, 75, 100)."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Speed")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)

        speeds = ["25%", "50%", "75%", "100%"]
        for col, val in enumerate(speeds):
            btn = QPushButton(str(val))
            btn.setStyleSheet(SPEED_SELECTION_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=val: self.select_speed(v))
            grid.addWidget(btn, 0, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_speed(self, n: int):
        """Update BasicParametersPage speed button text and return."""
        try:
            basic_page = self.stacked_widget.widget(4)
            if hasattr(basic_page, "speed_btn"):
                basic_page.speed_btn.setText(f"Speed\n{n}")
                basic_page.update_continue_button()
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(4)

class TimeSelectionPage(QWidget):
    """Page offering time choices (30sec, 1min, 1min30sec, 2min, 2min30sec, 3min)."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Time")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)

        # make columns stretch so buttons get equal width regardless of text
        for c in range(3):
            grid.setColumnStretch(c, 1)

        times = ["30sec", "1min", "1min30sec", "2min", "2min30sec", "3min"]
        # arrange in 3 columns x 2 rows
        for idx, val in enumerate(times):
            btn = QPushButton(val)
            btn.setStyleSheet(TIME_SELECTION_BUTTON_STYLE)
            # ensure all buttons have the same width (columns stretch) and same height
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setFixedHeight(150)   # choose desired uniform height
            btn.clicked.connect(lambda checked, v=val: self.select_time(v))
            row = idx // 3
            col = idx % 3
            grid.addWidget(btn, row, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_time(self, n: str):
        """Update BasicParametersPage time button text and return."""
        try:
            basic_page = self.stacked_widget.widget(4)
            if hasattr(basic_page, "time_btn"):
                basic_page.time_btn.setText(f"Time\n{n}")
                basic_page.update_continue_button()
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(4)

class RestSelectionPage(QWidget):
    """Page offering rest choices (10sec to 60sec in 10sec increments)."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Rest Time")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)

        # make columns stretch so buttons get equal width
        for c in range(3):
            grid.setColumnStretch(c, 1)

        rest_times = ["10sec", "20sec", "30sec", "40sec", "50sec", "1min"]
        # arrange in 3 columns x 2 rows
        for idx, val in enumerate(rest_times):
            btn = QPushButton(val)
            btn.setStyleSheet(TIME_SELECTION_BUTTON_STYLE)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setFixedHeight(150)
            btn.clicked.connect(lambda checked, v=val: self.select_rest(v))
            row = idx // 3
            col = idx % 3
            grid.addWidget(btn, row, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_rest(self, n: str):
        """Update BasicParametersPage rest button text and return."""
        try:
            basic_page = self.stacked_widget.widget(4)
            if hasattr(basic_page, "rest_btn"):
                basic_page.rest_btn.setText(f"Rest\n{n}")
                basic_page.update_continue_button()
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(4)

class CountdownPage(QWidget):
    """Page with 20 second countdown and pause button."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.countdown_value = 20
        self.is_paused = False
        self.on_finished = None  # callback to start training session
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

        self.pause_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)

        self.pause_btn.setFixedWidth(250)
        back_btn.setFixedWidth(250)

        self.pause_btn.clicked.connect(self.toggle_pause)
        back_btn.clicked.connect(self.on_back_clicked)

        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()

        main_layout.addWidget(title)
        main_layout.addWidget(self.countdown_label)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def start_countdown(self):
        """Start the countdown timer."""
        self.countdown_value = 20
        self.is_paused = False
        self.countdown_label.setText(str(self.countdown_value))
        self.pause_btn.setText("Pause")
        self.timer.start(1000)  # Update every 1000ms (1 second)

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
            self.is_paused = False
        else:
            self.timer.stop()
            self.pause_btn.setText("Resume")
            self.is_paused = True

    def on_back_clicked(self):
        """Stop timer and go back to BasicParametersPage."""
        self.timer.stop()
        self.stacked_widget.setCurrentIndex(4)

class TrainingSessionPage(QWidget):
    """Page showing the actual training session with round counter and timer."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_round = 1
        self.total_rounds = 1
        self.work_time = 60  # in seconds
        self.rest_time = 30  # in seconds
        self.time_remaining = self.work_time
        self.is_resting = False
        self.is_paused = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

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

        # Timer in the middle
        self.timer_label = QLabel(self.format_time(self.time_remaining))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")

        # Sequence display (visible only in self-select mode during work)
        self.sequence_label = QLabel("")
        self.sequence_label.setAlignment(Qt.AlignCenter)
        self.sequence_label.setStyleSheet("font-size: 40px; font-weight: bold; color: #2196F3; margin-top: 10px;")
        self.sequence_label.hide()

        # Create horizontal layout for pause and back buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        self.pause_btn = QPushButton("Pause")
        stop_btn = QPushButton("Stop")

        self.pause_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        stop_btn.setStyleSheet(BACK_BUTTON_STYLE_2)

        self.pause_btn.setFixedWidth(250)
        stop_btn.setFixedWidth(250)

        self.pause_btn.clicked.connect(self.toggle_pause)
        stop_btn.clicked.connect(self.on_stop_clicked)

        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(stop_btn)
        button_layout.addStretch()

        main_layout.addWidget(self.round_label)
        main_layout.addWidget(self.rest_label)
        main_layout.addWidget(self.timer_label)
        main_layout.addWidget(self.sequence_label)  # added under the timer
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

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

    def start_session(self, rounds, time_str, rest_str, difficulty=None, sequences=None):
        """Start the training session with the given parameters."""
        self.current_round = 1
        self.total_rounds = rounds

        # Convert time strings to seconds
        self.work_time = self.parse_time_to_seconds(time_str)
        self.rest_time = self.parse_time_to_seconds(rest_str)

        # Self-select setup
        self.is_self_select_mode = (difficulty == "Self-Select") and sequences and len(sequences) > 0
        self.sequences = sequences if self.is_self_select_mode else []
        self.sequence_index = 0
        self.sequence_time_remaining = self.sequence_cycle_seconds if self.sequences else 0

        self.time_remaining = self.work_time
        self.is_resting = False
        self.is_paused = False

        self.round_label.setText(f"Round {self.current_round}/{self.total_rounds}")
        self.rest_label.hide()
        self.timer_label.setText(self.format_time(self.time_remaining))
        self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")
        self.pause_btn.setText("Pause")

        if self.is_self_select_mode:
            self.sequence_label.show()
            self.update_sequence_display()
        else:
            self.sequence_label.hide()

        self.timer.start(1000)  # Update every 1 second

    def update_sequence_display(self):
        """Show the current sequence text."""
        if self.is_self_select_mode and self.sequences:
            self.sequence_label.setText(self.sequences[self.sequence_index])
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
                    self.sequence_label.show()
                    self.update_sequence_display()
                else:
                    self.sequence_label.hide()
            else:
                # Work finished
                if self.current_round < self.total_rounds:
                    # start rest
                    self.is_resting = True
                    self.time_remaining = self.rest_time
                    self.rest_label.show()
                    self.timer_label.setText(self.format_time(self.time_remaining))
                    self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #FF9800;")
                    self.sequence_label.hide()
                else:
                    # final round done
                    self.timer.stop()
                    self.sequence_label.hide()
                    self.stacked_widget.setCurrentIndex(4)

    def toggle_pause(self):
        """Pause or resume the timer."""
        if self.is_paused:
            self.timer.start(1000)
            self.pause_btn.setText("Pause")
            self.is_paused = False
        else:
            self.timer.stop()
            self.pause_btn.setText("Resume")
            self.is_paused = True

    def on_stop_clicked(self):
        """Stop timer and go back to BasicParametersPage."""
        self.timer.stop()
        self.stacked_widget.setCurrentIndex(4)

class SelfSelectSequencePage(QWidget):
    """Page for creating custom punch sequences."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_sequence = []  # Current sequence being built
        self.sequence_list = []  # List of confirmed sequences (max 5)
        self.editing_index = None  # Track which sequence is being edited
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)

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
            seq_btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    padding: 10px;
                    background-color: #f0f0f0;
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    text-align: left;
                    color: black;
                    min-height: 50px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border: 2px solid #2196F3;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
            seq_btn.clicked.connect(lambda checked, idx=i: self.edit_sequence(idx))
            
            # Up button
            up_btn = QPushButton("▲")
            up_btn.setFixedSize(40, 50)
            up_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                }
            """)
            up_btn.clicked.connect(lambda checked, idx=i: self.move_sequence_up(idx))
            
            # Down button
            down_btn = QPushButton("▼")
            down_btn.setFixedSize(40, 50)
            down_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                }
            """)
            down_btn.clicked.connect(lambda checked, idx=i: self.move_sequence_down(idx))
            
            # Delete button
            del_btn = QPushButton("✖")
            del_btn.setFixedSize(40, 50)
            del_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    background-color: #f44336;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #da190b;
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
        
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        self.next_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        
        back_btn.setFixedWidth(150)
        self.next_btn.setFixedWidth(150)
        
        back_btn.clicked.connect(self.on_back_clicked)
        self.next_btn.clicked.connect(self.on_next_clicked)
        
        button_layout.addWidget(back_btn)
        button_layout.addWidget(self.next_btn)

        left_layout.addWidget(list_title)
        left_layout.addLayout(self.sequence_buttons_layout)
        left_layout.addStretch()
        left_layout.addLayout(button_layout)

        # RIGHT SIDE - Input Area
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        # Text box showing current sequence
        self.sequence_input = QLabel("")
        self.sequence_input.setAlignment(Qt.AlignCenter)
        self.sequence_input.setStyleSheet("""
            font-size: 24px;
            padding: 15px;
            background-color: white;
            border: 2px solid #2196F3;
            border-radius: 8px;
            min-height: 60px;
            color: black;
        """)

        # Numpad grid (1-6)
        numpad_grid = QGridLayout()
        numpad_grid.setSpacing(10)
        
        for i in range(6):
            btn = QPushButton(str(i + 1))
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 28px;
                    padding: 20px;
                    min-width: 80px;
                    min-height: 80px;
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
            """)
            btn.clicked.connect(lambda checked, val=str(i + 1): self.add_to_sequence(val))
            row = i // 3
            col = i % 3
            numpad_grid.addWidget(btn, row, col)

        # Defense buttons (Slip-L, Slip-R, Block-L, Block-R)
        defense_grid = QGridLayout()
        defense_grid.setSpacing(10)
        
        defense_moves = ["Slip-L", "Slip-R", "Block-L", "Block-R"]
        for i, move in enumerate(defense_moves):
            btn = QPushButton(move)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    padding: 15px;
                    min-width: 100px;
                    min-height: 60px;
                    background-color: #FF9800;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
                QPushButton:pressed {
                    background-color: #E65100;
                }
            """)
            btn.clicked.connect(lambda checked, val=move: self.add_to_sequence(val))
            row = i // 2
            col = i % 2
            defense_grid.addWidget(btn, row, col)

        # Backspace and Confirm buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        backspace_btn = QPushButton("Backspace")
        self.confirm_btn = QPushButton("Confirm")
        
        backspace_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        self.confirm_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        backspace_btn.clicked.connect(self.backspace_sequence)
        self.confirm_btn.clicked.connect(self.confirm_sequence)
        
        action_layout.addWidget(backspace_btn)
        action_layout.addWidget(self.confirm_btn)

        right_layout.addWidget(self.sequence_input)
        right_layout.addLayout(numpad_grid)
        right_layout.addLayout(defense_grid)
        right_layout.addLayout(action_layout)
        right_layout.addStretch()

        # Add left and right layouts to main layout
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 1)

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
        self.stacked_widget.setCurrentIndex(3)

    def on_next_clicked(self):
        """Go to Basic Parameters page."""
        if len(self.sequence_list) >= 1:
            # Store sequences in BasicParametersPage
            basic_page = self.stacked_widget.widget(4)
            basic_page.custom_sequences = self.sequence_list.copy()
            self.stacked_widget.setCurrentIndex(4)

class DefenseTechniquePage(QWidget):
    """Page to pick a defense technique."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.previous_page = 2  # Default to Techniques page

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Defense Technique")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        for label in ["Slip-Counter", "Weave-Under", "Roll-Under", "Mix"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: self.on_technique_clicked(v))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.previous_page))
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_technique_clicked(self, technique):
        """Store technique and go to Basic Parameters page."""
        basic_page = self.stacked_widget.widget(4)
        basic_page.selected_technique = technique
        basic_page.selected_difficulty = "Defense"
        basic_page.previous_page = 12  # Set to Defense Technique page
        self.stacked_widget.setCurrentIndex(4)

class SparPage(QWidget):
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

        battle_btn = QPushButton("Battle")
        drills_btn = QPushButton("Sparring Drills")
        back_btn = QPushButton("Back")

        battle_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        drills_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

        battle_btn.clicked.connect(self.on_battle_clicked)
        drills_btn.clicked.connect(self.on_drills_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(battle_btn)
        layout.addWidget(drills_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_battle_clicked(self):
        self.stacked_widget.setCurrentIndex(14)

    def on_drills_clicked(self):
        print("Sparring Drills button clicked")
        self.stacked_widget.setCurrentIndex(15)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(1)

class BattlePage(QWidget):
    """Page with Battle style options."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Battle")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        for label in ["Pressure Fighter", "Counter Puncher", "Balanced Boxer", "Out Boxer", "Random"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: self.on_style_clicked(v))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(13))
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_style_clicked(self, style):
        """Store style and go to Basic Parameters page."""
        print(f"{style} selected")
        basic_page = self.stacked_widget.widget(4)
        basic_page.selected_battle_style = style
        basic_page.selected_difficulty = "Battle"
        basic_page.previous_page = 14  # Return here on back
        self.stacked_widget.setCurrentIndex(4)

class SparringDrillsPage(QWidget):
    """Page with Sparring Drills options."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Sparring Drills")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        for label in [
            "Jab-Only Sparring",
            "Counter-Only Sparring",
            "Touch Sparring",
            "Rhythm Change Drill",
            "Defence-Only Round"
        ]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: self.on_drill_clicked(v))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(13))
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_drill_clicked(self, drill):
        """Store drill and go to Basic Parameters page."""
        print(f"{drill} selected")
        basic_page = self.stacked_widget.widget(4)
        basic_page.selected_spar_drill = drill
        basic_page.selected_difficulty = "Sparring Drill"
        basic_page.previous_page = 15  # return here on back
        self.stacked_widget.setCurrentIndex(4)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boxing Training App")
        self.setFixedSize(1024, 600)

        self.stacked_widget = QStackedWidget()

        # Create pages
        self.homepage = Homepage(self.stacked_widget)
        self.training_page = TrainingPage(self.stacked_widget)
        self.techniques_page = TechniquesPage(self.stacked_widget)
        self.punch_combinations_page = PunchCombinationPage(self.stacked_widget)
        self.basic_parameters_page = BasicParametersPage(self.stacked_widget)
        self.round_selection_page = RoundSelectionPage(self.stacked_widget)
        self.speed_selection_page = SpeedSelectionPage(self.stacked_widget)
        self.time_selection_page = TimeSelectionPage(self.stacked_widget)
        self.rest_selection_page = RestSelectionPage(self.stacked_widget)
        self.countdown_page = CountdownPage(self.stacked_widget)
        self.training_session_page = TrainingSessionPage(self.stacked_widget)
        self.self_select_sequence_page = SelfSelectSequencePage(self.stacked_widget)
        self.defense_technique_page = DefenseTechniquePage(self.stacked_widget)
        self.spar_page = SparPage(self.stacked_widget)
        self.battle_page = BattlePage(self.stacked_widget)
        self.sparring_drills_page = SparringDrillsPage(self.stacked_widget)

        # Wire countdown completion to start the training session
        self.countdown_page.on_finished = self.start_training_session

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.homepage)                # 0
        self.stacked_widget.addWidget(self.training_page)           # 1
        self.stacked_widget.addWidget(self.techniques_page)         # 2
        self.stacked_widget.addWidget(self.punch_combinations_page) # 3
        self.stacked_widget.addWidget(self.basic_parameters_page)   # 4
        self.stacked_widget.addWidget(self.round_selection_page)    # 5
        self.stacked_widget.addWidget(self.speed_selection_page)    # 6
        self.stacked_widget.addWidget(self.time_selection_page)     # 7
        self.stacked_widget.addWidget(self.rest_selection_page)     # 8
        self.stacked_widget.addWidget(self.countdown_page)          # 9
        self.stacked_widget.addWidget(self.training_session_page)   # 10
        self.stacked_widget.addWidget(self.self_select_sequence_page) # 11
        self.stacked_widget.addWidget(self.defense_technique_page)  # 12
        self.stacked_widget.addWidget(self.spar_page)            # 13
        self.stacked_widget.addWidget(self.battle_page)          # 14
        self.stacked_widget.addWidget(self.sparring_drills_page)  # 15

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def start_training_session(self):
        """Extract parameters and start the training session."""
        try:
            basic_page = self.stacked_widget.widget(4)
            round_text = basic_page.round_btn.text()
            rounds = int(round_text.split("\n")[1])

            time_text = basic_page.time_btn.text()
            time_str = time_text.split("\n")[1]

            rest_text = basic_page.rest_btn.text()
            rest_str = rest_text.split("\n")[1]

            difficulty = getattr(basic_page, "selected_difficulty", None)
            sequences = getattr(basic_page, "custom_sequences", [])

            training_page = self.stacked_widget.widget(10)
            training_page.start_session(rounds, time_str, rest_str, difficulty, sequences)
            self.stacked_widget.setCurrentIndex(10)
        except Exception as e:
            print(f"Error starting training session: {e}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()