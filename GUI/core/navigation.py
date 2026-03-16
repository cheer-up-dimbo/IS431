from typing import List
from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QSizePolicy
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtGui import QColor


class ButtonNavigationMixin:
    """Provides consistent button styling and keyboard navigation."""

    BUTTON_STYLE = """
        QPushButton {
            font-size: 20px;
            padding: 20px;
            background-color: #1E293B;
            border: 2px solid #334155;
            border-radius: 10px;
            min-width: 360px;
            max-width: 420px;
            min-height: 65px;
            color: #F8FAFC;
            font-weight: 600;
        }
        QPushButton:focus {
            border: 4px solid #F97316;
            background-color: #263347;
            color: #F8FAFC;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #263347;
            border-color: #F97316;
        }
        QPushButton:pressed {
            background-color: #F97316;
            color: #0F172A;
            border-color: #F97316;
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
                glow.setColor(QColor(249, 115, 22, 220))
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
