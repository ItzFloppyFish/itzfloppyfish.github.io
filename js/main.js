// === NAV SCROLL ===
(function(){
  const n=document.getElementById('ffnav');
  if(!n)return;
  window.addEventListener('scroll',()=>n.classList.toggle('sc',window.scrollY>60),{passive:true});
})();

// === PARTICLE CANVAS ===
(function(){
  const c=document.getElementById('ff-cv');
  if(!c)return;
  const ctx=c.getContext('2d');
  let W,H,P=[];
  function rs(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
  function mk(){return{x:Math.random()*W,y:Math.random()*H,s:Math.random()*1.9+0.7,vx:(Math.random()-.5)*.28,vy:(Math.random()-.5)*.28,a:Math.random()*.32+.05,col:Math.random()>.7?'#00d4ff':'#2878ff'};}
  rs();
  for(let i=0;i<70;i++)P.push(mk());
  function lp(){
    ctx.clearRect(0,0,W,H);
    P.forEach(p=>{
      p.x+=p.vx;p.y+=p.vy;
      if(p.x<0||p.x>W||p.y<0||p.y>H)Object.assign(p,mk(),{x:Math.random()*W,y:Math.random()*H});
      ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);
      ctx.fillStyle=p.col;ctx.globalAlpha=p.a;ctx.fill();
    });
    requestAnimationFrame(lp);
  }
  lp();
  window.addEventListener('resize',rs);
})();

// === FADE-IN OBSERVER ===
function ffFI(){
  const o=new IntersectionObserver(es=>{
    es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('vis');o.unobserve(e.target);}});
  },{threshold:0.08});
  document.querySelectorAll('.fffade:not(.vis)').forEach(el=>o.observe(el));
}
document.addEventListener('DOMContentLoaded',ffFI);

// === COUNT UP ===
function ffCountUp(id,target,suffix,duration){
  const el=document.getElementById(id);
  if(!el)return;
  let startTime=null;
  function step(now){
    if(!startTime)startTime=now;
    const elapsed=now-startTime;
    const progress=Math.min(elapsed/duration,1);
    const ease=1-Math.pow(1-progress,3);
    el.textContent=Math.round(target*ease)+suffix;
    if(progress<1)requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

function ffInitCounters(){
  const stats=document.querySelector('.ffstats-g');
  if(!stats)return;
  let fired=false;
  const obs=new IntersectionObserver(function(entries){
    if(entries[0].isIntersecting&&!fired){
      fired=true;obs.disconnect();
      ffCountUp('st-s',80,'K+',1800);
      ffCountUp('st-v',11,'M+',2000);
      ffCountUp('st-vd',300,'+',1600);
    }
  },{threshold:0.3});
  obs.observe(stats);
}
document.addEventListener('DOMContentLoaded',ffInitCounters);

// === NAV ACTIVE STATE ===
document.addEventListener('DOMContentLoaded',function(){
  // Normalise current path: strip trailing slash (except root), drop any index.html
  let path=window.location.pathname.replace(/index\.html$/,'').replace(/\/+$/,'');
  if(path==='')path='/';
  document.querySelectorAll('.ffnl').forEach(l=>{
    l.classList.remove('on');
    let href=l.getAttribute('href');
    if(!href)return;
    // Normalise the link's href the same way
    href=href.replace(/index\.html$/,'').replace(/\/+$/,'');
    if(href==='')href='/';
    if(href==='/'){
      if(path==='/')l.classList.add('on');
    } else if(path===href||path.startsWith(href+'/')){
      l.classList.add('on');
    }
  });
});

// === SOCIAL ICON BURST ON HOVER ===
(function(){
  // Respect reduced-motion + skip touch devices (no real hover)
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const noHover = window.matchMedia('(hover: none)').matches;
  if(reduce || noHover) return;

  // SVG path per platform — small, single-path glyphs
  const ICONS = {
    youtube: '<path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2C0 8.1 0 12 0 12s0 3.9.5 5.8a3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1C24 15.9 24 12 24 12s0-3.9-.5-5.8zM9.8 15.5V8.5l6.3 3.5-6.3 3.5z"/>',
    discord: '<path d="M20.3 4.4A19.8 19.8 0 0 0 15.4 3l-.2.4a18.3 18.3 0 0 1 4.3 1.4 16.6 16.6 0 0 0-12.9 0A18 18 0 0 1 10.7 3.4L10.5 3A19.7 19.7 0 0 0 5.6 4.4 20.4 20.4 0 0 0 2 18.3a19.9 19.9 0 0 0 6 3l.4-.6a13 13 0 0 1-2-1l.5-.4a14.2 14.2 0 0 0 12 0l.5.4a12.7 12.7 0 0 1-2 1l.4.6a19.8 19.8 0 0 0 6-3 20.3 20.3 0 0 0-3.4-13.9zM9 15.3c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2zm6 0c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2z"/>',
    x: '<path d="M18.2 2h3.3l-7.2 8.3L23 22h-6.6l-5.2-6.8L5.3 22H2l7.7-8.8L1.5 2h6.8l4.7 6.2L18.2 2zm-1.2 18h1.8L7.1 3.9H5.1L17 20z"/>'
  };
  const COLORS = { youtube:'#ff3030', discord:'#5865f2', x:'#e8f0ff' };

  let lastBurst = 0;
  function burst(btn){
    const now = Date.now();
    if(now - lastBurst < 380) return; // cooldown: no machine-gunning
    lastBurst = now;

    const type = btn.getAttribute('data-burst');
    const icon = ICONS[type]; if(!icon) return;
    const color = COLORS[type] || '#2878ff';
    const r = btn.getBoundingClientRect();
    const cx = r.left + r.width/2;
    const cy = r.top + r.height/2;

    const N = 7;                       // particles per burst
    const baseAngle = -Math.PI/2;      // shoot generally upward
    const spread = Math.PI * 0.7;      // fan width

    for(let i=0;i<N;i++){
      const el = document.createElement('div');
      el.className = 'ffburst';
      el.innerHTML = '<svg viewBox="0 0 24 24" fill="'+color+'">'+icon+'</svg>';
      el.style.left = cx + 'px';
      el.style.top = cy + 'px';
      document.body.appendChild(el);

      const ang = baseAngle - spread/2 + (spread * (i/(N-1))) + (Math.random()-0.5)*0.25;
      const dist = 46 + Math.random()*44;
      const dx = Math.cos(ang) * dist;
      const dy = Math.sin(ang) * dist - (18 + Math.random()*14); // slight extra lift
      const rot = (Math.random()-0.5) * 90;
      const sc = 0.55 + Math.random()*0.5;

      el.animate([
        { transform:'translate(-50%,-50%) translate(0,0) scale(0.2) rotate(0deg)', opacity:0 },
        { transform:'translate(-50%,-50%) translate('+dx*0.45+'px,'+dy*0.45+'px) scale('+sc+') rotate('+rot*0.5+'deg)', opacity:1, offset:0.25 },
        { transform:'translate(-50%,-50%) translate('+dx+'px,'+dy+'px) scale('+sc*0.9+') rotate('+rot+'deg)', opacity:0 }
      ], { duration: 620 + Math.random()*180, easing:'cubic-bezier(.22,.7,.3,1)' })
      .onfinish = () => el.remove();
    }
  }

  document.querySelectorAll('[data-burst]').forEach(btn=>{
    btn.addEventListener('mouseenter', () => burst(btn));
  });
})();
