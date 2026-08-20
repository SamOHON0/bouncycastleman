# -*- coding: utf-8 -*-
"""Page builders for Bouncy Castle Man. Run: python3 generate.py"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
import generate as G

esc, write, head, footer = G.esc, G.write, G.head, G.footer
page_hero, card, safety_box, contact_block = (
    G.page_hero, G.card, G.safety_box, G.contact_block)
shot, wave = G.shot, G.wave

BUILT = []


def ld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False)


def biz():
    o = {
        "@context": "https://schema.org", "@type": "EntertainmentBusiness", "name": D.NAME,
        "url": D.SITE + "/", "telephone": D.PHONE_INTL,
        "image": D.HERO_MAIN,
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
        f'<div class="faq-item"><button class="faq-q">{esc(q)}<span class="pm"></span></button>'
        f'<div class="faq-a"><p>{esc(a)}</p></div></div>' for q, a in D.FAQS)


def filters_bar():
    btns = ['<button class="filter-btn active" data-cat="all">All</button>']
    for c in D.CATEGORIES:
        btns.append(f'<button class="filter-btn" data-cat="{c["cat"]}">{c["title"]}</button>')
    return '<div class="filters" id="filters">%s</div>' % "".join(btns)


def all_cards():
    return "".join(card(u) for u in D.UNITS)


def booking_strip():
    opts = "".join(f"<option>{o}</option>" for o in D.AREA_OPTIONS)
    cats = "".join(f'<option>{c["title"]}</option>' for c in D.CATEGORIES)
    return f"""
<div class="wrap" id="book">
  <div class="strip">
    <div class="strip-inner">
      <div class="strip-cell">
        <h3>Check your delivery area</h3>
        <p>We cover Tipperary &amp; the surrounding areas.</p>
        <div class="strip-row">
          <select id="areaSel" aria-label="Select your area">
            <option value="">Select your area…</option>{opts}
            <option value="__other__">My area isn't listed</option>
          </select>
          <button class="btn btn-pink" id="areaBtn">Check</button>
        </div>
        <div id="areaOut"></div>
      </div>
      <div class="strip-cell">
        <h3>Plan your day</h3>
        <p>Pick a date and what you're after.</p>
        <div class="strip-row">
          <input type="date" id="bDate" aria-label="Date">
          <select id="bCat" aria-label="Category"><option value="">Everything</option>{cats}</select>
          <a class="btn btn-yellow" href="/contact/" id="quoteBtn">Get quote</a>
        </div>
      </div>
    </div>
  </div>
</div>
"""


# ---------------------------------------------------------------- home ------
def build_home():
    tiles = ""
    for c in D.CATEGORIES:
        tiles += f"""      <a class="cat {c['k']}" href="/{c['slug']}/" data-reveal>
        <span class="cat-img">{shot(c['hero'], c['title'])}</span>
        <h3>{c['title']}</h3><span>{esc(c['blurb'])}</span>
      </a>
"""
    total = len(D.UNITS)
    steps = "".join(
        f'<div class="step" data-reveal><div class="num">{i+1}</div><h3>{t}</h3><p>{esc(p)}</p></div>'
        for i, (t, p) in enumerate(D.STEPS))
    whys = "".join(
        f'<div class="wcard" data-reveal><div class="ico">{e}</div><h3>{esc(h)}</h3>'
        f'<p>{esc(p)}</p></div>' for e, h, p in D.WHY)

    def initials(name):
        return "".join(p[0] for p in name.replace(".", "").split()[:2]).upper()

    revs = "".join(
        f'<div class="review" data-reveal><div class="stars">★★★★★</div>'
        f'<p>“{esc(t)}”</p>'
        f'<div class="who"><div class="avatar">{initials(w)}</div>'
        f'<div>{w}<span>{loc}</span></div></div></div>' for t, w, loc in D.REVIEWS)
    gal = "".join(f'<a href="/gallery/" data-reveal><img src="{g}" alt="{D.NAME} hire" '
                  f'loading="lazy"></a>' for g in D.GALLERY[:8])

    html = head(
        "Bouncy Castle Hire Tipperary | Obstacle Courses, Combi Castles &amp; Marquees | " + D.NAME,
        "Bouncy castles, combi castles, obstacle courses, disco dome and marquees across "
        f"Clonmel, Thurles, Nenagh, Cashel and all of Tipperary. Call {D.PHONE_DISPLAY}.",
        "/", D.HERO_IMG)
    html += ld(biz()) + ld(faq_ld())
    html += f"""
<section class="hero" id="top">
  <div class="deco" aria-hidden="true">
    <span class="cloud c1"></span><span class="cloud c2"></span><span class="cloud c3"></span>
    <span class="balloon bb1"></span><span class="balloon bb2"></span>
    <span class="balloon bb3"></span><span class="balloon bb4"></span>
  </div>
  <div class="wrap">
    <div class="hero-grid">
      <div class="hero-copy">
        <span class="pill">Family run in Tipperary since {D.FOUNDED}</span>
        <h1>Tipperary's biggest selection for the <span class="hl">best day ever!</span></h1>
        <p>Bouncy castles, combi castles with slides, obstacle courses from 30ft to 55ft, the disco dome, sumo suits and marquees. Delivered and set up across Clonmel, Thurles, Nenagh, Cashel, Roscrea and the rest of Tipperary.</p>
        <div class="hero-actions">
          <a href="/contact/" class="btn btn-yellow">Get a quote</a>
          <a href="tel:{D.PHONE_TEL}" class="btn btn-white">Call {D.PHONE_DISPLAY}</a>
        </div>
        <div class="hero-trust">
          <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Over 20 years hiring</span>
          <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Fully insured, IIHF certified</span>
          <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Rain covers as standard</span>
        </div>
      </div>
      <div class="hero-photo">
        <div class="ph-main">{shot(D.HERO_IMG, D.HERO_IMG_NAME, eager=True)}</div>
        <div class="ph-badge">{D.HERO_IMG_NAME}<b>{D.HERO_IMG_TAG}</b></div>
      </div>
    </div>
  </div>
  {wave()}
</section>
{booking_strip()}

<section id="categories"><div class="wrap">
  <div class="sec-head"><span class="label">The range</span><h2>Browse by <em>category</em></h2>
    <p>Six kinds of hire, all delivered and set up across Tipperary.</p></div>
  <div class="cats">
{tiles}  </div>
</div></section>

<section id="catalogue" style="background:var(--surface)"><div class="wrap">
  <div class="sec-head"><span class="label">What we hire</span><h2>Every <em>unit</em> we run</h2>
    <p>Tap any unit for the sizes, the features and what it suits.</p></div>
  {filters_bar()}
  <div class="catalogue cropped" id="grid">
{all_cards()}  </div>
  <div class="browse-all"><a href="#catalogue" id="viewAll" class="btn btn-pink">View all {total} units &rarr;</a></div>
</div></section>

<section id="how"><div class="wrap">
  <div class="sec-head"><span class="label">Booking</span><h2>How it <em>works</em></h2></div>
  <div class="steps">{steps}</div>
  <div class="wrap" style="padding:0;max-width:820px;margin-top:34px">{safety_box()}</div>
</div></section>

<section id="why" style="background:var(--surface)"><div class="wrap">
  <div class="sec-head"><span class="label">Why us</span><h2>Why <em>Bouncy Castle Man</em></h2></div>
  <div class="whys">{whys}</div>
</div></section>

<section id="gallery"><div class="wrap">
  <div class="sec-head"><span class="label">Gallery</span><h2>The <em>gallery</em></h2>
    <p>A few of our castles and courses out on the road.</p></div>
  <div class="gallery">{gal}</div>
  <div class="cat-more"><a href="/gallery/" class="btn btn-yellow">See the full gallery</a></div>
</div></section>

<section id="reviews" style="background:var(--surface)"><div class="wrap">
  <div class="sec-head"><span class="label">Happy customers</span><h2>What locals <em>say</em></h2></div>
  <div class="reviews">{revs}</div>
</div></section>

<section id="faq"><div class="wrap">
  <div class="sec-head"><span class="label">FAQs</span><h2>Common <em>questions</em></h2></div>
  <div class="faq-wrap">{faq_markup()}</div>
  <div class="cat-more"><a href="/faqs/" class="btn btn-white">All FAQs</a></div>
</div></section>
{contact_block()}{footer()}"""
    BUILT.append(write("index.html", html))


# ------------------------------------------------------------ categories ----
def build_categories():
    for c in D.CATEGORIES:
        items = "".join(card(u) for u in D.UNITS if u["cat"] == c["cat"])
        n = len([u for u in D.UNITS if u["cat"] == c["cat"]])
        html = head(f"{c['title']} Hire Tipperary | {D.NAME}",
                    esc(c["intro"])[:158], f"/{c['slug']}/", c["hero"])
        html += page_hero(f"{c['title']} hire in Tipperary", esc(c["blurb"]), c["hero"],
                          [(None, c["title"])])
        html += f"""
<section style="padding-top:34px"><div class="wrap">
  <div class="prose" style="margin:0 0 34px"><p>{esc(c['intro'])}</p></div>
  <div class="catalogue">{items}</div>
  <div class="wrap" style="padding:0;max-width:820px">{safety_box()}</div>
  <div class="cat-more"><a href="tel:{D.PHONE_TEL}" class="btn btn-pink">Call {D.PHONE_DISPLAY} for a price</a></div>
</div></section>

<section style="background:var(--surface)"><div class="wrap">
  <div class="sec-head"><span class="label">Where we go</span><h2>Delivered across <em>Tipperary</em></h2>
    <p>All {n} of our {c['title'].lower()} travel to every town we cover.</p></div>
  <div class="area-grid">{''.join(
      f'<a class="area-card" href="/{a["slug"]}/"><h3>{a["town"]}</h3><p>{a["county"]}</p></a>'
      for a in D.AREAS)}</div>
</div></section>
{contact_block()}{footer()}"""
        BUILT.append(write(f"{c['slug']}/index.html", html))


# ----------------------------------------------------------- unit pages ----
def build_units():
    bycat = {c["cat"]: c for c in D.CATEGORIES}
    for u in D.UNITS:
        c = bycat[u["cat"]]
        specs = "".join(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in u["specs"])
        body = "".join(f"<p>{esc(p)}</p>" for p in u["body"])
        rel = [x for x in D.UNITS if x["cat"] == u["cat"] and x["slug"] != u["slug"]][:3]
        relhtml = "".join(card(r) for r in rel)
        prod = {"@context": "https://schema.org", "@type": "Product", "name": u["n"],
                "description": u["short"],
                "brand": {"@type": "Brand", "name": D.NAME},
                "offers": {"@type": "Offer", "availability": "https://schema.org/InStock",
                           "priceCurrency": "EUR", "url": f"{D.SITE}/hire/{u['slug']}/"}}
        if u["img"] != D.SOON:
            prod["image"] = u["img"]
        html = head(f"{esc(u['n'])} Hire Tipperary | {D.NAME}", esc(u["short"])[:158],
                    f"/hire/{u['slug']}/", u["img"])
        html += ld(prod)
        html += page_hero(esc(u["n"]), esc(u["short"]), u["img"],
                          [(f"/{c['slug']}/", c["title"]), (None, esc(u["n"]))])
        more = ""
        if relhtml:
            more = f"""
<section style="background:var(--surface)"><div class="wrap">
  <div class="sec-head"><span class="label">More like this</span><h2>Other <em>{c['title'].lower()}</em></h2></div>
  <div class="catalogue">{relhtml}</div>
</div></section>
"""
        html += f"""
<section style="padding-top:34px"><div class="wrap">
  <div class="unit-grid">
    <div class="unit-body">
      <div class="unit-shot">{shot(u['img'], u['n'])}</div>
      <h2 style="font-size:24px;margin:24px 0 12px">About the {esc(u['n'])}</h2>
      {body}
      <table class="specs"><tbody>{specs}</tbody></table>
      {safety_box()}
    </div>
    <aside class="unit-side">
      <span class="price">{u['price']}</span>
      <p style="font-size:14.5px;color:var(--ink-soft);font-weight:600">Delivered, set up and collected across Tipperary and the surrounding areas.</p>
      <a href="tel:{D.PHONE_TEL}" class="btn btn-yellow">Call {D.PHONE_DISPLAY}</a>
      <a href="/contact/" class="btn btn-pink">Send an enquiry</a>
      <a href="{G.wa_link()}" target="_blank" rel="noopener" class="btn btn-white">WhatsApp us</a>
    </aside>
  </div>
</div></section>
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
                      "Tipperary and the surrounding areas. If your town is not listed, give us "
                      "a call, we may still reach you.",
                      D.IMG_AREAS, [(None, "Areas")])
    html += f"""
<section style="padding-top:34px"><div class="wrap">
  <div class="area-grid">{cards}</div>
</div></section>
{booking_strip()}
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
                    f"Call {D.PHONE_DISPLAY}.",
                    f"/{a['slug']}/")
        html += page_hero(f"Bouncy castle hire in {a['town']}",
                          f"Castles, combis, obstacle courses, the disco dome and marquees, "
                          f"delivered and set up in {a['town']} and around.",
                          D.HERO_MAIN,
                          [("/areas/", "Areas"), (None, a["town"])])
        html += f"""
<section style="padding-top:34px"><div class="wrap">
  <div class="prose">{copy}
    <h2>What we bring to {a['town']}</h2>
    <p>The full range travels: bouncy castles, combi castles with built in slides, obstacle
    courses from a 30ft block run up to the 55ft high adrenaline units, the disco dome, sumo
    suits, the gladiator challenge and marquees. Everything is delivered, set up and collected.</p>
    {safety_box()}
  </div>
</div></section>

<section style="background:var(--surface)"><div class="wrap">
  <div class="sec-head"><span class="label">Popular in {a['town']}</span><h2>What people <em>book</em></h2></div>
  <div class="catalogue">{picks}</div>
  <div class="cat-more"><a href="/combi-castles/" class="btn btn-yellow">See the full range</a></div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="label">Nearby</span><h2>Other <em>areas</em></h2></div>
  <div class="area-grid">{others}</div>
</div></section>
{contact_block()}{footer()}"""
        BUILT.append(write(f"{a['slug']}/index.html", html))


# ------------------------------------------------ gallery, faqs, contact ----
def build_simple():
    gal = "".join(f'<a href="/contact/" data-reveal><img src="{g}" alt="{D.NAME} hire" '
                  f'loading="lazy"></a>' for g in D.GALLERY)
    html = head(f"Gallery | {D.NAME}",
                "Photos of our bouncy castles, combi castles, obstacle courses, disco dome and "
                "marquees out on the road across Tipperary.", "/gallery/")
    html += page_hero("Gallery", "Our castles and courses out on the road.",
                      D.HERO_MAIN, [(None, "Gallery")])
    html += f"""
<section style="padding-top:34px"><div class="wrap">
  <div class="gallery">{gal}</div>
  <div class="note" style="margin-top:26px;max-width:70ch">More photos going up shortly. If you
  have a photo of one of our units at your event we would love to see it.</div>
</div></section>
{contact_block()}{footer()}"""
    BUILT.append(write("gallery/index.html", html))

    html = head(f"FAQs | Bouncy Castle Hire Tipperary | {D.NAME}",
                "Common questions about bouncy castle and obstacle course hire in Tipperary: "
                "what we hire, areas covered, insurance and how to book.", "/faqs/")
    html += ld(faq_ld())
    html += page_hero("Common questions",
                      "What we hire, where we go, insurance and how to book.",
                      D.IMG_GREENGOLD, [(None, "FAQs")])
    html += f"""
<section style="padding-top:34px"><div class="wrap">
  <div class="faq-wrap">{faq_markup()}</div>
  <div class="wrap" style="padding:0;max-width:820px;margin-top:26px">{safety_box()}</div>
</div></section>
{contact_block()}{footer()}"""
    BUILT.append(write("faqs/index.html", html))

    html = head(f"Contact | Bouncy Castle Hire Tipperary | {D.NAME}",
                f"Call or WhatsApp {D.PHONE_DISPLAY}, or send an enquiry. Bouncy castle, "
                "obstacle course and marquee hire across Tipperary.", "/contact/")
    html += page_hero("Contact",
                      f"Ring or WhatsApp {D.PHONE_DISPLAY}, or send an enquiry below.",
                      D.IMG_CASTLE_C3, [(None, "Contact")])
    html += booking_strip() + contact_block() + footer()
    BUILT.append(write("contact/index.html", html))

    terms = "".join(f"<li>{esc(s)}</li>" for s in D.SAFETY)
    html = head(f"Hire Terms | {D.NAME}",
                "Hire conditions for Bouncy Castle Man, including delivery and collection, "
                "supervision and insurance.", "/hire-terms/")
    html += page_hero("Hire terms", "The conditions that apply to every hire.",
                      D.IMG_BANNER, [(None, "Hire terms")])
    html += f"""
<section style="padding-top:34px"><div class="wrap"><div class="prose">
  <h2>Hire conditions</h2>
  <ul>{terms}</ul>
  <h2>Delivery and collection</h2>
  <p>{esc(D.DELIVERY_TERMS)}</p>
  <h2>Bookings</h2>
  <p>Bookings are confirmed by phone on {D.PHONE_DISPLAY}. Prices depend on the unit, the date
  and your area, and are given on enquiry.</p>
  <div class="note"><strong>To be completed.</strong> Adam still needs to supply the wording for
  deposits, cancellations, the weather policy, damage and the public liability cover. Those
  sections are left out rather than guessed at, because they are contractual.</div>
</div></div></section>
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
    for p in BUILT:
        print("  " + p)


if __name__ == "__main__":
    G.build_assets()
    main()
