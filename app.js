
const assetMap={};
const uri=n=>'https://sivencestudio.com/assets/'+n;
const mediaUri=n=>!n?'':n.startsWith('/')||n.startsWith('http')?n:uri(n);
document.querySelectorAll('[data-asset]').forEach(i=>i.src=mediaUri(i.dataset.asset));
document.querySelectorAll('video').forEach(v=>{if(v.dataset.poster)v.poster=mediaUri(v.dataset.poster)});
const motion=matchMedia('(prefers-reduced-motion: reduce)');let heroStarted=false;
function source(v){if(!v.src)v.src=mediaUri(v.dataset.film)}
function controls(v){const b=v.parentElement.querySelector('[data-play]');if(b){b.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true">'+(v.ended?'<path d="M5 8a8 8 0 1 1-1 7M5 3v5h5"/>':v.paused?'<path d="m8 5 11 7-11 7Z"/>':'<path d="M8 5v14M16 5v14"/>')+'</svg>';b.setAttribute('aria-label',v.ended?'Replay video':v.paused?'Play video':'Pause video')}}
document.querySelectorAll('video').forEach(v=>{['play','pause','ended'].forEach(e=>v.addEventListener(e,()=>controls(v)));v.addEventListener('play',()=>document.querySelectorAll('video').forEach(x=>{if(x!==v)x.pause()}));if(v.controls){source(v)}});
document.querySelectorAll('[data-play]').forEach(b=>b.addEventListener('click',()=>{const v=b.closest('.film').querySelector('video');source(v);if(v.ended)v.currentTime=0;if(v.paused)v.play().catch(()=>controls(v));else v.pause()}));
document.querySelectorAll('[data-sound]').forEach(b=>b.addEventListener('click',()=>{const v=b.closest('.film').querySelector('video');v.muted=!v.muted;b.closest('.film').classList.toggle('audible',!v.muted);b.setAttribute('aria-label',v.muted?'Unmute video':'Mute video')}));
function route(){if(document.querySelector('dialog').open)document.querySelector('dialog').close();let target=location.hash.slice(1).replace(/-+$/,'')||'home';const anchor=target==='creative'?'creative-group':target==='assignments'?'assignments-group':null;if(anchor)target='work';if(!document.querySelector('[data-page="'+CSS.escape(target)+'"]'))target='home';document.querySelectorAll('.page').forEach(p=>p.hidden=p.dataset.page!==target);document.querySelectorAll('video').forEach(v=>v.pause());document.querySelectorAll('nav a').forEach(a=>{if(a.hash==='#'+target)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});if(target==='home'&&!motion.matches){const v=document.querySelector('[data-hero]');source(v);v.play().catch(()=>controls(v));heroStarted=true}if(anchor)document.getElementById(anchor).scrollIntoView();else window.scrollTo({top:0,behavior:'instant'});document.title=target==='home'?'Sivence — Brand, Growth & Creative Direction':({remic:'REMIC',soaltech:'SoalTech',healthcan:'HealthCan',incuse:'Incuse',titanfile:'TitanFile'}[target]||target.replaceAll('-',' ').replace(/\b\w/g,c=>c.toUpperCase()))+' — Sivence'}
document.querySelector('.skip-link').addEventListener('click',e=>{e.preventDefault();document.querySelector('main').focus();document.querySelector('main').scrollIntoView()});window.addEventListener('hashchange',route);route();
document.querySelectorAll('[data-size]').forEach(b=>b.addEventListener('click',()=>{document.querySelector('.viewport').classList.toggle('mobile',b.dataset.size==='mobile');document.querySelectorAll('[data-size]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))}));
const dialog=document.querySelector('dialog');let gallery=[],index=0,trigger;
function showImage(){const im=dialog.querySelector('img');im.src=uri(gallery[index].dataset.enlarge);im.alt=gallery[index].querySelector('img').alt;}
document.querySelectorAll('[data-enlarge]').forEach(b=>b.addEventListener('click',()=>{trigger=b;gallery=Array.from(b.parentElement.querySelectorAll('[data-enlarge]'));index=gallery.indexOf(b);showImage();dialog.showModal()}));
document.querySelector('[data-close]').onclick=()=>dialog.close();document.querySelector('[data-next]').onclick=()=>{index=(index+1)%gallery.length;showImage()};document.querySelector('[data-prev]').onclick=()=>{index=(index+gallery.length-1)%gallery.length;showImage()};dialog.addEventListener('keydown',e=>{if(e.key==='ArrowRight')document.querySelector('[data-next]').click();if(e.key==='ArrowLeft')document.querySelector('[data-prev]').click()});dialog.addEventListener('close',()=>trigger?.focus());
document.querySelector('[data-pdf]').onclick=()=>{const a=document.createElement('a');a.href='https://sivencestudio.com/assets/minimalance-catalogue.pdf';a.download='Minimalance-complete-catalogue.pdf';a.click()};

const focusRegions=document.querySelectorAll('.focus-media');
focusRegions.forEach(el=>{el.addEventListener('pointermove',e=>{if(motion.matches||e.pointerType==='touch')return;const b=el.getBoundingClientRect();el.style.setProperty('--fx',((e.clientX-b.left)/b.width*100)+'%');el.style.setProperty('--fy',((e.clientY-b.top)/b.height*100)+'%');});el.addEventListener('pointerleave',()=>{el.style.setProperty('--fx','50%');el.style.setProperty('--fy','50%')})});
let ticking=false;function focusScroll(){if(ticking||motion.matches)return;ticking=true;requestAnimationFrame(()=>{focusRegions.forEach(el=>{if(el.closest('[hidden]'))return;const b=el.getBoundingClientRect();const d=Math.abs(b.top+b.height/2-innerHeight/2)/innerHeight;el.style.setProperty('--focus',Math.min(.9,.2+d));});ticking=false})}addEventListener('scroll',focusScroll,{passive:true});focusScroll();
document.querySelectorAll('video').forEach(v=>v.addEventListener('error',()=>{if(v.parentElement.querySelector('.media-error'))return;const p=document.createElement('p');p.className='media-error';p.textContent='This video could not load.';const b=document.createElement('button');b.textContent='Retry';b.onclick=()=>{v.load();v.play().catch(()=>{});p.remove()};p.append(' ',b);v.parentElement.append(p)}));

document.querySelectorAll('video').forEach(controls);document.addEventListener('visibilitychange',()=>{if(document.hidden){document.querySelectorAll('video').forEach(v=>v.pause())}else if((location.hash.slice(1)||'home')==='home'&&!motion.matches){const v=document.querySelector('[data-hero]');source(v);v.play().catch(()=>controls(v))}});dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});

const heroStage=document.querySelector('.hero-stage');
const heroReel=document.querySelector('.hero-reel');
let heroZoomTick=false;
function heroZoom(){
  if(heroZoomTick)return;
  heroZoomTick=true;
  requestAnimationFrame(()=>{
    if(!heroStage||!heroReel||motion.matches||heroStage.closest('[hidden]')){
      heroReel?.style.setProperty('--hero-scale','1');
      heroZoomTick=false;
      return;
    }
    const box=heroStage.getBoundingClientRect();
    const travel=Math.max(box.height*.72,1);
    const progress=Math.min(1,Math.max(0,-box.top/travel));
    heroReel.style.setProperty('--hero-scale',(1+progress*.13).toFixed(3));
    heroZoomTick=false;
  });
}
addEventListener('scroll',heroZoom,{passive:true});
addEventListener('resize',heroZoom,{passive:true});
heroZoom();

// Pages CMS writes the files in /content. The static site reads them directly,
// so editorial changes do not require a framework or a paid website builder.
const escapeCopy=value=>String(value??'').replace(/[&<>"']/g,char=>({
  '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'
}[char]));
const setText=(selector,value)=>{const node=document.querySelector(selector);if(node&&value!==undefined)node.textContent=value};
const setLines=(selector,first,second)=>{const node=document.querySelector(selector);if(node)node.innerHTML=escapeCopy(first)+'<br><em>'+escapeCopy(second)+'</em>'};
const setMedia=(node,path)=>{if(!node||!path)return;const resolved=mediaUri(path);if(node.tagName==='VIDEO'){node.dataset.film=resolved;node.removeAttribute('src');node.load()}else{node.src=resolved;node.dataset.asset=path.replace(/^\/assets\//,'')}};

async function loadEditableContent(){
  try{
    const [siteResponse,projectsResponse]=await Promise.all([fetch('/content/site.json'),fetch('/content/projects.json')]);
    if(!siteResponse.ok||!projectsResponse.ok)throw new Error('Editable content is unavailable');
    const site=await siteResponse.json();
    const projects=await projectsResponse.json();

    document.title=site.site_title||document.title;
    const description=document.querySelector('meta[name="description"]');
    if(description&&site.site_description)description.content=site.site_description;

    if(site.hero){
      setLines('#page-home .hero-heading h1',site.hero.line_one,site.hero.line_two);
      setText('#page-home .hero-heading p',site.hero.supporting_text);
      const hero=document.querySelector('[data-hero]');
      if(hero){
        if(site.hero.poster)hero.poster=mediaUri(site.hero.poster);
        if(site.hero.video&&hero.dataset.film!==site.hero.video){
          const wasPlaying=!hero.paused;
          setMedia(hero,site.hero.video);
          if(wasPlaying)hero.play().catch(()=>controls(hero));
        }
      }
    }

    if(site.meaning){
      setText('.sivence-meaning .eyebrow',site.meaning.label);
      setLines('#why-sivence-title',site.meaning.line_one,site.meaning.line_two);
      setText('.sivence-meaning .meaning-copy p',site.meaning.description);
    }

    if(site.about){
      setLines('#page-about .about-lead h1',site.about.headline_one,site.about.headline_two);
      setText('#page-about .about-deck',site.about.introduction);
      setText('#page-about .about-deck + p',site.about.summary);
      setMedia(document.querySelector('#page-about figure img'),site.about.portrait);
    }

    if(site.contact){
      setText('#page-contact .eyebrow',site.contact.label);
      const words=(site.contact.headline||'').trim().split(/\s+/);
      const emphasis=words.pop()||'';
      setLines('#page-contact h1',words.join(' '),emphasis);
      setText('#page-contact p',site.contact.supporting_text);
      const email=document.querySelector('#page-contact .contact-email');
      if(email&&site.contact.email){email.href='mailto:'+site.contact.email;email.textContent=site.contact.email+' ↗︎'}
      const linkedin=document.querySelector('#page-contact .contact-links a[target="_blank"]');
      if(linkedin&&site.contact.linkedin_url)linkedin.href=site.contact.linkedin_url;
    }

    projects.forEach(project=>{
      const tile=document.querySelector('#page-work .project-tile[href="#'+CSS.escape(project.id)+'"], #page-work .assignment-card[href="#'+CSS.escape(project.id)+'"]');
      if(!tile)return;
      setTextIn(tile,'h2, h3',project.title);
      const summary=tile.querySelector(':scope > p');
      if(summary)summary.textContent=project.summary;
      const meta=tile.querySelector('.project-meta');
      if(meta){
        const spans=meta.querySelectorAll('span');
        if(spans[0])spans[0].textContent=project.number+' / '+project.type;
        if(spans[1])spans[1].textContent=project.discipline;
      }else{
        const label=tile.querySelector(':scope > span');
        if(label)label.textContent=project.number+' / '+project.type;
      }
      if(project.image&&!['xipster','camfire'].includes(project.id))setMedia(tile.querySelector('img'),project.image);
    });
  }catch(error){
    console.warn('Sivence CMS content could not be loaded; embedded content remains visible.',error);
  }
}
function setTextIn(parent,selector,value){const node=parent.querySelector(selector);if(node&&value!==undefined)node.textContent=value}
loadEditableContent();
