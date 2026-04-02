const guiIntegrationSpecsEl = document.getElementById('gui-integration-specs');

if (guiIntegrationSpecsEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Component', width: '25%' },
      { name: 'Interface Method', width: '25%' },
      { name: 'Data Format', width: '25%' },
      { name: 'Update Rate', width: '25%' }
    ],
    data: [
      ['Arduino MPU6050', 'Serial (115200 baud)', 'ASCII text: "Total_Accel: X.XX"', '100 Hz'],
      ['Computer Vision', 'File-based handshake', 'Numeric scores (0-5 scale)', 'Post-processing (async)'],
      ['Robotic Arms', 'ROS topics / Serial commands', 'Actuation commands (punch type, timing)', 'On-demand']
    ],
    search: false,
    sort: false,
    pagination: false,
    style: {
      table: {
        'white-space': 'normal'
      }
    }
  }).render(guiIntegrationSpecsEl);
}
