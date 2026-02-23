const guiKnownIssuesEl = document.getElementById('gui-known-issues');

if (guiKnownIssuesEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Issue', width: '30%' },
      { name: 'Impact', width: '25%' },
      { name: 'Workaround', width: '25%' },
      { name: 'Priority', width: '20%' }
    ],
    data: [
      ['No password recovery', 'Users cannot recover forgotten passwords', 'Create new account', 'Low - acceptable for prototype'],
      ['Arduino buffer overflow on rapid punches', 'Occasionally misses very fast punch sequences', 'Increased buffer clearing frequency', 'Medium - 95% accuracy achieved'],
      ['No data export functionality', 'Cannot export training history to external tools', 'Manual database access if needed', 'Low - not critical for core usage'],
      ['AI feedback not fully integrated', 'Uses template responses instead of LLM', 'Template feedback functional and useful', 'Medium - framework ready for LLM']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'normal'
      }
    }
  }).render(guiKnownIssuesEl);
}
