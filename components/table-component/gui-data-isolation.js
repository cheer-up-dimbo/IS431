(function() {
  var el = document.getElementById('gui-data-isolation');
  if (!el) return;
  el.innerHTML = '<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:0.92rem;">' +
    '<thead><tr style="background:#f0f0f0;">' +
    '<th style="padding:10px;border:1px solid #ddd;width:18%;">Strategy</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:42%;">Description</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:40%;">Evaluation</th>' +
    '</tr></thead><tbody>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Shared Database with User Column</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Single SQLite database with a user_id column on every table to filter records.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Simpler setup but any query without a WHERE clause leaks data across users. Higher risk of cross-contamination bugs. Schema changes affect all users simultaneously.</td></tr>' +
    '<tr style="background:#e8f5e9;">' +
    '<td style="padding:10px;border:1px solid #ddd;font-weight:bold;">Per-User Database Files</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Each user gets their own SQLite database file stored in a dedicated directory (users/&lt;username&gt;/).</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Complete physical isolation: no query can accidentally access another user\'s data. Easy to back up, migrate, or delete individual users. Slight overhead in managing multiple database connections.</td></tr>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Cloud/Server Database</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Centralised database hosted on a remote server, accessed over the network.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Requires internet connectivity, which cannot be guaranteed in gym environments. Adds latency and a single point of failure. Overengineered for a standalone training robot.</td></tr>' +
    '</tbody></table>';
})();
