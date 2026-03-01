"""Shared placeholder helpers for training feedback flows."""

from typing import Dict, Any

from combo_curriculum import get_performance_score as _get_performance_score


def get_performance_score(video_path=None, combo_id=None) -> float:
    """Pass-through to the combo_curriculum placeholder scorer."""
    return _get_performance_score(video_path=video_path, combo_id=combo_id)


def format_feedback_data(combo_stats: Dict[str, Any], level_progress: Dict[str, Any], score: float) -> Dict[str, Any]:
    """Normalize feedback payload for downstream prompt generation/UI updates."""
    combo_stats = combo_stats or {}
    level_progress = level_progress or {}

    return {
        "score": float(score),
        "combo_name": combo_stats.get("combo_name", "Unknown"),
        "combo_sequence": combo_stats.get("combo_sequence", ""),
        "total_attempts": int(combo_stats.get("total_attempts", 0) or 0),
        "average_score": float(combo_stats.get("average_score", 0.0) or 0.0),
        "is_mastered": bool(combo_stats.get("is_mastered", False)),
        "current_group_number": int(level_progress.get("current_group_number", 0) or 0),
        "total_groups": int(level_progress.get("total_groups", 0) or 0),
        "current_group_name": level_progress.get("current_group_name", "N/A"),
        "current_group_progress": level_progress.get("current_group_progress", "0/0 combos mastered"),
        "mastered_combos": int(level_progress.get("mastered_combos", 0) or 0),
        "total_combos": int(level_progress.get("total_combos", 0) or 0),
        "can_level_up": bool(level_progress.get("can_level_up", False)),
    }
