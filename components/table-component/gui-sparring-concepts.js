(function() {
  var el = document.getElementById('gui-sparring-concepts');
  if (!el) return;
  el.innerHTML = '<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:0.92rem;">' +
    '<thead><tr style="background:#f0f0f0;">' +
    '<th style="padding:10px;border:1px solid #ddd;width:20%;">Concept</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:45%;">Description</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:35%;">Reason for Decision</th>' +
    '</tr></thead><tbody>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Hardcoded Sequences</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Pre-defined fixed combos stored in a list and cycled in order during sparring rounds.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Predictable after a few sessions. Users memorise the pattern and the training value diminishes. Does not adapt to user weaknesses.</td></tr>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Uniform Random Generation</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Each punch is generated independently with equal probability across all punch types. No state or memory between punches.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Produces sequences that lack natural boxing flow. A jab naturally leads to a cross, not a random uppercut. The output feels mechanical rather than stylistically coherent.</td></tr>' +
    '<tr style="background:#e8f5e9;">' +
    '<td style="padding:10px;border:1px solid #ddd;font-weight:bold;">Markov Chain with Style Matrices</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Each boxing style (Pressure Fighter, Counter Puncher, Infighter, Out-Boxer, Random) defines a transition probability matrix over punch types. The next punch depends on the current punch, producing naturalistic sequences. A weakness bias parameter blends in the user\'s weakness profile over time, increasing the probability of punches the user struggles with. A safety limit of six punches per combo prevents excessively long sequences.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Produces stylistically coherent, unpredictable sequences that adapt to the user. Each style plays differently, adding variety across sessions. The Markov property keeps implementation simple while capturing realistic punch transitions.</td></tr>' +
    '</tbody></table>';
})();
