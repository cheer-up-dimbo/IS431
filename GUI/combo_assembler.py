#!/usr/bin/env python3
"""
ComboAssembler: Ingests punch events and emits combo dictionaries when user returns to idle.
"""
import time


class ComboAssembler:
    """
    Assembles punch sequences into combos and calls a callback when combo completes.
    
    A combo is considered complete when:
    - An 'idle' move is detected
    - Timeout occurs (no new punch within debounce window)
    - Max combo length (8) is reached
    """
    
    def __init__(self, on_combo_callback, debounce_sec=1.5, max_combo_length=8):
        """
        Args:
            on_combo_callback: Function to call with combo_dict when combo completes
            debounce_sec: Time in seconds to wait before considering combo finished
            max_combo_length: Maximum number of punches in a combo
        """
        self.on_combo = on_combo_callback
        self.debounce_sec = debounce_sec
        self.max_combo_length = max_combo_length
        
        # Current combo state
        self.current_combo = []
        self.last_event_time = None
        self.combo_start_time = None
    
    def ingest_event(self, event):
        """
        Process an incoming event.
        
        Args:
            event: dict with keys {t, move, stance, distance, conf (optional)}
        """
        move = event.get("move", "").lower()
        timestamp = event.get("t", time.time())
        
        # Check if we should finalize current combo due to timeout
        if self.last_event_time is not None:
            time_since_last = timestamp - self.last_event_time
            if time_since_last > self.debounce_sec and len(self.current_combo) > 0:
                self._finalize_combo()
        
        # If idle, finalize any active combo and reset
        if move == "idle":
            if len(self.current_combo) > 0:
                self._finalize_combo()
            self.last_event_time = timestamp
            return
        
        # Otherwise, it's a punch - add to combo
        punch_event = {
            "t": timestamp,
            "punch": move,
            "stance": event.get("stance", "unknown"),
            "distance": event.get("distance", "unknown"),
        }
        if "conf" in event:
            punch_event["conf"] = event["conf"]
        
        # Start new combo if this is first punch
        if len(self.current_combo) == 0:
            self.combo_start_time = timestamp
        
        self.current_combo.append(punch_event)
        self.last_event_time = timestamp
        
        # Check if we've hit max combo length
        if len(self.current_combo) >= self.max_combo_length:
            self._finalize_combo()
    
    def _finalize_combo(self):
        """Emit the current combo and reset state."""
        if len(self.current_combo) == 0:
            return
        
        combo_dict = {
            "combo_start": self.combo_start_time,
            "combo_end": self.last_event_time,
            "duration": self.last_event_time - self.combo_start_time,
            "num_punches": len(self.current_combo),
            "punches": self.current_combo.copy(),
            "sequence": [p["punch"] for p in self.current_combo],
        }
        
        # Call the callback
        self.on_combo(combo_dict)
        
        # Reset state
        self.current_combo = []
        self.combo_start_time = None
    
    def check_timeout(self):
        """
        Manually check if timeout has occurred. 
        Call this periodically if events may stop coming.
        """
        if self.last_event_time is None or len(self.current_combo) == 0:
            return
        
        time_since_last = time.time() - self.last_event_time
        if time_since_last > self.debounce_sec:
            self._finalize_combo()
    
    def force_finalize(self):
        """Force finalization of current combo (e.g., on shutdown)."""
        self._finalize_combo()


# Example usage
if __name__ == "__main__":
    def print_combo(combo):
        print(f"\n🥊 COMBO DETECTED!")
        print(f"   Sequence: {' → '.join(combo['sequence'])}")
        print(f"   Duration: {combo['duration']:.2f}s")
        print(f"   Punches: {combo['num_punches']}")
        print(f"   Details: {combo}")
    
    assembler = ComboAssembler(on_combo_callback=print_combo, debounce_sec=1.5)
    
    # Simulate some events
    test_events = [
        {"t": 1.0, "move": "jab", "stance": "orthodox", "distance": "far", "conf": 0.92},
        {"t": 1.2, "move": "cross", "stance": "orthodox", "distance": "far", "conf": 0.88},
        {"t": 1.5, "move": "left_hook", "stance": "orthodox", "distance": "close", "conf": 0.85},
        {"t": 3.5, "move": "idle", "stance": "unknown", "distance": "unknown", "conf": 0.95},
        {"t": 5.0, "move": "jab", "stance": "southpaw", "distance": "mid", "conf": 0.90},
        {"t": 5.3, "move": "jab", "stance": "southpaw", "distance": "mid", "conf": 0.91},
        {"t": 7.0, "move": "idle", "stance": "unknown", "distance": "unknown", "conf": 0.93},
    ]
    
    print("Processing events...")
    for event in test_events:
        print(f"Event: {event['move']} at t={event['t']}")
        assembler.ingest_event(event)
    
    print("\nDone!")
