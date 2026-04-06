/**
 * lightbox.js — Global click-to-zoom lightbox for IS-431 report diagrams.
 * Usage: add data-zoom to any <img> element to make it zoomable.
 * The overlay is injected once and reused across all images.
 */
(function () {
  // Create shared overlay once
  const overlay = document.createElement('div');
  overlay.id = 'global-lightbox';
  overlay.style.cssText = [
    'display:none',
    'position:fixed',
    'inset:0',
    'background:rgba(0,0,0,0.85)',
    'z-index:9999',
    'align-items:center',
    'justify-content:center',
    'cursor:zoom-out',
    'padding:20px',
  ].join(';');

  const zoomedImg = document.createElement('img');
  zoomedImg.style.cssText = [
    'max-width:95vw',
    'max-height:90vh',
    'object-fit:contain',
    'border-radius:6px',
    'box-shadow:0 8px 40px rgba(0,0,0,0.6)',
  ].join(';');

  const hint = document.createElement('div');
  hint.style.cssText = [
    'position:absolute',
    'bottom:18px',
    'left:50%',
    'transform:translateX(-50%)',
    'color:rgba(255,255,255,0.6)',
    'font-size:0.8rem',
    'pointer-events:none',
  ].join(';');
  hint.textContent = 'Click anywhere to close';

  overlay.appendChild(zoomedImg);
  overlay.appendChild(hint);

  overlay.addEventListener('click', () => {
    overlay.style.display = 'none';
    zoomedImg.src = '';
  });

  // Keyboard dismiss
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      overlay.style.display = 'none';
      zoomedImg.src = '';
    }
  });

  function activateZoom(img) {
    img.style.cursor = 'zoom-in';
    img.title = 'Click to enlarge';
    img.addEventListener('click', () => {
      zoomedImg.src = img.src;
      zoomedImg.alt = img.alt + ' (full size)';
      overlay.style.display = 'flex';
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.body.appendChild(overlay);
    // Auto-activate all images with data-zoom attribute
    document.querySelectorAll('img[data-zoom]').forEach(activateZoom);
  });
})();
