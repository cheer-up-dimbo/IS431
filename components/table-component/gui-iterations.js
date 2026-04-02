const guiIterationsEl = document.getElementById('gui-iterations');

if (guiIterationsEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Iteration', width: '12%' },
      { name: 'Period', width: '18%' },
      { name: 'Objective', width: '35%' },
      { name: 'Key Outcome', width: '35%' }
    ],
    data: [
      ['1', 'Weeks 1-2 (Dec)', 'Application shell, PySide6 validation on Jetson Nano', 'QStackedWidget navigation confirmed, touch targets validated at 80x60px minimum'],
      ['2', 'Weeks 3-4 (Jan)', 'User management, login/signup, data persistence', 'Multi-user support functional, cascade deletion implemented, zero data mixing confirmed'],
      ['3', 'Weeks 5-7 (Jan-Feb)', 'Combo curriculum system, training session UI', '50-combo library loaded, mastery-based progression algorithm operational, session flow complete'],
      ['4', 'Weeks 8-10 (Feb-Mar)', 'Performance testing modes, Arduino serial integration', 'Power/Stamina/Reaction tests functional, multi-mode serial protocol working'],
      ['5', 'Weeks 11-13 (Mar)', 'Sparring mode, proficiency assessment, navigation stack', 'Markov chain combo generation, 6-question proficiency checklist, automatic back button history'],
      ['6', 'Weeks 14-15 (Apr)', 'AI coaching integration, polish, validation testing', 'LLM fallback architecture in place, full functional and performance validation pass completed']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'normal'
      }
    }
  }).render(guiIterationsEl);
}