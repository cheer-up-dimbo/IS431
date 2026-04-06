(function() {
  var el = document.getElementById('gui-framework-comparison');
  if (!el) return;
  el.innerHTML = '<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:0.92rem;">' +
    '<thead><tr style="background:#f0f0f0;">' +
    '<th style="padding:10px;border:1px solid #ddd;width:20%;">Framework</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:40%;">Pros</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:40%;">Cons</th>' +
    '</tr></thead><tbody>' +
    '<tr style="background:#e8f5e9;">' +
    '<td style="padding:10px;border:1px solid #ddd;font-weight:bold;">PySide6 (Qt for Python)</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Native on Jetson, mature touchscreen support, extensive Qt documentation, builds on existing Python knowledge</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Large framework footprint, steeper learning curve than lightweight alternatives</td></tr>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Tkinter</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Included with Python, minimal setup, simple API</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Limited widget set, poor touchscreen support, dated visual appearance, limited layout control</td></tr>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Kivy</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Designed for touch interfaces, cross-platform, modern look</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Not pre-installed on Jetson, smaller community, unfamiliar API requiring additional learning time</td></tr>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Web-based (Flask + Browser)</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Flexible UI with HTML/CSS, responsive design, familiar web technologies</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Requires running a local web server, adds browser dependency, latency concerns on resource-constrained hardware</td></tr>' +
    '</tbody></table>';
})();
