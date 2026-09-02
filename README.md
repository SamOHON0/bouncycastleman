# Bouncy Castle Man

Static site for Bouncy Castle Man (bouncycastleman.com), Tipperary.
`build/data.py` holds the content, `build/generate.py` holds the design and the
shared fragments, `build/pages.py` builds the pages.

Client contact: Adam Garrett, 086 194 5789, adamgarrett@rocketmail.com.
Deal: €449 build + €39/mo retainer, enquiry forms, no PartyOps.

## Build

```bash
cd build
python3 generate.py
```

No npm, no dependencies, Python 3 only. Safe to re-run, it only overwrites
files it generates. Writes 45 pages plus `assets/`, `sitemap.xml`,
`robots.txt` and `vercel.json` to the repo root.

Preview locally with `python3 -m http.server 8000`.

## Deploy

Push to GitHub and point Vercel at the repo root. No framework, no build
command, output directory is the root. `vercel.json` carries
`trailingSlash: true`, the old site's URL redirects and a one year immutable
cache on `/assets/`.

## Design

Rebuilt 20 Aug 2026. The cartoon "Bounce Land" house style is gone.

### Layout

A **persistent left rail** rather than a top nav, on a light cream ground. It
carries the mark, the six categories with their colour dots, the secondary
pages, the phone number and the one CTA, and it stays put while the content
column scrolls. Below 1100px it
becomes a top bar with a drawer, and a **sticky action bar** pins Call and
WhatsApp to the bottom of the screen, which is what a parent on a phone
actually wants.

The **range is six horizontal shelves**, one per category, replacing the old
tile grid plus filtered card grid. You walk sideways through the category you
want, or open it for the full set. The arrows are an enhancement: the track
scrolls by touch, wheel and keyboard on its own, and the arrows are hidden
below 640px where swiping is the natural gesture.

The masthead is a soft sky-blue block with the headline bottom-left and the
photo tilted and bleeding off the right edge, with the three fact cards
straddling the seam below it. The block is **drawn in the mark's language**
rather than decorated: bunting along the top in the six category colours in
order, and the seam cut as a wave carrying the same heavy ink line the castle is
outlined in. Both are flat fills with a 3 to 3.5px ink stroke, which is the one
rule the mark follows, so the hero reads as the same hand that drew the logo.
Art in `build/brand/bunting.svg` and `wave.svg`, hashed into `/assets/` like
everything else. `wave.svg` carries `--paper` as a literal `#f8fbff`: change
`--paper` and the wave has to change with it.

A cloud was drawn and cut. Everywhere it fit it sat half behind the photo frame
and read as a smudge, and the hero already carries bunting, a tilted frame and
the straddling cards. `build/brand/cloud.svg` is kept for a section with room
for it.

Stacked, below 1360px, the **text leads**. The photo used to be ordered above it,
which put a 448px tall image between the top bar and the h1 and pushed the
headline and both buttons below the fold on every phone and small laptop. Below
the text it is also wider and shallower, which suits one column. It reshapes at
that breakpoint, so its ratio comes from the stylesheet: `shot()` takes
`ratio=None` to omit the inline style, because an inline style beats a media
query.

Then: a dotted timeline for how it works, a six-cell bento
for why us, a full-bleed teal band with towns as pills and the area checker
inside it, staggered quote cards, a two-column FAQ, and a split contact block.
Every section is a different layout family and none repeats.

### Photos

**`/images/marquees/` holds the only real, local images on this site.** Nine
marquee photos from Adam, 2 Sep 2026. Everything else still hotlinks
`files.secure.website`, the old host, and **dies at the DNS cutover**. These do
not.

They arrived as 2.8MB of phone JPEG with names like
`WhatsApp Image 2026-09-02 at 12.27.33 (4).jpeg`, dropped into `/marquees/`,
which is a generated page directory. They are resized to a 1200px long edge at
q74, progressive, EXIF-rotated, and renamed for what they actually show: 1.7MB
for the nine, no visible loss, and a filename you can reason about. 1200 is 2x
for the largest place any of them is displayed.

Where they go, and why each one:

| Photo | Used for |
|---|---|
| `marquee-tables-chairs` (interior, laid out) | the home page marquee block, and the tables and chairs unit. It is the one photo that shows "furnished" rather than describing it |
| `marquee-inside` (interior, empty) | the marquee block on `/marquees/` |
| `marquee-astro-sunny` (landscape, blue sky) | the hero slideshow's marquee slide |
| `marquee-pair-astro` (two marquees) | the `/marquees/` page banner |
| `marquee-long-grass` | the marquee unit's main photo |
| the other four | the marquee unit's own photo strip, and the gallery |

Unit pages render a `gallery=` tuple as a four-up strip under the specs
(`.ugal`). Only the marquee has one so far.

The gallery page leads with all nine, then the old host's leftovers.

### The date picker

"Pick your date" sits between the headline and the photo in the hero.
`date_picker()` in generate.py, grid rendered by the JS block.

**It is not an availability calendar and must never look like one.** No day is
ever shown as free or booked, because there is no booking data behind this site
and the deal is enquiry forms with no PartyOps. What it does is remove a step:
the customer picks a day, lands on `/contact/?d=YYYY-MM-DD` with the date field
already filled, and the note under it says plainly that nothing is booked until
Adam comes back to them.

Past dates are `#64748b` at 4.76:1, not `--line-strong` at 1.62:1. WCAG exempts
disabled controls from contrast, but a date grid is read as a whole: you find
next Saturday by scanning past the days that are gone, and at 1.62:1 they were
effectively invisible.

Without JS the `.js` gate swaps the grid for a native date input, which does the
same job, and the button is a plain link to `/contact/` either way.

### The hero slideshow

Six of the eight usable photos rotate in the hero frame: a castle, a combi, two
courses, the dome and a marquee, all inside the first screen. One photo was
carrying the whole hero and the range read as thinner than it is. The marquee is
in the set on purpose, since Adam said that side of the business was being lost.

**Arrows are real always-visible buttons on the frame**, not a hover affordance:
half the audience is on a phone where hover does not exist, and the other half is
a client checking his own site. Clicking one stops the timer, because the visitor
is driving at that point and having the photo move a second later is worse than
no autoplay at all.

**The first slide is outdoors.** It used to be the Red Lizard, a good unit
photographed indoors on a gym floor under strip lights. Note for whoever changes
the order next: the marquee photos are the only images on this site anyone has
actually looked at. The rest are small hotlinks off the old host and unreachable
from the build environment, so we cannot tell which castle shots are outdoors. If
one of them is a good sunny castle photo it belongs first, ahead of the marquee,
because the headline above it says bouncy castles.

The first slide is **eager and already `.on` in the markup**, so the hero shows a
photo whether or not the script runs. A slideshow that needs JS to show its first
image is a blank box when the script fails. Crossfade pauses on hover, stops
entirely for `prefers-reduced-motion`, and does not run while the hero is off
screen.

The caption is anchored to `.shot-frame`, not to `.mast-shot`. `.mast-shot` also
contains the dots now, and a caption pinned to its bottom edge sat on top of them.

### Hero layout

**Two columns. Everything you read on the left, one big photo on the right.**
Copy, then the date card, in `.mast-left`; the slideshow fills the right column
top to bottom (`align-items:stretch`, `.pic{height:100%}`). Below 980 it stacks
in the same reading order: copy, calendar, photo.

**Nothing in the hero is rotated.** The photo frame was tilted 1.6deg and the
caption 3deg, the calendar sat square between them at a third angle, and the
whole thing read as clutter rather than three things doing three jobs. The
chunky offset shadows stay; they are the house style and they are not slanted.

There is **one "Get a price" in the hero, in the date card**. There used to be a
second one directly above it, two identical yellow buttons a hundred pixels
apart, which was half of why the hero felt busy. The rail keeps a permanent one
for anyone who does not want to pick a date first.

Slides use `object-position:center 35%`. The frame is tall and the photos are
landscape, so a centred crop spends its bottom third on grass and tarmac.

`.mast p` sets `--step-1` on everything in the hero, so anything small that lives
in there (the picker's note) has to out-specify it or it renders at
headline-adjacent size.

### Marquees

Adam, 27 Aug: *"Our marquee hire side of the business is being lost with the
current website."* One card in one shelf was never going to fix that, so
marquees carry a **spotlight block** on the home page and at the top of
`/marquees/`. `marquee_block()` in `generate.py`, content in `MARQUEE_EXTRAS`
in `data.py`.

It is its own layout family, not a reuse: a single bordered panel with a solid
colour header strip and the fit-out running as a row of tiles underneath. The
areas band is full-bleed colour with pills, the bento is six cells, the contact
block is a split. This is none of those.

**No marquee dimension is quoted anywhere.** Adam said "various sizes" and gave
none. The capacity that IS stated, 20 to 100 people, is sourced: it is their own
published figure from premiermarqueehire.com. Actual dimensions still need to
come from Adam; add them to `MARQUEE_EXTRAS` and the unit specs when they do.

**The marquee side has its own website.** `premiermarqueehire.com`, Thurles,
established 2010, same phone number, and it calls bouncycastleman.com "Our Main
Website" while the old marquee page links out to it. That is a large part of why
the marquee side is "being lost": it lives on a different domain. It also
carries two things not on this site at all: **mobile bars**, and a wider service
area for marquees (Tipperary, Limerick, Kilkenny, Laois) than for castles. Worth
asking Adam whether to fold it in and redirect the domain.

`MARQUEE_EXTRAS` is **names only**: Flooring, Tables, Chairs, Lighting,
Heating. Those five are Adam's own words and are confirmed twice over (his
email, and premiermarqueehire.com's "Marquees, Tables, Chairs, Flooring
Heating"). Each one used to carry a line of description underneath and every one
of those lines was ours: whether the floor is timber, whether the tables are set
out before you arrive, what the lighting actually is. None of it was sourced, so
it is gone. Add real detail here only when Adam gives it.

### Claims

**Nothing on this site states a fact Adam has not published somewhere.** Do not
add one. Sales copy invented for a client is how a site ends up promising
something the client does not do.

Sourced and safe to repeat:

| Claim | Source |
|---|---|
| Established 2001, family run, 20+ years | bouncycastleman.com |
| Fully insured, IIHF certified | bouncycastleman.com |
| Tipperary and surrounding areas | bouncycastleman.com |
| Rain covers | their own castle listings name them per unit, and 19 of 19 castles, combis and courses in `UNITS` carry a rain cover spec, so "every castle and course" holds |
| Based in Thurles | premiermarqueehire.com |
| Marquees for 20 to 100 people | premiermarqueehire.com |
| Flooring, tables, chairs, lighting, heating | Adam's email, and premiermarqueehire.com |
| Tables and chairs hired separately | Adam's email |
| Unit counts and sizes | their own catalogue |

Rewritten 28 Aug because they were ours, not theirs. Comparative claims about
competitors and claims about what sells best are the two kinds to watch for:

- "Tipperary's biggest selection" became "Twenty three units in the range", which
  is a count of their own catalogue rather than a claim about anyone else
- "the largest selection of obstacle courses in Tipperary" became "Ten obstacle
  courses in the range"
- combis being "the most popular thing we hire" became a description of the
  range: seven of them, 15ft to 19ft
- "the unit most people ring us for" became "the biggest combi in the range"
- "Clonmel is one of our busiest towns", "are all regular work for us here",
  "Communions and confirmations are the busiest dates here", "on our regular
  run", "a favourite with smaller children", "a regular at school sports days":
  all rewritten as description rather than as claims about their trade
- "Family run ever since, same phone number" and "The same family, the same phone
  number" lost the phone clause. Their site says nothing about the number

The unit count on the home page excludes the tables and chairs line (`HIRE_UNITS`
in pages.py). It is a hire line but it is not a unit, and counting it would put a
number on the page that does not match what a customer sees in the shelves.

On the home page the block sits inside a full-bleed tinted band with rules top
and bottom in the marquee colour, and an eyebrow reading "The other side of the
business". Floating on the paper between the shelves and "How it works" it read
as one more card in the flow, which is exactly the problem Adam was describing.
The band changes the ground colour, so the page visibly stops doing castles and
starts doing marquees.

The rail carries **"We also do marquees"** under the CTA, on all 45 pages. It is
deliberately NOT a second button: the rule is one call to action per screen, in
the logo yellow, and a second filled button beside it would make the page ask
twice and answer neither. It is an outlined link in the marquee colour, so it
reads as a signpost rather than as a competing ask.

A **signpost** carries marquees to the rest of the site: a one line cross link
on the other five category pages, the 22 other unit pages and all 9 town pages,
36 in total. `signpost()` in `generate.py`. A block on two pages does not fix
invisibility if a customer lands on "bouncy castle hire clonmel" and never sees
it, and for a local hire business a town page or a single unit page is where
they land far more often than the home page. It is one line with a rule and an
arrow rather than a card, so it signposts without competing with the page it
sits on, and the copy changes by context so it does not read as the same banner
stamped everywhere. Below 620px the label moves onto its own line, because
beside the copy it pinched the text to half width and ran it to seven lines.

Tables and chairs are a **separate hire line** with their own unit page at
`/hire/tables-and-chairs/`, because he hires them without a marquee and the old
site never said so. They live in the marquee category rather than becoming a
seventh one: same side of the business, and six categories is load bearing
across the rail, the shelves and the copy. Two knock-ons: the block carries an
explicit "only need the seating?" line so the furniture is not buried in a
sentence about marquees, and the marquee category gets its own "travels to"
sentence, since "All 2 of our marquees travel" would be counting the chairs as
a marquee.

### The mark

The castle, **centred above the name**. Source in `build/brand/castle.svg`,
about 1KB of paths. The generator copies it to `assets/logo.<hash>.svg` at build
time, hashed like the stylesheet because `/assets/` is served immutable for a
year. `favicon.png` (64) and `apple-touch-icon.png` (180) are rendered from
`build/brand/castle-square.svg` and go to the repo root, which carries no such
header.

It is **drawn, not cut out of the supplied artwork**. The supplied file is a
raster of a generated illustration: its outlines wobble, its flag is a smudge,
and it was exported on black, so every cut left either a dark fringe or a chewed
edge. Feathering the alpha, bleeding the artwork's own colour outward and
smoothing the contour at 3x each improved it and none of them fixed it, because
the ruggedness is in the linework itself and no raster pass straightens a line
that was drawn crooked. The redraw keeps the artwork's shapes and its exact
three colours, so it is the same mark, and being vector it is sharp at 32px and
at 3000px and can be tinted from the palette.

The character is not in the mark either way. In the supplied file his trousers
and the glow behind him are one connected blob at the same brightness, proven by
labelling the difference between two cuts: a single 51,000 pixel component
spanning both. No threshold separates them, so any cut that removes the glow
removes his legs.

The castle is 1.51:1, so it is sized by width and the height follows. It reads
down to about 32px wide.

The name is set as **one name, one weight, one colour**. MAN used to sit in a
filled pill, which emphasised the least meaningful word in the name and made
the lockup read as a brand plus a tag. The artwork's own wordmark is unused: it
set the name as "CASTLEMAN", one word, in a glow that vanished at nav size.

### Colour

**The palette is sampled from the logo, not chosen.** Three values were pulled
straight out of the artwork and everything else is built around them:

| Role | Value | Where it came from |
|---|---|---|
| Brand blue | `#0056db` | the castle's blue panels |
| Brand yellow | `#fec521` | the castle's pillars |
| Ink | `#0b1a2e` | the navy the whole illustration is outlined in |

Grounds are cool blue-whites rather than warm cream, so they sit under the
blue: `--paper #f8fbff`, `--paper-2 #eaf1fd`, rail white, masthead `#dbe9ff`.

**Every call to action is the logo yellow with ink on it.** No category uses
yellow, so it never collides. A yellow fill is only 1.53:1 against the page, so
every yellow button carries a 2px ink border, which doubles as an echo of the
heavy outline the artwork is drawn with. `--accent-text` (`#8a6100`) is the
same yellow taken down to a tone that survives as small text on a light ground,
which the yellow itself cannot.

The focus ring is the brand blue, not the yellow, for the same reason: a yellow
ring is invisible against a near-white page.

Every hire category still owns a colour, and that colour follows it everywhere:
its dot in the rail, its shelf, its cards, its no-photo panels, its page
banner. Colour is information here, not decoration.

| Category | Fill | Text on it |
|---|---|---|
| Bouncy castles | `#0056db` the logo blue | white |
| Combi castles | `#6d28d9` violet | white |
| Obstacle courses | `#047857` emerald | white |
| Disco dome | `#c81e6a` pink | white |
| Sumo and gladiator | `#c2410c` orange | white |
| Marquees | `#0e7490` teal | white |

Sumo moved off amber to orange when yellow became the CTA, so no category
duplicates the button colour.

`--c` is a category as a **fill**, `--ct` the same category as **text on a
light ground**. All six now match, but the pair is kept: the moment a light
colour is added back they diverge again, as amber did at 2.07:1 on white.

`--ct` is written out explicitly on every `[data-cat]` row rather than
defaulting to `var(--c)`. A custom property whose value is another `var()` is
substituted where it is *declared*, not where it is used, so `--ct:var(--c)` on
`:root` would resolve once against the root colour and every category would
inherit that one value.

### Light surfaces

Navy is not used for anything bigger than a line of text except the contact
band. The rail, the masthead, the footer and the mobile action bar are all
light, and the weight comes from the brand colours: the blue areas band, the
navy contact band, the yellow lead cell in the bento, and each category's own
page banner.

Two knock-on rules from that change:

- Category dots in the rail use `--ct`, not `--c`. Amber sits at 1.99:1 against
  the light rail and would vanish.
- The card tag pill is white with ink on it rather than ink with white on it,
  so it reads over both a photograph and a saturated colour panel.

### Photos we do not use

`IMG_BANNER` is the old site's masthead **graphic**, the wordmark on a blue
ground, not a photo of anything. It was the Sumo and Gladiator category hero and
cropped to a 16/10 banner it rendered as a zoomed fragment of the word CASTLE.
It was also sitting in the gallery among the units. Both gone. The sumo category
now uses the no-photo panel in its own orange, which is better than a wrong
photo. Swap it for a real sumo shot the moment Adam sends one.

### Other decisions

- **Type**: Fredoka for display, Figtree for body.
- **Shape**: buttons and pills are fully round, cards and media are 16px,
  inputs are 12px. One rule, followed everywhere.
- **Motion**: CSS only. Scroll reveal, hover lifts, chunky offset button
  shadows that compress on press. Reveal is gated behind a `.js` class so a
  script failure can never hide content, and cards carry no reveal of their own
  because they live inside horizontally scrolling shelves.
- **No-photo panels**: units without a photo render their name set large on
  their own category colour. Set `img=` on the unit in `data.py` and the panel
  swaps itself out for the photo.
- The chatbot widget is gone. The rail carries the phone number, WhatsApp and
  the CTA at all times, and mobile has the action bar, so the bubble was doing
  nothing the layout was not already doing better.

## What is here

- Home, 6 category pages, 24 unit pages, an areas index, 9 town pages,
  gallery, FAQs, contact, hire terms
- JSON-LD: EntertainmentBusiness and FAQPage on the home page, Product on
  every unit page
- Redirects from every old bouncycastleman.com path (`/obstacle_courses`,
  `/bouncy_castles`, `/disco_dome`, `/marquees`, `/gallery`, `/contact`,
  `/index`)
- Filterable catalogue, area checker, FAQ accordion, chatbot, WhatsApp float

## Before go-live

Everything below is blocked on Adam. All of it is marked `TODO` in
`build/data.py`.

1. **Photos.** Nine real marquee photos arrived 2 Sep and are in
   `/images/marquees/`. Castles, combis, courses, the dome, sumo and gladiator
   still run on the old site's eight small hotlinked images. Those are the gap
   now.
2. **Image hosting.** Those eight images hotlink `files.secure.website`, the
   old site's host, which goes away when the domain moves. Download local
   copies into `/images/` and repoint `data.py` before the DNS cutover.
3. **Formspree.** `FORMSPREE` in `data.py` is still `[FORM-ID]`, so the form
   renders in a DRAFT state: fields visible so the layout can be judged, submit
   disabled, and a note reading just "Not connected yet." The note used to
   explain what was needed to fix it, which is a message for Sam, not for
   whoever is looking at the page. It used to ship pointing at
   `https://formspree.io/f/[FORM-ID]`, so a real enquiry would have gone nowhere
   silently, and a client looking at a draft is very likely to test the form. Set
   a real ID and the whole thing turns itself back on.
4. **Email address.** The old site publishes none, so the contact block falls
   back to WhatsApp. Set `EMAIL` in `data.py` once Adam gives one.
5. **Facebook.** `FACEBOOK` is `[FACEBOOK-URL]`. The icon is not rendered while
   the value is a placeholder: it used to ship as `href="[FACEBOOK-URL]"`, a
   dead link in the footer of all 45 pages. Set the real URL and it comes back.
6. **Reviews.** The three on the home page are sample wording. They used to be
   attributed to invented people ("Sarah M., Thurles"), which on the page reads
   as three real five star reviews from named customers in his own towns, and a
   client looking at a draft has no way to know otherwise. Quoting invented
   customers is not a placeholder, it is a fake review, and it only has to
   survive one approval to be live. The slot is named as a slot now ("Your
   review here") and `REVIEWS_NOTE` labels the section. Replace both before
   go-live.
7. **Areas.** CONFIRMED by Adam 27 Aug: all of Tipperary, and he has also
   delivered to Kilkenny, Waterford, Laois, Offaly and other neighbouring
   counties, but not regularly. The 9 towns stand. The second tier is not on
   the site yet and needs wording that does not promise a regular service.
8. **Prices.** Every unit says "Call for price" because the old site published
   none. Set `price=` per unit if Adam wants figures shown.
9. **Marquee sizes.** Adam said "various sizes" but gave none. `/marquees/`
   is written so it does not need them, but the page is stronger with them.
   Also unknown: whether the tables and chairs have a minimum order.
10. **Hire terms.** Deposits, cancellations, weather policy, damage and public
   liability wording are deliberately left blank on `/hire-terms/` rather
   than guessed at, because they are contractual.

Note that Adam approved the earlier cartoon demo, not this design. Flag the
change when you send him the preview link.

## Verified

Built and rendered in headless Chromium on 20 Aug 2026.

- 45 pages, 0 broken internal links, 0 duplicate titles, descriptions or
  canonicals, one h1 per page, no description over 170 chars
- 16 pages swept across 15 widths from 320px to 1600px, testing real sideways
  scroll rather than reported scrollWidth: zero sideways scroll anywhere
- Every rendered text node checked against its computed background across all
  six category colours and the dark rail, drawer open and closed: zero WCAG AA
  contrast failures
- Zero horizontal overflow inside the rail at every width from 320 up. This was
  broken: the desktop rail centres the lockup with `width:100%` on `.brand`, and
  the mobile media query flipped it back to a row without unsetting that, so the
  brand filled the whole bar and pushed the burger 32px past the edge. Because
  `.rail` sets `overflow-y:auto`, and CSS resolves the other axis to `auto`
  along with it, that overflow became a horizontal scroll INSIDE the rail: the
  drawer opened scrolled 32px right and its labels were cut off ("HAT WE HIRE",
  "ORE"). Fixed with `width:auto`, plus a 380px breakpoint where the mark gives
  way rather than the name
- Masthead headline holds to two lines at every desktop width
- Bento fills every row at all three breakpoints, no empty cell
- Shelf arrows, disabled states, rail drawer, area checker and FAQ accordion
  all confirmed working; every card ends at opacity 1 after a full scroll
- Zero em-dashes or en-dashes anywhere in the output
