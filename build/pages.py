# -*- coding: utf-8 -*-
"""Page builders for Bouncy Castle Man. Run: python3 generate.py

Layout discipline notes (these are deliberate, do not "tidy" them away):
  - Eyebrows are rationed to one per three sections. The home page has 10
    sections and uses 3.
  - No section layout family repeats. Bento, filtered card grid, ruled columns,
    sticky split, typographic column list, ruled quotes, accordion, colour band
    are all used once each.
  - No three-equal-cards row anywhere.
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
import generate as G

esc, write, head, footer = G.esc, G.write, G.head, G.footer
page_hero, card, safety_box, contact_block = (
    G.page_hero, G.card, G.safety_box, G.contact_block)
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


def filters_bar():
    btns = ['<button class="filter-btn active" data-cat="all">Everything</button>']
    for c in D.CATEGORIES:
        btns.append(f'<button class="filter-btn" data-cat="{c["cat"]}">{c["title"]}</button>')
    return '<div class="filters" id="filters">%s</div>' % "".join(btns)


def booking_strip():
    opts = "".join(f"<option>{o}</option>" for o in D.AREA_OPTIONS)
    cats = "".join(f'<option>{c["title"]}</option>' for c in D.CATEGORIES)
    return f"""
<div class="strip">
  <div class="strip-cell">
    <h3>Do we come to you?</h3>
    <p>Tipperary and the surrounding areas.</p>
    <div class="strip-row">
      <select id="areaSel" aria-label="Select your area">
        <option value="">Select your area</option>{opts}
        <option value="__other__">My area isn't listed</option>
      </select>
      <button class="btn btn-ink" id="areaBtn">Check</button>
    </div>
    <div id="areaOut" role="status"></div>
  </div>
  <div class="strip-cell">
    <h3>Plan the day</h3>
    <p>Pick a date and what you're after.</p>
    <div class="strip-row">
      <input type="date" id="bDate" aria-label="Date of event">
      <select id="bCat" aria-label="Category"><option value="">Everything</option>{cats}</select>
      <a class="btn btn-accent" href="/contact/">Get a price</a>
    </div>
  </div>
</div>
"""


def area_columns():
    return '<div class="area-cols">%s</div>' % "".join(
        f'<a href="/{a["slug"]}/">{a["town"]}<span>{esc(a["nearby"])}</span></a>'
        for a in D.AREAS)


# ---------------------------------------------------------------- home ------
def build_home():
    # Bento: exactly six cells for six categories. First two run wide.
    tiles = "".join(f"""      <a class="cat" href="/{c['slug']}/" data-cat="{c['cat']}" data-reveal>
        {shot(c['hero'], c['title'], ratio="16/9" if i < 2 else "4/3")}
        <h3>{c['title']} {ico("arrow")}</h3>
        <p>{esc(c['blurb'])}</p>
      </a>
""" for i, c in enumerate(D.CATEGORIES))

    steps = "".join(
        f'<div class="step" data-reveal><div class="step-n">{i+1}</div>'
        f'<h3>{t}</h3><p>{esc(p)}</p></div>'
        for i, (t, p) in enumerate(D.STEPS))

    whys = "".join(
        f'<li data-reveal><span class="n">{i+1:02d}</span><div><h3>{esc(h)}</h3>'
        f'<p>{esc(p)}</p></div></li>' for i, (_e, h, p) in enumerate(D.WHY))

    revs = "".join(
        f'<div class="review" data-reveal><div class="stars">★★★★★</div>'
        f'<p>{esc(t)}</p><div class="who">{w}, {loc}</div></div>'
        for t, w, loc in D.REVIEWS)

    gal = "".join(f'<a href="/gallery/" data-reveal>{shot(g, "Bouncy Castle Man hire")}</a>'
                  for g in D.GALLERY[:6])

    html = head(
        "Bouncy Castle Hire Tipperary | Obstacle Courses, Combi Castles &amp; Marquees | " + D.NAME,
        "Bouncy castles, combi castles, obstacle courses, disco dome and marquees across "
        f"Clonmel, Thurles, Nenagh, Cashel and all of Tipperary. Call {D.PHONE_DISPLAY}.",
        "/", D.HERO_IMG)
    html += ld(biz()) + ld(faq_ld())
    html += f"""
<section class="hero">
  <div class="confetti" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Family run in Tipperary since {D.FOUNDED}</span>
        <h1>Bouncy castle hire in <em>Tipperary</em></h1>
        <p>Castles, combis and obstacle courses up to 55ft. Delivered, set up and collected.</p>
        <div class="hero-actions">
          <a href="/contact/" class="btn btn-accent">Get a price</a>
          <a href="tel:{D.PHONE_TEL}" class="btn btn-line">{ico("phone")}{D.PHONE_DISPLAY}</a>
        </div>
      </div>
      <div class="hero-photo">
        {shot(D.HERO_IMG, D.HERO_IMG_NAME, ratio="4/3.05", eager=True)}
        <div class="hero-badge">{D.HERO_IMG_NAME}<b>{D.HERO_IMG_TAG}</b></div>
      </div>
    </div>
    <div class="facts">
      <div><b>{D.FOUNDED}</b><span>Family run ever since, same phone number</span></div>
      <div><b>{len(D.UNITS)} units</b><span>From a 12ft arch castle to a 55ft course</span></div>
      <div><b>IIHF</b><span>Fully insured and certified</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <h2>What we hire</h2>
      <p>Six kinds of hire, every one delivered and set up across the county.</p>
    </div>
    <div class="cats">
{tiles}    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">The full range</span>
      <h2>Every unit we run</h2>
      <p>Tap any one for the sizes, the features and what it suits.</p>
    </div>
    {filters_bar()}
    <div class="catalogue cropped" id="grid">
{"".join(card(u) for u in D.UNITS)}    </div>
    <div class="more-row"><a href="#grid" id="viewAll" class="btn btn-ink">View all {len(D.UNITS)} units</a></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><h2>How it works</h2></div>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="why">
      <div class="why-head">
        <h2>Why people ring us</h2>
        <p class="lede" style="margin-top:16px;font-size:16.5px">Over twenty years of birthdays, communions and sports days across Tipperary.</p>
      </div>
      <ul class="why-list">{whys}</ul>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><h2>Where we deliver</h2>
      <p>Tipperary and the surrounding areas. If your town is not here, ring us, we may still reach you.</p></div>
    {area_columns()}
    <div style="margin-top:44px">{booking_strip()}</div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Testimonials</span><h2>What locals say</h2></div>
    <div class="reviews">{revs}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><h2>Out on the road</h2></div>
    <div class="gallery">{gal}</div>
    <div class="more-row"><a href="/gallery/" class="btn btn-line">See the gallery</a></div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><h2>Common questions</h2></div>
    <div class="faq">{faq_markup()}</div>
  </div>
</section>
{contact_block()}{footer()}"""
    BUILT.append(write("index.html", html))


# ------------------------------------------------------------ categories ----
def build_categories():
    for c in D.CATEGORIES:
        units = [u for u in D.UNITS if u["cat"] == c["cat"]]
        items = "".join(card(u) for u in units)
        html = head(f"{c['title']} Hire Tipperary | {D.NAME}",
                    esc(c["intro"])[:158], f"/{c['slug']}/", c["hero"])
        html += page_hero(f"{c['title']} hire in Tipperary", esc(c["blurb"]), c["hero"],
                          [(None, c["title"])], cat=c["cat"])
        html += f"""
<section>
  <div class="wrap">
    <div class="prose" style="margin-bottom:40px"><p>{esc(c['intro'])}</p></div>
    <div class="catalogue">{items}</div>
    {safety_box()}
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><h2>Delivered across Tipperary</h2>
      <p>All {len(units)} of our {c['title'].lower()} travel to every town we cover.</p></div>
    {area_columns()}
  </div>
</section>
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
<section class="tint">
  <div class="wrap">
    <div class="sec-head"><h2>Other {c['title'].lower()}</h2></div>
    <div class="catalogue">{"".join(card(r) for r in rel)}</div>
  </div>
</section>
"""
        html += f"""
<section>
  <div class="wrap">
    <div class="unit" data-cat="{u['cat']}">
      <div>
        {shot(u['img'], u['n'], ratio="16/10", eager=True)}
        <h2>About the {esc(u['n'])}</h2>
        <div class="prose">{body}</div>
        <dl class="specs">{specs}</dl>
        {safety_box()}
      </div>
      <aside class="unit-side">
        <span class="price">{u['price']}</span>
        <p>Delivered, set up and collected across Tipperary and the surrounding areas.</p>
        <a href="tel:{D.PHONE_TEL}" class="btn btn-accent">{ico("phone")}{D.PHONE_DISPLAY}</a>
        <a href="/contact/" class="btn btn-ink">Get a price</a>
        <a href="{wa_link()}" target="_blank" rel="noopener" class="btn btn-line">WhatsApp us</a>
      </aside>
    </div>
  </div>
</section>
{more}{contact_block()}{footer()}"""
        BUILT.append(write(f"hire/{u['slug']}/index.html", html))


# ----------------------------------------------------------- area pages -----
def build_areas():
    cards = "".join(
        f'<a class="area-card" href="/{a["slug"]}/" data-reveal><h3>{a["town"]}</h3>'
        f'<p>{a["county"]}. Also {esc(a["nearby"])}.</p></a>' for a in D.AREAS)
    html = head(f"Areas We Cover | Bouncy Castle Hire Tipperary | {D.NAME}",
                "The towns we deliver to across Tipperary, from Clonmel and Thurles to Nenagh, "
                "Cashel, Roscrea, Templemore, Cahir and Carrick on Suir.", "/areas/")
    html += page_hero("Areas we cover",
                      "Tipperary and the surrounding areas. If your town is not listed, ring us, "
                      "we may still reach you.", D.IMG_AREAS, [(None, "Areas")],
                      cat="marquee")
    html += f"""
<section>
  <div class="wrap">
    <div class="area-grid">{cards}</div>
    <div style="margin-top:44px">{booking_strip()}</div>
  </div>
</section>
{contact_block()}{footer()}"""
    BUILT.append(write("areas/index.html", html))

    for a in D.AREAS:
        copy = "".join(f"<p>{esc(p)}</p>" for p in a["copy"])
        others = "".join(f'<a class="area-card" href="/{o["slug"]}/"><h3>{o["town"]}</h3>'
                         f'<p>{o["county"]}</p></a>' for o in D.AREAS if o["slug"] != a["slug"])
        picks = "".join(card(u) for u in D.UNITS[:4])
        html = head(f"Bouncy Castle Hire {a['town']} | {D.NAME}",
                    f"Bouncy castle, combi castle and obstacle course hire in {a['town']}, "
                    f"{a['county']}. Delivered and set up, rain covers as standard. "
                    f"Call {D.PHONE_DISPLAY}.", f"/{a['slug']}/")
        html += page_hero(f"Bouncy castle hire in {a['town']}",
                          f"Castles, combis, obstacle courses, the disco dome and marquees, "
                          f"delivered and set up in {a['town']} and around.",
                          D.HERO_MAIN, [("/areas/", "Areas"), (None, a["town"])],
                          cat="castle")
        html += f"""
<section>
  <div class="wrap">
    <div class="prose">{copy}
      <h2>What we bring to {a['town']}</h2>
      <p>The full range travels: bouncy castles, combi castles with built in slides, obstacle
      courses from a 30ft block run up to the 55ft high adrenaline units, the disco dome, sumo
      suits, the gladiator challenge and marquees. Everything is delivered, set up and collected.</p>
    </div>
    {safety_box()}
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="sec-head"><h2>What people book in {a['town']}</h2></div>
    <div class="catalogue">{picks}</div>
    <div class="more-row"><a href="/combi-castles/" class="btn btn-ink">See the full range</a></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><h2>Other areas</h2></div>
    <div class="area-grid">{others}</div>
  </div>
</section>
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
<section>
  <div class="wrap">
    <div class="gallery">{gal}</div>
    <div class="note" style="margin-top:34px">More photos going up shortly. If you have a photo of
    one of our units at your event we would love to see it.</div>
  </div>
</section>
{contact_block()}{footer()}"""
    BUILT.append(write("gallery/index.html", html))

    html = head(f"FAQs | Bouncy Castle Hire Tipperary | {D.NAME}",
                "Common questions about bouncy castle and obstacle course hire in Tipperary: "
                "what we hire, areas covered, insurance and how to book.", "/faqs/")
    html += ld(faq_ld())
    html += page_hero("Common questions", "What we hire, where we go, insurance and how to book.",
                      D.SOON, [(None, "FAQs")], cat="combi")
    html += f"""
<section>
  <div class="wrap">
    <div class="faq">{faq_markup()}</div>
    {safety_box()}
  </div>
</section>
{contact_block()}{footer()}"""
    BUILT.append(write("faqs/index.html", html))

    html = head(f"Contact | Bouncy Castle Hire Tipperary | {D.NAME}",
                f"Call or WhatsApp {D.PHONE_DISPLAY}, or send an enquiry. Bouncy castle, "
                "obstacle course and marquee hire across Tipperary.", "/contact/")
    html += page_hero("Contact", f"Ring or WhatsApp {D.PHONE_DISPLAY}, or send an enquiry below.",
                      D.SOON, [(None, "Contact")], cat="obstacle")
    html += f"""
<section>
  <div class="wrap">{booking_strip()}</div>
</section>
{contact_block()}{footer()}"""
    BUILT.append(write("contact/index.html", html))

    terms = "".join(f"<li>{esc(s)}</li>" for s in D.SAFETY)
    html = head(f"Hire Terms | {D.NAME}",
                "Hire conditions for Bouncy Castle Man, including delivery and collection, "
                "supervision and insurance.", "/hire-terms/")
    html += page_hero("Hire terms", "The conditions that apply to every hire.",
                      D.SOON, [(None, "Hire terms")], cat="marquee")
    html += f"""
<section>
  <div class="wrap">
    <div class="prose">
      <h2 style="margin-top:0">Hire conditions</h2>
      <ul style="padding-left:20px;list-style:disc">{terms}</ul>
      <h2>Delivery and collection</h2>
      <p>{esc(D.DELIVERY_TERMS)}</p>
      <h2>Bookings</h2>
      <p>Bookings are confirmed by phone on {D.PHONE_DISPLAY}. Prices depend on the unit, the date
      and your area, and are given on enquiry.</p>
    </div>
    <div class="note" style="margin-top:30px"><strong>To be completed.</strong> Adam still needs to
    supply the wording for deposits, cancellations, the weather policy, damage and the public
    liability cover. Those sections are left out rather than guessed at, because they are
    contractual.</div>
  </div>
</section>
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
