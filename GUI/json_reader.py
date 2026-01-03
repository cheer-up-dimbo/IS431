import sys
import json
import subprocess
from datetime import datetime

def process_json_message(json_str):
    """Process and display JSON messages from the GUI."""
    try:
        data = json.loads(json_str)
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Check what type of message it is
        if "action" in data:
            action = data["action"]
            print(f"[{timestamp}] ACTION: {action}")
            
            if action == "Pause":
                print("  -> Training paused")
            elif action == "Resume":
                print("  -> Training resumed")
            elif action == "Stop":
                print("  -> Training stopped by user")
            elif action == "Log Training Session":
                print("  -> Training session completed successfully!")
                
        elif "mode" in data:
            mode = data["mode"]
            
            if mode == "Self-Select":
                sequence = data.get("sequence", "N/A")
                seq_index = data.get("sequence_index", "N/A")
                print(f"[{timestamp}] MODE: Self-Select")
                print(f"  -> Sequence: {sequence}")
                print(f"  -> Index: {seq_index}")
                
            elif mode == "Battle":
                battle_style = data.get("battle_style", "N/A")
                print(f"[{timestamp}] MODE: Battle")
                print(f"  -> Battle Style: {battle_style}")
                
            elif "Punch-Combination" in mode:
                print(f"[{timestamp}] MODE: {mode}")
                
            else:
                print(f"[{timestamp}] MODE: {mode}")
                
        else:
            # Unknown format
            print(f"[{timestamp}] UNKNOWN MESSAGE: {json_str}")
            
        print()  # Empty line for readability
        
    except json.JSONDecodeError:
        # Not a JSON string, ignore or log
        pass
    except Exception as e:
        print(f"Error processing message: {e}")


def read_gui_output():
    """Run the GUI and read its JSON output in real-time."""
    print("=" * 60)
    print("JSON Message Reader - Boxing Training App")
    print("=" * 60)
    print("Starting GUI and monitoring JSON messages...\n")
    
    # Path to the main GUI script
    gui_script = r"c:\Users\Zakir\OneDrive - National University of Singapore\Desktop\NUS Semesters\Y4S1\CDE4301\GitHub\IS431\GUI\main_gui_2.py"
    
    try:
        # Run the GUI as a subprocess
        process = subprocess.Popen(
            [sys.executable, gui_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Read output line by line
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            if line:
                # Try to process as JSON
                if line.startswith('{') and line.endswith('}'):
                    process_json_message(line)
                else:
                    # Non-JSON output (debug messages, etc.)
                    print(f"[DEBUG] {line}")
        
        process.wait()
        print("\nGUI has been closed.")
        
    except FileNotFoundError:
        print(f"Error: Could not find the GUI script at {gui_script}")
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
        if process:
            process.terminate()
    except Exception as e:
        print(f"Error running GUI: {e}")


def read_from_stdin():
    """Read JSON strings from standard input (for testing)."""
    print("=" * 60)
    print("JSON Message Reader - Stdin Mode")
    print("=" * 60)
    print("Paste JSON strings or pipe output here (Ctrl+C to exit)\n")
    
    try:
        for line in sys.stdin:
            line = line.strip()
            if line and line.startswith('{') and line.endswith('}'):
                process_json_message(line)
    except KeyboardInterrupt:
        print("\n\nStopped by user.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--stdin":
        # Read from stdin for testing
        read_from_stdin()
    else:
        # Run GUI and monitor output
        read_gui_output()
