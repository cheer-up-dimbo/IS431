const guiFrameworkComparisonEl = document.getElementById('gui-framework-comparison');

if (guiFrameworkComparisonEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Framework', width: '15%' },
      { name: 'Pros', width: '30%' },
      { name: 'Cons', width: '30%' },
      { name: 'Decision', width: '25%' }
    ],
    data: [
      [
        'PySide6 (Qt for Python)',
        'Native on Jetson Nano, mature touchscreen support, extensive Qt documentation, builds on existing Python knowledge',
        'Large framework footprint, steeper learning curve than lightweight alternatives',
        gridjs.html('<span style="color:#2e7d32; font-weight:bold;">Selected</span>')
      ],
      [
        'Tkinter',
        'Included with Python, minimal setup, simple API',
        'Limited widget set, poor touchscreen support, dated visual appearance, limited layout control',
        gridjs.html('<span style="color:#c62828; font-weight:bold;">Rejected</span>')
      ],
      [
        'Kivy',
        'Designed for touch interfaces, cross-platform, modern look',
        'Not pre-installed on Jetson Nano, smaller community, unfamiliar API requiring additional learning time',
        gridjs.html('<span style="color:#c62828; font-weight:bold;">Rejected</span>')
      ],
      [
        'Web-based (Flask + Browser)',
        'Flexible UI with HTML/CSS, responsive design, familiar web technologies',
        'Requires running a local web server, adds browser dependency, latency concerns on resource-constrained hardware',
        gridjs.html('<span style="color:#c62828; font-weight:bold;">Rejected</span>')
      ]
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: { 'white-space': 'normal' }
    }
  }).render(guiFrameworkComparisonEl);
}
