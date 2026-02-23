const guiComboNotationEl = document.getElementById('gui-combo-notation');

if (guiComboNotationEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Symbol', width: '20%' },
      { name: 'Meaning', width: '50%' },
      { name: 'Example', width: '30%' }
    ],
    data: [
      ['1-6', 'Punch types: 1=Jab, 2=Cross, 3=Lead Hook, 4=Rear Hook, 5=Lead Uppercut, 6=Rear Uppercut', '1-2 = Jab-Cross'],
      ['1b-6b', 'Same punches to body (b = body)', '1-2b-3 = Jab, Cross to body, Lead Hook'],
      ['slip, block, roll', 'Defensive movements', 'slip-1-2 = Slip then Jab-Cross'],
      ['Multiple digits', 'Combination sequence', '1-2-3-2 = Jab-Cross-Lead Hook-Cross']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'normal'
      }
    }
  }).render(guiComboNotationEl);
}
