const guiDataIsolationEl = document.getElementById('gui-data-isolation');

if (guiDataIsolationEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Approach', width: '22%' },
      { name: 'Implementation', width: '30%' },
      { name: 'Pros', width: '23%' },
      { name: 'Cons', width: '25%' }
    ],
    data: [
      ['Single Database with User IDs', 'All users share one database, filtered by user_id column', 'Simple setup\nEasy backups', 'Privacy concerns\nData mixing risk\nSlower queries as data grows'],
      ['Per-User Database Files', 'Each user gets their own directory: users/[username]/data.db', 'Complete data isolation\nEasy account deletion\nPrivacy assured', 'Slightly more complex setup\nMultiple files to manage'],
      ['OS User Accounts', 'Separate Linux users with home directory isolation', 'OS-level security\nBuilt-in access control', 'Cumbersome login flow\nHeavy-handed for a training app\nSlow user switching']
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
        const approach = row.cells[0]?.data || '';
        if (approach.startsWith('Per-User')) return 'gridjs-tr-selected';
        return 'gridjs-tr-rejected';
      }
    }
  }).render(guiDataIsolationEl);
}
