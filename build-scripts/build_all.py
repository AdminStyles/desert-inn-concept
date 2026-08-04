# -*- coding: utf-8 -*-
"""
build_all.py -- one command to (re)build the whole site from brand_config.py.
    python build-scripts/build_all.py
Picks the right menu builder from MENU_MODE, builds catering if enabled, and
regenerates the client guide PDFs (needs reportlab: pip install reportlab).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_config as C

def main():
    print("=== Building", C.BUSINESS_NAME, "site ===")
    import build_homepage; build_homepage.build()

    if C.MENU_MODE == "embed":
        import build_menu_embed; build_menu_embed.build()
    elif C.MENU_MODE == "items":
        import build_menu_items; build_menu_items.build()
    else:
        print("MENU_MODE = none -- no menu page.")

    if C.CATERING_ENABLED:
        import build_catering; build_catering.build()

    # Guides are optional (require reportlab). Don't fail the site build if missing.
    try:
        import editor_guide, setup_guide   # noqa: F401  (these build on import)
        print("Guides rebuilt.")
    except Exception as e:
        print("Guides skipped:", e)

    print("=== Done. Deploy the  site/  folder to Cloudflare Pages. ===")

if __name__ == "__main__":
    main()
