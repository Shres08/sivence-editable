(() => {
  const object = document.querySelector('.spatial-object');
  if (!object) return;
  const frame = object.querySelector('iframe');
  if (!frame) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let visible = true;
  function send(action, values = {}) {
    frame.contentWindow?.postMessage({scope: 'sivence-hero', action, ...values}, location.origin);
  }
  function applyPause() {
    send('pause', {value: reduced.matches});
  }
  function aim(event) {
    const rect = object.getBoundingClientRect();
    send('aim', {x: (event.clientX - rect.left) / rect.width, y: (event.clientY - rect.top) / rect.height});
  }
  object.addEventListener('pointermove', aim, {passive: true});
  object.addEventListener('pointerleave', () => send('leave'));
  function pulse() {
    send('pulse');
    document.dispatchEvent(new Event('sivence-interaction'));
  }
  object.addEventListener('click', event => { aim(event); pulse(); });
  document.querySelector('[data-signal-pulse]')?.addEventListener('click', pulse);
  reduced.addEventListener('change', applyPause);
  addEventListener('message', event => {
    if (event.origin !== location.origin || event.source !== frame.contentWindow || event.data?.scope !== 'sivence-hero-ready') return;
    applyPause();
    send('visible', {value: visible});
  });
  new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    if (visible && !frame.getAttribute('src') && frame.dataset.src) frame.src = frame.dataset.src;
    send('visible', {value: visible});
  }).observe(object);
  applyPause();
})();
