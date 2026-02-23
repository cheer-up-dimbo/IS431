const guiFunctionalRequirementsEl = document.getElementById('gui-functional-requirements');

if (guiFunctionalRequirementsEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Category', width: '20%' },
      { name: 'Requirement', width: '40%' },
      { name: 'Priority', width: '15%' },
      { name: 'Rationale', width: '25%' }
    ],
    data: [
      ['User Management', 'Multi-user support with individual profiles', 'High', 'BoxBot may be shared in gym/home setting'],
      ['Training Modes', 'Minimum 3 distinct modes: Combinations, Performance, Sparring', 'High', 'Addresses different training objectives'],
      ['Data Persistence', 'Store user progress, test results, training history', 'High', 'Essential for progress tracking and motivation'],
      ['Real-time Feedback', 'Display sensor/CV data with <500ms latency', 'High', 'Immediate feedback critical for motor learning'],
      ['Hardware Control', 'Reliable communication with Arduino, motors, CV system', 'High', 'Core system integration requirement'],
      ['AI Feedback', 'Optional intelligent coaching feedback', 'Medium', 'Enhances user experience but not critical for MVP']
    ],
    search: false,
    sort: true,
    pagination: false,
    style: {
      table: {
        'white-space': 'normal'
      }
    }
  }).render(guiFunctionalRequirementsEl);
}
