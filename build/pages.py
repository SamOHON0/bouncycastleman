# -*- coding: utf-8 -*-
"""Page builders for Bouncy Castle Man. Run: python3 generate.py

Layout discipline notes (these are deliberate, do not "tidy" them away):
  - The rail is emitted AFTER the content column in the DOM so the h1 is the
    first thing in the document. Grid puts it back on the left.
  - Eyebrows are rationed to one per three sections. The home page uses 2.
  - No section layout family repeats: masthead, straddling fact cards, shelves,
    dotted timeline, bento, colour band with pills, staggered quotes, two
    column accordion, split contact. Each appears once.
  - The bento has exactly six cells for six points, no empty cell at the end.
  - Cards carry no data-reveal. They sit inside horizontally scrolling shelves
    where an observer can miss one and leave it stuck at opacity 0; the shelf
    reveals as a whole instead.
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
import generate as G

esc, write, head, footer = G.esc, G.write, G.head, G.footer
page_hero, card, safety_box, contact_block = (
    G.page_hero, G.card, G.safety_box, G.contact_block)
marquee_block, signpost = G.marquee_block, G.signpost
shot, ico, wa_link = G.shot, G.ico, G.wa_link

BUILT = []


def ld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False)


def biz():
    o = {
        "@context": "https://schema.org", "@type": "EntertainmentBusiness", "name": D.NAME,
        "url": D.SITE + "/", "telephone": D.PHONE_INTL, "image": D.HERO_MAIN,
        "foundingDate": D.FOUNDED,
        "description": "Bouncy castle, combi castle, obstacle course, disco dome, sumo suit "
                       "and marquee hire across Tipperary and the surrounding areas.",
        "address": {"@type": "PostalAddress", "addressLocality": D.LOCALITY,
                    "addressRegion": D.REGION, "addressCountry": "IE"},
        "areaServed": [a["town"] for a in D.AREAS],
    }
    if D.EMAIL:
        o["email"] = D.EMAIL
    return o


def faq_ld():
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in D.FAQS]}


def faq_markup():
    return "".join(
        f'<div class="faq-item"><button class="faq-q" aria-expanded="false">{esc(q)}</button>'
        f'<div class="faq-a"><p>{esc(a)}</p></div></div>' for q, a in D.FAQS)


# ---------------------------------------------------------------- home ------
def shelf(c):
    """One category as a horizontal scroll shelf. Replaces the old tile grid
    plus filtered card grid: the range is browsed by walking sideways through
    the category you actually want."""
    units = [u for u in D.UNITS if u["cat"] == c["cat"]]
    cards = "".join(card(u) for u in units)
    return f"""
  <section class="shelf" data-shelf data-reveal data-cat="{c['cat']}" aria-label="{c['title']}">
    <div class="shelf-head">
      <span class="dot"></span>
      <h3>{c['title']}</h3>
      <a class="all" href="/{c['slug']}/">All {len(units)}</a>
      <div class="shelf-nav">
        <button type="button" data-dir="prev" aria-label="Scroll {c['title']} left">{ico("left")}</button>
        <button type="button" data-dir="next" aria-label="Scroll {c['title']} right">{ico("right")}</button>
      </div>
    </div>
    <div class="track">{cards}</div>
  </section>
"""


def build_home():
    steps = "".join(
        f'<div class="line-step" data-reveal><div class="line-n">{i+1}</div>'
        f'<h3>{t}</h3><p>{esc(p)}</p></div>'
        for i, (t, p) in enumerate(D.STEPS))

    whys = "".join(
        f'<li data-reveal><span class="n">{i+1:02d}</span><div><h3>{esc(h)}</h3>'
        f'<p>{esc(p)}</p></div></li>' for i, (_e, h, p) in enumerate(D.WHY))

    revs = "".join(
        f'<div class="rev" data-reveal><div class="stars">★★★★★</div>'
        f'<p>{esc(t)}</p><div class="who">{w}, {loc}</div></div>'
        for t, w, loc in D.REVIEWS)

    towns = "".join(f'<a href="/{a["slug"]}/">{a["town"]}</a>' for a in D.AREAS)
    opts = "".join(f"<option>{o}</option>" for o in D.AREA_OPTIONS)
    gal = "".join(f'<a href="/gallery/" data-reveal>{shot(g, "Bouncy Castle Man hire")}</a>'
                  for g in D.GALLERY[:6])
    shelves = "".join(shelf(c) for c in D.CATEGORIES)

    html = head(
        "Bouncy Castle Hire Tipperary | Obstacle Courses, Combi Castles &amp; Marquees | " + D.NAME,
        "Bouncy castles, combi castles, obstacle courses, disco dome and marquees across "
        f"Clonmel, Thurles, Nenagh, Cashel and all of Tipperary. Call {D.PHONE_DISPLAY}.",
        "/", D.HERO_IMG)
    html += ld(biz()) + ld(faq_ld())
    html += f"""
<section class="mast">
  <div class="mast-grid">
    <div>
      <span class="eyebrow">Family run in Tipperary since {D.FOUNDED}</span>
      <h1>Bouncy castle hire across <em>Tipperary</em></h1>
      <p>Castles, combis and obstacle courses up to 55ft. Delivered, set up and collected.</p>
      <div class="mast-actions">
        <a href="/contact/" class="btn btn-accent">Get a price</a>
        <a href="tel:{D.PHONE_TEL}" class="btn btn-line">{ico("phone")}{D.PHONE_DISPLAY}</a>
      </div>
    </div>
    <div class="mast-shot">
      {shot(D.HERO_IMG, D.HERO_IMG_NAME, ratio=None, eager=True)}
      <span class="mast-tag">{D.HERO_IMG_NAME}, {D.HERO_IMG_TAG}</span>
    </div>
  </div>
</section>
<div class="facts">
  <div><b>{D.FOUNDED}</b><span>Family run ever since, same phone number</span></div>
  <div><b>{len(D.UNITS)} units</b><span>From a 12ft arch castle to a 55ft course</span></div>
  <div><b>IIHF</b><span>Fully insured and certified</span></div>
</div>

<div class="band band-tight">
  <div class="sec-head" style="margin-bottom:0">
    <h2>The range</h2>
    <p>Six kinds of hire. Walk sideways through any shelf, or open a category for the lot.</p>
  </div>
</div>
{shelves}

<div class="band">{marquee_block(
    "Marquees, floored, furnished, lit and heated",
    "A marquee in the size your numbers need, on its own or fitted out. Communions, "
    "confirmations, corporate days and family parties, in any season.")}</div>

<div class="band tint">
  <div class="sec-head"><h2>How it works</h2></div>
  <div class="line narrow">{steps}</div>
</div>

<div class="band">
  <div class="sec-head"><h2>Why people ring us</h2></div>
  <ul class="bento">{whys}</ul>
</div>

<div class="band areas-band">
  <div class="sec-head"><h2>Where we deliver</h2>
    <p>Tipperary and the surrounding areas. If your town is not here, ring us, we may still reach you.</p></div>
  <div class="town-list">{towns}</div>
  <div class="checker">
    <h3>Check your area</h3>
    <div class="checker-row">
      <select id="areaSel" aria-label="Select your area">
        <option value="">Select your area</option>{opts}
        <option value="__other__">My area isn't listed</option>
      </select>
      <button class="btn btn-accent" id="areaBtn">Check</button>
    </div>
    <div id="areaOut" role="status"></div>
  </div>
</div>

<div class="band">
  <div class="sec-head"><span class="eyebrow">Testimonials</span><h2>What locals say</h2></div>
  <div class="revs">{revs}</div>
</div>

<div class="band tint">
  <div class="sec-head"><h2>Out on the road</h2></div>
  <div class="gallery">{gal}</div>
</div>

<div class="band">
  <div class="sec-head"><h2>Common questions</h2></div>
  <div class="faq">{faq_markup()}</div>
</div>
{contact_block()}{footer()}"""
    BUILT.append(write("index.html", html))


# ------------------------------------------------------------ categories ----
def build_categories():
    for c in D.CATEGORIES:
        units = [u for u in D.UNITS if u["cat"] == c["cat"]]
        items = "".join(card(u) for u in units)
        towns = "".join(f'<a href="/{a["slug"]}/">{a["town"]}</a>' for a in D.AREAS)
        # "All 1 of our disco dome travel" is broken English, so singular gets
        # its own sentence.
        # Marquees is the one category whose units are not all the same noun:
        # "All 2 of our marquees travel" would be counting the chairs as a
        # marquee. It gets its own sentence.
        if c["cat"] == "marquee":
            travels = "Marquees, tables and chairs travel to every town we cover."
        elif len(units) == 1:
            travels = f"Our {c['title'].lower().rstrip('s')} travels to every town we cover."
        else:
            travels = (f"All {len(units)} of our {c['title'].lower()} travel to every town "
                       f"we cover.")
        html = head(f"{c['title']} Hire Tipperary | {D.NAME}",
                    esc(c["intro"])[:158], f"/{c['slug']}/", c["hero"])
        html += page_hero(f"{c['title']} hire in Tipperary", esc(c["blurb"]), c["hero"],
                          [(None, c["title"])], cat=c["cat"])
        # Marquees lead with the fit-out block. The category is two hire lines
        # rather than a wall of units, so a card grid on its own says almost
        # nothing about what you actually get.
        sign = "" if c["cat"] == "marquee" else signpost(
            "We hire marquees as well, in a range of sizes, with flooring, tables, chairs, "
            "lighting and heating. Tables and chairs on their own too.")
        lead = ""
        if c["cat"] == "marquee":
            lead = ('<div class="band" style="padding-bottom:0">'
                    + marquee_block("What a marquee from us looks like",
                                    "Sized to your numbers, in all seasons, delivered, put up "
                                    "and taken down again. Fit it out with as much or as "
                                    "little as you need.")
                    + "</div>")
        html += lead + f"""
<div class="band" data-cat="{c['cat']}">
  <div class="prose" style="margin-bottom:36px"><p>{esc(c['intro'])}</p></div>
  <div class="grid" data-reveal>{items}</div>
  {safety_box()}
  {sign}
</div>

<div class="band areas-band">
  <div class="sec-head"><h2>Delivered across Tipperary</h2>
    <p>{travels}</p></div>
  <div class="town-list">{towns}</div>
</div>
{contact_block()}{footer()}"""
        BUILT.append(write(f"{c['slug']}/index.html", html))


# ----------------------------------------------------------- unit pages ----
def build_units():
    bycat = {c["cat"]: c for c in D.CATEGORIES}
    for u in D.UNITS:
        c = bycat[u["cat"]]
        specs = "".join(f'<div class="spec"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>'
                        for k, v in u["specs"])
        body = "".join(f"<p>{esc(p)}</p>" for p in u["body"])
        rel = [x for x in D.UNITS if x["cat"] == u["cat"] and x["slug"] != u["slug"]][:4]
        # Marquee units already sit on the marquee side of the site.
        sign = "" if u["cat"] == "marquee" else signpost(
            "Doing a communion, a confirmation or a party that needs cover as well? We hire "
            "marquees, and tables and chairs on their own.")
        prod = {"@context": "https://schema.org", "@type": "Product", "name": u["n"],
                "description": u["short"], "brand": {"@type": "Brand", "name": D.NAME},
                "offers": {"@type": "Offer", "availability": "https://schema.org/InStock",
                           "priceCurrency": "EUR", "url": f"{D.SITE}/hire/{u['slug']}/"}}
        if u["img"] != D.SOON:
            prod["image"] = u["img"]
        html = head(f"{esc(u['n'])} Hire Tipperary | {D.NAME}", esc(u["short"])[:158],
                    f"/hire/{u['slug']}/", u["img"])
        html += ld(prod)
        html += page_hero(esc(u["n"]), esc(u["short"]), D.SOON,
                          [(f"/{c['slug']}/", c["title"]), (None, esc(u["n"]))], cat=u["cat"])
        more = ""
        if rel:
            more = f"""
<div class="band tint" data-cat="{u['cat']}">
  <div class="sec-head"><h2>Other {c['title'].lower()}</h2></div>
  <div class="grid" data-reveal>{"".join(card(r) for r in rel)}</div>
</div>
"""
        html += f"""
<div class="band" data-cat="{u['cat']}">
  <div class="unit">
    <div>
      {shot(u['img'], u['n'], ratio="16/10", eager=True)}
      <h2>About the {esc(u['n'])}</h2>
      <div class="prose">{body}</div>
      <dl class="specs">{specs}</dl>
      {safety_box()}
      {sign}
    </div>
    <aside class="unit-side">
      <span class="price">{u['price']}</span>
      <p>Delivered, set up and collected across Tipperary and the surrounding areas.</p>
      <a href="tel:{D.PHONE_TEL}" class="btn btn-accent">{ico("phone")}{D.PHONE_DISPLAY}</a>
      <a href="/contact/" class="btn btn-line">Get a price</a>
      <a href="{wa_link()}" target="_blank" rel="noopener" class="btn btn-line">WhatsApp us</a>
    </aside>
  </div>
</div>
{more}{contact_block()}{footer()}"""
        BUILT.append(write(f"hire/{u['slug']}/index.html", html))


# ----------------------------------------------------------- area pages -----
def build_areas():
    opts = "".join(f"<option>{o}</option>" for o in D.AREA_OPTIONS)
    towns = "".join(f'<a href="/{a["slug"]}/">{a["town"]}</a>' for a in D.AREAS)
    rows = "".join(
        f'<div class="area-row" data-reveal><h3><a href="/{a["slug"]}/">{a["town"]}</a></h3>'
        f'<p>{a["county"]}. Also {esc(a["nearby"])}.</p></div>' for a in D.AREAS)
    html = head(f"Areas We Cover | Bouncy Castle Hire Tipperary | {D.NAME}",
                "The towns we deliver to across Tipperary, from Clonmel and Thurles to Nenagh, "
                "Cashel, Roscrea, Templemore, Cahir and Carrick on Suir.", "/areas/")
    html += page_hero("Areas we cover",
                      "Tipperary and the surrounding areas. If your town is not listed, ring us, "
                      "we may still reach you.", D.IMG_AREAS, [(None, "Areas")], cat="marquee")
    html += f"""
<div class="band">
  <div class="area-rows">{rows}</div>
</div>

<div class="band areas-band">
  <div class="sec-head"><h2>Check your area</h2></div>
  <div class="town-list">{towns}</div>
  <div class="checker">
    <h3>Do we come to you?</h3>
    <div class="checker-row">
      <select id="areaSel" aria-label="Select your area">
        <option value="">Select your area</option>{opts}
        <option value="__other__">My area isn't listed</option>
      </select>
      <button class="btn btn-accent" id="areaBtn">Check</button>
    </div>
    <div id="areaOut" role="status"></div>
  </div>
</div>
{contact_block()}{footer()}"""
    BUILT.append(write("areas/index.html", html))

    for a in D.AREAS:
        copy = "".join(f"<p>{esc(p)}</p>" for p in a["copy"])
        others = "".join(f'<a href="/{o["slug"]}/">{o["town"]}</a>'
                         for o in D.AREAS if o["slug"] != a["slug"])
        picks = "".join(card(u) for u in D.UNITS[:4])
        html = head(f"Bouncy Castle Hire {a['town']} | {D.NAME}",
                    f"Bouncy castle, combi castle and obstacle course hire in {a['town']}, "
                    f"{a['county']}. Delivered and set up, rain covers as standard. "
                    f"Call {D.PHONE_DISPLAY}.", f"/{a['slug']}/")
        html += page_hero(f"Bouncy castle hire in {a['town']}",
                          f"Castles, combis, obstacle courses, the disco dome and marquees, "
                          f"delivered and set up in {a['town']} and around.",
                          D.HERO_MAIN, [("/areas/", "Areas"), (None, a["town"])], cat="castle")
        html += f"""
<div class="band">
  <div class="prose">{copy}
    <h2>What we bring to {a['town']}</h2>
    <p>The full range travels: bouncy castles, combi castles with built in slides, obstacle
    courses from a 30ft block run up to the 55ft high adrenaline units, the disco dome, sumo
    suits, the gladiator challenge and marquees. Everything is delivered, set up and collected.</p>
  </div>
  {safety_box()}
  {signpost(
      f"Marquees come to {a['town']} too, in a range of sizes, with flooring, tables, chairs, "
      f"lighting and heating. Tables and chairs on their own as well.",
      link="See marquee hire")}
</div>

<div class="band tint">
  <div class="sec-head"><h2>What people book in {a['town']}</h2></div>
  <div class="grid" data-reveal>{picks}</div>
</div>

<div class="band areas-band">
  <div class="sec-head"><h2>Other areas</h2></div>
  <div class="town-list">{others}</div>
</div>
{contact_block()}{footer()}"""
        BUILT.append(write(f"{a['slug']}/index.html", html))


# ------------------------------------------------ gallery, faqs, contact ----
def build_simple():
    gal = "".join(f'<a href="/contact/" data-reveal>{shot(g, "Bouncy Castle Man hire")}</a>'
                  for g in D.GALLERY)
    html = head(f"Gallery | {D.NAME}",
                "Photos of our bouncy castles, combi castles, obstacle courses, disco dome and "
                "marquees out on the road across Tipperary.", "/gallery/")
    html += page_hero("Gallery", "Our castles and courses out on the road.",
                      D.SOON, [(None, "Gallery")], cat="disco")
    html += f"""
<div class="band">
  <div class="gallery">{gal}</div>
  <div class="note" style="margin-top:32px">More photos going up shortly. If you have a photo of
  one of our units at your event we would love to see it.</div>
</div>
{contact_block()}{footer()}"""
    BUILT.append(write("gallery/index.html", html))

    html = head(f"FAQs | Bouncy Castle Hire Tipperary | {D.NAME}",
                "Common questions about bouncy castle and obstacle course hire in Tipperary: "
                "what we hire, areas covered, insurance and how to book.", "/faqs/")
    html += ld(faq_ld())
    html += page_hero("Common questions", "What we hire, where we go, insurance and how to book.",
                      D.SOON, [(None, "FAQs")], cat="combi")
    html += f"""
<div class="band">
  <div class="faq">{faq_markup()}</div>
  {safety_box()}
</div>
{contact_block()}{footer()}"""
    BUILT.append(write("faqs/index.html", html))

    opts = "".join(f"<option>{o}</option>" for o in D.AREA_OPTIONS)
    html = head(f"Contact | Bouncy Castle Hire Tipperary | {D.NAME}",
                f"Call or WhatsApp {D.PHONE_DISPLAY}, or send an enquiry. Bouncy castle, "
                "obstacle course and marquee hire across Tipperary.", "/contact/")
    html += page_hero("Contact", f"Ring or WhatsApp {D.PHONE_DISPLAY}, or send an enquiry below.",
                      D.SOON, [(None, "Contact")], cat="obstacle")
    html += f"""
<div class="band areas-band">
  <div class="checker" style="margin-top:0">
    <h3>Do we come to you?</h3>
    <div class="checker-row">
      <select id="areaSel" aria-label="Select your area">
        <option value="">Select your area</option>{opts}
        <option value="__other__">My area isn't listed</option>
      </select>
      <button class="btn btn-accent" id="areaBtn">Check</button>
    </div>
    <div id="areaOut" role="status"></div>
  </div>
</div>
{contact_block()}{footer()}"""
    BUILT.append(write("contact/index.html", html))

    terms = "".join(f"<li>{esc(s)}</li>" for s in D.SAFETY)
    html = head(f"Hire Terms | {D.NAME}",
                "Hire conditions for Bouncy Castle Man, including delivery and collection, "
                "supervision and insurance.", "/hire-terms/")
    html += page_hero("Hire terms", "The conditions that apply to every hire.",
                      D.SOON, [(None, "Hire terms")], cat="marquee")
    html += f"""
<div class="band">
  <div class="prose">
    <h2 style="margin-top:0">Hire conditions</h2>
    <ul style="padding-left:20px;list-style:disc">{terms}</ul>
    <h2>Delivery and collection</h2>
    <p>{esc(D.DELIVERY_TERMS)}</p>
    <h2>Bookings</h2>
    <p>Bookings are confirmed by phone on {D.PHONE_DISPLAY}. Prices depend on the unit, the date
    and your area, and are given on enquiry.</p>
  </div>
  <div class="note" style="margin-top:28px"><strong>To be completed.</strong> Adam still needs to
  supply the wording for deposits, cancellations, the weather policy, damage and the public
  liability cover. Those sections are left out rather than guessed at, because they are
  contractual.</div>
</div>
{contact_block()}{footer()}"""
    BUILT.append(write("hire-terms/index.html", html))


# ------------------------------------------------- sitemap, robots, config --
def build_meta():
    urls = ["/"] + [f"/{c['slug']}/" for c in D.CATEGORIES] + \
           [f"/hire/{u['slug']}/" for u in D.UNITS] + \
           ["/areas/"] + [f"/{a['slug']}/" for a in D.AREAS] + \
           ["/gallery/", "/faqs/", "/contact/", "/hire-terms/"]
    body = "".join(f"  <url><loc>{D.SITE}{u}</loc></url>\n" for u in urls)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {D.SITE}/sitemap.xml\n")
    cfg = {
        "trailingSlash": True,
        "cleanUrls": False,
        "redirects": [{"source": s, "destination": d, "permanent": True}
                      for s, d in D.REDIRECTS],
        "headers": [{"source": "/assets/(.*)",
                     "headers": [{"key": "Cache-Control",
                                  "value": "public, max-age=31536000, immutable"}]}],
    }
    write("vercel.json", json.dumps(cfg, indent=2) + "\n")
    return urls


def main():
    build_home()
    build_categories()
    build_units()
    build_areas()
    build_simple()
    urls = build_meta()
    print("pages written: %d" % len(BUILT))
    print("sitemap urls: %d" % len(urls))


if __name__ == "__main__":
    G.build_assets()
    main()
