const guiFeatureSetEl = document.getElementById('gui-feature-set');

if (guiFeatureSetEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Category', width: '20%' },
      { name: 'Feature', width: '30%' },
      { name: 'Description', width: '50%' }
    ],
    data: [
      ['Training', 'Combo Curriculum', '50 punch combinations across Beginner, Intermediate, and Advanced levels with mastery-based progression'],
      ['Training', 'Training Session', 'Configurable rounds, work/rest timers, speed settings, real-time combo prompts'],
      ['Training', 'Self-Select Mode', 'User builds a custom punch sequence from individual punch buttons'],
      ['Training', 'AI Combo Chat', 'Post-session feedback via local LLM (Qwen 2.5 3B) with hardcoded fallback'],
      ['Performance', 'Power Test', 'Peak and average punch power measurement via Arduino MPU6050 accelerometer'],
      ['Performance', 'Stamina Test', '2-minute endurance test tracking total punches, punch rate, fatigue percentage'],
      ['Performance', 'Reaction Test', 'Reaction time measurement using the computer vision subsystem'],
      ['Performance', 'History Tracking', 'Per-user historical results stored in SQLite, viewable across sessions'],
      ['Sparring', 'Markov Chain Combos', 'Procedurally generated punch sequences biased by user weakness profile'],
      ['Sparring', 'Proficiency Gate', 'Access restricted to Intermediate and Advanced users via proficiency assessment'],
      ['User Management', 'Login/Signup', 'Per-user accounts with SHA-256 hashed credentials'],
      ['User Management', 'Proficiency Assessment', '6-question checklist on signup producing Beginner/Intermediate/Advanced classification']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'normal'
      }
    }
  }).render(guiFeatureSetEl);
}