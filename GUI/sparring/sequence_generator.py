from typing import Dict, List
import random
from sparring.combo_pools import STYLE_TRANSITION_MATRICES

# Constants (will be controlled by speed parameter in future)
PUNCH_DURATION_S = 1.0
INTER_COMBO_GAP_S = 0.5

def _weighted_choice(state_dict: Dict[str, float]) -> str:
    """
    Helper function to pick a key using weighted random choice.
    """
    choices, weights = zip(*state_dict.items())
    return random.choices(choices, weights=weights, k=1)[0]

def _apply_weakness_bias(matrix: Dict[str, Dict[str, float]], weakness_profile: Dict[str, float]) -> Dict[str, Dict[str, float]]:
    """
    Apply weakness bias to the transition matrix based on the weakness profile.
    Returns a modified copy of the matrix with blended weights.
    """
    if not weakness_profile:
        return matrix  # No modification if weakness profile is empty or None

    # Map weakness profile keys to punch keys
    punch_map = {
        "jab_freq": "1",
        "cross_freq": "2",
        "lead_hook_freq": "3",
        "rear_hook_freq": "4",
        "lead_upper_freq": "5",
        "rear_upper_freq": "6",
    }

    sessions_count = weakness_profile.get("sessions_count", 0)
    alpha = min(0.4, sessions_count * 0.05)

    modified_matrix = {}
    for state, transitions in matrix.items():
        modified_transitions = {}
        for punch, base_weight in transitions.items():
            if punch in punch_map.values():
                # Determine weakness multiplier
                if punch in ["1", "3", "5"]:  # Left-side punches
                    weakness_multiplier = sum(weakness_profile.get(key, 0) for key in ["cross_freq", "rear_hook_freq", "rear_upper_freq"])
                elif punch in ["2", "4", "6"]:  # Right-side punches
                    weakness_multiplier = sum(weakness_profile.get(key, 0) for key in ["jab_freq", "lead_hook_freq", "lead_upper_freq"])
                else:
                    weakness_multiplier = 0

                # Blend weights
                final_weight = (1 - alpha) * base_weight + alpha * weakness_multiplier
                modified_transitions[punch] = final_weight
            else:
                modified_transitions[punch] = base_weight

        # Normalize weights to sum to 1.0
        total_weight = sum(modified_transitions.values())
        for punch in modified_transitions:
            modified_transitions[punch] /= total_weight

        modified_matrix[state] = modified_transitions

    return modified_matrix

def generate_session_sequence(
    style: str,
    weakness_profile: Dict[str, float],
    rounds: int,
    round_duration_seconds: int,
) -> List[List[str]]:
    """
    Generate a full multi-round punch sequence based on the given style and weakness profile.

    Args:
        style: The fighting style to use (e.g., "Pressure Fighter").
        weakness_profile: A dictionary describing the user's weaknesses.
        rounds: Number of rounds to generate.
        round_duration_seconds: Duration of each round in seconds.

    Returns:
        A list of rounds, where each round is a list of punch strings.
    """
    if style not in STYLE_TRANSITION_MATRICES:
        raise ValueError(f"Style '{style}' not found in transition matrices.")

    base_matrix = STYLE_TRANSITION_MATRICES[style]
    matrix = _apply_weakness_bias(base_matrix, weakness_profile)

    session_sequence = []

    for _ in range(rounds):
        round_sequence = []
        time_elapsed = 0.0

        while time_elapsed < round_duration_seconds:
            combo = []
            state = "start"

            while state != "end" and len(combo) < 6:  # Safety limit: max 6 punches per combo
                if state not in matrix:
                    state = "end"  # Defensive check: treat missing state as "end"
                    break

                next_punch = _weighted_choice(matrix[state])
                if next_punch == "end":
                    break

                combo.append(next_punch)
                state = next_punch

            round_sequence.extend(combo)
            time_elapsed += len(combo) * PUNCH_DURATION_S + INTER_COMBO_GAP_S

        session_sequence.append(round_sequence)

    return session_sequence