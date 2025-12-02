import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget
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
        font-size: 22px;
        padding: 18px;
        min-width: 320px;
        min-height: 44px;
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

        round_btn = QPushButton("Round")
        speed_btn = QPushButton("Speed")
        time_btn = QPushButton("Time")
        rest_btn = QPushButton("Rest")
        back_btn = QPushButton("Back")

        round_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        speed_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        time_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        rest_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)

        round_btn.clicked.connect(self.on_round_clicked)
        speed_btn.clicked.connect(self.on_speed_clicked)
        time_btn.clicked.connect(self.on_time_clicked)
        rest_btn.clicked.connect(self.on_rest_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(round_btn)
        layout.addWidget(speed_btn)
        layout.addWidget(time_btn)
        layout.addWidget(rest_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_round_clicked(self):
        print("Round button clicked")

    def on_speed_clicked(self):
        print("Speed button clicked")

    def on_time_clicked(self):
        print("Time button clicked")

    def on_rest_clicked(self):
        print("Rest button clicked")

    def on_back_clicked(self):
        # go back to PunchCombinationPage (index 3)
        self.stacked_widget.setCurrentIndex(3)

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

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.homepage)               # Index 0
        self.stacked_widget.addWidget(self.training_page)         # Index 1
        self.stacked_widget.addWidget(self.techniques_page)       # Index 2
        self.stacked_widget.addWidget(self.punch_combinations_page) # Index 3
        self.stacked_widget.addWidget(self.basic_parameters_page)        # Index 4

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