# Bouncy Castle Man

Static site for Bouncy Castle Man (bouncycastleman.com), Tipperary. Same build
shape as Mr Bounce Sligo: `build/base.html` holds the design, `build/data.py`
holds the content, `build/pages.py` builds the pages.

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

To preview locally:

```bash
python3 -m http.server 8000
```

## Deploy

Push to GitHub and point Vercel at the repo root. No framework, no build
command, output directory is the root. `vercel.json` already carries
`trailingSlash: true`, the old site's URL redirects and a one year immutable
cache on `/assets/`.

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

1. **Photos.** The old site only serves eight usable images. Every unit
   without one renders a "photo coming soon" tile rather than a broken image.
   Set `img=` on the unit in `data.py` as photos arrive.
2. **Image hosting.** The eight images we do have hotlink
   `files.secure.website`, the old site's host. That host goes away when the
   domain moves. Download local copies into `/images/` and repoint `data.py`
   before the DNS cutover.
3. **Formspree.** `FORMSPREE` in `data.py` is still `[FORM-ID]`.
4. **Email address.** The old site publishes none, so the contact block falls
   back to WhatsApp. Set `EMAIL` in `data.py` once Adam gives one.
5. **Logo.** None supplied, the header uses the house SVG mark plus the
   business name. `LOGO` in `data.py` is empty.
6. **Facebook.** `FACEBOOK` is `[FACEBOOK-URL]`.
7. **Reviews.** The three on the home page are placeholders, marked as such in
   `data.py`. Replace before go-live.
8. **Areas.** The 9 towns are the ones from the demo pitch, not confirmed by
   Adam. Add or drop in `AREAS`.
9. **Prices.** Every unit says "Call for price" because the old site published
   none. Set `price=` per unit if Adam wants figures shown.
10. **Hire terms.** Deposits, cancellations, weather policy, damage and public
    liability wording are deliberately left blank on `/hire-terms/` rather
    than guessed at, because they are contractual.

## Verified

Built and rendered in a headless browser on 20 Aug 2026: 44 pages, 0 broken
internal links, 0 duplicate titles or canonicals, no description over 170
chars, one h1 per page, no unclosed tags, no horizontal scroll at 390px, no
JS console errors. Catalogue crop, View all, category filters, area checker,
FAQ accordion and chatbot all confirmed working.
