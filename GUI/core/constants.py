"""
Constants for page indices and button styles used throughout the GUI.
"""


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
    BATTLE = 13
    PERFORMANCE = 14
    POWER_INSTRUCTIONS = 15
    POWER_PUNCH = 16
    POWER_RESULT = 17
    STAMINA_INSTRUCTIONS = 18
    REACTION_INSTRUCTIONS = 19
    REACTION_TEST = 20
    REACTION_RESULT = 21
    OTHERS = 22
    LOGIN = 23
    USER_MANAGEMENT = 24
    USER_COMBO_PROGRESS = 25
    USER_PROGRESS_OVERVIEW = 26
    COMBO_RESULTS = 27
    COMBO_LLM_CHAT = 28
    STAMINA_TEST = 29
    STAMINA_RESULT = 30
    STAMINA_HISTORY = 31
    PERFORMANCE_HISTORY = 32
    BATTLE_STYLE_DESC = 33


class ButtonStyle:
    """Centralized button style management."""

    @staticmethod
    def _create_style(font_size, padding, min_width, min_height, bg_color, hover_color, pressed_color, border_radius=8):
        """Internal helper to generate button stylesheet."""
        return f"""
            QPushButton {{
                font-size: {font_size}px;
                padding: {padding}px;
                min-width: {min_width}px;
                min-height: {min_height}px;
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: {border_radius}px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """

    # Green buttons (Primary actions)
    PRIMARY_LARGE = _create_style.__func__(
        font_size=28, padding=40, min_width=500, min_height=50,
        bg_color="#4CAF50", hover_color="#45a049", pressed_color="#3d8b40",
    )

    PRIMARY_MEDIUM = _create_style.__func__(
        font_size=20, padding=25, min_width=250, min_height=40,
        bg_color="#4CAF50", hover_color="#45a049", pressed_color="#3d8b40",
    )

    PRIMARY_WIDE = _create_style.__func__(
        font_size=20, padding=40, min_width=500, min_height=20,
        bg_color="#4CAF50", hover_color="#45a049", pressed_color="#3d8b40",
    )

    # Red buttons (Back/Cancel)
    BACK_LARGE = _create_style.__func__(
        font_size=20, padding=25, min_width=500, min_height=40,
        bg_color="#f44336", hover_color="#da190b", pressed_color="#c41504",
    )

    BACK_MEDIUM = _create_style.__func__(
        font_size=20, padding=25, min_width=250, min_height=40,
        bg_color="#f44336", hover_color="#da190b", pressed_color="#c41504",
    )

    BACK_SMALL = _create_style.__func__(
        font_size=20, padding=25, min_width=200, min_height=40,
        bg_color="#f44336", hover_color="#da190b", pressed_color="#c41504",
    )

    # Blue buttons (Info/Secondary)
    INFO_SMALL = _create_style.__func__(
        font_size=20, padding=12, min_width=240, min_height=50,
        bg_color="#2196F3", hover_color="#1976D2", pressed_color="#155A8A",
    )

    INFO_MEDIUM = _create_style.__func__(
        font_size=20, padding=12, min_width=240, min_height=40,
        bg_color="#2196F3", hover_color="#1976D2", pressed_color="#155A8A",
    )

    # Special sizes
    ROUND_SELECTION = _create_style.__func__(
        font_size=20, padding=8, min_width=80, min_height=90,
        bg_color="#1976D2", hover_color="#1565C0", pressed_color="#0D47A1", border_radius=6,
    )

    SPEED_SELECTION = _create_style.__func__(
        font_size=40, padding=8, min_width=80, min_height=300,
        bg_color="#1976D2", hover_color="#1565C0", pressed_color="#0D47A1", border_radius=6,
    )

    TIME_SELECTION = _create_style.__func__(
        font_size=18, padding=8, min_width=0, min_height=100,
        bg_color="#1976D2", hover_color="#1565C0", pressed_color="#0D47A1", border_radius=6,
    )

    HOME_LARGE = _create_style.__func__(
        font_size=28, padding=30, min_width=500, min_height=30,
        bg_color="#4CAF50", hover_color="#45a049", pressed_color="#3d8b40",
    )
    TRACK_MEDIUM = _create_style.__func__(
        font_size=15, padding=10, min_width=250, min_height=15,
        bg_color="#f44336", hover_color="#da190b", pressed_color="#c41504",
    )
