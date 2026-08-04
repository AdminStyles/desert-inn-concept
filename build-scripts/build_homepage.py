# -*- coding: utf-8 -*-
"""
build_homepage.py -- generates the homepage (root working copy + site/index.html).
Works for any SITE_TYPE. Edit facts/colors in brand_config.py, then run:
    python build-scripts/build_homepage.py

Bilingual: every section pulls an optional *_ES translation from
es_translations.py via the safe _es()/_es_pairs() helpers below. A client that
hasn't filled in a given *_ES variable yet just falls back to the English copy
for that piece -- the build never breaks over a missing translation.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_config as C
import site_common as S
import es_translations as ES

def _es(en, attr):
    """Safe single-value ES lookup -- getattr with an English fallback so a
    client that hasn't translated this piece yet still builds cleanly."""
    return getattr(ES, attr, en)

def _es_pairs(en_list, attr):
    """Safe ES lookup for a list of tuples that zips against an English list
    (TRUST_ITEMS, FEATURES, EVENTS_SNAP...). Falls back to the English tuple
    itself, position by position, if the ES list is missing or shorter."""
    es_list = getattr(ES, attr, None) or []
    return [(es_list[i] if i < len(es_list) else en_list[i]) for i in range(len(en_list))]

def _slide_entry(p):
    """A HERO_SLIDES item may be a plain path (cover crop) or a (path, 'contain')
    tuple for a non-square promo flyer that must not be cropped (Fat Tony's
    Happy Hour / BOGO flyers)."""
    if isinstance(p, (tuple, list)):
        path, mode = p[0], (p[1] if len(p) > 1 else "cover")
    else:
        path, mode = p, "cover"
    return path, mode

def hero():
    logo = f'<img class="hero-logo" src="{S.embed_img(C.LOGO_IMAGE)}" alt="">' if C.LOGO_IMAGE else ""
    style = getattr(C, "HERO_STYLE", "classic")
    badge_es = _es(C.BADGE_LINE, "HERO_BADGE_ES")
    heading_es = _es(C.HERO_HEADING, "HERO_HEADING_ES")
    sub_es = _es(C.HERO_SUB, "HERO_SUB_ES")
    menu_btn_es = _es("View full menu", "HERO_MENU_BTN_ES")
    order_label_es = _es(C.ORDER_LABEL, "ORDER_LABEL_ES")
    if style == "collage":
        # Add-on: Hero 4 - stacked photo collage. 2-3 photos, no single 340px
        # square frame (that's the classic-hero convention, unchanged below).
        photos = getattr(C, "HERO_COLLAGE_PHOTOS", None) or []
        imgs = "".join(
            f'<div class="cimg"><img src="{S.embed_img(p)}" alt="{alt}"></div>'
            for p, alt in photos[:3])
        photo = (f'<div class="hero-photo"><div class="hero-photo-inner">'
                 f'<div class="hero-collage">{imgs}</div>{logo}</div></div>')
        order_btn = (f'<a class="btn btn-primary" href="{C.ORDER_URL}" target="_blank" '
                     f'rel="noopener" data-es="{order_label_es}">{C.ORDER_LABEL}</a>')
        menu_btn = (f'<a class="btn btn-ghost" href="__MENU__" data-es="{menu_btn_es}">View full menu</a>'
                    if C.MENU_MODE != "none" else "")
        return f"""<section class="hero" data-section="HERO"><div class="wrap">
  {photo}
  <div class="hero-text">
    <span class="badge-pill" data-es="{badge_es}">{C.BADGE_LINE}</span>
    <h1 data-es-html='{heading_es}'>{C.HERO_HEADING}</h1>
    <p class="lead" data-es="{sub_es}">{C.HERO_SUB}</p>
    <div class="hero-btns">{order_btn}{menu_btn}</div>
  </div>
</div></section>"""
    slides = C.HERO_SLIDES or [C.HERO_PHOTO]
    if len(slides) > 1:
        n = len(slides)
        hold = 7                     # seconds each slide is fully, solely visible
        fade = 1                     # seconds of true crossfade overlap between slides
        dur = n * hold
        # True dissolve: delay spacing is `hold` (not hold+fade), so image i's
        # fade-OUT window and image i+1's fade-IN window land on the exact same
        # real-time span -- one is going 1->0 while the next is going 0->1 at
        # the same moment, so full opacity never drops to 0 and the background
        # is never revealed between slides (unlike a spacing of hold+fade,
        # which schedules them back-to-back with a visible gap at the seam).
        fade_pct = fade / dur * 100
        hold_end_pct = hold / dur * 100
        fadeout_end_pct = (hold + fade) / dur * 100
        kf = ("@keyframes heroFade{0%{opacity:0}"
              f"{fade_pct:.3f}%{{opacity:1}}{hold_end_pct:.3f}%{{opacity:1}}"
              f"{fadeout_end_pct:.3f}%{{opacity:0}}100%{{opacity:0}}}}")
        imgs = []
        for i, p in enumerate(slides):
            path, mode = _slide_entry(p)
            cls = ' class="contain"' if mode == "contain" else ""
            imgs.append(f'<img{cls} style="animation-delay:{i*hold}s" src="{S.embed_img(path)}" alt="{C.BUSINESS_NAME}">')
        imgs = "".join(imgs)
        photo = (f'<style>{kf}</style>'
                 f'<div class="hero-photo"><div class="hero-photo-inner">'
                 f'<div class="hero-frame" style="--fadedur:{dur}s">{imgs}</div>{logo}</div></div>')
    else:
        path, mode = _slide_entry(slides[0])
        cls = "single contain" if mode == "contain" else "single"
        photo = (f'<div class="hero-photo"><div class="hero-photo-inner"><div class="hero-frame">'
                 f'<img class="{cls}" src="{S.embed_img(path)}" alt="{C.BUSINESS_NAME}"></div>{logo}</div></div>')
    order_btn = (f'<a class="btn btn-primary" href="{C.ORDER_URL}" target="_blank" '
                 f'rel="noopener" data-es="{order_label_es}">{C.ORDER_LABEL}</a>')
    menu_btn = (f'<a class="btn btn-ghost" href="__MENU__" data-es="{menu_btn_es}">View full menu</a>'
                if C.MENU_MODE != "none" else "")
    return f"""<section class="hero" data-section="HERO"><div class="wrap">
  {photo}
  <div class="hero-text">
    <span class="badge-pill" data-es="{badge_es}">{C.BADGE_LINE}</span>
    <h1 data-es-html='{heading_es}'>{C.HERO_HEADING}</h1>
    <p class="lead" data-es="{sub_es}">{C.HERO_SUB}</p>
    <div class="hero-btns">{order_btn}{menu_btn}</div>
  </div>
</div></section>"""

def trust():
    # Fat Tony's two-line stat blocks: bold value over a small label.
    es_items = _es_pairs(C.TRUST_ITEMS, "TRUST_ES")
    items = "".join(
        f'<div class="trust-item"><div class="num" data-es="{a_es}">{a}</div>'
        f'<div class="lbl" data-es="{b_es}">{b}</div></div>'
        for (a, b), (a_es, b_es) in zip(C.TRUST_ITEMS, es_items))
    return f'<section class="trust" data-section="TRUST"><div class="wrap">{items}</div></section>'

def favorites():
    """Fat Tony's pattern: a 4-up photo-card grid ('what people order first'),
    not the generic icon-card features. Set FAVORITES in brand_config to use
    this; falls back to the icon-card FEATURES layout if not set (other clients
    that don't have per-dish photos yet)."""
    items = getattr(C, "FAVORITES", None)
    if items:
        cards = "".join(
            f'<div class="photo-card"><div class="img"><img src="{S.embed_img(img)}" alt="{alt}"></div>'
            f'<h3>{title}</h3><p>{desc} &mdash; <span class="price">{price}</span></p></div>'
            for img, alt, title, desc, price in items)
        note = getattr(C, "FAVORITES_NOTE", "")
        note_html = f'<p class="sec-note">{note}</p>' if note else ""
        tag = getattr(C, "FAVORITES_TAG", "CROWD FAVORITES")
        title = getattr(C, "FAVORITES_TITLE", "What people order first")
        return (f'<section class="sec" id="favorites" data-section="FAVORITES"><div class="wrap">'
                f'<div class="sec-head"><span class="sec-tag">{tag}</span><h2>{title}</h2></div>'
                f'<div class="photo-cards">{cards}</div>{note_html}</div></section>')
    if not getattr(C, "FEATURES", None):
        return ""
    # Each FEATURES entry is (icon, title, desc) or, opt-in, (icon, title, desc,
    # img) -- when img is set it replaces the letter/number icon box with a
    # real photo. Backward compatible: every client still on 3-tuples is unaffected.
    norm_features = [(f[0], f[1], f[2], f[3] if len(f) > 3 else None) for f in C.FEATURES]
    es_items = _es_pairs([(t, d) for _, t, d, _ in norm_features], "FEATURES_ES")
    cards = "".join(
        (f'<div class="card"><div class="img"><img src="{S.embed_img(img)}" alt="{t}"></div>'
         if img else f'<div class="card"><div class="ic">{ic}</div>')
        + f'<h3 data-es="{t_es}">{t}</h3><p data-es="{d_es}">{d}</p></div>'
        for (ic, t, d, img), (t_es, d_es) in zip(norm_features, es_items))
    why_es = _es(f"WHY {C.BUSINESS_NAME.upper()}", "FAVORITES_WHY_ES")
    sets_apart_es = _es("What sets us apart", "FAVORITES_SETS_APART_ES")
    return (f'<section class="sec wrap" data-section="FAVORITES"><div class="sec-head">'
            f'<span class="sec-tag" data-es="{why_es}">WHY {C.BUSINESS_NAME.upper()}</span>'
            f'<h2 data-es="{sets_apart_es}">What sets us apart</h2></div><div class="cards">{cards}</div></section>')


def specials():
    """Fat Tony's pattern: up to 3 specials in a photo-card grid (SPECIALS list).
    Falls back to the single centered special block (SPECIALS_ENABLED) for
    clients with just one promo."""
    multi = getattr(C, "SPECIALS", None)
    if multi:
        es_items = _es_pairs([(tag, title, body) for _, _, tag, title, body in multi], "SPECIALS_MULTI_ES")
        cards = "".join(
            f'<div class="special-card"><div class="img"><img src="{S.embed_img(img)}" alt="{alt}"></div>'
            f'<div class="body"><div class="tag" data-es="{tag_es}">{tag}</div>'
            f'<h3 data-es="{title_es}">{title}</h3><p data-es="{body_es}">{body}</p></div></div>'
            for (img, alt, tag, title, body), (tag_es, title_es, body_es) in zip(multi, es_items))
        sec_tag = getattr(C, "SPECIALS_SECTION_TAG", "THIS WEEK")
        sec_title = getattr(C, "SPECIALS_SECTION_TITLE", "Specials worth planning around")
        sec_tag_es = _es(sec_tag, "SPECIALS_SECTION_TAG_ES")
        sec_title_es = _es(sec_title, "SPECIALS_SECTION_TITLE_ES")
        return (f'<section class="sec" id="specials" data-section="SPECIALS"><div class="wrap">'
                f'<div class="sec-tag" style="text-align:left" data-es="{sec_tag_es}">{sec_tag}</div>'
                f'<h2 style="text-align:left;margin-bottom:44px" data-es="{sec_title_es}">{sec_title}</h2>'
                f'<div class="specials-grid">{cards}</div></div></section>')
    if not getattr(C, "SPECIALS_ENABLED", False):
        return ""
    tag_es = _es(C.SPECIALS_TAG, "SPECIALS_TAG_ES")
    title_es = _es(C.SPECIALS_TITLE, "SPECIALS_TITLE_ES")
    body_es = _es(C.SPECIALS_BODY, "SPECIALS_BODY_ES")
    cta_es = _es(C.SPECIALS_CTA, "SPECIALS_CTA_ES")
    return f"""<section class="sec" id="specials" data-section="SPECIALS"><div class="special">
  <span class="tag" data-es="{tag_es}">{C.SPECIALS_TAG}</span>
  <h3 data-es="{title_es}">{C.SPECIALS_TITLE}</h3>
  <p data-es="{body_es}">{C.SPECIALS_BODY}</p>
  <a class="btn btn-primary" href="{C.ORDER_URL}" target="_blank" rel="noopener" data-es="{cta_es}">{C.SPECIALS_CTA}</a>
</div></section>"""

def events_snap():
    """Add-on: Scroll 4 - horizontal scroll-snap gallery. Opt-in via EVENTS_SNAP
    in brand_config.py: a list of (img, alt, title, desc) tuples, or (img, alt,
    title, desc, icon) with an optional 5th emoji/icon element. img may be None
    for an item with no real photo yet -- renders a promo-ad-style placeholder
    (diagonal "SPECIAL" ribbon + a circular price badge, price auto-pulled from
    `desc` if it contains a $ amount + an oversized faded watermark icon) in
    the client's own palette instead of a broken image or a plain "coming
    soon" box, using `icon` if given or a default. Built for recurring weekly
    specials/events (game nights, trivia, taco night...); empty/unset on every
    client that doesn't set it, so it's additive only."""
    items = getattr(C, "EVENTS_SNAP", None)
    if not items:
        return ""
    tag = getattr(C, "EVENTS_SNAP_TAG", "THIS WEEK")
    title = getattr(C, "EVENTS_SNAP_TITLE", "Something's always on")
    ribbon_word = getattr(C, "EVENTS_SNAP_RIBBON", "SPECIAL")
    tag_es = _es(tag, "EVENTS_SNAP_TAG_ES")
    title_es = _es(title, "EVENTS_SNAP_TITLE_ES")
    ribbon_es = _es(ribbon_word, "EVENTS_SNAP_RIBBON_ES")
    coming_soon_es = _es("Photo coming soon", "EVENTS_SNAP_COMING_SOON_ES")
    norm_items = [(it[0], it[1], it[2], it[3], it[4] if len(it) > 4 else "\U0001F374") for it in items]
    es_items = _es_pairs([(t, d) for _, _, t, d, _ in norm_items], "EVENTS_SNAP_ES")
    price_re = re.compile(r"\$[\d,]+(?:\.\d{2})?")
    def _photo_block(img, alt, icon, desc):
        if img:
            return f'<div class="ph"><img src="{S.embed_img(img)}" alt="{alt}"></div>'
        m = price_re.search(desc)
        if m:
            amt, lbl = m.group(0), "each" if "each" in desc.lower() else "special"
        else:
            amt, lbl = icon, "special"
        return (f'<div class="ph ph-placeholder">'
                f'<div class="ph-ribbon" data-es="{ribbon_es}">{ribbon_word}</div>'
                f'<div class="ph-icon-bg">{icon}</div>'
                f'<div class="ph-badge"><span class="amt">{amt}</span><span class="lbl">{lbl}</span></div>'
                f'<div class="ph-tag" data-es="{coming_soon_es}">Photo coming soon</div>'
                f'</div>')
    cards = "".join(
        f'<div class="card">{_photo_block(img, alt, icon, d)}'
        f'<div class="body"><h4 data-es="{t_es}">{t}</h4><p data-es="{d_es}">{d}</p></div></div>'
        for (img, alt, t, d, icon), (t_es, d_es) in zip(norm_items, es_items))
    return (f'<section class="sec" id="events" data-section="EVENTS"><div class="wrap">'
            f'<div class="sec-tag" style="text-align:left" data-es="{tag_es}">{tag}</div>'
            f'<h2 style="text-align:left;margin-bottom:32px" data-es="{title_es}">{title}</h2>'
            f'<div class="snap-row">{cards}</div></div></section>')

def story():
    """Fat Tony's pattern: photo + text side by side (STORY_IMAGE). Falls back
    to the info-card layout for clients without a story photo yet."""
    # Instagram callout in the story section is opt-in only (STORY_SHOW_INSTA) --
    # V1 doesn't have one here (Instagram already lives in the footer social
    # icons), so it must never appear unless a client explicitly asks for it.
    insta = ""
    if getattr(C, "STORY_SHOW_INSTA", False) and C.INSTAGRAM_URL:
        handle = C.INSTAGRAM_HANDLE or "Follow us"
        insta = (f'<p><a class="btn btn-ghost" href="{C.INSTAGRAM_URL}" target="_blank" '
                 f'rel="noopener">{handle} on Instagram</a></p>')
    tag_es = _es(C.STORY_TAG, "STORY_TAG_ES")
    title_es = _es(C.STORY_TITLE, "STORY_TITLE_ES")
    body_es = _es(C.STORY_BODY, "STORY_BODY_ES")
    story_img = getattr(C, "STORY_IMAGE", "")
    if story_img:
        img_html = f'<div class="story-img"><img src="{S.embed_img(story_img)}" alt="{C.STORY_IMAGE_ALT}"></div>'
        return f"""<section class="sec wrap" id="story" data-section="STORY"><div class="story-flex">
  {img_html}
  <div class="story-text">
    <h2 data-es="{title_es}">{C.STORY_TITLE}</h2>
    <p class="lead" data-es="{body_es}">{C.STORY_BODY}</p>
    {insta}
  </div>
</div></section>"""
    return f"""<section class="sec wrap" id="story" data-section="STORY"><div class="split">
  <div>
    <span class="sec-tag" data-es="{tag_es}">{C.STORY_TAG}</span>
    <h2 data-es="{title_es}">{C.STORY_TITLE}</h2>
    <p class="lead" data-es="{body_es}">{C.STORY_BODY}</p>
    {insta}
  </div>
  <div class="card" style="padding:34px">
    <h3>{C.BUSINESS_NAME}</h3>
    <p style="color:var(--cream-muted)">{C.CITY_STATE}{(' &middot; Since ' + C.ESTABLISHED) if C.ESTABLISHED else ''}</p>
    <p style="margin-top:12px">{C.TAGLINE}</p>
  </div>
</div></section>"""

def cta_band():
    """Fat Tony's pattern: optional award-plaque images flank the message,
    with Order + Call buttons. Falls back to a single order button/no plaques
    for clients without award badges."""
    plaques = getattr(C, "CTA_PLAQUES", None) or []
    plaque_html = [f'<div class="cta-plaque"><img src="{S.embed_img(img)}" alt="{alt}"></div>' for img, alt in plaques]
    left_plaque = plaque_html[0] if len(plaque_html) > 0 else ""
    right_plaque = plaque_html[1] if len(plaque_html) > 1 else ""
    call_label_es = _es("CALL", "CALL_LABEL_ES")
    call_btn = (f'<a class="btn btn-ghost" href="tel:{C.PHONE_TEL}" data-es="{call_label_es} {C.PHONE_DISPLAY}">CALL {C.PHONE_DISPLAY}</a>'
                if getattr(C, "CTA_SHOW_CALL", bool(plaques)) else "")
    title_es = _es(C.CTA_TITLE, "CTA_TITLE_ES")
    sub_es = _es(C.CTA_SUB, "CTA_SUB_ES")
    button_es = _es(C.CTA_BUTTON, "CTA_BUTTON_ES")
    # Opt-in: CTA_BUTTON_URL lets the primary CTA point somewhere other than
    # ORDER_URL (e.g. "__MENU__" for a "View Menu" CTA on a client with no
    # online ordering). Defaults to ORDER_URL for every existing client, so
    # this is additive/backward-compatible. Internal site tokens (start with
    # "__") skip target="_blank"/rel="noopener" since they're same-site links.
    cta_url = getattr(C, "CTA_BUTTON_URL", None) or C.ORDER_URL
    cta_ext_attrs = "" if cta_url.startswith("__") else ' target="_blank" rel="noopener"'
    return f"""<section class="cta-band" data-section="CTA"><div class="wrap">
  {left_plaque}
  <div class="center">
    <h2 data-es="{title_es}">{C.CTA_TITLE}</h2><p data-es="{sub_es}">{C.CTA_SUB}</p>
    <div class="cta-buttons">
      <a class="btn btn-primary" href="{cta_url}"{cta_ext_attrs} data-es="{button_es}">{C.CTA_BUTTON}</a>
      {call_btn}
    </div>
  </div>
  {right_plaque}
</div></section>"""

def find_us():
    """Fat Tony's pattern: address/hours + Get-directions & Call buttons next
    to the map, section id 'location' (matches the nav's Find Us anchor)."""
    loc_id = getattr(C, "LOCATION_SECTION_ID", "find")
    directions_url = getattr(C, "DIRECTIONS_URL", "") or (
        "https://www.google.com/maps/dir/?api=1&destination=" + C.ADDRESS_FULL.replace(" ", "+"))
    find_us_title_es = _es("Find us", "FIND_US_TITLE_ES")
    directions_es = _es("Get directions &rarr;", "DIRECTIONS_ES")
    call_label_es = _es("CALL", "CALL_LABEL_ES")
    return f"""<section class="sec wrap" id="{loc_id}" data-section="LOCATION"><div class="split find">
  <div>
    <h2 data-es="{find_us_title_es}">Find us</h2>
    <p class="lead" style="color:var(--cream);font-weight:700;font-size:16px">{C.ADDRESS_FULL}</p>
    <p style="margin-top:10px">{C.HOURS_TEXT}</p>
    <div class="cta-buttons" style="justify-content:flex-start;margin-top:14px">
      <a class="btn btn-primary" href="{directions_url}" target="_blank" rel="noopener" data-es="{directions_es}">Get directions &rarr;</a>
      <a class="btn btn-ghost" href="tel:{C.PHONE_TEL}" data-es="{call_label_es} {C.PHONE_DISPLAY}">CALL {C.PHONE_DISPLAY}</a>
    </div>
  </div>
  <div class="map"><iframe src="{C.MAP_EMBED_URL}" loading="lazy" title="Map"></iframe></div>
</div></section>"""


def build():
    title = f"{C.BUSINESS_NAME} - {C.TAGLINE}"
    desc  = C.HERO_SUB
    html = (
        S.head(title, desc)
        + S.age_gate()
        + S.nav("home")
        + hero()
        + trust()
        + favorites()
        + specials()
        + events_snap()
        + story()
        + cta_band()
        + find_us()
        + S.footer()
        + S.back_to_top()
        + S.close_html()
    )
    S.write_two_copies("home", html)

if __name__ == "__main__":
    build()
