const guiNavConceptsEl = document.getElementById('gui-nav-concepts');

if (guiNavConceptsEl) {
  const greenBg = 'background:#e8f5e9; width:100%; display:block; padding:8px; margin:0; box-sizing:border-box;';
  const redBg = 'background:#ffebee; width:100%; display:block; padding:8px; margin:0; box-sizing:border-box;';

  new gridjs.Grid({
    columns: [
      { name: 'Concept', width: '20%' },
      { name: 'Description', width: '40%' },
      { name: 'Evaluation', width: '40%' }
    ],
    data: [
      [
        gridjs.html('<div style="' + redBg + '">Flat Menu</div>'),
        gridjs.html('<div style="' + redBg + '">All pages accessible from a single top-level menu with no hierarchy</div>'),
        gridjs.html('<div style="' + redBg + '">Does not scale beyond 8-10 items. With 44 pages, the menu becomes unusable on a 10-inch touchscreen.</div>')
      ],
      [
        gridjs.html('<div style="' + redBg + '">Tab-Based Navigation</div>'),
        gridjs.html('<div style="' + redBg + '">Persistent tab bar at the top or bottom of the screen, each tab leading to a feature category</div>'),
        gridjs.html('<div style="' + redBg + '">Tab bar consumes screen space on every page. On a small display, this reduces the content area significantly. Tab count is also limited before horizontal scrolling is needed.</div>')
      ],
      [
        gridjs.html('<div style="' + greenBg + 'font-weight:bold;">Hierarchical Page Stack</div>'),
        gridjs.html('<div style="' + greenBg + '">Tree-structured navigation with a central QStackedWidget. Users drill down from the main menu through category pages to feature pages. A navigation stack tracks history for automatic back-button behaviour.</div>'),
        gridjs.html('<div style="' + greenBg + '">Scales to any number of pages without UI clutter. Full screen available for content on every page. The stack ensures consistent back-button behaviour regardless of entry path.</div>')
      ]
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: { 'white-space': 'normal' }
    }
  }).render(guiNavConceptsEl);
}
