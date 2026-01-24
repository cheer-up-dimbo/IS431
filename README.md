# Basic template for iDP report

## Tools used
- Grid.js for generating table
- Shoelace for custom web-components

## Windows Notes
- Camera backend: On Windows, the app uses DirectShow for stability. If the camera fails to open, check Windows privacy settings (Privacy & security → Camera) and close other apps using the camera.
- Model path: Paths are resolved relative to the repo root; run from the project folder or use absolute paths. The script resolves the model at `models/yolo11s-pose.pt` automatically.
- Stats file: Session stats persist in `boxbunny_stats.json` at the repo root using UTF‑8 encoding.
- Running the trainer:
	- PowerShell (from repo root):

```powershell
python GUI/reaction_time/reaction_time_runner.py
# or specify Anaconda python explicitly if needed
& C:/Users/Zakir/anaconda3/python.exe "c:/Users/Zakir/OneDrive - National University of Singapore/Desktop/NUS Semesters/Y4S1/CDE4301/GitHub/IS431/GUI/reaction_time/reaction_time_runner.py"
```

- Key controls: `SPACE` start, `R` replay, `G` settings, `+/-` sensitivity, `Q` quit.
