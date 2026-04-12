const guiIterationsEl = document.getElementById('gui-iterations');

if (guiIterationsEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Iteration', width: '16%' },
      { name: 'Period', width: '18%' },
      { name: 'Objective', width: '33%' },
      { name: 'Key Outcome', width: '33%' }
    ],
    data: [
      ['Iteration 1', 'Weeks 1-2 (Dec)', 'Application shell, PySide6 validation on Jetson Nano', 'QStackedWidget navigation confirmed, basic page transitions working on target hardware'],
      ['Iteration 2', 'Weeks 3-5 (Jan)', 'Combo curriculum system, training session UI', '50-combo library loaded, mastery-based progression algorithm operational, session flow complete'],
      ['Iteration 3', 'Weeks 6-8 (Jan-Feb)', 'Sparring mode, proficiency assessment', 'Markov chain combo generation working, 6-question proficiency checklist refined through user interviews at the Robotics Meets AI Showcase; assessment producing reliable level classification'],
      ['Iteration 4', 'Weeks 9-11 (Feb-Mar)', 'Performance testing modes, sensor integration', 'Power/Stamina/Reaction tests functional, multi-mode serial protocol working'],
      ['Iteration 5', 'Weeks 12-13 (Mar)', 'Navigation stack, AI coaching integration, polish', 'Automatic back button history, LLM fallback architecture in place'],
      ['Iteration 6', 'Weeks 14-15 (Apr)', 'User management, validation testing', 'Login/signup flow, per-user data isolation, full functional validation pass completed'],
      ['Iteration 7', 'Weeks 16-18 (Apr)', 'ROS 2 integration, phone dashboard, design system overhaul', 'GuiBridge connecting GUI to ROS nodes, Vue 3 phone dashboard via WiFi AP, centralized theme system, pattern lock authentication, coach station, free training mode']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: { 'white-space': 'normal' }
    }
  }).render(guiIterationsEl);
}
