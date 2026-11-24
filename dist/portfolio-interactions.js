(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');

  const work = document.querySelector('.work-explorer');
  if (work) {
    const choices = [...work.querySelectorAll('[data-case-choice]')];
    const panels = [...work.querySelectorAll('[data-case-panel]')];
    const stage = work.querySelector('[data-work-stage]');
    const strip = work.querySelector('.work-choices');
    const announcement = work.querySelector('[data-work-announcement]');
    let selected = choices[0]?.dataset.caseChoice;
    let raf = 0;
    function choose(slug, center = false) {
      if (!slug || slug === selected && !center) return;
      selected = slug;
      if (announcement) announcement.textContent = 'Showing ' + choices.find(button => button.dataset.caseChoice === slug)?.querySelector('.work-choice-name')?.textContent;
      panels.find(panel => panel.dataset.casePanel === slug)?.querySelectorAll('img').forEach(img => { img.loading = 'eager'; });
      choices.forEach(button => {
        const active = button.dataset.caseChoice === slug;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', String(active));
        if (active && center && innerWidth <= 760) button.scrollIntoView({behavior: reduced.matches ? 'instant' : 'smooth', block:'nearest', inline:'center'});
      });
      panels.forEach(panel => {
        const active = panel.dataset.casePanel === slug;
        panel.classList.toggle('is-active', active);
        panel.inert = !active;
        panel.setAttribute('aria-hidden', String(!active));
      });
    }
    choices.forEach(button => {
      button.addEventListener('click', () => choose(button.dataset.caseChoice, true));
      if (matchMedia('(hover:hover) and (pointer:fine)').matches) {
        button.addEventListener('pointerenter', () => choose(button.dataset.caseChoice));
      }
      button.addEventListener('focus', () => choose(button.dataset.caseChoice));
    });
    strip?.addEventListener('scroll', () => {
      if (innerWidth > 760 || raf) return;
      raf = requestAnimationFrame(() => {
        raf = 0;
        const middle = strip.getBoundingClientRect().left + strip.clientWidth / 2;
        const closest = choices.reduce((winner, current) =>
          Math.abs(current.getBoundingClientRect().left + current.offsetWidth / 2 - middle) <
          Math.abs(winner.getBoundingClientRect().left + winner.offsetWidth / 2 - middle)
          ? current : winner, choices[0]);
        choose(closest?.dataset.caseChoice);
      });
    }, {passive:true});
    if (!reduced.matches && matchMedia('(hover:hover) and (pointer:fine)').matches) {
      stage?.addEventListener('pointermove', e => {
        const r = stage.getBoundingClientRect();
        stage.style.setProperty('--art-x', ((e.clientX - r.left - r.width / 2) * .022).toFixed(1) + 'px');
        stage.style.setProperty('--art-y', ((e.clientY - r.top - r.height / 2) * .018).toFixed(1) + 'px');
      }, {passive:true});
      stage?.addEventListener('pointerleave', () => {
        stage.style.setProperty('--art-x','0px');
        stage.style.setProperty('--art-y','0px');
      });
    }
  }

  const casePage = document.querySelector('.case-story');
  if (casePage) {
    const rows = [...casePage.querySelectorAll('.story-row')];
    if ('IntersectionObserver' in window && !reduced.matches) {
      casePage.classList.add('has-case-observer');
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in-view');
            observer.unobserve(entry.target);
          }
        });
      }, {threshold:.12});
      rows.forEach(row => observer.observe(row));
    }
    document.querySelectorAll('.case-artifacts .artifact-grid, .case-artifacts .catalogue-grid').forEach((gallery, group) => {
      const cards = [...gallery.children];
      if (cards.length < 2) return;
      gallery.classList.add('case-rail');
      gallery.setAttribute('tabindex', '0');
      gallery.setAttribute('aria-label', 'Project material, gallery ' + (group + 1) + '. Scroll horizontally or use the arrow buttons.');
      const nav = document.createElement('div');
      nav.className = 'case-rail-nav';
      nav.innerHTML = '<span class="case-rail-count" aria-live="polite">01 / ' + String(cards.length).padStart(2,'0') + '</span><div><button type="button" class="case-rail-prev" aria-label="Previous item">←</button><button type="button" class="case-rail-next" aria-label="Next item">→</button></div>';
      gallery.before(nav);
      const count = nav.querySelector('.case-rail-count');
      const index = () => Math.max(0, cards.reduce((best, card, i) => {
        return Math.abs(card.getBoundingClientRect().left - gallery.getBoundingClientRect().left) <
          Math.abs(cards[best].getBoundingClientRect().left - gallery.getBoundingClientRect().left) ? i : best;
      }, 0));
      const move = delta => cards[Math.max(0, Math.min(cards.length - 1, index() + delta))]
        .scrollIntoView({behavior:reduced.matches ? 'instant' : 'smooth', block:'nearest', inline:'start'});
      nav.querySelector('.case-rail-prev').addEventListener('click', () => move(-1));
      nav.querySelector('.case-rail-next').addEventListener('click', () => move(1));
      let raf = 0;
      gallery.addEventListener('scroll', () => {
        if (raf) return;
        raf = requestAnimationFrame(() => {
          raf = 0;
          const current = index();
          count.textContent = String(current + 1).padStart(2,'0') + ' / ' + String(cards.length).padStart(2,'0');
          nav.querySelector('.case-rail-prev').disabled = current === 0;
          nav.querySelector('.case-rail-next').disabled = current === cards.length - 1;
        });
      }, {passive:true});
      nav.querySelector('.case-rail-prev').disabled = true;
    });
  }

  const exhibit = document.querySelector('.painting-exhibition');
  if (exhibit) {
    const stage = exhibit.querySelector('[data-exhibit-stage]');
    const pieces = [...exhibit.querySelectorAll('[data-painting-panel]')];
    const choices = [...exhibit.querySelectorAll('[data-painting-choice]')];
    let current = 0;
    function show(index, center = false) {
      current = (index + pieces.length) % pieces.length;
      pieces.forEach((piece, i) => {
        const active = i === current;
        piece.classList.toggle('is-active', active);
        piece.inert = !active;
        piece.setAttribute('aria-hidden', String(!active));
      });
      choices.forEach((button, i) => {
        const active = i === current;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', String(active));
        if (active && center) button.scrollIntoView({behavior: reduced.matches ? 'instant' : 'smooth', inline:'center', block:'nearest'});
      });
      stage.style.setProperty('--exhibit-progress', String((current + 1) / pieces.length));
      const title = choices[current]?.textContent.trim().replace(/^\d+/, '').trim();
      stage.setAttribute('aria-label', title + ', painting ' + (current + 1) + ' of ' + pieces.length + '. Use left and right arrow keys.');
      pieces[(current + 1) % pieces.length]?.querySelector('img')?.setAttribute('loading','eager');
    }
    const requested = new URLSearchParams(location.search).get('piece')?.toLowerCase();
    const requestedIndex = choices.findIndex(button => button.textContent.trim().toLowerCase().endsWith(requested || '\0'));
    if (requestedIndex >= 0) show(requestedIndex, true);
    choices.forEach(button => button.addEventListener('click', () => show(Number(button.dataset.paintingChoice), true)));
    exhibit.querySelector('[data-painting-previous]')?.addEventListener('click', () => show(current - 1, true));
    exhibit.querySelector('[data-painting-next]')?.addEventListener('click', () => show(current + 1, true));
    stage?.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        show(current + (e.key === 'ArrowRight' ? 1 : -1), true);
      }
    });
    let startX = null;
    let suppressClickUntil = 0;
    stage?.addEventListener('click', e => {
      if (performance.now() < suppressClickUntil && e.target.closest('.exhibit-image')) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);
    stage?.addEventListener('pointerdown', e => {
      if (e.pointerType === 'touch') startX = e.clientX;
    }, {passive:true});
    stage?.addEventListener('pointerup', e => {
      if (startX === null) return;
      const movement = e.clientX - startX;
      startX = null;
      if (Math.abs(movement) > 38) {
        suppressClickUntil = performance.now() + 350;
        show(current + (movement < 0 ? 1 : -1), true);
      }
    }, {passive:true});
    stage?.addEventListener('pointercancel', () => {startX = null});
    if (!reduced.matches && matchMedia('(hover:hover) and (pointer:fine)').matches) {
      stage?.addEventListener('pointermove', e => {
        const r = stage.getBoundingClientRect();
        stage.style.setProperty('--paint-x', ((e.clientX-r.left-r.width/2)*.012).toFixed(1)+'px');
        stage.style.setProperty('--paint-y', ((e.clientY-r.top-r.height/2)*.01).toFixed(1)+'px');
      }, {passive:true});
      stage?.addEventListener('pointerleave', () => {
        stage.style.setProperty('--paint-x','0px');
        stage.style.setProperty('--paint-y','0px');
      });
    }
    show(0);
  }
})();
