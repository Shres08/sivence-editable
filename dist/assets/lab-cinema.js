/* One film at a time. Scrolling advances the stage without trapping the page. */
(() => {
  const section = document.querySelector('.lab-cinema');
  if (!section) return;
  const panels = [...section.querySelectorAll('.cinema-panel')];
  const videos = panels.map(panel => panel.querySelector('video'));
  const jumps = [...section.querySelectorAll('[data-film-jump]')];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let active = -1;
  let playing = null;
  let queued = false;

  if (reduced.matches) {
    panels.forEach(panel => {
      panel.inert = false;
      panel.setAttribute('aria-hidden', 'false');
    });
    return; // Native controls remain available; no automatic motion.
  }

  function stop(video, rewind = false) {
    video.pause();
    video.muted = true;
    if (rewind) {
      try { video.currentTime = 0; } catch (_) { /* metadata may not be ready */ }
    }
    if (playing === video) playing = null;
  }

  async function play(video) {
    if (document.hidden || active < 0 || videos[active] !== video) return;
    video.muted = true;
    try {
      await video.play();
      if (active < 0 || videos[active] !== video || document.hidden) {
        stop(video);
        return;
      }
      playing = video;
    } catch (_) { /* Leave the poster and native playback controls available. */ }
  }

  function select(index) {
    if (!panels[index]) return;
    if (index !== active) {
      videos.forEach((video, i) => { if (i !== index) stop(video, true); });
      active = index;
      panels.forEach((panel, i) => {
        const shown = i === index;
        panel.classList.toggle('active', shown);
        panel.inert = !shown;
        panel.setAttribute('aria-hidden', String(!shown));
      });
      jumps.forEach((button, i) => {
        if (i === index) button.setAttribute('aria-current', 'true');
        else button.removeAttribute('aria-current');
      });
      section.style.setProperty('--film-progress', String((index + 1) / panels.length));
    }
    if (playing !== videos[index]) play(videos[index]);
  }

  function frame() {
    queued = false;
    const rect = section.getBoundingClientRect();
    const onStage = rect.top <= innerHeight * .55 && rect.bottom >= innerHeight * .45;
    if (!onStage) {
      videos.forEach(video => stop(video));
      return;
    }
    const distance = Math.max(1, rect.height - innerHeight);
    const progress = Math.max(0, Math.min(.99999, -rect.top / distance));
    select(Math.min(panels.length - 1, Math.floor(progress * panels.length)));
  }
  function queue() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(frame);
  }
  addEventListener('scroll', queue, {passive:true});
  addEventListener('resize', queue);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) videos.forEach(video => stop(video));
    else queue();
  });
  addEventListener('pagehide', () => videos.forEach(video => stop(video)));
  queue();

  jumps.forEach((button, index) => button.addEventListener('click', () => {
    const distance = section.offsetHeight - innerHeight;
    scrollTo({
      top: section.getBoundingClientRect().top + scrollY +
        distance * (index + .12) / panels.length,
      behavior: 'smooth'
    });
    select(index);
  }));

})();
