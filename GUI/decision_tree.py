#!/usr/bin/env python3
"""
DecisionTreeEngine: Decides robot response based on user combo and selected style.
"""


class DecisionTreeEngine:
    """
    Analyzes user combos and generates robot counter-responses based on fighting style.
    """
    
    STYLES = ["aggressive", "defensive", "balanced"]
    
    @staticmethod
    def decide(style, combo_dict):
        """
        Analyze combo and decide robot response.
        
        Args:
            style: str - one of "aggressive", "defensive", "balanced"
            combo_dict: dict - the combo from ComboAssembler with keys:
                - sequence: list of punch names
                - num_punches: int
                - duration: float
                - punches: list of punch event dicts
        
        Returns:
            dict with keys:
                - response_sequence: list of punch IDs
                - strategy: str description
                - timing: str ("immediate", "delayed", "counter")
        """
        sequence = combo_dict.get("sequence", [])
        num_punches = combo_dict.get("num_punches", 0)
        duration = combo_dict.get("duration", 0)
        
        # Default response
        response = {
            "response_sequence": [],
            "strategy": "wait",
            "timing": "delayed"
        }
        
        if num_punches == 0:
            return response
        
        # Calculate combo intensity
        punches_per_sec = num_punches / duration if duration > 0 else 0
        is_fast = punches_per_sec > 1.5
        is_heavy = any(p in sequence for p in ["cross", "right_hook", "left_hook"])
        
        if style == "aggressive":
            response = DecisionTreeEngine._aggressive_strategy(sequence, is_fast, is_heavy)
        elif style == "defensive":
            response = DecisionTreeEngine._defensive_strategy(sequence, is_fast, is_heavy)
        else:  # balanced
            response = DecisionTreeEngine._balanced_strategy(sequence, is_fast, is_heavy)
        
        return response
    
    @staticmethod
    def _aggressive_strategy(sequence, is_fast, is_heavy):
        """Aggressive style: counter-attack immediately with power punches."""
        if is_heavy:
            # Counter power with power
            return {
                "response_sequence": ["2", "5", "3"],  # cross, left_hook, jab combo
                "strategy": "counter-power",
                "timing": "immediate"
            }
        else:
            # Pressure with volume
            return {
                "response_sequence": ["1", "2", "1"],  # jab-cross-jab
                "strategy": "pressure",
                "timing": "immediate"
            }
    
    @staticmethod
    def _defensive_strategy(sequence, is_fast, is_heavy):
        """Defensive style: block and counter conservatively."""
        if is_fast:
            # Wait and single counter
            return {
                "response_sequence": ["2"],  # single cross counter
                "strategy": "patient-counter",
                "timing": "delayed"
            }
        else:
            # Block and jab
            return {
                "response_sequence": ["1"],  # single jab
                "strategy": "defensive-jab",
                "timing": "delayed"
            }
    
    @staticmethod
    def _balanced_strategy(sequence, is_fast, is_heavy):
        """Balanced style: adaptive response based on combo characteristics."""
        if is_heavy and not is_fast:
            # Counter heavy slow combo with speed
            return {
                "response_sequence": ["1", "2"],  # jab-cross
                "strategy": "speed-counter",
                "timing": "counter"
            }
        elif is_fast:
            # Counter fast combo with defense then power
            return {
                "response_sequence": ["2", "5"],  # cross-hook
                "strategy": "defend-punish",
                "timing": "delayed"
            }
        else:
            # Match rhythm
            return {
                "response_sequence": ["1", "1", "2"],  # jab-jab-cross
                "strategy": "rhythm-match",
                "timing": "counter"
            }
    
    @staticmethod
    def punch_id_to_name(punch_id):
        """Map punch ID to name."""
        mapping = {
            "1": "jab",
            "2": "cross",
            "3": "left_hook",
            "4": "right_hook",
            "5": "uppercut",
            "6": "hook"
        }
        return mapping.get(str(punch_id), "unknown")
    
    @staticmethod
    def punch_name_to_id(punch_name):
        """Map punch name to ID (1-6) or None."""
        mapping = {
            "jab": "1",
            "cross": "2",
            "left_hook": "3",
            "right_hook": "4",
            "left_uppercut": "5",
            "right_uppercut": "6",
        }
        return mapping.get(punch_name.lower(), None)


# Example usage
if __name__ == "__main__":
    engine = DecisionTreeEngine()
    
    # Test combo
    test_combo = {
        "sequence": ["jab", "cross", "left_hook"],
        "num_punches": 3,
        "duration": 1.2,
        "punches": []
    }
    
    for style in ["aggressive", "defensive", "balanced"]:
        print(f"\n{style.upper()} response:")
        decision = engine.decide(style, test_combo)
        print(f"  Sequence: {decision['response_sequence']}")
        print(f"  Strategy: {decision['strategy']}")
        print(f"  Timing: {decision['timing']}")
