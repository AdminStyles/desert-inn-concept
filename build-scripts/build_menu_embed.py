# -*- coding: utf-8 -*-
"""
build_menu_embed.py -- "Shop the Menu" page that wraps an EXTERNAL live menu
(Dutchie, TouchBistro, Toast, Square, etc.) in your own header + footer.
Use when brand_config.MENU_MODE == "embed". Run:
    python build-scripts/build_menu_embed.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_config as C
import site_common as S

MENU_CSS = """
.menu-page{min-height:100vh;display:flex;flex-direction:column}
.menu-card{flex:1;max-width:1120px;width:100%;margin:24px auto;padding:0 22px}
.menu-frame{border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,.12);background:#fff;min-height:760px}
.menu-frame iframe{width:100%;height:100%;min-height:760px;border:0;display:block}
.menu-head{padding:26px 0 6px}
@media(max-width:900px){.menu-frame,.menu-frame iframe{min-height:640px}}
"""

def build():
    title = f"Menu - {C.BUSINESS_NAME}"
    desc  = f"Browse the {C.BUSINESS_NAME} menu and order online."
    intro = f'<p class="lead">{C.MENU_INTRO}</p>' if C.MENU_INTRO else ""
    body = f"""<div class="menu-page">
  {S.nav('menu')}
  <div class="menu-card" id="menu">
    <div class="menu-head"><span class="sec-tag">MENU</span><h2>{C.BUSINESS_NAME}</h2>{intro}</div>
    <div class="menu-frame"><iframe src="{C.MENU_EMBED_URL}" title="{C.BUSINESS_NAME} menu" loading="lazy"></iframe></div>
  </div>
  {S.footer()}
</div>"""
    html = (S.head(title, desc) + "<style>" + MENU_CSS + "</style>"
            + S.age_gate() + body + S.back_to_top() + S.close_html())
    S.write_two_copies("menu", html)

if __name__ == "__main__":
    build()
