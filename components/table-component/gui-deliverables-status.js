const guiDeliverablesStatusEl = document.getElementById('gui-deliverables-status');

if (guiDeliverablesStatusEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Requirement', width: '30%' },
      { name: 'Status', width: '15%' },
      { name: 'Evidence', width: '55%' }
    ],
    data: [
      ['Ease of Use (Primary Requirement)', 'Achieved', 'Maximum 3 clicks to any feature\nLarge touch targets (80x60px minimum)\nClear visual hierarchy\nConsistent navigation pattern'],
      ['Combo Training', 'Achieved', '50-combo curriculum implemented\nProgressive difficulty (Beginner, Intermediate, Advanced)\nMastery-based progression validated'],
      ['Performance Testing', 'Achieved', 'Power test: IMU sensor integration working\nStamina test: 2-minute endurance with metrics\nReaction test: CV-based detection integrated'],
      ['Hardware Integration', 'Achieved', 'Sensor serial protocol functional\nCV system integration ready\nRobotic arm control interface implemented']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'pre-wrap'
      }
    }
  }).render(guiDeliverablesStatusEl);
}
