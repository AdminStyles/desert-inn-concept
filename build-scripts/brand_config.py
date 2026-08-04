# -*- coding: utf-8 -*-
"""
===============================================================================
 brand_config.py -- DESERT INN SPORTS BAR & GRILL (concept build)
===============================================================================
Built 2026-08-03 as a mAIntAIn Styles concept demo -- NOT yet a paying client.
Sourced from the EHM lead pipeline (see memory: ehm-lead-pipeline-2026-08-02).

Facts verified 2026-08-03:
  - Menu, specials, About Us copy: verbatim from desertinnsportsbarandgrill.com
    (/menu/, /specials/, /about/) -- the client's own official site.
  - Phone + address: the client's own site does NOT list a phone number or
    hours anywhere (home/menu/specials/about/contact all checked). Cross-
    verified instead via Travel Oregon's Visit Central Oregon partner listing
    (traveloregon.com/things-to-do/eat-drink/restaurants/desert-inn-sports-bar-grill/),
    which quotes the address and phone directly.
  - HOURS: could not be independently verified against a primary source (their
    site has none; Yelp/Facebook pages did not load for direct confirmation).
    Left as "call ahead" rather than invented -- confirm real hours with the
    owner before this goes in front of them.
  - Establishment year (sometimes cited elsewhere as 1942): NOT used anywhere
    in this build -- only found via aggregator search summaries, not a primary
    source. Confirm with the owner if it should be added.

PHOTOS: George dropped real Desert Inn photos + the real logo into INCOMING/
2026-08-03 (sandbox network couldn't reach the client's own site to pull them
directly). Hero collage, story section, and the Taco Tuesday card now use real
photos. Wing Wednesday / Fish Fry Friday / Game Day Platter still use clearly
labeled PLACEHOLDER_*.jpg (no matching real photo of those specific dishes
yet) -- swap in real ones before this goes in front of the client. Note: the
"pet-friendly" photo on their live site (a poodle-in-a-stroller brunch-cafe
shot) is very obviously stock/generic, not actually Desert Inn -- not used
anywhere in this build.

COLORS revised 2026-08-03 -- see section 6 below.
"""

# ----------------------------------------------------------------------------
# 1. IDENTITY
# ----------------------------------------------------------------------------
BUSINESS_NAME = "Desert Inn Sports Bar & Grill"
TAGLINE       = "Metolius&rsquo; neighborhood sports bar & grill"
SITE_TYPE     = "restaurant"
CITY_STATE    = "Metolius, OR"
ESTABLISHED   = ""   # not confirmed against a primary source -- see note above
BADGE_LINE    = "SPORTS BAR &amp; GRILL &middot; METOLIUS, OR"
BRAND_SHORT   = "DESERT INN"

# ----------------------------------------------------------------------------
# 2. CONTACT & BUSINESS FACTS
# ----------------------------------------------------------------------------
PHONE_DISPLAY = "541.546.7937"
PHONE_TEL     = "+15415467937"
ADDRESS_FULL  = "385 Jefferson Ave, Metolius, OR 97741"
HOURS_TEXT    = "Call ahead for today&rsquo;s hours"   # not independently verified -- confirm with owner
EMAIL         = "admin@desertinnsportsbarandgrill.com"   # pulled from their own contact page code; footer icon only -- George is calling first, not emailing, so confirm real inbox before relying on it for outreach
MAP_EMBED_URL = "https://www.google.com/maps?q=Desert+Inn+Sports+Bar+%26+Grill,385+Jefferson+Ave,Metolius,OR+97741&output=embed"

# ----------------------------------------------------------------------------
# 3. SOCIAL
# ----------------------------------------------------------------------------
INSTAGRAM_URL    = ""   # not found
INSTAGRAM_HANDLE = ""
FACEBOOK_URL     = "https://www.facebook.com/DesertInnBarandGrill/"

# ----------------------------------------------------------------------------
# 4. ORDERING / MENU LINKS
# ----------------------------------------------------------------------------
ORDER_URL   = "tel:+15415467937"   # no online ordering on their live site
ORDER_LABEL = "CALL TO ORDER"
CTA_CALL_LABEL = "CALL"
MENU_MODE      = "items"
MENU_EMBED_URL = ""

# ----------------------------------------------------------------------------
# 5. DEPLOY / HOSTING
# ----------------------------------------------------------------------------
PROJECT_SLUG    = "desert-inn-concept"
LIVE_URL        = "https://desert-inn-concept.pages.dev"   # placeholder until first deploy
SOURCE_OF_TRUTH = ("desertinnsportsbarandgrill.com (menu/specials/about) -- "
                    "phone & address cross-verified via Travel Oregon / Visit "
                    "Central Oregon partner listing, since the client's own "
                    "site lists neither.")
FOOTER_LABEL    = "Desert Inn Sports Bar &amp; Grill - Website Concept"

# ----------------------------------------------------------------------------
# 6. DESIGN TOKENS -- REVISED 2026-08-03 per George: dropped the indigo-plum
#    direction (he liked it but wants to save it for a different client) and
#    rebuilt the palette from Desert Inn's ACTUAL logo (INCOMING/logo.png --
#    a saguaro cactus + red-orange sunset circle + gold/tan lettering), plus
#    their real bar-interior photo (assets/gallery-08-bar.jpg), which has the
#    same rust-orange floor + sage-green accents. Accent orange is deliberately
#    darker/more burnt than the bright logo sun, per George's note.
#    The sage-green "glow" is the differentiator vs. Fat Tony's / Barney
#    Prine's (both warm-dark + gold/brass, no green) -- neither of them has
#    anything like it, and it's grounded in this client's real branding, not
#    invented. Distinct from Simon's (teal/yellow/red), Miracle Greens
#    (brighter green/orange), Tacos (navy/red).
# ----------------------------------------------------------------------------
COLORS = {
    "primary":        "#2a1710",   # warm umber-brown desert-night -- hero/cta gradient start
    "primary_bright": "#4e2c14",   # warm brown-orange gradient mid-stop
    "primary_deep":   "#140b06",   # near-black warm brown, deepest gradient stop
    "glow":           "#7c9a52",   # cactus/sage green -- from the logo's saguaro + the real bar interior's green accents
    "accent":         "#fb991c",   # their live site's actual bright orange (rgb(251,153,28), sampled from desertinnsportsbarandgrill.com) -- buttons/CTAs
    "accent_deep":    "#b46e14",   # darker shade of that same orange, for hover
    "on_accent":      "#1c0e05",   # dark text on orange
    "cream":          "#f0e0ba",   # warm gold-tan -- echoes the logo's lettering
    "cream_muted":    "#b8a37a",   # muted tan
    "bg_deep":        "#120a05",   # near-black warm brown background
    "panel":          "#211208",   # dark umber panel
    "ink":            "#1c0e05",   # dark text on light surfaces
}

FONT_HEADING       = "Staatliches"   # condensed bold poster/scoreboard face -- distinct from every other client's heading font
FONT_BODY          = "Inter"
# Nav wordmark only (next to the logo image) uses a separate font matching the
# real logo's bold high-contrast serif "D I" lettering -- George's request
# 2026-08-03. Everything else (hero, section headings) stays Staatliches.
NAV_WORDMARK_FONT  = "Abril Fatface"
NAV_WORDMARK_BOLD  = False   # George 2026-08-03: remove the bold weight from the nav text
GOOGLE_FONTS_HREF  = ("https://fonts.googleapis.com/css2?"
                      "family=Staatliches&"
                      "family=Abril+Fatface&"
                      "family=Inter:wght@400;500;600;700&display=swap")

# ----------------------------------------------------------------------------
# 7. AGE GATE (full-bar restaurant, not a dispensary -- off, same as Fat
#    Tony's / Barney Prine's)
# ----------------------------------------------------------------------------
AGE_GATE_ENABLED = False
AGE_GATE_MIN     = 21
AGE_GATE_TITLE   = "Are You 21 or Older?"
AGE_GATE_YES     = "Yes, enter"
AGE_GATE_NO      = "No"
AGE_GATE_BOUNCE  = "https://www.google.com"
AGE_GATE_DAYS    = 30

# ----------------------------------------------------------------------------
# 8. COMPLIANCE FOOTER LINES
# ----------------------------------------------------------------------------
COMPLIANCE_LINES = []

# ----------------------------------------------------------------------------
# 9. HERO -- George's pick: Hero 4 (stacked photo collage), approved 2026-08-03
#    as a new opt-in Add-on (see site_common.py / build_homepage.py). Real
#    photos dropped into INCOMING/ by George 2026-08-03 -- these are genuine
#    Desert Inn photos (burger, bar interior, dessert+local Deschutes beer),
#    not stock/placeholder.
# ----------------------------------------------------------------------------
LOGO_IMAGE   = "assets/logo.png"
HERO_STYLE   = "collage"
HERO_COLLAGE_PHOTOS = [
    ("assets/gallery-01-burger.jpg", "A burger and onion rings at Desert Inn Sports Bar & Grill"),
    ("assets/gallery-09-shrimp.jpg", "A shrimp appetizer at Desert Inn Sports Bar & Grill"),
    ("assets/gallery-11-dessert-beer.jpg", "Dessert and a local Deschutes Brewery beer at Desert Inn"),
]
HERO_HEADING = 'Your destination for<br><span class="accent">sports and fun</span>'
HERO_SUB     = ("Indoor and outdoor dining or carryout in Metolius. A full bar, "
                "wall-to-wall game coverage, and a menu of the food you actually "
                "want after the final whistle.")
HERO_PHOTO   = ""      # unused when HERO_STYLE == "collage"
HERO_SLIDES  = []       # unused when HERO_STYLE == "collage"

# ----------------------------------------------------------------------------
# 9b. BACK-TO-TOP ICON -- saguaro cactus, dropped by George 2026-08-03, ties
#     straight to the logo's cactus and the "desert" in Desert Inn.
# ----------------------------------------------------------------------------
TOTOP_ICON        = "assets/cactus-svgrepo-com.svg"
TOTOP_ICON_ROTATE = 0

# ----------------------------------------------------------------------------
# 10. TRUST STRIP -- all sourced from the client's own site copy
# ----------------------------------------------------------------------------
TRUST_ITEMS = [
    ("Live Music &amp; Events", "Entertainment"),
    ("Beer, Wine, &amp; Liquor", "Full Bar"),
    ("Indoor &amp; Outdoor", "Dining or carryout"),
    ("Pet-Friendly", "Patio seating"),
]

# ----------------------------------------------------------------------------
# 11. FEATURE CARDS -- real Desert Inn photos, dropped by George 2026-08-03:
#     the actual dining room TV (game on, cactus mural behind it), the real
#     bar (reused from the hero collage), and their own hand-painted
#     "Desert Inn Family Restaurant" sign.
# ----------------------------------------------------------------------------
FEATURES = [
    ("1", "Game day, every day", "Multiple TVs throughout the venue for football, basketball, baseball, hockey, and more.", "assets/feature-gameday-tv.jpg"),
    ("2", "Full bar", "A wide selection of beer, wine, and liquor &mdash; something for everyone.", "assets/gallery-08-bar.jpg"),
    ("3", "Family &amp; pet friendly", "Indoor and outdoor dining, carryout, and a pet-friendly patio.", "assets/feature-pet-friendly.jpg"),
]
FAVORITES = None   # no per-dish photos yet -- falls back to FEATURES above

# ----------------------------------------------------------------------------
# 12. SPECIALS -- shown via the new EVENTS_SNAP add-on (Scroll 4, George's
#     pick) below instead of the classic specials block, to demo the pattern
#     he asked to see. All items/prices verbatim from /specials/.
# ----------------------------------------------------------------------------
SPECIALS_ENABLED = False
EVENTS_SNAP_TAG   = "WEEKLY SPECIALS"
EVENTS_SNAP_TITLE = "Something&rsquo;s always on"
EVENTS_SNAP = [
    ("assets/gallery-03-tacos.jpg", "Real tacos at Desert Inn Sports Bar & Grill", "Taco Tuesday", "3 tacos &mdash; $9.99", "\U0001F32E"),
    (None, "", "Wing Wednesday", "10 wings &mdash; $12.99", "\U0001F357"),
    ("assets/gallery-fishfry.jpg", "Real fish and chips at Desert Inn Sports Bar & Grill", "Fish Fry Friday", "$14.99", "\U0001F41F"),
    (None, "", "Game Day Platter", "$26.99 &mdash; built for a crowd", "\U0001F3C8"),
]

# Full specials list -- the homepage strip above only shows 4 as a curated
# teaser (that's all that pattern was ever meant to hold); their live site
# has a dedicated Specials page with 20 items, so we need one too instead of
# quietly dropping the other 16. Verbatim from /specials/, checked 2026-08-03.
SPECIALS_PAGE_TAG   = "SPECIALS"
SPECIALS_PAGE_TITLE = "Desert Inn Specials"
SPECIALS_PAGE_INTRO = "Something good every day of the week &mdash; here&rsquo;s the full list."
SPECIALS_LIST = [
    ("Daily Lunch Special", "", "$10.99"),
    ("Burger &amp; Fries Special", "", "$11.99"),
    ("Taco Tuesday", "3 tacos", "$9.99"),
    ("Wing Wednesday", "10 wings", "$12.99"),
    ("Fish Fry Friday", "", "$14.99"),
    ("Steak Night Special", "", "$18.99"),
    ("BBQ Ribs Dinner", "", "$17.99"),
    ("Prime Rib Special", "", "$21.99"),
    ("Chicken Fried Steak Special", "", "$15.99"),
    ("Grilled Salmon Special", "", "$18.49"),
    ("Family Pizza Special", "", "$24.99"),
    ("Game Day Platter", "", "$26.99"),
    ("Happy Hour Appetizer Combo", "", "$13.99"),
    ("Soup &amp; Sandwich Combo", "", "$10.49"),
    ("Chicken Tender Basket Special", "", "$12.49"),
    ("Loaded Nachos Special", "", "$11.99"),
    ("Pulled Pork Sandwich Combo", "", "$13.99"),
    ("Two Cheeseburger Combo", "", "$17.99"),
    ("Shrimp Basket Special", "", "$15.99"),
    ("Weekend Breakfast Special", "", "$11.49"),
]

# ----------------------------------------------------------------------------
# 13. STORY SECTION -- condensed from the client's own About Us copy
# ----------------------------------------------------------------------------
STORY_IMAGE     = "assets/story-welcome-patio.jpg"
STORY_IMAGE_ALT = "The welcome sign over the patio at Desert Inn Sports Bar & Grill"
STORY_TAG   = "OUR STORY"
STORY_TITLE = "More than just a sports bar"
STORY_BODY  = ("Desert Inn Sports Bar &amp; Grill is Metolius&rsquo; neighborhood "
               "destination for great food, refreshing drinks, and an exciting "
               "sports bar atmosphere. With TVs throughout the venue, catch "
               "football, basketball, baseball, hockey, and more while you eat. "
               "It&rsquo;s a place for friends, families, coworkers, and visitors "
               "to relax, celebrate, and make it a regular stop.")

# ----------------------------------------------------------------------------
# 14. CTA BAND
# ----------------------------------------------------------------------------
CTA_TITLE  = "Come watch the game"
CTA_SUB    = "385 Jefferson Ave, Metolius, OR &middot; Call ahead for today&rsquo;s hours"
CTA_BUTTON = "VIEW MENU"
CTA_BUTTON_URL = "__MENU__"   # no online ordering, and the CALL button next to it already covers phone -- send this one to the menu instead
CTA_SHOW_CALL = True

# ----------------------------------------------------------------------------
# 14b. FIND US
# ----------------------------------------------------------------------------
LOCATION_SECTION_ID = "find"

# ----------------------------------------------------------------------------
# 15. FULL MENU (verified verbatim against desertinnsportsbarandgrill.com/menu/
#     2026-08-03)
# ----------------------------------------------------------------------------
MENU_INTRO = ""
MENU_SECTIONS = [
    ("Appetizers", "appetizers", [
        ("Mozzarella Sticks", "", "$8.99"),
        ("Onion Rings", "", "$7.99"),
        ("Loaded Nachos", "", "$11.99"),
        ("Fried Pickles", "", "$7.49"),
        ("Jalape&ntilde;o Poppers", "", "$8.49"),
        ("Chicken Quesadilla", "", "$10.99"),
        ("Potato Skins", "", "$9.49"),
        ("Chips &amp; Salsa", "", "$5.99"),
    ]),
    ("Burgers", "burgers", [
        ("Classic Cheeseburger", "", "$12.99"),
        ("Bacon Cheeseburger", "", "$14.49"),
        ("Mushroom Swiss Burger", "", "$14.99"),
        ("BBQ Burger", "", "$14.99"),
        ("Jalape&ntilde;o Burger", "", "$14.49"),
        ("Double Burger", "", "$16.99"),
        ("Western Burger", "", "$15.49"),
        ("Patty Melt", "", "$13.99"),
    ]),
    ("Sandwiches &amp; Wraps", "sandwiches", [
        ("Grilled Chicken Sandwich", "", "$12.99"),
        ("Philly Cheesesteak", "", "$14.99"),
        ("BLT Sandwich", "", "$10.99"),
        ("Club Sandwich", "", "$13.49"),
        ("Buffalo Chicken Wrap", "", "$12.99"),
        ("Turkey Wrap", "", "$11.99"),
        ("French Dip", "", "$14.49"),
        ("BBQ Pulled Pork Sandwich", "", "$13.99"),
    ]),
    ("Pizza", "pizza", [
        ("Cheese Pizza", "", "$13.99"),
        ("Pepperoni Pizza", "", "$15.49"),
        ("Meat Lovers Pizza", "", "$18.99"),
        ("Supreme Pizza", "", "$18.99"),
        ("BBQ Chicken Pizza", "", "$17.99"),
        ("Hawaiian Pizza", "", "$16.99"),
        ("Veggie Pizza", "", "$16.49"),
        ("Custom Pizza", "", "$17.99"),
    ]),
    ("Baskets", "baskets", [
        ("Fish &amp; Chips Basket", "", "$15.99"),
        ("Chicken Strip Basket", "", "$13.99"),
        ("Shrimp Basket", "", "$16.99"),
        ("Popcorn Chicken Basket", "", "$12.99"),
        ("Crispy Fish Basket", "", "$15.49"),
        ("Chicken Wings Basket", "", "$14.99"),
    ]),
    ("Salads", "salads", [
        ("House Salad", "", "$8.99"),
        ("Caesar Salad", "", "$9.99"),
        ("Chef Salad", "", "$12.99"),
        ("Grilled Chicken Salad", "", "$13.99"),
        ("Crispy Chicken Salad", "", "$13.99"),
        ("Taco Salad", "", "$12.99"),
    ]),
    ("Wings", "wings", [
        ("6 Piece Wings", "", "$9.99"),
        ("10 Piece Wings", "", "$14.99"),
        ("15 Piece Wings", "", "$20.99"),
        ("20 Piece Wings", "", "$26.99"),
        ("Boneless Wings", "", "$12.99"),
    ]),
    ("Sides", "sides", [
        ("French Fries", "", "$3.99"),
        ("Tater Tots", "", "$4.49"),
        ("Coleslaw", "", "$2.99"),
        ("Side Salad", "", "$4.99"),
        ("Onion Rings", "", "$5.49"),
        ("Sweet Potato Fries", "", "$5.99"),
    ]),
    ("Desserts", "desserts", [
        ("Chocolate Cake", "", "$6.99"),
        ("Cheesecake", "", "$6.99"),
        ("Ice Cream Sundae", "", "$5.99"),
        ("Brownie with Ice Cream", "", "$7.49"),
        ("Apple Pie", "", "$5.99"),
    ]),
    ("Beverages", "beverages", [
        ("Fountain Soda", "", "$2.99"),
        ("Iced Tea", "", "$2.99"),
        ("Lemonade", "", "$3.49"),
        ("Coffee", "", "$2.49"),
        ("Hot Tea", "", "$2.49"),
        ("Bottled Water", "", "$1.99"),
    ]),
]

# ----------------------------------------------------------------------------
# 16. CATERING (not mentioned on their site -- off)
# ----------------------------------------------------------------------------
CATERING_ENABLED  = False
CATERING_INTRO    = ""
CATERING_EMAIL    = EMAIL
CATERING_PACKAGES = []

# ----------------------------------------------------------------------------
# ADMIN STYLES PIN -- placeholder, change before this goes live.
# ----------------------------------------------------------------------------
ADMIN_STYLES_PIN = "4620"   # PLACEHOLDER -- set a real PIN before this goes live
