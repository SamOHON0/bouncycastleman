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

Bold modern and photo led. Off-black ink on warm paper with ONE saturated
accent, vermillion. The castles are the colour on this page, the furniture is
not, which is why the page furniture stays restrained: the moment Adam's
photos land, they carry the whole thing.

- **Type**: Bricolage Grotesque for display, Figtree for body.
- **Colour**: `--accent` (#f4491f) is for large display type and graphic marks
  only. `--accent-text` (#c9330f) is for anything under 24px and for filled
  buttons. This split exists purely for contrast, do not collapse it.
- **Radius**: one scale, 4px, everything. No pills, no mixed corners.
- **Motion**: CSS only, scroll reveal plus hover and active states. Reveal is
  gated behind a `.js` class so a script failure can never hide content.
- **Logo**: wordmark plus a castle mark (crenellated top, arch cut out),
  single path, one colour, also used as the SVG favicon. It is in
  `generate.py` as `logo_mark()`.
- **No-photo panels**: units without a photo render their name set large on
  ink rather than a broken image or a grey box. Set `img=` on the unit in
  `data.py` and the panel swaps itself out for the photo.

Layout rules that are deliberate: eyebrows are rationed to one per three
sections, no section layout family repeats on a page, and there is no
three-equal-cards row anywhere. `pages.py` has a note at the top.

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
- 15 pages swept across 10 breakpoints from 360px to 1440px: no horizontal
  overflow, no nav wrapping to a second line, no button label wrapping, no JS
  console errors
- Every rendered text node checked against its computed background: zero
  WCAG AA contrast failures
- Hero headline holds to two lines at every width
- Catalogue crop, View all, category filters, area checker, FAQ accordion and
  chatbot all confirmed working
- Zero em-dashes or en-dashes anywhere in the output
