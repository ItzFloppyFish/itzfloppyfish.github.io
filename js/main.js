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
  function mk(){return{x:Math.random()*W,y:Math.random()*H,s:Math.random()*1.4+0.4,vx:(Math.random()-.5)*.28,vy:(Math.random()-.5)*.28,a:Math.random()*.32+.05,col:Math.random()>.7?'#00d4ff':'#2878ff'};}
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
