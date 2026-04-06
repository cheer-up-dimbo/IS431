const guiFrameworkComparisonEl = document.getElementById('gui-framework-comparison');

if (guiFrameworkComparisonEl) {
  const greenBg = 'background:#e8f5e9; width:100%; display:block; padding:8px; margin:0; box-sizing:border-box;';
  const redBg = 'background:#ffebee; width:100%; display:block; padding:8px; margin:0; box-sizing:border-box;';

  new gridjs.Grid({
    columns: [
      { name: 'Framework', width: '20%' },
      { name: 'Pros', width: '40%' },
      { name: 'Cons', width: '40%' }
    ],
    data: [
      [
        gridjs.html('<div style="' + greenBg + 'font-weight:bold;">PySide6 (Qt for Python)</div>'),
        gridjs.html('<div style="' + greenBg + '">Native on Jetson Nano, mature touchscreen support, extensive Qt documentation, builds on existing Python knowledge</div>'),
        gridjs.html('<div style="' + greenBg + '">Large framework footprint, steeper learning curve than lightweight alternatives</div>')
      ],
      [
        gridjs.html('<div style="' + redBg + '">Tkinter</div>'),
        gridjs.html('<div style="' + redBg + '">Included with Python, minimal setup, simple API</div>'),
        gridjs.html('<div style="' + redBg + '">Limited widget set, poor touchscreen support, dated visual appearance, limited layout control</div>')
      ],
      [
        gridjs.html('<div style="' + redBg + '">Kivy</div>'),
        gridjs.html('<div style="' + redBg + '">Designed for touch interfaces, cross-platform, modern look</div>'),
        gridjs.html('<div style="' + redBg + '">Not pre-installed on Jetson Nano, smaller community, unfamiliar API requiring additional learning time</div>')
      ],
      [
        gridjs.html('<div style="' + redBg + '">Web-based (Flask + Browser)</div>'),
        gridjs.html('<div style="' + redBg + '">Flexible UI with HTML/CSS, responsive design, familiar web technologies</div>'),
        gridjs.html('<div style="' + redBg + '">Requires running a local web server, adds browser dependency, latency concerns on resource-constrained hardware</div>')
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
