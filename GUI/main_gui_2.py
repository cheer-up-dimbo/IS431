import sys
import json
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QGridLayout, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt, QTimer

import random
import time

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

# Define shared button styles at module level
PERFORMANCE_BUTTON_STYLE = """
    QPushButton {
        font-size: 20px;
        padding: 40px;
        min-width: 500px;
        min-height: 20px;
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

START_BUTTON_STYLE_2 = """
    QPushButton {
        font-size: 20px;
        padding: 25px;
        min-width: 250px;
        min-height: 40px;
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

HISTORY_BUTTON_STYLE_2 = """
    QPushButton {
        font-size: 20px;
        padding: 25px;
        min-width: 250px;
        min-height: 40px;
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
# Adjusted SMALL_BUTTON_STYLE to a smaller size (change values here to tune)
BASIC_PARAMETERS_BUTTON_STYLE = """
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

# Adjusted Battle Button Style to a smaller size (change values here to tune)
BATTLE_BUTTON_STYLE = """
    QPushButton {
        font-size: 20px;
        padding: 12px;
        min-width: 240px;
        min-height: 40px;
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
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

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

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(training_btn)
        layout.addStretch()
        layout.addWidget(performance_btn)
        layout.addStretch()
        layout.addWidget(others_btn)
        layout.addStretch()

        self.setLayout(layout)

    def on_training_clicked(self):
        print("Training button clicked")
        self.stacked_widget.setCurrentIndex(1)

    def on_performance_clicked(self):
        print("Performance button clicked")
        self.stacked_widget.setCurrentIndex(14)

    def on_others_clicked(self):
        print("Others button clicked")
        self.stacked_widget.setCurrentIndex(22)


class OthersPage(QWidget):
    """Simple page with History and stance toggle."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Others")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        history_btn = QPushButton("History")
        self.stance_btn = QPushButton("Orthodox")
        back_btn = QPushButton("Back")

        history_btn.setStyleSheet(BUTTON_STYLE)
        self.stance_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

        history_btn.clicked.connect(self.on_history_clicked)
        self.stance_btn.clicked.connect(self.on_stance_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(history_btn)
        layout.addStretch()
        layout.addWidget(self.stance_btn)
        layout.addStretch()
        layout.addWidget(back_btn)
        layout.addStretch()

        self.setLayout(layout)

    def on_history_clicked(self):
        print("History clicked - implement others history navigation")

    def on_stance_clicked(self):
        # Toggle button label between Orthodox and Southpaw
        current = self.stance_btn.text().strip()
        self.stance_btn.setText("Southpaw" if current == "Orthodox" else "Orthodox")

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(0)

class PerformancePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Performance")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        power_btn = QPushButton("Power")
        stamina_btn = QPushButton("Stamina")
        reaction_time_btn = QPushButton("Reaction Time")
        back_btn = QPushButton("Back")

        power_btn.setStyleSheet(PERFORMANCE_BUTTON_STYLE)
        stamina_btn.setStyleSheet(PERFORMANCE_BUTTON_STYLE)
        reaction_time_btn.setStyleSheet(PERFORMANCE_BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

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
        self.stacked_widget.setCurrentIndex(15)

    def on_stamina_clicked(self):
        print("Stamina button clicked")
        # Navigate to Stamina Instructions page (index 18)
        self.stacked_widget.setCurrentIndex(18)

    def on_reaction_time_clicked(self):
        print("Reaction Time button clicked")
        # Navigate to Reaction Instructions page (index 19)
        self.stacked_widget.setCurrentIndex(19)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(0)


class StaminaInstructionsPage(QWidget):
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
        start_btn = QPushButton("Start")

        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setStyleSheet(START_BUTTON_STYLE_2)

        back_btn.setFixedWidth(250)
        start_btn.setFixedWidth(250)

        back_btn.clicked.connect(self.on_back_clicked)
        start_btn.clicked.connect(self.on_start_clicked)

        button_layout.addWidget(back_btn)
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
        self.stacked_widget.setCurrentIndex(14)

    def on_start_clicked(self):
        try:
            countdown_page = self.stacked_widget.widget(9)
            countdown_page.on_finished = self.launch_stamina_punch_page
            countdown_page.return_page_index = 18  # back should return to stamina instructions
            countdown_page.start_countdown()
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(9)

    def launch_stamina_punch_page(self):
        try:
            punch_page = self.stacked_widget.widget(16)
            punch_page.reset_counter()
            self.stacked_widget.setCurrentIndex(16)
        except Exception:
            self.stacked_widget.setCurrentIndex(14)


class ReactionInstructionsPage(QWidget):
    """Instructions page for the Reaction Time mode."""
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
            "2. Wait until the screen turns green.\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 28px; font-weight: bold;")

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        back_btn = QPushButton("Back")
        start_btn = QPushButton("Start")

        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setStyleSheet(START_BUTTON_STYLE_2)

        back_btn.setFixedWidth(250)
        start_btn.setFixedWidth(250)

        back_btn.clicked.connect(self.on_back_clicked)
        start_btn.clicked.connect(self.on_start_clicked)

        button_layout.addWidget(back_btn)
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
        self.stacked_widget.setCurrentIndex(14)

    def on_start_clicked(self):
        try:
            countdown_page = self.stacked_widget.widget(9)
            countdown_page.on_finished = self.launch_reaction_test_page
            countdown_page.return_page_index = 19  # back should return to reaction instructions
            countdown_page.start_countdown()
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(9)

    def launch_reaction_test_page(self):
        try:
            reaction_test_page = self.stacked_widget.widget(20)
            reaction_test_page.start_test()
            self.stacked_widget.setCurrentIndex(20)
        except Exception:
            self.stacked_widget.setCurrentIndex(14)

class PowerInstructionsPage(QWidget):
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
        start_btn = QPushButton("Start")

        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setStyleSheet(START_BUTTON_STYLE_2)

        back_btn.setFixedWidth(250)
        start_btn.setFixedWidth(250)

        back_btn.clicked.connect(self.on_back_clicked)
        start_btn.clicked.connect(self.on_start_clicked)

        button_layout.addWidget(back_btn)
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
        self.stacked_widget.setCurrentIndex(14)

    def on_start_clicked(self):
        # Start the existing countdown flow then show CountdownPage (index 9)
        try:
            countdown_page = self.stacked_widget.widget(9)
            # When countdown finishes, go to Power Punch page
            countdown_page.on_finished = self.launch_power_punch_page
            countdown_page.return_page_index = 15  # back should return to instructions
            countdown_page.start_countdown()
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(9)

    def launch_power_punch_page(self):
        """Switch to the punch counting page after countdown."""
        try:
            punch_page = self.stacked_widget.widget(16)
            punch_page.reset_counter()
            self.stacked_widget.setCurrentIndex(16)
        except Exception:
            # If page not available, fall back to Performance page
            self.stacked_widget.setCurrentIndex(14)

class PowerPunchPage(QWidget):
    """Page to count power punches after countdown."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.target = 10
        self.count = 0

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
        quit_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
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
        self.count = 0
        self.counter_label.setText(self.counter_text())

    def mousePressEvent(self, event):
        """Increment punch count on screen press until target reached."""
        if self.count < self.target:
            self.count += 1
            self.counter_label.setText(self.counter_text())
            if self.count >= self.target:
                # Proceed to next page when target reached
                self.on_completed()
        super().mousePressEvent(event)

    def on_completed(self):
        """Called when punch target is reached."""
        # Navigate to Power Result page after completion
        try:
            result_page = self.stacked_widget.widget(17)
            if hasattr(result_page, "set_power_output"):
                result_page.set_power_output("100 kN")
            self.stacked_widget.setCurrentIndex(17)
        except Exception:
            # Fallback if result page not available
            self.stacked_widget.setCurrentIndex(14)

    def on_quit_clicked(self):
        # Abort and return to Performance page
        self.stacked_widget.setCurrentIndex(14)

class PowerResultPage(QWidget):
    """Result page shown after completing the Power punches."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        # Center message
        self.result_label = QLabel("Punches Thrown in a Minute: 100")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        history_btn = QPushButton("History")
        restart_btn = QPushButton("Restart")
        quit_btn = QPushButton("Quit")

        history_btn.setStyleSheet(HISTORY_BUTTON_STYLE_2)
        restart_btn.setStyleSheet(START_BUTTON_STYLE_2)
        quit_btn.setStyleSheet(BACK_BUTTON_STYLE_2)

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
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_power_output(self, value_str: str):
        self.result_label.setText(f"Your Power Output: {value_str}")

    def on_history_clicked(self):
        # Placeholder: no history page yet
        print("History clicked - implement history page navigation here")

    def on_restart_clicked(self):
        # Return to the Power Instructions to restart the flow
        self.stacked_widget.setCurrentIndex(15)

    def on_quit_clicked(self):
        # Return to Performance menu
        self.stacked_widget.setCurrentIndex(14)

class ReactionTestPage(QWidget):
    """Red/green screen to measure reaction time after countdown."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.state = "red"
        self.reaction_start_time = None

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
        self.reaction_start_time = None
        self.setStyleSheet("background-color: #b71c1c;")
        self.status_label.setText("Do Not Punch")

    def schedule_green(self):
        delay_ms = random.randint(5, 10) * 1000
        self.green_timer.stop()
        self.green_timer.start(delay_ms)

    def start_test(self):
        self.set_red_state()
        self.schedule_green()

    def flash_text(self):
        self.status_label.setText("")
        QTimer.singleShot(150, lambda: self.status_label.setText("Do Not Punch"))

    def go_green(self):
        self.state = "green"
        self.reaction_start_time = time.perf_counter()
        self.setStyleSheet("background-color: #2e7d32;")
        self.status_label.setText("Punch Now")

    def mousePressEvent(self, event):
        if self.state == "red":
            self.flash_text()
            self.schedule_green()
        elif self.state == "green":
            self.green_timer.stop()
            reaction_time = 0.0
            if self.reaction_start_time is not None:
                reaction_time = max(0.0, time.perf_counter() - self.reaction_start_time)
            try:
                result_page = self.stacked_widget.widget(21)
                if hasattr(result_page, "set_reaction_time"):
                    result_page.set_reaction_time(reaction_time)
                self.stacked_widget.setCurrentIndex(21)
            except Exception:
                self.stacked_widget.setCurrentIndex(14)
        super().mousePressEvent(event)

class ReactionResultPage(QWidget):
    """Shows measured reaction time after the test."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        self.result_label = QLabel("Reaction Time: -- s")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        history_btn = QPushButton("History")
        restart_btn = QPushButton("Restart")
        back_btn = QPushButton("Back")

        history_btn.setStyleSheet(HISTORY_BUTTON_STYLE_2)
        restart_btn.setStyleSheet(START_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)

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
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_reaction_time(self, seconds: float):
        self.result_label.setText(f"Reaction Time: {seconds:.3f} s")

    def on_history_clicked(self):
        # Placeholder: add history navigation when available
        print("History clicked - implement reaction history navigation")

    def on_restart_clicked(self):
        self.stacked_widget.setCurrentIndex(19)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(14)

class TrainingPage(QWidget):
    """
    TrainingPage class for displaying training options in a GUI application.
    This class extends QWidget and provides a user interface for selecting different
    training activities. It displays a centered layout with buttons for accessing
    techniques and sparring features, along with a back button for navigation.
    Attributes:
        stacked_widget (QStackedWidget): Reference to the parent stacked widget for
            managing page navigation between different sections of the application.
    Methods:
        __init__(stacked_widget): Initializes the TrainingPage with UI components
            including title, buttons, and layout configuration.
        on_techniques_clicked(): Handles the techniques button click event and
            navigates to the Techniques page (index 2).
        on_spar_clicked(): Handles the spar button click event and navigates to
            the SparPage (index 12).
        on_back_clicked(): Handles the back button click event and returns to
            the main page (index 0).
    """
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
        # SparPage is now at index 12 after removing DefenseTechniquePage
        self.stacked_widget.setCurrentIndex(12)

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
        back_btn = QPushButton("Back")

        punch_lib_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

        punch_lib_btn.clicked.connect(self.on_punch_combination_library_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(punch_lib_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_punch_combination_library_clicked(self):
        print("Punch Combination Library button clicked")
        self.stacked_widget.setCurrentIndex(3)

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
        
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        # Continue button should be green like Start actions
        self.continue_btn.setStyleSheet(START_BUTTON_STYLE_2)
        
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
        # Ensure training flow uses the training session start callback
        parent_window = self.stacked_widget.parent()
        if parent_window and hasattr(parent_window, "start_training_session"):
            countdown_page.on_finished = parent_window.start_training_session
        # Back from countdown should return to Basic Parameters during training flow
        countdown_page.return_page_index = 4
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
        # Where to return if user presses Back during countdown
        self.return_page_index = 4
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
        self.countdown_value = 20
        self.is_paused = False
        self.countdown_label.setText(str(self.countdown_value))
        self.pause_btn.setText("Pause")
        # Ensure Pause button starts in red style
        self.pause_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
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
            # Back to red when resuming (showing "Pause")
            self.pause_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
            self.is_paused = False
        else:
            self.timer.stop()
            self.pause_btn.setText("Resume")
            # Green while paused (showing "Resume")
            self.pause_btn.setStyleSheet(START_BUTTON_STYLE_2)
            self.is_paused = True

    def on_back_clicked(self):
        """Stop timer and go back to BasicParametersPage."""
        self.timer.stop()
        self.stacked_widget.setCurrentIndex(self.return_page_index)

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

        # Training mode attributes
        self.difficulty = None
        self.battle_style = None

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

        main_layout.addStretch()
        main_layout.addWidget(self.round_label)
        main_layout.addStretch()
        main_layout.addWidget(self.rest_label)
        main_layout.addStretch()
        main_layout.addWidget(self.timer_label)
        main_layout.addStretch()
        main_layout.addWidget(self.sequence_label)  # added under the timer
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
            else:
                # For other modes (Stamina, Reaction Time, Power, etc.)
                payload = {
                    "mode": self.difficulty,
                }
            print(json.dumps(payload))
        except Exception as e:
            print(f"Error sending round start message: {e}")

    def start_session(self, rounds, time_str, rest_str, difficulty=None, sequences=None, battle_style=None):
        """Start the training session with the given parameters."""
        self.current_round = 1
        self.total_rounds = rounds
        self.difficulty = difficulty
        self.battle_style = battle_style

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
        # Ensure Pause button starts in red style
        self.pause_btn.setStyleSheet(BACK_BUTTON_STYLE_2)

        if self.is_self_select_mode:
            self.sequence_label.show()
            self.update_sequence_display()
        else:
            self.sequence_label.hide()

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
                
                # Send round start message for new round
                self.send_round_start_message()
                
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
            # Back to red when resuming (showing "Pause")
            self.pause_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
            self.is_paused = False
        else:
            self.timer.stop()
            self.pause_btn.setText("Resume")
            # Green while paused (showing "Resume")
            self.pause_btn.setStyleSheet(START_BUTTON_STYLE_2)
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
        back_btn = QPushButton("Back")

        # Make Battle button look the same as the Spar button in TrainingPage
        battle_btn.setStyleSheet(BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

        battle_btn.clicked.connect(self.on_battle_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(battle_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_battle_clicked(self):
        # BattlePage index moved to 13 after removing defense page
        self.stacked_widget.setCurrentIndex(13)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(1)

class BattlePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(24)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Battle")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 8px;")

        buttons = [
            QPushButton("Pressure Fighter"),
            QPushButton("Counter Puncher"),
            QPushButton("Balanced Boxer"),
            QPushButton("Out Boxer"),
            QPushButton("Random"),
        ]
        back_btn = QPushButton("Back")

        for b in buttons:
            b.setStyleSheet(BATTLE_BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

        # wire clicks
        buttons[0].clicked.connect(lambda: self.on_style_clicked("Pressure Fighter"))
        buttons[1].clicked.connect(lambda: self.on_style_clicked("Counter Puncher"))
        buttons[2].clicked.connect(lambda: self.on_style_clicked("Balanced Boxer"))
        buttons[3].clicked.connect(lambda: self.on_style_clicked("Out Boxer"))
        buttons[4].clicked.connect(lambda: self.on_style_clicked("Random"))
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addStretch(1)
        layout.addWidget(title)
        for b in buttons:
            layout.addStretch(1)
            layout.addWidget(b)
        layout.addStretch(1)
        layout.addWidget(back_btn)
        layout.addStretch(1)

        self.setLayout(layout)

    def on_style_clicked(self, style):
        """Store style and go to Basic Parameters page."""
        print(f"{style} selected")
        basic_page = self.stacked_widget.widget(4)
        basic_page.selected_battle_style = style
        basic_page.selected_difficulty = "Battle"
        # BattlePage is now index 13
        basic_page.previous_page = 13  # Return here on back
        self.stacked_widget.setCurrentIndex(4)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(12)

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
        self.spar_page = SparPage(self.stacked_widget)
        self.battle_page = BattlePage(self.stacked_widget)
        self.performance_page = PerformancePage(self.stacked_widget)
        self.power_instructions_page = PowerInstructionsPage(self.stacked_widget)
        self.power_punch_page = PowerPunchPage(self.stacked_widget)
        self.power_result_page = PowerResultPage(self.stacked_widget)
        self.stamina_instructions_page = StaminaInstructionsPage(self.stacked_widget)
        self.reaction_instructions_page = ReactionInstructionsPage(self.stacked_widget)
        self.reaction_test_page = ReactionTestPage(self.stacked_widget)
        self.reaction_result_page = ReactionResultPage(self.stacked_widget)
        self.others_page = OthersPage(self.stacked_widget)

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
        self.stacked_widget.addWidget(self.spar_page)            # 12
        self.stacked_widget.addWidget(self.battle_page)          # 13
        self.stacked_widget.addWidget(self.performance_page)     # 14
        self.stacked_widget.addWidget(self.power_instructions_page) # 15
        self.stacked_widget.addWidget(self.power_punch_page) # 16
        self.stacked_widget.addWidget(self.power_result_page) # 17
        self.stacked_widget.addWidget(self.stamina_instructions_page) # 18
        self.stacked_widget.addWidget(self.reaction_instructions_page) # 19
        self.stacked_widget.addWidget(self.reaction_test_page) # 20
        self.stacked_widget.addWidget(self.reaction_result_page) # 21
        self.stacked_widget.addWidget(self.others_page) # 22

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
            battle_style = getattr(basic_page, "selected_battle_style", None)

            # Emit payload when countdown ends (battle or punch-library flows)
            # Skip emission for Self-Select; it will emit per-sequence refresh instead
            # if (difficulty != "Self-Select") and (difficulty or battle_style):
            #     payload = {
            #         "mode": difficulty,
            #         "battle_style": battle_style,
            #         "sequences": sequences,
            #     }
            #     print(json.dumps(payload))

            training_page = self.stacked_widget.widget(10)
            training_page.start_session(rounds, time_str, rest_str, difficulty, sequences, battle_style)
            self.stacked_widget.setCurrentIndex(10)
        except Exception as e:
            print(f"Error starting training session: {e}")

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