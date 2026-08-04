# AI-INSTRUCTIONS — [Client] Website

Read this before editing anything in this folder. It explains how the site is
actually built so you don't break it or create inconsistent files. (This file
ships with every client site; it's generic on purpose.)

## Architecture

A static HTML site generated from Python build scripts. No database, no CMS, no
live backend — every page is one self-contained `.html` file with inline CSS and
base64-embedded images, produced by running a Python script. The only live
element (on "embed" menu sites) is the external menu iframe, which updates itself.

**Do not hand-edit the `.html` files.** Always edit `build-scripts/brand_config.py`
(or the relevant build script), then re-run. Hand-edits to `.html` are silently
overwritten the next time a script runs.

## Where everything lives: `brand_config.py`

Almost every change a client asks for is a value in
`build-scripts/brand_config.py` — the single source of truth for this site:
business facts (phone, hours, address), colors, fonts, links, feature cards,
specials, story text, menu data, age gate, and compliance lines. **Change words
and facts there, not in the layout code.**

## File map

| Build script | Generates |
|---|---|
| `build-scripts/build_homepage.py` | root homepage + `site/index.html` |
| `build-scripts/build_menu_embed.py` | root menu + `site/menu.html` (iframe of an external live menu) |
| `build-scripts/build_menu_items.py` | root menu + `site/menu.html` (menu built from `MENU_SECTIONS`) |
| `build-scripts/build_catering.py` | root catering + `site/catering.html` (if `CATERING_ENABLED`) |
| `build-scripts/build_all.py` | everything above + the guide PDFs |

Which menu script is "live" depends on `MENU_MODE` in the config
(`embed` / `items` / `none`). Shared layout (nav, footer, age gate, CSS) lives in
`site_common.py` and is used by every page, so site-wide changes happen in one place.

**Locked style spec (decided 2026-07-06, Fat Tony's is the basis — do not change
without George's approval).** Only colors and fonts vary per client (brand_config.py).

- Page frame: wrap max 1180px, 32px side padding, 900px mobile breakpoint.
- Nav: sticky bar with 18px vertical padding; logo left (56px tall), menu links
  CENTER (space-between, 14px, 32px gaps), CALL + ORDER right. Nav buttons:
  6px radius, 13px, 10px/20px padding.
- Buttons: solid accent fill, 7px radius, 14px/28px padding, 15px bold; hover =
  darker accent + translateY(-2px) + shadow. No pulse animations, no gradients.
- Hero: 80px/70px section padding, 56px gap; photo LEFT (flex .9), text RIGHT
  (flex 1.1); solid accent badge-pill above a 48px h1; lead max 440px; square
  fading slideshow 340px, 8s per slide; transparent logo hangs over the
  slideshow's bottom-right corner (96px, ~33px overhang).
- Trust strip: 4 two-line stat blocks (bold 15px value / 12px label), spread
  evenly, 26px padding.
- Sections: 70px padding; card sections use a CENTERED label (13px tracked) +
  32px title (44px below); split sections use left 30px h2. Radius 12px on
  cards/specials/map/story; map 320px tall.
- Back-to-top: bare TOTOP_ICON (business-specific svg/png: pizza slice, leaf,
  chili...) with NO circle or background behind it.
- Footer: big centered logo divider, then Follow + social icons + @handle +
  email (when the business has one) + compliance lines (when legally required)
  + copyright. Address/hours/phone are NOT repeated in the footer — they live
  in Find Us and the trust strip. MG's footer is the maximum; never exceed it.

## The two output copies

Each page script writes TWO copies:
- **Root working copy** (`<slug>_homepage.html`, `<slug>_menu.html`) — for local
  preview. Never deployed (the folder root holds private notes).
- **`site/` copy** (`index.html`, `menu.html`) — the Cloudflare Pages deploy
  folder. **Only `site/` gets deployed.** Cross-page links differ between the two
  copies; that's handled automatically by `__HOME__` / `__MENU__` tokens.

## Safe editing pattern

Use an assert-guarded replace so a typo fails loudly instead of doing nothing:

```python
old = "HOURS_TEXT    = \"Open Daily 8:00am&ndash;9:30pm\""
new = "HOURS_TEXT    = \"Open Daily 8:00am&ndash;10:00pm\""
assert old in content
content = content.replace(old, new, 1)
```

## After editing

1. Run `python build-scripts/build_all.py` (or the single script you changed).
2. Confirm it prints `written ### -> ...` lines with no errors (each page = two files).
3. Confirm the updated files landed in the folder root AND `site/`.
4. Deploy `site/` to Cloudflare Pages (PowerShell / Desktop Commander — the
   sandbox can't reach Cloudflare or npm):
   ```powershell
   $env:CLOUDFLARE_API_TOKEN="<Pages-scoped token>"
   npx wrangler pages deploy "site" --project-name <PROJECT_SLUG> --branch main --commit-dirty=true
   ```

## Things not to invent

Never invent hours, phone, address, prices, or claims. Source of truth is the
client's official site (`SOURCE_OF_TRUTH` in the config), never third-party
listings. Compliance lines in the footer, where present, are legally required —
do not remove or reword them.
