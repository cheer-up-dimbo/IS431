(function() {
  var el = document.getElementById('gui-dashboard-concepts');
  if (!el) return;
  el.innerHTML = '<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:0.92rem;">' +
    '<thead><tr style="background:#f0f0f0;">' +
    '<th style="padding:10px;border:1px solid #ddd;width:20%;">Concept</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:45%;">Description</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:35%;">Reason for Decision</th>' +
    '</tr></thead><tbody>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Native Mobile App</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Separate iOS and Android apps communicating with the robot over WiFi.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Requires maintaining two codebases, App Store approval cycles, and ongoing updates. Overengineered for a local-network training robot.</td></tr>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Bluetooth Direct Control</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Phone connects via Bluetooth Low Energy for command-and-control.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Limited range, complex pairing, cannot serve a rich analytics dashboard. Suitable only for simple remote triggers, not data visualization.</td></tr>' +
    '<tr style="background:#e8f5e9;">' +
    '<td style="padding:10px;border:1px solid #ddd;font-weight:bold;">Local Web App via WiFi AP</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">The robot hosts its own WiFi access point. Users connect and access a Vue 3 dashboard through their phone browser. The dashboard shares the same SQLite database as the touchscreen GUI. Features include session history with letter grades, performance trend charts, achievement badges, AI coaching chat, remote training control, and robot height adjustment.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">No app installation required. Works on any phone with a browser. Data synchronized automatically through the shared database. The 100ms polling interval for remote commands provides near-instant response.</td></tr>' +
    '</tbody></table>';
})();
