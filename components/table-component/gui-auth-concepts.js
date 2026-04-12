(function() {
  var el = document.getElementById('gui-auth-concepts');
  if (!el) return;
  el.innerHTML = '<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:0.92rem;">' +
    '<thead><tr style="background:#f0f0f0;">' +
    '<th style="padding:10px;border:1px solid #ddd;width:20%;">Concept</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:45%;">Description</th>' +
    '<th style="padding:10px;border:1px solid #ddd;width:35%;">Reason for Decision</th>' +
    '</tr></thead><tbody>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Username/Password</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Standard text-based login requiring keyboard input on the touchscreen.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Requires fine-motor text input, which is slow and error-prone after warm-up or between rounds. A faster, more coarse-grained input method aligns better with training workflow pace.</td></tr>' +
    '<tr style="background:#ffebee;">' +
    '<td style="padding:10px;border:1px solid #ddd;">Biometric</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Fingerprint scanner or facial recognition for authentication.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Requires additional hardware. Face recognition is unreliable with headgear and sweat. Fingerprint sensors require precise contact and are less reliable when hands are wet or fatigued.</td></tr>' +
    '<tr style="background:#e8f5e9;">' +
    '<td style="padding:10px;border:1px solid #ddd;font-weight:bold;">Pattern Lock + Password Fallback</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">A 3x3 grid pattern lock on the touchscreen with dot targets sized at 48px hit radius to accommodate reliable padding-based presses. The pattern is SHA-256 hashed. Password login remains available on the phone dashboard for typed input.</td>' +
    '<td style="padding:10px;border:1px solid #ddd;">Large touch targets work reliably with the robot\'s padded controls. Drawing a pattern is faster than typing. The dual-method approach matches each interface to its appropriate input modality.</td></tr>' +
    '</tbody></table>';
})();
