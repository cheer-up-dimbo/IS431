const guiFunctionalTestingEl = document.getElementById('gui-functional-testing');

if (guiFunctionalTestingEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Feature', width: '20%' },
      { name: 'Test Scenario', width: '30%' },
      { name: 'Expected Result', width: '25%' },
      { name: 'Status', width: '25%' }
    ],
    data: [
      ['User Login', 'Login with correct credentials', 'Access granted, navigate to main menu', '✅ Pass'],
      ['User Login', 'Login with incorrect password', 'Error message, remain on login page', '✅ Pass'],
      ['Combo Curriculum', 'Complete 5 sessions of "Jab" with score ≥3.0', 'Jab marked as mastered, unlock next combo', '✅ Pass'],
      ['Combo Curriculum', 'Complete all 15 beginner combos', 'Unlock intermediate level option', '✅ Pass'],
      ['Power Test', 'Punch Arduino sensor 10 times', 'Display peak power, avg power, count', '✅ Pass'],
      ['Stamina Test', 'Run 2-minute test', 'Display total punches, rates, fatigue %, score', '✅ Pass'],
      ['Navigation Stack', 'Navigate: Menu → Perf → Stamina → Result → History → Back × 4', 'Return through: History → Result → Stamina → Perf → Menu', '✅ Pass'],
      ['Multi-User', 'User A trains, logout, User B trains', 'User B sees only their own progress', '✅ Pass']
    ],
    search: false,
    sort: true,
    pagination: false,
    style: {
      table: {
        'white-space': 'normal'
      }
    }
  }).render(guiFunctionalTestingEl);
}
