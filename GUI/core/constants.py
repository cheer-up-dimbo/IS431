"""
Constants for page indices, design system tokens, and button styles.
"""


# ============================================================================
# Design System — BoxBunny Dark Theme
# ============================================================================

class DS:
    """Design system color tokens for the BoxBunny dark theme."""

    # Backgrounds
    BG_DARK       = "#0F172A"   # Main background (deep navy / OLED-friendly)
    BG_SURFACE    = "#1E293B"   # Card / panel surface
    BG_ELEVATED   = "#263347"   # Hover / elevated surface

    # Borders
    BORDER        = "#334155"   # Default border / divider

    # Primary — Energy orange (main actions, CTAs)
    PRIMARY       = "#F97316"
    PRIMARY_HOVER = "#EA6C0A"
    PRIMARY_PRESS = "#D96209"
    PRIMARY_TEXT  = "#0F172A"   # Text ON primary buttons

    # Success — Green (proceed / confirm / navigate forward)
    SUCCESS       = "#22C55E"
    SUCCESS_HOVER = "#16A34A"
    SUCCESS_PRESS = "#15803D"

    # Info — Blue (secondary / informational)
    INFO          = "#3B82F6"
    INFO_HOVER    = "#2563EB"
    INFO_PRESS    = "#1D4ED8"

    # Danger — Red (back / cancel / destructive)
    DANGER        = "#EF4444"
    DANGER_HOVER  = "#DC2626"
    DANGER_PRESS  = "#B91C1C"

    # Text
    TEXT_PRIMARY   = "#F8FAFC"
    TEXT_SECONDARY = "#94A3B8"
    TEXT_MUTED     = "#64748B"

    # Semantic aliases
    ACCENT  = "#F97316"
    WARNING = "#FFC107"


# ============================================================================
# Global Application Stylesheet (apply once to QApplication or MainWindow)
# ============================================================================

GLOBAL_QSS = f"""
    QWidget {{
        background-color: {DS.BG_DARK};
        color: {DS.TEXT_PRIMARY};
        font-family: "Segoe UI", Arial, sans-serif;
    }}
    QLabel {{
        background-color: transparent;
        color: {DS.TEXT_PRIMARY};
    }}

    QLineEdit {{
        background-color: {DS.BG_SURFACE};
        border: 2px solid {DS.BORDER};
        border-radius: 8px;
        padding: 10px 12px;
        color: {DS.TEXT_PRIMARY};
        font-size: 16px;
        selection-background-color: {DS.PRIMARY};
    }}
    QLineEdit:focus {{
        border-color: {DS.PRIMARY};
    }}

    QTableWidget {{
        background-color: {DS.BG_SURFACE};
        color: {DS.TEXT_PRIMARY};
        border: 1px solid {DS.BORDER};
        border-radius: 8px;
        gridline-color: {DS.BORDER};
        outline: 0;
    }}
    QTableWidget::item {{
        padding: 10px;
        color: {DS.TEXT_PRIMARY};
        background-color: {DS.BG_SURFACE};
    }}
    QTableWidget::item:selected {{
        background-color: {DS.BG_ELEVATED};
        color: {DS.TEXT_PRIMARY};
    }}
    QHeaderView::section {{
        background-color: {DS.PRIMARY};
        color: {DS.PRIMARY_TEXT};
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
        border: none;
    }}
    QTableCornerButton::section {{
        background-color: {DS.PRIMARY};
        border: none;
    }}

    QScrollArea {{
        background-color: transparent;
        border: none;
    }}
    QScrollBar:vertical {{
        background-color: {DS.BG_SURFACE};
        width: 8px;
        margin: 0;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background-color: {DS.BORDER};
        border-radius: 4px;
        min-height: 20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: {DS.PRIMARY};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QScrollBar:horizontal {{
        background-color: {DS.BG_SURFACE};
        height: 8px;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal {{
        background-color: {DS.BORDER};
        border-radius: 4px;
        min-width: 20px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background-color: {DS.PRIMARY};
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
    }}

    QComboBox {{
        background-color: {DS.BG_SURFACE};
        border: 2px solid {DS.BORDER};
        border-radius: 8px;
        padding: 8px 12px;
        color: {DS.TEXT_PRIMARY};
        font-size: 14px;
        min-height: 40px;
    }}
    QComboBox:focus {{
        border-color: {DS.PRIMARY};
    }}
    QComboBox::drop-down {{
        border: none;
        padding-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {DS.BG_SURFACE};
        color: {DS.TEXT_PRIMARY};
        selection-background-color: {DS.BG_ELEVATED};
        border: 1px solid {DS.BORDER};
        border-radius: 4px;
        outline: 0;
    }}

    QTextEdit {{
        background-color: {DS.BG_SURFACE};
        border: 1px solid {DS.BORDER};
        border-radius: 8px;
        color: {DS.TEXT_PRIMARY};
        font-size: 14px;
        padding: 8px;
        selection-background-color: {DS.PRIMARY};
    }}

    QFrame[frameShape="4"] {{
        background-color: {DS.BORDER};
        max-width: 1px;
    }}
    QFrame[frameShape="5"] {{
        background-color: {DS.BORDER};
        max-height: 1px;
    }}

    QMessageBox {{
        background-color: {DS.BG_SURFACE};
        color: {DS.TEXT_PRIMARY};
    }}
    QMessageBox QLabel {{
        color: {DS.TEXT_PRIMARY};
    }}
    QMessageBox QPushButton {{
        background-color: {DS.BG_ELEVATED};
        color: {DS.TEXT_PRIMARY};
        border: 1px solid {DS.BORDER};
        border-radius: 6px;
        padding: 6px 16px;
        min-width: 80px;
        font-size: 13px;
    }}
    QMessageBox QPushButton:hover {{
        background-color: {DS.PRIMARY};
        color: {DS.PRIMARY_TEXT};
        border-color: {DS.PRIMARY};
    }}
"""


# ============================================================================
# Page Index
# ============================================================================

class PageIndex:
    """Page enumeration constants for QStackedWidget page navigation."""
    HOMEPAGE = 0
    TRAINING = 1
    TECHNIQUES = 2
    PUNCH_COMBINATIONS = 3
    BASIC_PARAMETERS = 4
    ROUND_SELECTION = 5
    SPEED_SELECTION = 6
    TIME_SELECTION = 7
    REST_SELECTION = 8
    COUNTDOWN = 9
    TRAINING_SESSION = 10
    SELF_SELECT_SEQUENCE = 11
    SPAR = 12
    PERFORMANCE = 13
    POWER_INSTRUCTIONS = 14
    POWER_PUNCH = 15
    POWER_RESULT = 16
    STAMINA_INSTRUCTIONS = 17
    REACTION_INSTRUCTIONS = 18
    REACTION_TEST = 19
    REACTION_RESULT = 20
    OTHERS = 21
    LOGIN = 22
    USER_MANAGEMENT = 23
    USER_COMBO_PROGRESS = 24
    USER_PROGRESS_OVERVIEW = 25
    COMBO_RESULTS = 26
    COMBO_LLM_CHAT = 27
    STAMINA_TEST = 28
    STAMINA_RESULT = 29
    STAMINA_HISTORY = 30
    PERFORMANCE_HISTORY = 31
    BATTLE_STYLE_DESC = 32
    SPAR_STYLE_SELECT = 33
    SPAR_ROUND_CONFIG  = 34
    SPAR_COUNTDOWN     = 35
    SPAR_SESSION       = 36
    SPAR_REST          = 37
    SPAR_PROCESSING    = 38
    SPAR_RESULT        = 39


# ============================================================================
# Button Styles — dark theme
# ============================================================================

class ButtonStyle:
    """Centralized button style management."""

    @staticmethod
    def _create_style(font_size, padding, min_width, min_height,
                      bg_color, hover_color, pressed_color,
                      border_radius=10, text_color="#FFFFFF"):
        """Internal helper to generate a dark-theme button stylesheet."""
        return f"""
            QPushButton {{
                font-size: {font_size}px;
                padding: {padding}px;
                min-width: {min_width}px;
                min-height: {min_height}px;
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-radius: {border_radius}px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
            QPushButton:disabled {{
                background-color: {DS.BG_ELEVATED};
                color: {DS.TEXT_MUTED};
                border: 1px solid {DS.BORDER};
            }}
        """

    # ── Primary (energy orange) ──────────────────────────────────────────────
    PRIMARY_LARGE = _create_style.__func__(
        font_size=26, padding=36, min_width=480, min_height=56,
        bg_color=DS.PRIMARY, hover_color=DS.PRIMARY_HOVER,
        pressed_color=DS.PRIMARY_PRESS, text_color=DS.PRIMARY_TEXT,
    )
    PRIMARY_MEDIUM = _create_style.__func__(
        font_size=20, padding=22, min_width=240, min_height=48,
        bg_color=DS.PRIMARY, hover_color=DS.PRIMARY_HOVER,
        pressed_color=DS.PRIMARY_PRESS, text_color=DS.PRIMARY_TEXT,
    )
    PRIMARY_WIDE = _create_style.__func__(
        font_size=20, padding=36, min_width=480, min_height=28,
        bg_color=DS.PRIMARY, hover_color=DS.PRIMARY_HOVER,
        pressed_color=DS.PRIMARY_PRESS, text_color=DS.PRIMARY_TEXT,
    )

    # ── Home / nav large (orange) ────────────────────────────────────────────
    HOME_LARGE = _create_style.__func__(
        font_size=24, padding=28, min_width=480, min_height=48,
        bg_color=DS.PRIMARY, hover_color=DS.PRIMARY_HOVER,
        pressed_color=DS.PRIMARY_PRESS, text_color=DS.PRIMARY_TEXT,
    )

    # ── Danger / Back (red) ──────────────────────────────────────────────────
    BACK_LARGE = _create_style.__func__(
        font_size=20, padding=22, min_width=480, min_height=48,
        bg_color=DS.DANGER, hover_color=DS.DANGER_HOVER,
        pressed_color=DS.DANGER_PRESS,
    )
    BACK_MEDIUM = _create_style.__func__(
        font_size=20, padding=22, min_width=240, min_height=48,
        bg_color=DS.DANGER, hover_color=DS.DANGER_HOVER,
        pressed_color=DS.DANGER_PRESS,
    )
    BACK_SMALL = _create_style.__func__(
        font_size=20, padding=22, min_width=190, min_height=48,
        bg_color=DS.DANGER, hover_color=DS.DANGER_HOVER,
        pressed_color=DS.DANGER_PRESS,
    )

    # ── Info / secondary (blue) ──────────────────────────────────────────────
    INFO_MEDIUM = _create_style.__func__(
        font_size=20, padding=12, min_width=240, min_height=48,
        bg_color=DS.INFO, hover_color=DS.INFO_HOVER,
        pressed_color=DS.INFO_PRESS,
    )
    INFO_SMALL = _create_style.__func__(
        font_size=18, padding=10, min_width=200, min_height=48,
        bg_color=DS.INFO, hover_color=DS.INFO_HOVER,
        pressed_color=DS.INFO_PRESS,
    )

    # ── Track (danger/red compact) ───────────────────────────────────────────
    TRACK_MEDIUM = _create_style.__func__(
        font_size=15, padding=10, min_width=240, min_height=22,
        bg_color=DS.DANGER, hover_color=DS.DANGER_HOVER,
        pressed_color=DS.DANGER_PRESS,
    )

    # ── Parameter selection (dark card — neutral) ────────────────────────────
    ROUND_SELECTION = _create_style.__func__(
        font_size=20, padding=8, min_width=80, min_height=90,
        bg_color=DS.BG_SURFACE, hover_color=DS.BG_ELEVATED,
        pressed_color=DS.PRIMARY, border_radius=8,
        text_color=DS.TEXT_PRIMARY,
    )
    SPEED_SELECTION = _create_style.__func__(
        font_size=36, padding=8, min_width=80, min_height=280,
        bg_color=DS.BG_SURFACE, hover_color=DS.BG_ELEVATED,
        pressed_color=DS.PRIMARY, border_radius=8,
        text_color=DS.TEXT_PRIMARY,
    )
    TIME_SELECTION = _create_style.__func__(
        font_size=18, padding=8, min_width=0, min_height=100,
        bg_color=DS.BG_SURFACE, hover_color=DS.BG_ELEVATED,
        pressed_color=DS.PRIMARY, border_radius=8,
        text_color=DS.TEXT_PRIMARY,
    )
