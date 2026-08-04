# -*- coding: utf-8 -*-
"""Editor Guide PDF -- plain-English "how to update your site" for the client.
Config note: rebuilt around Admin Styles as of 2026-07-14.
Config-driven. Run:  python build-scripts/editor_guide.py

2026-07-14: rewritten around Admin Styles (admin_styles_<slug>.html) as the
primary editing workflow, replacing the old "copy text into ChatGPT/Claude.ai
or VS Code+Copilot, paste it back, hand off to whoever runs the build script"
instructions. Admin Styles' chat now POSTs straight to the AI-edit Worker,
which rewrites the client's config and triggers a redeploy -- no manual
copy/paste and no build-script step for the owner to worry about."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_guides import *
import brand_config as CFG

AI_CLIENT_SLUG = getattr(CFG, "AI_EDIT_CLIENT_SLUG", CFG.PROJECT_SLUG.replace("-concept", ""))
ADMIN_STYLES_FILE = "admin_styles_" + AI_CLIENT_SLUG.replace("-", "_") + ".html"

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "guides")
os.makedirs(OUT_DIR, exist_ok=True)
doc = SimpleDocTemplate(
    os.path.join(OUT_DIR, f"{CFG.BUSINESS_NAME} - Editor Guide.pdf"), pagesize=letter,
    topMargin=0.6*inch, bottomMargin=0.85*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)

S = []
S.extend(make_title_block("Editor Guide", "Update your site instantly, no tech skills needed",
                          f"{CFG.BUSINESS_NAME} Website"))
S.append(Paragraph("How this works", styles["H1"]))
S.append(Paragraph(
    "Your site has its own private control panel called <b>Admin Styles</b>. Open it, type what "
    "you want changed (or click a ready-made option), and hit Send. An AI updates your site's "
    "settings and puts the new version live automatically, usually within about a minute. No "
    "copying text into ChatGPT, no build scripts, nothing to install.", styles["Body"]))
S.append(Spacer(1, 4))
S.append(PipelineDiagram([("OPEN","Admin Styles"),("TYPE OR CLICK","what you want"),
                          ("SEND","the request"),("LIVE","in about a minute")]))
S.append(Spacer(1, 14))

S.append(Paragraph("1. Opening Admin Styles", styles["H1"]))
S.append(Paragraph(
    f"Admin Styles is the file <b>{ADMIN_STYLES_FILE}</b> you were given -- double-click it and "
    "it opens right in your browser (Chrome, Safari, Edge, whatever you use). There's nothing to "
    "install and nowhere to log into online -- it runs from the file itself.", styles["Body"]))
S.append(Spacer(1, 6))

S.append(Paragraph("2. The four tabs", styles["H1"]))
rows = [["Tab", "What it's for"],
        ["Content & Preview", "Type a request in plain English and watch your site's preview update as you go."],
        ["Style Editor", "Change colors and fonts with simple pickers -- saves automatically, no request needed."],
        ["Add-ons", "A browsable gallery of ready-made touches (bouncy buttons, an expandable menu card, and more), each with a live sample so you know exactly what you're getting before you ask for it."],
        ["Activity", "A log of every change that's been made, each with a one-click Undo."]]
S.append(section_table(rows, col_widths=[1.5*inch, 5.5*inch]))
S.append(Spacer(1, 10))

S.append(Paragraph("3. Sending your first change", styles["H1"]))
S.append(Paragraph(
    "The first time you hit Send, it asks for your site's access code -- a separate one-time code "
    "that came with the file (not a password, and not something you need to remember day to day). "
    "Enter it once and the browser remembers it after that.", styles["Body"]))
S.append(Spacer(1, 6))

S.append(Paragraph("4. Things you can ask for", styles["H1"]))
for b in ["Our hours changed -- we're open until 10pm now, update the site.",
          "Change the special to 15% off this week.",
          "Update the phone number everywhere it appears.",
          "Swap the storefront photo for this new one: [paste an image link].",
          "Reword the second feature card to mention our daily deals."]:
    S.append(Paragraph("&#8226; &#8220;" + b + "&#8221;", styles["Bullet"]))
S.append(Paragraph(
    "<b>Tip &#8212; plan your changes, then submit them together.</b> Every request rewrites your "
    "whole settings file, even for a one-line change, so five separate one-line requests cost "
    "roughly five times what one request covering all five changes does. Jot down everything you "
    "want updated first, then ask for it all at once: &#8220;Update our hours to 11-10, change the "
    "special to 15% off Tuesdays, and update the phone number to (541) 555-0100.&#8221;",
    styles["BodyTan"]))
S.append(Spacer(1, 6))

S.append(Paragraph("5. Using the Add-ons tab", styles["H1"]))
S.append(Paragraph(
    "The Add-ons tab is a browsable gallery of small site touches -- things like bouncy buttons, "
    "an expandable menu card, a gliding tab highlight, or a countdown timer. Every card shows a "
    "live, working sample right on the page, so you can see exactly what it does before asking for "
    "it. Found one you like? Click <b>Add to my site</b> -- it fills in a precise, ready-to-send "
    "request on the Content &amp; Preview tab. A few need you to fill in a bracketed detail first "
    "(like an announcement's exact wording) -- review the request, then hit Send.", styles["Body"]))
S.append(Spacer(1, 6))

S.append(Paragraph("6. Confirming it went live", styles["H1"]))
for b in ["After you hit Send, the status pill at the top shows &#8220;Redeploying your site&#8230;&#8221; -- give it a minute to finish.",
          "Refresh your live site and confirm the change is there.",
          "Every change is logged on the Activity tab with a timestamp, so you can always see what changed and when."]:
    S.append(Paragraph("&#8226; " + b, styles["Bullet"]))
S.append(Spacer(1, 6))

S.append(Paragraph("7. If something looks wrong", styles["H1"]))
S.append(Paragraph(
    "Open the Activity tab, find the change, and click <b>Undo</b> -- it reverts your site to how "
    "it looked right before that request and redeploys automatically. No need to describe what "
    "went wrong or ask anyone to fix it by hand.", styles["Body"]))
S.append(Spacer(1, 6))

S.append(Paragraph("No computer handy?", styles["H2"]))
S.append(Paragraph(
    "Just email your change to whoever gave you this guide, exactly as you'd say it out loud -- "
    "&#8220;we're open till 10 now&#8221;, &#8220;new special: 15% off Tuesdays&#8221; -- and "
    "they'll send it through Admin Styles for you, same day.", styles["Body"]))

S = keep_headings_with_next(S)
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("Editor Guide built ->", os.path.join(OUT_DIR, f"{CFG.BUSINESS_NAME} - Editor Guide.pdf"))
