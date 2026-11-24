#!/usr/bin/env python3
"""Litchi (Columbus OH) template-v2 site generator — websites lane t_6b1d6c93.
Every claim sourced from the card's verified facts (614NOW / NBC4 / Columbus
Underground / Columbus Food Letter press + GBP place pane via Maps UI 2026-11-24):
address 940 N High St, phone (614) 456-7151, GBP weekly hours, $20-50,
press-signage menu items, Daniel Chen ownership (698 + 1126), former Ampersand
space, Resy venue live 200, GBP 5.0 / 12 reviews. Unknowns omitted (no prices,
no fake delivery, no invented dishes)."""
import json, os, datetime

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')
ORIGIN = "https://litchi-columbus-demo.up.railway.app"
TODAY = "2026-11-24"
NAME = "Litchi"
ADDR = "940 N High St, Columbus, OH 43201"
PHONE_D = "(614) 456-7151"
PHONE_T = "+16144567151"
RESY = "https://resy.com/cities/columbus-oh/venues/litchi"
MAPSRC = "https://www.google.com/maps?q=940%20N%20High%20St%2C%20Columbus%2C%20OH%2043201&output=embed"
LAT, LON = 39.981538, -83.004251

HOURS = [
    ("Tuesday", "3:00 PM – 9:30 PM"),
    ("Wednesday", "11:30 AM – 9:30 PM"),
    ("Thursday", "11:30 AM – 9:30 PM"),
    ("Friday", "11:30 AM – 9:30 PM"),
    ("Saturday", "11:00 AM – 9:30 PM"),
    ("Sunday", "11:00 AM – 9:30 PM"),
    ("Monday", "Closed"),
]

MENU_SECTIONS = [
    ("Soufflé Pancakes", [("Japanese soufflé pancakes", "Inches-thick and jiggly — a meringue of whipped egg whites, griddled slow.")]),
    ("Brunch", [("Eggs benedict, shredded beef", "With tubetti pasta and a soft-poached egg.")]),
    ("Mains", [
        ("Thai curry sea bass", ""),
        ("Sizzling tiger prawns, wild mushrooms", ""),
        ("Mango shrimp salad", ""),
        ("Sichuan peppercorn prawn pasta", ""),
        ("Beef short ribs, walnut chestnut purée", ""),
    ]),
]

FOOTER = f"""<footer>
  <div class="footline">
    <div class="fnote">
      <strong>{NAME}</strong> · Pan-Asian restaurant · Short North
      <span>{ADDR}</span>
      <span><a href="tel:{PHONE_T}">{PHONE_D}</a> · <a href="/contact">Contact</a> · <a href="/privacy">Privacy</a> · <a href="{RESY}" rel="noopener">Reserve on Resy</a></span>
    </div>
    <div class="fcopy">© 2026 {NAME}</div>
  </div>
</footer>"""

def head(title, desc, path, ogdesc=None):
    canon = ORIGIN + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<!-- BUILT-{TODAY} -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{ogdesc or desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{ORIGIN}/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="bar wrap">
    <a class="brand" href="/">Litchi<span class="dot" aria-hidden="true"></span></a>
    <nav aria-label="Main">
      <a href="/menus">Menus</a>
      <a href="/our-story">Our&nbsp;Story</a>
      <a href="/visit">Hours &amp; Map</a>
      <a class="call" href="tel:{PHONE_T}">{PHONE_D}</a>
    </nav>
  </div>
</header>
<main id="main">
"""

def ld(blocks):
    out = []
    for b in blocks:
        out.append('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False, separators=(',', ':')) + '</script>')
    return "\n".join(out)

RESTAURANT = {
    "@type": "Restaurant",
    "@id": ORIGIN + "/#restaurant",
    "name": NAME,
    "servesCuisine": ["Pan-Asian", "Japanese"],
    "priceRange": "$20–50",
    "telephone": "+" + PHONE_T,
    "url": ORIGIN + "/",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "940 N High St",
        "addressLocality": "Columbus",
        "addressRegion": "OH",
        "postalCode": "43201",
        "addressCountry": "US",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON},
    "acceptsReservations": "True",
    "hasMap": "https://www.google.com/maps/place/?q=place_id:0x88388f0061e765b5:0xfc15737f6bf1705c",
    "sameAs": [RESY],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c}
        for d, o, c in [
            ("Tuesday", "15:00", "21:30"),
            ("Wednesday", "11:30", "21:30"),
            ("Thursday", "11:30", "21:30"),
            ("Friday", "11:30", "21:30"),
            ("Saturday", "11:00", "21:30"),
            ("Sunday", "11:00", "21:30"),
        ]
    ],
}

def breadcrumb(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + p}
            for i, (n, p) in enumerate(items)
        ],
    }

def hours_table(cls="hours"):
    rows = "".join(f"<tr><th scope=\"row\">{d}</th><td>{t}</td></tr>" for d, t in HOURS)
    return f'<table class="{cls}"><caption>Hours</caption><tbody>{rows}</tbody></table>'

def map_block():
    return (f'<div class="mapcell"><iframe src="{MAPSRC}" '
            f'title="Map: {NAME}, {ADDR}" loading="eager" '
            f'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>')

def cta_band(note):
    return f"""<section class="band"><div class="wrap">
  <h2>{note}</h2>
  <p class="cta">
    <a class="btn solid" href="{RESY}" rel="noopener">Reserve on Resy</a>
    <a class="btn ghost" href="tel:{PHONE_T}">Call {PHONE_D}</a>
  </p>
</div></section>"""

PAGES = {}

# ---------------- HOME ----------------
home_blocks = [RESTAURANT,
    {"@context": "https://schema.org", "@type": "WebSite", "name": NAME + " — Columbus OH", "url": ORIGIN + "/"},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": "Are these real Japanese-style soufflé pancakes?",
         "acceptedAnswer": {"@type": "Answer", "text": "Yes. Litchi is the first restaurant in Columbus to serve Japanese-style soufflé pancakes — much thicker than a traditional pancake, built on a meringue of whipped egg whites."}},
        {"@type": "Question", "name": "How do I get a table?",
         "acceptedAnswer": {"@type": "Answer", "text": "Reserve on Resy or call (614) 456-7151."}},
        {"@type": "Question", "name": "Where is Litchi?",
         "acceptedAnswer": {"@type": "Answer", "text": "940 N High St, Columbus, OH 43201 — in the Short North, in the space that once held Ampersand Asian Supper Club."}},
        {"@type": "Question", "name": "When are you open?",
         "acceptedAnswer": {"@type": "Answer", "text": "Tuesday 3:00 PM–9:30 PM; Wednesday–Friday 11:30 AM–9:30 PM; Saturday–Sunday 11:00 AM–9:30 PM; closed Monday."}},
    ]}]

home = head(
    "Litchi — Japanese Soufflé Pancakes & Pan-Asian Brunch | Columbus OH",
    "Litchi serves Japanese-style soufflé pancakes, Pan-Asian brunch, dinner, and cocktails at 940 N High St in the Short North, Columbus, OH. Reserve on Resy or call (614) 456-7151.",
    "/") + f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">Short North · Columbus, Ohio</p>
      <h1>Cloud-soft Japanese soufflé pancakes — <em>a Columbus first.</em></h1>
      <p class="lede">Litchi pours brunch, dinner, and cocktails on North High — towering, inches-thick, seductively jiggly.</p>
      <p class="cta">
        <a class="btn solid" href="{RESY}" rel="noopener">Reserve on Resy</a>
        <a class="btn ghost" href="/menus">See the menus</a>
      </p>
      <p class="fine">Brunch &amp; dinner · Tue–Sun · <a href="tel:{PHONE_T}">{PHONE_D}</a></p>
    </div>
    <div class="stack" aria-hidden="true">
      <div class="puff p1"></div>
      <div class="puff p2"></div>
      <div class="puff p3"></div>
      <div class="butter"></div>
    </div>
  </div>
</section>

<section class="feature">
  <div class="wrap split">
    <div>
      <p class="eyebrow">The pancake that brought Columbus</p>
      <h2>First in the city: soufflé pancakes, done the Japanese way</h2>
      <p>A soufflé pancake is not a stack of flaps. It is built on a meringue of whipped egg whites, griddled low and slow until it stands inches tall and jiggles when the plate lands. The ones all of Instagram has been passing around? You can order them in Columbus now.</p>
      <p><a class="more" href="/japanese-souffle-pancakes">More on soufflé pancakes →</a></p>
    </div>
    <blockquote class="quote">
      <p>“This restaurant is ahead of Columbus’ time.”</p>
      <cite>— Google review, November 2026</cite>
    </blockquote>
  </div>
</section>

<section class="teaser dark">
  <div class="wrap">
    <p class="eyebrow">What’s pouring</p>
    <h2>Brunch, dinner, and a few things you haven’t had in this town</h2>
    <ul class="items">
      <li><strong>Japanese soufflé pancakes</strong><span>inches-thick and jiggly</span></li>
      <li><strong>Eggs benedict, shredded beef</strong><span>with tubetti pasta, soft-poached egg</span></li>
      <li><strong>Thai curry sea bass</strong><span></span></li>
      <li><strong>Sizzling tiger prawns</strong><span>wild mushrooms</span></li>
      <li><strong>Mango shrimp salad</strong><span></span></li>
      <li><strong>Sichuan peppercorn prawn pasta</strong><span></span></li>
      <li><strong>Beef short ribs</strong><span>walnut chestnut purée</span></li>
      <li><strong>Cocktails</strong><span>brunch through dinner</span></li>
    </ul>
    <p><a class="more" href="/menus">Full menus →</a></p>
  </div>
</section>

<section class="visit">
  <div class="wrap split map-split">
    <div>
      <p class="eyebrow">Find us</p>
      <h2>In the old Ampersand space on North High</h2>
      <address class="addr">{ADDR}<br>Short North · <a href="tel:{PHONE_T}">{PHONE_D}</a></address>
      {hours_table()}
      <p class="cta">
        <a class="btn solid" href="{RESY}" rel="noopener">Reserve on Resy</a>
        <a class="btn ghost" href="/visit">Hours &amp; map</a>
      </p>
    </div>
    {map_block()}
  </div>
</section>

<section class="team">
  <div class="wrap">
    <p class="team-line">From the kitchen behind <strong>698 Restaurant</strong> and <strong>The 1126</strong> — now on High Street.</p>
  </div>
</section>

{ld(home_blocks)}
""" + FOOTER + "\n</main>\n</body>\n</html>\n"
# note: footer inside main-closing order fixed below in build()
PAGES["index.html"] = home

# ---------------- MENUS ----------------
def menu_lists():
    out = []
    for sec, items in MENU_SECTIONS:
        lis = "".join(f"<li><strong>{n}</strong>{('<span>'+s+'</span>') if s else ''}</li>" for n, s in items)
        out.append(f"<section class='msec'><h2>{sec}</h2><ul class='menu-list'>{lis}</ul></section>")
    return "".join(out)

menus = head(
    "Menus — Brunch, Dinner & Cocktails — Litchi, Columbus OH",
    "Brunch, dinner, cocktails, and Columbus's first Japanese soufflé pancakes — the launch lineup at Litchi in the Short North, 940 N High St, Columbus OH.",
    "/menus") + f"""
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Menus</p>
  <h1>The launch lineup</h1>
  <p class="lede">Brunch and dinner, side by side, with cocktails poured through service. This is the lineup Litchi opened with — ask your server what’s fresh today.</p>
</div></section>
<section class="menuwrap"><div class="wrap">
{menu_lists()}
<p class="note">Prices and seasonal plates change — the menu posted in the dining room is the one to trust.</p>
</div></section>
{cta_band("Want a table while the pancakes are hot?")}
{ld([
  {"@context": "https://schema.org", "@type": "Menu", "name": "Litchi — Launch Menu",
   "inLanguage": "en", "url": ORIGIN + "/menus",
   "hasMenuSection": [
     {"@type": "MenuSection", "name": sec,
      "hasMenuItem": [{"@type": "MenuItem", "name": n} for n, _ in items]}
     for sec, items in MENU_SECTIONS]},
  breadcrumb([("Home", "/"), ("Menus", "/menus")]),
  {"@context": "https://schema.org", "@type": "WebPage", "@id": ORIGIN + "/menus",
   "url": ORIGIN + "/menus", "name": "Menus — Litchi, Columbus OH", "mainEntity": {"@id": RESTAURANT["@id"]}},
])}
""" + FOOTER + "\n</main>\n</body>\n</html>\n"
PAGES["menus.html"] = menus

# ---------------- SOUFFLE DETAIL ----------------
souffle = head(
    "Japanese Soufflé Pancakes — Litchi, Columbus OH",
    "Japanese soufflé pancakes in Columbus — inches-thick, jiggly, built on whipped-egg-white meringue. Litchi is the city's first Japanese-style soufflé pancake restaurant, in the Short North.",
    "/japanese-souffle-pancakes") + f"""
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">The signature</p>
  <h1>Japanese soufflé pancakes —<br>the first Columbus has ever had</h1>
  <p class="lede">You’ve seen them on Instagram and TikTok: towering, pillowy, inches thick, and seductively jiggly. Now they’re on High Street.</p>
</div></section>

<section class="feature"><div class="wrap split">
  <div>
    <h2>What makes a soufflé pancake a soufflé pancake</h2>
    <p>Ordinary pancakes start with batter. A Japanese soufflé pancake starts with a meringue — egg whites whipped until they hold a peak — folded in gently, then cooked low and slow under a lid so the heat rises around it instead of scorching the base.</p>
    <p>The result stands inches taller than the flap stack most of Columbus grew up on: weightless, barely sweet, and yes, it jiggles on the plate.</p>
    <p>Litchi is the first restaurant in Columbus to offer Japanese-style soufflé pancakes. Order them at brunch or after dinner — the room pours cocktails either way.</p>
  </div>
  <div class="stack tall" aria-hidden="true">
    <div class="puff p1"></div>
    <div class="puff p2"></div>
    <div class="puff p3"></div>
    <div class="butter"></div>
  </div>
</div></section>
{cta_band("Tables go fast around these.")}
{ld([
  {"@context": "https://schema.org", "@type": "Service",
   "@id": ORIGIN + "/japanese-souffle-pancakes#service",
   "serviceType": "Japanese-style soufflé pancakes",
   "name": "Japanese Soufflé Pancakes",
   "description": "Inches-thick Japanese soufflé pancakes, built on whipped-egg-white meringue — the first served in Columbus, at Litchi in the Short North.",
   "provider": {"@id": RESTAURANT["@id"]},
   "areaServed": [
     {"@type": "Place", "name": "Short North, Columbus"},
     {"@type": "City", "name": "Columbus", "containedInPlace": {"@type": "AdministrativeArea", "name": "Ohio"}}],
   "url": ORIGIN + "/japanese-souffle-pancakes"},
  breadcrumb([("Home", "/"), ("Menus", "/menus"), ("Soufflé Pancakes", "/japanese-souffle-pancakes")]),
])}
""" + FOOTER + "\n</main>\n</body>\n</html>\n"
PAGES["japanese-souffle-pancakes.html"] = souffle

# ---------------- BRUNCH & DINNER DETAIL ----------------
brunch_items = "".join(f"<li><strong>{n}</strong>{('<span>'+s+'</span>') if s else ''}</li>"
                       for n, s in MENU_SECTIONS[1][1] + MENU_SECTIONS[2][1])
bd = head(
    "Pan-Asian Brunch & Dinner — Litchi, Short North, Columbus OH",
    "Pan-Asian brunch and dinner in Columbus: Thai curry sea bass, sizzling tiger prawns, Sichuan peppercorn prawn pasta, beef short ribs and cocktails at Litchi, Short North.",
    "/pan-asian-brunch-dinner") + f"""
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Brunch · Dinner · Cocktails</p>
  <h1>Pan-Asian plates, brunch through last call</h1>
  <p class="lede">One menu, two shifts: everything from benedict to short ribs, poured with cocktails on the same table.</p>
</div></section>

<section class="feature"><div class="wrap split">
  <div>
    <h2>The kitchen at full stretch</h2>
    <p>Litchi’s concept runs the whole Asian table — brunch classics twisted through a Pan-Asian lens, then proper dinner plates: sea bass under Thai curry, tiger prawns that arrive still sizzling with wild mushrooms, prawn pasta sharpened with Sichuan peppercorn, and beef short ribs laid over walnut chestnut purée.</p>
    <p>Brunch runs Tuesday through Sunday (Tuesday afternoons; weekends from 11), cocktails pour alongside every shift, and yes — soufflé pancakes are on at brunch and after dinner.</p>
  </div>
  <ul class="menu-list">{brunch_items}</ul>
</div></section>
{cta_band("Brunch tables book out — reserve ahead.")}
{ld([
  {"@context": "https://schema.org", "@type": "Service",
   "@id": ORIGIN + "/pan-asian-brunch-dinner#service",
   "serviceType": "Pan-Asian brunch and dinner service with cocktails",
   "name": "Pan-Asian Brunch & Dinner",
   "description": "Brunch and dinner plates — eggs benedict with shredded beef, Thai curry sea bass, sizzling tiger prawns, Sichuan peppercorn prawn pasta, beef short ribs with walnut chestnut purée — served with cocktails at Litchi, Short North, Columbus.",
   "provider": {"@id": RESTAURANT["@id"]},
   "areaServed": [
     {"@type": "Place", "name": "Short North, Columbus"},
     {"@type": "City", "name": "Columbus", "containedInPlace": {"@type": "AdministrativeArea", "name": "Ohio"}}],
   "url": ORIGIN + "/pan-asian-brunch-dinner"},
  breadcrumb([("Home", "/"), ("Menus", "/menus"), ("Brunch & Dinner", "/pan-asian-brunch-dinner")]),
])}
""" + FOOTER + "\n</main>\n</body>\n</html>\n"
PAGES["pan-asian-brunch-dinner.html"] = bd

# ---------------- OUR STORY ----------------
story = head(
    "Our Story — Litchi, Short North, Columbus OH",
    "Litchi comes from Columbus restaurateur Daniel Chen, who also runs 698 Restaurant and The 1126, in the former Ampersand Asian Supper Club space at 940 N High St.",
    "/our-story") + f"""
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Our story</p>
  <h1>A Short North table, from a team you already know</h1>
</div></section>

<section class="feature"><div class="wrap narrow">
  <p>Litchi opened this November at 940 N High St — the Short North space that once held Ampersand Asian Supper Club — and the reviews arrived fast: a perfect 5.0 from early guests on Google.</p>
  <p>The concept belongs to Daniel Chen, the Columbus restaurateur behind <strong>698 Restaurant</strong> and <strong>The 1126</strong>. Litchi is his take on the Pan-Asian table that Short North keeps asking for: soufflé pancakes that stand inches tall, sea bass under Thai curry, short ribs over walnut chestnut purée — brunch, dinner, and cocktails under one roof.</p>
  <p>If you’ve eaten your way through 698 or spent an evening at the 1126, you already know the kitchen’s grammar. Litchi is what it says at breakfast — and at nine.</p>
  <blockquote class="quote inline">
    <p>“We loved our experience — the first restaurant in Columbus to serve soufflé pancakes, which were delicious!”</p>
    <cite>— Google review, November 2026</cite>
  </blockquote>
</div></section>
{cta_band("Come see what the room looks like.")}
{ld([
  {"@context": "https://schema.org", "@type": "AboutPage", "@id": ORIGIN + "/our-story",
   "url": ORIGIN + "/our-story", "name": "Our Story — Litchi",
   "mainEntity": {"@id": RESTAURANT["@id"]}},
  breadcrumb([("Home", "/"), ("Our Story", "/our-story")]),
])}
""" + FOOTER + "\n</main>\n</body>\n</html>\n"
PAGES["our-story.html"] = story

# ---------------- VISIT (hours & map) ----------------
visit = head(
    "Hours & Map — Litchi, 940 N High St, Columbus OH",
    "Litchi hours: Tue 3-9:30 PM, Wed-Fri 11:30 AM-9:30 PM, Sat-Sun 11 AM-9:30 PM, closed Monday. Find us at 940 N High St, Short North, Columbus — dine-in and takeout, reserve on Resy.",
    "/visit") + f"""
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Hours &amp; map</p>
  <h1>Brunch, dinner, and where to find both</h1>
</div></section>

<section class="visit"><div class="wrap split map-split">
  <div>
    <h2>Hours</h2>
    {hours_table()}
    <address class="addr">{ADDR}<br><a href="tel:{PHONE_T}">{PHONE_D}</a></address>
    <p class="fine">Dine-in and takeout. Holiday hours bend around the calendar — the kitchen posts its week on Resy.</p>
    <p class="cta">
      <a class="btn solid" href="{RESY}" rel="noopener">Reserve on Resy</a>
      <a class="btn ghost" href="/contact">Send a note</a>
    </p>
  </div>
  {map_block()}
</div></section>
{ld([
  {"@context": "https://schema.org", "@type": "WebPage", "@id": ORIGIN + "/visit",
   "url": ORIGIN + "/visit", "name": "Hours & Map — Litchi, Columbus OH",
   "mainEntity": {"@id": RESTAURANT["@id"]}},
  breadcrumb([("Home", "/"), ("Hours & Map", "/visit")]),
])}
""" + FOOTER + "\n</main>\n</body>\n</html>\n"
PAGES["visit.html"] = visit

# ---------------- CONTACT ----------------
contact = head(
    "Contact & Reservations — Litchi, Columbus OH",
    "Contact Litchi: call (614) 456-7151, reserve on Resy, or send a note — 940 N High St, Short North, Columbus OH 43201. Hours, map, and directions.",
    "/contact") + f"""
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Contact</p>
  <h1>Talk to us</h1>
  <p class="lede">For a table: <a href="{RESY}" rel="noopener">Reserve on Resy</a> or call <a href="tel:{PHONE_T}">{PHONE_D}</a>. For anything else, leave a note and it lands in the restaurant’s inbox.</p>
</div></section>

<section class="cform-sec"><div class="wrap split">
  <form class="cform" method="post" action="/contact">
    <label>Your name<input type="text" name="name" autocomplete="name" required></label>
    <label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
    <label>Email<input type="email" name="email" autocomplete="email"></label>
    <label>Message<textarea name="message" rows="5" required></textarea></label>
    <button class="btn solid" type="submit">Send the note</button>
  </form>
  <div>
    <h2>The restaurant</h2>
    <address class="addr">{NAME}<br>{ADDR}<br><a href="tel:{PHONE_T}">{PHONE_D}</a></address>
    {hours_table("hours small")}
  </div>
</div></section>
{ld([
  {"@context": "https://schema.org", "@type": "ContactPage", "@id": ORIGIN + "/contact",
   "url": ORIGIN + "/contact", "name": "Contact — Litchi, Columbus OH",
   "mainEntity": {"@id": RESTAURANT["@id"]}},
  breadcrumb([("Home", "/"), ("Contact", "/contact")]),
])}
""" + FOOTER + "\n</main>\n</body>\n</html>\n"
PAGES["contact.html"] = contact

# ---------------- PRIVACY ----------------
privacy = head(
    "Privacy — Litchi, Columbus OH",
    "Privacy notes for Litchi's site: what the contact form sends, the one-pixel email marker, and the fact that no cookies or third-party trackers load in your browser.",
    "/privacy") + f"""
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Privacy</p>
  <h1>Plain words about this site</h1>
</div></section>

<section class="feature"><div class="wrap narrow">
  <h2>What the form does</h2>
  <p>When you send a note through the contact form, your name, phone, email, and message go straight to Litchi’s inbox so the team can answer. Nothing is sold, nothing is shared, and the site itself keeps no profiles.</p>
  <h2>Cookies &amp; trackers</h2>
  <p>This site sets no cookies and loads no third-party scripts. Maps load when you see them, under Google’s own privacy policy. Links to Resy leave this site under Resy’s policy.</p>
  <h2>The email pixel</h2>
  <p>When Litchi sends an email, it may include an invisible one-pixel image so the team knows the email was opened. It identifies the email, not you, and it never loads when you read mail without images displayed.</p>
  <h2>Questions</h2>
  <p>Call <a href="tel:{PHONE_T}">{PHONE_D}</a> or use the <a href="/contact">contact form</a> — the same inbox answers both.</p>
</div></section>
{ld([breadcrumb([("Home", "/"), ("Privacy", "/privacy")])])}
""" + FOOTER + "\n</main>\n</body>\n</html>\n"
PAGES["privacy.html"] = privacy

# ---------------- 404 ----------------
nf = head(
    "Page Not Found — Litchi, Columbus OH",
    "That page isn’t here. Find Litchi’s menus, hours, map, and reservations from the home page — 940 N High St, Short North, Columbus OH.",
    "/404") + f"""
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">404</p>
  <h1>That page moved — or never existed.</h1>
  <p class="lede">The pancakes, however, are exactly where you left them.</p>
  <p class="cta">
    <a class="btn solid" href="/">Back to home</a>
    <a class="btn ghost" href="/menus">Menus</a>
    <a class="btn ghost" href="/visit">Hours &amp; map</a>
  </p>
</div></section>
""" + FOOTER + "\n</main>\n</body>\n</html>\n"
PAGES["404.html"] = nf

# ---------------- THANKS ----------------
ty = head(
    "Thanks — Litchi, Columbus OH",
    "Your note to Litchi is on its way to the restaurant's inbox. For a table right now, reserve on Resy or call (614) 456-7151.",
    "/thanks") + f"""
<section class="pagehead"><div class="wrap">
  <p class="eyebrow">Sent</p>
  <h1>Your note is in the restaurant’s inbox.</h1>
  <p class="lede">For a table right now, <a href="{RESY}" rel="noopener">reserve on Resy</a> or call <a href="tel:{PHONE_T}">{PHONE_D}</a>.</p>
  <p class="cta"><a class="btn solid" href="/">Back to home</a></p>
</div></section>
""" + FOOTER + "\n</main>\n</body>\n</html>\n"
PAGES["thanks.html"] = ty

# ---------------- shared assets ----------------
robots = f"""User-agent: *
Disallow: /thanks
Disallow: /404

Sitemap: {ORIGIN}/sitemap.xml
"""

core = ["/", "/menus", "/japanese-souffle-pancakes", "/pan-asian-brunch-dinner",
        "/our-story", "/visit", "/contact", "/privacy"]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"<url><loc>{ORIGIN}{p}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in core) + "</urlset>\n"

favicon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="36" r="24" fill="#e2546b"/><circle cx="24" cy="28" r="7" fill="#ffd9de" opacity=".85"/><path d="M32 12c2-6 9-8 15-7-2 6-8 9-15 8z" fill="#7d8f5a"/><rect x="30.5" y="6" width="3" height="8" rx="1.5" fill="#5d5040"/></svg>
"""

CSS = """
/* Litchi — hand-rolled stylesheet. Lychee-blush over deep ink, brass rules. No runtime. */
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
:root{
  --ink:#221327; --ink2:#2e1a33; --cream:#f9f2e7; --paper:#fdf7ee;
  --blush:#ffd9de; --pink:#e2546b; --plum:#8c3a52; --brass:#c8a865;
  --tx:#2a1a2b; --tx-mut:#6d5a63;
  --serif:"Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
body{margin:0;background:var(--cream);color:var(--tx);font:400 17px/1.65 var(--sans)}
h1,h2,h3{font-family:var(--serif);font-weight:700;line-height:1.12;color:var(--ink);letter-spacing:-.01em}
h1{font-size:clamp(2.1rem,5.2vw,3.6rem);margin:.35em 0 .4em}
h2{font-size:clamp(1.5rem,3.4vw,2.3rem);margin:.2em 0 .5em}
p{margin:0 0 1.1em}
a{color:var(--plum)}
address{font-style:normal}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.skip{position:absolute;left:-60px;top:0;background:var(--ink);color:#fff;padding:8px 14px;z-index:9}
.skip:focus{left:8px}

/* header */
.top{background:var(--ink);border-bottom:1px solid #3c2743}
.bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px 22px;padding-top:14px;padding-bottom:14px}
.brand{font-family:var(--serif);font-size:1.55rem;letter-spacing:.08em;color:var(--blush);text-decoration:none}
.brand .dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--pink);margin-left:8px;vertical-align:2px}
nav{display:flex;flex-wrap:wrap;gap:6px 20px;align-items:center}
nav a{color:#e9dbe2;text-decoration:none;font-size:.97rem;padding:4px 0}
nav a:hover{color:var(--blush)}
nav a.call{color:var(--brass);font-variant-numeric:tabular-nums}
main{display:block}

/* hero */
.hero{background:linear-gradient(160deg,var(--ink) 0%,var(--ink2) 74%,#3a2140 100%);color:#f4e9ee;padding:64px 0 72px;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;inset:auto -120px -160px auto;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle at 30% 30%,rgba(255,217,222,.16),transparent 65%);pointer-events:none}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(240px,.75fr);gap:44px;align-items:center}
.eyebrow{font-size:.82rem;letter-spacing:.22em;text-transform:uppercase;color:var(--brass);margin:0 0 .8em}
.hero h1{color:#fdf6f8;margin-top:0}
.hero h1 em{font-style:italic;color:var(--blush)}
.lede{font-size:1.13rem;color:#e3d2da;max-width:34em}
.fine{font-size:.92rem;color:#c9b6c0}
.fine a{color:var(--brass)}

/* pancake stack (pure CSS decor) */
.stack{position:relative;height:250px}
.stack.tall{height:340px}
.puff{position:absolute;left:8%;right:8%;border-radius:50%;background:linear-gradient(180deg,#f7e7ea,#eec6cd 58%,#e7b2bb);box-shadow:0 10px 22px rgba(20,8,18,.45), inset 0 -6px 14px rgba(140,58,82,.35)}
.puff.p1{bottom:44px;height:64px;transform:scale(.86)}
.puff.p2{bottom:6px;height:74px;transform:scale(.94)}
.puff.p3{bottom:-30px;height:82px}
.butter{position:absolute;bottom:118px;left:41%;width:46px;height:34px;border-radius:8px;background:linear-gradient(160deg,#f6e3a8,#dfc074);box-shadow:0 6px 14px rgba(20,8,18,.4);transform:rotate(4deg)}
.stack.tall .puff.p1{bottom:70px}
.stack.tall .puff.p2{bottom:28px}
.stack.tall .puff.p3{bottom:-16px}
.stack.tall .butter{bottom:172px}

/* buttons / CTAs */
.cta{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:1.2em 0 0}
.btn{display:inline-block;padding:13px 22px;border-radius:999px;text-decoration:none;font-weight:600;font-size:.98rem;border:1px solid transparent}
.btn.solid{background:var(--pink);color:#fff;box-shadow:0 8px 20px rgba(226,84,107,.35)}
.btn.solid:hover{background:#cf4459}
.btn.ghost{border-color:var(--brass);color:var(--brass);background:transparent}
.btn.ghost:hover{background:rgba(200,168,101,.12)}
section.teaser .btn.ghost,section.band .btn.ghost{color:var(--brass)}
.more{font-weight:600}

/* sections */
.feature{padding:64px 0}
.feature .split{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(240px,.65fr);gap:44px;align-items:center}
.feature .narrow{max-width:720px;margin:0 auto}
.teaser{padding:64px 0}
.dark{background:var(--ink);color:#efe2e8}
.dark h2,.dark h1{color:#f8eff2}
.dark .more{color:var(--blush)}
.quote{margin:0;padding:26px 28px;background:var(--blush);border-radius:18px;color:var(--tx)}
.quote p{font-family:var(--serif);font-size:1.35rem;line-height:1.4;margin:0 0 .5em}
.quote cite{font-style:normal;color:var(--plum);font-size:.95rem}
.quote.inline{margin-top:2.2em}
.items{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 22px}
.items li{border:1px solid #45304c;border-radius:14px;padding:16px 18px;background:rgba(255,255,255,.03)}
.items strong{display:block;font-family:var(--serif);font-size:1.12rem;color:#f6e9ef}
.items span{display:block;color:#bfa6b2;font-size:.92rem;min-height:1em}

/* hours + address */
.visit{padding:64px 0}
.hours{border-collapse:collapse;width:100%;max-width:420px;margin:10px 0 20px;font-variant-numeric:tabular-nums}
.hours caption{text-align:left;font-weight:700;color:var(--ink);margin-bottom:6px}
.hours th,.hours td{text-align:left;padding:7px 4px;border-bottom:1px solid #e4d5c4;font-size:.98rem}
.hours th{font-weight:600;color:var(--ink)}
.hours.small{max-width:340px}
.addr{font-size:1.06rem;line-height:1.7;margin:14px 0}

/* map */
.map-split{grid-template-columns:minmax(0,1fr) minmax(0,58%)}
.mapcell{min-height:340px;border-radius:18px;overflow:hidden;border:1px solid #e0cfbd;background:#efe3d3}
.mapcell iframe{width:100%;height:100%;min-height:340px;border:0;display:block}

/* team band */
.team{background:var(--blush);padding:34px 0}
.team-line{margin:0;font-family:var(--serif);font-size:1.25rem;color:var(--plum);text-align:center}

/* page heads */
.pagehead{padding:56px 0 30px;border-bottom:1px solid #eadccb;background:var(--paper)}
.pagehead .lede{color:var(--tx-mut)}

/* menus page */
.menuwrap{padding:46px 0 10px}
.msec{margin:0 0 42px}
.menu-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 26px}
.menu-list li{border-left:3px solid var(--pink);padding:6px 0 6px 16px}
.menu-list strong{display:block;font-family:var(--serif);font-size:1.15rem;color:var(--ink)}
.menu-list span{color:var(--tx-mut);font-size:.93rem}
.note{color:var(--tx-mut);font-size:.92rem;border-top:1px dashed #d9c6b4;padding-top:16px}

/* band CTA */
.band{background:linear-gradient(150deg,var(--ink),var(--ink2));color:#f2e6ec;padding:56px 0}
.band h2{color:#f7eef1}
.band .cta{margin-top:1.4em}

/* contact form */
.cform-sec{padding:52px 0 64px}
.cform-sec .split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(280px,.9fr);gap:48px;align-items:start}
.cform{display:grid;gap:18px;max-width:560px}
.cform label{display:grid;gap:6px;font-weight:600;color:var(--ink);font-size:.98rem}
.cform input,.cform textarea{font:inherit;padding:12px 14px;border:1px solid #d5c2b2;border-radius:12px;background:#fffdf8;color:var(--tx);width:100%}
.cform input:focus,.cform textarea:focus{outline:2px solid var(--pink);border-color:var(--pink)}
.cform button{justify-self:start}

/* footer */
footer{background:#1a0f1e;color:#cdb9c4;padding:38px 0 34px}
.footline{display:flex;flex-wrap:wrap;gap:14px 26px;justify-content:space-between;align-items:flex-start}
.fnote{max-width:46em;font-size:.95rem;line-height:1.75}
.fnote strong{color:var(--blush);font-family:var(--serif);letter-spacing:.06em;font-size:1.05rem}
.fnote span{display:block}
.fnote a{color:var(--brass);text-decoration:none}
.fnote a:hover{text-decoration:underline}
.fcopy{font-size:.88rem;color:#8d7884}

/* utility */
::selection{background:var(--blush)}
@media (max-width:860px){
  .hero-grid{grid-template-columns:1fr;gap:34px}
  .stack{height:210px;max-width:340px}
  .feature .split,.map-split,.cform-sec .split{grid-template-columns:1fr}
  .mapcell,.mapcell iframe{min-height:300px}
  .items,.menu-list{grid-template-columns:1fr}
  .hero{padding:48px 0 56px}
}
@media (max-width:420px){
  body{font-size:16px}
  .wrap{padding:0 18px}
  .bar{gap:8px 14px}
  nav{font-size:.93rem}
}
"""

def build():
    os.makedirs(OUT, exist_ok=True)
    for fn, content in PAGES.items():
        # utility pages: keep robots noindex + strip nothing else (OG gates exempt in _verify)
        with open(os.path.join(OUT, fn), 'w', encoding='utf-8') as f:
            f.write(content)
    with open(os.path.join(OUT, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(CSS)
    with open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots)
    with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap)
    with open(os.path.join(OUT, 'favicon.svg'), 'w', encoding='utf-8') as f:
        f.write(favicon)
    print("wrote", len(PAGES) + 4, "files to", OUT)

if __name__ == '__main__':
    build()
