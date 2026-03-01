"""
Combo Curriculum Package

This package provides functionality for managing and querying
boxing combination curricula from a SQLite database.
"""

from .curriculum import ComboCurriculum
from .action_recognition_placeholder import (
    get_performance_score,
    USE_ACTION_RECOGNITION,
    integrate_score_after_training
)

__all__ = [
    'ComboCurriculum',
    'get_performance_score',
    'USE_ACTION_RECOGNITION',
    'integrate_score_after_training'
]
