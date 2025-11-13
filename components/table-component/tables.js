 // Robot Intelligence Table
  new gridjs.Grid({
    columns: ["Parameter", "Specification", "Rationale"],
    data: [
      ["System Latency", "≤ 100 ms", "Ensures minimal delay between user motion and robot reaction"],
      ["Reaction Time", "≈ 150 ms", "Matches average human defensive response time"],
      ["Minimum Frame Rate", "≥ 7 FPS", "Maintains smooth tracking for reliable pose estimation"],
    ],
  }).render(document.getElementById("table-robot-intelligence"));
  