"""
ComboCurriculum - Boxing Combo Database Manager

This module provides a class for managing and querying boxing combinations
from a SQLite database containing beginner, intermediate, and advanced combos.

Database Schema:
    - combos table: combo_id, combo_name, combo_sequence, difficulty_level,
                   mastery_score, total_attempts, last_trained_timestamp, created_date
    - performance_history table: id, combo_id, timestamp, performance_score
"""

import sqlite3
from typing import List, Dict, Optional, Any
from datetime import datetime


DEBUG = False


def _debug_log(message: str) -> None:
    if DEBUG:
        print(message)


class ComboCurriculum:
    """
    Manages boxing combo curriculum database.
    
    Provides methods to connect to the database and query combos by difficulty level.
    
    Attributes:
        db_path (str): Path to the SQLite database file
        connection (sqlite3.Connection): Database connection object
    
    Example:
        >>> curriculum = ComboCurriculum("combos.db")
        >>> beginner_combos = curriculum.get_combos_by_difficulty("Beginner")
        >>> combo = curriculum.get_combo_by_id("beginner_001")
    """

    GROUP_BOUNDARIES = {
        "Beginner": [
            (1, 6, "Single Punches"),
            (7, 12, "2-Punch Combos with Jab"),
            (13, 15, "2-Punch Other Combos"),
        ],
        "Intermediate": [
            (1, 8, "3-Punch Combos"),
            (9, 11, "Body Shot Combos"),
            (12, 13, "Defense Combos"),
            (14, 20, "Advanced Patterns"),
        ],
        "Advanced": [
            (1, 5, "Long Combinations"),
            (6, 8, "Complex Defense"),
            (9, 15, "Counter Punching"),
        ],
    }
    
    def __init__(self, db_path: str):
        """
        Initialize the ComboCurriculum with a database connection.
        
        Args:
            db_path (str): Path to the SQLite database file (e.g., "combos.db")
        
        Raises:
            sqlite3.Error: If database connection fails
        """
        self.db_path = db_path
        self.connection = None
        self._connect()
    
    def _connect(self):
        """Establish connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            _debug_log(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def get_combos_by_difficulty(self, difficulty_level: str) -> List[Dict[str, Any]]:
        """
        Retrieve all combos for a specific difficulty level.
        
        Args:
            difficulty_level (str): Difficulty level - "Beginner", "Intermediate", or "Advanced"
        
        Returns:
            List[Dict[str, Any]]: List of combo dictionaries with all fields from the combos table
        
        Example:
            >>> combos = curriculum.get_combos_by_difficulty("Beginner")
            >>> print(f"Found {len(combos)} beginner combos")
        """
        if not self.connection:
            raise RuntimeError("Database connection not established")
        
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT combo_id, combo_name, combo_sequence, difficulty_level,
                       mastery_score, total_attempts, last_trained_timestamp, created_date
                FROM combos
                WHERE difficulty_level = ?
                ORDER BY combo_id
            """
            cursor.execute(query, (difficulty_level,))
            rows = cursor.fetchall()
            
            # Convert rows to list of dictionaries
            combos = []
            for row in rows:
                combos.append({
                    'combo_id': row['combo_id'],
                    'combo_name': row['combo_name'],
                    'combo_sequence': row['combo_sequence'],
                    'difficulty_level': row['difficulty_level'],
                    'mastery_score': row['mastery_score'],
                    'total_attempts': row['total_attempts'],
                    'last_trained_timestamp': row['last_trained_timestamp'],
                    'created_date': row['created_date']
                })
            
            return combos
        except sqlite3.Error as e:
            print(f"Error querying combos by difficulty: {e}")
            return []
    
    def get_combo_by_id(self, combo_id: str) -> Optional[Dict[str, Any]]:
        """
        Query a specific combo by its combo_id.
        
        Args:
            combo_id (str): The unique combo identifier (e.g., "beginner_001")
        
        Returns:
            Optional[Dict[str, Any]]: Combo dictionary with all fields, or None if not found
        
        Example:
            >>> combo = curriculum.get_combo_by_id("beginner_001")
            >>> if combo:
            >>>     print(f"Combo: {combo['combo_name']}")
        """
        if not self.connection:
            raise RuntimeError("Database connection not established")
        
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT combo_id, combo_name, combo_sequence, difficulty_level,
                       mastery_score, total_attempts, last_trained_timestamp, created_date
                FROM combos
                WHERE combo_id = ?
            """
            cursor.execute(query, (combo_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'combo_id': row['combo_id'],
                    'combo_name': row['combo_name'],
                    'combo_sequence': row['combo_sequence'],
                    'difficulty_level': row['difficulty_level'],
                    'mastery_score': row['mastery_score'],
                    'total_attempts': row['total_attempts'],
                    'last_trained_timestamp': row['last_trained_timestamp'],
                    'created_date': row['created_date']
                }
            return None
        except sqlite3.Error as e:
            print(f"Error querying combo by ID: {e}")
            return None
    
    def update_score(self, combo_id: str, score: float) -> bool:
        """
        Update combo score after training session.
        
        This method:
        1. Inserts score into performance_history with current timestamp
        2. Gets last 5 scores for this combo
        3. Calculates average of those last 5 scores
        4. Updates combos table with new mastery_score, increments total_attempts,
           and updates last_trained_timestamp
        
        Args:
            combo_id (str): The combo identifier (e.g., "beginner_001")
            score (float): Performance score from action recognition model (0-5)
        
        Returns:
            bool: True on success, False on failure
        
        Example:
            >>> curriculum.update_score("beginner_001", 4.2)
            >>> True
        """
        if not self.connection:
            raise RuntimeError("Database connection not established")
        
        try:
            cursor = self.connection.cursor()
            current_time = datetime.now().isoformat()
            
            # Step 1: Insert score into performance_history
            insert_query = """
                INSERT INTO performance_history (combo_id, timestamp, performance_score)
                VALUES (?, ?, ?)
            """
            cursor.execute(insert_query, (combo_id, current_time, score))
            
            # Step 2: Get last 5 scores for this combo
            history_query = """
                SELECT performance_score
                FROM performance_history
                WHERE combo_id = ?
                ORDER BY timestamp DESC
                LIMIT 5
            """
            cursor.execute(history_query, (combo_id,))
            recent_scores = cursor.fetchall()
            
            # Step 3: Calculate average of last 5 scores (0-5 scale)
            if recent_scores:
                scores = [row['performance_score'] for row in recent_scores]
                avg_score = sum(scores) / len(scores)
                # Store mastery score directly on 0-5 scale
                mastery_score = avg_score
                num_sessions = len(scores)
            else:
                mastery_score = score
                num_sessions = 1
            
            # Step 4: Update combos table
            update_query = """
                UPDATE combos
                SET mastery_score = ?,
                    total_attempts = total_attempts + 1,
                    last_trained_timestamp = ?
                WHERE combo_id = ?
            """
            cursor.execute(update_query, (mastery_score, current_time, combo_id))
            
            # Commit changes
            self.connection.commit()
            
            print(f"Updated {combo_id}: score={score:.2f}, mastery={mastery_score:.3f} (avg of {num_sessions} sessions)")
            return True
            
        except sqlite3.Error as e:
            print(f"[ERROR] SQLite error updating score for {combo_id}: {e}")
            import traceback
            traceback.print_exc()
            if self.connection:
                self.connection.rollback()
            return False
        except Exception as e:
            print(f"[ERROR] Unexpected error updating score for {combo_id}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_next_combo(self, difficulty: str, last_combo_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get the next combo to train for a difficulty level using group-based progression.

        Selection rules:
        1. Identify the FIRST group in this difficulty that still has unmastered combos.
        2. Within that group, prioritize combos with the lowest attempts.
        3. Avoid selecting the provided last_combo_id when alternatives exist.
        4. Return None when all groups at this difficulty are fully mastered.

        Mastery criteria per combo:
        - Beginner: total_attempts >= 5 AND average/mastery >= 3.0 (0-5 scale)
        - Intermediate/Advanced: total_attempts >= 5 AND average/mastery >= 4.0 (0-5 scale)
        
        Args:
            difficulty (str): Difficulty level - "Beginner", "Intermediate", or "Advanced"
            last_combo_id (Optional[str]): Most recently trained combo ID to avoid immediate repetition
        
        Returns:
            Optional[Dict[str, Any]]: Next combo to practice, or None if all are mastered
        
        Example:
            >>> next_combo = curriculum.get_next_combo("Beginner")
            >>> if next_combo:
            >>>     print(f"Practice: {next_combo['combo_name']}")
            >>> else:
            >>>     print("All combos mastered!")
        """
        if not self.connection:
            raise RuntimeError("Database connection not established")

        if difficulty not in self.GROUP_BOUNDARIES:
            return None

        threshold = 3.0 if difficulty == "Beginner" else 4.0

        def combo_index(combo_id: str) -> int:
            try:
                return int(combo_id.split("_")[-1])
            except (ValueError, IndexError):
                return 0

        def is_mastered(combo: Dict[str, Any]) -> bool:
            total_attempts = combo.get('total_attempts') or 0
            mastery_score = combo.get('mastery_score') or 0.0
            return total_attempts >= 5 and mastery_score >= threshold

        try:
            all_combos = self.get_combos_by_difficulty(difficulty)
            if not all_combos:
                return None

            # Group combos by configured ID boundaries and find first unfinished group
            active_group = None
            for start_idx, end_idx, _group_name in self.GROUP_BOUNDARIES[difficulty]:
                group_combos = [
                    combo for combo in all_combos
                    if start_idx <= combo_index(combo['combo_id']) <= end_idx
                ]

                if not group_combos:
                    continue

                if any(not is_mastered(combo) for combo in group_combos):
                    active_group = group_combos
                    break

            # All groups are mastered
            if not active_group:
                return None

            # Train only unmastered combos in the current active group
            candidates = [combo for combo in active_group if not is_mastered(combo)]
            if not candidates:
                return None

            # Prefer caller-provided last combo; fallback to most recent in active group
            recent_combo = last_combo_id
            if not recent_combo:
                recent_timestamp = ""
                for combo in active_group:
                    ts = combo.get('last_trained_timestamp') or ""
                    if ts > recent_timestamp:
                        recent_timestamp = ts
                        recent_combo = combo.get('combo_id')

            # Prioritize lowest attempts first, then stable combo_id order
            min_attempts = min((combo.get('total_attempts') or 0) for combo in candidates)
            lowest_attempt_candidates = [
                combo for combo in candidates
                if (combo.get('total_attempts') or 0) == min_attempts
            ]
            lowest_attempt_candidates.sort(key=lambda combo: combo.get('combo_id', ''))

            # Avoid immediately repeating the most recently trained combo when possible
            non_recent_candidates = [
                combo for combo in lowest_attempt_candidates
                if combo.get('combo_id') != recent_combo
            ]
            selected = non_recent_candidates[0] if non_recent_candidates else lowest_attempt_candidates[0]

            return {
                'combo_id': selected['combo_id'],
                'combo_name': selected['combo_name'],
                'combo_sequence': selected['combo_sequence'],
                'difficulty_level': selected['difficulty_level'],
                'mastery_score': selected['mastery_score'],
                'total_attempts': selected['total_attempts'],
                'last_trained_timestamp': selected['last_trained_timestamp'],
                'created_date': selected['created_date'],
            }

        except Exception as e:
            print(f"Error getting next combo: {e}")
            return None
    
    def get_combo_stats(self, combo_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed statistics for a specific combo.
        
        Returns comprehensive stats including last 5 scores, average,
        mastery status, and threshold for the combo's difficulty level.
        
        Args:
            combo_id (str): The combo identifier (e.g., "beginner_001")
        
        Returns:
            Optional[Dict[str, Any]]: Statistics dictionary or None if combo not found
            
            Dictionary contains:
            - combo_name: Name of the combo
            - combo_sequence: Punch sequence
            - last_5_scores: List of last 5 performance scores (0-5 scale)
            - average_score: Average of last 5 scores (0-5 scale)
            - total_attempts: Total number of training sessions
            - is_mastered: True if >= 5 attempts AND >= threshold
            - threshold: Mastery threshold (3.0 for Beginner, 4.0 for Intermediate/Advanced)
        
        Example:
            >>> stats = curriculum.get_combo_stats("beginner_001")
            >>> print(f"Average: {stats['average_score']:.1f}/5.0")
            >>> print(f"Mastered: {stats['is_mastered']}")
        """
        if not self.connection:
            raise RuntimeError("Database connection not established")
        
        try:
            cursor = self.connection.cursor()
            
            # Get combo info
            combo_query = """
                SELECT combo_name, combo_sequence, difficulty_level, total_attempts
                FROM combos
                WHERE combo_id = ?
            """
            cursor.execute(combo_query, (combo_id,))
            combo_row = cursor.fetchone()
            
            if not combo_row:
                return None
            
            # Get last 5 scores from performance_history
            history_query = """
                SELECT performance_score
                FROM performance_history
                WHERE combo_id = ?
                ORDER BY timestamp DESC
                LIMIT 5
            """
            cursor.execute(history_query, (combo_id,))
            score_rows = cursor.fetchall()
            
            # Extract scores (they're on 0-5 scale in database)
            last_5_scores = [row['performance_score'] for row in score_rows]
            last_5_scores.reverse()  # Show oldest to newest
            
            # Calculate average
            if last_5_scores:
                average_score = sum(last_5_scores) / len(last_5_scores)
            else:
                average_score = 0.0
            
            # Determine threshold based on difficulty
            difficulty = combo_row['difficulty_level']
            threshold = 3.0 if difficulty == "Beginner" else 4.0
            
            # Check if mastered
            total_attempts = combo_row['total_attempts'] or 0
            is_mastered = total_attempts >= 5 and average_score >= threshold
            
            return {
                'combo_name': combo_row['combo_name'],
                'combo_sequence': combo_row['combo_sequence'],
                'last_5_scores': last_5_scores,
                'average_score': average_score,
                'total_attempts': total_attempts,
                'is_mastered': is_mastered,
                'threshold': threshold
            }
            
        except sqlite3.Error as e:
            print(f"Error getting combo stats: {e}")
            return None
    
    def get_level_progress(self, difficulty: str) -> Dict[str, Any]:
        """
        Get progress statistics for an entire difficulty level with group context.
        
        Args:
            difficulty (str): Difficulty level - "Beginner", "Intermediate", or "Advanced"
        
        Returns:
            Dict[str, Any]: Progress statistics including current group details.
        
        Example:
            >>> progress = curriculum.get_level_progress("Beginner")
            >>> print(f"Current group: {progress['current_group_name']}")
            >>> print(f"Group progress: {progress['current_group_progress']}")
        """
        if not self.connection:
            raise RuntimeError("Database connection not established")
        
        # Set threshold based on difficulty (0-5 scale)
        threshold = 3.0 if difficulty == "Beginner" else 4.0

        if difficulty not in self.GROUP_BOUNDARIES:
            return {
                'difficulty': difficulty,
                'total_combos': 0,
                'mastered_combos': 0,
                'current_group_number': 0,
                'current_group_name': 'Unknown difficulty',
                'current_group_progress': '0/0 combos mastered',
                'groups_completed': 0,
                'total_groups': 0,
                'can_level_up': False,
                'in_progress_combos': 0,
                'struggling_combos': 0
            }

        def combo_index(combo_id: str) -> int:
            try:
                return int(combo_id.split("_")[-1])
            except (ValueError, IndexError):
                return 0

        def is_mastered(total_attempts: int, mastery_score: float) -> bool:
            return total_attempts >= 5 and mastery_score >= threshold
        
        try:
            cursor = self.connection.cursor()
            
            # Get all combos for this difficulty
            query = """
                SELECT combo_id, total_attempts, mastery_score
                FROM combos
                WHERE difficulty_level = ?
                ORDER BY combo_id
            """
            cursor.execute(query, (difficulty,))
            rows = cursor.fetchall()
            
            total_combos = len(rows)
            mastered_combos = 0
            in_progress_combos = 0
            struggling_combos = 0

            combo_by_id = {}
            
            for row in rows:
                combo_id = row['combo_id']
                total_attempts = row['total_attempts'] or 0
                mastery_score = row['mastery_score'] or 0.0

                combo_by_id[combo_id] = {
                    'total_attempts': total_attempts,
                    'mastery_score': mastery_score,
                }
                
                if total_attempts < 5:
                    # Not enough attempts yet
                    in_progress_combos += 1
                elif is_mastered(total_attempts, mastery_score):
                    # Mastered: >= 5 attempts AND >= threshold
                    mastered_combos += 1
                else:
                    # Struggling: >= 5 attempts but below threshold
                    struggling_combos += 1

            groups = self.GROUP_BOUNDARIES[difficulty]
            total_groups = len(groups)
            groups_completed = 0
            current_group_number = 0
            current_group_name = "All groups mastered"
            current_group_progress = "0/0 combos mastered"

            for index, (start_idx, end_idx, group_name) in enumerate(groups, start=1):
                group_combo_ids = [
                    combo_id for combo_id in combo_by_id.keys()
                    if start_idx <= combo_index(combo_id) <= end_idx
                ]
                group_total = len(group_combo_ids)

                group_mastered = 0
                for combo_id in group_combo_ids:
                    combo_data = combo_by_id[combo_id]
                    if is_mastered(combo_data['total_attempts'], combo_data['mastery_score']):
                        group_mastered += 1

                group_is_complete = group_total > 0 and group_mastered == group_total

                if group_is_complete:
                    groups_completed += 1
                elif current_group_number == 0:
                    current_group_number = index
                    current_group_name = group_name
                    current_group_progress = f"{group_mastered}/{group_total} combos mastered"

            can_level_up = groups_completed == total_groups and total_groups > 0
            if can_level_up:
                current_group_progress = "All groups completed"
            
            return {
                'difficulty': difficulty,
                'total_combos': total_combos,
                'mastered_combos': mastered_combos,
                'current_group_number': current_group_number,
                'current_group_name': current_group_name,
                'current_group_progress': current_group_progress,
                'groups_completed': groups_completed,
                'total_groups': total_groups,
                'can_level_up': can_level_up,
                'in_progress_combos': in_progress_combos,
                'struggling_combos': struggling_combos
            }
            
        except sqlite3.Error as e:
            print(f"Error getting level progress: {e}")
            return {
                'difficulty': difficulty,
                'total_combos': 0,
                'mastered_combos': 0,
                'current_group_number': 0,
                'current_group_name': 'Unavailable',
                'current_group_progress': '0/0 combos mastered',
                'groups_completed': 0,
                'total_groups': len(self.GROUP_BOUNDARIES.get(difficulty, [])),
                'can_level_up': False,
                'in_progress_combos': 0,
                'struggling_combos': 0
            }
    
    def check_progression_eligibility(self, current_difficulty: str) -> bool:
        """
        Check if user is eligible to progress to the next difficulty level.
        
        Progression requirements:
        - Beginner → Intermediate: ALL 15 beginner combos have total_attempts >= 5 AND mastery_score >= 3.0
        - Intermediate → Advanced: ALL 20 intermediate combos have total_attempts >= 5 AND mastery_score >= 4.0
        - Advanced: No next level (all combos mastered at highest level)
        
        Args:
            current_difficulty (str): Current difficulty level - "Beginner", "Intermediate", or "Advanced"
        
        Returns:
            bool: True if user meets criteria to level up, False otherwise
        
        Example:
            >>> if curriculum.check_progression_eligibility("Beginner"):
            >>>     print("Ready to advance to Intermediate!")
        """
        if not self.connection:
            raise RuntimeError("Database connection not established")
        
        # Advanced is the highest level - no progression beyond it
        if current_difficulty == "Advanced":
            return False
        
        # Set mastery threshold based on difficulty (0-5 scale)
        threshold = 3.0 if current_difficulty == "Beginner" else 4.0
        
        try:
            cursor = self.connection.cursor()
            
            # Get all combos for current difficulty
            query = """
                SELECT combo_id, total_attempts, mastery_score
                FROM combos
                WHERE difficulty_level = ?
                ORDER BY combo_id
            """
            cursor.execute(query, (current_difficulty,))
            rows = cursor.fetchall()
            
            # Check if ALL combos meet mastery criteria
            for row in rows:
                total_attempts = row['total_attempts'] or 0
                mastery_score = row['mastery_score'] or 0.0
                
                # If ANY combo doesn't meet criteria, user cannot progress
                if total_attempts < 5 or mastery_score < threshold:
                    return False
            
            # All combos meet the criteria
            return True
            
        except sqlite3.Error as e:
            print(f"Error checking progression eligibility: {e}")
            return False
    
    def get_next_difficulty(self, current_difficulty: str) -> Optional[str]:
        """
        Get the next difficulty level after the current one.
        
        Args:
            current_difficulty (str): Current difficulty level - "Beginner", "Intermediate", or "Advanced"
        
        Returns:
            Optional[str]: Next difficulty level ('Intermediate', 'Advanced', or None)
        
        Example:
            >>> next_level = curriculum.get_next_difficulty("Beginner")
            >>> print(f"Next level: {next_level}")  # Output: Next level: Intermediate
        """
        difficulty_progression = {
            "Beginner": "Intermediate",
            "Intermediate": "Advanced",
            "Advanced": None  # No level after Advanced
        }
        
        return difficulty_progression.get(current_difficulty)
    
    def get_all_combos_with_progress(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all combos organized by difficulty with their progress data.
        
        Returns:
            Dict[str, List[Dict]]: Dictionary with difficulty levels as keys,
            each containing list of combos with: combo_id, combo_name, combo_sequence,
            mastery_score, total_attempts, is_mastered
        
        Example:
            >>> combos = curriculum.get_all_combos_with_progress()
            >>> for difficulty, combo_list in combos.items():
            >>>     for combo in combo_list:
            >>>         print(f"{combo['combo_name']}: {combo['mastery_score']:.1f}")
        """
        if not self.connection:
            raise RuntimeError("Database connection not established")
        
        result = {}
        
        for difficulty in ["Beginner", "Intermediate", "Advanced"]:
            threshold = 3.0 if difficulty == "Beginner" else 4.0
            
            try:
                cursor = self.connection.cursor()
                query = """
                    SELECT combo_id, combo_name, combo_sequence, mastery_score, total_attempts
                    FROM combos
                    WHERE difficulty_level = ?
                    ORDER BY combo_id
                """
                cursor.execute(query, (difficulty,))
                rows = cursor.fetchall()
                
                combos_list = []
                for row in rows:
                    total_attempts = row['total_attempts'] or 0
                    mastery_score = row['mastery_score'] or 0.0
                    is_mastered = total_attempts >= 5 and mastery_score >= threshold
                    
                    combos_list.append({
                        'combo_id': row['combo_id'],
                        'combo_name': row['combo_name'],
                        'combo_sequence': row['combo_sequence'],
                        'mastery_score': mastery_score,
                        'total_attempts': total_attempts,
                        'is_mastered': is_mastered
                    })
                
                result[difficulty] = combos_list
            except sqlite3.Error as e:
                print(f"Error getting combos for {difficulty}: {e}")
                result[difficulty] = []
        
        return result
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            _debug_log("Database connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures connection is closed."""
        self.close()
