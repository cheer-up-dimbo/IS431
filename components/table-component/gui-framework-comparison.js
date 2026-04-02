const guiFrameworkComparisonEl = document.getElementById('gui-framework-comparison');

if (guiFrameworkComparisonEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Framework', width: '22%' },
      { name: 'Pros', width: '28%' },
      { name: 'Cons', width: '28%' },
      { name: 'Verdict', width: '22%' }
    ],
    data: [
      ['React Native / Flutter\n(Cross-platform mobile frameworks using JavaScript or Dart)', 'Modern and popular\nCross-platform support\nGood documentation', 'Requires learning a new language\nInsufficient time to gain proficiency\nJetson Nano compatibility uncertain', 'Rejected: timeline too short for new language acquisition'],
      ['Tkinter\n(Python built-in GUI library based on Tk)', 'Built into Python, no installation needed\nSimple to learn\nLightweight', 'Dated visual appearance\nLimited styling and theming options\nBasic widget set for complex layouts', 'Rejected: insufficient widget variety for a multi-page training application'],
      ['Kivy\n(Python framework designed for multi-touch applications)', 'Purpose-built for touch interfaces\nModern UI capabilities\nPython-based', 'Smaller community and ecosystem\nUnconventional design paradigm (kv language)\nLess documentation available', 'Considered but not selected: community and documentation risk too high'],
      ['PySide6\n(Qt for Python, official Python bindings for the Qt framework)', 'Professional widget library\nExtensive documentation and community\nPython-based, leveraging existing skills\nProven on ARM/Linux platforms\nNative touchscreen support', 'Steeper learning curve than Tkinter\nLarger deployment footprint', 'Selected: best balance of capability, documentation, and timeline feasibility']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'pre-wrap'
      }
    },
    className: {
      tr: (_, row) => {
        if (!row) return '';
        const verdict = row.cells[3]?.data || '';
        if (verdict.startsWith('Selected')) return 'gridjs-tr-selected';
        if (verdict.startsWith('Considered')) return 'gridjs-tr-considered';
        return 'gridjs-tr-rejected';
      }
    }
  }).render(guiFrameworkComparisonEl);

  // Inject color-coding styles
  const style = document.createElement('style');
  style.textContent = `
    .gridjs-tr-selected td { background-color: #e8f5e9 !important; }
    .gridjs-tr-rejected td { background-color: #ffebee !important; }
    .gridjs-tr-considered td { background-color: #fff8e1 !important; }
  `;
  document.head.appendChild(style);
}
