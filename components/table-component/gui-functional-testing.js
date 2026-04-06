const guiFunctionalTestingEl = document.getElementById('gui-functional-testing');

if (guiFunctionalTestingEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Feature', width: '20%' },
      { name: 'Test Scenario', width: '35%' },
      { name: 'Expected Result', width: '25%' },
      { name: 'Status', width: '20%' }
    ],
    data: [
      ['User Login', 'Login with correct credentials', 'Access granted, navigate to main menu', 'Pass'],
      ['User Login', 'Login with incorrect password', 'Error message, remain on login page', 'Pass'],
      ['Combo Curriculum', 'Complete 5 sessions of "Jab" with score >= 3.0', 'Jab marked as mastered, unlock next combo', 'Pass'],
      ['Combo Curriculum', 'Complete all 15 beginner combos', 'Unlock intermediate level option', 'Pass'],
      ['Combo Session Setup', 'Configure round count, work/rest time, playback speed', 'Session runs with configured parameters', 'Pass'],
      ['Proficiency Assessment', 'Complete 6-question checklist on signup', 'System suggests correct proficiency level based on total score', 'Pass']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: { 'white-space': 'normal' }
    }
  }).render(guiFunctionalTestingEl);
}
