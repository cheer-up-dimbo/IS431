#!/usr/bin/env python3
"""Focused Phase 1 validation for TrainingSessionPage curriculum integration."""

import os
import sys
from pathlib import Path

GUI_DIR = Path(__file__).resolve().parents[1]
if str(GUI_DIR) not in sys.path:
    sys.path.insert(0, str(GUI_DIR))

from PySide6.QtWidgets import QApplication, QStackedWidget, QWidget

import main_gui
from core import PageIndex


def main():
    app = QApplication.instance() or QApplication([])

    # Make score deterministic for test repeatability
    main_gui.get_performance_score = lambda video_path=None, combo_id=None: 3.5

    stack = QStackedWidget()
    # Populate enough dummy pages so setCurrentIndex calls are safe
    for _ in range(PageIndex.COMBO_LLM_CHAT + 1):
        stack.addWidget(QWidget())

    page = main_gui.TrainingSessionPage(stack)

    # Avoid routing into UI results pages during headless test
    page.show_combo_results = lambda: print("[TEST] show_combo_results called")

    rounds = 3
    page.start_session(
        rounds=rounds,
        time_str="10sec",
        rest_str="10sec",
        difficulty="Beginner",
        sequences=None,
        battle_style=None,
        username="123",
    )

    # Drive state machine manually instead of waiting for real-time QTimer
    page.timer.stop()

    observed_combo_ids = []
    safety = 0
    while safety < 400:
        safety += 1

        if (
            not page.is_resting
            and page.current_difficulty in ["Beginner", "Intermediate", "Advanced"]
            and page.current_combo_id
        ):
            if not observed_combo_ids or observed_combo_ids[-1] != page.current_combo_id:
                observed_combo_ids.append(page.current_combo_id)

        was_active = page.timer.isActive()
        page.update_timer()

        # End condition after final round flow completes
        if not page.timer.isActive() and (was_active or page.current_round >= rounds):
            break

    print("=== TRAINING SESSION PHASE 1 TEST ===")
    print(f"Observed combo ids: {observed_combo_ids}")
    print(f"Rounds configured: {rounds}")
    print(f"Final round counter: {page.current_round}")
    print(f"Final combo score: {page.combo_score}")

    # Verify DB writes for observed combos
    db_path = os.path.join(os.path.dirname(main_gui.__file__), "data", "combos.db")
    with main_gui.ComboCurriculum(db_path) as curriculum:
        for combo_id in observed_combo_ids:
            stats = curriculum.get_combo_stats(combo_id) or {}
            attempts = stats.get("total_attempts", "?")
            mastery = stats.get("mastery_score", "?")
            print(f"Combo {combo_id}: attempts={attempts}, mastery={mastery}")

    if len(observed_combo_ids) >= 2:
        print("PASS: combo rotation observed across rounds")
    else:
        print("FAIL: combo rotation not observed")


if __name__ == "__main__":
    main()
