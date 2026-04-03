const guiNavConceptsEl = document.getElementById('gui-nav-concepts');

if (guiNavConceptsEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Concept', width: '15%' },
      { name: 'Description', width: '30%' },
      { name: 'Evaluation', width: '30%' },
      { name: 'Decision', width: '25%' }
    ],
    data: [
      [
        'Flat Menu',
        'All pages accessible from a single top-level menu with no hierarchy',
        'Does not scale beyond 8-10 items. With 44 pages, the menu becomes unusable on a 10-inch touchscreen.',
        gridjs.html('<span style="color:#c62828; font-weight:bold;">Rejected</span>')
      ],
      [
        'Tab-Based Navigation',
        'Persistent tab bar at the top or bottom of the screen, each tab leading to a feature category',
        'Tab bar consumes screen space on every page. On a small display, this reduces the content area significantly. Tab count is also limited before horizontal scrolling is needed.',
        gridjs.html('<span style="color:#c62828; font-weight:bold;">Rejected</span>')
      ],
      [
        'Hierarchical Page Stack',
        'Tree-structured navigation with a central QStackedWidget. Users drill down from the main menu through category pages to feature pages. A navigation stack tracks history for automatic back-button behaviour.',
        'Scales to any number of pages without UI clutter. Full screen available for content on every page. The stack ensures consistent back-button behaviour regardless of entry path.',
        gridjs.html('<span style="color:#2e7d32; font-weight:bold;">Selected</span>')
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
