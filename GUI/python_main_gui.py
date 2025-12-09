import sys
import random
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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

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
        self.stacked_widget.setCurrentIndex(16)

    def on_others_clicked(self):
        print("Others button clicked")


class PerformancePage(QWidget):
    """Page with Performance options."""
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
        layout.addWidget(title)

        # Power navigates to instructions page
        power_btn = QPushButton("Power")
        power_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        power_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))
        layout.addWidget(power_btn)

        # Keep others as prints for now
        for label in ["Stamina", "Reaction Time"]:
            btn = QPushButton(label)
            btn.setStyleSheet(SMALL_BUTTON_STYLE)
            btn.clicked.connect(lambda checked, v=label: print(f"{v} clicked"))
            layout.addWidget(btn)

        layout.addStretch()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BACK_BUTTON_STYLE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        self.setLayout(layout)

# New page for Power instructions
class PowerInstructionsPage(QWidget):
    """Instructions page for Power."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 22px; margin-bottom: 20px;")
        layout.addWidget(instructions)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        start_btn = QPushButton("Start")
        back_btn = QPushButton("Back")
        start_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        back_btn.setStyleSheet(BACK_BUTTON_STYLE_2)
        start_btn.setFixedWidth(200)
        back_btn.setFixedWidth(200)

        # Placeholder: hook up to desired flow later
        start_btn.clicked.connect(lambda: print("Power start clicked"))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        btn_row.addWidget(start_btn)
        btn_row.addWidget(back_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)
        self.setLayout(layout)

class Homepage(QWidget):
    def __init__(self, stacked_widget):
       