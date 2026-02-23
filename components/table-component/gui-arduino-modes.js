const guiArduinoModesEl = document.getElementById('gui-arduino-modes');

if (guiArduinoModesEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Mode', width: '20%' },
      { name: 'Purpose', width: '25%' },
      { name: 'Arduino Behavior', width: '30%' },
      { name: 'GUI Receives', width: '25%' }
    ],
    data: [
      ['CONTINUOUS', 'Debugging, development', 'Stream acceleration continuously at 100Hz', '"Total_Accel: X.XX" messages'],
      ['STAMINA', 'Endurance testing (2 min)', 'Count punches internally for duration', '"PUNCH_DETECTED: N" (real-time)\n"RESULT:PUNCHES:N" (final)'],
      ['POWER', 'Explosive power testing', 'Track peak and average acceleration', '"POWER_PUNCH: X.XX" (per punch)\n"RESULT:PEAK:X,AVG:Y,COUNT:Z" (final)']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'pre-wrap'
      }
    }
  }).render(guiArduinoModesEl);
}
