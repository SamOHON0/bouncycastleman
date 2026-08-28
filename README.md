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

**No marquee size is quoted anywhere.** Adam said "various sizes" and has not
given the actual dimensions, capacities or prices. The copy is written so it
does not need them ("sized to your numbers") rather than guessing at a figure.
Add them to `MARQUEE_EXTRAS` and the unit specs when he comes back and the page
reads a good deal stronger.

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

1. **Photos.** The old site only serves eight usable images. This design is
   photo led, so photos are the single biggest lift available to it.
2. **Image hosting.** Those eight images hotlink `files.secure.website`, the
   old site's host, which goes away when the domain moves. Download local
   copies into `/images/` and repoint `data.py` before the DNS cutover.
3. **Formspree.** `FORMSPREE` in `data.py` is still `[FORM-ID]`.
4. **Email address.** The old site publishes none, so the contact block falls
   back to WhatsApp. Set `EMAIL` in `data.py` once Adam gives one.
5. **Facebook.** `FACEBOOK` is `[FACEBOOK-URL]`.
6. **Reviews.** The three on the home page are placeholders, marked as such in
   `data.py`. Replace before go-live.
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
- Masthead headline holds to two lines at every desktop width
- Bento fills every row at all three breakpoints, no empty cell
- Shelf arrows, disabled states, rail drawer, area checker and FAQ accordion
  all confirmed working; every card ends at opacity 1 after a full scroll
- Zero em-dashes or en-dashes anywhere in the output
