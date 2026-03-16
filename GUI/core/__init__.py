"""Core module containing configuration structures and constants."""

from .config import TrainingConfig, AppState, TRAINING_PRESETS, apply_preset
from .constants import PageIndex, ButtonStyle, DS, GLOBAL_QSS

__all__ = [
    "TrainingConfig",
    "AppState",
    "TRAINING_PRESETS",
    "apply_preset",
    "PageIndex",
    "ButtonStyle",
    "DS",
    "GLOBAL_QSS",
]
