# -*- coding: utf-8 -*-
"""
build_menu_items.py -- full printed-style menu built from MENU_SECTIONS in
brand_config.py. Use when brand_config.MENU_MODE == "items" (restaurants). Run:
    python build-scripts/build_menu_items.py

Bilingual: section titles/intro/items pull from es_translations.py
(MENU_SECTION_TITLES_ES, MENU_INTRO_ES, MENU_ITEMS_ES) when present; a client
that hasn't translated the menu yet just falls back to English per item.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_config as C
import site_common as S
import es_translations as ES

MENU_CSS = """
.menu-wrap{max-width:900px;margin:0 auto;padding:40px 22px}
.menu-hero{background:radial-gradient(ellipse at 70% 30%,var(--accent) 0%,var(--accent-deep) 55%,var(--primary-deep) 100%);border:2px solid var(--cream);border-radius:16px;padding:36px 28px;margin-bottom:30px;text-align:center}
.menu-hero .sec-tag{color:var(--cream)}
.menu-hero h2{font-size:34px;text-transform:uppercase;margin:8px 0 10px;color:var(--primary-deep)}
.menu-hero h2 .wordmark{font-family:var(--font-nav);font-weight:var(--font-nav-weight);color:var(--cream);text-shadow:0 2px 3px rgba(0,0,0,.4)}
.menu-hero .lead{max-width:560px;margin:0 auto;color:var(--cream)}
.menu-jump{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 30px}
.menu-jump a{background:var(--panel);border:1px solid rgba(255,255,255,.1);padding:7px 15px;border-radius:20px;font-size:14px;color:var(--cream-muted)}
.menu-jump a:hover{color:var(--accent);border-color:var(--accent)}
.menu-section{margin-bottom:40px}
.menu-section h2{font-size:28px;color:var(--accent);border-bottom:1px solid rgba(255,255,255,.12);padding-bottom:8px;margin-bottom:16px}
.menu-item{display:flex;justify-content:space-between;gap:18px;padding:12px 0;border-bottom:1px dashed rgba(255,255,255,.08)}
.menu-item .nm{font-weight:600;color:var(--cream)}
.menu-item .ds{color:var(--cream-muted);font-size:14px;margin-top:2px}
.menu-item .pr{color:var(--glow);font-weight:700;white-space:nowrap}
"""

def render_items(items, anchor):
    es_items = getattr(ES, "MENU_ITEMS_ES", {}).get(anchor, [])
    out = []
    for i, (n, d, p) in enumerate(items):
        n_es, d_es = (es_items[i] if i < len(es_items) else (None, None))
        n_attr = f' data-es="{n_es}"' if n_es else ""
        d_attr = f' data-es="{d_es}"' if d_es else ""
        out.append(f'<div class="menu-item"><div><div class="nm"{n_attr}>{n}</div>'
                    f'<div class="ds"{d_attr}>{d}</div></div><div class="pr">{p}</div></div>')
    return "".join(out)

def build():
    title = f"Menu - {C.BUSINESS_NAME}"
    desc  = f"The full {C.BUSINESS_NAME} menu."
    sec_titles_es = getattr(ES, "MENU_SECTION_TITLES_ES", {})
    jump = "".join(
        f'<a href="#{a}" data-es="{sec_titles_es.get(a, t)}">{t}</a>'
        for t, a, _ in C.MENU_SECTIONS)
    sections = "".join(
        f'<section class="menu-section" id="{a}"><h2 data-es="{sec_titles_es.get(a, t)}">{t}</h2>'
        f'{render_items(items, a)}</section>'
        for t, a, items in C.MENU_SECTIONS)
    menu_intro_es = getattr(ES, "MENU_INTRO_ES", C.MENU_INTRO)
    intro = f'<p class="lead" data-es="{menu_intro_es}">{C.MENU_INTRO}</p>' if C.MENU_INTRO else ""
    menu_label_es = getattr(ES, "NAV_ES", {}).get("MENU", "MENU")
    order_label_es = getattr(ES, "ORDER_LABEL_ES", C.ORDER_LABEL)
    call_label_es = getattr(ES, "CALL_LABEL_ES", "CALL")
    # "Desert Inn" set in the same font as the header logo wordmark
    # (--font-nav, Abril Fatface); rest of the name stays in the normal
    # heading font.
    hero_title = C.BUSINESS_NAME.replace(
        "Desert Inn", '<span class="wordmark">Desert Inn</span>', 1)
    body = f"""{S.nav('menu')}
<div class="menu-wrap" id="menu" data-section="MENU">
  <div class="menu-hero" data-section="MENU-HERO">
    <span class="sec-tag" data-es="{menu_label_es}">MENU</span>
    <h2>{hero_title}</h2>
    {intro}
  </div>
  <div class="menu-jump">{jump}</div>
  <div data-section="MENU-SECTIONS">{sections}</div>
  <div class="cta-buttons" style="margin-top:20px">
    <a class="btn btn-primary" href="{C.ORDER_URL}" target="_blank" rel="noopener" data-es="{order_label_es}">{C.ORDER_LABEL}</a>
    <a class="btn btn-ghost" href="tel:{C.PHONE_TEL}" data-es="{call_label_es} {C.PHONE_DISPLAY}">CALL {C.PHONE_DISPLAY}</a>
  </div>
</div>
{S.footer()}"""
    html = (S.head(title, desc) + "<style>" + MENU_CSS + "</style>"
            + S.age_gate() + body + S.back_to_top() + S.close_html())
    S.write_two_copies("menu", html)

if __name__ == "__main__":
    build()
