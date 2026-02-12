"""
Boxing Combo Curriculum System
Manages combo progression and queries from SQLite database.
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any


# ============================================================================
# ACTION RECOGNITION CONFIGURATION
# ============================================================================
# Set to True when real action recognition model is implemented
USE_ACTION_RECOGNITION = False


def get_performance_score(video_path: Optional[str] = None, combo_id: Optional[str] = None) -> float:
    """
    Get performance score from action recognition model.
    
    Args:
        video_path: Path to the video file to analyze
        combo_id: The combo being performed (for model reference)
        
    Returns:
        Performance score from 0.0 to 5.0
    
    TODO: Implement real action recognition integration
    ------------------------------------------------
    When USE_ACTION_RECOGNITION is True:
    1. Import the trained action recognition model
    2. Load and preprocess the video from video_path
    3. Run inference to detect punches and sequences
    4. Compare detected sequence against expected combo_id sequence
    5. Calculate and return accuracy score (0.0 - 5.0)
    
    Example future implementation:
        if USE_ACTION_RECOGNITION:
            from CV.action_model import ActionRecognitionModel
            model = ActionRecognitionModel.load('models/trained_action_model')
            return model.evaluate(video_path, combo_id)
    """
    if USE_ACTION_RECOGNITION:
        # TODO: Replace with real model inference
        # from CV.action_model import ActionRecognitionModel
        # model = ActionRecognitionModel.load('models/trained_action_model')
        # return model.evaluate(video_path, combo_id)
        pass
    
    # Placeholder: return fixed score for testing progression system
    return 3.0


# ============================================================================
# LLM CHATBOT CONFIGURATION
# ============================================================================
# Set to True when real LLM chatbot is implemented
USE_LLM_CHATBOT = False


def format_feedback_data(combo_stats: Dict[str, Any], level_progress: Dict[str, Any], score_received: float) -> Dict[str, Any]:
    """
    Format training data for LLM chatbot feedback.
    
    Args:
        combo_stats: Output from ComboCurriculum.get_combo_stats()
        level_progress: Output from ComboCurriculum.get_level_progress()
        score_received: The score from the current round
        
    Returns:
        Structured dict ready for LLM consumption
    """
    # Determine if improving (compare to previous average)
    previous_scores = combo_stats.get("last_5_scores", [])
    avg_score = combo_stats.get("average_score", 0.0)
    is_improving = score_received > avg_score if avg_score > 0 else True
    
    # Determine current status
    total_attempts = combo_stats.get("total_attempts", 0)
    threshold = combo_stats.get("threshold", 3.0)
    is_mastered = combo_stats.get("is_mastered", False)
    
    if is_mastered:
        current_status = "mastered"
    elif total_attempts >= 5 and avg_score < threshold:
        current_status = "struggling"
    else:
        current_status = "in_progress"
    
    # Determine next steps
    mastered_all = level_progress.get("mastered_combos", 0) == level_progress.get("total_combos", 0)
    
    return {
        "round_summary": {
            "combo_practiced": combo_stats.get("combo_name", ""),
            "score_received": score_received,
            "previous_scores": previous_scores,
            "average_score": avg_score,
            "is_improving": is_improving
        },
        "progress": {
            "difficulty": level_progress.get("difficulty", ""),
            "combos_mastered": level_progress.get("mastered_combos", 0),
            "total_combos": level_progress.get("total_combos", 0),
            "current_status": current_status
        },
        "next_steps": {
            "continue_same_combo": not is_mastered,
            "move_to_next_combo": is_mastered and not mastered_all,
            "ready_to_level_up": mastered_all
        }
    }


def get_chatbot_feedback(feedback_data: Dict[str, Any]) -> str:
    """
    Get motivational feedback from chatbot.
    
    Args:
        feedback_data: Output from format_feedback_data()
        
    Returns:
        Feedback message string
    
    TODO: Replace with actual LLM API call
    --------------------------------------
    When USE_LLM_CHATBOT is True:
    1. Import the LLM chatbot module
    2. Send feedback_data as context
    3. Get personalized response
    
    Example future implementation:
        if USE_LLM_CHATBOT:
            from llm_chatbot import generate_feedback
            response = generate_feedback(feedback_data)
            return response
    """
    if USE_LLM_CHATBOT:
        # TODO: Replace with actual LLM API call
        # from llm_chatbot import generate_feedback
        # response = generate_feedback(feedback_data)
        # return response
        pass
    
    # Placeholder: return templated feedback based on data
    round_summary = feedback_data.get("round_summary", {})
    progress = feedback_data.get("progress", {})
    next_steps = feedback_data.get("next_steps", {})
    
    combo_name = round_summary.get("combo_practiced", "this combo")
    score = round_summary.get("score_received", 0.0)
    avg = round_summary.get("average_score", 0.0)
    is_improving = round_summary.get("is_improving", False)
    
    status = progress.get("current_status", "in_progress")
    difficulty = progress.get("difficulty", "")
    mastered_count = progress.get("combos_mastered", 0)
    total_count = progress.get("total_combos", 0)
    
    # Generate appropriate template response
    if next_steps.get("ready_to_level_up"):
        return f"Congratulations! You've mastered all {total_count} {difficulty} combos. Ready for the next level?"
    
    if status == "mastered":
        return f"Excellent! You've mastered {combo_name}. Moving to next combo. ({mastered_count}/{total_count} combos mastered)"
    
    if status == "struggling":
        threshold = 3.0 if difficulty.lower() == "beginner" else 4.0
        return f"Keep practicing {combo_name}. You're at {avg:.1f}/5, aim for {threshold:.1f}/5. You've got this!"
    
    # In progress
    if is_improving:
        return f"Great job! Your score improved to {score:.1f}/5. Keep it up with {combo_name}!"
    else:
        return f"Good effort on {combo_name}! Score: {score:.1f}/5. Keep practicing to improve your average of {avg:.1f}."


class ComboCurriculum:
    """Handles boxing combo curriculum with database operations."""
    
    def __init__(self, db_path: str):
        """
        Initialize the curriculum system with database connection.
        
        Args:
            db_path: Path to the SQLite database file (combos.db)
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row  # Enable dict-like access
        self.cursor = self.connection.cursor()
    
    def get_combos_by_difficulty(self, difficulty_level: str) -> List[Dict[str, Any]]:
        """
        Get all combos for a specific difficulty level.
        
        Args:
            difficulty_level: One of 'beginner', 'intermediate', or 'advanced'
            
        Returns:
            List of combo dictionaries
        """
        query = """
            SELECT combo_id, combo_name, combo_sequence, difficulty_level,
                   mastery_score, total_attempts, last_trained_timestamp, created_date
            FROM combos
            WHERE LOWER(difficulty_level) = LOWER(?)
            ORDER BY combo_id
        """
        self.cursor.execute(query, (difficulty_level,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_combo_by_id(self, combo_id: str) -> Optional[Dict[str, Any]]:
        """
        Query a specific combo by its ID.
        
        Args:
            combo_id: The unique combo identifier (e.g., 'beginner_001')
            
        Returns:
            Combo dictionary if found, None otherwise
        """
        query = """
            SELECT combo_id, combo_name, combo_sequence, difficulty_level,
                   mastery_score, total_attempts, last_trained_timestamp, created_date
            FROM combos
            WHERE combo_id = ?
        """
        self.cursor.execute(query, (combo_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_next_combo(self, difficulty: str) -> Optional[Dict[str, Any]]:
        """
        Get the next combo to practice for sequential progression.
        
        Finds the first combo (ordered by combo_id) that is NOT mastered.
        A combo is mastered if: total_attempts >= 5 AND mastery_score >= threshold
        
        Args:
            difficulty: One of 'Beginner', 'Intermediate', or 'Advanced'
            
        Returns:
            Dict with combo_id, combo_name, combo_sequence, mastery_score, total_attempts
            or None if all combos at this difficulty are mastered
        """
        # Set mastery threshold based on difficulty
        threshold = 3.0 if difficulty.lower() == "beginner" else 4.0
        
        # Get all combos ordered by combo_id
        combos = self.get_combos_by_difficulty(difficulty)
        
        # Find first unmastered combo
        for combo in combos:
            total_attempts = combo.get("total_attempts") or 0
            mastery_score = combo.get("mastery_score") or 0.0
            
            # Not mastered: total_attempts < 5 OR mastery_score < threshold
            if total_attempts < 5 or mastery_score < threshold:
                return {
                    "combo_id": combo["combo_id"],
                    "combo_name": combo["combo_name"],
                    "combo_sequence": combo["combo_sequence"],
                    "mastery_score": mastery_score,
                    "total_attempts": total_attempts
                }
        
        # All combos mastered
        return None
    
    def update_score(self, combo_id: str, score: float) -> None:
        """
        Update scores after a training session.
        
        Args:
            combo_id: The combo that was trained
            score: Performance score from 0-5 from action recognition model
        """
        timestamp = datetime.now().isoformat()
        
        # 1. Insert score into performance_history
        self.cursor.execute(
            "INSERT INTO performance_history (combo_id, timestamp, performance_score) VALUES (?, ?, ?)",
            (combo_id, timestamp, score)
        )
        
        # 2. Get last 5 scores for this combo_id
        self.cursor.execute(
            """
            SELECT performance_score FROM performance_history
            WHERE combo_id = ?
            ORDER BY timestamp DESC
            LIMIT 5
            """,
            (combo_id,)
        )
        rows = self.cursor.fetchall()
        
        # 3. Calculate average of last 5 (or fewer if < 5 exist)
        scores = [row["performance_score"] for row in rows]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        # 4. Update combos table
        self.cursor.execute(
            """
            UPDATE combos
            SET mastery_score = ?,
                total_attempts = total_attempts + 1,
                last_trained_timestamp = ?
            WHERE combo_id = ?
            """,
            (avg_score, timestamp, combo_id)
        )
        
        self.connection.commit()
    
    def _get_threshold(self, difficulty: str) -> float:
        """Get mastery threshold for a difficulty level."""
        return 3.0 if difficulty.lower() == "beginner" else 4.0
    
    def get_combo_stats(self, combo_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed statistics for a specific combo.
        
        Args:
            combo_id: The combo identifier
            
        Returns:
            Dict with combo stats or None if combo not found
        """
        # Get combo info
        combo = self.get_combo_by_id(combo_id)
        if not combo:
            return None
        
        # Get last 5 scores from performance_history
        self.cursor.execute(
            """
            SELECT performance_score FROM performance_history
            WHERE combo_id = ?
            ORDER BY timestamp DESC
            LIMIT 5
            """,
            (combo_id,)
        )
        rows = self.cursor.fetchall()
        last_5_scores = [row["performance_score"] for row in rows]
        
        # Calculate average
        average_score = sum(last_5_scores) / len(last_5_scores) if last_5_scores else 0.0
        
        # Determine threshold based on difficulty
        difficulty = combo.get("difficulty_level", "beginner")
        threshold = self._get_threshold(difficulty)
        
        total_attempts = combo.get("total_attempts") or 0
        is_mastered = total_attempts >= 5 and average_score >= threshold
        
        return {
            "combo_name": combo["combo_name"],
            "combo_sequence": combo["combo_sequence"],
            "last_5_scores": last_5_scores,
            "average_score": average_score,
            "total_attempts": total_attempts,
            "is_mastered": is_mastered,
            "threshold": threshold
        }
    
    def get_level_progress(self, difficulty: str) -> Dict[str, Any]:
        """
        Get progress summary for a difficulty level.
        
        Args:
            difficulty: One of 'Beginner', 'Intermediate', or 'Advanced'
            
        Returns:
            Dict with progress statistics
        """
        combos = self.get_combos_by_difficulty(difficulty)
        threshold = self._get_threshold(difficulty)
        
        mastered_count = 0
        in_progress_count = 0
        struggling_count = 0
        
        for combo in combos:
            total_attempts = combo.get("total_attempts") or 0
            mastery_score = combo.get("mastery_score") or 0.0
            
            if total_attempts >= 5 and mastery_score >= threshold:
                mastered_count += 1
            elif total_attempts < 5:
                in_progress_count += 1
            else:
                # >= 5 attempts but below threshold
                struggling_count += 1
        
        return {
            "difficulty": difficulty,
            "total_combos": len(combos),
            "mastered_combos": mastered_count,
            "in_progress_combos": in_progress_count,
            "struggling_combos": struggling_count
        }
    
    def get_next_difficulty(self, current_difficulty: str) -> Optional[str]:
        """
        Get the next difficulty level.
        
        Args:
            current_difficulty: Current difficulty level
            
        Returns:
            Next difficulty level or None if at highest level
        """
        progression = {
            "beginner": "Intermediate",
            "intermediate": "Advanced",
            "advanced": None
        }
        return progression.get(current_difficulty.lower())
    
    def check_progression_eligibility(self, current_difficulty: str) -> bool:
        """
        Check if user can progress to next difficulty level.
        
        Rules:
        - Beginner → Intermediate: All 15 beginner combos mastered (>=5 attempts, >=3.0 score)
        - Intermediate → Advanced: All 20 intermediate combos mastered (>=5 attempts, >=4.0 score)
        - Advanced: Returns True if all 15 advanced combos mastered (no next level)
        
        Args:
            current_difficulty: Current difficulty level
            
        Returns:
            True if eligible to progress, False otherwise
        """
        combos = self.get_combos_by_difficulty(current_difficulty)
        threshold = self._get_threshold(current_difficulty)
        
        # Check if ALL combos are mastered
        for combo in combos:
            total_attempts = combo.get("total_attempts") or 0
            mastery_score = combo.get("mastery_score") or 0.0
            
            if total_attempts < 5 or mastery_score < threshold:
                return False
        
        return True
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Example usage
if __name__ == "__main__":
    # Example with context manager
    with ComboCurriculum("combos.db") as curriculum:
        # Get all beginner combos
        beginner_combos = curriculum.get_combos_by_difficulty("beginner")
        print(f"Found {len(beginner_combos)} beginner combos")
        
        # Get a specific combo
        combo = curriculum.get_combo_by_id("beginner_001")
        if combo:
            print(f"Combo: {combo['combo_name']}")
