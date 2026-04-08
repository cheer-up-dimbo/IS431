/**
 * svg-zoom.js — Click-to-zoom for SVG diagrams.
 * Usage: add the `zoomable` class to any <svg> element to make it zoomable.
 * A small "expand" button is added to the top-right of each SVG, and clicking
 * either the SVG body or the button opens a fullscreen modal showing a cloned
 * copy at full size.
 */
(function () {
  // ---- Shared overlay (created once) ----
  const overlay = document.createElement('div');
  overlay.id = 'global-svg-zoom-overlay';
  overlay.style.cssText = [
    'display:none',
    'position:fixed',
    'inset:0',
    'background:rgba(15,23,42,0.85)',
    'backdrop-filter:blur(6px)',
    '-webkit-backdrop-filter:blur(6px)',
    'z-index:9999',
    'align-items:center',
    'justify-content:center',
    'padding:24px',
    'cursor:zoom-out',
  ].join(';');

  const inner = document.createElement('div');
  inner.style.cssText = [
    'position:relative',
    'background:#fff',
    'border-radius:14px',
    'box-shadow:0 24px 80px rgba(0,0,0,0.5)',
    'padding:32px 36px',
    'width:min(95vw, 1500px)',
    'max-height:92vh',
    'overflow:auto',
    'cursor:default',
    'box-sizing:border-box',
  ].join(';');
  inner.addEventListener('click', (e) => e.stopPropagation());

  const closeBtn = document.createElement('div');
  closeBtn.textContent = '\u2715';
  closeBtn.title = 'Close';
  closeBtn.style.cssText = [
    'position:absolute',
    'top:-14px',
    'right:-14px',
    'width:34px',
    'height:34px',
    'border-radius:50%',
    'background:#fff',
    'border:1px solid #e2e8f0',
    'box-shadow:0 2px 8px rgba(0,0,0,0.2)',
    'font-size:18px',
    'line-height:34px',
    'text-align:center',
    'cursor:pointer',
    'color:#475569',
    'z-index:10',
    'user-select:none',
  ].join(';');
  closeBtn.addEventListener('click', closeOverlay);
  closeBtn.addEventListener('mouseenter', () => {
    closeBtn.style.background = '#fee2e2';
    closeBtn.style.color = '#dc2626';
  });
  closeBtn.addEventListener('mouseleave', () => {
    closeBtn.style.background = '#fff';
    closeBtn.style.color = '#475569';
  });

  inner.appendChild(closeBtn);
  overlay.appendChild(inner);

  overlay.addEventListener('click', closeOverlay);

  function closeOverlay() {
    overlay.style.display = 'none';
    // Remove the cloned svg and any caption
    const existingSvg = inner.querySelector('svg');
    if (existingSvg) existingSvg.remove();
    const existingCaption = inner.querySelector('.svg-zoom-caption');
    if (existingCaption) existingCaption.remove();
    document.body.style.overflow = '';
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.style.display === 'flex') closeOverlay();
  });

  // ---- Per-SVG activation ----
  function activateZoom(svg) {
    // Wrap if not already wrapped
    let wrapper = svg.closest('.svg-zoom-wrapper');
    if (!wrapper) {
      wrapper = document.createElement('div');
      wrapper.className = 'svg-zoom-wrapper';
      wrapper.style.cssText = 'position:relative; cursor:zoom-in;';
      svg.parentNode.insertBefore(wrapper, svg);
      wrapper.appendChild(svg);
    }

    // Add expand button (top-right)
    if (!wrapper.querySelector('.svg-zoom-btn')) {
      const btn = document.createElement('button');
      btn.className = 'svg-zoom-btn';
      btn.title = 'Click to enlarge';
      btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" fill="currentColor" viewBox="0 0 16 16"><path d="M1.5 1h4a.5.5 0 0 1 0 1H2.707l3.647 3.646a.5.5 0 1 1-.708.708L2 2.707V5.5a.5.5 0 0 1-1 0v-4A.5.5 0 0 1 1.5 1zm13 0a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0V2.707l-3.646 3.647a.5.5 0 0 1-.708-.708L13.293 2H10.5a.5.5 0 0 1 0-1h4zm-13 13h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5v-4a.5.5 0 0 1 1 0v2.793l3.646-3.647a.5.5 0 0 1 .708.708L2.707 14H5.5zm9.354-3.854a.5.5 0 0 1 .708 0l3.646 3.647V11.5a.5.5 0 0 1 1 0v4a.5.5 0 0 1-.5.5h-4a.5.5 0 0 1 0-1h2.793l-3.647-3.646a.5.5 0 0 1 0-.708z"/></svg> Expand';
      btn.style.cssText = [
        'position:absolute',
        'top:10px',
        'right:10px',
        'background:rgba(255,255,255,0.92)',
        'border:1px solid #e2e8f0',
        'border-radius:8px',
        'padding:5px 10px',
        'font-size:12px',
        'font-family:Inter, system-ui, sans-serif',
        'color:#475569',
        'cursor:pointer',
        'display:flex',
        'align-items:center',
        'gap:5px',
        'box-shadow:0 1px 4px rgba(0,0,0,0.08)',
        'z-index:2',
      ].join(';');
      btn.addEventListener('mouseenter', () => {
        btn.style.background = 'rgba(255,255,255,1)';
        btn.style.color = '#1e40af';
        btn.style.borderColor = '#93c5fd';
      });
      btn.addEventListener('mouseleave', () => {
        btn.style.background = 'rgba(255,255,255,0.92)';
        btn.style.color = '#475569';
        btn.style.borderColor = '#e2e8f0';
      });
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        openOverlay(svg);
      });
      wrapper.appendChild(btn);
    }

    // Click anywhere on the SVG also opens overlay
    svg.style.cursor = 'zoom-in';
    svg.addEventListener('click', () => openOverlay(svg));
  }

  function openOverlay(svg) {
    // Remove any existing clone
    const existingSvg = inner.querySelector('svg');
    if (existingSvg) existingSvg.remove();
    const existingCaption = inner.querySelector('.svg-zoom-caption');
    if (existingCaption) existingCaption.remove();

    const clone = svg.cloneNode(true);
    // Override all original sizing styles so the SVG fills the modal width
    clone.removeAttribute('style');
    clone.removeAttribute('class');
    clone.style.cssText = 'display:block; width:100%; height:auto; max-height:80vh; cursor:default;';
    clone.removeAttribute('onclick');
    inner.appendChild(clone);

    // Optional caption: look for adjacent figcaption / italic small text
    const next = svg.parentNode && svg.parentNode.nextElementSibling;
    if (next && (next.tagName === 'FIGCAPTION' || (next.tagName === 'P' && next.style.fontStyle === 'italic'))) {
      const cap = document.createElement('div');
      cap.className = 'svg-zoom-caption';
      cap.textContent = next.textContent.trim();
      cap.style.cssText = 'margin-top:14px; text-align:center; font-style:italic; font-size:0.9rem; color:#64748b;';
      inner.appendChild(cap);
    }

    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.body.appendChild(overlay);
    document.querySelectorAll('svg.zoomable').forEach(activateZoom);
  });
})();
