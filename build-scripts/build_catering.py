# -*- coding: utf-8 -*-
"""
build_catering.py -- optional catering page (restaurants). Only builds when
brand_config.CATERING_ENABLED is True. Run:
    python build-scripts/build_catering.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_config as C
import site_common as S

# Same red-gradient "hero" treatment as the MENU page's .menu-hero, scoped to
# this page so the two builders stay independent (edit facts/colors in
# brand_config.py, not here).
CATERING_CSS = """
.catering-hero{background:radial-gradient(ellipse at 70% 30%,var(--primary) 0%,var(--primary-bright) 55%,var(--primary-deep) 100%);border-radius:16px;padding:36px 28px;margin-bottom:30px;text-align:center}
.catering-hero .sec-tag{display:block;margin-bottom:8px}
.catering-hero h2{font-size:34px;text-transform:uppercase;margin:8px 0 10px;color:var(--cream)}
.catering-hero .lead{max-width:560px;margin:0 auto;color:var(--cream)}
"""

def build():
    if not C.CATERING_ENABLED:
        print("CATERING_ENABLED is False -- skipping catering page.")
        return
    title = f"Catering - {C.BUSINESS_NAME}"
    desc  = f"Catering from {C.BUSINESS_NAME}."
    pkgs = "".join(
        f'<div class="card"><h3>{n}</h3><p>{d}</p>'
        f'<p style="color:var(--glow);font-weight:700;margin-top:8px">{p}</p></div>'
        for n, d, p in C.CATERING_PACKAGES)
    body = f"""{S.nav('catering')}
<section class="sec wrap" id="menu" data-section="CATERING">
  <div class="catering-hero">
    <span class="sec-tag">CATERING</span><h2>Let us cater your event</h2>
    <p class="lead">{C.CATERING_INTRO}</p>
  </div>
  <div class="cards" style="margin-top:26px">{pkgs}</div>
  <div class="cta-buttons" style="margin-top:26px">
    <a class="btn btn-primary" href="mailto:{C.CATERING_EMAIL}">REQUEST CATERING</a>
    <a class="btn btn-ghost" href="tel:{C.PHONE_TEL}">CALL {C.PHONE_DISPLAY}</a>
  </div>
</section>
{S.footer()}"""
    html = (S.head(title, desc) + "<style>" + CATERING_CSS + "</style>" + S.age_gate() + body
            + S.back_to_top() + S.close_html())
    S.write_two_copies("catering", html)

if __name__ == "__main__":
    build()
