"""Quick curriculum flow verification without GUI."""

from pathlib import Path
import sys

GUI_DIR = Path(__file__).resolve().parents[1]
if str(GUI_DIR) not in sys.path:
    sys.path.insert(0, str(GUI_DIR))


def test_curriculum_flow():
    """Test curriculum system without GUI."""
    from combo_curriculum import ComboCurriculum
    from placeholders import get_performance_score, format_feedback_data

    primary_db = GUI_DIR / "data" / "combos.db"
    fallback_db = GUI_DIR / "setup" / "combos.db"
    db_path = primary_db if primary_db.exists() else fallback_db

    curriculum = ComboCurriculum(str(db_path))
    difficulty = 'Beginner'
    last_combo = None

    print("=== TESTING CURRICULUM FLOW ===")
    print(f"Database: {db_path}")
    print()

    # Simulate 10 rounds
    for round_num in range(1, 11):
        print(f"--- Round {round_num} ---")

        # Get next combo
        combo = curriculum.get_next_combo(difficulty, last_combo)

        if not combo:
            print("All combos mastered!")
            break

        print(f"Training: {combo['combo_name']} ({combo['combo_sequence']})")
        print(f"Current mastery: {float(combo.get('mastery_score', 0) or 0):.1f}/5.0")
        print(f"Attempts: {int(combo.get('total_attempts', 0) or 0)}")

        # Simulate scoring
        score = get_performance_score()
        curriculum.update_score(combo['combo_id'], score)

        # Get stats
        stats = curriculum.get_combo_stats(combo['combo_id'])
        progress = curriculum.get_level_progress(difficulty)

        feedback_data = format_feedback_data(stats, progress, score)

        print(f"Score this round: {score:.1f}/5.0")
        print(f"New average: {stats['average_score']:.1f}/5.0")
        print(f"Group: {progress['current_group_name']} - {progress['current_group_progress']}")
        print(
            "Feedback payload: "
            f"group={feedback_data['current_group_name']}, "
            f"progress={feedback_data['current_group_progress']}, "
            f"can_level_up={feedback_data['can_level_up']}"
        )
        print()

        last_combo = combo['combo_id']

    # Check progression
    can_level_up = curriculum.check_progression_eligibility(difficulty)
    print(f"Can level up: {can_level_up}")

    curriculum.close()


if __name__ == "__main__":
    test_curriculum_flow()
