# [Client] Website — Start Here

A plain-language guide for finding your site, making small changes yourself, and
asking an AI to make changes for you. (Hand this to the client.)

---

## 1. Where the site lives

Your site runs for free on **Cloudflare Pages**.

- **Live site:** _[fill in the pages.dev URL once deployed]_
- **Cloudflare account login:** _[fill in]_
- **Source files:** the folder you're looking at. The pages that go live are the
  files in the **`site/`** subfolder (`index.html`, `menu.html`).

---

## 2. How to make a small change yourself

You never edit the web pages directly — they're auto-generated, so your changes
would be overwritten the next time the site is rebuilt.

Instead, everything about your site — hours, phone, specials, colors, section
text — lives in one plain-English settings file:

**`build-scripts/brand_config.py`**

Open it and you'll see clearly-labeled lines like:

```
HOURS_TEXT    = "Open Daily 8:00am–9:30pm"
PHONE_DISPLAY = "(541) 555-0100"
SPECIALS_BODY = "Describe the current promo in one line."
```

To change something, edit the text inside the quotes. Then the site needs to be
**rebuilt** to update the actual pages — that part is easiest to hand to an AI
(next section).

---

## 3. What to ask an AI to do for you

If you have access to a free AI assistant (Claude, ChatGPT, etc.), give it access
to this folder and describe what you want in plain English:

- "Change the special to 15% off this week."
- "Our hours changed — we're open until 10pm now, update the site."
- "Update the phone number everywhere it appears."
- "Swap the storefront photo for this new one: [paste an image link]."

**Before you ask, tell the AI to read `AI-INSTRUCTIONS.md` in this folder first.**
That file explains exactly how the site is built so the AI doesn't guess or break
anything.

After the AI makes a change, ask it to:
1. Show you what it changed before finishing.
2. Re-run the build script so the pages update.
3. Confirm the updated files are saved in the folder AND its `site/` subfolder.
4. Deploy the `site/` folder so the change goes live.

The two PDFs in **`guides/`** — an **Editor Guide** and a **Setup Guide** — walk
through all of this in more detail.

---

## 4. If something looks broken

If a page shows raw code instead of a normal webpage, the usual cause is someone
edited a `.html` file directly instead of the settings file. Tell your AI:
"Something looks broken on [page name] — fix it from the build script."
