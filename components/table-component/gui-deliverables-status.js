const guiDeliverablesStatusEl = document.getElementById('gui-deliverables-status');

if (guiDeliverablesStatusEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Requirement', width: '35%' },
      { name: 'Status', width: '15%' },
      { name: 'Evidence', width: '50%' }
    ],
    data: [
      ['Ease of Use (Primary Requirement)', '✅ Achieved', 'Maximum 3 clicks to any feature\nLarge touch targets (80x60px minimum)\nClear visual hierarchy\nConsistent navigation pattern'],
      ['Multi-User Support', '✅ Achieved', 'Login/signup system functional\nPer-user data isolation via separate database files\nTested with 5 users, zero data mixing'],
      ['Combo Training', '✅ Achieved', '50-combo curriculum implemented\nProgressive difficulty (Beginner → Intermediate → Advanced)\nMastery-based progression validated'],
      ['Performance Testing', '✅ Achieved', 'Power test: Arduino MPU6050 integration working\nStamina test: 2-minute endurance with metrics\nReaction test: CV-based detection integrated'],
      ['Hardware Integration', '✅ Achieved', 'Arduino serial protocol (multi-mode) functional\nCV system integration ready\nRobotic arm control interface implemented'],
      ['Data Persistence', '✅ Achieved', 'SQLite databases per user\nCombo progress tracked across sessions\nPerformance history stored and retrievable'],
      ['Real-time Feedback', '✅ Achieved', 'Arduino data latency: 320ms average (<500ms target)\nCV scoring displayed immediately post-round\nUI responsive to user actions']
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
