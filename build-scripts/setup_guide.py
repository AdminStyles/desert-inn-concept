# -*- coding: utf-8 -*-
"""Setup Guide PDF -- hosting, file structure & how the site is built (technical).
Config-driven. Run:  python build-scripts/setup_guide.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_guides import *
from reportlab.platypus import PageBreak
import brand_config as CFG

MENU_SCRIPT = {"embed": "build_menu_embed.py", "items": "build_menu_items.py"}.get(CFG.MENU_MODE, "")
AI_CLIENT_SLUG = getattr(CFG, "AI_EDIT_CLIENT_SLUG", CFG.PROJECT_SLUG.replace("-concept", ""))
ADMIN_STYLES_FILE = "admin_styles_" + AI_CLIENT_SLUG.replace("-", "_") + ".html"
CONFIG_FILE_NAME = "brand_config.py"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "guides")
os.makedirs(OUT_DIR, exist_ok=True)
doc = SimpleDocTemplate(
    os.path.join(OUT_DIR, f"{CFG.BUSINESS_NAME} - Setup Guide.pdf"), pagesize=letter,
    topMargin=0.6*inch, bottomMargin=0.85*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)

S = []
S.extend(make_title_block("Setup Guide", "Hosting, file structure & how the site is built",
                          f"{CFG.BUSINESS_NAME} Website"))
S.append(Paragraph("Who this is for", styles["H1"]))
S.append(Paragraph(
    "For whoever sets up or maintains the site at a technical level -- deploying it, finding "
    "the right files, or handing the project to an AI assistant. To just update hours or a "
    "special, use the <b>Editor Guide</b> instead.", styles["Body"]))
S.append(Paragraph("1. Where the site lives", styles["H1"]))
S.append(Paragraph("The site runs for free on <b>Cloudflare Pages</b>.", styles["Body"]))
S.append(Paragraph(f"&#8226; Live site: <b>{CFG.LIVE_URL}</b>", styles["Bullet"]))
S.append(Paragraph("&#8226; Cloudflare account login: <i>[fill in]</i>", styles["Bullet"]))
S.append(Paragraph(
    "Source files live in the project folder. Only the <b>site/</b> subfolder gets deployed. "
    "The .html files in the folder root are working copies for local preview -- never "
    "deployed. Everything else (notes, build scripts, guides) stays private.", styles["Body"]))
S.append(Paragraph("Deploy command (PowerShell)", styles["H2"]))
S.append(Paragraph(
    f'npx wrangler pages deploy "site" --project-name {CFG.PROJECT_SLUG} '
    '--branch main --commit-dirty=true', styles["Code"]))
S.append(Paragraph(
    "Requires the CLOUDFLARE_API_TOKEN environment variable -- see AI-INSTRUCTIONS.md in "
    "the project folder for the token and the full one-line command.", styles["BodyTan"]))
S.append(PageBreak())

S.append(Paragraph("2. Architecture -- how the site is built", styles["H1"]))
S.append(Paragraph(
    "A static HTML site generated from Python scripts. No database, no live backend -- each "
    "page is one self-contained .html file with inline CSS and embedded images, produced by "
    "running a build script.", styles["Body"]))
S.append(Paragraph(
    "<b>Never hand-edit the .html files.</b> Always edit brand_config.py (facts, colors) or "
    "the matching build script, then re-run. Hand-edits are silently overwritten.", styles["Body"]))
S.append(Paragraph("File map", styles["H2"]))
rows = [["Build script", "Generates"],
        ["build-scripts/build_homepage.py", "root homepage + site/index.html"]]
if MENU_SCRIPT:
    rows.append(["build-scripts/" + MENU_SCRIPT, "root menu + site/menu.html"])
if CFG.CATERING_ENABLED:
    rows.append(["build-scripts/build_catering.py", "root catering + site/catering.html"])
rows.append(["build-scripts/build_all.py", "everything above, in one command"])
S.append(section_table(rows, col_widths=[3.4*inch, 3.6*inch]))
S.append(Spacer(1, 12))
S.append(Paragraph("How a build works", styles["H2"]))
S.append(PipelineDiagram([("CONFIG","brand_config.py"),("BUILD","run script"),
                          ("2 FILES","root + site/"),("DEPLOY","site/ to CF")], height=1.0*inch))
S.append(Spacer(1, 10))
for b in ["All business facts and colors are in brand_config.py -- one file.",
          "Each script writes TWO copies: a root working file and the deployable site/ file.",
          "Images in assets/ are embedded at build time, so pages are self-contained.",
          "Run build-scripts/build_all.py to rebuild the whole site at once."]:
    S.append(Paragraph("&#8226; " + b, styles["Bullet"]))

S.append(Paragraph("Safe editing pattern", styles["H2"]))
S.append(Paragraph(
    "old = \"HOURS_TEXT = 'Open Daily 8:00am&amp;ndash;9:30pm'\"<br/>"
    "new = \"HOURS_TEXT = 'Open Daily 8:00am&amp;ndash;10:00pm'\"<br/>"
    "assert old in content<br/>content = content.replace(old, new, 1)", styles["Code"]))
S.append(PageBreak())
S.append(Paragraph("3. Built-in behaviors worth knowing", styles["H1"]))
if CFG.AGE_GATE_ENABLED:
    S.append(Paragraph(f"&#8226; <b>Age gate:</b> visitors see an &#8220;{CFG.AGE_GATE_MIN}+&#8221; "
        "overlay. Yes is remembered 30 days; No redirects off-site. Required for this "
        "business type -- do not remove.", styles["Bullet"]))
if CFG.COMPLIANCE_LINES:
    S.append(Paragraph("&#8226; <b>Compliance lines:</b> the footer's legal warnings are "
        "required -- do not remove or reword them.", styles["Bullet"]))
S.append(Paragraph("&#8226; <b>Back-to-top button:</b> appears bottom-right after scrolling.", styles["Bullet"]))
if CFG.MENU_MODE == "embed":
    S.append(Paragraph("&#8226; <b>Live menu:</b> the Menu page embeds an external ordering "
        "menu -- product names, prices and stock update automatically, no site edits needed.",
        styles["Bullet"]))
S.append(Paragraph("4. The AI-edit pipeline (Admin Styles)", styles["H1"]))
S.append(Paragraph(
    "There's a second layer on top of everything above: a private tool called "
    f"<b>{ADMIN_STYLES_FILE}</b> that lets the business owner request edits in plain English "
    "(see the Editor Guide) without ever touching build scripts or a terminal. It's a separate "
    "local file, not yet part of the site/ deploy folder -- it isn't publicly reachable, by "
    "design, until the pipeline below is fully signed off.", styles["Body"]))
S.append(PipelineDiagram([("WIDGET","POSTs request"),("WORKER","asks the AI"),
                          ("GITHUB","commits the .py"),("ACTIONS","redeploys")], height=1.0*inch))
S.append(Spacer(1, 8))
S.append(Paragraph(
    f"Admin Styles' chat POSTs <code>{{client, message, code}}</code> to one shared Cloudflare "
    "Worker (<b>och-ai-site-editor</b>) used by every client site. The Worker reads that client's "
    f"config file (<b>{CONFIG_FILE_NAME}</b>) straight from GitHub, asks an AI model to make only "
    "the requested edit, sanity-checks that the file structure survived, and commits the result "
    "back to GitHub -- which triggers the same GitHub Actions -> Cloudflare Pages deploy you'd "
    "otherwise run by hand. Typically live in well under a minute.", styles["Body"]))
S.append(Paragraph(
    "Each client is pinned to an AI provider in the Worker's own source (Anthropic by default; "
    "NVIDIA or Groq have been used as fallbacks when a provider's endpoint was timing out; a "
    "bring-your-own-key Gemini mode also exists as an opt-in per client). The Worker's per-client "
    "config (GitHub owner/repo/path, which provider) and its reference source both live in "
    "<b>Workspace.txt</b> at the project root -- edit that before it's redeployed to Cloudflare.",
    styles["BodyTan"]))
S.append(Paragraph(
    "<b>Secrets never live in a file.</b> Each client's GitHub token, widget access code, and any "
    "bring-your-own API key are Worker secrets set directly in the Cloudflare dashboard, not "
    "written anywhere in this project. The widget itself only ever asks the owner for their "
    "access code, which the Worker checks before making any edit.", styles["Body"]))
S.append(Paragraph(
    "The Worker only ever edits the .py config file, the same file this guide's build scripts "
    "read -- it never touches the built .html directly, so the &#8220;never hand-edit .html, "
    "always edit then rebuild&#8221; rule above holds no matter which path a change came through.",
    styles["Body"]))

S.append(Paragraph("5. After any change", styles["H1"]))
for b in ["Run the script (python build-scripts/build_all.py).",
          "Confirm it prints &#8220;written ###&#8221; lines with no errors.",
          "Deploy the site/ folder with the wrangler command on page 1.",
          f"Business facts must match {CFG.SOURCE_OF_TRUTH} -- the official site is the source of truth.",
          "If the change came through Admin Styles instead, GitHub Actions already redeployed it -- just confirm the live site reflects it."]:
    S.append(Paragraph("&#8226; " + b, styles["Bullet"]))
S = keep_headings_with_next(S)
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("Setup Guide built ->", os.path.join(OUT_DIR, f"{CFG.BUSINESS_NAME} - Setup Guide.pdf"))
