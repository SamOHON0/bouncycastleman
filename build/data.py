# -*- coding: utf-8 -*-
"""
Bouncy Castle Man, content model.

Source: bouncycastleman.com (the old site) scraped 20 Aug 2026, plus the demo
approved by the client at bouncycastleman.vercel.app. Adam Garrett is the
contact (086 194 5789); Mike Garrett handed the job over on 12 Aug.

CLIENT FEEDBACK, 3 Sep 2026 (Adam, after reviewing the first draft). Six
changes, all applied in this pass:
  1. Home page was too long. Four sections cut, see pages.py build_home.
  2. Kiddies Bouncer removed. "We no longer have it." Gone from UNITS.
  3. NO UNIT COUNTS ANYWHERE. "Remove any reference to the specific amount of
     units we have." The facts strip, the WHY cell and the two category intros
     all carried one. DO NOT PUT A COUNT BACK ON THIS SITE.
  4. NO OWNER NAME IN CONTACT COPY. "Remove any reference of my name regarding
     call backs and getting in contact." Every "Ring Adam" is now "Ring us".
  5. The area checker is gone. The town list plus one line saying to ring if
     your town is not listed is what he asked for and all he wants.
  6. The first hero slide showed a castle they no longer have. That photo,
     castle-outdoor.jpg, is off the site entirely.

WITH THE KIDDIES BOUNCER GONE the old Bouncy Castles category had nothing in
it. The combi castles moved into it rather than the category being dropped:
a combi IS a bouncy castle to whoever is booking, the business is called
Bouncy Castle Man, and /bouncy-castles/ is the page the search term lands on.
/combi-castles/ redirects to it.

TODOs Adam must supply, all marked below:
  - the real Formspree form ID
  - a business email address (the old site publishes none)
  - confirmation of the delivery areas and any prices he wants shown
  - real reviews (the three here are placeholders and are marked as such)
  - whether he still has the FOUR UNITS REMOVED on 2 Sep. See the note above
    the UNITS list. They come back the moment he says he has them.

IMAGES ARE LOCAL. Every photo on this site is a file in this repo. Nothing
hotlinks files.secure.website any more, so nothing breaks at the DNS cutover.
"""

SITE = "https://bouncycastleman.com"
NAME = "Bouncy Castle Man"
OWNER = "Adam"                                    # NOT RENDERED. Adam asked for his
                                                  # name off the contact copy, 3 Sep.
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

# ---- UNIT PHOTOS, pulled off the old site 2 Sep 2026 and now LOCAL ----------
# Nothing on this site hotlinks files.secure.website any more. That matters:
# the old host serves images off the old domain's account, and it goes away at
# the DNS cutover. Every image below is in this repo.
#
# HOW EACH ONE WAS IDENTIFIED. The old site keeps its captions in elements that
# are not related to the images in the markup, so filename matching got twelve
# of them and no more. The other ten had filenames like img-0278 and a UUID.
# They were identified by loading each old page in a browser, shrinking it and
# READING it: the caption beside a photo on the rendered page is what names it.
# So these assignments come from the client's own published captions, not from
# my guess at what an inflatable looks like.
#
# THREE IMAGES WERE ON THE WRONG UNIT before this pass, all inherited from the
# old site's filenames:
#   c3_567.png                 was the Large Combi hero. It is the CRAYOLA
#                              PLAYLAND, the words are printed on the unit.
#   Bouncy_Castles_Limerick    was the Standard Arch Castle hero. It is the
#                              GLADIATOR CHALLENGE duel platform.
#   bouncy_castle_2.jpg        was the Kiddies Bouncer hero. It is a SUMO SUIT.
#                              Now on the Sumo Suits unit, where it belongs.
#                              See the note on sumo-suit.jpg below before you
#                              touch it: there is a watermark question on it.
_U = "/images/units/"
IMG_COMBI_JUNGLE    = _U + "combi-jungle.jpg"        # Jungle Castle 15x15
IMG_COMBI_MINECRAFT = _U + "combi-minecraft.jpg"     # Minecraft Castle 17x19
IMG_COMBI_COCOMELON = _U + "combi-cocomelon.jpg"     # Cocomelon Castle 17x19
IMG_COMBI_MINIONS   = _U + "combi-minions.jpg"       # Minions Combi 17x19
IMG_COMBI_CRAYOLA   = _U + "combi-crayola.jpg"       # Crayola Playland 15x15
# RETIRED 3 Sep 2026. castle-outdoor.jpg was the first hero slide and the
# Bouncy Castles category hero. Adam: "Under the calendar the first image is
# of a castle, we no longer have this castle so it can be removed." It is a
# photo of a unit that is no longer in the fleet, so it is off the site, not
# moved to the gallery. DO NOT REINSTATE IT.
IMG_OBS_MAX         = _U + "obs-adrenaline-max.jpg"  # Adrenaline Max 55ft
IMG_OBS_ZONE        = _U + "obs-adrenaline-zone.jpg" # Adrenaline Zone 55ft
IMG_OBS_LIZARD      = _U + "obs-red-lizard.jpg"      # Red Lizard 50ft
IMG_OBS_CROC        = _U + "obs-crocodile.jpg"       # Crocodile 50ft (SEE BELOW)
IMG_OBS_BLUEYELLOW  = _U + "obs-blue-yellow.jpg"     # Blue and Yellow 50ft
IMG_OBS_ORANGEGREEN = _U + "obs-orange-green.jpg"    # Orange and Green 50ft
IMG_OBS_BOOSTER     = _U + "obs-booster.jpg"         # Booster 45ft
IMG_OBS_JUNGLERUN   = _U + "obs-jungle-run.jpg"      # Jungle Run 45ft
IMG_OBS_BLOCKRUN    = _U + "obs-block-run.jpg"       # Block Run 30ft
IMG_DISCO           = _U + "disco-dome.jpg"          # Disco Dome
IMG_GLADIATOR       = _U + "gladiator.jpg"           # Gladiator Challenge (SEE BELOW)
IMG_SUMO            = _U + "sumo-suit.jpg"           # Sumo Suits (SEE BELOW)
IMG_VAN             = _U + "van.jpg"                 # the branded van, unused

# Extra shots. The old site captions FIVE different inflatables "Adrenaline Max"
# and THREE "Booster Obstacle". They are visibly not the same units. Rather than
# pick which four are mislabelled, one of each goes on the unit page and the
# rest go in the site gallery, where no photo claims to be a particular unit.
IMG_OBS_MAX_STUDIO  = _U + "obs-max-studio.jpg"
IMG_OBS_MAX_RED     = _U + "obs-max-red.jpg"
IMG_OBS_MAX_TEAL    = _U + "obs-max-teal.jpg"
IMG_OBS_MAX_BLUE    = _U + "obs-max-blue.jpg"
IMG_OBS_BOOSTER_2   = _U + "obs-booster-2.jpg"
IMG_OBS_BOOSTER_IN  = _U + "obs-booster-indoor.jpg"

# THREE WEAK IMAGES, all kept because they are the only shot of that unit and a
# soft photo beats a "coming soon" tile on a draft. Replace all three when Adam
# sends phone photos, which will be better than any of them.
#   obs-crocodile.jpg  300x168. The old site never held a bigger copy.
#   gladiator.jpg      312x139, a supplier render on white, not a photo.
#   sumo-suit.jpg      226x127 originally, and it is a SUPPLIER STOCK SHOT that
#                      carried an "indigo INFLATABLES" watermark top right.
#
# READ THIS BEFORE CHANGING sumo-suit.jpg.
# The watermark is another company's mark, and the source is their stock photo
# rather than a photo of Adam's kit. Two things make it defensible to ship:
# Adam has been publishing this exact image on bouncycastleman.com for years,
# so we are carrying across his own existing use rather than introducing it;
# and Indigo Inflatables is a manufacturer, so if he bought the suits from them
# he is very likely entitled to their product shot.
# The crop is 170x127 of the 226x127 original, which is 1.339 against the
# card's 4/3, so it is the ratio the card wants and it centres the suit. The
# watermark sat at x172-222 and falls outside that crop. That is a real side
# effect and it was not an accident, so it is written down here rather than
# left for someone to discover. The mark was NOT painted out or cloned over.
# If Adam is not an Indigo customer the photo should come off entirely, and
# cropping would not have made it alright. ASK HIM.

# ---- REAL PHOTOS, and the first local images on this site --------------------
# Nine marquee photos from Adam, 2 Sep 2026, via Sam. Resized to a 1200px long
# edge at q74 and saved progressive: the originals were 2.8MB of phone JPEG for
# 2.5MB of grass texture, and this is 1.7MB for the nine with no visible loss.
# They live in /images/ like everything else on this site now.
_MQ = "/images/marquees/"
IMG_MQ_ASTRO  = _MQ + "marquee-astro-sunny.jpg"      # landscape, blue sky
IMG_MQ_PAIR   = _MQ + "marquee-pair-astro.jpg"       # landscape, two marquees
IMG_MQ_LONG   = _MQ + "marquee-long-grass.jpg"       # landscape, long, on grass
IMG_MQ_GRAVEL = _MQ + "marquee-gravel.jpg"           # portrait, exterior
IMG_MQ_TREE   = _MQ + "marquee-grass-tree.jpg"       # portrait, exterior
IMG_MQ_STONE  = _MQ + "marquee-stone-building.jpg"   # portrait, exterior
IMG_MQ_TABLES = _MQ + "marquee-tables-chairs.jpg"    # INTERIOR, tables and chairs out
IMG_MQ_FLOOR  = _MQ + "marquee-flooring.jpg"         # INTERIOR, the floor
IMG_MQ_INSIDE = _MQ + "marquee-inside.jpg"           # INTERIOR, empty and bright

# Units with no photo on the old site get this. generate.py renders it as a
# branded "photo coming soon" tile rather than a broken image.
SOON = "__SOON__"

HERO_MAIN = IMG_OBS_MAX

# The hero photo is a SLIDESHOW.
# ORDER MATTERS. The first slide is the first thing anyone sees.
#
# It used to open on castle-outdoor.jpg. Adam killed that on 3 Sep: it is a
# unit they no longer have. The replacement opener is the Adrenaline Max,
# which is the best photograph on the whole site and the only one that is
# outdoors, landscape, in daylight AND has their own branded van in the frame
# with the phone number on the side.
#
# EVERY REMAINING CASTLE PHOTO IS A SUPPLIER WAREHOUSE SHOT, taken on a
# concrete floor under strip lights, several with Indigo Inflatables' label
# visible on the unit. They are fine on a unit card where the job is to show
# what the thing looks like. They are not a hero. That is why an obstacle
# course opens a page headed "bouncy castle hire", and it stays that way until
# Adam sends a phone photo of a castle on grass.
#
# The rest alternate sides of the business. The two marquees are in here on
# purpose, because Adam said that side was being lost.
HERO_SLIDES = [
    (IMG_OBS_MAX,         "Adrenaline Max",           "55ft"),
    (IMG_MQ_ASTRO,        "Marquee",                  "20 to 100 people"),
    (IMG_COMBI_JUNGLE,    "Jungle Castle",            "15x15ft"),
    (IMG_OBS_BLUEYELLOW,  "Blue and Yellow Obstacle", "50ft"),
    (IMG_MQ_PAIR,         "Marquees",                 "Two on site"),
    (IMG_DISCO,           "Disco Dome",               "Lights and sound"),
]
HERO_IMG = HERO_SLIDES[0][0]
HERO_IMG_NAME = HERO_SLIDES[0][1]
HERO_IMG_TAG = HERO_SLIDES[0][2]
IMG_AREAS = IMG_OBS_ORANGEGREEN

# NOT SOURCED, SO NOT STATED. Their whole site, all seven pages, says nothing
# about delivery, set up, collection, what is included in a hire, or how a drop
# time is agreed. Neither does anything Adam has emailed. This used to promise
# all of it. Almost every hire firm in the trade does deliver and set up, which
# is exactly why it was easy to write and easy to miss.
# Ask Adam and put the real wording here.
# NO OWNER NAME. Adam, 3 Sep: "Can we remove any reference of my name regarding
# calls backs and getting in contact." Every one of these used to say "Ring
# Adam". They say "Ring us" now. Keep it that way.
DELIVERY_TERMS = ("Ring us on " + PHONE_DISPLAY + " and we will go through how the hire "
                  "works, what is included and what we need from you on the day.")

# ONE LINE, because one line is all their site supports. The supervision rule
# and the setup requirements (flat clear surface, blower, power supply) were
# both ours. They are standard in the trade and they are probably right, which
# is not the same as Adam having said them. Get his real conditions.
SAFETY = [
    "We are fully insured and certified with the Irish Inflatable Hirers Federation.",
]

# ------------------------------------------------------------- categories ----
# ORDER IS LOAD BEARING AND IT IS DELIBERATE. This one list drives the rail, the
# shelves on the home page, the footer range list and the sitemap, so reordering
# here reorders the whole site at once.
#
# FIVE CATEGORIES SINCE 3 SEP, not six. Adam removed the Kiddies Bouncer, which
# was the only unit left in Bouncy Castles, and killed the one photo that
# category had. Rather than drop the page, the combi castles moved into it and
# /combi-castles/ now redirects to /bouncy-castles/.
#
# Why that way round and not the other:
#   - the business is called Bouncy Castle Man and the h1 says bouncy castle
#     hire, so a site with no bouncy castles page reads as a mistake
#   - "bouncy castle hire tipperary" is the search term the whole site is built
#     to win, and /bouncy-castles/ is where it lands
#   - a combi IS a bouncy castle to whoever is booking. It is a bouncing area
#     with a slide attached, not a different product
#   - the old site's own /bouncy_castles path redirects here, so nothing that is
#     already indexed or linked goes anywhere unexpected
#
# Bouncy castles lead now. Five units, every one with a photo. They opened with
# two "photo coming soon" tiles before 2 Sep, which is why obstacle courses were
# put in front; that reason is gone.
#
# NO COUNTS IN ANY INTRO. Adam, 3 Sep: "Can we please remove any reference to
# the specific amount of units we have." The obstacle intro said nine and the
# combi intro said five. Both are now described rather than counted.
#
# `k` is currently read by nothing. Kept in step with the order anyway so it
# does not start lying to the next person who greps for it.
CATEGORIES = [
    dict(slug="bouncy-castles", cat="castle", k="k1", title="Bouncy Castles",
         hero=IMG_COMBI_JUNGLE,
         blurb="A full bouncing area with a slide built in, most with a basketball ring.",
         intro="Our bouncy castles are combi units: a full bouncing area and a slide in the "
               "one castle, and most have a basketball ring inside. They run from 15ft up to "
               "19ft, and every one has a full rain cover."),
    dict(slug="obstacle-courses", cat="obstacle", k="k2", title="Obstacle Courses",
         hero=IMG_OBS_BLUEYELLOW,
         blurb="30ft up to 55ft, with rock climbs, tunnels and slides.",
         intro="Obstacle courses from a 30ft block run for younger children up to the 55ft "
               "high adrenaline units with double rock climbs and extra high slides. Every "
               "course has a full rain cover."),
    dict(slug="disco-dome", cat="disco", k="k3", title="Disco Dome",
         hero=IMG_DISCO,
         blurb="Enclosed dome with disco lighting and a full sound system.",
         intro="The disco dome is an enclosed bouncing unit with disco lighting and a full "
               "surround speaker system. It connects over Bluetooth or cable and works with "
               "Apple and Android, so the kids pick their own playlist."),
    # This was the no-photo panel until 2 Sep. It is the gladiator platform now.
    # It is NOT the old site's masthead graphic, which is the wordmark on a blue
    # ground and cropped to a 16/10 banner rendered as a zoomed fragment of the
    # word CASTLE. Never put that back.
    dict(slug="sumo-gladiator", cat="sumo", k="k4", title="Sumo & Gladiator",
         hero=IMG_GLADIATOR,
         blurb="Sumo suits and the gladiator challenge for older groups.",
         intro="Sumo suits and the gladiator challenge are what we hire for adults and "
               "corporate days. Their old site put both under Corporate Hire, so ring us "
               "for numbers and availability."),
    dict(slug="marquees", cat="marquee", k="k5", title="Marquees",
         hero=IMG_MQ_PAIR,
         blurb="Marquees in a range of sizes, with flooring, furniture, lighting and heat.",
         intro="We hire marquees in a range of sizes across Tipperary and the surrounding "
               "areas, in all seasons and for all events, from communions and confirmations "
               "to corporate days and family parties. A marquee can go out on its own or "
               "fitted out with flooring, tables, chairs, lighting and heaters, and we hire "
               "tables and chairs on their own as well."),
]

# ---- FOUR UNITS WERE REMOVED ON 2 SEP. DO NOT PUT THEM BACK WITHOUT ADAM. ----
#
#   Large Combi Castle 19 x 19ft
#   Combi Castle 15 x 15ft
#   Standard Arch Castle 12 x 12ft
#   50ft Rock Climb Course
#
# All four came from text that is in bouncycastleman.com's markup as WHITE TEXT
# ON A WHITE BACKGROUND, computed colour rgb(255,255,255). It is in the page and
# it is what a text dump returns, but no human visitor to their site can read a
# word of it, and none of the four had a photo or a visible card anywhere.
#
# It reads like a caption set stranded by an older version of the page: the same
# hidden column also holds captions for the Minions Combi and the Crayola
# Playland, which DO still have visible cards and photos. So it is not a list of
# discontinued units, and the honest position is that we cannot tell from their
# site which of them Adam still owns.
#
# THE KIDDIES BOUNCER STAYS, on Sam's call. Its evidence is different and
# weaker still: the words "Kiddies Bouncers" once, in the home page range list,
# visible, with no size, no ages and no features anywhere. It keeps its name and
# says only that it exists. It is the whole Bouncy Castles category now.
#
# Put any of the four back the moment Adam confirms he has it, with a photo.
# NOTHING COUNTS THEM ANY MORE. The WHY cell, the two category intros and the
# home page facts strip all carried a number and all three are gone, because
# Adam asked on 3 Sep for every reference to the specific amount of units to
# come off the site. Adding a unit is now a one line change here and nowhere
# else. Keep it that way.

# ------------------------------------------------------------------ units ----
def _u(slug, n, cat, tag, short, body, specs, img=SOON, price="Call for price", gallery=()):
    return dict(slug=slug, n=n, cat=cat, tag=tag, short=short, body=body,
                specs=specs, img=img, price=price, gallery=list(gallery))


UNITS = [
    # ---- bouncy castles, all of them combi units ----
    _u("minions-combi-castle", "Minions Combi Castle 17 x 19ft", "castle", "17x19ft",
       "Minions themed combi with a slide, basketball ring and rain cover.",
       ["A themed combi castle at 17ft by 19ft with the slide built in and a basketball ring "
        "inside. A reliable pick for younger birthday parties.",
        "Full rain cover included."],
       [("Size", "17ft x 19ft"), ("Slide", "Built in"), ("Basketball ring", "Yes"),
        ("Rain cover", "Full cover included")], img=IMG_COMBI_MINIONS),
    _u("cocomelon-castle", "Cocomelon Castle 17 x 19ft", "castle", "17x19ft",
       "Cocomelon themed unit with a large bounce area, slide and rain cover.",
       ["The Cocomelon castle suits smaller children. It has a large bouncing area with the "
        "slide built into the same unit.",
        "Rain cover included as standard."],
       [("Size", "17ft x 19ft"), ("Slide", "Built in"),
        ("Rain cover", "Full cover included")], img=IMG_COMBI_COCOMELON),
    _u("minecraft-castle", "Minecraft Castle 17 x 19ft", "castle", "17x19ft",
       "Minecraft themed combi with a large bounce area, slide and rain cover.",
       ["A Minecraft themed combi at 17ft by 19ft, with a large bouncing area and a slide in "
        "the one unit.",
        "Rain cover included as standard."],
       [("Size", "17ft x 19ft"), ("Slide", "Built in"),
        ("Rain cover", "Full cover included")], img=IMG_COMBI_MINECRAFT),
    _u("crayola-playland", "Crayola Playland 15 x 15ft", "castle", "15x15ft",
       "Bright Crayola themed unit with an internal slide and rain cover.",
       ["The Crayola Playland is a 15ft by 15ft unit with the slide inside rather than on the "
        "outside, which suits smaller gardens and younger children.",
        "Rain cover included."],
       [("Size", "15ft x 15ft"), ("Slide", "Internal"),
        ("Rain cover", "Included")], img=IMG_COMBI_CRAYOLA),
    _u("jungle-castle", "Jungle Castle 15 x 15ft", "castle", "Up to 8 yrs",
       "Jungle themed unit with a large bounce area and slide, suited to under eights.",
       ["The Jungle Castle is a 15ft by 15ft unit with a large bouncing area and a slide, and "
        "it is sized for children up to about eight years old.",
        "Rain cover included as standard."],
       [("Size", "15ft x 15ft"), ("Slide", "Built in"), ("Ages", "Up to 8 years"),
        ("Rain cover", "Included")], img=IMG_COMBI_JUNGLE),

    # THE KIDDIES BOUNCER WAS HERE AND IT IS GONE. Adam, 3 Sep 2026: "You can
    # remove the section about the kiddies bouncer as we no longer have it."
    # It was the last unit in the old Bouncy Castles category, which is why
    # that category is now the combis. Do not put it back.

    # ---- obstacle courses ----
    _u("adrenaline-max", "Adrenaline Max 55 x 15ft", "obstacle", "55ft",
       "High adrenaline 55ft course with an extra high slide and double rock climb.",
       ["The Adrenaline Max is one of the biggest units we run. At 55ft by 15ft it has an "
        "extra high slide, a double rock climb, biff and bash, tunnels and bash pillars.",
        "Their own listing calls it a high adrenaline unit. Full rain cover included."],
       [("Size", "55ft x 15ft"), ("Slide", "Extra high"), ("Rock climb", "Double"),
        ("Features", "Biff and bash, tunnels, bash pillars"),
        ("Rain cover", "Full cover included")], img=IMG_OBS_MAX,
       gallery=(IMG_OBS_MAX_BLUE, IMG_OBS_MAX_TEAL, IMG_OBS_MAX_RED, IMG_OBS_MAX_STUDIO)),
    _u("adrenaline-zone", "Adrenaline Zone 55ft", "obstacle", "55ft",
       "55ft course with an extra high slide, double rock climb and bash pillars.",
       ["The Adrenaline Zone runs to 55ft with an extra high slide and a double rock climb, "
        "plus bash pillars and tunnels along the way.",
        "Another of their high adrenaline units. Full rain cover included."],
       [("Size", "55ft"), ("Slide", "Extra high"), ("Rock climb", "Double"),
        ("Features", "Bash pillars, tunnels"),
        ("Rain cover", "Full cover included")], img=IMG_OBS_ZONE),
    _u("red-lizard-obstacle", "Red Lizard Obstacle 50ft", "obstacle", "50ft",
       "50ft course with biff and bash, a rock climb and a slide.",
       ["The Red Lizard is a 50ft obstacle course with biff and bash sections, a rock climb "
        "and a slide to finish.",
        "Full rain cover included, so it runs whatever the forecast."],
       [("Size", "50ft"), ("Features", "Biff and bash, rock climb, slide"),
        ("Rain cover", "Full cover included")], img=IMG_OBS_LIZARD),
    _u("crocodile-obstacle", "Crocodile Obstacle 50ft", "obstacle", "50ft",
       "50ft crocodile themed course with biff and bash, rock climb and slide.",
       ["A 50ft crocodile themed obstacle course with biff and bash sections, a rock climb and "
        "a slide at the end.",
        "Full rain cover included."],
       [("Size", "50ft"), ("Features", "Biff and bash, rock climb, slide"),
        ("Rain cover", "Full cover included")], img=IMG_OBS_CROC),
    _u("blue-yellow-obstacle", "Blue and Yellow Obstacle 50ft", "obstacle", "50ft",
       "Blue and yellow 50ft course with tunnels, a rock climb and a slide to finish.",
       ["A 50ft obstacle course in blue and yellow, with biff and bash, a rock climb, tunnels "
        "and a slide.",
        "Rain cover included."],
       [("Size", "50ft"), ("Features", "Biff and bash, rock climb, tunnels, slide"),
        ("Rain cover", "Included")], img=IMG_OBS_BLUEYELLOW),
    _u("orange-green-obstacle", "Orange and Green Obstacle 50ft", "obstacle", "50ft",
       "50ft course with biff and bash, a rock climb, tunnels and a slide.",
       ["A 50ft obstacle course in orange and green, with biff and bash sections, a rock "
        "climb, tunnels and a slide.",
        "Rain cover included."],
       [("Size", "50ft"), ("Features", "Biff and bash, rock climb, tunnels, slide"),
        ("Rain cover", "Included")], img=IMG_OBS_ORANGEGREEN),
    _u("booster-obstacle", "Booster Obstacle 45ft", "obstacle", "45ft",
       "45ft course with a slide, rock climb, tunnels and biff and bash.",
       ["The Booster is a 45ft obstacle course with a slide, a rock climb, tunnels and biff "
        "and bash sections.",
        "A good middle size where the 55ft units are too big for the space. Rain cover "
        "included."],
       [("Size", "45ft"), ("Features", "Slide, rock climb, tunnels, biff and bash"),
        ("Rain cover", "Included")], img=IMG_OBS_BOOSTER,
       gallery=(IMG_OBS_BOOSTER_2, IMG_OBS_BOOSTER_IN)),
    _u("jungle-run-obstacle", "Jungle Run Obstacle 45ft", "obstacle", "45ft",
       "45ft jungle themed course with a high slide, rock climb and biff and bash.",
       ["The Jungle Run is a 45ft obstacle course with a high slide, a rock climb and biff and "
        "bash sections.",
        "Full rain cover included."],
       [("Size", "45ft"), ("Features", "High slide, rock climb, biff and bash"),
        ("Rain cover", "Full cover included")], img=IMG_OBS_JUNGLERUN),
    _u("block-run-obstacle", "Block Run Obstacle 30ft", "obstacle", "30ft",
       "Our smallest course at 30ft, with a slide, rock climb and bounce area.",
       ["The Block Run is a 30ft obstacle course with a slide, a rock climb, a bounce area and "
        "biff and bash sections.",
        "At 30ft it fits gardens that will not take the bigger courses, and it suits younger "
        "children. Rain cover included."],
       [("Size", "30ft"), ("Features", "Slide, rock climb, bounce area, biff and bash"),
        ("Rain cover", "Included")], img=IMG_OBS_BLOCKRUN),

    # ---- disco dome ----
    _u("disco-dome", "Disco Dome 17 x 19ft", "disco", "17x19ft",
       "Enclosed dome with disco lighting and a full surround sound system.",
       ["The disco dome is an enclosed bouncing unit with disco lighting inside and a full "
        "surround speaker system.",
        "It connects over Bluetooth or by cable and works with both Apple and Android, so the "
        "kids can run their own playlist."],
       [("Size", "17ft x 19ft"), ("Lighting", "Disco lighting"),
        ("Sound", "Full surround speaker system"),
        ("Connectivity", "Bluetooth or cable, Apple and Android")], img=IMG_DISCO),

    # ---- sumo and gladiator ----
    _u("sumo-suits", "Sumo Suits", "sumo", "Groups",
       "Adult size padded sumo suits, with the mat and two helmets.",
       ["A set of padded sumo suits, adult size, with the sumo mat and two helmets.",
        "Their corporate page is where these live, so ring us for numbers and availability."],
       # "Adult supervision required" and "Teenagers" were ours. Their corporate
       # page gives the size, the mat, the two helmets and the words "We
       # specialize in corporate hire", and nothing else. Corporate stays
       # because it is theirs. The rest goes.
       [("Suit size", "Adult, 3m x 3m"), ("Comes with", "Sumo mat and two helmets"),
        ("Suits", "Adults and corporate days")], img=IMG_SUMO),
    # SOURCED, the old site's Corporate page, read 2 Sep 2026, verbatim:
    # "Sumo Suits / Adult Size 3m x 3m / Sumo Mat & 2 Helmets" and
    # "Gladiator Challenge / 5 X 5 M". Nothing here is inferred.
    _u("gladiator-challenge", "Gladiator Challenge", "sumo", "Head to head",
       "Head to head gladiator duel platform, 5m by 5m, for adults and corporate days.",
       ["The gladiator challenge is a head to head duel on a raised platform with padded "
        "poles. Two go up, one comes down.",
        "5m by 5m. Ring us for numbers and availability."],
       [("Size", "5m x 5m"), ("Format", "Head to head"),
        ("Suits", "Adults and corporate days")], img=IMG_GLADIATOR),

    # ---- marquees ----
    _u("marquee-hire", "Marquee Hire", "marquee", "All seasons",
       "Marquees in a range of sizes, with flooring, furniture, lighting and heating.",
       ["We hire marquees in a range of sizes across Tipperary and the surrounding areas, for "
        "anywhere from 20 to 100 people, and they can be used in all seasons and for all "
        "events.",
        "A marquee can go out on its own, or with flooring, tables, chairs, lighting and "
        "heating.",
        "Communions, confirmations, corporate days, birthdays and family parties. Ring us "
        "with your date and the numbers you are expecting and we will size it for you."],
       [("Sizes", "A range, sized to your numbers"), ("Numbers", "20 to 100 people"),
        ("Flooring", "Available"),
        ("Tables and chairs", "Available"), ("Lighting", "Available"),
        ("Heating", "Available"), ("Season", "All seasons")], img=IMG_MQ_LONG,
       gallery=(IMG_MQ_INSIDE, IMG_MQ_FLOOR, IMG_MQ_GRAVEL, IMG_MQ_TREE)),
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
        ("Numbers", "Sized to your guest list")], img=IMG_MQ_TABLES),
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
# TOWN COPY, REWRITTEN 2 Sep. Every one of these nine used to open with "We
# deliver to", and several closed with a drop-and-collect promise. Their site
# and Adam's emails say nothing about delivery, so all of it went. What is left
# is the part that IS sourced: Adam's 27 Aug email, "We cover all of Tipperary",
# plus the range itself. "Cover" is his word. "Deliver" was ours.
# The neighbouring villages are geography, not claims: they are in Tipperary,
# and Adam said all of Tipperary.
AREAS = [
    dict(slug="bouncy-castle-hire-clonmel", town="Clonmel", county="Co Tipperary",
         nearby="Ardfinnan, Kilsheelan and Fethard",
         copy=["We cover Clonmel and out through Ardfinnan, Kilsheelan and Fethard, with "
               "bouncy castles, combi castles and the full run of obstacle courses.",
               "Back garden birthdays, school sports days and community fun days. Ring us "
               "with your date and we will tell you what is free."]),
    dict(slug="bouncy-castle-hire-thurles", town="Thurles", county="Co Tipperary",
         nearby="Holycross, Littleton and Two Mile Borris",
         copy=["Thurles is home ground. We are based here, so it is the shortest run we do.",
               "We cover Holycross, Littleton and Two Mile Borris as well, with the full "
               "range: castles, combis, obstacle courses, the disco dome and marquees."]),
    dict(slug="bouncy-castle-hire-nenagh", town="Nenagh", county="Co Tipperary",
         nearby="Borrisokane, Newport and Puckane",
         copy=["We cover Nenagh and out around Borrisokane, Newport and Puckane, with the "
               "full range of castles and obstacle courses.",
               "If you are running a bigger day, the 55ft high adrenaline courses and the "
               "marquees come this way too. Ring us with your numbers and we will size it."]),
    dict(slug="bouncy-castle-hire-cashel", town="Cashel", county="Co Tipperary",
         nearby="Golden, Rosegreen and New Inn",
         copy=["Cashel, Golden, Rosegreen and New Inn are all inside the area we cover, for "
               "everything from a 15ft combi castle to the 55ft obstacle courses.",
               "If you are looking at communion or confirmation season, get your date in to "
               "us early."]),
    dict(slug="bouncy-castle-hire-roscrea", town="Roscrea", county="Co Tipperary",
         nearby="Templemore, Borris in Ossory and Moneygall",
         copy=["We cover Roscrea and the surrounding villages, including Templemore, Borris "
               "in Ossory and Moneygall.",
               "Castles, combis with slides, obstacle courses, the disco dome and sumo suits "
               "all come up this way."]),
    dict(slug="bouncy-castle-hire-tipperary-town", town="Tipperary Town", county="Co Tipperary",
         nearby="Bansha, Cappawhite and Dundrum",
         copy=["We cover Tipperary Town and the surrounding villages of Bansha, Cappawhite "
               "and Dundrum.",
               "Whether it is a back garden birthday or a full community fun day, there is a "
               "unit for it. Ring us and we will point you at the right one."]),
    dict(slug="bouncy-castle-hire-templemore", town="Templemore", county="Co Tipperary",
         nearby="Borrisoleigh, Loughmore and Clonmore",
         copy=["We cover Templemore, Borrisoleigh, Loughmore and Clonmore.",
               "The full range comes here: castles, combis with built in slides, obstacle "
               "courses from 30ft to 55ft, the disco dome, sumo suits and marquees."]),
    dict(slug="bouncy-castle-hire-cahir", town="Cahir", county="Co Tipperary",
         nearby="Ardfinnan, Bansha and Ballylooby",
         copy=["Cahir, Ardfinnan, Bansha and Ballylooby are all inside the area we cover.",
               "The combi castles suit younger birthdays and the 45ft and 50ft obstacle "
               "courses suit school and club days."]),
    dict(slug="bouncy-castle-hire-carrick-on-suir", town="Carrick on Suir", county="Co Tipperary",
         nearby="Kilsheelan, Piltown and Mooncoin",
         copy=["We cover Carrick on Suir and out towards Kilsheelan, Piltown and Mooncoin.",
               "Castles, obstacle courses, the disco dome and marquees all come down this "
               "end of the county. Ring us with your date and we will confirm availability."]),
]

# Old site URLs, so nothing that is already indexed or linked 404s after the
# switchover. Source paths come from bouncycastleman.com's own navigation.
REDIRECTS = [
    ("/index", "/"),
    ("/obstacle_courses", "/obstacle-courses/"),
    ("/bouncy_castles", "/bouncy-castles/"),
    # The combis moved into /bouncy-castles/ on 3 Sep when the Kiddies Bouncer
    # came off and left that category empty. This keeps every link we have
    # already sent Adam, and anything Google picked up off the draft, alive.
    ("/combi-castles", "/bouncy-castles/"),
    ("/combi-castles/", "/bouncy-castles/"),
    ("/disco_dome", "/disco-dome/"),
    ("/marquees", "/marquees/"),
    ("/gallery", "/gallery/"),
    ("/contact", "/contact/"),
]

# AREA_OPTIONS FED THE AREA CHECKER, WHICH IS GONE. Adam, 3 Sep: "We also
# don't see the benefit of the 'Do we come to you' box where you select your
# town. Once the areas are mentioned and also mentioning if your area is not
# listed please still call as we may reach you is sufficient." The town list
# and that one line are what is on the site now, on the home page, the areas
# page and the contact page. Do not rebuild the picker.

# ------------------------------------------------------------------- misc ----
# Step three used to be "We deliver and set up", describing a drop, a safety
# runthrough and a collection. None of that is on their site or in an email.
# What is left describes only the enquiry, which is the part we can stand over,
# because it is the thing this website actually does.
STEPS = [
    ("Pick your unit", "Have a look through the range and note the one you want, or ring us "
                       "and he will talk you through what suits the space and the ages."),
    ("Send us the date", "Your date, your town and the ages of the children is all we need. "
                         "Ring, WhatsApp or use the form."),
    ("We come back to you", "We confirm what is free on your date and what it costs. "
                            "Nothing is booked until we have spoken."),
]

# THREE CELLS, NOT SIX. Adam's first note on 3 Sep was that the home page shows
# too much and scrolls too long, and this bento was six cells of it. What is
# left is the three things a person actually weighs before ringing a hire firm:
# are they real, are they insured, and does rain cancel it.
#
# The three that went:
#   "Nineteen units in the range"      a COUNT. Adam asked for every count off
#                                      the site. Do not put one back.
#   "Quality, service and punctuality" their own words, but it is a slogan and
#                                      it sat beside two hard facts
#   "Every kind of day"                a list of occasions, already covered by
#                                      the copy on the area and category pages
WHY = [
    # The old site says "Established in 2001", "Family Run Business" and "20+
    # Years Experience". It says nothing about the phone number never changing,
    # so that claim is gone. Do not put a fact on this site that Adam has not
    # said somewhere first.
    ("\U0001F3F0", "Family run since " + FOUNDED,
     "Over twenty years hiring castles and courses across Tipperary, and still the same "
     "family running it."),
    ("\U0001F6E1\ufe0f", "Fully insured and IIHF certified",
     "We are fully insured and certified with the Irish Inflatable Hirers Federation, so "
     "schools and committees can book with confidence."),
    ("\u2614", "Rain covers on the range",
     "Their listings name a rain cover on castles, combis and courses alike, so an Irish "
     "forecast does not cancel the party."),
]

# TODO: placeholders. Replace with Adam's real reviews before go-live.
#
# The attributions used to be invented people: "Sarah M., Thurles", "Declan B.,
# Clonmel". On the page that reads as three real five star reviews from named
# customers in his own towns, and a client looking at a draft has no way to know
# otherwise. Quoting invented customers is not a placeholder, it is a fake
# review, and it only has to survive one approval to be live on the internet.
# The slot is named as a slot instead, and REVIEWS_NOTE labels the section.
# EMPTY ON PURPOSE. The attributions were fixed on 28 Aug ("Your review here"
# instead of invented people), but the QUOTES were still ours: "set up early,
# collected on time", "spotless condition", "great value". Nobody said those.
# A fabricated testimonial with a placeholder name on it is still a fabricated
# testimonial, and it only has to survive one approval to be live.
# pages.py renders an empty REVIEWS list as a single "your reviews go here"
# panel, so the section still shows Adam where they will sit.
REVIEWS = []
REVIEWS_NOTE = ("This is where three of your reviews will go. Send us the three you like "
                "best, or the link to where they are, and we will set them in.")

FAQS = [
    ("What can I hire?",
     "Bouncy castles with built in slides, obstacle courses from 30ft up to 55ft, a disco "
     "dome, sumo suits, the gladiator challenge and marquees."),
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

# The old site's wordmark graphic is out: it is not a photo of their work and it
# read as a mistake sitting among the units. So is the clip art castle logo, and
# so is the watermarked sumo stock shot.
# Marquees and outdoor shots lead, because they are the strongest images.
# The six "extra" obstacle shots live here and nowhere else. The old site gives
# five different inflatables the same caption, so on a unit page one of them
# would be making a claim we cannot stand over. In a gallery no photo claims to
# be a particular unit, which is exactly what these are good for.
GALLERY = [IMG_MQ_ASTRO, IMG_MQ_TABLES, IMG_OBS_BLUEYELLOW,
           IMG_MQ_LONG, IMG_OBS_MAX, IMG_MQ_INSIDE, IMG_OBS_MAX_BLUE,
           IMG_MQ_STONE, IMG_OBS_MAX_TEAL, IMG_MQ_FLOOR, IMG_OBS_MAX_RED,
           IMG_MQ_PAIR, IMG_OBS_BOOSTER_2, IMG_MQ_TREE, IMG_OBS_BOOSTER_IN,
           IMG_MQ_GRAVEL, IMG_OBS_MAX_STUDIO,
           IMG_COMBI_JUNGLE, IMG_COMBI_MINECRAFT, IMG_COMBI_COCOMELON,
           IMG_OBS_LIZARD, IMG_OBS_ORANGEGREEN, IMG_OBS_JUNGLERUN,
           IMG_OBS_BLOCKRUN, IMG_DISCO]
