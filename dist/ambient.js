/* Subtle artwork-led lighting. No image pixels, text or navigation are altered. */
(() => {
  const family = document.body.dataset.ambient;
  if (!family) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const selectors = {
    home: '.theatre-pin, .think, .paint-feature',
    work: '.work-stage',
    case: '.case-cover, .case-artifacts .artifact-grid',
    thinking: '.method-feature, .method-film',
    article: '.article-illustration, .article-diagram',
    about: '.about-hero figure',
    contact: '.contact-form',
    lab: '.lab-grid',
    'lab-detail': '.lab-detail > .artifact, .lab-detail > .artifact-grid, .lab-detail > .film, .exhibit-stage'
  };
  const zones = [...document.querySelectorAll(selectors[family] || '')];
  zones.forEach(zone => zone.classList.add('ambient-zone'));

  if (reduced.matches || !('IntersectionObserver' in window)) {
    zones.forEach(zone => zone.classList.add('is-lit'));
  } else {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.target.classList.toggle('is-lit', entry.isIntersecting));
    }, {rootMargin:'0px 0px -8% 0px', threshold:0.01});
    zones.forEach(zone => observer.observe(zone));
  }

  if (!reduced.matches && finePointer.matches) {
    zones.forEach(zone => {
      let frame = 0, x = 0, y = 0;
      zone.addEventListener('pointermove', event => {
        const rect = zone.getBoundingClientRect();
        x = Math.max(-12, Math.min(12, (event.clientX - rect.left - rect.width / 2) * .018));
        y = Math.max(-10, Math.min(10, (event.clientY - rect.top - rect.height / 2) * .018));
        if (frame) return;
        frame = requestAnimationFrame(() => {
          zone.style.setProperty('--wash-x', x.toFixed(1) + 'px');
          zone.style.setProperty('--wash-y', y.toFixed(1) + 'px');
          frame = 0;
        });
      }, {passive:true});
      zone.addEventListener('pointerleave', () => {
        zone.style.setProperty('--wash-x', '0px');
        zone.style.setProperty('--wash-y', '0px');
      });
    });
  }

  const projects = {
    camfire:['#a5744d','#d29a63'],
    remic:['#416ac1','#df8849'],
    minimalance:['#9c8064','#bcb6a2'],
    incuse:['#527e9b','#c48261'],
    xipster:['#508c98','#d97e5c'],
    'nett-technologies':['#628a79','#b09b72'],
    'bhatt-bros-alea':['#aa7659','#c2a17a'],
    soaltech:['#559a92','#92bab0'],
    autoreel:['#6574a3','#9787ad']
  };
  const paintings = [
    ['#7d9a75','#c8b091'], ['#718ea5','#c1a68e'],
    ['#a96d55','#c4a77c'], ['#a37d81','#c4a19e'],
    ['#77949a','#c8b3a5'], ['#858b83','#b5ab98']
  ];
  function palette(zone, pair) {
    if (!zone || !pair) return;
    zone.style.setProperty('--wash-a', pair[0]);
    zone.style.setProperty('--wash-b', pair[1]);
  }
  function watchActive(items, target, getPalette) {
    if (!items.length || !target) return;
    let frame = 0;
    const update = () => {
      frame = 0;
      const index = items.findIndex(item => item.classList.contains('is-active') || item.classList.contains('active'));
      if (index >= 0) palette(target, getPalette(items[index], index));
    };
    const observer = new MutationObserver(() => {
      if (!frame) frame = requestAnimationFrame(update);
    });
    items.forEach(item => observer.observe(item, {attributes:true, attributeFilter:['class']}));
    update();
  }

  if (family === 'case' && document.body.dataset.project === 'remic') {
    const groups = [...document.querySelectorAll('.case-artifacts .artifact-grid')];
    const sequence = [
      ['#416ac1','#df8849'], ['#ba8264','#d9ab71'],
      ['#c27958','#d6ae83'], ['#7f988c','#c2a085'],
      ['#4f7b9b','#b49375']
    ];
    groups.forEach((group, index) => palette(group, sequence[index]));
  }
  if (family === 'case' && document.body.dataset.project === 'xipster') {
    document.querySelectorAll('.case-artifacts .artifact-grid').forEach((group, index) =>
      palette(group, index ? ['#b57560','#d6a084'] : projects.xipster));
  }

  if (family === 'work') {
    const stage = document.querySelector('.work-stage');
    watchActive([...document.querySelectorAll('.work-panel')], stage,
      panel => projects[panel.dataset.casePanel]);
  }
  if (family === 'home') {
    const order = ['remic','camfire','minimalance','xipster','nett-technologies','incuse','bhatt-bros-alea','soaltech','autoreel'];
    watchActive([...document.querySelectorAll('.theatre .chapter')],
      document.querySelector('.theatre-pin'), (_chapter, index) => projects[order[index]]);

    const rail = document.querySelector('.painting-rail');
    const feature = document.querySelector('.paint-feature');
    const tiles = [...(rail?.querySelectorAll('.painting-tile') || [])];
    let frame = 0, last = -1;
    const updatePainting = () => {
      frame = 0;
      if (!rail || !tiles.length) return;
      const left = rail.getBoundingClientRect().left;
      const index = tiles.reduce((best, tile, i) =>
        Math.abs(tile.getBoundingClientRect().left - left) <
        Math.abs(tiles[best].getBoundingClientRect().left - left) ? i : best, 0);
      if (index !== last) { palette(feature, paintings[index]); last = index; }
    };
    rail?.addEventListener('scroll', () => {
      if (!frame) frame = requestAnimationFrame(updatePainting);
    }, {passive:true});
    updatePainting();
  }
  if (family === 'lab-detail' && document.body.dataset.project === 'paintings') {
    watchActive([...document.querySelectorAll('.exhibit-choice')],
      document.querySelector('.exhibit-stage'), (_choice, index) => paintings[index]);
  }
})();
