# -*- coding: utf-8 -*-
"""
Bouncy Castle Man static site generator.

    cd build && python3 generate.py

Reads content from data.py and writes the whole site to the repo root. Safe to
re-run: it only ever overwrites files it generates.

DESIGN (20 Aug 2026, replacing the cartoon "Bounce Land" house style)
Playful and colourful, but as a SYSTEM rather than decoration: every hire
category owns a colour, and that colour follows it everywhere it appears, on
its tile, its cards, its no-photo panels and its page banner. That is why the
page can carry six brights without turning into confetti.

One colour never varies: the call to action is always vermillion, so "the thing
you press" is learnable in one glance.

Fredoka for display, Figtree for body. Soft shapes: cards 16px, inputs 12px,
buttons full pill. No gradients on text, no glows, no clip art.

The design lives in this file (build_assets writes assets/styles.css from the
CSS string below). There is no base.html any more.
"""
import hashlib, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ASSET = {"css": "/assets/styles.css", "js": "/assets/script.js",
         "logo": "/assets/logo.png"}

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Fredoka:wght@500;600;700"
         "&family=Figtree:wght@400;500;600;700;800&display=swap")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(relpath, html):
    full = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    io.open(full, "w", encoding="utf-8", newline="\n").write(full and html)
    return relpath


# ------------------------------------------------------------------ logo ----
# The mark is the castle from Adam's artwork (build/brand/logo.png).
#
# The supplied file was a mascot on a castle, on a black ground with a glow
# around it. The castle cuts out cleanly. The character does not: his trousers
# sit at the same brightness as the glow, so any threshold that removes the
# glow behind him also removes his legs and leaves his shoes floating. Getting
# him back properly needs the logo re-exported on a white or transparent
# ground rather than on black.
#
# The character is composed BESIDE the castle rather than on it, bottom
# aligned with a slight overlap, because his legs cannot be recovered: in the
# supplied file his trousers and the glow behind him are one connected blob at
# the same brightness. Sitting him on the baseline crops him at the hem, which
# reads as a character standing behind the castle rather than a broken cut-out.
# Re-exporting the logo on a white or transparent ground would let the whole
# figure cut in one pass.
#
# The lockup is wide, roughly 2.26:1, so it is sized by WIDTH and the height
# follows. It reads down to about 110px wide.
def logo_mark():
    return (f'<img class="mark" src="{ASSET["logo"]}" alt="" width="510" '
            f'height="226" decoding="async">')


def logo(cls="brand", href="/"):
    """Mark plus the wordmark, set as one name.

    "Man" used to sit in a filled pill. It emphasised the least meaningful word
    in the name for no reason and made the lockup read as two separate things,
    a brand plus a tag. The name is one thing, so it is set as one thing.
    """
    return (f'<a href="{href}" class="{cls}" aria-label="{D.NAME} home">'
            f'{logo_mark()}'
            f'<span class="wordmark">{D.NAME}</span></a>')


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
/* Bouncy Castle Man.
   Layout: persistent left rail + content column. Range shown as horizontal
   scroll shelves, one per category. Sticky action bar on mobile. */

*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;overflow-x:hidden}
img,svg{display:block;max-width:100%}
button,input,select,textarea{font:inherit;color:inherit}
a{color:inherit;text-decoration:none}
h1,h2,h3,h4,p,ul,ol,figure{margin:0}
ul{padding:0;list-style:none}

:root{
  /* ---- the category palette ----------------------------------------------
     Every hire category owns a colour. It follows the category everywhere:
     its shelf, its cards, its no-photo panels, its page banner, its dot in the
     rail. Colour is information here, not decoration.

     --c    the category colour, a FILL
     --ct   the same category as TEXT on a light background
     --on-c what goes ON the fill
     Amber is the reason --c and --ct are separate: it needs ink on it, and as
     text on white it is only 2.07:1, so its text tone is a dark bronze. */
  --c-castle:#2563eb;      /* blue     white 5.17:1 */
  --c-combi:#7c3aed;       /* violet   white 5.70:1 */
  --c-obstacle:#047857;    /* emerald  white 5.48:1 */
  --c-disco:#c81e6a;       /* pink     white 5.45:1 */
  --c-sumo:#f5a300;        /* amber    ink   9.11:1 */
  --c-marquee:#0e7490;     /* teal     white 5.36:1 */
  --ct-sumo:#966300;

  /* The call to action is vermillion everywhere, on every page, so "the thing
     you press" is learnable at a glance. Category colour never reaches a
     button. --accent is large display type and graphic marks only,
     --accent-text is anything under 24px and every filled button. */
  --accent:#f4491f;
  --accent-text:#c9330f;
  --accent-deep:#a8280a;

  --ink:#141310;
  --ink-70:#4c4a44;
  --ink-45:#6b6961;
  --paper:#fffdf7;
  --paper-2:#fff6e6;
  /* Light surfaces. Near-black is no longer used for anything larger than a
     line of text: the rail, the masthead and the footer are all light now, and
     the weight on the page comes from the category colour bands instead. */
  --sky:#e9f1ff;
  --sky-line:#cfe0fb;
  --rail-bg:#fffaf0;
  --rail-line:#f0e6d2;
  --rail-hover:#fff1d8;
  --line:#eee6d5;
  --line-strong:#d9cfb8;

  --r:16px;
  --r-sm:12px;
  --r-pill:999px;

  --rail:286px;   /* wide enough for the full wordmark beside the mark */
  --gut:clamp(20px,3vw,52px);

  --step-0:clamp(16px,.3vw + 15px,17.5px);
  --step-1:clamp(19px,.6vw + 17px,22px);
  --step-2:clamp(24px,1.4vw + 20px,32px);
  --step-3:clamp(28px,2.6vw + 18px,44px);
  --step-4:clamp(36px,4vw + 16px,62px);

  --display:'Fredoka','Figtree',system-ui,sans-serif;
  --body:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;

  --c:var(--accent-text);
  --ct:var(--accent-text);
  --on-c:#fff;
}

/* --ct is written out on every row rather than defaulting to var(--c). A
   custom property holding a var() is substituted where it is DECLARED, not
   where it is used, so the root value would leak into every category. */
[data-cat="castle"]{--c:var(--c-castle);--ct:var(--c-castle);--on-c:#fff}
[data-cat="combi"]{--c:var(--c-combi);--ct:var(--c-combi);--on-c:#fff}
[data-cat="obstacle"]{--c:var(--c-obstacle);--ct:var(--c-obstacle);--on-c:#fff}
[data-cat="disco"]{--c:var(--c-disco);--ct:var(--c-disco);--on-c:#fff}
[data-cat="sumo"]{--c:var(--c-sumo);--ct:var(--ct-sumo);--on-c:var(--ink)}
[data-cat="marquee"]{--c:var(--c-marquee);--ct:var(--c-marquee);--on-c:#fff}

body{font-family:var(--body);font-size:var(--step-0);line-height:1.55;
  color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased}

h1,h2,h3,.display{font-family:var(--display);font-weight:600;line-height:1.06;
  letter-spacing:-.015em}
h1{font-size:var(--step-4)}
h2{font-size:var(--step-3);text-wrap:balance}
h3{font-size:var(--step-1);line-height:1.18}

/* ------------------------------------------------------------- the shell -- */
/* Persistent rail on the left, content column on the right. The rail is a
   real <nav> and comes AFTER <main> in the DOM so the h1 is the first thing
   in the document; grid puts it back on the left visually. */
.shell{display:grid;grid-template-columns:var(--rail) minmax(0,1fr);align-items:start}
.col{grid-column:2;grid-row:1;min-width:0}
.rail{grid-column:1;grid-row:1;position:sticky;top:0;height:100dvh;
  display:flex;flex-direction:column;gap:22px;padding:24px 22px;
  background:var(--rail-bg);color:var(--ink-70);overflow-y:auto;z-index:60;
  border-right:2px solid var(--rail-line)}
.rail-top{display:flex;align-items:center;justify-content:space-between;gap:12px}
.rail .brand{color:var(--ink)}
.mark{flex:none;width:96px;height:auto}
/* In the rail the lockup stacks: the castle is wide and the rail is narrow, so
   side by side would not fit the name. On the mobile top bar it goes back to a
   row, where vertical space is the scarce thing instead. */
.rail .brand{flex-direction:column;align-items:flex-start;gap:9px}
.rail .mark{width:170px}
.rail .wordmark{font-size:19px}
.rail-label{font-size:11px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-45);margin-bottom:10px}
.rail-nav{display:flex;flex-direction:column;gap:1px}
.rail-nav a{display:flex;align-items:center;gap:11px;padding:10px 12px;
  border-radius:var(--r-sm);font-weight:600;font-size:15.5px;
  transition:background .14s,color .14s}
.rail-nav a{color:var(--ink)}
.rail-nav a:hover,.rail-nav a[aria-current="page"]{background:var(--rail-hover);color:var(--ct)}
/* Dots use --ct, not --c: amber sits at 1.99:1 against the light rail. */
.rail-nav .dot{width:11px;height:11px;border-radius:50%;background:var(--ct);flex:none}
.rail-nav .plain{color:var(--ink-70);font-size:14.5px;font-weight:500}
.rail-sec{margin-top:auto}
.rail-tel{display:block;background:#fff;border-radius:var(--r);
  padding:16px 18px;margin-bottom:10px;transition:background .15s;
  border:2px solid var(--rail-line)}
.rail-tel:hover{background:var(--rail-hover)}
.rail-tel span{display:block;font-size:12px;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-45);margin-bottom:4px}
.rail-tel b{font-family:var(--display);font-weight:600;font-size:21px;color:var(--ink);
  letter-spacing:-.02em}
.rail .btn{width:100%}
.rail-legal{font-size:12.5px;color:var(--ink-45);line-height:1.5}
.rail-legal a{text-decoration:underline;text-underline-offset:2px}
.rail-legal a:hover{color:var(--accent-text)}
.burger{display:none;background:none;border:0;padding:8px;cursor:pointer;color:inherit}
.burger span{display:block;width:22px;height:2.5px;border-radius:2px;background:currentColor;
  margin:4px 0}

@media(max-width:1100px){
  .shell{grid-template-columns:1fr}
  .col{grid-column:1;grid-row:2}
  .rail{grid-column:1;grid-row:1;position:sticky;height:auto;flex-direction:column;
    gap:0;padding:12px 20px}
  .rail-top{gap:14px}
  .rail .brand{flex-direction:row;align-items:center;gap:11px}
  .rail .mark{width:96px}
  .rail .wordmark{font-size:17.5px}
  .burger{display:block}
  .rail-body{display:none;padding-top:16px}
  .rail.open .rail-body{display:block}
  .rail-sec{margin-top:18px}
  .rail-nav{gap:0}
}

/* ------------------------------------------------------------ the mark --- */
.brand{display:flex;align-items:center;gap:10px;flex:none;min-width:0}
/* One name, one weight, one colour. No word is emphasised over another. */
.wordmark{font-family:var(--display);font-weight:600;font-size:17.5px;letter-spacing:-.02em;
  white-space:nowrap;line-height:1.1}

/* ------------------------------------------------------------- content --- */
.pad{padding-left:var(--gut);padding-right:var(--gut)}
.band{padding:clamp(48px,5.5vw,86px) var(--gut);position:relative}
.band-tight{padding-bottom:clamp(20px,2vw,30px)}
.tint{background:var(--paper-2)}
.lede{font-size:var(--step-1);color:var(--ink-70);max-width:58ch;font-weight:500}
.prose{max-width:65ch;color:var(--ink-70);font-weight:450}
.prose p{margin-bottom:16px}
.prose h2{margin:34px 0 14px}
.narrow{max-width:1080px}

.eyebrow{display:inline-block;font-size:12.5px;font-weight:800;letter-spacing:.1em;
  text-transform:uppercase;color:var(--accent-text);background:#ffe9e2;
  border-radius:var(--r-pill);padding:7px 15px;margin-bottom:16px}
.sec-head{margin-bottom:clamp(24px,3vw,40px);max-width:70ch}
.sec-head p{margin-top:14px;color:var(--ink-70);font-size:var(--step-1);max-width:56ch}

/* ------------------------------------------------------------- buttons --- */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;
  padding:15px 26px;border-radius:var(--r-pill);border:2px solid transparent;
  font-family:var(--body);font-weight:800;font-size:15.5px;white-space:nowrap;
  cursor:pointer;transition:background .15s,color .15s,border-color .15s,
  transform .12s cubic-bezier(.2,.8,.3,1),box-shadow .15s}
.btn:hover{transform:translateY(-2px)}
.btn:active{transform:translateY(1px)}
.btn-accent{background:var(--accent-text);color:#fff;box-shadow:0 4px 0 var(--accent-deep)}
.btn-accent:hover{background:var(--accent);box-shadow:0 6px 0 var(--accent-deep)}
.btn-accent:active{box-shadow:0 2px 0 var(--accent-deep)}
.btn-ink{background:var(--ink);color:#fff;box-shadow:0 4px 0 #000}
.btn-ink:hover{box-shadow:0 6px 0 #000}
.btn-line{background:#fff;color:var(--ink);border-color:var(--line-strong)}
.btn-line:hover{border-color:var(--ink)}
.btn-ghost{background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.22)}
.btn-ghost:hover{background:rgba(255,255,255,.18)}
.btn svg{width:17px;height:17px;flex:none}

/* -------------------------------------------------------------- masthead -- */
/* Not a centred hero. A wide colour block with the headline bottom-left and
   the photo bleeding off the right edge, then the facts sitting on the seam. */
.mast{background:var(--sky);color:var(--ink);position:relative;overflow:hidden;
  padding:clamp(40px,4.6vw,72px) var(--gut) clamp(74px,7vw,110px)}
.mast-grid{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(0,.88fr);
  gap:clamp(24px,3.5vw,54px);align-items:end;position:relative;z-index:2}
/* The masthead headline is capped below the global display size: the left
   column is narrow because the rail takes 266px, and the hard rule is that
   the headline never runs past two lines on desktop. */
.mast h1{font-size:clamp(33px,3vw + 14px,52px);max-width:19ch;text-wrap:balance}
.mast h1 em{font-style:normal;color:var(--accent-text)}
.mast p{margin-top:18px;font-size:var(--step-1);color:var(--ink-70);max-width:46ch;
  font-weight:500}
.mast-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.mast-shot{position:relative}
.mast-shot .pic{--ratio:4/3.2;border:3px solid var(--ink);transform:rotate(-1.6deg);
  box-shadow:12px 12px 0 var(--c-castle)}
.mast-tag{position:absolute;left:-10px;bottom:-14px;background:var(--c-sumo);color:var(--ink);
  padding:10px 18px;border-radius:var(--r-pill);font-family:var(--display);font-weight:600;
  font-size:14.5px;transform:rotate(-3deg)}
.mast::before{content:"";position:absolute;width:420px;height:420px;border-radius:50%;
  right:-150px;top:-190px;background:var(--c-combi);opacity:.16}
.mast::after{content:"";position:absolute;width:190px;height:190px;border-radius:50%;
  left:-80px;bottom:-70px;background:var(--c-sumo);opacity:.3}
/* The rail keeps 266px, so between 1100 and 1360 the masthead's left column
   is too narrow to hold the headline to two lines. Stack it instead. */
@media(max-width:1360px){.mast-grid{grid-template-columns:1fr}
  .mast-shot{order:-1;margin-bottom:10px;max-width:560px}}

/* Facts sit across the seam between the masthead and the page. */
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;
  margin:-58px var(--gut) 0;position:relative;z-index:3}
.facts div{background:#fff;border:2px solid var(--line);border-radius:var(--r);
  padding:20px 22px;box-shadow:0 8px 0 -2px rgba(20,19,16,.07)}
.facts div:nth-child(1){--fc:var(--c-castle)}
.facts div:nth-child(2){--fc:var(--c-obstacle)}
.facts div:nth-child(3){--fc:var(--c-disco)}
.facts b{display:block;font-family:var(--display);font-weight:600;font-size:var(--step-2);
  color:var(--fc);line-height:1.1;margin-bottom:2px}
.facts span{color:var(--ink-70);font-size:14.5px;font-weight:500}
@media(max-width:760px){.facts{grid-template-columns:1fr;margin-top:-40px}}

/* -------------------------------------------------------------- picture -- */
.pic{display:block;position:relative;aspect-ratio:var(--ratio,4/3);overflow:hidden;
  border-radius:var(--r);background:var(--paper-2)}
.pic img{width:100%;height:100%;object-fit:cover}
/* No photo yet: the unit's name set large on its own category colour. Reads as
   a designed object, and colour-codes the shelf. Set img= in data.py to swap. */
.pic-panel{background:var(--c);color:var(--on-c);display:flex;flex-direction:column;
  justify-content:flex-end;padding:18px}
.pic-panel .panel-name{font-family:var(--display);font-weight:600;line-height:1.08;
  font-size:clamp(17px,1.6vw,23px);max-width:13ch;overflow-wrap:break-word}
.pic-panel::after{content:"";position:absolute;width:92px;height:92px;border-radius:50%;
  right:-24px;top:-24px;background:currentColor;opacity:.16}

/* --------------------------------------------------------------- shelves -- */
/* The range is six horizontal shelves, one per category, instead of a tile
   grid plus a filtered grid. Each shelf scroll-snaps and is keyboard and
   touch scrollable; the arrows are an enhancement, not the only way through. */
.shelf{margin-bottom:clamp(34px,4vw,58px)}
.shelf-head{display:flex;align-items:center;gap:14px;padding:0 var(--gut);
  margin-bottom:16px;flex-wrap:wrap}
.shelf-head .dot{width:14px;height:14px;border-radius:50%;background:var(--c);flex:none}
.shelf-head h3{font-size:var(--step-2);margin-right:auto}
.shelf-head .all{font-size:14.5px;font-weight:800;color:var(--ct);white-space:nowrap}
.shelf-head .all:hover{text-decoration:underline;text-underline-offset:3px}
.shelf-nav{display:flex;gap:7px}
.shelf-nav button{width:38px;height:38px;border-radius:50%;border:2px solid var(--line-strong);
  background:#fff;cursor:pointer;display:grid;place-items:center;
  transition:border-color .14s,background .14s,transform .12s}
.shelf-nav button:hover{border-color:var(--c);transform:translateY(-2px)}
.shelf-nav button:disabled{opacity:.35;cursor:default;transform:none;
  border-color:var(--line)}
.shelf-nav svg{width:16px;height:16px}
.track{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(232px,268px);gap:16px;
  overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;
  padding:4px var(--gut) 14px;scrollbar-width:thin}
.track>*{scroll-snap-align:start}
.track::-webkit-scrollbar{height:8px}
.track::-webkit-scrollbar-thumb{background:var(--line-strong);border-radius:var(--r-pill)}
/* On touch you swipe the shelf, so the arrows are dead weight and at 320px
   they push the header row past the viewport. */
@media(max-width:640px){.shelf-nav{display:none}}
@media(max-width:560px){.track{grid-auto-columns:minmax(210px,74%)}}

/* ----------------------------------------------------------------- card -- */
.card{min-width:0;display:flex;flex-direction:column;color:inherit;background:#fff;
  border:2px solid var(--line);border-radius:var(--r);padding:11px 11px 15px;
  transition:transform .2s cubic-bezier(.2,.8,.3,1),border-color .16s,box-shadow .16s}
.card:hover{transform:translateY(-5px);border-color:var(--c);box-shadow:0 10px 0 -2px var(--c)}
.card .pic{--ratio:4/3}
.card-tag{position:absolute;top:9px;left:9px;z-index:2;background:#fff;color:var(--ink);
  font-size:10.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;
  padding:5px 10px;border-radius:var(--r-pill);box-shadow:0 1px 4px rgba(20,19,16,.18)}

.card h3{margin:13px 3px 0;font-size:17px}
.card p{color:var(--ink-70);font-size:14.5px;margin:6px 3px 0;font-weight:450;flex:1}
.card-foot{margin:13px 3px 0;padding-top:11px;border-top:2px solid var(--line);
  display:flex;align-items:center;justify-content:space-between;gap:10px}
.price{font-family:var(--display);font-weight:600;font-size:15.5px}
.card-cta{font-size:13.5px;font-weight:800;color:var(--accent-text)}
.card:hover .card-cta{text-decoration:underline;text-underline-offset:3px}

/* A plain grid, used on the category, area and unit pages where the set is
   small and complete. The home page uses shelves instead. */
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
@media(max-width:1500px){.grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:1040px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.grid{grid-template-columns:1fr}}

/* ------------------------------------------------------------- timeline -- */
/* How it works, as a horizontal run with a connecting line rather than cards. */
.line{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;position:relative}
.line::before{content:"";position:absolute;left:23px;right:23px;top:23px;height:3px;
  background:repeating-linear-gradient(90deg,var(--line-strong) 0 9px,transparent 9px 18px)}
.line-step{position:relative}
.line-step:nth-child(1){--lc:var(--c-combi)}
.line-step:nth-child(2){--lc:var(--c-marquee)}
.line-step:nth-child(3){--lc:var(--c-obstacle)}
.line-n{width:46px;height:46px;border-radius:50%;background:var(--lc);color:#fff;
  display:grid;place-items:center;font-family:var(--display);font-weight:600;font-size:20px;
  position:relative;z-index:1;margin-bottom:16px;border:4px solid var(--paper)}
.tint .line-n{border-color:var(--paper-2)}
.line-step p{color:var(--ink-70);font-size:15.5px;margin-top:8px;font-weight:450}
@media(max-width:820px){.line{grid-template-columns:1fr;gap:22px}
  .line::before{left:23px;right:auto;top:23px;bottom:23px;width:3px;height:auto;
    background:repeating-linear-gradient(180deg,var(--line-strong) 0 9px,transparent 9px 18px)}
  .line-step{padding-left:0}}

/* ----------------------------------------------------------------- why --- */
/* Bento, not a list: one wide cell then five. Exactly six cells for six points. */
.bento{display:grid;grid-template-columns:repeat(6,1fr);gap:16px}
.bento li{grid-column:span 2;background:#fff;border:2px solid var(--line);
  border-radius:var(--r);padding:24px}
/* Six points, six cells, no gaps: 1 wide, then 3, then 2 half-width. A bento
   with an empty cell at the end means the grid was planned wrong. */
.bento li:nth-child(5),.bento li:nth-child(6){grid-column:span 3}
.bento li:nth-child(1){grid-column:span 6;display:grid;
  grid-template-columns:auto minmax(0,1fr);gap:20px;align-items:center;
  background:var(--c-sumo);color:var(--ink);border-color:var(--c-sumo)}
.bento li:nth-child(1) p{color:#4a3608;font-size:var(--step-1)}
.bento li:nth-child(1) .n{width:52px;height:52px;font-size:19px}
.bento li:nth-child(6n+1){--wc:var(--c-sumo)}
.bento li:nth-child(6n+2){--wc:var(--c-castle)}
.bento li:nth-child(6n+3){--wc:var(--c-obstacle)}
.bento li:nth-child(6n+4){--wc:var(--c-combi)}
.bento li:nth-child(6n+5){--wc:var(--c-disco)}
.bento li:nth-child(6n+6){--wc:var(--c-marquee)}
.bento .n{width:38px;height:38px;border-radius:50%;background:var(--wc);color:#fff;
  display:grid;place-items:center;font-family:var(--display);font-weight:600;font-size:15px;
  margin-bottom:14px}
.bento li:nth-child(1) .n{margin-bottom:0;background:var(--ink);color:var(--c-sumo)}
.bento p{color:var(--ink-70);font-size:15px;margin-top:7px;font-weight:450}
@media(max-width:1000px){.bento{grid-template-columns:repeat(4,1fr)}
  .bento li,.bento li:nth-child(5){grid-column:span 2}
  .bento li:nth-child(1),.bento li:nth-child(6){grid-column:span 4}}
@media(max-width:620px){.bento{grid-template-columns:1fr}
  .bento li,.bento li:nth-child(1){grid-column:span 1}
  .bento li:nth-child(1){grid-template-columns:1fr}}

/* --------------------------------------------------------------- areas --- */
/* Full-bleed colour band. Towns as big type, checker sitting inside it. */
.areas-band{background:var(--c-marquee);color:#fff;position:relative;overflow:hidden}
.areas-band::after{content:"";position:absolute;width:300px;height:300px;border-radius:50%;
  right:-110px;bottom:-140px;background:#fff;opacity:.08}
.areas-band .sec-head p{color:#e2f3f8}
.town-list{display:flex;flex-wrap:wrap;gap:10px;position:relative;z-index:1}
.town-list a{display:block;padding:12px 22px;border-radius:var(--r-pill);
  border:2px solid rgba(255,255,255,.34);font-family:var(--display);font-weight:600;
  font-size:19px;transition:background .15s,transform .15s,border-color .15s}
.town-list a:hover{background:#fff;color:var(--c-marquee);border-color:#fff;
  transform:translateY(-3px)}
.checker{margin-top:30px;background:rgba(255,255,255,.12);border-radius:var(--r);
  padding:24px 26px;position:relative;z-index:1;max-width:640px}
.checker h3{margin-bottom:12px}
.checker-row{display:flex;gap:10px;flex-wrap:wrap}
.checker select{flex:1;min-width:170px;padding:13px 15px;border:2px solid transparent;
  border-radius:var(--r-sm);background:#fff;color:var(--ink);font-size:15px}
.checker select:focus{outline:3px solid var(--c-sumo);outline-offset:1px}
#areaOut{margin-top:13px;font-size:15.5px;font-weight:700;min-height:22px}

/* Areas index: full-width rows with a rule, not a card grid. */
.area-rows{display:grid;gap:0}
.area-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:24px;
  padding:22px 0;border-top:2px solid var(--line);align-items:baseline}
.area-row:last-child{border-bottom:2px solid var(--line)}
.area-row h3{font-size:var(--step-2)}
.area-row h3 a:hover{color:var(--accent-text)}
.area-row p{color:var(--ink-70);font-weight:450}
@media(max-width:760px){.area-row{grid-template-columns:1fr;gap:6px}}

/* ------------------------------------------------------------- reviews --- */
/* Staggered, not three equal columns. */
.revs{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;align-items:start}
.rev{background:#fff;border:2px solid var(--line);border-radius:var(--r);padding:26px}
.rev:nth-child(1){--rc:var(--c-disco);margin-top:30px}
.rev:nth-child(2){--rc:var(--c-castle)}
.rev:nth-child(3){--rc:var(--c-obstacle);margin-top:52px}
.rev .stars{color:var(--ct-sumo);font-size:14px;letter-spacing:3px;margin-bottom:12px}
.rev p{font-family:var(--display);font-weight:500;font-size:var(--step-1);line-height:1.35}
.rev .who{margin-top:16px;padding-top:14px;border-top:2px solid var(--line);
  font-size:14px;font-weight:700;color:var(--rc)}
@media(max-width:900px){.revs{grid-template-columns:1fr}
  .rev,.rev:nth-child(1),.rev:nth-child(3){margin-top:0}}

/* ----------------------------------------------------------------- faq --- */
.faq{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}
.faq-item{background:#fff;border:2px solid var(--line);border-radius:var(--r);
  transition:border-color .16s}
.faq-item.open{border-color:var(--accent)}
.faq-q{width:100%;background:none;border:0;text-align:left;cursor:pointer;
  padding:20px 54px 20px 22px;font-family:var(--display);font-weight:600;
  font-size:var(--step-1);position:relative;line-height:1.25}
.faq-q::after{content:"";position:absolute;right:18px;top:50%;width:26px;height:26px;
  margin-top:-13px;border-radius:50%;background:var(--paper-2);transition:background .2s}
.faq-q::before{content:"";position:absolute;right:24px;top:50%;width:14px;height:14px;
  margin-top:-7px;z-index:1;background:var(--ink);transition:transform .25s,background .2s;
  clip-path:polygon(43% 0,57% 0,57% 43%,100% 43%,100% 57%,57% 57%,57% 100%,43% 100%,43% 57%,0 57%,0 43%,43% 43%)}
.faq-item.open .faq-q::after{background:var(--accent-text)}
.faq-item.open .faq-q::before{transform:rotate(135deg);background:#fff}
.faq-a{max-height:0;overflow:hidden;transition:max-height .3s ease}
.faq-a p{padding:0 22px 20px;color:var(--ink-70);font-weight:450}
@media(max-width:820px){.faq{grid-template-columns:1fr}}

/* ------------------------------------------------------------- notices --- */
.note{background:#fff4de;border:2px solid #f0dfb8;border-radius:var(--r);padding:20px 24px;
  font-size:15.5px;font-weight:500;max-width:70ch}
.safety{background:#fff;border:2px solid var(--line);border-radius:var(--r);
  padding:26px 28px;margin-top:30px;max-width:70ch}
.safety h3{margin-bottom:14px}
.safety li{position:relative;padding-left:30px;margin-bottom:11px;color:var(--ink-70);
  font-size:15.5px;font-weight:450}
.safety li::before{content:"";position:absolute;left:0;top:5px;width:16px;height:16px;
  border-radius:50%;background:var(--c-obstacle)}
.safety li::after{content:"";position:absolute;left:4.5px;top:10px;width:7px;height:4px;
  border-left:2px solid #fff;border-bottom:2px solid #fff;transform:rotate(-45deg)}

/* ----------------------------------------------------------- page hero --- */
.page-hero{background:var(--c);color:var(--on-c);padding:clamp(36px,4vw,58px) var(--gut);
  position:relative;overflow:hidden}
.page-hero::after{content:"";position:absolute;width:280px;height:280px;border-radius:50%;
  right:-90px;top:-120px;background:currentColor;opacity:.1}
.page-hero .crumb{font-size:14px;font-weight:700;margin-bottom:16px;opacity:.85}
.page-hero .crumb a:hover{text-decoration:underline}
.page-hero .crumb i{font-style:normal;margin:0 8px;opacity:.55}
.page-hero h1{max-width:17ch}
.page-hero p{margin-top:15px;font-size:var(--step-1);max-width:54ch;font-weight:500;opacity:.93}
.ph-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(24px,3.5vw,50px);
  align-items:center;position:relative;z-index:1}
.ph-grid .pic{--ratio:16/10;border:3px solid var(--ink)}
@media(max-width:900px){.ph-grid{grid-template-columns:1fr}.ph-grid .pic{display:none}}

/* ------------------------------------------------------------- unit pg --- */
.unit{display:grid;grid-template-columns:minmax(0,1fr) 330px;
  gap:clamp(26px,3.5vw,52px);align-items:start}
.unit>div>.pic{--ratio:16/10;border:3px solid var(--ink)}
.unit h2{font-size:var(--step-2);margin:30px 0 14px}
.unit-side{background:#fff;border:2px solid var(--line);border-radius:var(--r);padding:24px;
  position:sticky;top:22px;display:flex;flex-direction:column;gap:11px}
.unit-side .price{font-size:var(--step-2);color:var(--ct)}
.unit-side>p{color:var(--ink-70);font-size:14.5px;font-weight:450;margin-bottom:6px}
.unit-side .btn{width:100%}
.specs{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:26px 0 0}
.spec{background:#fff;border:2px solid var(--line);border-radius:var(--r-sm);padding:16px 18px}
.spec dt{font-size:11.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;
  color:var(--ct);margin-bottom:5px}
.spec dd{margin:0;font-family:var(--display);font-weight:600;font-size:16.5px}
@media(max-width:1000px){.unit{grid-template-columns:1fr}.unit-side{position:static}}
@media(max-width:520px){.specs{grid-template-columns:1fr}}

/* ------------------------------------------------------------- gallery --- */
.gallery{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.gallery .pic{--ratio:1/1}
.gallery a:nth-child(6n+1){grid-column:span 2}
.gallery a:nth-child(6n+1) .pic{--ratio:2/1}
@media(max-width:860px){.gallery{grid-template-columns:repeat(2,1fr)}}

/* ------------------------------------------------------------- contact --- */
.contact{background:var(--accent-text);color:#fff;position:relative;overflow:hidden}
.contact::after{content:"";position:absolute;width:320px;height:320px;border-radius:50%;
  left:-130px;bottom:-160px;background:#fff;opacity:.08}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,3.5vw,58px);
  align-items:start;position:relative;z-index:1}
.contact h2{max-width:15ch}
.contact .lede{color:#fff0ec;margin-top:16px}
.contact-list{margin-top:26px;display:flex;flex-direction:column;gap:10px}
.contact-list a,.contact-list div{display:flex;align-items:center;gap:12px;
  padding:14px 20px;border-radius:var(--r-pill);background:rgba(255,255,255,.13);
  font-weight:700;font-size:16.5px}
.contact-list a:hover{background:rgba(255,255,255,.22)}
.contact-list svg{width:19px;height:19px;flex:none}
form{background:#fff;border-radius:var(--r);padding:26px;color:var(--ink)}
.fld{display:flex;flex-direction:column;gap:7px;margin-bottom:14px}
.fld label{font-size:13.5px;font-weight:800;color:var(--ink-70)}
.fld input,.fld textarea{padding:13px 15px;border:2px solid var(--line-strong);
  border-radius:var(--r-sm);font-size:15.5px;background:#fff;color:var(--ink);width:100%}
.fld input:focus,.fld textarea:focus{outline:3px solid var(--accent);outline-offset:1px;
  border-color:var(--accent)}
.fld textarea{resize:vertical;min-height:84px}
form .btn{width:100%;margin-top:6px}
@media(max-width:900px){.contact-grid{grid-template-columns:1fr}}

/* -------------------------------------------------------------- footer --- */
footer{background:var(--paper-2);color:var(--ink-70);
  padding:clamp(44px,4.5vw,68px) var(--gut) 28px;font-size:15px;
  border-top:2px solid var(--line)}
.foot-top{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:34px}
.foot-col h4{font-family:var(--display);font-weight:600;font-size:15px;color:var(--ink);
  margin-bottom:13px}
.foot-col a{display:block;padding:5px 0;transition:color .14s}
.foot-col a:hover{color:var(--accent-text)}
.foot-top>div>p{max-width:36ch;font-weight:450;line-height:1.6;margin-top:14px}
.socials{display:flex;gap:10px;margin-top:18px}
.socials a{width:40px;height:40px;border:2px solid var(--line-strong);border-radius:50%;
  display:grid;place-items:center;transition:background .14s,border-color .14s,transform .14s}
.socials a:hover{background:var(--accent);border-color:var(--accent);color:#fff;
  transform:translateY(-2px)}
.socials svg{width:17px;height:17px}
.foot-bottom{margin-top:40px;padding-top:22px;border-top:2px solid var(--line);
  display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:14px}
.foot-bottom a{text-decoration:underline;text-underline-offset:2px}
.foot-bottom a:hover{color:var(--accent-text)}
@media(max-width:820px){.foot-top{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.foot-top{grid-template-columns:1fr}}

/* ---------------------------------------------------------- action bar --- */
/* Mobile only. Replaces the floating bubbles: the two things a parent actually
   wants are a phone call and WhatsApp, so they get a real bar. */
.actionbar{display:none;position:fixed;left:0;right:0;bottom:0;z-index:80;
  background:rgba(255,253,247,.97);backdrop-filter:blur(8px);padding:10px 14px;
  gap:10px;border-top:2px solid var(--line-strong)}
.actionbar a{flex:1;display:flex;align-items:center;justify-content:center;gap:8px;
  padding:14px 10px;border-radius:var(--r-pill);font-weight:800;font-size:15px}
.actionbar .ab-call{background:var(--accent-text);color:#fff}
.actionbar .ab-wa{background:#1eaf53;color:#fff}
.actionbar svg{width:18px;height:18px}
@media(max-width:1100px){.actionbar{display:flex}
  footer{padding-bottom:96px}}

/* Desktop keeps one WhatsApp button, bottom right, out of the rail's way. */
.wa-float{position:fixed;right:20px;bottom:20px;z-index:70;width:54px;height:54px;
  border-radius:50%;background:#1eaf53;color:#fff;display:grid;place-items:center;
  box-shadow:0 6px 22px rgba(20,19,16,.26);transition:transform .18s}
.wa-float:hover{transform:translateY(-4px) rotate(-6deg)}
.wa-float svg{width:27px;height:27px}
@media(max-width:1100px){.wa-float{display:none}}

/* -------------------------------------------------------------- motion --- */
/* Reveal is opt-in via the .js class set by an inline script in the head.
   Without JS, or if the script fails, everything renders visible. Content must
   never be hidden by a broken animation. */
.js [data-reveal]{opacity:0;transform:translateY(18px);
  transition:opacity .55s cubic-bezier(.2,.7,.3,1),transform .55s cubic-bezier(.2,.7,.3,1)}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .track{scroll-behavior:auto}
  .js [data-reveal]{opacity:1!important;transform:none!important;transition:none}
  *{animation-duration:.01ms!important;transition-duration:.01ms!important}
}

/* ---------------------------------------------------------------- a11y --- */
:focus-visible{outline:3px solid var(--accent);outline-offset:2px;border-radius:4px}

.skip{position:absolute;left:-9999px;top:0;background:var(--ink);color:#fff;
  padding:12px 18px;z-index:100}
.skip:focus{left:0}
::selection{background:var(--accent);color:#fff}
"""

JS = r"""
/* Bouncy Castle Man, shared behaviour. Loaded on every page.
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

/* RAIL: top bar plus drawer below 1100px */
const burger = document.getElementById('burger'), rail = document.getElementById('rail');
if (burger && rail) {
  burger.addEventListener('click', () => {
    const open = rail.classList.toggle('open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  rail.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    rail.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
  }));
}

/* SHELVES: the arrows are an enhancement. The track scrolls by touch, wheel
   and keyboard on its own, so if this never runs nothing is lost. */
document.querySelectorAll('[data-shelf]').forEach(shelf => {
  const track = shelf.querySelector('.track');
  const prev = shelf.querySelector('[data-dir="prev"]');
  const next = shelf.querySelector('[data-dir="next"]');
  if (!track || !prev || !next) return;

  const step = () => {
    const card = track.firstElementChild;
    if (!card) return track.clientWidth;
    const gap = parseFloat(getComputedStyle(track).columnGap) || 16;
    return (card.getBoundingClientRect().width + gap) * Math.max(1,
      Math.floor(track.clientWidth / (card.getBoundingClientRect().width + gap)) - 1);
  };
  const sync = () => {
    const max = track.scrollWidth - track.clientWidth - 2;
    prev.disabled = track.scrollLeft <= 2;
    next.disabled = track.scrollLeft >= max;
  };
  prev.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
  next.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
  track.addEventListener('scroll', sync, { passive: true });
  window.addEventListener('resize', sync);
  sync();
});

/* AREA CHECKER */
const areaBtn = document.getElementById('areaBtn');
if (areaBtn) {
  areaBtn.addEventListener('click', () => {
    const v = document.getElementById('areaSel').value, r = document.getElementById('areaOut');
    if (!v) { r.textContent = 'Pick your area first.'; return; }
    if (v === '__other__') {
      r.innerHTML = 'Not listed? <a href="tel:PHONE_TEL" style="text-decoration:underline">Give us a call</a>, we may still reach you.';
    } else {
      r.textContent = 'Yes, we deliver to ' + v + '. Send us your date for a price.';
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

/* INIT */
const yr = document.getElementById('yr');
if (yr) yr.textContent = new Date().getFullYear();
"""


def build_assets():
    """Write the stylesheet and script with their content hash in the FILENAME.

    Not in a query string. /assets/ is served with Cache-Control immutable for a
    year, and a browser that cached styles.css?v=X will keep serving that file
    for a year if the URL does not change. It bit us once already: the redesign
    shipped against a year-cached copy of the old stylesheet. A hashed filename
    cannot go stale, because new content means a new file.
    """
    adir = os.path.join(ROOT, "assets")
    os.makedirs(adir, exist_ok=True)
    for f in os.listdir(adir):
        if re.fullmatch(r"(styles|script|logo)\.[0-9a-f]{8}\.(css|js|png)", f):
            os.remove(os.path.join(adir, f))

    # Brand artwork. The logo is hashed like the stylesheet because /assets/ is
    # served immutable for a year; the icons go to the root, which is not.
    bdir = os.path.join(HERE, "brand")
    raw = io.open(os.path.join(bdir, "logo.png"), "rb").read()
    h = hashlib.md5(raw).hexdigest()[:8]
    ASSET["logo"] = "/assets/logo.%s.png" % h
    io.open(os.path.join(adir, "logo.%s.png" % h), "wb").write(raw)
    for icon in ("favicon.png", "apple-touch-icon.png"):
        io.open(os.path.join(ROOT, icon), "wb").write(
            io.open(os.path.join(bdir, icon), "rb").read())

    css = CSS.strip() + "\n"
    h = hashlib.md5(css.encode("utf-8")).hexdigest()[:8]
    ASSET["css"] = "/assets/styles.%s.css" % h
    write("assets/styles.%s.css" % h, css)

    js = JS.replace("PHONE_TEL", D.PHONE_TEL).replace("PHONE_DISPLAY", D.PHONE_DISPLAY)
    js = js.strip() + "\n"
    h = hashlib.md5(js.encode("utf-8")).hexdigest()[:8]
    ASSET["js"] = "/assets/script.%s.js" % h
    write("assets/script.%s.js" % h, js)


# ------------------------------------------------------------- fragments ----
# Labels are short on purpose: the nav must stay on one line at 1024px.
NAV = [("/bouncy-castles/", "Castles"), ("/combi-castles/", "Combis"),
       ("/obstacle-courses/", "Obstacle Courses"), ("/disco-dome/", "Disco Dome"),
       ("/marquees/", "Marquees"), ("/areas/", "Areas"), ("/faqs/", "FAQs")]

ICON = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.8.4 1.6.7 2.4a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.8.3 1.5.6 2.3.7a2 2 0 0 1 1.7 2Z"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "left": '<path d="m15 18-6-6 6-6"/>',
    "right": '<path d="m9 18 6-6-6-6"/>',
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
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#141310">
<link rel="canonical" href="{D.SITE}{canon}">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
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
<link rel="stylesheet" href="{ASSET["css"]}">
<script>document.documentElement.className+=" js"</script>
</head>
<body>
<a href="#main" class="skip">Skip to content</a>
<div class="shell">
<div class="col">
<main id="main">
"""


def rail(current=None):
    """The persistent left rail. Emitted AFTER the content column in the DOM so
    the h1 is the first thing in the document; grid puts it back on the left.
    Below 1100px it becomes a top bar with a drawer."""
    def row(href, label, cat=None):
        cur = ' aria-current="page"' if href == current else ""
        dot = f'<span class="dot"></span>' if cat else ""
        attr = f' data-cat="{cat}"' if cat else ""
        cls = "" if cat else ' class="plain"'
        return f'<a href="{href}"{attr}{cur}{cls}>{dot}{label}</a>'

    cats = "".join(row(f'/{c["slug"]}/', c["title"], c["cat"]) for c in D.CATEGORIES)
    more = "".join(row(h, t) for h, t in
                   [("/areas/", "Areas we cover"), ("/gallery/", "Gallery"),
                    ("/faqs/", "FAQs"), ("/hire-terms/", "Hire terms"),
                    ("/contact/", "Contact")])
    return f"""
<nav class="rail" id="rail" aria-label="Main">
  <div class="rail-top">
    {logo()}
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="railBody"><span></span><span></span><span></span></button>
  </div>
  <div class="rail-body" id="railBody">
    <div>
      <div class="rail-label">What we hire</div>
      <div class="rail-nav">{cats}</div>
    </div>
    <div style="margin-top:20px">
      <div class="rail-label">More</div>
      <div class="rail-nav">{more}</div>
    </div>
    <div class="rail-sec">
      <a class="rail-tel" href="tel:{D.PHONE_TEL}"><span>Ring us</span><b>{D.PHONE_DISPLAY}</b></a>
      <a href="/contact/" class="btn btn-accent">Get a price</a>
      <p class="rail-legal" style="margin-top:18px">Family run in {D.LOCALITY} since {D.FOUNDED}. Fully insured and IIHF certified.<br>Site by <a href="https://squaretwo.ie" target="_blank" rel="noopener">SquareTwo</a></p>
    </div>
  </div>
</nav>
"""


def crumbs(trail):
    out = ['<div class="crumb"><a href="/">Home</a>']
    for u, t in trail:
        out.append("<i>/</i>")
        out.append(t if u is None else f'<a href="{u}">{t}</a>')
    return "".join(out) + "</div>"


def page_hero(title, sub, img, trail, cat="castle"):
    """Inner page banner, painted in the colour of whatever the page is for.

    `cat` is a category key from data.py (castle, combi, obstacle, disco, sumo,
    marquee). Pages that are not about a single category still pick one, so the
    banner always sits inside the palette rather than inventing a colour.
    """
    pic = "" if img == D.SOON else f'<div>{shot(img, title, ratio="16/10", eager=True)}</div>'
    grid_open = '<div class="ph-grid">' if pic else "<div>"
    return f"""
<section class="page-hero" data-cat="{cat}">
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
    # No data-reveal on the card itself. Cards live inside horizontally
    # scrolling shelves, where an IntersectionObserver can miss one and leave
    # it permanently at opacity 0. The shelf reveals as a whole instead.
    return f"""      <a class="card" href="/hire/{u['slug']}/" data-cat="{u['cat']}">
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
<section class="contact band" id="contact">
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
</section>
"""


def footer():
    ranges = "".join(f'<a href="/{c["slug"]}/">{c["title"]}</a>' for c in D.CATEGORIES)
    areas = "".join(f'<a href="/{a["slug"]}/">{a["town"]}</a>' for a in D.AREAS[:6])
    wa = wa_link()
    return f"""</main>
<footer>
  <div class="foot-top">
    <div>
      {logo()}
      <p>Bouncy castle, obstacle course, disco dome and marquee hire across Tipperary. Family run since {D.FOUNDED}, fully insured and certified with the Irish Inflatable Hirers Federation.</p>
      <div class="socials">
        <!-- TODO: replace [FACEBOOK-URL] with the real page -->
        <a href="{D.FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{FB_SVG}</a>
        <a href="{wa}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}</a>
      </div>
    </div>
    <div class="foot-col"><h4>The range</h4>{ranges}</div>
    <div class="foot-col"><h4>Areas</h4>{areas}<a href="/areas/">All areas</a></div>
  </div>
  <div class="foot-bottom">
    <span>&copy; <span id="yr"></span> {D.NAME}. All rights reserved.</span>
    <span><a href="tel:{D.PHONE_TEL}">{D.PHONE_DISPLAY}</a> &nbsp; <a href="/hire-terms/">Hire terms</a></span>
  </div>
</footer>
</div>
{rail()}
</div>

<a href="{wa}" target="_blank" rel="noopener" class="wa-float" aria-label="WhatsApp us">{WA_SVG}</a>
<div class="actionbar">
  <a class="ab-call" href="tel:{D.PHONE_TEL}">{ico("phone")}Call us</a>
  <a class="ab-wa" href="{wa}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a>
</div>
<script src="{ASSET["js"]}"></script>
</body>
</html>
"""


if __name__ == "__main__":
    # pages.py does `import generate`. Without this alias Python loads this file
    # a SECOND time under the name "generate", with its own fresh ASSET dict, so
    # build_assets() would populate one copy while the pages were built from the
    # other. That shipped every page pointing at a placeholder asset URL.
    sys.modules["generate"] = sys.modules["__main__"]
    build_assets()
    import pages
    pages.main()
