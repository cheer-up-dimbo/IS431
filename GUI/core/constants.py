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
    BORDER_LIGHT  = "#475569"   # Elevated / hover border

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

    # Radius tokens
    RADIUS_SM   = "8px"
    RADIUS_MD   = "12px"
    RADIUS_LG   = "16px"
    RADIUS_PILL = "22px"

    # Card border helpers
    CARD_BORDER          = "1px solid #334155"
    CARD_BORDER_ELEVATED = "1px solid #475569"
    CARD_BORDER_ACCENT   = "2px solid #F97316"

    # Spacing scale (int px, use in setSpacing / setContentsMargins)
    SPACE_XS  = 4
    SPACE_SM  = 8
    SPACE_MD  = 16
    SPACE_LG  = 24
    SPACE_XL  = 32
    SPACE_2XL = 48

    # Font sizes (int px)
    FONT_XS   = 11
    FONT_SM   = 13
    FONT_BASE = 15
    FONT_MD   = 18
    FONT_LG   = 24
    FONT_XL   = 32
    FONT_2XL  = 48
    FONT_HERO = 64


# ============================================================================
# Global Application Stylesheet (apply once to QApplication or MainWindow)
# ============================================================================

GLOBAL_QSS = f"""
    /* ── Base ──────────────────────────────────────────────────────────────── */
    QWidget {{
        background-color: {DS.BG_DARK};
        color: {DS.TEXT_PRIMARY};
        font-family: "Barlow Condensed", "Arial Narrow", "Liberation Sans Narrow",
                     "DejaVu Sans Condensed", Arial, sans-serif;
        font-size: 15px;
    }}
    QLabel {{
        background-color: transparent;
        color: {DS.TEXT_PRIMARY};
    }}

    /* ── Named label roles ──────────────────────────────────────────────────── */
    QLabel#pageTitle {{
        font-size: 32px;
        font-weight: 700;
        color: {DS.PRIMARY};
        letter-spacing: 1px;
    }}
    QLabel#sectionHeader {{
        font-size: 11px;
        font-weight: 600;
        color: {DS.TEXT_MUTED};
        letter-spacing: 2px;
    }}
    QLabel#metricValue {{
        font-size: 64px;
        font-weight: 800;
        color: {DS.TEXT_PRIMARY};
    }}
    QLabel#metricLabel {{
        font-size: 13px;
        color: {DS.TEXT_SECONDARY};
        letter-spacing: 1px;
    }}
    QLabel#subtitleLabel {{
        font-size: 15px;
        color: {DS.TEXT_SECONDARY};
    }}
    QLabel#heroText {{
        font-size: 64px;
        font-weight: 800;
        color: {DS.TEXT_PRIMARY};
        letter-spacing: 2px;
    }}
    QLabel#countdownHero {{
        font-size: 120px;
        font-weight: 900;
        color: {DS.PRIMARY};
    }}
    QLabel#badgeLabel {{
        font-size: 11px;
        font-weight: 700;
        color: {DS.PRIMARY_TEXT};
        background-color: {DS.PRIMARY};
        border-radius: 8px;
        padding: 2px 8px;
    }}

    /* ── Card QFrame — setProperty("class","card") ──────────────────────── */
    QFrame[class="card"] {{
        background-color: {DS.BG_SURFACE};
        border: 1px solid {DS.BORDER};
        border-radius: 12px;
    }}
    QFrame[class="card--accent"] {{
        background-color: {DS.BG_SURFACE};
        border: 2px solid {DS.PRIMARY};
        border-radius: 12px;
    }}
    QFrame[class="card--elevated"] {{
        background-color: {DS.BG_ELEVATED};
        border: 1px solid {DS.BORDER_LIGHT};
        border-radius: 12px;
    }}
    QFrame[class="header-bar"] {{
        background-color: {DS.BG_SURFACE};
        border-bottom: 1px solid {DS.BORDER};
        border-radius: 0px;
    }}
    QFrame[class="footer-bar"] {{
        background-color: {DS.BG_SURFACE};
        border-top: 1px solid {DS.BORDER};
        border-radius: 0px;
    }}

    /* ── Inputs ─────────────────────────────────────────────────────────────── */
    QLineEdit {{
        background-color: {DS.BG_SURFACE};
        border: 1px solid {DS.BORDER};
        border-radius: 8px;
        padding: 10px 14px;
        color: {DS.TEXT_PRIMARY};
        font-size: 15px;
        selection-background-color: {DS.PRIMARY};
    }}
    QLineEdit:focus {{
        border: 2px solid {DS.PRIMARY};
    }}

    /* ── Pill buttons (objectName="pillBtn") ────────────────────────────────── */
    QPushButton#pillBtn {{
        background-color: {DS.BG_SURFACE};
        border: 1px solid {DS.BORDER};
        border-radius: 22px;
        min-width: 80px;
        min-height: 44px;
        padding: 0 20px;
        font-size: 15px;
        font-weight: 600;
        color: {DS.TEXT_SECONDARY};
    }}
    QPushButton#pillBtn:hover {{
        background-color: {DS.BG_ELEVATED};
        border-color: {DS.BORDER_LIGHT};
        color: {DS.TEXT_PRIMARY};
    }}
    QPushButton#pillBtn:checked {{
        background-color: {DS.PRIMARY};
        border-color: {DS.PRIMARY};
        color: {DS.PRIMARY_TEXT};
        font-weight: 700;
    }}
    QPushButton#pillBtn:focus {{
        border: 2px solid {DS.PRIMARY};
        color: {DS.TEXT_PRIMARY};
    }}

    /* ── Table ──────────────────────────────────────────────────────────────── */
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
        background-color: {DS.PRIMARY};
        color: {DS.PRIMARY_TEXT};
    }}
    QHeaderView::section {{
        background-color: {DS.BG_ELEVATED};
        color: {DS.TEXT_SECONDARY};
        padding: 8px 12px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        border: none;
        border-bottom: 1px solid {DS.BORDER};
    }}
    QTableCornerButton::section {{
        background-color: {DS.BG_ELEVATED};
        border: none;
    }}

    /* ── ScrollArea / ScrollBar ─────────────────────────────────────────────── */
    QScrollArea {{
        background-color: transparent;
        border: none;
    }}
    QScrollBar:vertical {{
        background-color: {DS.BG_DARK};
        width: 6px;
        margin: 0;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical {{
        background-color: {DS.BORDER};
        border-radius: 3px;
        min-height: 20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: {DS.PRIMARY};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QScrollBar:horizontal {{
        background-color: {DS.BG_DARK};
        height: 6px;
        border-radius: 3px;
    }}
    QScrollBar::handle:horizontal {{
        background-color: {DS.BORDER};
        border-radius: 3px;
        min-width: 20px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background-color: {DS.PRIMARY};
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
    }}

    /* ── ComboBox ───────────────────────────────────────────────────────────── */
    QComboBox {{
        background-color: {DS.BG_SURFACE};
        border: 1px solid {DS.BORDER};
        border-radius: 8px;
        padding: 8px 12px;
        color: {DS.TEXT_PRIMARY};
        font-size: 15px;
        min-height: 44px;
    }}
    QComboBox:focus {{
        border: 2px solid {DS.PRIMARY};
    }}
    QComboBox::drop-down {{
        border: none;
        padding-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {DS.BG_SURFACE};
        color: {DS.TEXT_PRIMARY};
        selection-background-color: {DS.PRIMARY};
        selection-color: {DS.PRIMARY_TEXT};
        border: 1px solid {DS.BORDER};
        border-radius: 4px;
        outline: 0;
    }}

    /* ── TextEdit ───────────────────────────────────────────────────────────── */
    QTextEdit {{
        background-color: {DS.BG_SURFACE};
        border: 1px solid {DS.BORDER};
        border-radius: 8px;
        color: {DS.TEXT_PRIMARY};
        font-size: 14px;
        padding: 8px;
        selection-background-color: {DS.PRIMARY};
    }}

    /* ── Frame dividers ─────────────────────────────────────────────────────── */
    QFrame[frameShape="4"] {{
        background-color: {DS.BORDER};
        max-width: 1px;
    }}
    QFrame[frameShape="5"] {{
        background-color: {DS.BORDER};
        max-height: 1px;
    }}

    /* ── MessageBox ─────────────────────────────────────────────────────────── */
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

    # ── Nav card — large card-style navigation button ────────────────────────
    NAV_CARD = f"""
        QPushButton {{
            background-color: {DS.BG_SURFACE};
            border: 1px solid {DS.BORDER};
            border-radius: 12px;
            padding: 20px 24px;
            font-size: 17px;
            font-weight: 600;
            color: {DS.TEXT_PRIMARY};
            min-height: 120px;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: {DS.BG_ELEVATED};
            border: 1px solid {DS.BORDER_LIGHT};
            border-left: 3px solid {DS.PRIMARY};
        }}
        QPushButton:pressed {{
            background-color: #1a2a3a;
        }}
        QPushButton:focus {{
            border: 2px solid {DS.PRIMARY};
        }}
    """

    # ── Pill — compact rounded selector button ───────────────────────────────
    PILL = f"""
        QPushButton {{
            background-color: {DS.BG_SURFACE};
            border: 1px solid {DS.BORDER};
            border-radius: 22px;
            min-width: 80px;
            min-height: 44px;
            padding: 0 20px;
            font-size: 15px;
            font-weight: 600;
            color: {DS.TEXT_SECONDARY};
        }}
        QPushButton:hover {{
            background-color: {DS.BG_ELEVATED};
            border-color: {DS.BORDER_LIGHT};
            color: {DS.TEXT_PRIMARY};
        }}
        QPushButton:focus {{
            border: 2px solid {DS.PRIMARY};
            color: {DS.TEXT_PRIMARY};
        }}
    """

    PILL_SELECTED = f"""
        QPushButton {{
            background-color: {DS.PRIMARY};
            border: 1px solid {DS.PRIMARY};
            border-radius: 22px;
            min-width: 80px;
            min-height: 44px;
            padding: 0 20px;
            font-size: 15px;
            font-weight: 700;
            color: {DS.PRIMARY_TEXT};
        }}
        QPushButton:hover {{
            background-color: {DS.PRIMARY_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {DS.PRIMARY_PRESS};
        }}
        QPushButton:focus {{
            border: 2px solid {DS.TEXT_PRIMARY};
        }}
    """

    # ── Session action — large touch-friendly CTA ────────────────────────────
    SESSION_ACTION = f"""
        QPushButton {{
            background-color: {DS.PRIMARY};
            border: none;
            border-radius: 16px;
            min-height: 72px;
            min-width: 200px;
            font-size: 20px;
            font-weight: 800;
            color: {DS.PRIMARY_TEXT};
            letter-spacing: 1px;
        }}
        QPushButton:hover {{
            background-color: {DS.PRIMARY_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {DS.PRIMARY_PRESS};
        }}
        QPushButton:disabled {{
            background-color: {DS.BORDER};
            color: {DS.TEXT_MUTED};
        }}
        QPushButton:focus {{
            border: 2px solid {DS.TEXT_PRIMARY};
        }}
    """

    SESSION_ACTION_DANGER = f"""
        QPushButton {{
            background-color: {DS.DANGER};
            border: none;
            border-radius: 16px;
            min-height: 72px;
            min-width: 200px;
            font-size: 20px;
            font-weight: 800;
            color: {DS.TEXT_PRIMARY};
            letter-spacing: 1px;
        }}
        QPushButton:hover {{
            background-color: {DS.DANGER_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {DS.DANGER_PRESS};
        }}
        QPushButton:focus {{
            border: 2px solid {DS.TEXT_PRIMARY};
        }}
    """

    # ── Ghost — flat text-only button ───────────────────────────────────────
    GHOST = f"""
        QPushButton {{
            background-color: transparent;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 13px;
            color: {DS.TEXT_MUTED};
        }}
        QPushButton:hover {{
            color: {DS.TEXT_PRIMARY};
            background-color: {DS.BG_ELEVATED};
        }}
        QPushButton:pressed {{
            color: {DS.PRIMARY};
        }}
    """

    @staticmethod
    def preset_card_colored(accent_hex: str) -> str:
        """Generate a preset card button style with a colored top accent bar."""
        return f"""
            QPushButton {{
                background-color: {DS.BG_SURFACE};
                border: 1px solid {DS.BORDER};
                border-top: 3px solid {accent_hex};
                border-radius: 12px;
                padding: 14px 12px;
                font-size: 13px;
                font-weight: 600;
                color: {DS.TEXT_PRIMARY};
                min-height: 90px;
                min-width: 130px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {DS.BG_ELEVATED};
                border-top: 3px solid {accent_hex};
                border-left: 1px solid {DS.BORDER_LIGHT};
                border-right: 1px solid {DS.BORDER_LIGHT};
                border-bottom: 1px solid {DS.BORDER_LIGHT};
            }}
            QPushButton:pressed {{
                background-color: #1a2a3a;
            }}
            QPushButton:focus {{
                border: 2px solid {accent_hex};
                border-top: 3px solid {accent_hex};
            }}
        """
