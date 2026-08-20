# -*- coding: utf-8 -*-
"""
Bouncy Castle Man static site generator.

    cd build && python3 generate.py

Reads content from data.py and the design from base.html (the single page demo
the client approved), then writes the whole site to the repo root. Safe to
re-run: it only ever overwrites files it generates.

Same shape as the Mr Bounce Sligo build, so the layout is familiar: base.html
holds the design, data.py holds the content, pages.py builds the pages.
"""
import hashlib, io, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = io.open(os.path.join(HERE, "base.html"), encoding="utf-8").read()

# Set by build_assets(). Appended to the asset URLs so a year long immutable
# cache never serves a stale stylesheet against fresh markup.
ASSET_V = {"css": "0", "js": "0"}

WAVE = "#fffdf8"          # --bg, the colour the wave dips into
BRAND_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M3 21V11l9-6 9 6v10"/>'
             '<path d="M3 15h18"/><path d="M9 21v-6h6v6"/></svg>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(relpath, html):
    full = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    io.open(full, "w", encoding="utf-8", newline="\n").write(html)
    return relpath


def shot(src, alt, cls="", eager=False):
    """Image tag, or a branded placeholder tile when we have no photo yet.

    Adam has not sent photos, and the old site only serves eight usable images.
    Rather than ship broken images or fake ones, every unit without a real
    photo renders this tile. Replace by setting img= on the unit in data.py.
    """
    load = "eager" if eager else "lazy"
    if src == D.SOON:
        return (f'<span class="soon {cls}" role="img" aria-label="{esc(alt)}, photo coming soon">'
                f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
                f'stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" '
                f'height="14" rx="2"/><circle cx="8.5" cy="10.5" r="1.6"/>'
                f'<path d="m21 15-5-5L5 21"/></svg><b>Photo coming soon</b></span>')
    return f'<img src="{src}" alt="{esc(alt)}" loading="{load}" class="{cls}">'


# ---------------------------------------------------------------- assets ----
def build_assets():
    css = re.search(r"<style>([\s\S]*?)</style>", BASE).group(1)
    css += """
  /* ---- multi-page additions ---- */

  /* The hero renders taller than its content ends, which left a band of bare
     photo below the wave. Pinning the wave to the hero's bottom edge means the
     photo can never show underneath it, whatever the copy length does. */
  .hero{padding-bottom:46px}
  .hero .wave{position:absolute;left:0;right:0;bottom:0;z-index:3}

  /* Inner page banner. Same purple as the brand rather than a photo wash, so
     it still reads when a unit has no photo yet. */
  .page-hero{position:relative;overflow:hidden;
    background:linear-gradient(180deg,#8b5cf6 0%,#7c3aed 45%,#5b21b6 100%)}
  .page-hero .ph-bg{position:absolute;inset:0;z-index:0}
  .page-hero .ph-bg img{width:100%;height:100%;object-fit:cover;object-position:50% 42%;
    opacity:.34}
  .page-hero .ph-bg::after{content:"";position:absolute;inset:0;
    background:linear-gradient(90deg,rgba(46,16,101,.82) 0%,rgba(76,29,149,.62) 45%,
      rgba(91,33,182,.34) 100%)}
  .page-hero .wrap{position:relative;z-index:2;padding-top:74px;padding-bottom:78px}
  @media(max-width:700px){.page-hero .wrap{padding-top:50px;padding-bottom:54px}}
  .page-hero h1{font-size:clamp(30px,4.6vw,50px);color:#fff;
    text-shadow:0 3px 0 rgba(46,16,101,.34);max-width:20ch}
  .page-hero p{color:#f3e9ff;font-weight:600;font-size:clamp(15px,1.8vw,18px);
    margin-top:14px;max-width:56ch}
  .crumb{font-size:13.5px;font-weight:700;color:#e6d6ff;margin-bottom:14px}
  .crumb a{color:#e6d6ff;text-decoration:underline;text-underline-offset:2px}
  .crumb span{margin:0 7px;opacity:.6}

  /* ---- photo coming soon tile ---- */
  .soon{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;
    width:100%;height:100%;min-height:150px;color:var(--p1);
    background:repeating-linear-gradient(45deg,#f6efff,#f6efff 12px,#f1e7ff 12px,#f1e7ff 24px);
    border-radius:inherit;text-align:center;padding:14px}
  .soon svg{width:30px;height:30px;opacity:.55}
  .soon b{font-family:'Nunito',sans-serif;font-weight:800;font-size:12.5px;
    letter-spacing:.02em;opacity:.75}
  .card-img .soon{min-height:0;position:absolute;inset:0}

  /* Homepage catalogue ships cropped to two rows, the View all button drops
     the crop. Card 9 onward is hidden at 4 columns, 7 onward at 3, 5 at 2, so
     it is always exactly two rows whatever the breakpoint. */
  .catalogue.cropped .card:nth-child(n+9){display:none}
  @media(max-width:1040px){.catalogue.cropped .card:nth-child(n+7){display:none}}
  @media(max-width:760px){.catalogue.cropped .card:nth-child(n+5){display:none}}
  .browse-all{margin-top:24px;display:flex;justify-content:center}
  .browse-all .btn{min-width:240px;justify-content:center}

  /* ---- inner page furniture ---- */
  .prose{max-width:70ch;color:var(--ink-soft);font-weight:600;font-size:16.5px;line-height:1.7}
  .prose p{margin-bottom:14px}
  .cat-more{display:flex;justify-content:center;margin-top:30px}

  .unit-grid{display:grid;grid-template-columns:1fr 320px;gap:34px;align-items:start}
  .unit-shot{border:2px solid var(--line);border-radius:var(--r);overflow:hidden;
    aspect-ratio:4/3;background:var(--surface)}
  .unit-shot img{width:100%;height:100%;object-fit:cover}
  .unit-side{background:#fff;border:2px solid var(--line);border-radius:var(--r);
    padding:22px;position:sticky;top:96px;display:flex;flex-direction:column;gap:10px}
  .unit-side .price{font-family:'Baloo 2',cursive;font-weight:800;font-size:26px;
    color:var(--p1)}
  .unit-side .btn{width:100%;justify-content:center}
  @media(max-width:900px){.unit-grid{grid-template-columns:1fr}
    .unit-side{position:static}}

  .specs{width:100%;border-collapse:collapse;margin:20px 0 24px;font-size:15.5px}
  .specs th,.specs td{text-align:left;padding:11px 14px;border:2px solid var(--line);
    font-weight:700}
  .specs th{background:var(--surface);color:var(--ink);width:40%}
  .specs td{color:var(--ink-soft)}

  .safety-box{background:var(--surface);border:2px solid var(--line);border-radius:var(--r);
    padding:22px 24px;margin-top:26px}
  .safety-box h3{font-family:'Baloo 2',cursive;font-size:19px;color:var(--ink);
    margin-bottom:10px}
  .safety-box ul{margin:0;padding-left:20px;color:var(--ink-soft);font-weight:600;
    font-size:15.5px;line-height:1.65}
  .safety-box li{margin-bottom:7px}

  .area-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
  .area-card{display:block;background:#fff;border:2px solid var(--line);border-radius:var(--r);
    padding:22px;transition:border-color .15s,transform .15s}
  .area-card:hover{border-color:var(--p1);transform:translateY(-2px)}
  .area-card h3{font-family:'Baloo 2',cursive;font-size:21px;color:var(--p1);margin-bottom:5px}
  .area-card p{color:var(--ink-soft);font-weight:600;font-size:14.5px}
  @media(max-width:900px){.area-grid{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:560px){.area-grid{grid-template-columns:1fr}}

  /* Category tiles carry a photo on the multi page build. */
  .cat-img{display:block;width:100%;aspect-ratio:16/9;border-radius:var(--r-sm);
    overflow:hidden;margin-bottom:12px;background:rgba(255,255,255,.35);position:relative}
  .cat-img img{width:100%;height:100%;object-fit:cover}
  .cat-img .soon{min-height:0;position:absolute;inset:0}
"""
    css_out = css.strip() + "\n"
    ASSET_V["css"] = hashlib.md5(css_out.encode("utf-8")).hexdigest()[:8]
    write("assets/styles.css", css_out)

    # Shared script. Written explicitly rather than cut out of base.html, because
    # every page loads the same file and not every page has every element. Each
    # block guards its own targets so a missing element never throws.
    js = """/* Bouncy Castle Man, shared behaviour. Loaded on every page. */

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
      r.innerHTML='Not listed? <a href="tel:PHONE_TEL" style="color:var(--p1);font-weight:800">Give us a call</a>, we may still reach you.';
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
  book:"Easiest way is to ring or WhatsApp PHONE_DISPLAY, or send an enquiry through the form with your date, your town and the ages. We will come back to you with a price."
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
"""
    js = js.replace("PHONE_TEL", D.PHONE_TEL).replace("PHONE_DISPLAY", D.PHONE_DISPLAY)
    ASSET_V["js"] = hashlib.md5(js.encode("utf-8")).hexdigest()[:8]
    write("assets/script.js", js)


# ------------------------------------------------------------- fragments ----
NAV = [("/bouncy-castles/", "Castles"), ("/combi-castles/", "Combi Castles"),
       ("/obstacle-courses/", "Obstacle Courses"), ("/disco-dome/", "Disco Dome"),
       ("/marquees/", "Marquees"), ("/areas/", "Areas"), ("/faqs/", "FAQs")]

TAGLINE = ("Bouncy castles, obstacle courses, disco dome &amp; marquees across Tipperary")


def head(title, desc, canon, img=None):
    img = img or D.HERO_MAIN
    if img == D.SOON:
        img = D.HERO_MAIN
    if img.startswith("/"):
        img = D.SITE + img
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{D.SITE}{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{D.SITE}{canon}">
<meta property="og:type" content="website">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css?v={ASSET_V["css"]}">
</head>
<body>

<div class="topbar">
  <div class="wrap">
    <div>{TAGLINE}</div>
    <div class="tb-r"><a href="tel:{D.PHONE_TEL}">Call us: {D.PHONE_DISPLAY}</a></div>
  </div>
</div>

<header class="nav">
  <div class="wrap">
    <a href="/" class="brand" aria-label="{D.NAME} home">
      <span class="mark">{BRAND_SVG}</span>
      {D.NAME}
    </a>
    <nav class="navlinks">{''.join(f'<a href="{u}">{t}</a>' for u, t in NAV)}</nav>
    <a href="/contact/" class="nav-cta">Get a quote</a>
    <button class="burger" id="burger" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    {''.join(f'<a href="{u}">{t}</a>' for u, t in NAV)}<a href="/contact/">Get a quote</a>
  </div>
</header>
"""


def wave():
    return (f'<div class="wave" aria-hidden="true"><svg viewBox="0 0 1440 46" '
            f'preserveAspectRatio="none"><path fill="{WAVE}" d="M0,46 L0,20 C240,44 480,0 '
            f'720,12 C960,24 1200,46 1440,18 L1440,46 Z"/></svg></div>')


def crumbs(trail):
    out = ['<div class="crumb"><a href="/">Home</a>']
    for u, t in trail:
        out.append("<span>/</span>")
        out.append(t if u is None else f'<a href="{u}">{t}</a>')
    return "".join(out) + "</div>"


def page_hero(title, sub, img, trail):
    bg = "" if img == D.SOON else f'<div class="ph-bg"><img src="{img}" alt=""></div>'
    return f"""
<section class="page-hero">
  {bg}
  <div class="wrap">
    {crumbs(trail)}
    <h1>{title}</h1>
    <p>{sub}</p>
  </div>
</section>
{wave()}
"""


def card(u):
    return f"""      <a class="card" href="/hire/{u['slug']}/" data-cat="{u['cat']}" data-reveal>
        <div class="card-img"><span class="card-tag">{u['tag']}</span>{shot(u['img'], u['n'])}</div>
        <div class="card-body">
          <h3>{esc(u['n'])}</h3>
          <p>{esc(u['short'])}</p>
          <div class="card-foot"><div class="price">{u['price']}</div><span class="card-cta">View &rarr;</span></div>
        </div>
      </a>
"""


def safety_box():
    lis = "".join(f"<li>{esc(s)}</li>" for s in D.SAFETY)
    return f'<div class="safety-box"><h3>Safety and insurance</h3><ul>{lis}</ul></div>'


PHONE_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 '
             '1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 '
             '1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.6.7 2.34a2 2 0 0 '
             '1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.74.34 1.53.57 '
             '2.34.7A2 2 0 0 1 22 16.92z"/></svg>')
PIN_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
           'stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 '
           '9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/></svg>')
WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.15-1.7-.85-2-.95-.27'
          '-.1-.46-.15-.65.15-.2.3-.75.95-.92 1.14-.17.2-.34.22-.63.07-.3-.15-1.25-.46-2.38-1.47-.88'
          '-.78-1.47-1.75-1.64-2.05-.17-.3-.02-.46.13-.6.13-.13.3-.34.45-.5.15-.18.2-.3.3-.5.1-.2.05'
          '-.37-.02-.52-.08-.15-.65-1.57-.9-2.15-.23-.56-.47-.48-.65-.5h-.55c-.2 0-.5.07-.76.37-.27.3'
          '-1 1-1 2.42s1.03 2.8 1.17 3c.15.2 2.02 3.08 4.9 4.32.68.3 1.22.47 1.63.6.69.22 1.31.19 '
          '1.8.12.55-.08 1.7-.7 1.94-1.36.24-.67.24-1.24.17-1.36-.07-.12-.27-.2-.56-.34ZM12 2a10 10 '
          '0 0 0-8.5 15.3L2 22l4.8-1.5A10 10 0 1 0 12 2Z"/></svg>')


def wa_link():
    return (f"https://wa.me/{D.WHATSAPP}"
            f"?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20hire.")


def contact_block():
    email_row = (f'<a href="mailto:{D.EMAIL}">{D.EMAIL}</a>' if D.EMAIL else
                 f'<a href="{wa_link()}" target="_blank" rel="noopener">{WA_SVG}WhatsApp us</a>')
    return f"""
<section class="contact" id="contact">
  <div class="wrap">
    <div>
      <h2>Get in <em>touch</em></h2>
      <p class="lede">Send us your date, your town and the ages of the children and we will come straight back with a price.</p>
      <div class="contact-list">
        <a href="tel:{D.PHONE_TEL}">{PHONE_SVG}Call {D.PHONE_DISPLAY}</a>
        {email_row}
        <div>{PIN_SVG}{D.LOCALITY}, {D.REGION}</div>
      </div>
    </div>
    <!-- TODO: replace [FORM-ID] with the real Formspree form ID -->
    <form action="{D.FORMSPREE}" method="POST">
      <div class="fld"><label for="n">Your name</label><input id="n" name="name" type="text" required></div>
      <div class="fld"><label for="p">Phone</label><input id="p" name="phone" type="tel" required></div>
      <div class="fld"><label for="t">Your town</label><input id="t" name="town" type="text"></div>
      <div class="fld"><label for="d">Date of event</label><input id="d" name="date" type="date"></div>
      <div class="fld"><label for="m">What are you after?</label><textarea id="m" name="message" rows="3" placeholder="Which unit, your area, date and ages..."></textarea></div>
      <button type="submit" class="btn btn-pink">Send enquiry</button>
    </form>
  </div>
</section>
"""


def footer():
    ranges = "".join(f'<a href="/{c["slug"]}/">{c["title"]}</a>' for c in D.CATEGORIES)
    areas = "".join(f'<a href="/{a["slug"]}/">{a["town"]}</a>' for a in D.AREAS)
    wa = wa_link()
    social = (f'<a href="{D.FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">'
              f'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 '
              f'0-11.5 9.9v-7H8v-2.9h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c'
              f'-1.2 0-1.6.8-1.6 1.6v1.9h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12Z"/></svg></a>')
    return f"""
<footer>
  <div class="wrap">
    <div class="foot-top">
      <div>
        <div class="foot-brand"><span class="mark">{BRAND_SVG}</span>{D.NAME}</div>
        <p style="max-width:38ch">Bouncy castle, obstacle course, disco dome and marquee hire, family run since {D.FOUNDED}. Serving Clonmel, Thurles, Nenagh, Cashel, Roscrea and the rest of Tipperary.</p>
        <div class="socials">
          <!-- TODO: replace [FACEBOOK-URL] with the real page -->
          {social}
        </div>
      </div>
      <div class="foot-col"><h4>The Range</h4>{ranges}</div>
      <div class="foot-col"><h4>Areas</h4>{areas}</div>
      <div class="foot-col"><h4>Get in touch</h4>
        <a href="tel:{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a>
        <a href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
        <a href="/contact/">Send an enquiry</a>
        <a href="/faqs/">FAQs</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; <span id="yr"></span> {D.NAME}. All rights reserved.</span>
      <span>Site by <a href="https://squaretwo.ie" target="_blank" rel="noopener">SquareTwo</a></span>
    </div>
  </div>
</footer>

<a href="{wa}" target="_blank" rel="noopener" class="wa-float" aria-label="WhatsApp">{WA_SVG}</a>
<button class="chat-btn" id="chatBtn" aria-label="Open chat">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
</button>
<div class="chat-window" id="chatWindow">
  <div class="chat-head">
    <div><div class="ch-name">{D.NAME}</div><div class="ch-status">We usually reply fast</div></div>
    <button class="chat-close" id="chatClose" aria-label="Close">&times;</button>
  </div>
  <div class="chat-body" id="chatBody"><div class="msg bot">Hi, how can we help?</div></div>
  <div class="chips" id="chips">
    <button class="chip" data-q="hire">What can I hire?</button>
    <button class="chip" data-q="area">My area</button>
    <button class="chip" data-q="package">Prices</button>
    <button class="chip" data-q="safe">Safety</button>
    <button class="chip" data-q="book">How to book</button>
  </div>
  <div class="chat-foot">
    <a class="chat-wa" href="{wa}" target="_blank" rel="noopener">{WA_SVG}Continue on WhatsApp</a>
  </div>
</div>
<script src="/assets/script.js?v={ASSET_V["js"]}"></script>
</body>
</html>
"""


if __name__ == "__main__":
    build_assets()
    import pages
    pages.main()
