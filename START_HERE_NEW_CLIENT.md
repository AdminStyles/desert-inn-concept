# START HERE — New Client Site Template

This folder is a **reusable template** for building a concept site for any local
business, the same way Fat Tony's (portfolio #1) and Miracle Greens (#2) were built.
Clone it, fill in one config file, run one command, deploy. Then pitch it for
recurring "I'll host + update your site" revenue.

---

## The model (why this exists)

1. Build a concept site that's better than what the business has now.
2. Host it live for free on **Cloudflare Pages** so they can see it working.
3. Pitch: *"Here's what your site could look like. I'll manage it on free hosting
   with AI-assisted updates — you never need a developer again."*
4. Close = recurring revenue. If they pass, swap the config and pitch the next
   business. **The work is reusable — that's the whole point of this folder.**

---

## New-client intake checklist (gather these BEFORE building)

Every new site needs these decided/collected up front — they're the only things
that change between clients (layout is locked to the Fat Tony's spec):

1. **Colors** — a unique dark scheme pulled from the client's branding (fill `COLORS`).
2. **Heading font** — pick a Google Font that fits the brand (`FONT_HEADING`); body stays clean.
3. **Transparent logo** — png/svg with NO background; it overhangs the slideshow
   corner and sits on the footer logo divider. A white box behind it = not ready.
4. **Slideshow photos** — 3–6 square-ish photos for the hero (`HERO_SLIDES`).
   If the client hasn't provided photos yet, run a single promo image
   (`HERO_PHOTO`) until they do — Miracle Greens pattern.
5. **Back-to-top icon** — a transparent svg/png that reflects the business
   (pizza slice / leaf / chili pepper) for `TOTOP_ICON`.
6. **Content** — verified facts (hours, phone, address), specials/promo, story
   text, and the menu source (embed URL or item list).

---

## Spin up a new client in 6 steps

1. **Copy this whole `_SITE_TEMPLATE` folder** and rename it to the client
   (e.g. `BENDS BEST BAKERY`). Put it alongside the other client folders in
   `C:\STUFF\CCA and DBD\`.
2. **Open `build-scripts/brand_config.py`** and fill in every value marked `TODO`.
   This is the ONLY file with the client's facts, colors, links, and menu. Verify
   every fact against the client's official site — never invent hours/prices/claims.
3. **Drop the client's images** into `assets/` (hero photo, logo). Point the
   `HERO_PHOTO` / `LOGO_IMAGE` paths in the config at them. (URLs work too.)
4. **Build it:** from the client folder run
   `python build-scripts/build_all.py`
   This regenerates the homepage, the menu page, catering (if enabled), and the
   two client guide PDFs.
5. **Preview locally** by opening the root `*_homepage.html` / `*_menu.html`
   files in a browser. Iterate on the config until it looks right.
6. **Deploy the `site/` folder** to Cloudflare Pages (see below), grab the live
   URL, put it in `brand_config.LIVE_URL`, rebuild once so the guides show it,
   then pitch.

---

## What's in this folder

| Path | What it is |
|---|---|
| `build-scripts/brand_config.py` | **THE file you fill in.** Every per-client value lives here. |
| `build-scripts/site_common.py` | Shared layout (head, nav, footer, age gate, back-to-top, CSS). Rarely edited. |
| `build-scripts/build_homepage.py` | Generates the homepage. |
| `build-scripts/build_menu_embed.py` | Menu page that wraps an external live menu (Dutchie/TouchBistro/etc.) in an iframe. |
| `build-scripts/build_menu_items.py` | Menu page built from your own item list (printed-menu style). |
| `build-scripts/build_catering.py` | Optional catering page (restaurants). |
| `build-scripts/build_all.py` | Runs the right builders + guides in one command. |
| `build-scripts/build_guides.py` | Shared PDF styling (auto-matches the site colors). |
| `build-scripts/editor_guide.py` / `setup_guide.py` | The two client-handoff PDFs. |
| `site/` | **The only folder you deploy.** Holds `index.html`, `menu.html`, etc. |
| `guides/` | Generated client PDFs (Editor Guide + Setup Guide). |
| `assets/` | Drop client images here. |
| `AI-INSTRUCTIONS.md` | Technical reference — point any AI assistant here before it edits. |
| `START_HERE.md` | Plain-language guide to hand the client. |
| `doc-templates/` | Your private working docs to copy per client (checklist, pitch email, notes). |

---

## Which menu builder?

Set `MENU_MODE` in the config:

- **`"embed"`** — the business already has an online ordering/menu system
  (Dutchie for dispensaries, TouchBistro/Toast/Square for restaurants). We wrap
  their live menu in our header/footer. Prices/stock stay auto-updated by them.
  → uses `build_menu_embed.py`. *(This is what Miracle Greens uses.)*
- **`"items"`** — no online system, or you want a classic printed menu on the
  page. You type the items into `MENU_SECTIONS` in the config.
  → uses `build_menu_items.py`. *(This is the Fat Tony's style.)*
- **`"none"`** — single-page site, no menu.

For restaurants that cater, also set `CATERING_ENABLED = True` and fill
`CATERING_PACKAGES`.

---

## Deploy to Cloudflare Pages (PowerShell, on your machine)

The Cowork sandbox can't reach Cloudflare or npm — deploy from PowerShell /
Desktop Commander on your own machine (same as Miracle Greens). First time for a
new client creates a new Pages project:

```powershell
$env:CLOUDFLARE_API_TOKEN="<your Pages-scoped token>"
npx wrangler pages deploy "site" --project-name <PROJECT_SLUG> --branch main --commit-dirty=true
```

- `<PROJECT_SLUG>` = the `PROJECT_SLUG` you set in `brand_config.py`.
- Only the `site/` folder is deployed. Everything else stays private.
- After the first deploy, copy the `*.pages.dev` URL into `brand_config.LIVE_URL`
  and rebuild so the Setup Guide shows it.

> ⚠️ Rotate the shared Pages token after a sale closes.

---

## Rules (same discipline as FT's / MG's)

1. **Never invent business facts** — verify hours, phone, address, prices, and
   claims against the client's official site.
2. **Never hand-edit the generated `.html` files** — edit `brand_config.py` or a
   build script, then re-run. Hand-edits get overwritten.
3. **Never add unrequested sections** or silently change colors/copy — propose first.
4. **Compliance lines** (if any) are legally required — never remove or reword them.
5. On this machine, run builds/deploys via PowerShell / Desktop Commander — the
   sandbox mount has desynced and corrupted files on these projects before.
