# [Client] — Setup Checklist

Ordered by phase. Copy this into the client folder and check items off as you go.

## Phase 1 — Build the concept
- [ ] Copy `_SITE_TEMPLATE`, rename to the client
- [ ] Fill in every `TODO` in `build-scripts/brand_config.py` (verify facts vs. their official site)
- [ ] Add hero photo + logo to `assets/`, point config paths at them
- [ ] Pick `MENU_MODE` (embed / items / none); set catering if a restaurant
- [ ] `python build-scripts/build_all.py` — no errors, pages preview correctly
- [ ] Deploy `site/` to Cloudflare Pages; paste live URL into `LIVE_URL`; rebuild

## Phase 2 — Polish before the pitch
- [ ] Real page titles (not "Concept") — already driven by `BUSINESS_NAME`/`TAGLINE`
- [ ] SEO check: meta description, OG tags present (they're in `site_common.head()`)
- [ ] Verify every price/claim against the client's source of truth
- [ ] Get 2–3 real review quotes to add, if available
- [ ] Take before/after screenshots (their current site vs. the concept)
- [ ] Record a 60-second "watch me change a price live" demo

## Phase 3 — The pitch
- [ ] Fill in the pitch email (`doc-templates/PITCH_EMAIL.txt`), drop in the live URL
- [ ] Send from your business account to the owner / general inbox
- [ ] Anchor high, know your floor — keep the floor private

## Phase 4 — If they say yes (domain cutover)
- [ ] Add a `_redirects` file mapping their old URLs to the new pages
- [ ] Point their domain's DNS to Cloudflare Pages
- [ ] Test every page, phone/order links, forms, mobile, redirects
- [ ] Submit sitemap in Google Search Console; update Google Business Profile link
- [ ] Cancel their old host (confirm email isn't hosted there first!)

## Phase 5 — Recurring value + next client
- [ ] Add Cloudflare Web Analytics (free) — this is your success-story data
- [ ] After 30 days, write up before/after numbers as a case study
- [ ] Reuse the template for the next business
