# -*- coding: utf-8 -*-
"""
Bouncy Castle Man static site generator.

    cd build && python3 generate.py

Reads content from data.py and writes the whole site to the repo root. Safe to
re-run: it only ever overwrites files it generates.

DESIGN (rebuilt 20 Aug 2026, replacing the cartoon "Bounce Land" house style)
Bold modern, photo led. Off-black ink on warm paper, ONE saturated accent
(vermillion). The castles are the colour on this page, the furniture is not.
Bricolage Grotesque for display, Figtree for body. One radius scale (4px, all
sharp). No gradients, no glows, no cartoon clip art.

The design lives in this file (build_assets writes assets/styles.css from the
CSS string below). There is no base.html any more.
"""
import hashlib, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ASSET_V = {"css": "0", "js": "0"}

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800"
         "&family=Figtree:wght@400;500;600;700&display=swap")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(relpath, html):
    full = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    io.open(full, "w", encoding="utf-8", newline="\n").write(full and html)
    return relpath


# ------------------------------------------------------------------ logo ----
# Wordmark plus mark. The mark is a castle block: crenellated top, arch cut out
# of the bottom centre. One colour, one path, reads at 16px, works as favicon.
def logo_mark(size=34, fill="currentColor"):
    return (f'<svg class="mark" viewBox="0 0 32 32" width="{size}" height="{size}" '
            f'aria-hidden="true" focusable="false">'
            f'<path fill="{fill}" fill-rule="evenodd" d="M2 8h5v3h4V8h5v3h4V8h5v22h-8v-7'
            f'a5 5 0 0 0-10 0v7H2V8Z"/></svg>')


def logo(cls="brand", href="/"):
    return (f'<a href="{href}" class="{cls}" aria-label="{D.NAME} home">'
            f'{logo_mark()}'
            f'<span class="wordmark"><b>Bouncy Castle</b><i>Man</i></span></a>')


FAVICON = ('data:image/svg+xml,'
           '%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E'
           '%3Crect width=%2232%22 height=%2232%22 fill=%22%23111110%22/%3E'
           '%3Cpath fill=%22%23f4491f%22 fill-rule=%22evenodd%22 d=%22M2 8h5v3h4V8h5v3h4V8h5v22'
           'h-8v-7a5 5 0 0 0-10 0v7H2V8Z%22/%3E%3C/svg%3E')


# --------------------------------------------------------------- pictures ----
def shot(src, alt, ratio="4/3", eager=False, tag=None):
    """A photo, or a typographic panel when we have no photo yet.

    Adam has not sent photos and the old site only serves eight usable images.
    Rather than a broken image or a grey "coming soon" rectangle, a unit
    without a photo gets its name set large on the accent. It reads as a
    deliberate design object, not a hole. Set img= on the unit in data.py as
    photos arrive and this swaps itself out.
    """
    t = f'<span class="card-tag">{esc(tag)}</span>' if tag else ""
    if src == D.SOON:
        return (f'<span class="pic pic-panel" style="--ratio:{ratio}" role="img" '
                f'aria-label="{esc(alt)}">{t}<span class="panel-name">{esc(alt)}</span></span>')
    load = "eager" if eager else "lazy"
    return (f'<span class="pic" style="--ratio:{ratio}">{t}'
            f'<img src="{src}" alt="{esc(alt)}" loading="{load}"></span>')


# ---------------------------------------------------------------- assets ----
CSS = r"""
/* Bouncy Castle Man. Bold modern, photo led. One accent, one radius scale. */

*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;overflow-x:hidden}
img,svg{display:block;max-width:100%}
button,input,select,textarea{font:inherit;color:inherit}
a{color:inherit;text-decoration:none}
h1,h2,h3,h4,p,ul,ol,figure{margin:0}
ul{padding:0;list-style:none}

:root{
  /* One accent. The castles supply the rest of the colour.
     Two tones for one reason only, contrast:
       --accent      bright vermillion. LARGE display type and graphic marks
                     only (3.43:1 on paper, passes the 3:1 large-text bar).
       --accent-text small text and filled buttons (5.03:1 on paper, 5.3:1
                     against white, passes AA at any size).
     Do not use --accent on anything under 24px. */
  --accent:#f4491f;
  --accent-text:#c9330f;
  --accent-deep:#a8280a;
  --accent-soft:#ffe9e2;

  --ink:#111110;
  --ink-70:#4a4945;
  --ink-45:#6b6961;
  --paper:#faf9f5;
  --paper-2:#f1efe8;
  --line:#e0ddd3;
  --line-strong:#c9c5b8;

  --r:4px;                 /* ONE radius scale, everything is 4px. */
  --wrap:1280px;
  --nav-h:72px;

  --step--1:clamp(13px,.35vw + 12px,14.5px);
  --step-0:clamp(16px,.3vw + 15px,17.5px);
  --step-1:clamp(19px,.6vw + 17px,22px);
  --step-2:clamp(24px,1.4vw + 20px,32px);
  --step-3:clamp(30px,3vw + 20px,50px);
  --step-4:clamp(36px,4.4vw + 16px,64px);

  --display:'Bricolage Grotesque','Figtree',system-ui,sans-serif;
  --body:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;
}

body{font-family:var(--body);font-size:var(--step-0);line-height:1.55;
  color:var(--ink);background:var(--paper);
  font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}

h1,h2,h3,.display{font-family:var(--display);font-weight:800;line-height:1.02;
  letter-spacing:-.025em;font-variation-settings:'opsz' 48}
h1{font-size:var(--step-4)}
h2{font-size:var(--step-3);text-wrap:balance}
h3{font-size:var(--step-1);letter-spacing:-.015em;line-height:1.15}

.wrap{width:100%;max-width:var(--wrap);margin:0 auto;padding:0 28px}
@media(max-width:640px){.wrap{padding:0 20px}}
section{padding:clamp(56px,7vw,104px) 0}
.tint{background:var(--paper-2)}
.lede{font-size:var(--step-1);color:var(--ink-70);max-width:58ch;font-weight:500}
.prose{max-width:65ch;color:var(--ink-70);font-weight:450}
.prose p{margin-bottom:16px}
.prose h2{margin:34px 0 14px}

/* Eyebrow. Rationed: max one per three sections, per the design rules. */
.eyebrow{font-family:var(--body);font-size:12px;font-weight:700;letter-spacing:.14em;
  text-transform:uppercase;color:var(--accent-text);margin-bottom:14px;display:block}

.sec-head{margin-bottom:clamp(28px,3.4vw,48px);max-width:70ch}
.sec-head p{margin-top:14px;color:var(--ink-70);font-size:var(--step-1);max-width:56ch}

/* ------------------------------------------------------------- buttons --- */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;
  padding:15px 26px;border-radius:var(--r);border:1.5px solid transparent;
  font-family:var(--body);font-weight:700;font-size:15.5px;letter-spacing:-.005em;
  white-space:nowrap;cursor:pointer;transition:background .14s,color .14s,
  border-color .14s,transform .08s}
.btn:active{transform:translateY(1px)}
.btn-accent{background:var(--accent-text);color:#fff}
.btn-accent:hover{background:var(--accent-deep)}
.btn-ink{background:var(--ink);color:var(--paper)}
.btn-ink:hover{background:#000}
.btn-line{background:transparent;color:var(--ink);border-color:var(--line-strong)}
.btn-line:hover{border-color:var(--ink);background:var(--ink);color:var(--paper)}
.btn-onink{background:var(--paper);color:var(--ink)}
.btn-onink:hover{background:#fff}
.btn-onaccent{background:#fff;color:var(--accent-deep)}
.btn-onaccent:hover{background:var(--ink);color:#fff}
.btn svg{width:17px;height:17px;flex:none}

/* ----------------------------------------------------------------- nav --- */
.nav{position:sticky;top:0;z-index:60;background:rgba(250,249,245,.92);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
@supports not (backdrop-filter:blur(2px)){.nav{background:var(--paper)}}
.nav>.wrap{height:var(--nav-h);display:flex;align-items:center;gap:26px}
.brand{display:flex;align-items:center;gap:10px;flex:none;color:var(--ink)}
.brand .mark{color:var(--accent)}
.wordmark{font-family:var(--display);font-weight:800;line-height:.98;
  letter-spacing:-.03em;font-size:17px;display:flex;flex-direction:column}
.wordmark i{font-style:normal;color:var(--accent-text)}
.navlinks{display:flex;align-items:center;gap:22px;margin-left:auto;
  font-size:15px;font-weight:600;color:var(--ink-70)}
.navlinks a{padding:6px 0;white-space:nowrap;border-bottom:2px solid transparent;
  transition:color .14s,border-color .14s}
.navlinks a:hover{color:var(--ink);border-color:var(--accent)}
.nav-r{display:flex;align-items:center;gap:14px;flex:none}
.nav-tel{font-family:var(--display);font-weight:700;font-size:16px;letter-spacing:-.02em;
  display:flex;align-items:center;gap:7px}
.nav-tel svg{width:16px;height:16px;color:var(--accent)}
.nav .btn{padding:11px 19px;font-size:14.5px}
.burger{display:none;background:none;border:0;padding:8px;cursor:pointer}
.burger span{display:block;width:22px;height:2px;background:var(--ink);margin:4px 0}
.mobile-menu{display:none;flex-direction:column;padding:8px 28px 22px;gap:2px;
  border-top:1px solid var(--line);background:var(--paper)}
.mobile-menu.open{display:flex}
.mobile-menu a{padding:13px 0;font-weight:600;border-bottom:1px solid var(--line)}
.mobile-menu a:last-child{border:0}
/* The nav must never wrap to a second line. The quote button goes first, then
   the links. The phone number stays at every width, it is the real CTA. */
@media(max-width:1280px){.nav-r .btn{display:none}}
@media(max-width:1080px){.navlinks{display:none}.burger{display:block;margin-left:auto}}
@media(max-width:520px){.nav-tel span{display:none}}

/* ---------------------------------------------------------------- hero --- */
.hero{padding:clamp(38px,4.6vw,64px) 0 0}
.hero-grid{display:grid;grid-template-columns:1.02fr .98fr;gap:clamp(28px,4vw,64px);
  align-items:center}
.hero h1{max-width:17ch;margin-bottom:20px;text-wrap:balance}
.hero h1 em{font-style:normal;color:var(--accent)}
.hero p{font-size:var(--step-1);color:var(--ink-70);max-width:44ch;font-weight:500}
.hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.hero-photo{position:relative}
.hero-photo .pic{--ratio:4/3.05}
.hero-badge{position:absolute;left:0;bottom:0;background:var(--ink);color:var(--paper);
  padding:13px 18px;font-family:var(--display);font-weight:700;font-size:15px;
  letter-spacing:-.02em;display:flex;align-items:baseline;gap:9px}
.hero-badge b{color:var(--accent);font-size:13px;letter-spacing:.04em;text-transform:uppercase}
/* Breaks to one column below 1240. Narrower than that, the left column cannot
   hold the h1 to two lines, which is a hard layout rule. */
@media(max-width:1240px){.hero-grid{grid-template-columns:1fr;gap:30px}
  .hero h1{max-width:20ch}
  .hero-photo{order:-1}}

/* Facts strip. Sits under the hero, never inside it. Hairlines, not cards. */
.facts{border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  margin-top:clamp(44px,5vw,72px);display:grid;grid-template-columns:repeat(3,1fr)}
.facts div{padding:26px 30px;border-left:1px solid var(--line)}
.facts div:first-child{border-left:0;padding-left:0}
.facts b{display:block;font-family:var(--display);font-weight:800;font-size:var(--step-2);
  letter-spacing:-.03em;margin-bottom:4px}
.facts span{color:var(--ink-70);font-size:15px;font-weight:500}
@media(max-width:760px){.facts{grid-template-columns:1fr}
  .facts div{border-left:0;border-top:1px solid var(--line);padding:20px 0}
  .facts div:first-child{border-top:0}}

/* -------------------------------------------------------------- picture --- */
.pic{display:block;position:relative;aspect-ratio:var(--ratio,4/3);overflow:hidden;
  border-radius:var(--r);background:var(--paper-2)}
.pic img{width:100%;height:100%;object-fit:cover}
/* No-photo panel. Deliberately quiet: ink, not accent. Most units have no
   photo yet, and a grid of accent tiles turns the page into one loud block.
   Ink lets the real photographs lead, which is the whole point of the design.
   The hairline rule and the accent tag are the only marks. */
.pic-panel{background:var(--ink);display:flex;flex-direction:column;
  justify-content:flex-end;padding:20px;color:var(--paper)}
.pic-panel .panel-name{font-family:var(--display);font-weight:800;line-height:1.02;
  letter-spacing:-.03em;font-size:clamp(18px,1.9vw,26px);max-width:13ch;position:relative}
.pic-panel .panel-name::before{content:"";position:absolute;top:-14px;left:0;width:26px;
  height:2px;background:var(--accent)}
.pic-panel .card-tag{background:#33322f;color:var(--paper)}

/* ------------------------------------------------------------- category --- */
/* Bento: exactly six cells for six categories, two wide and four narrow. */
.cats{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.cat{grid-column:span 2;display:block;color:inherit}
.cat:nth-child(1),.cat:nth-child(2){grid-column:span 3}
.cat:nth-child(1) .pic,.cat:nth-child(2) .pic{--ratio:16/9}
.cat .pic{--ratio:4/3;transition:transform .3s cubic-bezier(.2,.7,.3,1)}
.cat:hover .pic{transform:translateY(-3px)}
.cat h3{margin-top:14px;display:flex;align-items:center;gap:8px}
.cat h3 svg{width:16px;height:16px;color:var(--accent);transition:transform .18s}
.cat:hover h3 svg{transform:translateX(4px)}
.cat p{color:var(--ink-70);font-size:15px;margin-top:5px;font-weight:450}
@media(max-width:900px){.cats{grid-template-columns:repeat(2,1fr)}
  .cat,.cat:nth-child(1),.cat:nth-child(2){grid-column:span 1}
  .cat:nth-child(1) .pic,.cat:nth-child(2) .pic{--ratio:4/3}}
@media(max-width:520px){.cats{grid-template-columns:1fr}}

/* ------------------------------------------------------------ catalogue --- */
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:26px}
.filter-btn{padding:9px 16px;border:1.5px solid var(--line-strong);background:transparent;
  border-radius:var(--r);font-size:14.5px;font-weight:600;cursor:pointer;
  transition:background .14s,color .14s,border-color .14s}
.filter-btn:hover{border-color:var(--ink)}
.filter-btn.active{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.catalogue{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.card{display:flex;flex-direction:column;color:inherit}
.card .pic{--ratio:4/3;transition:transform .3s cubic-bezier(.2,.7,.3,1)}
.card:hover .pic{transform:translateY(-3px)}
.card-tag{position:absolute;top:12px;left:12px;z-index:2;background:var(--ink);color:var(--paper);
  font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:5px 9px;
  border-radius:var(--r)}
.card h3{margin-top:13px;font-size:17.5px}
.card p{color:var(--ink-70);font-size:14.5px;margin-top:5px;font-weight:450;flex:1}
.card-foot{margin-top:12px;padding-top:11px;border-top:1px solid var(--line);
  display:flex;align-items:center;justify-content:space-between;gap:10px}
.price{font-family:var(--display);font-weight:700;font-size:15.5px;letter-spacing:-.02em}
.card-cta{font-size:14px;font-weight:700;color:var(--accent-text)}
.card:hover .card-cta{text-decoration:underline;text-underline-offset:3px}
@media(max-width:1040px){.catalogue{grid-template-columns:repeat(3,1fr)}}
@media(max-width:760px){.catalogue{grid-template-columns:repeat(2,1fr);gap:14px}}
/* Cropped to two rows until View all. Card counts match the column counts. */
.catalogue.cropped .card:nth-child(n+9){display:none}
@media(max-width:1040px){.catalogue.cropped .card:nth-child(n+7){display:none}}
@media(max-width:760px){.catalogue.cropped .card:nth-child(n+5){display:none}}
.more-row{display:flex;justify-content:center;margin-top:32px}

/* ----------------------------------------------------------------- how --- */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:0;
  border-top:2px solid var(--ink)}
.step{padding:30px 34px 0 0;border-left:1px solid var(--line)}
.step:first-child{border-left:0}
.step:not(:first-child){padding-left:34px}
.step-n{font-family:var(--display);font-weight:800;font-size:var(--step-2);
  color:var(--accent);letter-spacing:-.04em;line-height:1;margin-bottom:12px}
.step p{color:var(--ink-70);font-size:15.5px;margin-top:8px;font-weight:450}
@media(max-width:820px){.steps{grid-template-columns:1fr}
  .step,.step:not(:first-child){border-left:0;border-top:1px solid var(--line);
    padding:24px 0 24px}
  .step:first-child{border-top:0}}

/* ----------------------------------------------------------------- why --- */
.why{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);
  gap:clamp(28px,4vw,64px);align-items:start}
.why-head{position:sticky;top:calc(var(--nav-h) + 34px)}
.why-list li{display:grid;grid-template-columns:auto 1fr;gap:16px;padding:22px 0;
  border-top:1px solid var(--line)}
.why-list li:first-child{border-top:0;padding-top:0}
.why-list .n{font-family:var(--display);font-weight:700;font-size:14px;color:var(--accent-text);
  letter-spacing:.04em;padding-top:3px}
.why-list p{color:var(--ink-70);font-size:15.5px;margin-top:6px;font-weight:450;max-width:52ch}
@media(max-width:900px){.why{grid-template-columns:1fr}.why-head{position:static}}

/* --------------------------------------------------------------- areas --- */
.area-cols{columns:3;column-gap:34px}
.area-cols a{display:block;break-inside:avoid;padding:15px 0;border-top:1px solid var(--line);
  font-family:var(--display);font-weight:700;font-size:var(--step-1);letter-spacing:-.02em;
  transition:color .14s,padding-left .14s}
.area-cols a:hover{color:var(--accent-text);padding-left:8px}
.area-cols a span{display:block;font-family:var(--body);font-weight:450;font-size:14px;
  color:var(--ink-45);letter-spacing:0;margin-top:3px}
@media(max-width:900px){.area-cols{columns:2}}
@media(max-width:560px){.area-cols{columns:1}}
.area-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.area-card{display:block;border:1px solid var(--line);border-radius:var(--r);padding:22px;
  transition:border-color .14s,transform .14s}
.area-card:hover{border-color:var(--ink);transform:translateY(-2px)}
.area-card h3{font-size:19px}
.area-card p{color:var(--ink-70);font-size:14.5px;margin-top:5px;font-weight:450}
@media(max-width:860px){.area-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.area-grid{grid-template-columns:1fr}}

/* ------------------------------------------------------------- reviews --- */
.reviews{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:2px solid var(--ink)}
.review{padding:30px 34px 0 0;border-left:1px solid var(--line)}
.review:first-child{border-left:0}
.review:not(:first-child){padding-left:34px}
.review .stars{color:var(--accent);font-size:14px;letter-spacing:3px;margin-bottom:14px}
.review p{font-family:var(--display);font-weight:600;font-size:var(--step-1);
  line-height:1.3;letter-spacing:-.015em}
.review .who{margin-top:18px;font-size:14px;font-weight:600;color:var(--ink-45)}
@media(max-width:860px){.reviews{grid-template-columns:1fr}
  .review,.review:not(:first-child){border-left:0;border-top:1px solid var(--line);
    padding:26px 0 0}
  .review:first-child{border-top:0}}

/* ----------------------------------------------------------------- faq --- */
.faq{max-width:860px}
.faq-item{border-top:1px solid var(--line)}
.faq-item:last-child{border-bottom:1px solid var(--line)}
.faq-q{width:100%;background:none;border:0;text-align:left;cursor:pointer;padding:24px 44px 24px 0;
  font-family:var(--display);font-weight:700;font-size:var(--step-1);letter-spacing:-.02em;
  position:relative}
.faq-q::after{content:"";position:absolute;right:6px;top:50%;width:13px;height:13px;
  margin-top:-7px;background:currentColor;transition:transform .22s;
  clip-path:polygon(43% 0,57% 0,57% 43%,100% 43%,100% 57%,57% 57%,57% 100%,43% 100%,43% 57%,0 57%,0 43%,43% 43%)}
.faq-item.open .faq-q::after{transform:rotate(135deg);color:var(--accent)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .3s ease}
.faq-a p{padding:0 0 24px;color:var(--ink-70);max-width:62ch;font-weight:450}

/* ------------------------------------------------------------- notices --- */
.note{border-left:3px solid var(--accent);background:var(--accent-soft);padding:18px 22px;
  border-radius:0 var(--r) var(--r) 0;font-size:15.5px;font-weight:500;max-width:70ch}
.safety{border:1px solid var(--line);border-radius:var(--r);padding:26px 28px;margin-top:30px}
.safety h3{font-size:18px;margin-bottom:14px}
.safety li{position:relative;padding-left:26px;margin-bottom:10px;color:var(--ink-70);
  font-size:15.5px;font-weight:450}
.safety li::before{content:"";position:absolute;left:0;top:8px;width:11px;height:2px;
  background:var(--accent)}

/* ----------------------------------------------------------- strip/area --- */
.strip{border:1px solid var(--line);border-radius:var(--r);background:#fff;
  display:grid;grid-template-columns:1fr 1fr}
.strip-cell{padding:26px 28px;border-left:1px solid var(--line)}
.strip-cell:first-child{border-left:0}
.strip-cell h3{font-size:18px;margin-bottom:5px}
.strip-cell>p{color:var(--ink-70);font-size:14.5px;margin-bottom:14px;font-weight:450}
.strip-row{display:flex;gap:9px;flex-wrap:wrap}
.strip-row select,.strip-row input{flex:1;min-width:130px;padding:12px 13px;
  border:1.5px solid var(--line-strong);border-radius:var(--r);background:#fff;font-size:15px}
.strip-row select:focus,.strip-row input:focus{outline:2px solid var(--accent);outline-offset:1px;
  border-color:var(--accent)}
.strip-row .btn{padding:12px 20px}
#areaOut{margin-top:12px;font-size:15px;font-weight:600;min-height:22px}
@media(max-width:820px){.strip{grid-template-columns:1fr}
  .strip-cell{border-left:0;border-top:1px solid var(--line)}
  .strip-cell:first-child{border-top:0}}

/* ----------------------------------------------------------- page hero --- */
.page-hero{background:var(--ink);color:var(--paper);padding:clamp(44px,5vw,72px) 0
  clamp(44px,5vw,72px)}
.page-hero .crumb{font-size:14px;font-weight:600;color:#949189;margin-bottom:20px}
.page-hero .crumb a:hover{color:var(--paper)}
.page-hero .crumb i{font-style:normal;margin:0 8px;opacity:.5}
.page-hero h1{max-width:17ch}
.page-hero p{margin-top:18px;font-size:var(--step-1);color:#c8c5bd;max-width:54ch;font-weight:450}
.ph-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(26px,4vw,56px);align-items:center}
.ph-grid .pic{--ratio:16/10}
@media(max-width:860px){.ph-grid{grid-template-columns:1fr}.ph-grid .pic{display:none}}

/* ------------------------------------------------------------- unit pg --- */
.unit{display:grid;grid-template-columns:1fr 330px;gap:clamp(28px,4vw,56px);align-items:start}
.unit .pic{--ratio:16/10}
.unit h2{font-size:var(--step-2);margin:30px 0 14px}
.unit-side{border:1px solid var(--line);border-radius:var(--r);padding:24px;background:#fff;
  position:sticky;top:calc(var(--nav-h) + 22px);display:flex;flex-direction:column;gap:10px}
.unit-side .price{font-size:var(--step-2);font-weight:800}
.unit-side>p{color:var(--ink-70);font-size:14.5px;font-weight:450;margin-bottom:6px}
.unit-side .btn{width:100%}
.specs{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:24px 0 0}
.spec{border:1px solid var(--line);border-radius:var(--r);padding:16px 18px}
.spec dt{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-45);margin-bottom:5px}
.spec dd{margin:0;font-family:var(--display);font-weight:700;font-size:16.5px;
  letter-spacing:-.015em}
@media(max-width:900px){.unit{grid-template-columns:1fr}.unit-side{position:static}}
@media(max-width:520px){.specs{grid-template-columns:1fr}}

/* ------------------------------------------------------------- gallery --- */
.gallery{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.gallery .pic{--ratio:1/1}
.gallery a:nth-child(6n+1){grid-column:span 2}
.gallery a:nth-child(6n+1) .pic{--ratio:2/1}
@media(max-width:860px){.gallery{grid-template-columns:repeat(2,1fr)}}

/* ------------------------------------------------------------- contact --- */
.contact{background:var(--accent-text);color:#fff}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(30px,4vw,64px);
  align-items:start}
.contact h2{max-width:15ch}
.contact .lede{color:#fff0ec;margin-top:16px}
.contact-list{margin-top:28px;display:flex;flex-direction:column;gap:2px}
.contact-list a,.contact-list div{display:flex;align-items:center;gap:12px;padding:15px 0;
  border-top:1px solid rgba(255,255,255,.24);font-weight:600;font-size:16.5px}
.contact-list svg{width:19px;height:19px;flex:none;opacity:.9}
.contact-list a:hover{padding-left:6px;transition:padding-left .14s}
form{background:#fff;border-radius:var(--r);padding:26px}
.fld{display:flex;flex-direction:column;gap:7px;margin-bottom:15px}
.fld label{font-size:13.5px;font-weight:700;color:var(--ink-70)}
.fld input,.fld textarea{padding:12px 14px;border:1.5px solid var(--line-strong);
  border-radius:var(--r);font-size:15.5px;background:#fff;color:var(--ink);width:100%}
.fld input:focus,.fld textarea:focus{outline:2px solid var(--accent);outline-offset:1px;
  border-color:var(--accent)}
.fld textarea{resize:vertical;min-height:88px}
form .btn{width:100%;margin-top:6px}
@media(max-width:860px){.contact-grid{grid-template-columns:1fr}}

/* -------------------------------------------------------------- footer --- */
footer{background:var(--ink);color:#b0ada3;padding:clamp(48px,5vw,76px) 0 30px;font-size:15px}
.foot-top{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:34px}
.foot-brand{color:var(--paper);margin-bottom:16px}
/* On the dark footer the accent-text tone drops to 3.57:1, so the wordmark
   and mark use a lighter tint of the same accent there. */
footer .wordmark i{color:#ff7a58}
footer .brand .mark{color:#f4491f}
.foot-top>div>p{max-width:34ch;font-weight:450;line-height:1.6}
.foot-col h4{font-family:var(--display);font-weight:700;font-size:14px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--paper);margin-bottom:14px}
.foot-col a{display:block;padding:5px 0;transition:color .14s}
.foot-col a:hover{color:#ff7a58}
.socials{display:flex;gap:10px;margin-top:18px}
.socials a{width:38px;height:38px;border:1px solid rgba(255,255,255,.2);border-radius:var(--r);
  display:grid;place-items:center;transition:background .14s,border-color .14s}
.socials a:hover{background:var(--accent);border-color:var(--accent);color:#fff}
.socials svg{width:17px;height:17px}
.foot-bottom{margin-top:44px;padding-top:24px;border-top:1px solid rgba(255,255,255,.14);
  display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:14px}
.foot-bottom a{text-decoration:underline;text-underline-offset:2px}
.foot-bottom a:hover{color:#ff7a58}
@media(max-width:900px){.foot-top{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.foot-top{grid-template-columns:1fr}}

/* -------------------------------------------------------------- floats --- */
.wa-float{position:fixed;right:20px;bottom:20px;z-index:70;width:54px;height:54px;
  border-radius:var(--r);background:#25d366;color:#fff;display:grid;place-items:center;
  box-shadow:0 6px 22px rgba(17,17,16,.22);transition:transform .16s}
.wa-float:hover{transform:translateY(-3px)}
.wa-float svg{width:27px;height:27px}
.chat-btn{position:fixed;right:20px;bottom:84px;z-index:70;width:54px;height:54px;
  border-radius:var(--r);background:var(--ink);color:var(--paper);border:0;cursor:pointer;
  display:grid;place-items:center;box-shadow:0 6px 22px rgba(17,17,16,.22);transition:transform .16s}
.chat-btn:hover{transform:translateY(-3px)}
.chat-btn svg{width:24px;height:24px}
.chat-window{position:fixed;right:20px;bottom:84px;z-index:71;width:min(340px,calc(100vw - 40px));
  background:#fff;border:1px solid var(--line);border-radius:var(--r);
  box-shadow:0 18px 50px rgba(17,17,16,.2);display:none;flex-direction:column;overflow:hidden}
.chat-window.open{display:flex}
.chat-head{background:var(--ink);color:var(--paper);padding:16px 18px;display:flex;
  align-items:center;justify-content:space-between}
.ch-name{font-family:var(--display);font-weight:700;font-size:15.5px;letter-spacing:-.02em}
.ch-status{font-size:12.5px;color:#b0ada3}
.chat-close{background:none;border:0;color:inherit;font-size:22px;cursor:pointer;line-height:1}
.chat-body{padding:16px;display:flex;flex-direction:column;gap:9px;max-height:270px;
  overflow-y:auto}
.msg{padding:10px 13px;border-radius:var(--r);font-size:14.5px;max-width:88%;font-weight:450}
.msg.bot{background:var(--paper-2);align-self:flex-start}
.msg.user{background:var(--ink);color:var(--paper);align-self:flex-end}
.chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 16px 14px}
.chip{padding:7px 12px;border:1.5px solid var(--line-strong);background:#fff;border-radius:var(--r);
  font-size:13.5px;font-weight:600;cursor:pointer;transition:border-color .14s}
.chip:hover{border-color:var(--accent-text);color:var(--accent-text)}
.chat-foot{padding:12px 16px;border-top:1px solid var(--line)}
.chat-wa{display:flex;align-items:center;justify-content:center;gap:8px;padding:11px;
  background:#25d366;color:#fff;border-radius:var(--r);font-weight:700;font-size:14.5px}
.chat-wa svg{width:17px;height:17px}
@media(max-width:520px){.wa-float,.chat-btn{width:48px;height:48px}
  .chat-btn{bottom:76px}.chat-window{bottom:76px}}

/* -------------------------------------------------------------- motion --- */
/* Reveal is opt-in via the .js class set by an inline script in the head.
   Without JS, or if the script fails, everything renders visible. Content must
   never be hidden by a broken animation. */
.js [data-reveal]{opacity:0;transform:translateY(16px);
  transition:opacity .6s cubic-bezier(.2,.7,.3,1),transform .6s cubic-bezier(.2,.7,.3,1)}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .js [data-reveal]{opacity:1!important;transform:none!important;transition:none}
  *{animation-duration:.01ms!important;transition-duration:.01ms!important}
}

/* ---------------------------------------------------------------- a11y --- */
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.skip{position:absolute;left:-9999px;top:0;background:var(--ink);color:var(--paper);
  padding:12px 18px;z-index:100}
.skip:focus{left:0}
::selection{background:var(--accent);color:#fff}
"""

JS = r"""/* Bouncy Castle Man, shared behaviour. Loaded on every page.
   Every block guards its own targets, so a missing element never throws. */

/* REVEAL (defined before first use) */
const io = new IntersectionObserver(es => {
  es.forEach(en => {
    if (en.isIntersecting) {
      en.target.style.opacity = '1';
      en.target.style.transform = 'none';
      io.unobserve(en.target);
    }
  });
}, { threshold: .08, rootMargin: '0px 0px -40px' });
document.querySelectorAll('[data-reveal]').forEach((el, i) => {
  el.style.transitionDelay = (i % 4 * 55) + 'ms';
  io.observe(el);
});

/* NAV */
const burger = document.getElementById('burger'), mob = document.getElementById('mobileMenu');
if (burger && mob) {
  burger.addEventListener('click', () => mob.classList.toggle('open'));
  mob.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mob.classList.remove('open')));
}

/* CATALOGUE FILTERS: the cards are real HTML, this only shows and hides */
const filterBar = document.getElementById('filters');
if (filterBar) {
  filterBar.addEventListener('click', e => {
    const b = e.target.closest('.filter-btn'); if (!b) return;
    uncrop();
    document.querySelectorAll('.filter-btn').forEach(x => x.classList.toggle('active', x === b));
    document.querySelectorAll('#grid .card').forEach(c => {
      c.style.display = (b.dataset.cat === 'all' || c.dataset.cat === b.dataset.cat) ? '' : 'none';
    });
  });
}

/* VIEW ALL: the grid ships cropped to two rows, this drops the crop */
function uncrop() {
  const g = document.getElementById('grid'), w = document.querySelector('.more-row');
  if (g) g.classList.remove('cropped');
  if (w) w.style.display = 'none';
  /* The cards that were display:none never intersected, so show them outright
     rather than waiting on an observer callback that may not fire. */
  if (g) g.querySelectorAll('[data-reveal]').forEach(el => {
    el.style.transitionDelay = '0ms';
    el.style.opacity = '1';
    el.style.transform = 'none';
  });
}
const viewAll = document.getElementById('viewAll');
if (viewAll) viewAll.addEventListener('click', e => { e.preventDefault(); uncrop(); });

/* AREA CHECKER */
const areaBtn = document.getElementById('areaBtn');
if (areaBtn) {
  areaBtn.addEventListener('click', () => {
    const v = document.getElementById('areaSel').value, r = document.getElementById('areaOut');
    if (!v) { r.textContent = 'Pick your area first.'; r.style.color = 'var(--ink-45)'; return; }
    if (v === '__other__') {
      r.innerHTML = 'Not listed? <a href="tel:PHONE_TEL" style="color:var(--accent-text);text-decoration:underline">Give us a call</a>, we may still reach you.';
      r.style.color = 'var(--ink-70)';
    } else {
      r.textContent = 'Yes, we deliver to ' + v + '. Send us your date for a price.';
      r.style.color = 'var(--accent-text)';
    }
  });
}

/* FAQ */
document.querySelectorAll('.faq-q').forEach(q => q.addEventListener('click', () => {
  const item = q.parentElement, a = item.querySelector('.faq-a'),
        open = item.classList.contains('open');
  document.querySelectorAll('.faq-item').forEach(i => {
    i.classList.remove('open');
    i.querySelector('.faq-a').style.maxHeight = null;
    i.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
  });
  if (!open) {
    item.classList.add('open');
    a.style.maxHeight = a.scrollHeight + 'px';
    q.setAttribute('aria-expanded', 'true');
  }
}));

/* CHATBOT */
const cw = document.getElementById('chatWindow'), cb = document.getElementById('chatBody'),
      chatBtn = document.getElementById('chatBtn'), chips = document.getElementById('chips');
const KB = {
  hire: "Bouncy castles, combi castles with slides, obstacle courses from 30ft up to the 55ft high adrenaline units, a disco dome, sumo suits, the gladiator challenge and marquees.",
  area: "We cover Tipperary and the surrounding areas, including Clonmel, Thurles, Nenagh, Cashel, Roscrea, Tipperary Town, Templemore, Cahir and Carrick on Suir. Use the area checker or tell us your town.",
  package: "Prices depend on the unit, the date and your area. Ring or WhatsApp us and we will give you a price straight away.",
  safe: "We are fully insured and certified with the Irish Inflatable Hirers Federation. Every unit must be supervised by a responsible adult, and we run through the safety points with you at set up.",
  book: "Easiest way is to ring or WhatsApp PHONE_DISPLAY, or send an enquiry through the form with your date, your town and the ages. We will come back to you with a price."
};
function add(t, who) {
  const d = document.createElement('div');
  d.className = 'msg ' + who; d.textContent = t;
  cb.appendChild(d); cb.scrollTop = cb.scrollHeight;
}
if (cw && chatBtn) {
  chatBtn.addEventListener('click', () => {
    const open = cw.classList.toggle('open');
    chatBtn.style.display = open ? 'none' : '';
  });
  const cl = document.getElementById('chatClose');
  if (cl) cl.addEventListener('click', () => {
    cw.classList.remove('open'); chatBtn.style.display = '';
  });
}
if (chips) {
  chips.addEventListener('click', e => {
    const c = e.target.closest('.chip'); if (!c) return;
    add(c.textContent, 'user');
    setTimeout(() => add(KB[c.dataset.q], 'bot'), 350);
  });
}

/* INIT */
const yr = document.getElementById('yr');
if (yr) yr.textContent = new Date().getFullYear();
"""


def build_assets():
    css = CSS.strip() + "\n"
    ASSET_V["css"] = hashlib.md5(css.encode("utf-8")).hexdigest()[:8]
    write("assets/styles.css", css)
    js = JS.replace("PHONE_TEL", D.PHONE_TEL).replace("PHONE_DISPLAY", D.PHONE_DISPLAY)
    js = js.strip() + "\n"
    ASSET_V["js"] = hashlib.md5(js.encode("utf-8")).hexdigest()[:8]
    write("assets/script.js", js)


# ------------------------------------------------------------- fragments ----
# Labels are short on purpose: the nav must stay on one line at 1024px.
NAV = [("/bouncy-castles/", "Castles"), ("/combi-castles/", "Combis"),
       ("/obstacle-courses/", "Obstacle Courses"), ("/disco-dome/", "Disco Dome"),
       ("/marquees/", "Marquees"), ("/areas/", "Areas"), ("/faqs/", "FAQs")]

ICON = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.8.4 1.6.7 2.4a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.8.3 1.5.6 2.3.7a2 2 0 0 1 1.7 2Z"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
}


def ico(name, w=None):
    sw = w or 1.9
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>')


WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3'
          '-.15-1.7-.85-2-.95-.27-.1-.46-.15-.65.15-.2.3-.75.95-.92 1.14-.17.2-.34.22-.63.07-.3-.15'
          '-1.25-.46-2.38-1.47-.88-.78-1.47-1.75-1.64-2.05-.17-.3-.02-.46.13-.6.13-.13.3-.34.45-.5'
          '.15-.18.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.65-1.57-.9-2.15-.23-.56-.47-.48-.65-.5h'
          '-.55c-.2 0-.5.07-.76.37-.27.3-1 1-1 2.42s1.03 2.8 1.17 3c.15.2 2.02 3.08 4.9 4.32.68.3 '
          '1.22.47 1.63.6.69.22 1.31.19 1.8.12.55-.08 1.7-.7 1.94-1.36.24-.67.24-1.24.17-1.36-.07'
          '-.12-.27-.2-.56-.34ZM12 2a10 10 0 0 0-8.5 15.3L2 22l4.8-1.5A10 10 0 1 0 12 2Z"/></svg>')

FB_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12a10 10 0 '
          '1 0-11.5 9.9v-7H8v-2.9h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0'
          '-1.6.8-1.6 1.6v1.9h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12Z"/></svg>')


def wa_link():
    return f"https://wa.me/{D.WHATSAPP}?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20hire."


def head(title, desc, canon, img=None):
    img = img or D.HERO_MAIN
    if img == D.SOON:
        img = D.HERO_MAIN
    if img.startswith("/"):
        img = D.SITE + img
    links = "".join(f'<a href="{u}">{t}</a>' for u, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#111110">
<link rel="canonical" href="{D.SITE}{canon}">
<link rel="icon" href="{FAVICON}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{D.SITE}{canon}">
<meta property="og:type" content="website">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="en_IE">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css?v={ASSET_V["css"]}">
<script>document.documentElement.className+=" js"</script>
</head>
<body>
<a href="#main" class="skip">Skip to content</a>

<header class="nav">
  <div class="wrap">
    {logo()}
    <nav class="navlinks" aria-label="Main">{links}</nav>
    <div class="nav-r">
      <a class="nav-tel" href="tel:{D.PHONE_TEL}">{ico("phone")}<span>{D.PHONE_DISPLAY}</span></a>
      <a href="/contact/" class="btn btn-accent">Get a price</a>
      <button class="burger" id="burger" aria-label="Menu" aria-controls="mobileMenu"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="mobile-menu" id="mobileMenu">{links}<a href="/contact/">Get a price</a></div>
</header>
<main id="main">
"""


def crumbs(trail):
    out = ['<div class="crumb"><a href="/">Home</a>']
    for u, t in trail:
        out.append("<i>/</i>")
        out.append(t if u is None else f'<a href="{u}">{t}</a>')
    return "".join(out) + "</div>"


def page_hero(title, sub, img, trail, tag=None):
    pic = "" if img == D.SOON else f'<div>{shot(img, title, ratio="16/10", eager=True)}</div>'
    grid_open = '<div class="ph-grid">' if pic else "<div>"
    return f"""
<section class="page-hero">
  <div class="wrap">
    {grid_open}
      <div>
        {crumbs(trail)}
        <h1>{title}</h1>
        <p>{sub}</p>
      </div>
      {pic}
    </div>
  </div>
</section>
"""


def card(u):
    return f"""      <a class="card" href="/hire/{u['slug']}/" data-cat="{u['cat']}" data-reveal>
        {shot(u['img'], u['n'], tag=u['tag'])}
        <h3>{esc(u['n'])}</h3>
        <p>{esc(u['short'])}</p>
        <div class="card-foot"><span class="price">{u['price']}</span><span class="card-cta">View</span></div>
      </a>
"""


def safety_box():
    lis = "".join(f"<li>{esc(s)}</li>" for s in D.SAFETY)
    return f'<div class="safety"><h3>Safety and insurance</h3><ul>{lis}</ul></div>'


def contact_block():
    email_row = (f'<a href="mailto:{D.EMAIL}">{ico("phone")}{D.EMAIL}</a>' if D.EMAIL else
                 f'<a href="{wa_link()}" target="_blank" rel="noopener">{WA_SVG}WhatsApp us</a>')
    return f"""
<section class="contact" id="contact">
  <div class="wrap">
    <div class="contact-grid">
      <div>
        <h2>Tell us your date and we will price it</h2>
        <p class="lede">Your town, your date and the ages of the children is all we need. We come straight back to you.</p>
        <div class="contact-list">
          <a href="tel:{D.PHONE_TEL}">{ico("phone")}{D.PHONE_DISPLAY}</a>
          {email_row}
          <div>{ico("pin")}{D.LOCALITY}, {D.REGION}</div>
        </div>
      </div>
      <!-- TODO: replace [FORM-ID] with the real Formspree form ID -->
      <form action="{D.FORMSPREE}" method="POST">
        <div class="fld"><label for="n">Your name</label><input id="n" name="name" type="text" required></div>
        <div class="fld"><label for="p">Phone</label><input id="p" name="phone" type="tel" required></div>
        <div class="fld"><label for="t">Your town</label><input id="t" name="town" type="text"></div>
        <div class="fld"><label for="d">Date of event</label><input id="d" name="date" type="date"></div>
        <div class="fld"><label for="m">What are you after?</label><textarea id="m" name="message" rows="3"></textarea></div>
        <button type="submit" class="btn btn-accent">Send enquiry</button>
      </form>
    </div>
  </div>
</section>
"""


def footer():
    ranges = "".join(f'<a href="/{c["slug"]}/">{c["title"]}</a>' for c in D.CATEGORIES)
    areas = "".join(f'<a href="/{a["slug"]}/">{a["town"]}</a>' for a in D.AREAS[:6])
    wa = wa_link()
    return f"""</main>
<footer>
  <div class="wrap">
    <div class="foot-top">
      <div>
        {logo(cls="brand foot-brand")}
        <p>Bouncy castle, obstacle course, disco dome and marquee hire. Family run in Tipperary since {D.FOUNDED}, fully insured and IIHF certified.</p>
        <div class="socials">
          <!-- TODO: replace [FACEBOOK-URL] with the real page -->
          <a href="{D.FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{FB_SVG}</a>
          <a href="{wa}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}</a>
        </div>
      </div>
      <div class="foot-col"><h4>The range</h4>{ranges}</div>
      <div class="foot-col"><h4>Areas</h4>{areas}<a href="/areas/">All areas</a></div>
      <div class="foot-col"><h4>Get in touch</h4>
        <a href="tel:{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a>
        <a href="/contact/">Send an enquiry</a>
        <a href="/faqs/">FAQs</a>
        <a href="/hire-terms/">Hire terms</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; <span id="yr"></span> {D.NAME}. All rights reserved.</span>
      <span>Site by <a href="https://squaretwo.ie" target="_blank" rel="noopener">SquareTwo</a></span>
    </div>
  </div>
</footer>

<a href="{wa}" target="_blank" rel="noopener" class="wa-float" aria-label="WhatsApp us">{WA_SVG}</a>
<button class="chat-btn" id="chatBtn" aria-label="Open chat">{ico("chat")}</button>
<div class="chat-window" id="chatWindow">
  <div class="chat-head">
    <div><div class="ch-name">{D.NAME}</div><div class="ch-status">We usually reply fast</div></div>
    <button class="chat-close" id="chatClose" aria-label="Close chat">&times;</button>
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
