const guiPerformanceTestingEl = document.getElementById('gui-performance-testing');

if (guiPerformanceTestingEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Metric', width: '30%' },
      { name: 'Target', width: '20%' },
      { name: 'Measured', width: '20%' },
      { name: 'Status', width: '30%' }
    ],
    data: [
      ['App Startup Time', '< 3s', '2.1s', '✅ Pass (30% under target)'],
      ['Page Transition', '< 500ms', '180-250ms', '✅ Pass (50-64% under target)'],
      ['Arduino Latency', '< 500ms', '320ms avg', '✅ Pass (36% under target)'],
      ['Database Query', '< 200ms', '45-120ms', '✅ Pass (40-77% under target)'],
      ['Memory Usage', '< 500MB', '180MB', '✅ Pass (64% under target)']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'normal'
      }
    }
  }).render(guiPerformanceTestingEl);
}
