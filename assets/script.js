/* Bouncy Castle Man, shared behaviour. Loaded on every page. */

/* REVEAL (defined before first use) */
const io=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){
  en.target.style.opacity='1';en.target.style.transform='translateY(0)';io.unobserve(en.target);
}});},{threshold:.08});
function revealNew(){document.querySelectorAll('[data-reveal]').forEach((el,i)=>{
  if(!el.dataset.r){el.dataset.r='1';el.style.transitionDelay=(i%4*50)+'ms';io.observe(el);}
});}

/* NAV */
const burger=document.getElementById('burger'),mob=document.getElementById('mobileMenu');
if(burger&&mob){
  burger.addEventListener('click',()=>mob.classList.toggle('open'));
  mob.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>mob.classList.remove('open')));
}

/* CATALOGUE FILTERS: cards are real HTML here, so this only shows and hides */
const filterBar=document.getElementById('filters');
if(filterBar){
  filterBar.addEventListener('click',e=>{
    const b=e.target.closest('.filter-btn');if(!b)return;
    uncrop();
    document.querySelectorAll('.filter-btn').forEach(x=>x.classList.toggle('active',x===b));
    document.querySelectorAll('#grid .card').forEach(c=>{
      c.style.display=(b.dataset.cat==='all'||c.dataset.cat===b.dataset.cat)?'':'none';
    });
  });
}

/* VIEW ALL: the grid ships cropped to two rows, this drops the crop */
function uncrop(){
  const g=document.getElementById('grid'),w=document.querySelector('.browse-all');
  if(g)g.classList.remove('cropped');
  if(w)w.style.display='none';
}
const viewAll=document.getElementById('viewAll');
if(viewAll)viewAll.addEventListener('click',e=>{e.preventDefault();uncrop();});

/* AREA CHECKER */
const areaBtn=document.getElementById('areaBtn');
if(areaBtn){
  areaBtn.addEventListener('click',()=>{
    const v=document.getElementById('areaSel').value,r=document.getElementById('areaOut');
    if(!v){r.textContent="Pick your area first.";r.style.color="var(--ink-faint)";return;}
    if(v==='__other__'){
      r.innerHTML='Not listed? <a href="tel:0879005391" style="color:var(--p1);font-weight:800">Give us a call</a>, we may still reach you.';
      r.style.color="var(--ink-soft)";
    }else{
      r.textContent="Yes, we deliver to "+v+". Send us your date for a price.";
      r.style.color="var(--p1)";
    }
  });
}

/* FAQ */
document.querySelectorAll('.faq-q').forEach(q=>q.addEventListener('click',()=>{
  const item=q.parentElement,a=item.querySelector('.faq-a'),open=item.classList.contains('open');
  document.querySelectorAll('.faq-item').forEach(i=>{
    i.classList.remove('open');i.querySelector('.faq-a').style.maxHeight=null;
  });
  if(!open){item.classList.add('open');a.style.maxHeight=a.scrollHeight+'px';}
}));

/* CHATBOT */
const cw=document.getElementById('chatWindow'),cb=document.getElementById('chatBody'),
      chatBtn=document.getElementById('chatBtn'),chips=document.getElementById('chips');
const KB={
  hire:"Bouncy castles, combi castles with slides, obstacle courses from 30ft up to the 55ft high adrenaline units, a disco dome, sumo suits, the gladiator challenge and marquees.",
  area:"We cover Tipperary and the surrounding areas, including Clonmel, Thurles, Nenagh, Cashel, Roscrea, Tipperary Town, Templemore, Cahir and Carrick on Suir. Use the area checker or tell us your town.",
  package:"Prices depend on the unit, the date and your area. Ring or WhatsApp us and we will give you a price straight away.",
  safe:"We are fully insured and certified with the Irish Inflatable Hirers Federation. Every unit must be supervised by a responsible adult, and we run through the safety points with you at set up.",
  book:"Easiest way is to ring or WhatsApp 087 900 5391, or send an enquiry through the form with your date, your town and the ages. We will come back to you with a price."
};
function add(t,who){const d=document.createElement('div');d.className='msg '+who;d.textContent=t;
  cb.appendChild(d);cb.scrollTop=cb.scrollHeight;}
if(cw&&chatBtn){
  chatBtn.addEventListener('click',()=>cw.classList.toggle('open'));
  const cl=document.getElementById('chatClose');
  if(cl)cl.addEventListener('click',()=>cw.classList.remove('open'));
}
if(chips){
  chips.addEventListener('click',e=>{
    const c=e.target.closest('.chip');if(!c)return;
    add(c.textContent,'user');setTimeout(()=>add(KB[c.dataset.q],'bot'),350);
  });
}

/* INIT */
revealNew();
const yr=document.getElementById('yr');
if(yr)yr.textContent=new Date().getFullYear();
