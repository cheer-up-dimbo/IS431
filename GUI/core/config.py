"""
Core configuration data classes for boxing training application.

Defines the main configuration objects used throughout the app:
- TrainingConfig: All training session parameters
- TechCorrConfig: Technique Correction mode configuration
- AppState: Central application state manager
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List


@dataclass
class TrainingConfig:
    """Configuration for boxing training sessions.
    
    This dataclass stores all training parameters including rounds, timing,
    speed, difficulty level, battle style, and custom punch sequences.
    
    Attributes:
        rounds: Number of training rounds (1-12, default: 3)
        time_minutes: Work time in minutes (default: 3)
        time_seconds: Work time in seconds (0-59, default: 0)
        rest_minutes: Rest time in minutes (default: 1)
        rest_seconds: Rest time in seconds (0-59, default: 0)
        speed: Training speed percentage.
            Valid values: "25%", "50%", "75%", "100%" (default: "100%")
        difficulty: Training difficulty mode.
            Valid values: "Beginner", "Intermediate", "Advanced", "Self-Select", "Battle", None
        battle_style: Boxing style for Battle mode.
            Valid values: "Pressure Fighter", "Counter Puncher", "Balanced Boxer", 
                         "Out Boxer", "Random", None
        custom_sequences: List of custom punch sequences for Self-Select mode.
            Example: ["1-2-3", "Cross-Hook", "Jab-Cross-Uppercut"]
    
    Example:
        >>> config = TrainingConfig()
        >>> config.rounds = 5
        >>> config.set_time_from_str("3:30")
        >>> config.difficulty = "Advanced"
        >>> config.speed = "75%"
        >>> print(config.to_dict())
    """
    rounds: int = 12
    time_minutes: int = 3
    time_seconds: int = 0
    rest_minutes: int = 1
    rest_seconds: int = 0
    speed: str = "100%"
    difficulty: Optional[str] = None
    battle_style: Optional[str] = None
    custom_sequences: List[str] = field(default_factory=list)
    
    def get_time_str(self) -> str:
        """Format time as 'M:SS'.
        
        Returns:
            Time formatted as string (e.g., "3:00", "2:30")
            
        Example:
            >>> config.time_minutes = 3
            >>> config.time_seconds = 30
            >>> config.get_time_str()
            '3:30'
        """
        return f"{self.time_minutes}:{self.time_seconds:02d}"
    
    def set_time_from_str(self, time_str: str) -> None:
        """Parse time string in format 'M:SS' or 'MM:SS'.
        
        Accepts common time formats like "30sec", "1min", "3:00", etc.
        Silently ignores invalid formats.
        
        Args:
            time_str: Time string to parse (e.g., "3:30", "2:00")
            
        Example:
            >>> config.set_time_from_str("3:30")
            >>> config.time_minutes  # 3
            >>> config.time_seconds  # 30
        """
        try:
            parts = time_str.split(':')
            if len(parts) == 2:
                self.time_minutes = int(parts[0])
                self.time_seconds = int(parts[1])
        except (ValueError, IndexError):
            pass
    
    def get_rest_str(self) -> str:
        """Format rest time as 'M:SS'.
        
        Returns:
            Rest time formatted as string (e.g., "1:00", "0:30")
            
        Example:
            >>> config.rest_minutes = 1
            >>> config.rest_seconds = 30
            >>> config.get_rest_str()
            '1:30'
        """
        return f"{self.rest_minutes}:{self.rest_seconds:02d}"
    
    def set_rest_from_str(self, rest_str: str) -> None:
        """Parse rest time string in format 'M:SS' or 'MM:SS'.
        
        Accepts common time formats like "10sec", "30sec", "1:00", etc.
        Silently ignores invalid formats.
        
        Args:
            rest_str: Rest time string to parse (e.g., "1:30", "0:45")
            
        Example:
            >>> config.set_rest_from_str("1:30")
            >>> config.rest_minutes  # 1
            >>> config.rest_seconds  # 30
        """
        try:
            parts = rest_str.split(':')
            if len(parts) == 2:
                self.rest_minutes = int(parts[0])
                self.rest_seconds = int(parts[1])
        except (ValueError, IndexError):
            pass
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization.
        
        Returns:
            Dictionary containing all config fields
            
        Example:
            >>> config.to_dict()
            {'rounds': 3, 'time_minutes': 3, 'time_seconds': 0, ...}
        """
        return asdict(self)
    
    def reset(self) -> None:
        """Reset to default values.
        
        Resets all fields to their initial defaults:
        - rounds: 3
        - time: 3:00
        - rest: 1:00
        - speed: "100%"
        - difficulty, battle_style, custom_sequences: cleared
        
        Example:
            >>> config.rounds = 10
            >>> config.reset()
            >>> config.rounds  # 3
        """
        self.rounds = 3
        self.time_minutes = 3
        self.time_seconds = 0
        self.rest_minutes = 1
        self.rest_seconds = 0
        self.speed = "100%"


@dataclass
class TechCorrConfig:
    """Persistent configuration for Technique Correction mode."""
    difficulty: str
    rounds: int
    round_seconds: int
    rest_seconds: int
    speed: str


class AppState:
    """Manages application state and training configuration.
    
    Central state manager for the boxing training app. Holds a TrainingConfig
    instance and provides methods for updating configuration values. Pages should
    use this to share state instead of directly accessing other pages' attributes.
    
    Attributes:
        config: TrainingConfig instance holding all training parameters
        previous_page: PageIndex for navigation (which page to return to on back)
        time_label: Display label for time (e.g., "3min", "2min30sec")
        rest_label: Display label for rest (e.g., "1min", "30sec")
    
    Common Usage Patterns:
        
        # In MainWindow.__init__:
        >>> self.app_state = AppState(initial_page=PageIndex.HOMEPAGE)
        >>> self.basic_page = BasicParametersPage(stacked_widget, self.app_state)
        
        # In selection pages (RoundSelectionPage, SpeedSelectionPage, etc.):
        >>> def select_value(self, value):
        ...     self.app_state.update_rounds(value)  # or update_speed, update_time, etc.
        ...     basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
        ...     basic_page.update_button_displays()
        ...     self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS)
        
        # In difficulty/mode pages:
        >>> self.app_state.update_difficulty("Advanced")
        >>> self.app_state.previous_page = PageIndex.PUNCH_COMBINATIONS
        
        # In battle style page:
        >>> self.app_state.update_battle_style("Pressure Fighter")
        >>> self.app_state.update_difficulty("Battle")
        
        # Reading config values:
        >>> config = self.app_state.get_config()
        >>> rounds = config.rounds
        >>> difficulty = config.difficulty
        >>> sequences = config.custom_sequences
    
    Example:
        >>> app_state = AppState()
        >>> app_state.update_rounds(5)
        >>> app_state.update_time("3:30")
        >>> app_state.update_difficulty("Advanced")
        >>> config = app_state.get_config()
        >>> print(config.rounds)  # 5
        >>> print(config.get_time_str())  # "3:30"
    """
    
    def __init__(self, initial_page: int = 0):
        """Initialize AppState with a TrainingConfig instance.
        
        Args:
            initial_page: Initial page index for navigation tracking (default: 0).
                         Use PageIndex constants (e.g., PageIndex.HOMEPAGE)
        """
        self.config = TrainingConfig()
        self.previous_page = initial_page
        self.time_label: Optional[str] = "3min"
        self.rest_label: Optional[str] = "1min"
        # Technique Correction specific persistent config
        self.tech_corr_config: Optional[TechCorrConfig] = None
        # AI Chat setting
        self.ai_chat_enabled: bool = True

    def set_tech_corr_config(self, cfg: "TechCorrConfig") -> None:
        """Persist Technique Correction configuration."""
        self.tech_corr_config = cfg
    
    def update_rounds(self, rounds: int) -> None:
        """Update the number of rounds.
        
        Args:
            rounds: Number of training rounds (must be > 0)
            
        Example:
            >>> app_state.update_rounds(5)
        """
        if rounds > 0:
            self.config.rounds = rounds
    
    def update_time(self, time_str: str) -> None:
        """Update time from a time format string.
        
        Stores both the display label and parses into minutes/seconds.
        Accepts formats like "30sec", "1min", "3min", "2min30sec".
        
        Args:
            time_str: Time string (e.g., "3min", "2min30sec")
            
        Example:
            >>> app_state.update_time("3min")
            >>> app_state.update_time("2min30sec")
        """
        self.time_label = time_str
        self.config.set_time_from_str(time_str)
    
    def update_rest(self, rest_str: str) -> None:
        """Update rest time from a time format string.
        
        Stores both the display label and parses into minutes/seconds.
        Accepts formats like "10sec", "30sec", "1min".
        
        Args:
            rest_str: Rest time string (e.g., "1min", "30sec")
            
        Example:
            >>> app_state.update_rest("1min")
            >>> app_state.update_rest("30sec")
        """
        self.rest_label = rest_str
        self.config.set_rest_from_str(rest_str)
    
    def update_speed(self, speed: str) -> None:
        """Update the speed setting.
        
        Args:
            speed: Speed percentage. Valid: "25%", "50%", "75%", "100%"
            
        Example:
            >>> app_state.update_speed("75%")
        """
        self.config.speed = speed
    
    def update_difficulty(self, difficulty: str) -> None:
        """Update the difficulty setting.
        
        Args:
            difficulty: Difficulty mode. 
                       Valid: "Beginner", "Intermediate", "Advanced", 
                              "Self-Select", "Battle"
                              
        Example:
            >>> app_state.update_difficulty("Advanced")
            >>> app_state.update_difficulty("Battle")
        """
        self.config.difficulty = difficulty
    
    def update_battle_style(self, style: str) -> None:
        """Update the battle style.
        
        Args:
            style: Boxing style for Battle mode.
                  Valid: "Pressure Fighter", "Counter Puncher", 
                         "Balanced Boxer", "Out Boxer", "Random"
                         
        Example:
            >>> app_state.update_battle_style("Pressure Fighter")
            >>> app_state.update_difficulty("Battle")  # Usually set together
        """
        self.config.battle_style = style
    
    def set_sequences(self, sequences: List[str]) -> None:
        """Set the list of custom sequences.
        
        Replaces the entire sequence list. Used in Self-Select mode.
        
        Args:
            sequences: List of punch sequence strings
            
        Example:
            >>> sequences = ["1-2-3", "Cross-Hook", "Jab-Uppercut"]
            >>> app_state.set_sequences(sequences)
        """
        self.config.custom_sequences = sequences
    
    def add_sequence(self, sequence: str) -> None:
        """Add a single sequence to the list.
        
        Only adds if not already present (prevents duplicates).
        
        Args:
            sequence: Punch sequence string to add
            
        Example:
            >>> app_state.add_sequence("1-2-3")
            >>> app_state.add_sequence("Cross-Hook")
        """
        if sequence not in self.config.custom_sequences:
            self.config.custom_sequences.append(sequence)
    
    def get_config(self) -> TrainingConfig:
        """Get the current TrainingConfig instance.
        
        Returns:
            TrainingConfig: Current configuration object
            
        Example:
            >>> config = app_state.get_config()
            >>> print(config.rounds, config.difficulty)
        """
        return self.config
    
    def reset_config(self) -> None:
        """Reset the configuration to defaults.
        
        Resets the TrainingConfig and display labels to initial values.
        Call this when starting a new session or returning to main menu.
        
        Example:
            >>> app_state.reset_config()
            >>> config = app_state.get_config()
            >>> config.rounds  # 3 (default)
        """
        self.config.reset()
        self.time_label = "3min"
        self.rest_label = "1min"
