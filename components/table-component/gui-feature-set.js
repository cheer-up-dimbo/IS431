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
      ['Training', 'Free Training', 'Open reactive session where the robot counters user pad hits with no structured drills'],
      ['Sparring', 'Markov Chain Combos', 'Procedurally generated punch sequences with five AI opponent styles (Boxer, Brawler, Counter-Puncher, Pressure, Switch)'],
      ['Sparring', 'Weakness Tracking', 'User defense rates tracked per punch type; AI biases attacks toward weak areas'],
      ['Performance', 'Power Test', 'Peak and average punch power measurement via IMU accelerometer'],
      ['Performance', 'Stamina Test', '2-minute endurance test tracking total punches, punch rate, fatigue percentage'],
      ['Performance', 'Reaction Test', 'Reaction time measurement using CV pose estimation with tier classification'],
      ['Performance', 'History Hub', 'Unified history interface consolidating all training types with mode filtering'],
      ['User Management', 'Pattern Lock', '3x3 grid authentication with 48px hit radius for gloved-hand input'],
      ['User Management', 'Proficiency Assessment', '6-question checklist on signup producing Beginner/Intermediate/Advanced classification'],
      ['User Management', 'Per-User Database', 'Complete data isolation via separate SQLite database files per user'],
      ['Companion', 'Phone Dashboard', 'Vue 3 web app served over WiFi AP for session history, analytics, remote control, and AI chat'],
      ['Companion', 'Quick Start Presets', 'Saved training configurations for one-tap session launch from touchscreen or phone'],
      ['Companion', 'Coach Station', 'Group circuit training mode supporting up to 30 rotating participants'],
      ['AI', 'AI Coaching Chat', 'Post-session feedback via local LLM (Qwen 2.5 3B) with hardcoded fallback'],
      ['Gamification', 'XP and Ranks', 'Experience points per session with six progression ranks from Novice to Elite'],
      ['Gamification', 'Achievements', '12 milestone badges tracking training accomplishments'],
      ['Gamification', 'Training Streaks', 'Consecutive training day counter with bonus XP multipliers'],
      ['System', 'ROS 2 Bridge', 'GuiBridge QThread connecting GUI to ROS nodes for real-time data flow'],
      ['System', 'Design System', 'Centralized theme.py with dark theme, Inter font, 60px touch targets, punch-type color coding']
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