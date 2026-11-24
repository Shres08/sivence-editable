/* No rendering loop, external dependencies, audio downloads or autoplay. */
(() => {
  'use strict';
  const stage = document.querySelector('.human-stage');
  if (!stage) return;
  const exhibit = stage.closest('.human-exhibit');
  const pieces = [...stage.querySelectorAll('[data-fragment]')];
  const image = stage.querySelector('img');
  const live = stage.querySelector('output');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const sound = exhibit.querySelector('[data-human-sound]');
  const pause = exhibit.querySelector('[data-human-motion]');
  const replay = exhibit.querySelector('[data-human-replay]');
  const help = exhibit.querySelector('[data-human-help]');
  let context, enabled = false, paused = reduced.matches, lastTone = 0, frame = 0, assemblyTimer;
  const isQuiet = () => paused || reduced.matches || document.hidden;
  function tip(button, text) {
    button.setAttribute('aria-label', text);
    button.title = text;
    button.dataset.tip = text;
  }
  function tone(index = 0) {
    if (!enabled || !context || document.hidden || context.state !== 'running') return;
    const now = context.currentTime;
    if (now - lastTone < .15) return;
    lastTone = now;
    // A soft pair of harmonics with a short attack and a rounded, quiet decay.
    [1, 2.002].forEach((ratio, i) => {
      const osc = context.createOscillator();
      const gain = context.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime([261.63, 293.66, 329.63, 392, 440][index % 5] * ratio, now);
      gain.gain.setValueAtTime(0, now);
      gain.gain.linearRampToValueAtTime(i ? .003 : .013, now + .018);
      gain.gain.exponentialRampToValueAtTime(.0001, now + .36);
      osc.connect(gain).connect(context.destination);
      osc.start(now); osc.stop(now + .38);
      osc.onended = () => { osc.disconnect(); gain.disconnect(); };
    });
  }
  sound.addEventListener('click', async () => {
    if (enabled) {
      enabled = false;
      sound.setAttribute('aria-pressed', 'false');
      tip(sound, 'Enable interaction sounds');
      await context?.suspend().catch(() => {});
      return;
    }
    try {
      const Audio = window.AudioContext || window.webkitAudioContext;
      if (!Audio) throw new Error('Audio unavailable');
      context ||= new Audio();
      await context.resume();
      enabled = true;
      sound.setAttribute('aria-pressed', 'true');
      tip(sound, 'Mute interaction sounds');
      tone(3);
    } catch (_) {
      enabled = false;
      sound.setAttribute('aria-pressed', 'false');
      tip(sound, 'Interaction sounds unavailable');
    }
  });
  function clear(piece) {
    piece.classList.remove('is-active');
    piece.setAttribute('aria-pressed', 'false');
    piece.style.removeProperty('--tilt-x');
    piece.style.removeProperty('--tilt-y');
  }
  function reveal(piece, announce = false) {
    if (!piece.classList.contains('is-active')) tone(Number(piece.dataset.fragment));
    piece.classList.add('is-active');
    piece.setAttribute('aria-pressed', 'true');
    if (announce) live.textContent = piece.getAttribute('aria-label');
  }
  let touchWasActive = false, touchFocus = false;
  pieces.forEach(piece => {
    piece.addEventListener('pointerdown', event => {
      touchFocus = event.pointerType === 'touch';
      touchWasActive = piece.classList.contains('is-active');
    }, {passive:true});
    piece.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'touch') reveal(piece);
    });
    piece.addEventListener('pointermove', event => {
      if (event.pointerType === 'touch' || isQuiet() || frame) return;
      frame = requestAnimationFrame(() => {
        const rect = stage.getBoundingClientRect();
        piece.style.setProperty('--tilt-x', ((event.clientX - rect.left) / rect.width - .5) * 10 + 'px');
        piece.style.setProperty('--tilt-y', ((event.clientY - rect.top) / rect.height - .5) * 10 + 'px');
        frame = 0;
      });
    }, {passive: true});
    piece.addEventListener('pointerleave', event => {
      if (event.pointerType !== 'touch' && document.activeElement !== piece) clear(piece);
    });
    piece.addEventListener('focus', () => { if (!touchFocus) reveal(piece); });
    piece.addEventListener('blur', () => clear(piece));
    piece.addEventListener('click', event => {
      // Touch keeps one insight open without cancelling vertical page scrolling.
      if (event.pointerType === 'touch') {
        pieces.forEach(clear);
        if (!touchWasActive) reveal(piece, true);
      } else reveal(piece, true);
    });
    piece.addEventListener('keydown', event => {
      if (event.key === 'Escape') { clear(piece); live.textContent = ''; }
    });
  });
  function assemble() {
    clearTimeout(assemblyTimer);
    pieces.forEach(clear);
    stage.classList.remove('is-assembling');
    if (isQuiet()) return;
    // One layout read restarts only the arrival animation, never a permanent RAF.
    void stage.offsetWidth;
    stage.classList.add('is-assembling');
    assemblyTimer = setTimeout(() => stage.classList.remove('is-assembling'), 2100);
  }
  function applyMotion() {
    stage.classList.toggle('is-paused', paused || reduced.matches);
    pause.setAttribute('aria-pressed', String(paused || reduced.matches));
    tip(pause, paused || reduced.matches ? 'Resume motion' : 'Pause motion');
    if (paused || reduced.matches) {
      stage.classList.remove('is-assembling');
      clearTimeout(assemblyTimer);
    }
  }
  pause.addEventListener('click', () => {
    paused = !paused;
    applyMotion();
    if (!paused) assemble();
  });
  replay.addEventListener('click', () => { assemble(); tone(2); });
  reduced.addEventListener('change', () => { paused = reduced.matches; applyMotion(); });
  help.addEventListener('click', () => {
    const bubble = exhibit.querySelector('.human-help');
    bubble.hidden = !bubble.hidden;
    help.setAttribute('aria-expanded', String(!bubble.hidden));
  });
  help.setAttribute('aria-expanded', 'false');
  document.addEventListener('keydown', event => {
    if (event.key === 'Tab') touchFocus = false;
    if (event.key === 'Escape') {
      pieces.forEach(clear);
      exhibit.querySelector('.human-help').hidden = true;
      help.setAttribute('aria-expanded', 'false');
    }
  });
  document.addEventListener('sivence-interaction', () => tone(2));
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stage.classList.remove('is-assembling');
      context?.suspend().catch(() => {});
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
    } else if (enabled) context?.resume().catch(() => {});
  });
  function ready() {
    if (!image.naturalWidth) return;
    stage.classList.add('human-ready');
    assemble();
  }
  applyMotion();
  if (image.complete) ready(); else image.addEventListener('load', ready, {once:true});
})();
