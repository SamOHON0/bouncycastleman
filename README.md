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
files it generates. Writes 44 pages plus `assets/`, `sitemap.xml`,
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

A **persistent left rail** rather than a top nav. It carries the mark, the six
categories with their colour dots, the secondary pages, the phone number and
the one CTA, and it stays put while the content column scrolls. Below 1100px it
becomes a top bar with a drawer, and a **sticky action bar** pins Call and
WhatsApp to the bottom of the screen, which is what a parent on a phone
actually wants.

The **range is six horizontal shelves**, one per category, replacing the old
tile grid plus filtered card grid. You walk sideways through the category you
want, or open it for the full set. The arrows are an enhancement: the track
scrolls by touch, wheel and keyboard on its own, and the arrows are hidden
below 640px where swiping is the natural gesture.

The masthead is a dark block with the headline bottom-left and the photo
tilted and bleeding off the right edge, with the three fact cards straddling
the seam below it. Then: a dotted timeline for how it works, a six-cell bento
for why us, a full-bleed teal band with towns as pills and the area checker
inside it, staggered quote cards, a two-column FAQ, and a split contact block.
Every section is a different layout family and none repeats.

### The mark

An arch with a pennant flying off it, replacing the flat crenellated block. The
arch reads as a castle doorway rather than a battlement, the flag gives it a
fairground note, and the doorway is cut out with `fill-rule evenodd` so the
whole thing is one path. Two tone, vermillion and amber. The wordmark sets MAN
in a filled pill beside it. Same shape does duty as the SVG favicon.
`logo_mark()` in `generate.py`.

### Colour

Playful as a **system** rather than decoration. Every hire category owns a
colour, and that colour follows it everywhere: its dot in the rail, its shelf,
its cards, its no-photo panels, its page banner. Colour is information here,
which is why the page can carry six brights without turning into confetti.

| Category | Fill | Text on it |
|---|---|---|
| Bouncy castles | `#2563eb` blue | white |
| Combi castles | `#7c3aed` violet | white |
| Obstacle courses | `#047857` emerald | white |
| Disco dome | `#c81e6a` pink | white |
| Sumo and gladiator | `#f5a300` amber | ink |
| Marquees | `#0e7490` teal | white |

One colour never varies: **every call to action is vermillion**, on every page,
in every section, so "the thing you press" is learnable at a glance. Category
colour never leaks onto a button.

Two rules that are load bearing, do not collapse them:

- `--c` is a category's colour as a **fill**. `--ct` is the same category as
  **text on a light background**. For five of the six they are identical; amber
  is only 2.07:1 on white so its text tone is a dark bronze `#966300`.
- `--accent` (#f4491f) is for large display type and graphic marks only.
  `--accent-text` (#c9330f) is for anything under 24px and for filled buttons.

`--ct` is written out explicitly on every `[data-cat]` row rather than
defaulting to `var(--c)`. A custom property whose value is another `var()` is
substituted where it is *declared*, not where it is used, so `--ct:var(--c)` on
`:root` would resolve once against the root colour and every category would
inherit that one value.

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

- Home, 6 category pages, 23 unit pages, an areas index, 9 town pages,
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
7. **Areas.** The 9 towns are the ones from the demo pitch, not confirmed by
   Adam. Add or drop in `AREAS`.
8. **Prices.** Every unit says "Call for price" because the old site published
   none. Set `price=` per unit if Adam wants figures shown.
9. **Hire terms.** Deposits, cancellations, weather policy, damage and public
   liability wording are deliberately left blank on `/hire-terms/` rather
   than guessed at, because they are contractual.

Note that Adam approved the earlier cartoon demo, not this design. Flag the
change when you send him the preview link.

## Verified

Built and rendered in headless Chromium on 20 Aug 2026.

- 44 pages, 0 broken internal links, 0 duplicate titles, descriptions or
  canonicals, one h1 per page, no unclosed tags, no description over 170 chars
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
