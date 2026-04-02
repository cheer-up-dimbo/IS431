const guiNavConceptsEl = document.getElementById('gui-nav-concepts');

if (guiNavConceptsEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Concept', width: '25%' },
      { name: 'Description', width: '40%' },
      { name: 'Decision', width: '35%' }
    ],
    data: [
      ['Tab-Based Navigation', 'All major sections behind a persistent tab bar at the top of every screen.', 'Rejected. Tab targets are narrow on a small display and the layout does not suit multi-step training workflows that require sequential progression.'],
      ['Hierarchical Pages with Navigation Stack', 'Tree-structured pages where the user moves forward through menus and steps back via a back button. Navigation history is managed centrally.', 'Selected. Maximises screen space per page, supports large touch targets, and naturally matches the sequential flow of configuring and running a training session.'],
      ['Dashboard with Modal Dialogs', 'A single dashboard screen where all functions open as popup dialogs overlaying the main view.', 'Rejected. Scales poorly with the number of training modes and produces a fragmented experience across multi-step workflows.']
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
        const decision = row.cells[2]?.data || '';
        if (decision.startsWith('Selected')) return 'gridjs-tr-selected';
        return 'gridjs-tr-rejected';
      }
    }
  }).render(guiNavConceptsEl);
}
