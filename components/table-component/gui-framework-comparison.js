const guiFrameworkComparisonEl = document.getElementById('gui-framework-comparison');

if (guiFrameworkComparisonEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Framework', width: '15%' },
      { name: 'Pros', width: '30%' },
      { name: 'Cons', width: '30%' },
      { name: 'Verdict', width: '25%' }
    ],
    data: [
      ['React Native / Flutter', '• Modern, popular\n• Cross-platform\n• Good documentation', '• Requires learning JavaScript/Dart\n• Limited time for new language\n• Jetson compatibility uncertain', '❌ Rejected - Timeline too short'],
      ['Tkinter (Python)', '• Built into Python\n• No installation needed\n• Simple to learn', '• Dated appearance\n• Limited styling options\n• Poor touch support', '❌ Rejected - Inadequate for touch UI'],
      ['Kivy (Python)', '• Designed for touch\n• Modern UI\n• Python-based', '• Smaller community\n• Unconventional design paradigm\n• Less documentation', '⚠️ Considered but not selected'],
      ['PySide6 / PyQt6', '• Professional appearance\n• Extensive widget library\n• Python-based\n• Excellent documentation\n• Touch screen support\n• Proven on ARM/Linux', '• Steeper learning curve than Tkinter\n• Larger deployment size', '✅ Selected - Best balance of features and timeline']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'pre-wrap'
      }
    }
  }).render(guiFrameworkComparisonEl);
}
