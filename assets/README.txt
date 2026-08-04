Drop the client's images in this folder, then point the paths in
build-scripts/brand_config.py at them. Anything here is base64-embedded into the
pages at build time, so the site stays self-contained.

Suggested files (names are just a convention — match them in brand_config.py):
  hero.jpg          -> HERO_PHOTO   (main storefront / food / product photo)
  logo.png          -> LOGO_IMAGE   (nav + hero logo; transparent PNG is best)
  hero2.jpg, hero3.jpg -> add to HERO_SLIDES for a fading hero slideshow
  guide-badge.png   -> optional round badge shown on the guide PDF covers

Tips:
- Web URLs also work in the config (e.g. https://i.imgur.com/....png) — handy
  before you have the real files.
- Keep hero photos landscape and at least ~1200px wide.
- If a path in the config points at a file that doesn't exist yet, the build
  still succeeds — the page just shows a broken image until you add the file.
