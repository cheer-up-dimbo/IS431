const guiDataIsolationEl = document.getElementById('gui-data-isolation');

if (guiDataIsolationEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Approach', width: '25%' },
      { name: 'Implementation', width: '30%' },
      { name: 'Pros', width: '20%' },
      { name: 'Cons', width: '25%' }
    ],
    data: [
      ['Single Database with User IDs', 'All users share one database, filtered by user_id column', 'Simple setup\nEasy backups', 'Privacy concerns\nData mixing risk\nSlower queries'],
      ['Per-User Database Files ✓', 'Each user gets users/username/data.db file', 'Complete isolation\nEasy deletion\nPrivacy assured', 'Slightly more complex\nMultiple files to manage'],
      ['OS User Accounts', 'Separate Linux users, home directory isolation', 'OS-level security', 'Cumbersome login\nHeavy-handed approach\nSlow user switching']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'pre-wrap'
      }
    }
  }).render(guiDataIsolationEl);
}
