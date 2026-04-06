const guiDataIsolationEl = document.getElementById('gui-data-isolation');

if (guiDataIsolationEl) {
  const greenBg = 'background:#e8f5e9; width:100%; display:block; padding:8px; margin:0; box-sizing:border-box;';
  const redBg = 'background:#ffebee; width:100%; display:block; padding:8px; margin:0; box-sizing:border-box;';

  new gridjs.Grid({
    columns: [
      { name: 'Strategy', width: '20%' },
      { name: 'Description', width: '40%' },
      { name: 'Evaluation', width: '40%' }
    ],
    data: [
      [
        gridjs.html('<div style="' + redBg + '">Shared Database with User Column</div>'),
        gridjs.html('<div style="' + redBg + '">Single SQLite database with a user_id column on every table to filter records</div>'),
        gridjs.html('<div style="' + redBg + '">Simpler setup but any query without a WHERE clause leaks data across users. Higher risk of cross-contamination bugs. Schema changes affect all users simultaneously.</div>')
      ],
      [
        gridjs.html('<div style="' + greenBg + 'font-weight:bold;">Per-User Database Files</div>'),
        gridjs.html('<div style="' + greenBg + '">Each user gets their own SQLite database file stored in a dedicated directory (GUI/users/&lt;username&gt;/)</div>'),
        gridjs.html('<div style="' + greenBg + '">Complete physical isolation: no query can accidentally access another user\'s data. Easy to back up, migrate, or delete individual users. Slight overhead in managing multiple database connections.</div>')
      ],
      [
        gridjs.html('<div style="' + redBg + '">Cloud/Server Database</div>'),
        gridjs.html('<div style="' + redBg + '">Centralised database hosted on a remote server, accessed over the network</div>'),
        gridjs.html('<div style="' + redBg + '">Requires internet connectivity, which cannot be guaranteed in gym environments. Adds latency and a single point of failure. Overengineered for a standalone training robot.</div>')
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
