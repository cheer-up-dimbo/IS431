from __future__ import annotations

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy)
from PySide6.QtCore import Qt
from core.navigation import ButtonNavigationMixin
from core.constants import PageIndex, ButtonStyle
from utils import load_users, save_users, set_user_level


class ProficiencyChecklistPage(ButtonNavigationMixin, QWidget):
    LAYOUT_SPACING = 12
    LAYOUT_MARGINS = (40, 20, 40, 20)
    SKIP_NORMALIZE = True
    SKIP_NAV_SETUP = True

    _QUESTIONS = [
        ("Have you trained boxing before?", ["Never", "A few times", "Regularly"]),
        ("Do you know the basic punches (jab, cross, hook, uppercut)?", ["No", "Somewhat", "Yes"]),
        ("Can you throw a basic 1-2-3 combo?", ["No", "With help", "Yes"]),
        ("Have you done any sparring before?", ["Never", "Once or twice", "Yes regularly"]),
        ("How would you describe your fitness level?", ["Low", "Moderate", "High"]),
        ("Have you used boxing equipment before (bag, pads)?", ["Never", "Occasionally", "Often"]),
    ]

    _OPTION_BASE_STYLE = """
        QPushButton {
            font-size: 14px;
            min-width: 108px;
            min-height: 44px;
            background-color: #555555;
            color: white;
            border: 2px solid #555555;
            border-radius: 8px;
            padding: 8px 12px;
        }
        QPushButton:hover {
            background-color: #666666;
            border-color: #666666;
        }
    """

    _OPTION_SELECTED_STYLE = """
        QPushButton {
            font-size: 14px;
            min-width: 108px;
            min-height: 44px;
            background-color: #4CAF50;
            color: white;
            border: 2px solid #2e7d32;
            border-radius: 8px;
            padding: 8px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #4CAF50;
            border-color: #2e7d32;
        }
    """

    _SMALL_BTN_STYLE = """
        QPushButton {
            font-size: 14px;
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 8px;
        }
        QPushButton:hover { background-color: #d32f2f; }
    """

    _NEXT_DISABLED_STYLE = """
        QPushButton {
            font-size: 14px;
            background-color: #777777;
            color: #dddddd;
            border: none;
            border-radius: 8px;
        }
        QPushButton:hover { background-color: #777777; }
    """

    _NEXT_ENABLED_STYLE = """
        QPushButton {
            font-size: 14px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        }
        QPushButton:hover { background-color: #388e3c; }
    """

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self._username = ""
        self._selected_indices = [None] * len(self._QUESTIONS)
        self._question_option_buttons = []

        main_layout = QVBoxLayout()
        main_layout.setSpacing(self.LAYOUT_SPACING)
        main_layout.setContentsMargins(*self.LAYOUT_MARGINS)

        title = QLabel("Quick Proficiency Check")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; color: white;")
        main_layout.addWidget(title)

        subtitle = QLabel("Tell us your background so we can suggest your starting level")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 15px; color: #aaaaaa;")
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(8)

        for question_index, (question_text, options) in enumerate(self._QUESTIONS):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(10)

            question_label = QLabel(question_text)
            question_label.setStyleSheet("font-size: 16px; color: white;")
            question_label.setFixedWidth(540)
            question_label.setWordWrap(True)
            question_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
            row_layout.addWidget(question_label, alignment=Qt.AlignVCenter)

            option_layout = QHBoxLayout()
            option_layout.setSpacing(8)
            option_buttons = []

            for option_index, option_text in enumerate(options):
                option_btn = QPushButton(option_text)
                option_btn.setStyleSheet(self._OPTION_BASE_STYLE)
                option_btn.clicked.connect(
                    lambda checked=False, qi=question_index, oi=option_index: self._select_option(qi, oi)
                )
                option_layout.addWidget(option_btn)
                option_buttons.append(option_btn)

            row_layout.addLayout(option_layout)
            main_layout.addLayout(row_layout)
            self._question_option_buttons.append(option_buttons)

        main_layout.addStretch()

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(16)
        bottom_row.setContentsMargins(0, 0, 0, 0)

        self._next_enabled_style = self._NEXT_ENABLED_STYLE
        self._next_disabled_style = self._NEXT_DISABLED_STYLE

        def _make_small_widget(btn, style):
            btn.setStyleSheet(style)
            container = QWidget()
            container.setFixedSize(120, 40)
            container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            inner = QHBoxLayout(container)
            inner.setContentsMargins(0, 0, 0, 0)
            inner.setSpacing(0)
            inner.addWidget(btn)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            return container

        skip_btn = QPushButton("Skip")
        skip_btn.clicked.connect(self._on_skip)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self._discard_and_go_back)

        self.next_btn = QPushButton("Next")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self._on_next)

        bottom_row.addWidget(_make_small_widget(skip_btn, self._SMALL_BTN_STYLE))
        bottom_row.addWidget(_make_small_widget(back_btn, self._SMALL_BTN_STYLE))
        bottom_row.addStretch()
        bottom_row.addWidget(_make_small_widget(self.next_btn, self._NEXT_DISABLED_STYLE))

        main_layout.addLayout(bottom_row)
        self.setLayout(main_layout)

    def load_for_user(self, username: str):
        self._username = username
        self._selected_indices = [None] * len(self._QUESTIONS)
        self._refresh_question_buttons()
        self._refresh_next_button_state()

    def _select_option(self, question_index: int, option_index: int):
        if self._selected_indices[question_index] == option_index:
            return

        self._selected_indices[question_index] = option_index
        self._refresh_question_buttons()
        self._refresh_next_button_state()

    def _refresh_question_buttons(self):
        for question_index, buttons in enumerate(self._question_option_buttons):
            selected_option = self._selected_indices[question_index]
            for option_index, btn in enumerate(buttons):
                if selected_option == option_index:
                    btn.setStyleSheet(self._OPTION_SELECTED_STYLE)
                else:
                    btn.setStyleSheet(self._OPTION_BASE_STYLE)

    def _refresh_next_button_state(self):
        all_answered = all(index is not None for index in self._selected_indices)
        self.next_btn.setEnabled(all_answered)
        if all_answered:
            self.next_btn.setStyleSheet(self._next_enabled_style)
        else:
            self.next_btn.setStyleSheet(self._next_disabled_style)

    def _on_skip(self):
        if self._username:
            set_user_level(self._username, "Beginner")
        self.navigate_to(PageIndex.HOMEPAGE)

    def _discard_and_go_back(self):
        if self._username:
            users = load_users()
            if self._username in users:
                users.pop(self._username, None)
                save_users(users)
        self.navigate_to(PageIndex.LOGIN)

    def _on_next(self):
        if not all(index is not None for index in self._selected_indices):
            return

        score = sum(self._selected_indices)

        if score <= 4:
            suggested_level = "Beginner"
        elif score <= 8:
            suggested_level = "Intermediate"
        else:
            suggested_level = "Advanced"

        result_page = self.stacked_widget.widget(PageIndex.PROFICIENCY_RESULT)
        if result_page is not None and hasattr(result_page, "load"):
            result_page.load(self._username, suggested_level)
        self.navigate_to(PageIndex.PROFICIENCY_RESULT)


class ProficiencyResultPage(ButtonNavigationMixin, QWidget):
    LAYOUT_SPACING = 18
    LAYOUT_MARGINS = (80, 30, 80, 30)

    _LEVELS = ["Beginner", "Intermediate", "Advanced"]
    _LEVEL_DESCRIPTIONS = {
        "Beginner": "New to boxing. You'll start with fundamental punches and basic combos.",
        "Intermediate": "Some boxing experience. You'll work on combinations and technique.",
        "Advanced": "Experienced boxer. You'll tackle complex combos and sparring modes.",
    }

    _LEVEL_UNSELECTED_STYLE = """
        QPushButton {
            font-size: 18px;
            min-width: 180px;
            min-height: 60px;
            background-color: #555555;
            color: white;
            border: 3px solid #555555;
            border-radius: 10px;
            padding: 10px 14px;
        }
        QPushButton:hover {
            background-color: #666666;
            border-color: #666666;
        }
    """

    _LEVEL_SELECTED_STYLE = """
        QPushButton {
            font-size: 18px;
            min-width: 180px;
            min-height: 60px;
            background-color: #4CAF50;
            color: white;
            border: 3px solid #2e7d32;
            border-radius: 10px;
            padding: 10px 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #4CAF50;
            border-color: #2e7d32;
        }
    """

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self._username = ""
        self._suggested_level = "Beginner"
        self._chosen_level = "Beginner"
        self._level_buttons = {}

        main_layout = QVBoxLayout()
        main_layout.setSpacing(self.LAYOUT_SPACING)
        main_layout.setContentsMargins(*self.LAYOUT_MARGINS)

        self.title_label = QLabel("Your Proficiency Result")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        main_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("Based on your answers, we suggest:")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("font-size: 16px; color: #aaaaaa;")
        main_layout.addWidget(self.subtitle_label)

        self.suggestion_label = QLabel("Beginner")
        self.suggestion_label.setAlignment(Qt.AlignCenter)
        self.suggestion_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #4CAF50;")
        main_layout.addWidget(self.suggestion_label)

        main_layout.addStretch()

        choose_label = QLabel("You can still choose your own level:")
        choose_label.setAlignment(Qt.AlignCenter)
        choose_label.setStyleSheet("font-size: 15px; color: white;")
        main_layout.addWidget(choose_label)

        level_row = QHBoxLayout()
        level_row.setSpacing(12)

        for level in self._LEVELS:
            btn = QPushButton(level)
            btn.setStyleSheet(self._LEVEL_UNSELECTED_STYLE)
            btn.setMinimumWidth(180)
            btn.setMinimumHeight(60)
            btn.clicked.connect(lambda checked=False, lvl=level: self._on_level_clicked(lvl))
            level_row.addWidget(btn)
            self._level_buttons[level] = btn

        main_layout.addLayout(level_row)

        self.level_description_label = QLabel("")
        self.level_description_label.setAlignment(Qt.AlignCenter)
        self.level_description_label.setWordWrap(True)
        self.level_description_label.setStyleSheet("font-size: 14px; color: #cccccc;")
        self.level_description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        main_layout.addWidget(self.level_description_label)

        main_layout.addStretch()

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(16)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        back_btn.clicked.connect(lambda: self.navigate_to(PageIndex.PROFICIENCY_CHECKLIST))

        confirm_btn = QPushButton("Confirm")
        confirm_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        confirm_btn.clicked.connect(self._on_confirm)

        bottom_row.addWidget(back_btn)
        bottom_row.addStretch()
        bottom_row.addWidget(confirm_btn)

        main_layout.addLayout(bottom_row)
        self.setLayout(main_layout)

    def load(self, username: str, suggested_level: str):
        self._username = username
        if suggested_level in self._LEVELS:
            self._suggested_level = suggested_level
        else:
            self._suggested_level = "Beginner"

        self._chosen_level = self._suggested_level
        self.suggestion_label.setText(self._suggested_level)
        self._refresh_level_buttons()
        self._refresh_level_description()

    def _on_level_clicked(self, level: str):
        if level not in self._LEVELS:
            return
        self._chosen_level = level
        self._refresh_level_buttons()
        self._refresh_level_description()

    def _refresh_level_buttons(self):
        for level, btn in self._level_buttons.items():
            if level == self._chosen_level:
                btn.setStyleSheet(self._LEVEL_SELECTED_STYLE)
            else:
                btn.setStyleSheet(self._LEVEL_UNSELECTED_STYLE)

    def _refresh_level_description(self):
        self.level_description_label.setText(self._LEVEL_DESCRIPTIONS.get(self._chosen_level, ""))

    def _on_confirm(self):
        if self._username:
            set_user_level(self._username, self._chosen_level)
        self.navigate_to(PageIndex.HOMEPAGE)
