"""Tooltip bubble system for the BoxBunny GUI (1024×600 touchscreen)."""
from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt, QTimer, QObject, QEvent, QPoint


class TooltipBubble(QLabel):
    """Dark rounded bubble that floats over MainWindow's child widgets."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignLeft)
        self.setMaximumWidth(260)
        self.setStyleSheet(
            "background-color: #222222;"
            "color: white;"
            "font-size: 13px;"
            "padding: 8px 12px;"
            "border-radius: 10px;"
            "border: 1px solid #444444;"
        )
        self.hide()

    def show_near(self, button: QWidget, main_window: QWidget) -> None:
        """Position the bubble to the right of *button* (clamped to 1024×600)."""
        global_pos = button.mapToGlobal(QPoint(0, 0))
        local_pos = main_window.mapFromGlobal(global_pos)

        hint = self.sizeHint()

        x = local_pos.x() + button.width() + 12
        y = local_pos.y() + (button.height() // 2) - (hint.height() // 2)

        # Clamp within 1024×600
        x = min(x, 1024 - hint.width() - 8)
        y = max(8, min(y, 600 - hint.height() - 8))

        # If placing right would overlap the button, place left instead
        if x < local_pos.x() + button.width():
            x = local_pos.x() - hint.width() - 12

        self.move(x, y)
        self.raise_()
        self.show()


# ---------------------------------------------------------------------------
# Event-filter helper (one instance per button)
# ---------------------------------------------------------------------------

class _ButtonEventFilter(QObject):
    def __init__(
        self,
        button: QPushButton,
        text: str,
        bubble: TooltipBubble,
        main_window: QWidget,
        timer: QTimer,
    ) -> None:
        super().__init__(button)  # parent = button keeps lifetime in sync
        self._button = button
        self._text = text
        self._bubble = bubble
        self._main_window = main_window
        self._timer = timer

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        t = event.type()

        if t in (QEvent.Enter, QEvent.MouseButtonPress):
            self._timer.start()

        elif t in (QEvent.Leave, QEvent.MouseButtonRelease):
            self._timer.stop()
            if (
                self._bubble.isVisible()
                and self._bubble.property("owner") is self._button
            ):
                self._bubble.hide()

        return False  # never consume the event


def attach_tooltip(
    button: QPushButton,
    text: str,
    main_window: QWidget,
    long_press_ms: int = 500,
) -> None:
    """Install long-press tooltip behaviour on *button*."""

    # One shared bubble per MainWindow
    if not hasattr(main_window, "_tooltip_bubble"):
        main_window._tooltip_bubble = TooltipBubble(main_window)
    bubble: TooltipBubble = main_window._tooltip_bubble

    timer = QTimer()
    timer.setSingleShot(True)
    timer.setInterval(long_press_ms)

    def _show_tooltip() -> None:
        bubble.setText(text)
        bubble.setProperty("owner", button)
        bubble.adjustSize()
        bubble.show_near(button, main_window)

    timer.timeout.connect(_show_tooltip)

    event_filter = _ButtonEventFilter(button, text, bubble, main_window, timer)
    button.installEventFilter(event_filter)

    # Keep timer alive (event_filter is already parented to button)
    button._tooltip_timer = timer
    button._tooltip_filter = event_filter
