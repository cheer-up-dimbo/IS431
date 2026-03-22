const guiMoscowEl = document.getElementById('gui-moscow');

if (guiMoscowEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Priority', width: '30%' },
      { name: 'Features', width: '70%' }
    ],
    data: [
      ['Must Have', 'User authentication, navigation framework, combination training flow, database schema, Arduino sensor integration'],
      ['Should Have', 'Smart combo curriculum, performance history tracking, real-time feedback, settings management'],
      ['Could Have', 'AI coaching feedback, progress charts, customisable training programs, data export'],
      ['Will Not Have (this time)', 'Cloud sync, mobile companion app, social leaderboards, video recording']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'pre-wrap'
      }
    }
  }).render(guiMoscowEl);
}
