# Transition Matrices for Sparring Combos
# Notation:
# - Each style is a dictionary with states as keys.
# - "start" defines the opening move.
# - Each punch number ("1", "2", "3", "4", "5", "6", "3b", "2b") is a state defining what comes next.
# - "end" is a special value meaning stop the combo here.
# - Values in each state are dictionaries of {next_punch: probability} that sum to 1.0.
# - Punch notation:
#   "1" = jab, "2" = cross, "3" = lead hook, "4" = rear hook,
#   "5" = lead uppercut, "6" = rear uppercut,
#   "3b" = lead hook to body, "2b" = cross to body

STYLE_TRANSITION_MATRICES = {
    # Pressure Fighter: Aggressive, prefers combos, low end probability early, heavy on hooks and body shots
    "Pressure Fighter": {
        "start": {"1": 0.4, "3": 0.3, "3b": 0.2, "end": 0.1},
        "1": {"2": 0.3, "3": 0.3, "end": 0.4},
        "2": {"3": 0.4, "4": 0.3, "end": 0.3},
        "3": {"5": 0.4, "3b": 0.3, "end": 0.3},
        "3b": {"4": 0.5, "end": 0.5},
        "4": {"6": 0.4, "end": 0.6},
        "5": {"6": 0.5, "end": 0.5},
        "6": {"end": 1.0},
    },

    # Counter Puncher: Precise, higher end probability, waits and counters, single punches are common
    "Counter Puncher": {
        "start": {"1": 0.3, "2": 0.3, "end": 0.4},
        "1": {"end": 0.6, "2": 0.4},
        "2": {"end": 0.5, "3": 0.3, "4": 0.2},
        "3": {"end": 0.7, "5": 0.3},
        "4": {"end": 0.8, "6": 0.2},
        "5": {"end": 0.9, "6": 0.1},
        "6": {"end": 1.0},
    },

    # Infighter: Close range, uppercuts and hooks, medium length combos
    "Infighter": {
        "start": {"5": 0.4, "3": 0.3, "4": 0.2, "end": 0.1},
        "5": {"6": 0.4, "3": 0.3, "end": 0.3},
        "3": {"4": 0.4, "5": 0.3, "end": 0.3},
        "4": {"6": 0.5, "end": 0.5},
        "6": {"end": 1.0},
    },

    # Out-Boxer: Jab heavy, lots of single jabs, occasional combos, keeps distance
    "Out-Boxer": {
        "start": {"1": 0.6, "2": 0.2, "end": 0.2},
        "1": {"1": 0.5, "2": 0.3, "end": 0.2},
        "2": {"1": 0.4, "end": 0.6},
        "3": {"end": 0.8, "1": 0.2},
        "4": {"end": 0.8, "2": 0.2},
        "5": {"end": 0.9, "1": 0.1},
        "6": {"end": 0.9, "2": 0.1},
    },

    # Random: Balanced across all punches, medium end probability
    "Random": {
        "start": {"1": 0.142, "2": 0.142, "3": 0.142, "4": 0.142, "5": 0.142, "6": 0.142, "end": 0.148},
        "1": {"2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2, "end": 0.2},
        "2": {"1": 0.2, "3": 0.2, "4": 0.2, "5": 0.2, "end": 0.2},
        "3": {"1": 0.2, "2": 0.2, "4": 0.2, "5": 0.2, "end": 0.2},
        "4": {"1": 0.2, "2": 0.2, "3": 0.2, "5": 0.2, "end": 0.2},
        "5": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "end": 0.2},
        "6": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "end": 0.2},
    },
}