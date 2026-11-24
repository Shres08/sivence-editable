(() => {
  const rail=document.querySelector('.painting-rail');
  if(!rail)return;
  const items=[...rail.querySelectorAll('.painting-tile')];
  const count=document.querySelector('[data-paint-count]');
  const previous=document.querySelector('[data-paint-previous]');
  const next=document.querySelector('[data-paint-next]');
  let active=0,tick=false;
  function update(){
    tick=false;
    const left=rail.getBoundingClientRect().left;
    active=items.reduce((best,item,i)=>Math.abs(item.getBoundingClientRect().left-left)<Math.abs(items[best].getBoundingClientRect().left-left)?i:best,0);
    count.textContent=String(active+1).padStart(2,'0')+' / '+String(items.length).padStart(2,'0');
    previous.disabled=active===0;next.disabled=active===items.length-1;
  }
  rail.addEventListener('scroll',()=>{if(!tick){tick=true;requestAnimationFrame(update)}},{passive:true});
  function move(offset){items[Math.max(0,Math.min(items.length-1,active+offset))].scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'nearest',inline:'start'})}
  previous.addEventListener('click',()=>move(-1));next.addEventListener('click',()=>move(1));
  let drag=null, suppressClickUntil=0;
  rail.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse')drag={id:e.pointerId,x:e.clientX,left:rail.scrollLeft,active:false}});
  rail.addEventListener('pointermove',e=>{
    if(!drag || e.pointerId!==drag.id)return;
    const distance=e.clientX-drag.x;
    if(Math.abs(distance)>8){
      if(!drag.active){rail.setPointerCapture(e.pointerId);drag.active=true}
      rail.scrollLeft=drag.left-distance;suppressClickUntil=performance.now()+350;
    }
  });
  rail.addEventListener('pointerup',()=>{drag=null});
  rail.addEventListener('pointercancel',()=>{drag=null});
  rail.addEventListener('click',e=>{if(performance.now()<suppressClickUntil){e.preventDefault();e.stopImmediatePropagation()}},true);
  update();
})();
