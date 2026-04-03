const guiDataIsolationEl = document.getElementById('gui-data-isolation');

if (guiDataIsolationEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Strategy', width: '15%' },
      { name: 'Description', width: '30%' },
      { name: 'Evaluation', width: '30%' },
      { name: 'Decision', width: '25%' }
    ],
    data: [
      [
        'Shared Database with User Column',
        'Single SQLite database with a user_id column on every table to filter records',
        'Simpler setup but any query without a WHERE clause leaks data across users. Higher risk of cross-contamination bugs. Schema changes affect all users simultaneously.',
        gridjs.html('<span style="color:#c62828; font-weight:bold;">Rejected</span>')
      ],
      [
        'Per-User Database Files',
        'Each user gets their own SQLite database file stored in a dedicated directory (GUI/users/<username>/)',
        'Complete physical isolation: no query can accidentally access another user\'s data. Easy to back up, migrate, or delete individual users. Slight overhead in managing multiple database connections.',
        gridjs.html('<span style="color:#2e7d32; font-weight:bold;">Selected</span>')
      ],
      [
        'Cloud/Server Database',
        'Centralised database hosted on a remote server, accessed over the network',
        'Requires internet connectivity, which cannot be guaranteed in gym environments. Adds latency and a single point of failure. Overengineered for a standalone training robot.',
        gridjs.html('<span style="color:#c62828; font-weight:bold;">Rejected</span>')
      ]
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: { 'white-space': 'normal' }
    }
  }).render(guiDataIsolationEl);
}
