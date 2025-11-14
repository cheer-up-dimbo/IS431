// Display Parameters Table
new gridjs.Grid({
    columns: ["Parameter", "Specification", "Rationale"],
    data: [
        ["Brightness","≥ 300 nits","According to the LED Screen Brightness Guide (UNIT, n.d.), displays above 300 nits provide clear visibility while avoiding glare, ensuring comfortable long-duration viewing."],
        ["Reaction Time", "≤ 100 ms","Based on findings in a conference paper (Forch, Valentin, Franke, Rauh, & Krems, 2017), a latency of 100 ms or below remains largely imperceptible to users and preserves smooth interaction."]
  ],
}).render(document.getElementById("gui-func-spec"));


  