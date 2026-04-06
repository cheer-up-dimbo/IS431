/**
 * Report Navigation Sidebar
 * Auto-injects a left-side report TOC sidebar into any page that loads this script.
 * Detects the current page and highlights it. Sections are collapsible.
 */
(function () {
  'use strict';

  // ─── Navigation Structure ───────────────────────────────────────────
  const NAV_TREE = [
    {
      label: '§1 Introduction',
      href: '/index.html#introduction',
    },
    {
      label: '§2 Problem Clarification',
      href: '/index.html#problem-clarification',
      children: [
        { label: '2.1 Background', href: '/index.html#background' },
        { label: '2.2 Primary Research', href: '/index.html#primary-research' },
        { label: '2.3 Secondary Research', href: '/index.html#secondary-research' },
        { label: '2.4 Value Propositions', href: '/index.html#value-proposition' },
      ]
    },
    {
      label: '§3 Design Methodology',
      href: '/index.html#design-methodology',
      children: [
        { label: '3.1 Clarification of Task', href: '/index.html#clarification-of-task' },
        { label: '3.2 V-Model', href: '/index.html#v-model' },
      ]
    },
    {
      label: '§4 Final Design',
      href: '/index.html#final-design',
      children: [
        { label: '4.1 System Overview', href: '/index.html#system-overview' },
        { label: '4.2 User Journey', href: '/index.html#user-journey' },
      ]
    },
    {
      label: '§5 Conceptual Design',
      href: '/index.html#conceptual-design',
      children: [
        { label: '5.1 GUI', href: '/pages/gui.html' },
        {
          label: '5.2 Robot Mechanism',
          href: '/pages/robot-mechanism.html',
          children: [
            { label: '5.2.1 Base', href: '/pages/robot-mechanism/base.html' },
            { label: '5.2.2 Rotation', href: '/pages/robot-mechanism/rotation.html' },
            { label: '5.2.3 Height Adjustment', href: '/pages/robot-mechanism/height-adjustment.html' },
            { label: '5.2.4 Padding', href: '/pages/robot-mechanism/padding.html' },
            { label: '5.2.5 Arm Actuation', href: '/pages/robot-mechanism/arm-actuation.html' },
            { label: 'Verification Results', href: '/pages/robot-mechanism/testing.html' },
          ]
        },
        { label: '5.3 Robot Intelligence', href: '/index.html#robot-intelligence' },
      ]
    },
    {
      label: '§6 Project Timeline',
      href: '/index.html#project-timeline',
    },
    {
      label: 'References',
      href: '/index.html#references',
    },
    {
      label: 'Appendices',
      href: '/index.html#appendices',
      children: [
        { label: 'Appendix 1: Upper Mechanism', href: '/pages/appendix-upper.html' },
        { label: 'Appendix 2: Lower Mechanism', href: '/pages/appendix-lower.html' },
      ]
    },
  ];

  // ─── Subsystem Sub-Pages ───────────────────────────────────────────
  const SUBSYSTEM_SUBPAGES = {
    '/pages/robot-mechanism/base.html': [
      { label: 'Design Ideation', href: '/pages/robot-mechanism/base/design-ideation.html' },
      { label: 'Mechanical Design', href: '/pages/robot-mechanism/base/mechanical-design.html' },
      { label: 'Load & Stability', href: '/pages/robot-mechanism/base/load-stability-analysis.html' },
      { label: 'Testing & Evaluation', href: '/pages/robot-mechanism/base/testing-evaluation.html' },
    ],
    '/pages/robot-mechanism/rotation.html': [
      { label: 'Design Ideation', href: '/pages/robot-mechanism/rotation/design-ideation.html' },
      { label: 'Motion Axis Selection', href: '/pages/robot-mechanism/rotation/motion-axis-selection.html' },
      { label: 'Bearing Selection', href: '/pages/robot-mechanism/rotation/bearing-selection.html' },
      { label: 'Drive Architecture', href: '/pages/robot-mechanism/rotation/drive-architecture.html' },
      { label: 'Outboard Support', href: '/pages/robot-mechanism/rotation/outboard-support.html' },
      { label: 'Electrical & Control', href: '/pages/robot-mechanism/rotation/electrical-control.html' },
      { label: 'Mechanical Design', href: '/pages/robot-mechanism/rotation/mechanical-design.html' },
      { label: 'Load Analysis', href: '/pages/robot-mechanism/rotation/load-analysis.html' },
      { label: 'Testing & Evaluation', href: '/pages/robot-mechanism/rotation/testing-evaluation.html' },
    ],
    '/pages/robot-mechanism/height-adjustment.html': [
      { label: 'Concept Generation', href: '/pages/robot-mechanism/height-adjustment/concept-generation.html' },
      { label: 'Design Ideation', href: '/pages/robot-mechanism/height-adjustment/design-ideation.html' },
      { label: 'Calculations & Sizing', href: '/pages/robot-mechanism/height-adjustment/calculations-sizing.html' },
      { label: 'Structural Layout', href: '/pages/robot-mechanism/height-adjustment/structural-layout.html' },
      { label: 'Mechanical Design', href: '/pages/robot-mechanism/height-adjustment/mechanical-design.html' },
      { label: 'Lift-Structure Separation', href: '/pages/robot-mechanism/height-adjustment/lift-structure-separation.html' },
      { label: 'Electrical & Control', href: '/pages/robot-mechanism/height-adjustment/electrical-control.html' },
      { label: 'Load Analysis', href: '/pages/robot-mechanism/height-adjustment/load-analysis.html' },
      { label: 'Testing & Evaluation', href: '/pages/robot-mechanism/height-adjustment/testing-evaluation.html' },
    ],
    '/pages/robot-mechanism/padding.html': [
      { label: 'Mechanical Design', href: '/pages/robot-mechanism/padding/mechanical-design.html' },
      { label: 'Electrical Integration', href: '/pages/robot-mechanism/padding/electrical-integration.html' },
      { label: 'Testing & Evaluation', href: '/pages/robot-mechanism/padding/testing-evaluation.html' },
      { label: 'Troubleshooting', href: '/pages/robot-mechanism/padding/troubleshooting.html' },
    ],
    '/pages/robot-mechanism/arm-actuation.html': [
      { label: 'Design & Ideation', href: '/pages/robot-mechanism/arm-actuation/design-ideation.html' },
      { label: 'Mechanical Design', href: '/pages/robot-mechanism/arm-actuation/mechanical-design.html' },
      { label: 'Electrical Integration', href: '/pages/robot-mechanism/arm-actuation/electrical-integration.html' },
      { label: 'Firmware & Software', href: '/pages/robot-mechanism/arm-actuation/firmware-software.html' },
      { label: 'Testing & Evaluation', href: '/pages/robot-mechanism/arm-actuation/testing-evaluation.html' },
      { label: 'Troubleshooting', href: '/pages/robot-mechanism/arm-actuation/troubleshooting.html' },
    ],
  };

  // ─── Helpers ────────────────────────────────────────────────────────
  function currentPath() {
    return window.location.pathname;
  }

  function resolveHref(href) {
    return href;
  }

  function isActive(href) {
    const path = currentPath();
    const hrefPath = href.split('#')[0];
    if (!hrefPath || hrefPath === '/') return false;
    return path.endsWith(hrefPath) || path === hrefPath;
  }

  function isInSubsystem(parentHref) {
    const path = currentPath();
    const parentPath = parentHref.split('#')[0];
    if (isActive(parentHref)) return true;
    const subpages = SUBSYSTEM_SUBPAGES[parentPath];
    if (subpages) {
      return subpages.some(sp => isActive(sp.href));
    }
    return false;
  }

  // Track all section/linksList pairs for Expand/Collapse All
  const sectionPairs = [];

  function openSection(pair) {
    pair.sectionEl.classList.add('open');
    pair.linksList.classList.add('open');
  }

  function closeSection(pair) {
    pair.sectionEl.classList.remove('open');
    pair.linksList.classList.remove('open');
  }

  // ─── Build the Sidebar ──────────────────────────────────────────────
  function buildNav() {
    const nav = document.createElement('nav');
    nav.className = 'report-nav';
    nav.setAttribute('aria-label', 'Report Navigation');

    // Title
    const title = document.createElement('a');
    title.className = 'report-nav__title';
    title.href = resolveHref('/index.html');
    title.textContent = 'IS-431 Report';
    nav.appendChild(title);

    // Expand / Collapse All controls
    const controls = document.createElement('div');
    controls.className = 'report-nav__controls';

    const expandAllBtn = document.createElement('button');
    expandAllBtn.className = 'report-nav__ctrl-btn';
    expandAllBtn.textContent = '▼ Expand All';
    expandAllBtn.addEventListener('click', () => {
      sectionPairs.forEach(openSection);
    });

    const collapseAllBtn = document.createElement('button');
    collapseAllBtn.className = 'report-nav__ctrl-btn';
    collapseAllBtn.textContent = '▲ Collapse All';
    collapseAllBtn.addEventListener('click', () => {
      sectionPairs.forEach(closeSection);
    });

    controls.appendChild(expandAllBtn);
    controls.appendChild(collapseAllBtn);
    nav.appendChild(controls);

    // Build sections
    NAV_TREE.forEach(section => {
      const sectionEl = document.createElement('div');
      sectionEl.className = 'report-nav__section';

      const hasChildren = section.children && section.children.length > 0;

      // Check if this section or any child is active
      let sectionActive = isActive(section.href);
      if (hasChildren) {
        sectionActive = sectionActive || section.children.some(c => {
          if (isActive(c.href)) return true;
          if (c.children) return c.children.some(gc => isActive(gc.href) || isInSubsystem(gc.href));
          return isInSubsystem(c.href);
        });
      }

      const labelSpan = document.createElement('span');
      labelSpan.textContent = section.label;
      sectionEl.appendChild(labelSpan);

      if (hasChildren) {
        const arrow = document.createElement('span');
        arrow.className = 'report-nav__section-arrow';
        arrow.textContent = '▶';
        sectionEl.appendChild(arrow);

        // Build children list FIRST so we can reference it in the click handler
        const linksList = document.createElement('ul');
        linksList.className = 'report-nav__links';

        // Auto-open if current page is within this section
        if (sectionActive) {
          sectionEl.classList.add('open');
          linksList.classList.add('open');
        }

        // Track for expand/collapse all
        const pair = { sectionEl, linksList };
        sectionPairs.push(pair);

        // Click ONLY opens (never closes). Use Collapse All to close.
        sectionEl.addEventListener('click', () => {
          openSection(pair);
        });

        // Populate children
        section.children.forEach(child => {
          const li = document.createElement('li');
          const a = document.createElement('a');
          a.className = 'report-nav__link';
          a.href = resolveHref(child.href);
          a.textContent = child.label;
          if (isActive(child.href) || isInSubsystem(child.href)) {
            a.classList.add('active');
          }
          li.appendChild(a);
          linksList.appendChild(li);

          // Grandchildren (subsystem sub-pages)
          if (child.children) {
            child.children.forEach(gc => {
              const gcLi = document.createElement('li');
              const gcA = document.createElement('a');
              gcA.className = 'report-nav__link report-nav__sublink';
              gcA.href = resolveHref(gc.href);
              gcA.textContent = gc.label;
              if (isActive(gc.href) || isInSubsystem(gc.href)) {
                gcA.classList.add('active');
              }
              gcLi.appendChild(gcA);
              linksList.appendChild(gcLi);

              // Sub-page links for this subsystem
              const subPages = SUBSYSTEM_SUBPAGES[gc.href.split('#')[0]];
              if (subPages && isInSubsystem(gc.href)) {
                subPages.forEach(sp => {
                  const spLi = document.createElement('li');
                  const spA = document.createElement('a');
                  spA.className = 'report-nav__link';
                  spA.style.paddingLeft = '52px';
                  spA.style.fontSize = '0.72rem';
                  spA.href = resolveHref(sp.href);
                  spA.textContent = sp.label;
                  if (isActive(sp.href)) spA.classList.add('active');
                  spLi.appendChild(spA);
                  linksList.appendChild(spLi);
                });
              }
            });
          }
        });

        nav.appendChild(sectionEl);
        nav.appendChild(linksList);
      } else {
        // No children — make it a direct link
        sectionEl.style.cursor = 'pointer';
        sectionEl.addEventListener('click', () => {
          window.location.href = resolveHref(section.href);
        });
        if (sectionActive) sectionEl.style.color = '#1d4ed8';
        nav.appendChild(sectionEl);
      }
    });

    return nav;
  }

  // ─── Toggle Button (mobile) ────────────────────────────────────────
  function buildToggle(nav) {
    const btn = document.createElement('button');
    btn.className = 'report-nav__toggle';
    btn.innerHTML = '☰';
    btn.setAttribute('aria-label', 'Toggle navigation');
    btn.addEventListener('click', () => {
      nav.classList.toggle('mobile-open');
      nav.classList.toggle('collapsed');
      document.body.classList.toggle('nav-collapsed');
    });
    return btn;
  }

  // ─── Inject ─────────────────────────────────────────────────────────
  function init() {
    // Inject CSS
    const cssPath = resolveHref('/components/report-nav/report-nav.css');
    if (!document.querySelector('link[href*="report-nav"]')) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = cssPath;
      document.head.appendChild(link);
    }

    const nav = buildNav();
    const toggle = buildToggle(nav);

    document.body.prepend(nav);
    document.body.prepend(toggle);
    document.body.classList.add('has-report-nav');

    // Scroll active item into view
    requestAnimationFrame(() => {
      const active = nav.querySelector('.report-nav__link.active');
      if (active) {
        active.scrollIntoView({ block: 'center', behavior: 'instant' });
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
