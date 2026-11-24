/* Signals become an organized decision as this chapter is scrolled. */
(() => {
  const section = document.querySelector('.signal-story');
  const canvas = document.querySelector('#signal-canvas');
  if (!section) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small = matchMedia('(max-width: 760px)').matches;
  const steps = [...section.querySelectorAll('[data-signal-step]')];
  const legend = section.querySelector('[data-signal-legend]');
  const labels = ['SCATTERED SIGNALS', 'A CLEAR PRIORITY', 'EVIDENCE FOR THE NEXT MOVE'];
  let progress = reduced ? .5 : 0;
  let stage = -1;
  function setStage(index) {
    if (index === stage) return;
    stage = index;
    steps.forEach((el, i) => el.classList.toggle('active', i === index));
    if (legend) legend.textContent = labels[index];
  }
  setStage(reduced ? 1 : 0);

  if (!reduced && window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    ScrollTrigger.create({
      trigger: section, start: 'top top', end: 'bottom bottom',
      onUpdate: self => {
        progress = self.progress;
        setStage(Math.min(2, Math.floor(Math.min(.999, progress) * 3)));
      }
    });
  } else if (!reduced) {
    addEventListener('scroll', () => {
      const length = Math.max(1, section.offsetHeight - innerHeight);
      progress = Math.max(0, Math.min(1, (scrollY - section.offsetTop) / length));
      setStage(Math.min(2, Math.floor(Math.min(.999, progress) * 3)));
    }, {passive:true});
  }

  if (!canvas) return; // The original sculpture now occupies Customer Signals.
  const T = window.THREE;
  if (!T) return;
  let renderer;
  try { renderer = new T.WebGLRenderer({canvas, alpha:true, antialias:!small, powerPreference:'low-power'}); }
  catch (_) { return; }
  section.classList.add('webgl-ready');
  canvas.addEventListener('webglcontextlost', event => {
    event.preventDefault();
    section.classList.remove('webgl-ready');
  });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, small ? 1.2 : 1.6));
  renderer.outputEncoding = T.sRGBEncoding;
  const scene = new T.Scene();
  const camera = new T.PerspectiveCamera(38, 1, .1, 100);
  camera.position.z = small ? 11.5 : 10;
  const coreUniforms = {
    uTime:{value:0}, uProgress:{value:progress}, uPointer:{value:new T.Vector2(0,0)}
  };
  const core = new T.Mesh(new T.IcosahedronGeometry(2.05, 5), new T.ShaderMaterial({
    uniforms:coreUniforms,
    vertexShader:`
      uniform float uTime; uniform float uProgress;
      varying vec3 vNormal; varying vec3 vPosition;
      void main(){
        float unrest=(1.0-uProgress)*0.13;
        float wave=sin(position.x*4.0+uTime*.55)*sin(position.y*3.7-uTime*.38)*sin(position.z*3.1);
        vec3 displaced=position+normal*wave*unrest;
        vec4 mv=modelViewMatrix*vec4(displaced,1.0);
        vNormal=normalize(normalMatrix*normal);
        vPosition=mv.xyz;
        gl_Position=projectionMatrix*mv;
      }`,
    fragmentShader:`
      uniform float uTime; uniform float uProgress; uniform vec2 uPointer;
      varying vec3 vNormal; varying vec3 vPosition;
      void main(){
        vec3 n=normalize(vNormal); vec3 view=normalize(-vPosition);
        float fresnel=pow(1.0-max(dot(n,view),0.0),2.45);
        vec3 lightDir=normalize(vec3(.48+uPointer.x*.4,.72+uPointer.y*.3,1.0));
        float diffuse=max(dot(n,lightDir),0.0);
        float spec=pow(max(dot(reflect(-lightDir,n),view),0.0),22.0);
        float contour=.5+.5*sin(19.0*atan(n.y,n.x)+n.z*9.0+uTime*.15);
        vec3 ink=vec3(.035,.05,.055);
        vec3 silver=vec3(.21,.27,.29)*(.2+diffuse*.9)+vec3(.7,.76,.72)*spec*.55;
        vec3 amber=vec3(1.0,.23,.055)*(fresnel*.9+contour*.065);
        vec3 color=ink+silver+amber*(.58+uProgress*.44);
        gl_FragColor=vec4(color,1.0);
      }`
  }));
  scene.add(core);

  const halo = new T.Mesh(new T.SphereGeometry(2.23, 48, 32), new T.ShaderMaterial({
    uniforms:{uProgress:coreUniforms.uProgress}, side:T.BackSide,
    transparent:true, depthWrite:false, blending:T.AdditiveBlending,
    vertexShader:`varying vec3 vN; varying vec3 vV; void main(){vec4 mv=modelViewMatrix*vec4(position,1.);vN=normalize(normalMatrix*normal);vV=normalize(-mv.xyz);gl_Position=projectionMatrix*mv;}`,
    fragmentShader:`uniform float uProgress; varying vec3 vN; varying vec3 vV; void main(){float f=pow(1.-abs(dot(normalize(vN),normalize(vV))),3.);gl_FragColor=vec4(1.,.20,.04,f*(.17+uProgress*.16));}`
  }));
  scene.add(halo);

  // One draw call for the data field. Point size and softness create depth cues.
  const count = small ? 80 : 150;
  const positions = new Float32Array(count*3);
  const sizes = new Float32Array(count);
  const colors = new Float32Array(count*3);
  const source = [], orbit = [], resolved = [];
  let seed = 8147;
  const rand = () => ((seed = (seed*1664525+1013904223) >>> 0) / 4294967296);
  for (let i=0;i<count;i++) {
    const theta=rand()*Math.PI*2, z=rand()*2-1, r=3.1+rand()*2.5;
    source.push([Math.cos(theta)*r, z*3.7, Math.sin(theta)*r]);
    const angle=i*2.39996;
    orbit.push([Math.cos(angle)*3.1, Math.sin(angle)*2.9, Math.sin(i*.42)*.7]);
    const row=(i%3)-1, t=(i/(count-1))*2-1;
    resolved.push([row*.82+t*.25, t*3.9, Math.sin(t*5+row)*.28]);
    sizes[i]=small ? 9+rand()*9 : 8+rand()*13;
    const bright=i%6===0;
    colors.set(bright?[1,.30,.09]:[.46,.56,.56],i*3);
  }
  const geometry=new T.BufferGeometry();
  geometry.setAttribute('position',new T.BufferAttribute(positions,3));
  geometry.setAttribute('aSize',new T.BufferAttribute(sizes,1));
  geometry.setAttribute('aColor',new T.BufferAttribute(colors,3));
  const cloud=new T.Points(geometry,new T.ShaderMaterial({
    transparent:true,depthWrite:false,blending:T.AdditiveBlending,
    vertexShader:`attribute float aSize;attribute vec3 aColor;varying vec3 vColor;void main(){vColor=aColor;vec4 mv=modelViewMatrix*vec4(position,1.);gl_PointSize=aSize*(10.0/-mv.z);gl_Position=projectionMatrix*mv;}`,
    fragmentShader:`varying vec3 vColor;void main(){float d=length(gl_PointCoord-.5)*2.;float glow=exp(-d*d*4.5);float center=1.-smoothstep(.1,.48,d);gl_FragColor=vec4(vColor,glow*.18+center*.8);}`
  }));
  scene.add(cloud);

  let targetX=0,targetY=0,mouseX=0,mouseY=0;
  section.addEventListener('pointermove', e => {
    const box=canvas.getBoundingClientRect();
    targetX=((e.clientX-box.left)/Math.max(1,box.width)-.5)*2;
    targetY=((e.clientY-box.top)/Math.max(1,box.height)-.5)*-2;
  },{passive:true});
  section.addEventListener('pointerleave',()=>{targetX=0;targetY=0});
  function resize(){
    const w=canvas.clientWidth,h=canvas.clientHeight;
    if(!w||!h)return;
    renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();
  }
  addEventListener('resize',resize);resize();
  let visible=false;
  if ('IntersectionObserver' in window) new IntersectionObserver(entries=>{visible=entries[0].isIntersecting},{rootMargin:'100px'}).observe(section);
  else visible=true;
  function draw(time){
    if (!reduced) requestAnimationFrame(draw);
    if (!visible && !reduced || document.hidden) return;
    const t=time*.001,p=Math.max(0,Math.min(1,progress));
    const smooth=x=>x*x*(3-2*x);
    const mix=(a,b,q)=>a+(b-a)*q;
    const first=smooth(Math.min(1,p*2)), second=smooth(Math.max(0,p*2-1));
    for(let i=0;i<count;i++){
      for(let axis=0;axis<3;axis++){
        const mid=mix(source[i][axis],orbit[i][axis],first);
        positions[i*3+axis]=mix(mid,resolved[i][axis],second);
      }
    }
    geometry.attributes.position.needsUpdate=true;
    mouseX+=(targetX-mouseX)*.055;mouseY+=(targetY-mouseY)*.055;
    coreUniforms.uTime.value=t;coreUniforms.uProgress.value=p;
    coreUniforms.uPointer.value.set(mouseX,mouseY);
    core.rotation.y=t*.075+p*1.15+mouseX*.08;
    core.rotation.x=p*.4+mouseY*.08;
    halo.rotation.copy(core.rotation);
    cloud.rotation.y=t*.018+mouseX*.06;
    renderer.render(scene,camera);
  }
  if(reduced){visible=true;draw(0)}else requestAnimationFrame(draw);
})();
