(function() {
  var el = document.getElementById('gui-nav-concepts');
  if (!el) return;
  el.innerHTML = '<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:0.92rem;">' +
    '<thead><tr style="background:#f0f0f0;">' +
    '<th style="padding:10px;border:1px solid #ddd;width:18%;">Concept</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:42%;">Description</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:40%;">Evaluation</th>' +
    '</tr></thead><tbody>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Flat Menu</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">All pages accessible from a single top-level menu with no hierarchy.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Does not scale beyond 8-10 items. With 44 pages, the menu becomes unusable on a 10-inch touchscreen.</td></tr>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Tab-Based Navigation</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Persistent tab bar at the top or bottom of the screen, each tab leading to a feature category.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Tab bar consumes screen space on every page. On a small display, this reduces the content area significantly. Tab count is also limited before horizontal scrolling is needed.</td></tr>' +
    '<tr style="background:#e8f5e9;">' +
    '<td style="padding:10px;border:1px solid #ddd;font-weight:bold;">Hierarchical Page Stack</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Tree-structured navigation with a central QStackedWidget. Users drill down from the main menu through category pages to feature pages. A navigation stack tracks history for automatic back-button behaviour.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Scales to any number of pages without UI clutter. Full screen available for content on every page. The stack ensures consistent back-button behaviour regardless of entry path.</td></tr>' +
    '</tbody></table>';
})();
