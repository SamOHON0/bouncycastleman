# -*- coding: utf-8 -*-
"""
Bouncy Castle Man, content model.

Source: bouncycastleman.com (the old site) scraped 20 Aug 2026, plus the demo
approved by the client at bouncycastleman.vercel.app. Adam Garrett is the
contact (086 194 5789); Mike Garrett handed the job over on 12 Aug.

TODOs Adam must supply, all marked below:
  - real product photos (the old site only has 8 usable images, see IMAGES)
  - the real Formspree form ID
  - a business email address (the old site publishes none)
  - confirmation of the delivery areas and any prices he wants shown
  - real reviews (the three here are placeholders and are marked as such)

NOTE: the images that do exist hotlink files.secure.website, the old site's
host. That host disappears when the domain moves, so download local copies
into /images/ before go-live.
"""

SITE = "https://bouncycastleman.com"
NAME = "Bouncy Castle Man"
OWNER = "Adam"
PHONE_DISPLAY = "087 900 5391"
PHONE_TEL = "0879005391"
PHONE_INTL = "+353879005391"
WHATSAPP = "353879005391"
EMAIL = ""                                        # TODO: Adam has not given one
LOCALITY = "Thurles"
REGION = "Co Tipperary"
LOGO = ""                                         # TODO: no logo file supplied
FORMSPREE = "https://formspree.io/f/[FORM-ID]"    # TODO: Adam's real Formspree ID
FOUNDED = "2001"
FACEBOOK = "[FACEBOOK-URL]"                       # TODO: confirm with Adam

# Every image the old site actually serves. Nothing here is guessed.
_S = "https://files.secure.website/wscfus/10590302/"
IMG_BANNER = _S + "4489225/tvituvbevatafuao9m8r-w640-o.jpg"
IMG_LIZARD = _S + "8420309/lizard-castle-w480-o.jpg"
IMG_GREENGOLD = _S + "8407799/obstacle-green-n-gold-1-w640-o.jpg"
IMG_DISCO = _S + "8404155/disco-dome-w360-o.jpg"
IMG_CASTLE_C3 = _S + "uploads/c3_567.png"
IMG_MARQUEE = _S + "uploads/50ft-x-20ft-Marquee1-274x170.jpg"
IMG_CASTLE_A = _S + "uploads/Bouncy_Castles_Limerick_325.png"
IMG_CASTLE_B = _S + "uploads/bouncy_castle_2.jpg"

# Units with no photo on the old site get this. generate.py renders it as a
# branded "photo coming soon" tile rather than a broken image.
SOON = "__SOON__"

HERO_MAIN = IMG_LIZARD
HERO_IMG = IMG_LIZARD
HERO_IMG_NAME = "Red Lizard Obstacle"
HERO_IMG_TAG = "50ft"
IMG_AREAS = IMG_GREENGOLD

DELIVERY_TERMS = ("Delivery, set up and collection are included across Tipperary and the "
                  "surrounding areas. We agree a drop time with you when you book and take "
                  "the unit away again at the end of your hire.")

SAFETY = [
    "All castles and obstacle courses must be supervised by a responsible adult at all times.",
    "We are fully insured and certified with the Irish Inflatable Hirers Federation.",
    "Units are set up on a flat, clear surface with access for the blower and a power supply.",
]

# ------------------------------------------------------------- categories ----
CATEGORIES = [
    dict(slug="bouncy-castles", cat="castle", k="k1", title="Bouncy Castles",
         hero=IMG_CASTLE_A,
         blurb="Arch castles and kiddies bouncers, all with rain covers.",
         intro="Our standard bouncy castles suit birthday parties, communions and back garden "
               "days out. Every unit comes with a rain cover as standard, so an Irish forecast "
               "does not cancel the party. Delivered, set up and collected across Tipperary."),
    dict(slug="combi-castles", cat="combi", k="k2", title="Combi Castles",
         hero=IMG_CASTLE_C3,
         blurb="Bounce area and a built in slide, most with a basketball ring.",
         intro="Combi castles give you a full bouncing area and a slide in the one unit, and "
               "most have a basketball ring inside. Seven of them in the range, from 15ft up "
               "to 19ft, every one with a full rain cover."),
    dict(slug="obstacle-courses", cat="obstacle", k="k3", title="Obstacle Courses",
         hero=IMG_GREENGOLD,
         blurb="30ft up to 55ft, with rock climbs, tunnels and slides.",
         intro="Ten obstacle courses in the range, from a 30ft block run for younger children "
               "up to the 55ft high adrenaline units with double rock climbs and extra high "
               "slides. Every course has a full rain cover."),
    dict(slug="disco-dome", cat="disco", k="k4", title="Disco Dome",
         hero=IMG_DISCO,
         blurb="Enclosed dome with disco lighting and a full sound system.",
         intro="The disco dome is an enclosed bouncing unit with disco lighting and a full "
               "surround speaker system. It connects over Bluetooth or cable and works with "
               "Apple and Android, so the kids pick their own playlist."),
    dict(slug="sumo-gladiator", cat="sumo", k="k5", title="Sumo & Gladiator",
         hero=IMG_BANNER,
         blurb="Sumo suits and the gladiator challenge for older groups.",
         intro="Sumo suits and the gladiator challenge are our two units for teenagers, adults "
               "and corporate days. They suit school sports days, fun days and office events "
               "across Tipperary."),
    dict(slug="marquees", cat="marquee", k="k6", title="Marquees",
         hero=IMG_MARQUEE,
         blurb="Marquees in a range of sizes, with flooring, furniture, lighting and heat.",
         intro="We hire marquees in a range of sizes across Tipperary and the surrounding "
               "areas, in all seasons and for all events, from communions and confirmations "
               "to corporate days and family parties. A marquee can go out on its own or "
               "fitted out with flooring, tables, chairs, lighting and heaters, and we hire "
               "tables and chairs on their own as well."),
]

# ------------------------------------------------------------------ units ----
def _u(slug, n, cat, tag, short, body, specs, img=SOON, price="Call for price", gallery=()):
    return dict(slug=slug, n=n, cat=cat, tag=tag, short=short, body=body,
                specs=specs, img=img, price=price, gallery=list(gallery))


UNITS = [
    # ---- combi castles ----
    _u("large-combi-castle", "Large Combi Castle 19 x 19ft", "combi", "19x19ft",
       "Our biggest combi, with a built in slide, basketball ring and full rain cover.",
       ["At 19ft by 19ft this is the biggest combi in the range. It gives a full bouncing "
        "area alongside the slide, so a group of children can use both at once without "
        "queueing.",
        "It comes with a basketball ring inside and a full rain cover, and we deliver, set it "
        "up and collect it again across Tipperary."],
       [("Size", "19ft x 19ft"), ("Slide", "Built in"), ("Basketball ring", "Yes"),
        ("Rain cover", "Full cover included")], img=IMG_CASTLE_C3),
    _u("minions-combi-castle", "Minions Combi Castle 17 x 19ft", "combi", "17x19ft",
       "Minions themed combi with a slide, basketball ring and rain cover.",
       ["A themed combi castle at 17ft by 19ft with the slide built in and a basketball ring "
        "inside. A reliable pick for younger birthday parties.",
        "Full rain cover included, delivered and set up."],
       [("Size", "17ft x 19ft"), ("Slide", "Built in"), ("Basketball ring", "Yes"),
        ("Rain cover", "Full cover included")]),
    _u("cocomelon-castle", "Cocomelon Castle 17 x 19ft", "combi", "17x19ft",
       "Cocomelon themed unit with a large bounce area, slide and rain cover.",
       ["The Cocomelon castle suits smaller children. It has a large bouncing area with the "
        "slide built into the same unit.",
        "Rain cover included as standard."],
       [("Size", "17ft x 19ft"), ("Slide", "Built in"),
        ("Rain cover", "Full cover included")]),
    _u("minecraft-castle", "Minecraft Castle 17 x 19ft", "combi", "17x19ft",
       "Minecraft themed combi with a large bounce area, slide and rain cover.",
       ["A Minecraft themed combi at 17ft by 19ft, with a large bouncing area and a slide in "
        "the one unit. Popular with the seven to twelve age group.",
        "Rain cover included as standard."],
       [("Size", "17ft x 19ft"), ("Slide", "Built in"),
        ("Rain cover", "Full cover included")]),
    _u("crayola-playland", "Crayola Playland 15 x 15ft", "combi", "15x15ft",
       "Bright Crayola themed unit with an internal slide and rain cover.",
       ["The Crayola Playland is a 15ft by 15ft unit with the slide inside rather than on the "
        "outside, which suits smaller gardens and younger children.",
        "Rain cover included."],
       [("Size", "15ft x 15ft"), ("Slide", "Internal"),
        ("Rain cover", "Included")]),
    _u("combi-castle-15", "Combi Castle 15 x 15ft", "combi", "15x15ft",
       "Compact combi with an internal slide and rain cover.",
       ["A 15ft by 15ft combi with the slide built inside the unit. A good fit where space is "
        "tight but you still want a slide as well as a bounce area.",
        "Rain cover included."],
       [("Size", "15ft x 15ft"), ("Slide", "Internal"),
        ("Rain cover", "Included")]),
    _u("jungle-castle", "Jungle Castle 15 x 15ft", "combi", "Up to 8 yrs",
       "Jungle themed unit with a large bounce area and slide, suited to under eights.",
       ["The Jungle Castle is a 15ft by 15ft unit with a large bouncing area and a slide, and "
        "it is sized for children up to about eight years old.",
        "Rain cover included as standard."],
       [("Size", "15ft x 15ft"), ("Slide", "Built in"), ("Ages", "Up to 8 years"),
        ("Rain cover", "Included")]),

    # ---- bouncy castles ----
    _u("standard-arch-castle", "Standard Arch Castle 12 x 12ft", "castle", "12x12ft",
       "The classic arch castle, rain cover included.",
       ["Our standard 12ft by 12ft arch castle is the straightforward option for a back garden "
        "birthday party. All bouncing area, no slide.",
        "Rain cover included, delivered and set up across Tipperary."],
       [("Size", "12ft x 12ft"), ("Rain cover", "Included")], img=IMG_CASTLE_A),
    _u("kiddies-bouncer", "Kiddies Bouncer", "castle", "Toddlers",
       "A smaller unit sized for toddlers and pre school parties.",
       ["The kiddies bouncer is our smallest unit, sized for toddlers and pre school age "
        "children where a full size castle would be too much.",
        "Ring Adam to check sizes and availability for your date."],
       [("Suits", "Toddlers and pre school"), ("Rain cover", "Included")], img=IMG_CASTLE_B),

    # ---- obstacle courses ----
    _u("adrenaline-max", "Adrenaline Max 55 x 15ft", "obstacle", "55ft",
       "High adrenaline 55ft course with an extra high slide and double rock climb.",
       ["The Adrenaline Max is one of the two biggest units we run. At 55ft by 15ft it has an "
        "extra high slide, a double rock climb, biff and bash, tunnels and bash pillars.",
        "This is a high adrenaline unit, so it suits older children, teenagers and school "
        "sports days rather than toddler parties. Full rain cover included."],
       [("Size", "55ft x 15ft"), ("Slide", "Extra high"), ("Rock climb", "Double"),
        ("Features", "Biff and bash, tunnels, bash pillars"),
        ("Rain cover", "Full cover included")]),
    _u("adrenaline-zone", "Adrenaline Zone 55ft", "obstacle", "55ft",
       "55ft course with an extra high slide, double rock climb and bash pillars.",
       ["The Adrenaline Zone runs to 55ft with an extra high slide and a double rock climb, "
        "plus bash pillars and tunnels along the way.",
        "Another high adrenaline unit, popular for school sports days and community fun days. "
        "Full rain cover included."],
       [("Size", "55ft"), ("Slide", "Extra high"), ("Rock climb", "Double"),
        ("Features", "Bash pillars, tunnels"),
        ("Rain cover", "Full cover included")]),
    _u("red-lizard-obstacle", "Red Lizard Obstacle 50ft", "obstacle", "50ft",
       "50ft course with biff and bash, a rock climb and a slide.",
       ["The Red Lizard is a 50ft obstacle course with biff and bash sections, a rock climb "
        "and a slide to finish.",
        "Full rain cover included, so it runs whatever the forecast."],
       [("Size", "50ft"), ("Features", "Biff and bash, rock climb, slide"),
        ("Rain cover", "Full cover included")], img=IMG_LIZARD),
    _u("crocodile-obstacle", "Crocodile Obstacle 50ft", "obstacle", "50ft",
       "50ft crocodile themed course with biff and bash, rock climb and slide.",
       ["A 50ft crocodile themed obstacle course with biff and bash sections, a rock climb and "
        "a slide at the end.",
        "Full rain cover included."],
       [("Size", "50ft"), ("Features", "Biff and bash, rock climb, slide"),
        ("Rain cover", "Full cover included")]),
    _u("blue-yellow-obstacle", "Blue and Yellow Obstacle 50ft", "obstacle", "50ft",
       "Blue and yellow 50ft course with tunnels, a rock climb and a slide to finish.",
       ["A 50ft obstacle course in blue and yellow, with biff and bash, a rock climb, tunnels "
        "and a slide.",
        "Rain cover included."],
       [("Size", "50ft"), ("Features", "Biff and bash, rock climb, tunnels, slide"),
        ("Rain cover", "Included")]),
    _u("orange-green-obstacle", "Orange and Green Obstacle 50ft", "obstacle", "50ft",
       "50ft course with biff and bash, a rock climb, tunnels and a slide.",
       ["A 50ft obstacle course in orange and green, with biff and bash sections, a rock "
        "climb, tunnels and a slide.",
        "Rain cover included."],
       [("Size", "50ft"), ("Features", "Biff and bash, rock climb, tunnels, slide"),
        ("Rain cover", "Included")], img=IMG_GREENGOLD),
    _u("rock-climb-course", "50ft Rock Climb Course", "obstacle", "50ft",
       "50ft course built around the rock climb, rain cover included.",
       ["A 50ft obstacle course built around the rock climb section.",
        "Rain cover included as standard."],
       [("Size", "50ft"), ("Features", "Rock climb"), ("Rain cover", "Included")]),
    _u("booster-obstacle", "Booster Obstacle 45ft", "obstacle", "45ft",
       "45ft course with a slide, rock climb, tunnels and biff and bash.",
       ["The Booster is a 45ft obstacle course with a slide, a rock climb, tunnels and biff "
        "and bash sections.",
        "A good middle size where the 55ft units are too big for the space. Rain cover "
        "included."],
       [("Size", "45ft"), ("Features", "Slide, rock climb, tunnels, biff and bash"),
        ("Rain cover", "Included")]),
    _u("jungle-run-obstacle", "Jungle Run Obstacle 45ft", "obstacle", "45ft",
       "45ft jungle themed course with a high slide, rock climb and biff and bash.",
       ["The Jungle Run is a 45ft obstacle course with a high slide, a rock climb and biff and "
        "bash sections.",
        "Full rain cover included."],
       [("Size", "45ft"), ("Features", "High slide, rock climb, biff and bash"),
        ("Rain cover", "Full cover included")]),
    _u("block-run-obstacle", "Block Run Obstacle 30ft", "obstacle", "30ft",
       "Our smallest course at 30ft, with a slide, rock climb and bounce area.",
       ["The Block Run is a 30ft obstacle course with a slide, a rock climb, a bounce area and "
        "biff and bash sections.",
        "At 30ft it fits gardens that will not take the bigger courses, and it suits younger "
        "children. Rain cover included."],
       [("Size", "30ft"), ("Features", "Slide, rock climb, bounce area, biff and bash"),
        ("Rain cover", "Included")]),

    # ---- disco dome ----
    _u("disco-dome", "Disco Dome 17 x 19ft", "disco", "17x19ft",
       "Enclosed dome with disco lighting and a full surround sound system.",
       ["The disco dome is an enclosed bouncing unit with disco lighting inside and a full "
        "surround speaker system.",
        "It connects over Bluetooth or by cable and works with both Apple and Android, so the "
        "kids can run their own playlist. Popular for birthdays and teenage parties."],
       [("Size", "17ft x 19ft"), ("Lighting", "Disco lighting"),
        ("Sound", "Full surround speaker system"),
        ("Connectivity", "Bluetooth or cable, Apple and Android")], img=IMG_DISCO),

    # ---- sumo and gladiator ----
    _u("sumo-suits", "Sumo Suits", "sumo", "Groups",
       "Padded sumo suits for teenagers, adults and corporate days.",
       ["A set of padded sumo suits with the mat, for teenagers, adults and corporate events.",
        "Suits school sports days, fun days and office events. Ring Adam for numbers and "
        "availability."],
       [("Suits", "Teenagers, adults, corporate"), ("Supervision", "Adult supervision required")]),
    _u("gladiator-challenge", "Gladiator Challenge", "sumo", "Head to head",
       "Head to head gladiator duel platform for older groups and corporate days.",
       ["The gladiator challenge is a head to head duel on a raised platform, with the padded "
        "poles. Two go up, one comes down.",
        "Suits teenagers, adults and corporate days rather than small children."],
       [("Format", "Head to head"), ("Suits", "Teenagers, adults, corporate"),
        ("Supervision", "Adult supervision required")]),

    # ---- marquees ----
    _u("marquee-hire", "Marquee Hire", "marquee", "All seasons",
       "Marquees in a range of sizes, with flooring, furniture, lighting and heating.",
       ["We hire marquees in a range of sizes across Tipperary and the surrounding areas, for "
        "anywhere from 20 to 100 people, and they can be used in all seasons and for all "
        "events.",
        "A marquee can go out on its own, or with flooring, tables, chairs, lighting and "
        "heating.",
        "Communions, confirmations, corporate days, birthdays and family parties. Ring Adam "
        "with your date and the numbers you are expecting and we will size it for you."],
       [("Sizes", "A range, sized to your numbers"), ("Numbers", "20 to 100 people"),
        ("Flooring", "Available"),
        ("Tables and chairs", "Available"), ("Lighting", "Available"),
        ("Heating", "Available"), ("Season", "All seasons")], img=IMG_MARQUEE),
    # Furniture on its own. Adam: "We also hire tables and chairs separately from
    # the marquees." It sits in the marquee category rather than becoming a
    # seventh one: it is the same side of the business, and six categories is
    # load bearing across the rail, the shelves and the copy.
    _u("tables-and-chairs", "Tables & Chairs", "marquee", "Separate hire",
       "Tables and chairs hired on their own, with or without a marquee.",
       ["We hire tables and chairs on their own, not only as part of a marquee. If you have "
        "the room already and you just need to seat people, this is the one to ring about.",
        "Tell us how many you are expecting and we will work out the tables and chairs you "
        "need."],
       [("Hire", "On their own or with a marquee"),
        ("Numbers", "Sized to your guest list")]),
]

# ------------------------------------------------------- marquee extras ----
# What a marquee can be fitted out with. Straight from Adam, 27 Aug 2026:
# "we hire various sizes that can home with floors , tables , chairs , lights
# and heaters", plus tables and chairs hired separately from the marquees.
# TODO: Adam has NOT given the actual marquee sizes, capacities or prices. The
# page is deliberately written so it does not need them, but add them here as
# soon as he comes back and the sizes will read a lot stronger than "a range".
# SOURCED, premiermarqueehire.com (their own marquee site, which links back to
# bouncycastleman.com as "Our Main Website"): "Provide Marquees, Tables, Chairs,
# Flooring Heating, For 20-100 People". That is their published capacity, so it
# is safe to state. Adam still has not given the actual marquee dimensions.
MARQUEE_CAPACITY = "20 to 100 people"

# NAMES ONLY, deliberately. The five items are Adam's own words and are
# confirmed twice over, but every descriptive sentence under them was ours and
# none of it was sourced: whether the floor is timber, whether tables are set
# out before you arrive, what the lighting actually is. Sales copy invented for
# a client is how a site ends up promising something the client does not do.
# Add real detail here only when Adam gives it, as (name, detail) pairs.
MARQUEE_EXTRAS = ["Flooring", "Tables", "Chairs", "Lighting", "Heating"]

# ------------------------------------------------------------------ areas ----
# TODO: Adam has not confirmed the travel radius. This list is the one used in
# the demo pitch. Add or drop towns once he comes back.
AREAS = [
    dict(slug="bouncy-castle-hire-clonmel", town="Clonmel", county="Co Tipperary",
         nearby="Ardfinnan, Kilsheelan and Fethard",
         copy=["We deliver bouncy castles, combi castles and the full run of obstacle courses "
               "across Clonmel and out through Ardfinnan, Kilsheelan and Fethard.",
               "Back garden birthdays, school sports days and community fun days: we drop the "
               "unit out, set it up and collect it again, so there is nothing for you to "
               "lift."]),
    dict(slug="bouncy-castle-hire-thurles", town="Thurles", county="Co Tipperary",
         nearby="Holycross, Littleton and Two Mile Borris",
         copy=["Thurles is home ground for us. We are based here, so it is the shortest run "
               "we do.",
               "We cover Holycross, Littleton and Two Mile Borris as well, with the full range "
               "travelling: castles, combis, obstacle courses, the disco dome and marquees."]),
    dict(slug="bouncy-castle-hire-nenagh", town="Nenagh", county="Co Tipperary",
         nearby="Borrisokane, Newport and Puckane",
         copy=["We deliver to Nenagh and out around Borrisokane, Newport and Puckane, with the "
               "full range of castles and obstacle courses.",
               "If you are running a bigger day, the 55ft high adrenaline courses and the "
               "marquees travel here too. Ring us with your numbers and we will size it."]),
    dict(slug="bouncy-castle-hire-cashel", town="Cashel", county="Co Tipperary",
         nearby="Golden, Rosegreen and New Inn",
         copy=["Cashel, Golden, Rosegreen and New Inn are all inside our delivery area, for "
               "everything from a 12ft arch castle to the 55ft obstacle courses.",
               "If you are booking around communion or confirmation season, get your date in "
               "to us early."]),
    dict(slug="bouncy-castle-hire-roscrea", town="Roscrea", county="Co Tipperary",
         nearby="Templemore, Borris in Ossory and Moneygall",
         copy=["We cover Roscrea and the surrounding villages, including Templemore, Borris in "
               "Ossory and Moneygall.",
               "Castles, combis with slides, obstacle courses, the disco dome and sumo suits "
               "all travel up this way. Delivered, set up and collected."]),
    dict(slug="bouncy-castle-hire-tipperary-town", town="Tipperary Town", county="Co Tipperary",
         nearby="Bansha, Cappawhite and Dundrum",
         copy=["We deliver to Tipperary Town and the surrounding villages of Bansha, "
               "Cappawhite and Dundrum.",
               "Whether it is a back garden birthday or a full community fun day, we have the "
               "unit for it, and every castle and course comes with a rain cover."]),
    dict(slug="bouncy-castle-hire-templemore", town="Templemore", county="Co Tipperary",
         nearby="Borrisoleigh, Loughmore and Clonmore",
         copy=["We deliver to Templemore, Borrisoleigh, Loughmore and Clonmore.",
               "The full range travels here: castles, combis with built in slides, obstacle "
               "courses from 30ft to 55ft, the disco dome, sumo suits and marquees."]),
    dict(slug="bouncy-castle-hire-cahir", town="Cahir", county="Co Tipperary",
         nearby="Ardfinnan, Bansha and Ballylooby",
         copy=["Cahir, Ardfinnan, Bansha and Ballylooby are all within our delivery area.",
               "Popular here are the combi castles for younger birthdays and the 45ft and 50ft "
               "obstacle courses for school and club days."]),
    dict(slug="bouncy-castle-hire-carrick-on-suir", town="Carrick on Suir", county="Co Tipperary",
         nearby="Kilsheelan, Piltown and Mooncoin",
         copy=["We cover Carrick on Suir and out towards Kilsheelan, Piltown and Mooncoin.",
               "Castles, obstacle courses, the disco dome and marquees all travel down this "
               "end of the county. Ring us with your date and we will confirm availability."]),
]

# Old site URLs, so nothing that is already indexed or linked 404s after the
# switchover. Source paths come from bouncycastleman.com's own navigation.
REDIRECTS = [
    ("/index", "/"),
    ("/obstacle_courses", "/obstacle-courses/"),
    ("/bouncy_castles", "/bouncy-castles/"),
    ("/disco_dome", "/disco-dome/"),
    ("/marquees", "/marquees/"),
    ("/gallery", "/gallery/"),
    ("/contact", "/contact/"),
]

AREA_OPTIONS = [a["town"] for a in AREAS] + ["Littleton", "Borrisokane", "Newport"]

# ------------------------------------------------------------------- misc ----
STEPS = [
    ("Pick your unit", "Have a look through the range and note the one you want, or ring Adam "
                       "and he will point you at the right size for the space and the ages."),
    ("Check your date", "Send an enquiry or ring with your date, your town and the ages of the "
                        "children. We come back to you with the price."),
    ("We deliver and set up", "We drop the unit out, set it up, run through the safety points "
                              "with you and collect it again at the end of the hire."),
]

WHY = [
    # The old site says "Established in 2001", "Family Run Business" and "20+
    # Years Experience". It says nothing about the phone number never changing,
    # so that claim is gone. Do not put a fact on this site that Adam has not
    # said somewhere first.
    ("\U0001F3F0", "Family run since " + FOUNDED,
     "Over twenty years hiring castles and courses across Tipperary, and still the same "
     "family running it."),
    ("\U0001F6E1️", "Fully insured and IIHF certified",
     "We are fully insured and certified with the Irish Inflatable Hirers Federation, so "
     "schools and committees can book with confidence."),
    # Was "Tipperary's biggest selection", which we could not source and which is
    # a claim about competitors. The count is a fact about their own catalogue.
    ("\U0001F4CF", "Twenty three units in the range",
     "From a 30ft block run up to the 55ft high adrenaline courses, plus combis, disco dome, "
     "sumo suits and marquees."),
    ("☔", "Rain covers as standard",
     "Every castle and course comes with a rain cover, so an Irish forecast does not cancel "
     "the party."),
    ("\U0001F69A", "Delivered, set up and collected",
     "We bring it out, set it up and take it away again. You do not lift a thing."),
    ("\U0001F389", "Every kind of day",
     "Birthdays, communions, confirmations, school sports days, corporate events, carnivals "
     "and community fun days."),
]

# TODO: placeholders. Replace with Adam's real reviews before go-live.
REVIEWS = [
    ("Booked the 55ft course for our school sports day. Set up early, collected on time and "
     "the kids did not come off it all afternoon.", "Sarah M.", "Thurles"),
    ("Got a combi castle for a garden birthday. Spotless condition and the rain cover meant "
     "we did not have to worry about the forecast.", "Declan B.", "Clonmel"),
    ("Used them for our community fun day. Great value, arrived when they said they would and "
     "nothing was any trouble.", "Aoife K.", "Nenagh"),
]

FAQS = [
    ("What can I hire?",
     "Bouncy castles, combi castles with slides, obstacle courses from 30ft up to 55ft, a "
     "disco dome, sumo suits, the gladiator challenge and marquees."),
    ("What areas do you cover?",
     "We cover Tipperary and the surrounding areas, including Clonmel, Thurles, Nenagh, "
     "Cashel, Roscrea, Tipperary Town, Templemore, Cahir and Carrick on Suir. If your town is "
     "not listed, ring us, we may still reach you."),
    ("Are you insured?",
     "Yes. We are fully insured and certified with the Irish Inflatable Hirers Federation."),
    ("What occasions do you cover?",
     "Birthday parties, school events, sports days, communions, confirmations, corporate "
     "events, carnivals and community fun days."),
]

GALLERY = [IMG_LIZARD, IMG_GREENGOLD, IMG_CASTLE_C3, IMG_DISCO, IMG_MARQUEE,
           IMG_CASTLE_A, IMG_CASTLE_B, IMG_BANNER]
