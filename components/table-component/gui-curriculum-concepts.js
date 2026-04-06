(function() {
  var el = document.getElementById('gui-curriculum-concepts');
  if (!el) return;
  el.innerHTML = '<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:0.92rem;">' +
    '<thead><tr style="background:#f0f0f0;">' +
    '<th style="padding:10px;border:1px solid #ddd;width:20%;">Concept</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:45%;">Description</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:35%;">Reason for Decision</th>' +
    '</tr></thead><tbody>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Spaced Repetition (Anki-style)</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Schedule combos based on forgetting curves, inspired by the Ebbinghaus spacing effect. Each combo would reappear at increasing intervals after successful recall.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">While spaced practice benefits motor skill learning (Shea et al., 2000), the Anki card-review model assumes discrete recall events. Boxing training is session-based and continuous; users do not "recall" a combo in isolation but execute it within a round. The scheduling model did not map to the session structure.</td></tr>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Random Rotation</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Present combos randomly from the current difficulty tier with no fixed order or grouping.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">No structured progression path. Users could repeatedly encounter combos they have already mastered while rarely seeing new ones. No mastery tracking or unlock mechanism.</td></tr>' +
    '<tr style="background:#e8f5e9;">' +
    '<td style="padding:10px;border:1px solid #ddd;font-weight:bold;">Group-Based Sequential Progression</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Combos are grouped by technique family. The system rotates through the current group until a mastery threshold is met (average score of 3.0 out of 5.0 over the last 5 sessions), then unlocks the next group. This mirrors how boxing coaches structure pad work: drill a technique family until the boxer is comfortable, then layer on the next.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Provides clear progression, measurable mastery, and a structure that aligns with real coaching practice. The threshold and window size are configurable.</td></tr>' +
    '</tbody></table>';
})();
