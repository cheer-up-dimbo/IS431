import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt

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

        beginner_btn.clicked.connect(self.on_beginner_clicked)
        intermediate_btn.clicked.connect(self.on_intermediate_clicked)
        advanced_btn.clicked.connect(self.on_advanced_clicked)
        self_select_btn.clicked.connect(self.on_self_select_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(beginner_btn)
        layout.addWidget(intermediate_btn)
        layout.addWidget(advanced_btn)
        layout.addWidget(self_select_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_beginner_clicked(self):
        print("Beginner button clicked")
        self.stacked_widget.setCurrentIndex(4)

    def on_intermediate_clicked(self):
        print("Intermediate button clicked")
        self.stacked_widget.setCurrentIndex(4)

    def on_advanced_clicked(self):
        print("Advanced button clicked")
        self.stacked_widget.setCurrentIndex(4)

    def on_self_select_clicked(self):
        print("Self-Select button clicked")
        self.stacked_widget.setCurrentIndex(4)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(2)

class BasicParametersPage(QWidget):
    """Page for basic parameters (index 4)."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Basic Parameters")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        # store as instance attribute so other pages can update it
        self.round_btn = QPushButton("Round")
        self.speed_btn = QPushButton("Speed")        # changed to instance attribute
        self.time_btn = QPushButton("Time")
        self.rest_btn = QPushButton("Rest")
        back_btn = QPushButton("Back")

        self.round_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        self.speed_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        self.time_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        self.rest_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

        self.round_btn.clicked.connect(self.on_round_clicked)
        self.speed_btn.clicked.connect(self.on_speed_clicked)   # opens speed selection page
        self.time_btn.clicked.connect(self.on_time_clicked)
        self.rest_btn.clicked.connect(self.on_rest_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(self.round_btn)
        layout.addWidget(self.speed_btn)
        layout.addWidget(self.time_btn)
        layout.addWidget(self.rest_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_round_clicked(self):
        # open RoundSelectionPage (index 5)
        self.stacked_widget.setCurrentIndex(5)

    def on_speed_clicked(self):
        # open SpeedSelectionPage (index 6)
        self.stacked_widget.setCurrentIndex(6)

    def on_time_clicked(self):
        # open TimeSelectionPage (index 7)
        self.stacked_widget.setCurrentIndex(7)

    def on_rest_clicked(self):
        print("Rest button clicked")

    def on_back_clicked(self):
        # go back to PunchCombinationPage (index 3)
        self.stacked_widget.setCurrentIndex(3)

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
        # widget index 4 is BasicParametersPage in MainWindow setup
        try:
            basic_page = self.stacked_widget.widget(4)
            # ensure target has attribute round_btn
            if hasattr(basic_page, "round_btn"):
                basic_page.round_btn.setText(f"Round\n{n}")
        except Exception:
            pass
        # go back to BasicParametersPage
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
        except Exception:
            pass
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
        self.speed_selection_page = SpeedSelectionPage(self.stacked_widget)   # added
        self.time_selection_page = TimeSelectionPage(self.stacked_widget)     # added

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.homepage)               # Index 0
        self.stacked_widget.addWidget(self.training_page)         # Index 1
        self.stacked_widget.addWidget(self.techniques_page)       # Index 2
        self.stacked_widget.addWidget(self.punch_combinations_page) # Index 3
        self.stacked_widget.addWidget(self.basic_parameters_page)        # Index 4
        self.stacked_widget.addWidget(self.round_selection_page)         # Index 5
        self.stacked_widget.addWidget(self.speed_selection_page)         # Index 6
        self.stacked_widget.addWidget(self.time_selection_page)          # Index 7

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()