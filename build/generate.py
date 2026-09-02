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
         "logo": "/assets/logo.svg"}

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
# The castle, centred above the name. Source in build/brand/castle.svg.
#
# It is DRAWN, not cut out of the supplied artwork. The supplied file is a
# raster of a generated illustration: its outlines wobble, its flag is a smudge,
# and it was exported on black, so every cut left either a dark fringe or a
# chewed edge. Three passes of feathering, colour bleeding and contour smoothing
# each improved it and none of them fixed it, because the ruggedness is in the
# linework itself and no raster pass can straighten a line that was drawn
# crooked.
#
# The redraw keeps the artwork's shapes and its exact three colours, so it is
# the same mark, and being vector it is sharp at 32px and at 3000px, tints from
# the palette, and weighs about 1KB.
#
# The castle is 1.51:1, so it is sized by WIDTH and the height follows.
def logo_mark():
    return (f'<img class="mark" src="{ASSET["logo"]}" alt="" width="512" '
            f'height="340" decoding="async">')


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
    # ratio=None leaves the aspect ratio to the stylesheet. An inline style beats
    # a media query, so anything that has to reshape at a breakpoint (the
    # masthead photo does) must not carry its ratio inline.
    r = f' style="--ratio:{ratio}"' if ratio else ""
    if src == D.SOON:
        return (f'<span class="pic pic-panel"{r} role="img" '
                f'aria-label="{esc(alt)}">{t}<span class="panel-name">{esc(alt)}</span></span>')
    load = "eager" if eager else "lazy"
    return (f'<span class="pic"{r}>{t}'
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
     All six now work as both fill and text, so --c and --ct match on every
     row. The pair is kept because the moment a light colour is added back the
     two diverge again, as amber did. */
  --c-castle:#0056db;      /* THE LOGO BLUE, sampled from the artwork  white 6.26:1 */
  --c-combi:#6d28d9;       /* violet                                   white 7.10:1 */
  --c-obstacle:#047857;    /* emerald                                  white 5.48:1 */
  --c-disco:#c81e6a;       /* pink                                     white 5.45:1 */
  --c-sumo:#c2410c;        /* orange                                   white 5.18:1 */
  --c-marquee:#0e7490;     /* teal                                     white 5.36:1 */

  /* THE LOGO YELLOW, sampled from the artwork. Every call to action is this
     yellow with ink on it, on every page, so "the thing you press" is
     learnable at a glance. No category uses it, so it never collides.
     A yellow fill is only 1.53:1 against the page, so every yellow button
     carries a 2px ink border, which also echoes the heavy outline the artwork
     is drawn with.
     --accent-text is the same yellow taken down to a tone that works as small
     TEXT on a light ground, which the yellow itself cannot. */
  --accent:#fec521;
  --accent-text:#8a6100;
  --accent-deep:#d9a200;

  /* Ink is the navy the artwork is outlined in, not a neutral black. */
  --ink:#0b1a2e;
  --ink-70:#48566b;
  --ink-45:#54637b;
  --paper:#f8fbff;
  --paper-2:#eaf1fd;
  /* Light surfaces. Navy is not used for anything larger than a line of text
     except the contact band; the rail, the masthead and the footer are light,
     and the weight comes from the logo blue and yellow. */
  --sky:#dbe9ff;
  --sky-line:#bcd4f8;
  --rail-bg:#ffffff;
  --rail-line:#dde8f8;
  --rail-hover:#eaf1fd;
  --line:#d8e5f7;
  --line-strong:#b9cdeb;

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
[data-cat="sumo"]{--c:var(--c-sumo);--ct:var(--c-sumo);--on-c:#fff}
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
/* The castle is centred over the name, and the lockup is centred in the rail. */
.rail .brand{flex-direction:column;align-items:center;gap:10px;width:100%}
.rail .wordmark{text-align:center}
.rail .mark{width:150px}
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
/* Marquees, one line under the CTA. Adam's point was that the marquee side is
   invisible, and the rail is the one element on every page. It is NOT a second
   button: the rule is one call to action per screen, in the logo yellow, and a
   second filled button beside it would make the page ask twice and answer
   neither. This is a link in the marquee colour that reads as a signpost. */
.rail-marq{display:flex;align-items:center;justify-content:center;gap:8px;
  margin-top:10px;padding:11px 14px;border-radius:var(--r-pill);
  border:2px solid var(--c-marquee);color:var(--c-marquee);
  font-family:var(--display);font-weight:600;font-size:15px;text-align:center;
  transition:background .15s,color .15s}
.rail-marq:hover{background:var(--c-marquee);color:#fff}
.rail-marq::after{content:"";width:8px;height:8px;flex:none;
  border-right:2.5px solid currentColor;border-top:2.5px solid currentColor;
  transform:rotate(45deg)}
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
  /* width:auto matters. The desktop rail centres the lockup with width:100% on
     .brand; going back to a row here without unsetting that left the brand
     filling the whole bar and pushing the burger 32px past the edge. Because
     the rail sets overflow-y:auto, and CSS resolves the other axis to auto
     along with it, that overflow became a horizontal scroll INSIDE the rail: it
     opened scrolled 32px to the right and the drawer's first characters were
     cut off ("HAT WE HIRE", "ORE"). */
  .rail .brand{flex-direction:row;align-items:center;gap:11px;width:auto}
  .rail .mark{width:96px}
  .rail .wordmark{font-size:17.5px}
  .burger{display:block}
  .rail-body{display:none;padding-top:16px}
  .rail.open .rail-body{display:block}
  .rail-sec{margin-top:18px}
  .rail-nav{gap:0}
}
/* At 320 the mark plus the full name plus the burger is still 42px wider than
   the bar. The name does not wrap and is not abbreviated, so the mark gives way
   instead. */
@media(max-width:380px){
  .rail .mark{width:66px}
  .rail .wordmark{font-size:15.5px}
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
  text-transform:uppercase;color:var(--accent-text);background:#fff2cc;
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
.btn-accent{background:var(--accent);color:var(--ink);border-color:var(--ink);
  box-shadow:0 4px 0 var(--ink)}
.btn-accent:hover{background:#ffd45a;box-shadow:0 6px 0 var(--ink)}
.btn-accent:active{box-shadow:0 2px 0 var(--ink)}
.btn-ink{background:var(--ink);color:#fff;box-shadow:0 4px 0 #000}
.btn-ink:hover{box-shadow:0 6px 0 #000}
.btn-line{background:#fff;color:var(--ink);border-color:var(--line-strong)}
.btn-line:hover{border-color:var(--ink)}
.btn-ghost{background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.22)}
.btn-ghost:hover{background:rgba(255,255,255,.18)}
.btn svg{width:17px;height:17px;flex:none}

/* -------------------------------------------------------------- masthead -- */
/* Not a centred hero. A wide colour block with the headline bottom-left and
   the photo bleeding off the right edge, then the facts sitting on the seam.

   The sky block is DRAWN in the mark's language rather than decorated with
   gradients: bunting along the top, outlined clouds behind, and the seam cut as
   a wave with the same heavy ink line the castle is outlined in. All four
   pieces are flat fills with a 3 to 5px ink stroke, which is the one rule the
   mark follows, so the hero reads as the same hand.
   The bunting is the six category colours in order, so even the decoration is
   the palette doing its job.
   Art lives in build/brand/*.svg and is hashed into /assets/ like everything
   else. wave.svg carries --paper as a literal fill (#f8fbff): change --paper
   and the wave has to change with it. */
.mast{color:var(--ink);position:relative;overflow:hidden;
  padding:clamp(58px,5.4vw,84px) var(--gut) clamp(104px,8.4vw,140px);
  background:
    url("__ART_BUNTING__") repeat-x left -6px top -2px,
    url("__ART_WAVE__") repeat-x left bottom,
    var(--sky)}
/* Three columns above 1280: headline, date picker, photo. The picker is a fixed
   300px because a date grid has a floor below which it stops being tappable;
   the headline and the photo share what is left. */
/* Two columns: everything you read on the left, one big photo on the right.
   align-items:stretch, so the photo is as tall as the copy and the calendar
   together rather than floating at one end of it. */
/* Copy and the slideshow on the left, the date card on the right. The photo is
   a wide rectangle under the headline rather than a full height panel: a tall
   frame cropped every landscape photo we have down to a vertical strip. */
.mast-grid{display:grid;grid-template-columns:minmax(0,1.28fr) minmax(280px,.72fr);
  gap:clamp(24px,3vw,52px);align-items:center;position:relative;z-index:2}
.mast-left{display:flex;flex-direction:column;
  gap:clamp(24px,2.6vw,34px);min-width:0}
/* The masthead headline is capped below the global display size: the left
   column is narrow because the rail takes 266px, and the hard rule is that
   the headline never runs past two lines on desktop. */
/* Smaller than it was at two columns. Three columns leave the headline about
   370px at 1440, and the hard rule is still that it never runs past two lines. */
/* No ch cap in the three column hero: the column itself is the measure, and a
   14ch cap was forcing a third line the column had room to avoid. */
.mast h1{font-size:clamp(31px,2.4vw + 8px,46px);max-width:17ch;text-wrap:balance}
.mast h1 em{font-style:normal;color:var(--c-castle)}
.mast p{margin-top:18px;font-size:var(--step-1);color:var(--ink-70);max-width:46ch;
  font-weight:500}
.mast-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.mast-shot{position:relative;min-width:0}
.shot-frame{position:relative}
/* Portrait in the three column hero. Beside a date card that is naturally tall,
   a landscape photo left a lot of empty sky above it and read as an
   afterthought. */
/* Straight. The frame and the caption were both tilted, the calendar sat at a
   third angle between them, and the hero read as clutter rather than as three
   things doing three jobs. Nothing in the hero is rotated now. */
.mast-shot .pic{border:3px solid var(--ink);box-shadow:12px 12px 0 var(--c-castle);
  background:var(--paper-2);aspect-ratio:16/10}
/* Set here, not inline on the element, so the stacked breakpoint can reshape it. */
.mast-tag{position:absolute;left:-10px;bottom:-14px;background:var(--accent);color:var(--ink);
  padding:10px 18px;border-radius:var(--r-pill);font-family:var(--display);font-weight:600;
  font-size:14.5px}
/* Clouds, drawn and outlined rather than blurred blobs. Held back to .55 so
   they sit behind the headline instead of competing with it, and hidden on
   narrow screens where there is no room to be scenery. */
/* No cloud. It was tried and cut: everywhere it fit it sat half behind the
   photo frame and read as a smudge, and the hero already carries bunting, a
   tilted frame and the straddling cards. build/brand/cloud.svg is kept for a
   section that has room for it. */
/* The rail keeps 266px, so between 1100 and 1360 the masthead's left column
   is too narrow to hold the headline to two lines. Stack it instead. */
/* Stacked, the TEXT leads. The photo used to be ordered above it, which put a
   448px tall image between the top bar and the h1 and pushed the headline and
   both buttons below the fold on every phone and small laptop. Below the text
   it also gets to be wider and shallower, which suits a single column. */
/* Below 1280 there is not room for three. The picker goes under the buttons
   beside the photo, which keeps it above the fold, and below 1000 everything
   stacks with the text leading. */
/* Below 980 the two columns stack: copy, then the calendar, then the photo,
   which is the same reading order the desktop layout has. */
@media(max-width:980px){
  .mast-grid{grid-template-columns:1fr;gap:clamp(24px,4vw,34px)}
  .mast-left{gap:26px}
  .dpick{max-width:380px}
  .mast-shot{max-width:640px}
  .mast-shot .pic{aspect-ratio:4/3}}

/* Facts sit across the seam between the masthead and the page. */
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;
  margin:-38px var(--gut) 0;position:relative;z-index:3}
.facts div{background:#fff;border:2px solid var(--line);border-radius:var(--r);
  padding:20px 22px;box-shadow:0 8px 0 -2px rgba(20,19,16,.07)}
.facts div:nth-child(1){--fc:var(--c-castle)}
.facts div:nth-child(2){--fc:var(--c-obstacle)}
.facts div:nth-child(3){--fc:var(--c-disco)}
.facts b{display:block;font-family:var(--display);font-weight:600;font-size:var(--step-2);
  color:var(--fc);line-height:1.1;margin-bottom:2px}
.facts span{color:var(--ink-70);font-size:14.5px;font-weight:500}
@media(max-width:760px){.facts{grid-template-columns:1fr;margin-top:-26px}}

/* --------------------------------------------------------- hero slides --- */
.slides{position:relative}
/* 42%: the frame is 16/10 and the photos are 4/3, so there is a little vertical
   overflow and the ground is the half worth losing. */
.slides .slide{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  object-position:center 42%;opacity:0;transition:opacity .7s ease}
.slides .slide.on{opacity:1}
/* No JS: the first slide is already .on and already loaded, so the hero shows a
   photo whatever happens to the script. */
/* Chunky, always on, same round-and-outlined language as the buttons. */
.slide-arrow{display:none;position:absolute;top:50%;margin-top:-24px;z-index:3;
  width:48px;height:48px;border-radius:50%;background:#fff;border:3px solid var(--ink);
  cursor:pointer;padding:0;box-shadow:0 3px 0 var(--ink);
  transition:background .14s,transform .12s,box-shadow .12s}
.js .slide-arrow{display:grid;place-items:center}
.slide-arrow:hover{background:var(--accent)}
.slide-arrow:active{transform:translateY(3px);box-shadow:0 0 0 var(--ink)}
.slide-arrow::before{content:"";width:12px;height:12px;
  border-top:3px solid var(--ink);border-right:3px solid var(--ink)}
.slide-arrow.prev{left:14px}
.slide-arrow.prev::before{transform:rotate(-135deg);margin-left:4px}
.slide-arrow.next{right:14px}
.slide-arrow.next::before{transform:rotate(45deg);margin-right:4px}
@media(max-width:480px){.slide-arrow{width:40px;height:40px;margin-top:-20px}
  .slide-arrow.prev{left:8px}.slide-arrow.next{right:8px}}
.slide-dots{display:none;gap:7px;justify-content:center;margin-top:26px}
.js .slide-dots{display:flex}
.slide-dots .dot{width:9px;height:9px;padding:0;border-radius:50%;cursor:pointer;
  border:2px solid var(--ink);background:transparent;transition:background .16s}
.slide-dots .dot.on{background:var(--ink)}
@media(prefers-reduced-motion:reduce){.slides .slide{transition:none}}

/* ---------------------------------------------------------- date pick --- */
/* Sits between the headline and the photo in the hero. Same card language as
   everything else: white, 3px ink border, chunky offset shadow.
   Deliberately NOT an availability calendar. No day is ever shown as free or
   booked, because we have no booking data and inventing one would be a promise
   Adam has not made. It picks a date and carries it into the enquiry. */
.dpick{background:#fff;border:3px solid var(--ink);border-radius:var(--r);
  padding:18px 18px 16px;box-shadow:8px 8px 0 var(--accent);
  width:100%;align-self:center}
.dp-label{display:block;font-size:11px;font-weight:800;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink-45);margin-bottom:12px}
.dp-head{display:flex;align-items:center;justify-content:space-between;gap:6px;
  margin-bottom:10px}
.dp-month{font-family:var(--display);font-weight:600;font-size:16.5px;
  text-align:center;flex:1;min-width:0}
.dp-nav{width:30px;height:30px;flex:none;border:2px solid var(--line-strong);
  border-radius:50%;background:#fff;cursor:pointer;font-size:17px;line-height:1;
  color:var(--ink);transition:background .14s,border-color .14s}
.dp-nav:hover:not(:disabled){background:var(--accent);border-color:var(--ink)}
.dp-nav:disabled{opacity:.32;cursor:not-allowed}
.dp-dow,.dp-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}
.dp-dow{margin-bottom:4px}
.dp-dow span{text-align:center;font-size:11px;font-weight:800;color:var(--ink-45)}
.dp-grid{display:none}
.js .dp-grid{display:grid}
.dp-grid button{aspect-ratio:1;border:0;background:none;border-radius:8px;
  font-size:13.5px;font-weight:600;color:var(--ink);cursor:pointer;padding:0;
  transition:background .12s,color .12s}
.dp-grid button:hover:not(:disabled){background:var(--paper-2)}
/* Past dates. WCAG exempts disabled controls from contrast, but a date grid is
   read as a whole: you find next Saturday by scanning past the days that are
   gone. #b9cdeb measured 1.62:1 and was effectively invisible. #64748b is
   4.76:1, still obviously muted against the ink of a live day. */
.dp-grid button:disabled{color:#64748b;opacity:.75;cursor:default}
.dp-grid button.today{box-shadow:inset 0 0 0 2px var(--line-strong)}
.dp-grid button.on{background:var(--c-castle);color:#fff}
.dp-grid span{aspect-ratio:1}
/* No JS: a native date input does the same job. */
.dp-fallback{display:block;font-size:13px;font-weight:700;color:var(--ink-70)}
.dp-fallback input{width:100%;margin-top:6px;padding:11px 12px;
  border:2px solid var(--line-strong);border-radius:var(--r-sm);font-size:15px}
.js .dp-fallback{display:none}
.dp-go{width:100%;margin-top:14px}
/* .mast p sets step-1 on everything in the hero, and this lives in the hero, so
   it has to out-specify that or the note renders at headline-adjacent size. */
.mast .dp-note,.dp-note{margin-top:10px;font-size:12.5px;line-height:1.45;
  color:var(--ink-45);font-weight:500;max-width:none}

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
  background:var(--accent);color:var(--ink);border-color:var(--ink)}
.bento li:nth-child(1) p{color:#4a3608;font-size:var(--step-1)}
.bento li:nth-child(1) .n{width:52px;height:52px;font-size:19px}
.bento li:nth-child(6n+1){--wc:var(--c-castle)}
.bento li:nth-child(6n+2){--wc:var(--c-castle)}
.bento li:nth-child(6n+3){--wc:var(--c-obstacle)}
.bento li:nth-child(6n+4){--wc:var(--c-combi)}
.bento li:nth-child(6n+5){--wc:var(--c-disco)}
.bento li:nth-child(6n+6){--wc:var(--c-marquee)}
.bento .n{width:38px;height:38px;border-radius:50%;background:var(--wc);color:#fff;
  display:grid;place-items:center;font-family:var(--display);font-weight:600;font-size:15px;
  margin-bottom:14px}
.bento li:nth-child(1) .n{margin-bottom:0;background:var(--ink);color:var(--accent)}
.bento p{color:var(--ink-70);font-size:15px;margin-top:7px;font-weight:450}
@media(max-width:1000px){.bento{grid-template-columns:repeat(4,1fr)}
  .bento li,.bento li:nth-child(5){grid-column:span 2}
  .bento li:nth-child(1),.bento li:nth-child(6){grid-column:span 4}}
@media(max-width:620px){.bento{grid-template-columns:1fr}
  .bento li,.bento li:nth-child(1){grid-column:span 1}
  .bento li:nth-child(1){grid-template-columns:1fr}}

/* --------------------------------------------------------------- areas --- */
/* Full-bleed colour band. Towns as big type, checker sitting inside it. */
.areas-band{background:var(--c-castle);color:#fff;position:relative;overflow:hidden}
.areas-band::after{content:"";position:absolute;width:300px;height:300px;border-radius:50%;
  right:-110px;bottom:-140px;background:#fff;opacity:.08}
.areas-band .sec-head p{color:#dbe7fb}
.town-list{display:flex;flex-wrap:wrap;gap:10px;position:relative;z-index:1}
.town-list a{display:block;padding:12px 22px;border-radius:var(--r-pill);
  border:2px solid rgba(255,255,255,.34);font-family:var(--display);font-weight:600;
  font-size:19px;transition:background .15s,transform .15s,border-color .15s}
.town-list a:hover{background:#fff;color:var(--c-castle);border-color:#fff;
  transform:translateY(-3px)}
.checker{margin-top:30px;background:rgba(255,255,255,.12);border-radius:var(--r);
  padding:24px 26px;position:relative;z-index:1;max-width:640px}
.checker h3{margin-bottom:12px}
.checker-row{display:flex;gap:10px;flex-wrap:wrap}
.checker select{flex:1;min-width:170px;padding:13px 15px;border:2px solid transparent;
  border-radius:var(--r-sm);background:#fff;color:var(--ink);font-size:15px}
.checker select:focus{outline:3px solid var(--accent);outline-offset:1px}
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
.rev .stars{color:var(--accent-text);font-size:14px;letter-spacing:3px;margin-bottom:12px}
.rev p{font-family:var(--display);font-weight:500;font-size:var(--step-1);line-height:1.35}
.rev .who{margin-top:16px;padding-top:14px;border-top:2px solid var(--line);
  font-size:14px;font-weight:700;color:var(--rc)}
@media(max-width:900px){.revs{grid-template-columns:1fr}
  .rev,.rev:nth-child(1),.rev:nth-child(3){margin-top:0}}

/* ----------------------------------------------------------------- faq --- */
.faq{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}
.faq-item{background:#fff;border:2px solid var(--line);border-radius:var(--r);
  transition:border-color .16s}
.faq-item.open{border-color:var(--ink)}
.faq-q{width:100%;background:none;border:0;text-align:left;cursor:pointer;
  padding:20px 54px 20px 22px;font-family:var(--display);font-weight:600;
  font-size:var(--step-1);position:relative;line-height:1.25}
.faq-q::after{content:"";position:absolute;right:18px;top:50%;width:26px;height:26px;
  margin-top:-13px;border-radius:50%;background:var(--paper-2);transition:background .2s}
.faq-q::before{content:"";position:absolute;right:24px;top:50%;width:14px;height:14px;
  margin-top:-7px;z-index:1;background:var(--ink);transition:transform .25s,background .2s;
  clip-path:polygon(43% 0,57% 0,57% 43%,100% 43%,100% 57%,57% 57%,57% 100%,43% 100%,43% 57%,0 57%,0 43%,43% 43%)}
.faq-item.open .faq-q::after{background:var(--accent)}
.faq-item.open .faq-q::before{transform:rotate(135deg);background:var(--ink)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .3s ease}
.faq-a p{padding:0 22px 20px;color:var(--ink-70);font-weight:450}
@media(max-width:820px){.faq{grid-template-columns:1fr}}

/* ------------------------------------------------------------- marquee --- */
/* Adam, 27 Aug: "Our marquee hire side of the business is being lost with the
   current website." One card in one shelf was never going to fix that, so
   marquees get their own block on the home page and at the top of their
   category page.

   Its own layout family, not a reuse: a single bordered panel with a solid
   colour header strip and the fit-out running as a row of tiles underneath.
   The areas band is full-bleed colour with pills, the bento is six cells, the
   contact block is a split. This is none of those.

   No sizes are quoted anywhere in it. Adam has not given them, and the copy is
   written so it does not need them rather than guessing at a number. */
/* On the home page the block sits inside a full-bleed tinted band. Floating on
   the paper between the shelves and "How it works" it read as one more card in
   the flow, which is exactly the problem Adam was describing. The band changes
   the ground colour, so the page visibly stops doing castles and starts doing
   marquees. Rules top and bottom in the marquee colour rather than ink, so it
   reads as a section of this site and not a pasted in advert. */
.marq-band{background:#e8f4f7;border-top:4px solid var(--c-marquee);
  border-bottom:4px solid var(--c-marquee)}
.marq-band .marq{box-shadow:10px 10px 0 rgba(14,116,144,.28)}
.marq-eyebrow{display:inline-block;font-size:12.5px;font-weight:800;
  letter-spacing:.1em;text-transform:uppercase;color:var(--c-marquee);
  background:#fff;border-radius:var(--r-pill);padding:7px 15px;margin-bottom:14px}
.marq{border:3px solid var(--ink);border-radius:var(--r);overflow:hidden;
  background:#fff;box-shadow:10px 10px 0 var(--c-marquee)}
.marq-head{background:var(--c-marquee);color:#fff;padding:clamp(26px,3vw,40px);
  display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.82fr);
  gap:clamp(20px,3vw,42px);align-items:center}
.marq-head-text{min-width:0}
.marq-pic{display:block;border:3px solid var(--ink);border-radius:var(--r);
  overflow:hidden;aspect-ratio:4/3;background:rgba(255,255,255,.14)}
.marq-pic img{width:100%;height:100%;object-fit:cover;display:block}
@media(max-width:900px){.marq-head{grid-template-columns:1fr}
  .marq-pic{aspect-ratio:16/9}}
.marq-head h2{max-width:20ch}
/* #d6eef4 measured 4.44:1 on the teal, just under AA. #e0f3f8 is 4.68:1. */
.marq-head .lede{margin-top:14px;color:#e0f3f8;font-size:var(--step-1);
  font-weight:500;max-width:56ch}
.marq-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.marq-body{padding:clamp(24px,2.6vw,34px)}
.marq-label{font-size:11px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-45);margin-bottom:16px}
/* Names, not sales copy. Each item carried a line of description underneath and
   every one of those lines was invented: whether the floor is timber, whether
   the tables are set out before you arrive, what the lighting is. Adam gave us
   five words and those five words are the content. Set them large so the row
   still carries the block. */
.marq-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}
.marq-grid li{border:2px solid var(--line);border-radius:var(--r-sm);
  padding:22px 18px;min-width:0;font-family:var(--display);font-weight:600;
  font-size:var(--step-1);color:var(--c-marquee);text-align:center;
  overflow-wrap:break-word}
/* Furniture on its own is a real hire line, not a footnote to the marquee. */
.marq-also{margin-top:16px;border:2px dashed var(--line-strong);border-radius:var(--r-sm);
  padding:16px 20px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;
  font-weight:500;color:var(--ink-70);font-size:15.5px}
.marq-also a{font-weight:800;color:var(--c-marquee);text-decoration:underline;
  text-underline-offset:3px}
@media(max-width:1100px){.marq-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:640px){.marq-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .marq{box-shadow:6px 6px 0 var(--c-marquee)}}
@media(max-width:380px){.marq-grid{grid-template-columns:1fr}}

/* Signpost. A one line cross link to marquees from every page where marquees
   are not the subject: the other five category pages, the 22 other unit pages
   and all 9 town pages. Adam's whole point was that the marquee side of the
   business is invisible, and a block on two pages does not fix that if a
   customer lands on "bouncy castle hire clonmel" and never sees it.

   Kept to one line with a rule and an arrow rather than made into a card, so it
   signposts without competing with the page it is sitting on. The copy changes
   by context so it does not read as the same banner stamped everywhere. */
.signpost{display:flex;align-items:center;gap:18px;flex-wrap:wrap;
  border-top:3px solid var(--c-marquee);background:#fff;
  border-radius:0 0 var(--r) var(--r);padding:20px 24px;margin-top:34px;
  box-shadow:0 8px 0 -2px rgba(20,19,16,.06)}
.signpost .sp-l{font-size:11px;font-weight:800;letter-spacing:.14em;
  text-transform:uppercase;color:var(--c-marquee);flex:none}
.signpost p{flex:1;min-width:220px;font-weight:500;color:var(--ink-70);
  font-size:15.5px;margin:0}
.signpost a{flex:none;display:inline-flex;align-items:center;gap:9px;
  font-family:var(--display);font-weight:600;font-size:16px;color:var(--c-marquee);
  border-bottom:2px solid transparent;transition:border-color .15s}
.signpost a:hover{border-color:var(--c-marquee)}
.signpost a::after{content:"";width:9px;height:9px;border-right:2.5px solid currentColor;
  border-top:2.5px solid currentColor;transform:rotate(45deg);flex:none}
/* Narrow: the label goes on its own line. Left beside the copy it pinched
   the text into half the width and ran it to seven lines. */
@media(max-width:620px){.signpost{flex-direction:column;align-items:flex-start;gap:10px}
  .signpost p{min-width:0}}

/* ------------------------------------------------------------- notices --- */
.note{background:#fff6db;border:2px solid #f2e2ac;border-radius:var(--r);padding:20px 24px;
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

/* A unit's own photo strip, under its specs. Only the marquee has one so far. */
.ugal{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:26px}
.ugal .pic{--ratio:1/1;border:2px solid var(--line)}
@media(max-width:620px){.ugal{grid-template-columns:repeat(2,1fr)}}

/* ------------------------------------------------------------- gallery --- */
.gallery{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.gallery .pic{--ratio:1/1}
.gallery a:nth-child(6n+1){grid-column:span 2}
.gallery a:nth-child(6n+1) .pic{--ratio:2/1}
@media(max-width:860px){.gallery{grid-template-columns:repeat(2,1fr)}}

/* ------------------------------------------------------------- contact --- */
.contact{background:var(--ink);color:#fff;position:relative;overflow:hidden}
.contact::after{content:"";position:absolute;width:320px;height:320px;border-radius:50%;
  left:-130px;bottom:-160px;background:#fff;opacity:.08}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,3.5vw,58px);
  align-items:start;position:relative;z-index:1}
.contact h2{max-width:15ch}
.contact .lede{color:#c8d6ea;margin-top:16px}
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
.fld input:focus,.fld textarea:focus{outline:3px solid var(--c-castle);outline-offset:1px;
  border-color:var(--c-castle)}
.fld textarea{resize:vertical;min-height:84px}
form .btn{width:100%;margin-top:6px}
/* Draft state: the form is not wired to Formspree yet. */
form .btn[disabled]{opacity:.5;cursor:not-allowed;box-shadow:0 2px 0 var(--ink)}
.form-note{margin-top:12px;font-size:14px;font-weight:500;color:var(--ink-70);
  background:#fff6db;border:2px solid #f2e2ac;border-radius:var(--r-sm);
  padding:12px 14px}
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
.socials a:hover{background:var(--accent);border-color:var(--ink);color:var(--ink);
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
.actionbar .ab-call{background:var(--accent);color:var(--ink);border:2px solid var(--ink)}
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
:focus-visible{outline:3px solid var(--c-castle);outline-offset:2px;border-radius:4px}

.skip{position:absolute;left:-9999px;top:0;background:var(--ink);color:#fff;
  padding:12px 18px;z-index:100}
.skip:focus{left:0}
::selection{background:var(--accent);color:var(--ink)}
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
/* HERO SLIDESHOW. Crossfade, pause on hover, stop entirely for anyone who has
   asked for reduced motion. The first slide is already visible from the markup,
   so none of this is load bearing. */
const slidesEl = document.getElementById('heroSlides');
if (slidesEl) {
  const slides = [...slidesEl.querySelectorAll('.slide')];
  const dots = [...document.querySelectorAll('#heroDots .dot')];
  const cap = document.querySelector('.mast-tag');
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let i = 0, timer = null;

  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('on', k === i));
    dots.forEach((d, k) => d.classList.toggle('on', k === i));
    if (cap) cap.textContent = slides[i].dataset.cap;
  }
  function start() { if (!still && !timer) timer = setInterval(() => show(i + 1), 5000); }
  function stop() { clearInterval(timer); timer = null; }

  dots.forEach((d, k) => d.addEventListener('click', () => { show(k); stop(); }));
  /* Clicking an arrow means the visitor is driving. Stop the timer so it does
     not move the photo out from under them a second later. */
  const prev = document.getElementById('heroPrev');
  const next = document.getElementById('heroNext');
  if (prev) prev.addEventListener('click', () => { show(i - 1); stop(); });
  if (next) next.addEventListener('click', () => { show(i + 1); stop(); });
  slidesEl.addEventListener('mouseenter', stop);
  slidesEl.addEventListener('mouseleave', start);
  /* Nothing animates while the hero is off screen. */
  new IntersectionObserver(es => es[0].isIntersecting ? start() : stop(),
                           { threshold: 0.2 }).observe(slidesEl);
}

/* DATE PICKER (hero) and the date it hands to the contact form.
   Not an availability calendar: no day is ever marked free or booked, because
   there is no booking data behind this site. It picks a date, puts it in the
   link to the contact page, and the contact page fills the field. */
const dpGrid = document.getElementById('dpGrid');
if (dpGrid) {
  const MONTHS = ['January','February','March','April','May','June','July',
                  'August','September','October','November','December'];
  const monthEl = document.getElementById('dpMonth');
  const goEl = document.getElementById('dpGo');
  const prevEl = document.getElementById('dpPrev');
  const nextEl = document.getElementById('dpNext');
  const today = new Date(); today.setHours(0, 0, 0, 0);
  let view = new Date(today.getFullYear(), today.getMonth(), 1);
  let picked = null;

  const iso = d => d.getFullYear() + '-' +
    String(d.getMonth() + 1).padStart(2, '0') + '-' +
    String(d.getDate()).padStart(2, '0');

  function render() {
    monthEl.textContent = MONTHS[view.getMonth()] + ' ' + view.getFullYear();
    prevEl.disabled = view.getFullYear() === today.getFullYear() &&
                      view.getMonth() === today.getMonth();
    dpGrid.textContent = '';
    /* Monday first: getDay() is 0 for Sunday, so shift it. */
    const lead = (new Date(view.getFullYear(), view.getMonth(), 1).getDay() + 6) % 7;
    for (let i = 0; i < lead; i++) dpGrid.appendChild(document.createElement('span'));
    const days = new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate();
    for (let d = 1; d <= days; d++) {
      const date = new Date(view.getFullYear(), view.getMonth(), d);
      const b = document.createElement('button');
      b.type = 'button'; b.textContent = d;
      if (date < today) { b.disabled = true; }
      if (date.getTime() === today.getTime()) b.classList.add('today');
      if (picked && date.getTime() === picked.getTime()) {
        b.classList.add('on'); b.setAttribute('aria-pressed', 'true');
      }
      b.addEventListener('click', () => { picked = date; render(); });
      dpGrid.appendChild(b);
    }
    goEl.href = picked ? '/contact/?d=' + iso(picked) : '/contact/';
    goEl.textContent = picked
      ? 'Get a price for ' + picked.getDate() + ' ' + MONTHS[picked.getMonth()].slice(0, 3)
      : 'Get a price';
  }
  prevEl.addEventListener('click', () => {
    view = new Date(view.getFullYear(), view.getMonth() - 1, 1); render();
  });
  nextEl.addEventListener('click', () => {
    view = new Date(view.getFullYear(), view.getMonth() + 1, 1); render();
  });
  render();
}

/* The contact form picks the date up out of the URL. */
const dField = document.getElementById('d');
if (dField) {
  const q = new URLSearchParams(location.search).get('d');
  if (q && /^\d{4}-\d{2}-\d{2}$/.test(q)) {
    dField.value = q;
    dField.closest('form').scrollIntoView({ block: 'center' });
  }
}

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
        if re.fullmatch(r"(styles|script|logo|bunting|wave|cloud)"
                        r"\.[0-9a-f]{8}\.(css|js|png|svg)", f):
            os.remove(os.path.join(adir, f))

    # Brand artwork. Hashed like the stylesheet because /assets/ is served
    # immutable for a year; the icons go to the root, which is not.
    bdir = os.path.join(HERE, "brand")

    def art(src, name):
        raw = io.open(os.path.join(bdir, src), "rb").read()
        h = hashlib.md5(raw).hexdigest()[:8]
        url = "/assets/%s.%s.svg" % (name, h)
        io.open(os.path.join(adir, "%s.%s.svg" % (name, h)), "wb").write(raw)
        return url

    ASSET["logo"] = art("castle.svg", "logo")
    for icon in ("favicon.png", "apple-touch-icon.png"):
        io.open(os.path.join(ROOT, icon), "wb").write(
            io.open(os.path.join(bdir, icon), "rb").read())

    # The masthead art is referenced from the stylesheet, so it has to be
    # substituted BEFORE the CSS is hashed or the hash will not track the art.
    css = CSS.strip() + "\n"
    for token, src, name in (("__ART_BUNTING__", "bunting.svg", "bunting"),
                             ("__ART_WAVE__", "wave.svg", "wave")):
        css = css.replace(token, art(src, name))
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
      <a href="/marquees/" class="rail-marq">We also do marquees</a>
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


def signpost(copy, label="Also from us", href="/marquees/", link="See marquee hire"):
    """One line pointing at marquees from a page that is about something else.

    Adam's complaint was that marquees are invisible on the old site. The
    spotlight block covers the home page and /marquees/; this covers everywhere
    else a customer actually lands, which for a local hire business is a town
    page or a single unit page far more often than the home page.
    """
    return (f'<div class="signpost"><span class="sp-l">{esc(label)}</span>'
            f'<p>{esc(copy)}</p><a href="{href}">{esc(link)}</a></div>')


def hero_slides():
    """The hero photo, as a slideshow.

    Eight usable images exist and one of them was carrying the whole hero, so
    the range read as thinner than it is. Six rotate here: a castle, a combi,
    two courses, the dome and a marquee, all inside the first screen. The
    marquee is in the set on purpose, since Adam said that side of the business
    was being lost.

    The first slide is eager and visible with no JS at all; the rest are lazy
    and only fade in if the script runs. A slideshow that needs JS to show its
    FIRST image is a blank box when the script fails.
    """
    out = []
    for i, (src, name, tag) in enumerate(D.HERO_SLIDES):
        cls = "slide on" if i == 0 else "slide"
        load = "eager" if i == 0 else "lazy"
        out.append(f'<img class="{cls}" src="{src}" alt="{esc(name)}" loading="{load}" '
                   f'data-cap="{esc(name)}, {esc(tag)}">')
    dots = "".join(
        f'<button type="button" class="dot{" on" if i == 0 else ""}" '
        f'aria-label="Photo {i + 1}"></button>' for i in range(len(D.HERO_SLIDES)))
    # The caption is anchored to the FRAME, not to .mast-shot. .mast-shot now
    # also contains the dots, so a tag pinned to its bottom edge sat on top of
    # them and they were invisible.
    # Arrows are real buttons sitting on the frame, always visible, not a hover
    # affordance. Half the people looking at this are on a phone, where hover
    # does not exist, and the other half are a client checking his own site.
    arrows = ('<button type="button" class="slide-arrow prev" id="heroPrev"'
              ' aria-label="Previous photo"></button>'
              '<button type="button" class="slide-arrow next" id="heroNext"'
              ' aria-label="Next photo"></button>')
    return (f'<div class="shot-frame">'
            f'<span class="pic slides" id="heroSlides">{"".join(out)}</span>'
            f'{arrows}'
            f'<span class="mast-tag">{esc(D.HERO_IMG_NAME)}, {esc(D.HERO_IMG_TAG)}</span>'
            f'</div>'
            f'<div class="slide-dots" id="heroDots">{dots}</div>')


def date_picker():
    """"Pick your date" in the hero. It carries the date into the enquiry.

    It is NOT an availability calendar and must never look like one. We have no
    booking data, so a grid showing free and booked days would be invented, and
    the deal is enquiry forms with no PartyOps behind them. What this does is
    remove a step: the customer picks the day here, lands on the contact form
    with it already filled, and the note says plainly that nothing is booked
    until Adam comes back to them.

    The grid is JS. Without JS the .js gate leaves a native date input in its
    place, which does the same job, and the button is a plain link either way.
    """
    return f"""
<div class="dpick">
  <span class="dp-label">Pick your date</span>
  <div class="dp-head">
    <button type="button" class="dp-nav" id="dpPrev" aria-label="Previous month">&#8249;</button>
    <span class="dp-month" id="dpMonth" aria-live="polite">&nbsp;</span>
    <button type="button" class="dp-nav" id="dpNext" aria-label="Next month">&#8250;</button>
  </div>
  <div class="dp-dow" aria-hidden="true"><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span><span>S</span></div>
  <div class="dp-grid" id="dpGrid"></div>
  <label class="dp-fallback">Date of your party
    <input type="date" id="dpInput"></label>
  <a href="/contact/" class="btn btn-accent dp-go" id="dpGo">Get a price</a>
  <p class="dp-note">We come straight back with a price. Nothing is booked until we talk.</p>
</div>
"""


def marquee_block(heading, lede, eyebrow=None, photo=None):
    """The marquee spotlight. Used on the home page and the marquee category page.

    Adam told us the marquee side of the business was being lost on the old
    site. This block is the answer to that: the fit-out spelled out, and the
    furniture-only hire given its own line rather than being buried in a
    sentence about marquees.
    """
    # Names only. Everything we had written under them was invented, so it went.
    tiles = "".join(f"<li>{esc(n)}</li>" for n in D.MARQUEE_EXTRAS)
    eb = f'<span class="marq-eyebrow">{esc(eyebrow)}</span>' if eyebrow else ""
    # A photo in the header. The block was tiles and type, which was all we had
    # before Adam's photos arrived; a marquee section with no marquee in it was
    # only ever a stopgap.
    pic = (f'<span class="marq-pic">'
           f'<img src="{photo}" alt="Marquee hire in Tipperary" loading="lazy">'
           f'</span>') if photo else ""
    return f"""
<div class="marq" data-cat="marquee">
  <div class="marq-head">
    <div class="marq-head-text">
      {eb}
      <h2>{heading}</h2>
      <p class="lede">{esc(lede)}</p>
      <div class="marq-actions">
        <a href="/contact/" class="btn btn-accent">Get a marquee price</a>
        <a href="tel:{D.PHONE_TEL}" class="btn btn-ghost">{ico("phone")}{D.PHONE_DISPLAY}</a>
      </div>
    </div>
    {pic}
  </div>
  <div class="marq-body">
    <div class="marq-label">Fit it out with</div>
    <ul class="marq-grid">{tiles}</ul>
    <div class="marq-also">
      <span>Only need the seating?</span>
      <a href="/hire/tables-and-chairs/">We hire tables and chairs on their own</a>
    </div>
  </div>
</div>
"""


def safety_box():
    lis = "".join(f"<li>{esc(s)}</li>" for s in D.SAFETY)
    return f'<div class="safety"><h3>Safety and insurance</h3><ul>{lis}</ul></div>'


def contact_block():
    """The contact block. The form is LIVE only when FORMSPREE has a real ID.

    Until then it shipped pointing at "https://formspree.io/f/[FORM-ID]", so a
    real enquiry would have gone nowhere silently. On a draft the client is very
    likely to test the form, and a form that swallows an enquiry is worse than a
    form that says it is not connected yet. The fields stay so the layout can be
    judged; the submit is disabled and a line says why. Set FORMSPREE in data.py
    and the whole thing turns itself back on.
    """
    live = D.FORMSPREE and "[" not in D.FORMSPREE
    form_open = (f'<form action="{D.FORMSPREE}" method="POST">' if live else
                 '<form class="form-draft" onsubmit="return false">')
    submit = ('<button type="submit" class="btn btn-accent">Send enquiry</button>'
              if live else
              '<button type="submit" class="btn btn-accent" disabled>Send enquiry</button>'
              '<p class="form-note">Not connected yet.</p>')
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
      {form_open}
        <div class="fld"><label for="n">Your name</label><input id="n" name="name" type="text" required></div>
        <div class="fld"><label for="p">Phone</label><input id="p" name="phone" type="tel" required></div>
        <div class="fld"><label for="t">Your town</label><input id="t" name="town" type="text"></div>
        <div class="fld"><label for="d">Date of event</label><input id="d" name="date" type="date"></div>
        <div class="fld"><label for="m">What are you after?</label><textarea id="m" name="message" rows="3"></textarea></div>
        {submit}
      </form>
    </div>
</section>
"""


def footer():
    ranges = "".join(f'<a href="/{c["slug"]}/">{c["title"]}</a>' for c in D.CATEGORIES)
    areas = "".join(f'<a href="/{a["slug"]}/">{a["town"]}</a>' for a in D.AREAS[:6])
    # The Facebook icon is only rendered when there IS a Facebook URL. It used
    # to ship as href="[FACEBOOK-URL]", a dead link in the footer of all 45
    # pages. A placeholder is not worth a broken link on every page.
    fb = ("" if not D.FACEBOOK or D.FACEBOOK.startswith("[") else
          f'<a href="{D.FACEBOOK}" target="_blank" rel="noopener" '
          f'aria-label="Facebook">{FB_SVG}</a>')
    wa = wa_link()
    return f"""</main>
<footer>
  <div class="foot-top">
    <div>
      {logo()}
      <p>Bouncy castle, obstacle course, disco dome and marquee hire across Tipperary. Family run since {D.FOUNDED}, fully insured and certified with the Irish Inflatable Hirers Federation.</p>
      <div class="socials">
        {fb}
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
