/* The actual campaign work becomes an nine-chapter, scroll-controlled story.
   The existing hero and menu scripts own Lenis and navigation. */
(() => {
  const theatre = document.querySelector('.theatre');
  if (!theatre) return;
  const pin = theatre.querySelector('.theatre-pin');
  const chapters = [...theatre.querySelectorAll('.chapter')];
  const jumps = [...theatre.querySelectorAll('[data-jump]')];
  const counter = theatre.querySelector('[data-chapter-number]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let active = -1;
  let ticking = false;

  function select(index) {
    if (index === active || !chapters[index]) return;
    active = index;
    chapters.forEach((el, i) => {
      const shown = i === index;
      el.classList.toggle('active', shown);
      el.inert = !shown;
      el.setAttribute('aria-hidden', String(!shown));
    });
    jumps.forEach((el, i) => {
      el.classList.toggle('active', i === index);
      if (i === index) el.setAttribute('aria-current', 'true');
      else el.removeAttribute('aria-current');
    });
    if (counter) counter.textContent = `${String(index + 1).padStart(2, '0')} / ${String(chapters.length).padStart(2, '0')}`;
    pin.style.setProperty('--stage-color', chapters[index].style.getPropertyValue('--scene'));
  }

  function frame() {
    ticking = false;
    const box = theatre.getBoundingClientRect();
    const distance = Math.max(1, box.height - innerHeight);
    const progress = Math.max(0, Math.min(.99999, -box.top / distance));
    const exact = progress * chapters.length;
    const index = Math.min(chapters.length - 1, Math.floor(exact));
    if (!reduced.matches) select(index);
    pin.style.setProperty('--chapter-progress', (exact - index).toFixed(3));
    if (!reduced.matches) pin.style.setProperty('--media-y', `${(exact - index - .5) * 15}px`);
  }
  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(frame);
  }
  addEventListener('scroll', queue, {passive:true});
  addEventListener('resize', queue);
  document.fonts?.ready?.then(queue);
  if (reduced.matches) chapters.forEach(el => { el.inert = false; el.setAttribute('aria-hidden','false'); el.classList.add('active'); });
  queue();

  jumps.forEach((button, index) => button.addEventListener('click', () => {
    const target = theatre.getBoundingClientRect().top + scrollY +
      (theatre.offsetHeight - innerHeight) * (index + .08) / chapters.length;
    scrollTo({top: target, behavior: reduced.matches ? 'instant' : 'smooth'});
    select(index);
  }));

  // Let artwork open at its complete native aspect ratio. Hover cues the
  // interaction; a click or keyboard action opens a stable, accessible view.
  const overlay = document.querySelector('.work-lightbox');
  const expanded = overlay?.querySelector('img');
  let previousFocus;
  if (overlay && expanded) {
    theatre.querySelectorAll('.artifact').forEach(figure => {
      figure.tabIndex = 0;
      figure.setAttribute('role', 'button');
      const source = figure.querySelector('img');
      figure.setAttribute('aria-label', 'Enlarge ' + source.alt);
      function open() {
        previousFocus = figure;
        expanded.src = source.currentSrc || source.src;
        expanded.alt = source.alt;
        overlay.querySelector('p').textContent = figure.querySelector('figcaption')?.textContent || '';
        overlay.showModal();
        document.body.classList.add('work-lightbox-open');
      }
      figure.addEventListener('click', open);
      figure.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
      });
    });
    overlay.querySelector('button').addEventListener('click', () => overlay.close());
    overlay.addEventListener('click', e => {
      if (e.target === overlay) overlay.close();
    });
    overlay.addEventListener('close', () => {
      document.body.classList.remove('work-lightbox-open');
      expanded.removeAttribute('src');
      previousFocus?.focus();
    });
  }
})();
