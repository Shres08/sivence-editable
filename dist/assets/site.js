/* Sivence homepage, immersive edition.
   Needs three.js r128 + RoomEnvironment (for the hero) and Lenis (smooth scroll). Each part checks for its
   dependency and the page still reads fully without any of them. */
(function () {
  var legacy = {work:'/work/',about:'/about/',contact:'/contact/','case-camfire':'/work/camfire/','case-remic':'/work/remic/','case-minimalance':'/work/minimalance/','case-xipster':'/work/xipster/','case-radhe':'/lab/radhe-dhokla/','project-experiments':'/lab/'}; if(legacy[location.hash.slice(1)]) location.replace(legacy[location.hash.slice(1)]);
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* Rolling letters: wrap every character of [data-roll] */
  $$('[data-roll]').forEach(function (el) {
    var t = el.textContent, owner = el.closest('a,button'); if(owner && !owner.hasAttribute('aria-label')) owner.setAttribute('aria-label', owner.textContent.trim().replace(/\s+/g, ' ')); el.setAttribute('aria-label', t); el.textContent = '';
    for (var i = 0; i < t.length; i++) {
      var s = document.createElement('span'); s.className = 'ch'; s.style.setProperty('--i', i);
      s.setAttribute('aria-hidden', 'true'); s.textContent = t[i]; el.appendChild(s);
    }
  });

  /* Headline: wrap words (keeps <em>) for the staggered rise */
  var wi = 0;
  function splitWords(node, cls) {
    Array.prototype.slice.call(node.childNodes).forEach(function (c) {
      if (c.nodeType === 3) {
        var frag = document.createDocumentFragment();
        c.textContent.split(/(\s+)/).forEach(function (w) {
          if (!w) return;
          if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(' ')); return; }
          var o = document.createElement('span'); o.className = cls;
          if (cls === 'w') { var i = document.createElement('span'); i.textContent = w; i.style.setProperty('--i', wi++); o.appendChild(i); }
          else o.textContent = w;
          frag.appendChild(o);
        });
        node.replaceChild(frag, c);
      } else if (c.nodeType === 1) splitWords(c, cls);
    });
  }
  $$('[data-split]').forEach(function (el) { splitWords(el, 'w'); });
  $$('[data-words]').forEach(function (el) { splitWords(el, 'wd'); });
  requestAnimationFrame(function () { document.documentElement.classList.add('is-ready'); });

  /* Smooth scroll */
  var lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ lerp: 0.09, smoothWheel: true });
    (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(performance.now());
  }

  /* Menu */
  var btn = $('.menu-btn'), menu = $('#menu'), main = $('main'), footer = $('.foot');
  function setMenu(open) {
    document.body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false'); if(main) main.inert = open; if(footer) footer.inert = open; menu.inert = !open;
    if (open) { menu.hidden = false; if (lenis) lenis.stop(); setTimeout(function () { var a = $('a', menu); if (a) a.focus(); }, 300); }
    else { if (lenis) lenis.start(); setTimeout(function () { if (!document.body.classList.contains('menu-open')) menu.hidden = true; }, 700); }
  }
  if (btn && menu) {
    btn.addEventListener('click', function () { setMenu(!document.body.classList.contains('menu-open')); });
    document.addEventListener('keydown', function (e) {
      if (!document.body.classList.contains('menu-open')) return;
      if (e.key === 'Escape') { setMenu(false); btn.focus(); }
      if (e.key === 'Tab') {
        var items = [btn].concat($$('a[href]', menu)), first = items[0], last = items[items.length-1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
        else if(items.indexOf(document.activeElement)<0){e.preventDefault();first.focus();}
      }
    });
    menu.addEventListener('click', function(e){if(e.target.closest('a'))setMenu(false);});
  }

  /* Cursor */
  var cur = $('.cursor'), cx = 0, cy = 0, tx = 0, ty = 0;
  if (fine && cur && !reduce) {
    window.addEventListener('pointermove', function (e) { tx = e.clientX; ty = e.clientY; }, { passive: true });
    document.addEventListener('pointerover', function (e) { cur.classList.toggle('is-link', !!e.target.closest('a,button')); });
    (function loop() { cx += (tx - cx) * 0.2; cy += (ty - cy) * 0.2; cur.style.transform = 'translate(' + cx + 'px,' + cy + 'px)'; requestAnimationFrame(loop); })();
  } else if (cur) cur.remove();

  /* Scroll-driven: scrubbed words, header colour, count-ups */
  var top = $('.top'), darks = $$('.spatial-hero, .theatre, .signal-story, .lab-spotlight, .close, .foot'), scrubs = $$('[data-words]');
  function onScroll() {
    var vh = window.innerHeight;
    scrubs.forEach(function (el) {
      var r = el.getBoundingClientRect(), words = el._w || (el._w = $$('.wd', el));
      var p = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.3)));
      var n = Math.round(p * words.length * 1.15);
      words.forEach(function (w, i) { w.classList.toggle('on', i < n); });
    });
    var onDark = darks.some(function (d) { var r = d.getBoundingClientRect(); return r.top <= 44 && r.bottom >= 44; });
    if (top) top.classList.toggle('on-dark', onDark);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); onScroll();

  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) {
        if (!e.isIntersecting) return; io.unobserve(e.target);
        var el = e.target, target = parseFloat(el.dataset.count), dec = el.dataset.count.indexOf('.') > -1, t0 = performance.now();
        (function step(now) {
          var k = Math.min(1, (now - t0) / 1300), v = target * (1 - Math.pow(1 - k, 3));
          el.textContent = (el.dataset.pre || '') + (dec ? v.toFixed(1) : Math.round(v).toLocaleString('en-CA')) + (el.dataset.suf || '');
          if (k < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, { threshold: 0.6 });
    $$('[data-count]').forEach(function (el) { io.observe(el); });
  }

  /* Work rows: preview card follows the cursor */
  var prev = $('.preview'), pin = $('.preview-in');
  if (fine && prev && !reduce) {
    var px = 0, py = 0, qx = 0, qy = 0, running = false;
    function follow() { qx += (px - qx) * 0.14; qy += (py - qy) * 0.14; prev.style.left = qx + 'px'; prev.style.top = qy + 'px'; if (running) requestAnimationFrame(follow); }
    $$('[data-rows] a').forEach(function (a) {
      a.addEventListener('pointerenter', function (e) {
        var src = a.dataset.preview || '';
        if (src.indexOf('tile:') === 0) { pin.style.backgroundImage = 'none'; pin.textContent = src.slice(5); }
        else { pin.textContent = ''; pin.style.backgroundImage = 'url("' + src + '")'; }
        if (!running) { qx = px = e.clientX; qy = py = e.clientY; running = true; follow(); }
        prev.classList.add('on');
      });
      a.addEventListener('pointermove', function (e) { px = e.clientX; py = e.clientY; });
      a.addEventListener('pointerleave', function () { prev.classList.remove('on'); });
    });
    $('[data-rows]').addEventListener('pointerleave', function () { running = false; });
  }

  /* Hero 3D scene: glossy signal objects with soft physics.
     The cursor shoves them; scrolling pulls them out of chaos into one ordered line of evidence. */
  /* Version 28 fallback. Kept intact so the original ball-and-ring scene can be
     restored by switching the final bootstrap call to startRingScene(). */
  function startRingScene() {
    var canvas = $('[data-scene]'), hero = $('[data-hero]');
    if (!canvas || !window.THREE) return;
    var T = window.THREE, renderer;
    try { renderer = new T.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true }); } catch (e) { return; }
    hero.classList.add('scene-ready');
    canvas.addEventListener('webglcontextlost', function () { hero.classList.remove('scene-ready'); }, { once: true });
    var small = window.innerWidth < 760;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, small ? 1.5 : 2));
    renderer.outputEncoding = T.sRGBEncoding;
    renderer.toneMapping = T.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
    var scene = new T.Scene(), camera = new T.PerspectiveCamera(32, 1, 0.1, 100);
    camera.position.set(0, 0, 22);
    if (T.RoomEnvironment) { var pm = new T.PMREMGenerator(renderer); scene.environment = pm.fromScene(new T.RoomEnvironment(), 0.04).texture; }
    scene.add(new T.AmbientLight(0xffffff, 0.35));
    var key = new T.DirectionalLight(0xffffff, 1.4); key.position.set(6, 9, 10); scene.add(key);
    var rim = new T.DirectionalLight(0xffb08a, 0.6); rim.position.set(-8, -4, 4); scene.add(rim);

    var mats = {
      ink: new T.MeshPhysicalMaterial({ color: new T.Color(0x121311).convertSRGBToLinear(), roughness: 0.22, metalness: 0.1, clearcoat: 1, clearcoatRoughness: 0.08 }),
      paper: new T.MeshPhysicalMaterial({ color: new T.Color(0xf2f2ee).convertSRGBToLinear(), roughness: 0.32, metalness: 0, clearcoat: 0.6 }),
      orange: new T.MeshPhysicalMaterial({ color: new T.Color(0xff5a1f).convertSRGBToLinear(), roughness: 0.28, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.12 }),
      chrome: new T.MeshPhysicalMaterial({ color: new T.Color(0xd7d8d2).convertSRGBToLinear(), roughness: 0.12, metalness: 1 })
    };
    var geos = { ball: new T.SphereGeometry(1, 48, 48), ring: new T.TorusGeometry(0.72, 0.3, 32, 96), pill: T.CapsuleGeometry ? new T.CapsuleGeometry(0.55, 1, 16, 32) : new T.SphereGeometry(1, 48, 48) };
    var plan = small
      ? [['ink', 6], ['paper', 5], ['orange', 3], ['chrome', 2]]
      : [['ink', 9], ['paper', 8], ['orange', 5], ['chrome', 4]];
    var bodies = [];
    plan.forEach(function (pair) {
      for (var k = 0; k < pair[1]; k++) {
        var kind = Math.random() < 0.6 ? 'ball' : (Math.random() < 0.6 ? 'ring' : 'pill');
        var r = kind === 'ball' ? 0.55 + Math.random() * 0.95 : 0.9 + Math.random() * 0.4;
        var m = new T.Mesh(geos[kind], mats[pair[0]]);
        m.scale.setScalar(kind === 'ball' ? r : r * 1.05);
        m.rotation.set(Math.random() * 6, Math.random() * 6, 0);
        scene.add(m);
        bodies.push({ m: m, r: r, p: new T.Vector3(), v: new T.Vector3(), home: new T.Vector3(), scatter: new T.Vector3(), line: new T.Vector3(), spin: new T.Vector3((Math.random() - .5) * .6, (Math.random() - .5) * .6, 0), ph: Math.random() * 6.28 });
      }
    });
    function layout() {
      var w = canvas.clientWidth, h = canvas.clientHeight, aspect = w / h;
      var halfH = Math.tan((camera.fov * Math.PI / 180) / 2) * camera.position.z, halfW = halfH * aspect;
      bodies.forEach(function (b, i) {
        // scatter: weighted to the right half and the edges so the headline stays readable
        var corner = i % 7 === 0;
        b.scatter.set(
          corner ? -halfW * (0.75 + Math.random() * 0.2) : (0.12 + Math.random() * 0.82) * halfW,
          corner ? -halfH * (0.75 + Math.random() * 0.15) : (Math.random() * 2 - 1) * halfH * 0.85,
          (Math.random() * 2 - 1) * 3 - 1);
        if (small) b.scatter.set((Math.random() * 2 - 1) * halfW * 0.9, (Math.random() < .5 ? -1 : 1) * (halfH * (0.45 + Math.random() * 0.45)), (Math.random() * 2 - 1) * 2 - 1);
      });
      var sorted = bodies.slice().sort(function (a, b) { return a.scatter.x - b.scatter.x; });
      sorted.forEach(function (b, i) {
        var t = sorted.length > 1 ? i / (sorted.length - 1) : .5;
        b.line.set(-halfW * 0.92 + t * halfW * 1.84, -halfH * 0.62, 0);
      });
      bodies.forEach(function (b) { if (!b.placed) { b.p.copy(b.scatter); b.placed = true; } });
    }
    function resize() {
      var w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); layout();
    }
    window.addEventListener('resize', resize); resize();

    var ptr = new T.Vector3(999, 999, 0), last = new T.Vector3(999, 999, 0), pv = new T.Vector3(), active = false;
    var ray = new T.Raycaster(), plane = new T.Plane(new T.Vector3(0, 0, 1), 0), ndc = new T.Vector2(), cam = { x: 0, y: 0 };
    hero.addEventListener('pointermove', function (e) {
      var r = canvas.getBoundingClientRect();
      ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
      ray.setFromCamera(ndc, camera); ray.ray.intersectPlane(plane, ptr); if(!active) last.copy(ptr); active = true;
    }, { passive: true });
    hero.addEventListener('pointerleave', function () { active = false; });

    var order = 0, tmp = new T.Vector3();
    function step(t, dt) {
      var target = Math.min(1, Math.max(0, window.scrollY / (hero.offsetHeight * 0.75)));
      order += (target - order) * 0.08;
      var e = order * order * (3 - 2 * order);
      pv.subVectors(ptr, last).multiplyScalar(1 / Math.max(dt, 0.008)).clampLength(0, 30); last.copy(ptr);
      for (var i = 0; i < bodies.length; i++) {
        var b = bodies[i];
        b.home.lerpVectors(b.scatter, b.line, e);
        b.home.y += Math.sin(t * 0.6 + b.ph) * 0.25 * (1 - e);
        tmp.subVectors(b.home, b.p).multiplyScalar(2.2 * dt);
        b.v.add(tmp);
        if (active) {
          tmp.subVectors(b.p, ptr); tmp.z *= 0.3;
          var d = tmp.length(), R = 2.4 + b.r;
          if (d < R && d > 0.0001) {
            tmp.multiplyScalar((R - d) / d * 9 * dt); b.v.add(tmp);
            b.v.addScaledVector(pv, 0.015 * (R - d) / R);
          }
        }
        b.v.multiplyScalar(Math.pow(0.06, dt));
      }
      for (var a = 0; a < bodies.length; a++) for (var c = a + 1; c < bodies.length; c++) {
        var A = bodies[a], B = bodies[c]; tmp.subVectors(A.p, B.p);
        var dist = tmp.length(), min = (A.r + B.r) * (1 - e * 0.35);
        if (dist < min && dist > 0.0001) { tmp.multiplyScalar((min - dist) / dist * 0.5); A.p.add(tmp); B.p.sub(tmp); }
      }
      for (var j = 0; j < bodies.length; j++) {
        var q = bodies[j];
        q.p.addScaledVector(q.v, dt);
        q.m.position.copy(q.p);
        var sp = 1 + q.v.length() * 0.6;
        q.m.rotation.x += q.spin.x * dt * sp; q.m.rotation.y += q.spin.y * dt * sp;
        q.m.scale.setScalar((q.m.geometry === geos.ball ? q.r : q.r * 1.05) * (1 - e * 0.35));
      }
      cam.x += ((active ? ndc.x : 0) * 0.8 - cam.x) * 0.04; cam.y += ((active ? ndc.y : 0) * 0.5 - cam.y) * 0.04;
      camera.position.x = cam.x; camera.position.y = cam.y; camera.lookAt(0, 0, 0);
      renderer.render(scene, camera);
    }
    if (reduce) { step(0, 0.016); return; }
    var visible = true, prevT = performance.now();
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }).observe(hero);
    (function loop(now) {
      requestAnimationFrame(loop);
      var dt = Math.min(0.033, (now - prevT) / 1000); prevT = now;
      if (visible && !document.hidden) step(now / 1000, dt);
    })(prevT);
  }
  /* Hero 3D scene: four business inputs resolve into one Sivence direction.
     Cursor proximity aligns the planes; scroll completes the resolution. */
  function startScene() {
    var canvas = $('[data-scene]'), hero = $('[data-hero]');
    if (!canvas || !hero || !window.THREE) return;
    var T = window.THREE, renderer;
    try { renderer = new T.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true }); } catch (e) { return; }
    hero.classList.add('scene-ready');
    canvas.addEventListener('webglcontextlost', function () { hero.classList.remove('scene-ready'); }, { once: true });
    var small = window.innerWidth < 760;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, small ? 1.35 : 1.8));
    renderer.outputEncoding = T.sRGBEncoding;
    renderer.toneMapping = T.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.04;

    var scene = new T.Scene(), camera = new T.PerspectiveCamera(34, 1, 0.1, 100);
    camera.position.set(0, 0, 18);
    if (T.RoomEnvironment) {
      var pm = new T.PMREMGenerator(renderer);
      scene.environment = pm.fromScene(new T.RoomEnvironment(), 0.04).texture;
    }
    scene.add(new T.HemisphereLight(0xffffff, 0x565656, 1.15));
    var key = new T.DirectionalLight(0xffffff, 1.8); key.position.set(5, 7, 9); scene.add(key);
    var warm = new T.PointLight(0xff5a1f, 1.2, 22); warm.position.set(4, -1, 5); scene.add(warm);

    var group = new T.Group(); scene.add(group);
    var orange = 0xff5a1f;
    var planeGeo = new T.BoxGeometry(4.5, 6.7, 0.055);
    var edgeGeo = new T.EdgesGeometry(planeGeo);
    var inputs = [
      { label: 'Customer', x: -2.4, y: .85, ry: -.55, rz: -.08 },
      { label: 'Brand', x: -.8, y: -.35, ry: -.18, rz: .045 },
      { label: 'Data', x: .9, y: .42, ry: .22, rz: -.035 },
      { label: 'Commercial', x: 2.55, y: -.2, ry: .58, rz: .075 }
    ];
    var planes = [];
    function labelSprite(text) {
      var c = document.createElement('canvas'), x = c.getContext('2d');
      c.width = 512; c.height = 96;
      x.font = '500 32px Arial, sans-serif'; x.fillStyle = '#565656'; x.fillText(text, 10, 55);
      var tex = new T.CanvasTexture(c); tex.minFilter = T.LinearFilter;
      var s = new T.Sprite(new T.SpriteMaterial({ map: tex, transparent: true, depthTest: false, opacity: .72 }));
      s.scale.set(2.45, .46, 1); return s;
    }
    inputs.forEach(function (d, i) {
      var mat = new T.MeshPhysicalMaterial({
        color: i % 2 ? 0xc7c7c7 : 0x303130,
        transparent: true, opacity: i % 2 ? .12 : .17,
        roughness: .16, metalness: .08, clearcoat: 1, clearcoatRoughness: .08,
        side: T.DoubleSide, depthWrite: false
      });
      if ('transmission' in mat) { mat.transmission = .72; mat.thickness = .28; mat.ior = 1.34; }
      var mesh = new T.Mesh(planeGeo, mat);
      var edges = new T.LineSegments(edgeGeo, new T.LineBasicMaterial({ color: i === 3 ? orange : 0x222321, transparent: true, opacity: i === 3 ? .72 : .34 }));
      mesh.add(edges);
      var label = labelSprite(d.label); label.position.set(-1.65, 3.65, .12); mesh.add(label);
      group.add(mesh); planes.push({ mesh: mesh, data: d, label: label });
    });

    var mark = new T.Group(); group.add(mark);
    var markMat = new T.MeshPhysicalMaterial({ color: orange, emissive: 0x7a1600, emissiveIntensity: .22, roughness: .22, clearcoat: 1, transparent: true, opacity: 0 });
    var barGeo = new T.BoxGeometry(.26, 2.8, .22);
    var topBar = new T.Mesh(barGeo, markMat), bottomBar = new T.Mesh(barGeo, markMat);
    topBar.rotation.z = -.72; topBar.position.set(-.42, .86, .62);
    bottomBar.rotation.z = .72; bottomBar.position.set(.42, -.86, .62);
    mark.add(topBar); mark.add(bottomBar);

    var pointer = { x: 1, y: 1, active: false }, smooth = { x: 0, y: 0 }, alignment = 0;
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      pointer.x = ((e.clientX - r.left) / r.width) * 2 - 1;
      pointer.y = -(((e.clientY - r.top) / r.height) * 2 - 1);
      pointer.active = true;
    }, { passive: true });
    hero.addEventListener('pointerleave', function () { pointer.active = false; });

    function resize() {
      var w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
      small = w < 760;
      group.scale.setScalar(small ? .63 : 1);
      group.position.set(small ? 1.15 : 3.55, small ? -1.55 : .1, 0);
    }
    window.addEventListener('resize', resize); resize();

    function step(t) {
      var scroll = Math.min(1, Math.max(0, window.scrollY / Math.max(1, hero.offsetHeight * .72)));
      var proximity = pointer.active ? Math.max(0, 1 - Math.sqrt(Math.pow(pointer.x - .38, 2) + pointer.y * pointer.y) / .95) : 0;
      var target = Math.max(scroll, proximity);
      alignment += (target - alignment) * (reduce ? 1 : .075);
      var ease = alignment * alignment * (3 - 2 * alignment);
      smooth.x += ((pointer.active ? pointer.x : 0) - smooth.x) * .045;
      smooth.y += ((pointer.active ? pointer.y : 0) - smooth.y) * .045;
      planes.forEach(function (p, i) {
        var d = p.data, spread = 1 - ease;
        p.mesh.position.x = d.x * spread;
        p.mesh.position.y = d.y * spread;
        p.mesh.position.z = (i - 1.5) * .38 * spread;
        p.mesh.rotation.y = d.ry * spread + smooth.x * .035;
        p.mesh.rotation.z = d.rz * spread;
        p.mesh.rotation.x = -smooth.y * .025;
        p.label.material.opacity = .72 * spread;
      });
      markMat.opacity = Math.max(0, (ease - .42) / .58) * .95;
      mark.rotation.y = smooth.x * .08;
      mark.position.y = -scroll * 1.15;
      group.rotation.y = smooth.x * .08;
      group.rotation.x = -smooth.y * .045;
      warm.intensity = .55 + ease * 1.15;
      camera.position.x = smooth.x * .28; camera.position.y = smooth.y * .16; camera.lookAt(0, 0, 0);
      renderer.render(scene, camera);
    }
    if (reduce) { alignment = 1; step(0); return; }
    var visible = true;
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }).observe(hero);
    (function loop(now) { requestAnimationFrame(loop); if (visible && !document.hidden) step(now / 1000); })(performance.now());
  }
  var heroScene = new URLSearchParams(window.location.search).get('hero') === 'planes' ? startScene : startRingScene;
  if (window.THREE) heroScene(); else window.addEventListener('load', heroScene);
})();
