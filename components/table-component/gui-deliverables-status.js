const guiDeliverablesStatusEl = document.getElementById('gui-deliverables-status');

if (guiDeliverablesStatusEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Requirement', width: '24%' },
      { name: 'Status', width: '16%' },
      { name: 'Evidence', width: '60%' }
    ],
    data: [
      ['GUI-1: Ease of Use', 'Achieved', 'Hierarchical page stack navigation ensures intuitive drill-down and consistent back-button behaviour\nLarge touch targets (minimum 60px) for reliable padding-based screen interaction\nClear visual hierarchy with dark theme and color-coded punch types\nPattern lock authentication designed for padding-based input'],
      ['GUI-3: Structured Training Progression', 'Achieved', '50-combo curriculum implemented across Beginner, Intermediate, and Advanced tiers\nGroup-based sequential progression with mastery threshold (3.0/5.0 over 5 sessions)\nProficiency assessment on signup sets initial difficulty tier'],
      ['GUI-4: Real-Time Session Data', 'Achieved', 'Combo prompts displayed in real-time during training sessions\nRound timers, rest timers, and performance metrics visible during active sessions\nPost-session results pages with scoring and trend indicators']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: { 'white-space': 'normal' }
    }
  }).render(guiDeliverablesStatusEl);
}
