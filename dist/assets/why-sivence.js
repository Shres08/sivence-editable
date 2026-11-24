/* The Why Sivence decision method: four sources are compared, then resolved.
   This scene is independent of the original homepage hero renderer. */
(function () {
  var host = document.querySelector('[data-why-visual]');
  var canvas = document.querySelector('[data-why-scene]');
  var controls = Array.prototype.slice.call(document.querySelectorAll('[data-why-step]'));
  var title = document.querySelector('[data-why-title]');
  var detail = document.querySelector('[data-why-detail]');
  if (!host || !canvas || !controls.length) return;
  function fallback() {
    controls.forEach(function (control, index) {
      control.addEventListener('click', function () {
        controls.forEach(function (button, n) { button.setAttribute('aria-pressed', String(n === index)); });
        host.setAttribute('data-step', String(index));
        if (title && detail) {
          title.textContent = readings[index][0];
          detail.textContent = readings[index][1];
        }
      });
    });
  }
  var readings = [
    ['Listen across sources', 'Different signals begin in different places.'],
    ['Compare what holds up', 'The strongest patterns become easier to see.'],
    ['Choose a direction', 'The evidence resolves into one clear priority.'],
    ['Learn from the result', 'The outcome informs the next decision.']
  ];
  if (!window.THREE) { fallback(); return; }

  var T = window.THREE, renderer;
  try {
    renderer = new T.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
  } catch (e) { fallback(); return; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.6));
  renderer.outputEncoding = T.sRGBEncoding;
  renderer.toneMapping = T.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.18;

  var scene = new T.Scene();
  var camera = new T.PerspectiveCamera(35, 1, .1, 60);
  camera.position.set(0, 1.2, 17);
  scene.add(new T.AmbientLight(0xffffff, .85));
  var key = new T.DirectionalLight(0xffffff, 1.8);
  key.position.set(-3, 7, 8); scene.add(key);
  var warm = new T.PointLight(0xff5a1f, 1.3, 18);
  warm.position.set(3, -1, 4); scene.add(warm);

  var assembly = new T.Group();
  scene.add(assembly);
  var locations = [-3.6, -1.25, 1.15, 3.55];
  var planeItems = [];
  var orange = new T.Color(0xff5a1f);
  var white = new T.Color(0xe8e9e4);
  var planeGeometry = new T.BoxGeometry(2.8, 5.05, .035);
  var edgeGeometry = new T.EdgesGeometry(planeGeometry);
  var dotMaterial = new T.PointsMaterial({ color: 0xaeb1ab, size: .038, transparent: true, opacity: .7 });

  locations.forEach(function (x, index) {
    var group = new T.Group();
    group.position.set(x, index % 2 ? -.13 : .18, (index - 1.5) * .36);
    group.rotation.y = [-.32, .25, -.22, .31][index];
    var surface = new T.Mesh(planeGeometry, new T.MeshPhysicalMaterial({
      color: 0xb0b5b1, metalness: .08, roughness: .18, transparent: true,
      opacity: .13, depthWrite: false, side: T.DoubleSide, clearcoat: 1,
      clearcoatRoughness: .12
    }));
    group.add(surface);
    group.add(new T.LineSegments(edgeGeometry, new T.LineBasicMaterial({
      color: white, transparent: true, opacity: .55, depthWrite: false
    })));
    // These marks are abstract observations, not invented customer data.
    var marks = [];
    for (var row = 0; row < 17; row++) {
      for (var col = 0; col < 8; col++) {
        if ((row * 13 + col * 7 + index * 11) % 5 === 0) continue;
        marks.push(-1.08 + col * .305, -2.05 + row * .255, .08);
      }
    }
    var marksGeometry = new T.BufferGeometry();
    marksGeometry.setAttribute('position', new T.Float32BufferAttribute(marks, 3));
    group.add(new T.Points(marksGeometry, dotMaterial));
    assembly.add(group);
    planeItems.push(group);
  });

  var pathPoints = [
    new T.Vector3(-4.85, .18, .78),
    new T.Vector3(-3.6, .18, .78),
    new T.Vector3(-1.25, -.12, .78),
    new T.Vector3(1.15, .31, .78),
    new T.Vector3(3.55, -.04, .78),
    new T.Vector3(4.72, -.04, .78),
    new T.Vector3(4.72, -2.35, .78)
  ];
  var tubes = [], beacons = [];
  var pathMaterial = new T.MeshBasicMaterial({ color: orange, transparent: true, opacity: .06, depthWrite: false });
  for (var i = 0; i < pathPoints.length - 1; i++) {
    var geom = new T.CylinderGeometry(.018, .018, pathPoints[i].distanceTo(pathPoints[i + 1]), 7);
    var mat = pathMaterial.clone();
    var segment = new T.Mesh(geom, mat);
    segment.position.copy(pathPoints[i]).add(pathPoints[i + 1]).multiplyScalar(.5);
    segment.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), pathPoints[i + 1].clone().sub(pathPoints[i]).normalize());
    assembly.add(segment);
    tubes.push(segment);
  }
  locations.forEach(function (x, i) {
    var dot = new T.Mesh(new T.SphereGeometry(.055, 12, 12),
      new T.MeshBasicMaterial({ color: orange, transparent: true, opacity: .08 }));
    dot.position.copy(pathPoints[i + 1]); assembly.add(dot); beacons.push(dot);
  });
  var base = new T.Mesh(new T.BoxGeometry(1.35, .12, 1.2),
    new T.MeshStandardMaterial({ color: 0x22241f, roughness: .55, metalness: .12 }));
  base.position.set(4.72, -2.43, .3); assembly.add(base);
  var baseEdge = new T.LineSegments(new T.EdgesGeometry(base.geometry),
    new T.LineBasicMaterial({ color: 0x74786f, transparent: true, opacity: .55 }));
  base.add(baseEdge);

  var decision = new T.Group();
  decision.position.set(0, .05, 1.05);
  var decisionRing = new T.Mesh(new T.TorusGeometry(.72, .014, 6, 96),
    new T.MeshBasicMaterial({ color: orange, transparent: true, opacity: .8, depthWrite: false }));
  decision.add(decisionRing);
  decision.add(new T.Mesh(new T.SphereGeometry(.11, 20, 20),
    new T.MeshBasicMaterial({ color: orange })));
  assembly.add(decision);
  decision.scale.setScalar(.001);

  var layouts = [
    [[-3.6, .18, -.54, -.32, 1], [-1.25, -.13, -.18, .25, 1], [1.15, .18, .18, -.22, 1], [3.55, -.13, .54, .31, 1]],
    [[-3.3, 0, -.42, -.08, 1], [-1.1, 0, -.14, .06, 1], [1.1, 0, .14, -.06, 1], [3.3, 0, .42, .08, 1]],
    [[-.93, 0, -.7, -.08, .82], [-.31, 0, -.27, -.025, .82], [.31, 0, .16, .025, .82], [.93, 0, .59, .08, .82]],
    [[-.72, 0, -.83, 0, .74], [-.24, 0, -.38, 0, .74], [.24, 0, .07, 0, .74], [.72, 0, .52, 0, .74]]
  ];

  var selected = 0, progress = 0, hoverX = 0, hoverY = 0, isDragging = false;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var visible = true, interacted = false;
  function setSelected(index) {
    var next = Math.max(0, Math.min(3, index));
    if (selected !== next || !host.hasAttribute('data-step')) {
      selected = next;
      host.setAttribute('data-step', String(selected));
      if (title && detail) {
        title.textContent = readings[selected][0];
        detail.textContent = readings[selected][1];
      }
    }
    controls.forEach(function (control, n) {
      control.setAttribute('aria-pressed', String(n === selected));
    });
  }
  controls.forEach(function (control, index) {
    control.addEventListener('click', function () { interacted = true; setSelected(index); if (reduced) render(); });
    control.addEventListener('focus', function () { interacted = true; setSelected(index); if (reduced) render(); });
  });
  function aim(e) {
    var r = host.getBoundingClientRect();
    hoverX = ((e.clientX - r.left) / r.width - .5) * 2;
    hoverY = ((e.clientY - r.top) / r.height - .5) * 2;
    if (isDragging) { interacted = true; setSelected(Math.round(Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * 3)); }
  }
  host.addEventListener('pointermove', aim, { passive: true });
  host.addEventListener('pointerdown', function (e) {
    if (e.pointerType !== 'mouse' && e.pointerType !== 'pen') return;
    isDragging = true; interacted = true; host.setPointerCapture(e.pointerId); aim(e);
  });
  host.addEventListener('click', function (e) {
    if (e.pointerType !== 'touch') return;
    var r = host.getBoundingClientRect();
    interacted = true;
    setSelected(Math.round(Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * 3));
    if (reduced) render();
  });
  host.addEventListener('pointerup', function () { isDragging = false; });
  host.addEventListener('pointercancel', function () { isDragging = false; });
  host.addEventListener('pointerleave', function () { if (!isDragging) { hoverX = 0; hoverY = 0; } });

  function resize() {
    var width = canvas.clientWidth, height = canvas.clientHeight;
    if (!width || !height) return;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.fov = width < 600 ? 52 : 35;
    camera.position.z = width < 600 ? 21 : 17;
    camera.updateProjectionMatrix();
    assembly.scale.setScalar(width < 600 ? .87 : 1);
    render();
  }
  function render() {
    var speed = reduced ? 1 : .065;
    progress += (selected - progress) * speed;
    assembly.rotation.y += ((reduced ? -.08 : hoverX * .12) - assembly.rotation.y) * (reduced ? 1 : .06);
    assembly.rotation.x += ((reduced ? 0 : -hoverY * .045) - assembly.rotation.x) * (reduced ? 1 : .06);
    planeItems.forEach(function (item, index) {
      var from = Math.floor(progress), to = Math.min(3, from + 1);
      var t = Math.max(0, Math.min(1, progress - from));
      var a = layouts[from][index], b = layouts[to][index];
      item.position.set(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t);
      item.rotation.y = a[3] + (b[3] - a[3]) * t;
      item.scale.setScalar(a[4] + (b[4] - a[4]) * t);
    });
    tubes.forEach(function (segment, index) {
      var route = progress < 1 ? progress : progress < 2 ? 1 : progress < 2.8 ? 1 - (progress - 2) : (progress - 2.8) * 5;
      segment.material.opacity = Math.max(.045, Math.min(.88, (index < 4 ? .7 : .88) * route));
    });
    beacons.forEach(function (beacon, index) {
      beacon.material.opacity = progress < 2 ? .2 + progress * .3 : Math.max(.12, (progress - 2.7) * 2.5);
      beacon.scale.setScalar(index === selected ? 1.8 : 1);
    });
    decision.scale.setScalar(Math.max(.001, Math.min(1, (progress - 1.35) * 1.55)));
    decisionRing.rotation.z += reduced ? 0 : .002;
    warm.intensity = 1.05 + progress * .2;
    renderer.render(scene, camera);
  }
  window.addEventListener('resize', resize);
  window.addEventListener('scroll', function () {
    if (interacted) return;
    var r = host.getBoundingClientRect();
    if (r.top < window.innerHeight && r.bottom > 0) {
      var amount = Math.max(0, Math.min(1, (window.innerHeight * .75 - r.top) / (r.height + window.innerHeight * .4)));
      setSelected(Math.min(3, Math.floor(amount * 4)));
      if (reduced) render();
    }
  }, { passive: true });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; }).observe(host);
  }
  setSelected(reduced ? 3 : 0);
  resize();
  host.classList.add('scene-ready');
  if (!reduced) {
    (function loop() {
      requestAnimationFrame(loop);
      if (visible && !document.hidden) render();
    })();
  }
})();
