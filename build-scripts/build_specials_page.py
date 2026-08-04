# -*- coding: utf-8 -*-
"""
build_specials_page.py -- a dedicated Specials page (name / description /
price rows), built from SPECIALS_LIST in brand_config.py. Opt-in: only runs
anything if SPECIALS_LIST is set. Use for a client whose real specials list
is too long for the homepage "weekly specials" teaser strip (events_snap /
the old 3-card specials() grid) -- both of those stay as curated homepage
highlights; this page is the complete list, same pattern as build_menu_items.py.
Run:
    python build-scripts/build_specials_page.py

SPECIALS_LIST format: a flat list of (name, desc, price) tuples, e.g.
    SPECIALS_LIST = [
        ("Taco Tuesday", "3 tacos", "$9.99"),
        ("Daily Lunch Special", "", "$10.99"),
        ...
    ]
desc may be "" for items with no extra detail.

Bilingual: reuses the same MENU_ITEMS_ES convention as the menu page, keyed
under the anchor "specials" -- ES.MENU_ITEMS_ES.get("specials", []), a list
of (name_es, desc_es) tuples in the same order as SPECIALS_LIST. A client
that hasn't translated it yet just falls back to English per item.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_config as C
import site_common as S
import es_translations as ES

# Reuses the exact same visual language as the printed menu (menu-wrap,
# menu-hero, menu-item row layout) so the page reads as part of the same
# site instead of a bolted-on template -- just one section, no jump nav.
SPECIALS_CSS = """
.menu-wrap{max-width:900px;margin:0 auto;padding:40px 22px}
.menu-hero{background:radial-gradient(ellipse at 70% 30%,var(--accent) 0%,var(--accent-deep) 55%,var(--primary-deep) 100%);border:2px solid var(--cream);border-radius:16px;padding:36px 28px;margin-bottom:30px;text-align:center}
.menu-hero .sec-tag{color:var(--cream)}
.menu-hero h2{font-size:34px;text-transform:uppercase;margin:8px 0 10px;color:var(--primary-deep)}
.menu-hero h2 .wordmark{font-family:var(--font-nav);font-weight:var(--font-nav-weight);color:var(--cream);text-shadow:0 2px 3px rgba(0,0,0,.4)}
.menu-hero .lead{max-width:560px;margin:0 auto;color:var(--cream)}
.menu-section{margin-bottom:40px}
.menu-item{display:flex;justify-content:space-between;gap:18px;padding:12px 0;border-bottom:1px dashed rgba(255,255,255,.08)}
.menu-item .nm{font-weight:600;color:var(--cream)}
.menu-item .ds{color:var(--cream-muted);font-size:14px;margin-top:2px}
.menu-item .pr{color:var(--glow);font-weight:700;white-space:nowrap}
"""

def render_items(items):
    es_items = getattr(ES, "MENU_ITEMS_ES", {}).get("specials", [])
    out = []
    for i, (n, d, p) in enumerate(items):
        n_es, d_es = (es_items[i] if i < len(es_items) else (None, None))
        n_attr = f' data-es="{n_es}"' if n_es else ""
        d_attr = f' data-es="{d_es}"' if d_es else ""
        ds_html = f'<div class="ds"{d_attr}>{d}</div>' if d else ""
        out.append(f'<div class="menu-item"><div><div class="nm"{n_attr}>{n}</div>'
                    f'{ds_html}</div><div class="pr">{p}</div></div>')
    return "".join(out)

def build():
    items = getattr(C, "SPECIALS_LIST", None)
    if not items:
        return
    title = f"Specials - {C.BUSINESS_NAME}"
    desc  = f"The full list of specials at {C.BUSINESS_NAME}."
    page_tag = getattr(C, "SPECIALS_PAGE_TAG", "SPECIALS")
    page_title = getattr(C, "SPECIALS_PAGE_TITLE", C.BUSINESS_NAME)
    page_intro = getattr(C, "SPECIALS_PAGE_INTRO", "")
    tag_es = ES.NAV_ES.get("SPECIALS", page_tag)
    intro_es = getattr(ES, "SPECIALS_PAGE_INTRO_ES", page_intro)
    intro_html = f'<p class="lead" data-es="{intro_es}">{page_intro}</p>' if page_intro else ""
    order_label_es = getattr(ES, "ORDER_LABEL_ES", C.ORDER_LABEL)
    call_label_es = getattr(ES, "CALL_LABEL_ES", "CALL")
    # "Desert Inn" set in the same font as the header logo wordmark
    # (--font-nav, Abril Fatface), matching the menu page's hero heading.
    hero_title = page_title.replace(
        "Desert Inn", '<span class="wordmark">Desert Inn</span>', 1)
    body = f"""{S.nav('specials')}
<div class="menu-wrap" id="specials" data-section="SPECIALS">
  <div class="menu-hero" data-section="SPECIALS-HERO">
    <span class="sec-tag" data-es="{tag_es}">{page_tag}</span>
    <h2>{hero_title}</h2>
    {intro_html}
  </div>
  <div class="menu-section" data-section="SPECIALS-LIST">{render_items(items)}</div>
  <div class="cta-buttons" style="margin-top:20px">
    <a class="btn btn-primary" href="{C.ORDER_URL}" target="_blank" rel="noopener" data-es="{order_label_es}">{C.ORDER_LABEL}</a>
    <a class="btn btn-ghost" href="tel:{C.PHONE_TEL}" data-es="{call_label_es} {C.PHONE_DISPLAY}">CALL {C.PHONE_DISPLAY}</a>
  </div>
</div>
{S.footer()}"""
    html = (S.head(title, desc) + "<style>" + SPECIALS_CSS + "</style>"
            + S.age_gate() + body + S.back_to_top() + S.close_html())
    S.write_two_copies("specials", html)

if __name__ == "__main__":
    build()
