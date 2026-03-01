const guiIntegrationSpecsEl = document.getElementById('gui-integration-specs');

if (guiIntegrationSpecsEl) {
  new gridjs.Grid({
    columns: [
      { name: 'Component', width: '20%' },
      { name: 'Interface', width: '20%' },
      { name: 'Data Format', width: '30%' },
      { name: 'Update Rate', width: '30%' }
    ],
    data: [
      ['Arduino MPU6050', 'Serial (115200 baud)', 'ASCII text: "Total_Accel: X.XX"', '100 Hz'],
      ['Computer Vision (Yogee)', 'Python function calls', 'Numeric scores (0-5 scale)', 'Post-processing (async)'],
      ['Robotic Arms (Elgin)', 'ROS topics / Serial commands', 'Actuation commands (punch type, timing)', 'On-demand'],
      ['Height/Rotation (Jeanette)', 'Serial / GPIO', 'Position commands', 'On-demand']
    ],
    search: false,
    sort: true,
    pagination: false,
    style: {
      table: {
        'white-space': 'normal'
      }
    }
  }).render(guiIntegrationSpecsEl);
}
