# -*- coding: utf-8 -*-
"""
build_admin_styles.py -- generates admin_styles_<slug>.html, the client-facing
"Admin Styles" tool (Content & Preview / Style Editor / Activity tabs in one
page).

This is the templated version: every client built from _SITE_TEMPLATE gets
their own branded copy, generated from THEIR brand_config.py -- colors,
fonts, business name, pages, hero copy, trust strip, and favorites all pull
from the client's own config. Nothing here should ever need per-client
hand-editing; if a client needs something different, change brand_config.py
and rerun this script, same as every other page on the site.

2026-07-13: rewritten to (a) use plain token substitution instead of
str.format() -- the old {{double-brace}} escaping across ~500 lines of CSS/JS
was fragile and easy to break silently, this is not -- and (b) include the
Activity Log, Quick Actions, device preview toggle, persistent photo library,
tips panel, and config-download button that were prototyped by hand on Fat
Tony's and Simon's admin pages and then folded back into this generator so
they survive a rebuild instead of being hand-maintained forks.

Run: python build-scripts/build_admin_styles.py
Output: ../admin_styles_<slug>.html (root working copy -- e.g.
admin_styles_simons.html -- not yet part of the public site/ deploy folder;
wire that in once the AI Update Pipeline is confirmed live end-to-end and
this is meant to be client-facing).
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_config as C
import site_common as S

def _color(key, fallback):
    """Some client configs (e.g. Simon's) are missing optional keys like
    primary_deep -- fall back sanely instead of throwing."""
    return C.COLORS.get(key, C.COLORS.get(fallback, "#000000"))

def _pages():
    live = C.LIVE_URL.rstrip("/")
    pages = [("Home", live + "/", "index.html")]
    if getattr(C, "MENU_MODE", "none") != "none":
        pages.append(("Menu", live + "/menu.html", "menu.html"))
    if getattr(C, "CATERING_ENABLED", False):
        pages.append(("Catering", live + "/catering.html", "catering.html"))
    return pages

def _favorites_preview():
    """Up to 3 FAVORITES cards for the Style Editor's mock preview. Falls
    back to generic placeholder cards if the site has none defined (e.g. a
    future non-menu site type using this template)."""
    favs = getattr(C, "FAVORITES", [])[:3]
    if not favs:
        return [("Item one", "Description goes here", ""),
                ("Item two", "Description goes here", ""),
                ("Item three", "Description goes here", "")]
    out = []
    for f in favs:
        # FAVORITES tuples are (image, alt, name, desc, price)
        name = f[2] if len(f) > 2 else "Item"
        desc = f[3] if len(f) > 3 else ""
        price = f[4] if len(f) > 4 else ""
        out.append((name, desc, price))
    return out

def _trust_items():
    items = getattr(C, "TRUST_ITEMS", [])[:4]
    while len(items) < 4:
        items.append(("--", "--"))
    return items

def page_list_html():
    """<option> tags for the Page dropdown in the preview header -- one per
    page, first one selected by default. Kept as a helper function (rather
    than inlined) because clients can have 2-4 pages depending on
    MENU_MODE/CATERING_ENABLED."""
    rows = []
    for i, (name, url, fname) in enumerate(_pages()):
        selected = " selected" if i == 0 else ""
        rows.append(
            f'<option value="{url}" data-name="{name}"{selected}>{name}</option>'
        )
    return "\n".join(rows)

def favorites_preview_html():
    cards = []
    for name, desc, price in _favorites_preview():
        price_html = f'<div class="price">{price}</div>' if price else ""
        cards.append(f'<div class="pv-card"><h3>{name}</h3><p>{desc}</p>{price_html}</div>')
    return "\n".join(cards)

def trust_preview_html():
    rows = []
    for val, lbl in _trust_items():
        rows.append(f'<div class="pv-trust-item"><div class="num">{val}</div><div class="lbl">{lbl}</div></div>')
    return "\n".join(rows)

def build():
    live = C.LIVE_URL.rstrip("/")
    pages = _pages()
    nav_links = "".join(f"<span>{name}</span>" for name, _, _ in pages[1:])

    colors = {
        "primary": _color("primary", "primary"),
        "primary_bright": _color("primary_bright", "primary"),
        "primary_deep": _color("primary_deep", "primary_bright"),
        "glow": _color("glow", "cream"),
        "accent": _color("accent", "accent"),
        "accent_deep": _color("accent_deep", "accent"),
        "on_accent": _color("on_accent", "ink"),
        "cream": _color("cream", "cream"),
        "cream_muted": _color("cream_muted", "cream"),
        "bg_deep": _color("bg_deep", "bg_deep"),
        "panel": _color("panel", "bg_deep"),
        "ink": _color("ink", "bg_deep"),
    }

    defaults_json = json.dumps({
        "fontHead": C.FONT_HEADING,
        "fontBody": C.FONT_BODY,
        "colors": colors,
    })

    # AI-edit backend wiring -- same shared och-ai-site-editor Worker used by
    # every client's /assets/ai-edit widget. AI_EDIT_CLIENT_SLUG and
    # AI_EDIT_STORAGE_KEY can be overridden in brand_config.py; otherwise
    # they're derived from PROJECT_SLUG. IMPORTANT: if this client already
    # has a live /assets/ai-edit widget, these MUST match that widget's
    # CLIENT_SLUG and its localStorage key exactly, so a code the owner
    # already entered there works here too -- check the widget's page source
    # rather than trusting the derived default if one already exists.
    ai_client_slug = getattr(C, "AI_EDIT_CLIENT_SLUG", C.PROJECT_SLUG.replace("-concept", ""))
    ai_access_key = getattr(C, "AI_EDIT_STORAGE_KEY", ai_client_slug.replace("-", "") + "EditAccessCode")
    storage_key = C.PROJECT_SLUG.replace("-", "_") + "_admin_styles_v1"

    # Page-view PIN gate -- separate from the AI_ACCESS_KEY code above (which
    # the Worker validates server-side on every Send). This PIN only gates
    # whether the Admin Styles page *opens* at all; it lives in plain text in
    # this static HTML file, so it's a deterrent against someone stumbling on
    # or guessing the URL, not real cryptography -- anyone who views page
    # source can read it. Set a real one per client in brand_config.py
    # (ADMIN_STYLES_PIN = "1234"); this fallback is a placeholder only.
    admin_pin = getattr(C, "ADMIN_STYLES_PIN", None)
    if not admin_pin:
        admin_pin = "0000"
        print(f"WARNING: {ai_client_slug} has no ADMIN_STYLES_PIN set in brand_config.py -- "
              f"using placeholder '0000'. Set a real PIN before this site goes anywhere near live.")

    tokens = {
        "@@BUSINESS_NAME@@": C.BUSINESS_NAME,
        "@@AI_CLIENT_SLUG@@": ai_client_slug,
        "@@AI_ACCESS_KEY@@": ai_access_key,
        "@@ADMIN_STYLES_PIN@@": admin_pin,
        "@@LIVE_URL@@": live,
        "@@FIRST_PAGE_URL@@": pages[0][1],
        "@@FIRST_PAGE_NAME@@": pages[0][0],
        "@@ACCENT@@": colors["accent"],
        "@@ON_ACCENT@@": colors["on_accent"],
        "@@PAGE_LIST@@": page_list_html(),
        "@@NAV_LINKS@@": nav_links,
        "@@HERO_BADGE@@": getattr(C, "BADGE_LINE", ""),
        "@@HERO_HEADING@@": getattr(C, "HERO_HEADING", C.BUSINESS_NAME),
        "@@HERO_SUB@@": getattr(C, "HERO_SUB", ""),
        "@@ORDER_LABEL@@": getattr(C, "ORDER_LABEL", "ORDER ONLINE"),
        "@@TRUST_ROWS@@": trust_preview_html(),
        "@@FAVORITES_TAG@@": getattr(C, "FAVORITES_TAG", "FEATURED"),
        "@@FAVORITES_TITLE@@": getattr(C, "FAVORITES_TITLE", "What people love"),
        "@@FAVORITES_CARDS@@": favorites_preview_html(),
        "@@PHONE_DISPLAY@@": getattr(C, "PHONE_DISPLAY", ""),
        "@@ADDRESS_FULL@@": getattr(C, "ADDRESS_FULL", ""),
        "@@BRAND_SHORT@@": getattr(C, "BRAND_SHORT", C.BUSINESS_NAME),
        "@@FONT_HEAD@@": C.FONT_HEADING,
        "@@FONT_BODY@@": C.FONT_BODY,
        "@@DEFAULTS_JSON@@": defaults_json,
        "@@STORAGE_KEY@@": storage_key,
        "@@PHOTO_KEY@@": storage_key + "_photos",
        "@@LOG_KEY@@": storage_key + "_activity",
    }

    html = TEMPLATE
    for token, value in tokens.items():
        html = html.replace(token, str(value))

    out_name = "admin_styles_" + ai_client_slug.replace("-", "_") + ".html"
    out_path = os.path.join(S.ROOT, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("written", out_path)

# The CSS and JS below are the shared UI chrome -- deliberately identical
# across every client (George's own dark design system, not the client's
# brand). Substitution uses plain @@TOKEN@@ replace(), not str.format(), so
# every brace in this CSS/JS can be written exactly as it would run in a
# browser -- no doubled-brace escaping to keep in sync by hand.
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>Admin Styles &mdash; @@BUSINESS_NAME@@</title>
<style>
:root{
--ui-bg:#0f1115; --ui-panel:#181b22; --ui-panel2:#1f232c; --ui-border:#2b303a;
--ui-text:#e8e9ec; --ui-text-muted:#9aa0ab; --ui-accent:@@ACCENT@@; --ui-green:#7fd67f; --ui-red:#e06a5f;
--ease-spring:cubic-bezier(0.34,1.56,0.64,1);
}
*{box-sizing:border-box}
.pin-gate{position:fixed;inset:0;background:var(--ui-bg);display:flex;align-items:center;justify-content:center;z-index:1000;padding:20px}
.pin-box{background:var(--ui-panel);border:1px solid var(--ui-border);border-radius:14px;padding:36px 32px;width:min(90vw,340px);text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.5)}
.pin-box h2{font-size:17px;margin:0 0 6px;color:var(--ui-text)}
.pin-box p{font-size:13px;color:var(--ui-text-muted);margin:0 0 18px}
.pin-box input{width:100%;padding:12px 14px;border-radius:8px;border:1px solid var(--ui-border);background:var(--ui-panel2);color:var(--ui-text);font-size:20px;text-align:center;letter-spacing:.3em;margin-bottom:14px}
.pin-box input:focus{outline:none;border-color:var(--ui-accent)}
.pin-box button{width:100%}
.pin-error{display:none;color:var(--ui-red);font-size:12px;margin-top:12px}
.pin-error.show{display:block}
@keyframes tbounce{0%,60%,100%{transform:translateY(0);opacity:.5}30%{transform:translateY(-4px);opacity:1}}
@keyframes btncheck{to{stroke-dashoffset:0}}
@keyframes pillpop{0%{transform:scale(1)}50%{transform:scale(1.08)}100%{transform:scale(1)}}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(1.3)}}
body{margin:0;background:var(--ui-bg);color:var(--ui-text);font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif}

.topbar{display:flex;align-items:center;justify-content:space-between;padding:14px 22px;background:var(--ui-panel);border-bottom:1px solid var(--ui-border);flex-wrap:wrap;gap:12px}
.topbar-left{display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.topbar h1{font-size:16px;margin:0;font-weight:700}
.topbar h1 span{color:var(--ui-text-muted);font-weight:400;font-size:13px;display:block;margin-top:2px}
.topbar-actions{display:flex;gap:10px;align-items:center}
.save-status{font-size:12px;color:var(--ui-text-muted)}
button.ui-btn{background:var(--ui-panel2);color:var(--ui-text);border:1px solid var(--ui-border);padding:9px 16px;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;transition:transform .15s var(--ease-spring),border-color .15s ease,background .15s ease}
button.ui-btn:hover{border-color:var(--ui-accent)}
button.ui-btn:active{transform:scale(.96)}
button.ui-btn.primary{background:var(--ui-accent);color:@@ON_ACCENT@@;border-color:var(--ui-accent)}
button.ui-btn.primary:hover{filter:brightness(1.08)}
button.ui-btn.small{padding:6px 11px;font-size:12px}
button.ui-btn.danger:hover{border-color:var(--ui-red);color:var(--ui-red)}
.btn-dots{display:inline-flex;gap:3px;align-items:center}
.btn-dots span{width:4px;height:4px;border-radius:50%;background:currentColor;animation:tbounce 1s infinite;display:inline-block}
.btn-dots span:nth-child(2){animation-delay:.16s}
.btn-dots span:nth-child(3){animation-delay:.32s}
.btn-check{display:block}
.btn-check path{stroke-dasharray:30;stroke-dashoffset:30;animation:btncheck .35s var(--ease-spring) forwards}

.status-pill{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--ui-text-muted);background:var(--ui-panel2);border:1px solid var(--ui-border);padding:6px 12px;border-radius:999px;transition:background .2s ease}
.status-pill .sdot{width:7px;height:7px;border-radius:50%;background:var(--ui-text-muted);flex-shrink:0}
.status-pill.ok .sdot{background:var(--ui-green)}
.status-pill.err .sdot{background:var(--ui-red)}
.status-pill.syncing .sdot{background:var(--ui-accent);animation:pulse 1s infinite}
.status-pill.pop{animation:pillpop .35s var(--ease-spring)}

.tab-switch{position:relative;display:flex;gap:6px;background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:8px;padding:4px}
.tab-pill{position:absolute;top:4px;bottom:4px;left:4px;background:var(--ui-accent);border-radius:6px;transition:transform .35s var(--ease-spring),width .35s var(--ease-spring);z-index:0}
.tab-btn{position:relative;z-index:1;background:transparent;border:none;color:var(--ui-text-muted);padding:8px 16px;border-radius:6px;font-size:13px;font-weight:700;cursor:pointer;transition:color .15s ease,transform .15s var(--ease-spring)}
.tab-btn:hover{color:var(--ui-text)}
.tab-btn:active{transform:scale(.96)}
.tab-btn.active{color:@@ON_ACCENT@@}

.section{display:none}
.section.active{display:block}

.panel-section{margin-bottom:26px}
.panel-section h2{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--ui-text-muted);margin:0 0 12px}

#section-content .layout{display:grid;grid-template-columns:380px 1fr;min-height:calc(100vh - 89px)}
#section-content .sidebar.chat-col{background:var(--ui-panel);border-right:1px solid var(--ui-border);padding:0;overflow:hidden;max-height:calc(100vh - 89px);display:flex;flex-direction:column}
#section-content .main{display:flex;flex-direction:column;max-height:calc(100vh - 89px)}

.tb-item{position:relative}
.popover{display:none;position:absolute;top:calc(100% + 8px);right:0;background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:10px;padding:14px;width:290px;max-height:70vh;overflow-y:auto;z-index:30;box-shadow:0 10px 28px rgba(0,0,0,.45)}
.popover.show{display:block}

.quick-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.quick-btn{background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:7px;padding:10px 8px;font-size:12px;font-weight:600;color:var(--ui-text);cursor:pointer;text-align:center;line-height:1.3}
.quick-btn:hover{border-color:var(--ui-accent)}
.quick-btn .ic{display:block;font-size:16px;margin-bottom:4px}
.quick-form{margin-top:10px;background:var(--ui-panel);border:1px solid var(--ui-border);border-radius:8px;padding:12px;display:none}
.quick-form.show{display:block}
.quick-form label{display:block;font-size:11px;color:var(--ui-text-muted);margin:8px 0 4px}
.quick-form label:first-child{margin-top:0}
.quick-form input, .quick-form select{width:100%;padding:8px 9px;border-radius:6px;border:1px solid var(--ui-border);background:var(--ui-bg);color:var(--ui-text);font-size:13px}
.quick-form .qf-actions{display:flex;gap:8px;margin-top:12px}

.drop-zone{border:1.5px dashed var(--ui-border);border-radius:8px;padding:20px 12px;text-align:center;cursor:pointer;background:var(--ui-panel)}
.drop-zone:hover,.drop-zone.drag{border-color:var(--ui-accent);background:#262b35}
.drop-zone .ic{font-size:22px;margin-bottom:6px}
.drop-zone .txt{font-size:12.5px;color:var(--ui-text-muted)}
.drop-zone input{display:none}
.upload-list{margin-top:10px;display:flex;flex-direction:column;gap:6px}
.upload-item{display:flex;align-items:center;gap:8px;background:var(--ui-panel);border:1px solid var(--ui-border);border-radius:6px;padding:6px 8px;font-size:12px}
.upload-item img{width:28px;height:28px;object-fit:cover;border-radius:4px;flex-shrink:0}
.upload-item .nm{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.upload-item .cp{cursor:pointer;color:var(--ui-text-muted);font-size:11px;padding:2px 6px;border:1px solid var(--ui-border);border-radius:4px;flex-shrink:0}
.upload-item .cp:hover{border-color:var(--ui-accent);color:var(--ui-text)}
.upload-item .rm{cursor:pointer;color:var(--ui-text-muted);font-size:14px;padding:0 4px;flex-shrink:0}
.upload-item .rm:hover{color:var(--ui-red)}
.upload-hint{font-size:11px;color:var(--ui-text-muted);margin-top:8px;line-height:1.5}
.upload-warn{font-size:11px;color:var(--ui-accent);margin-top:6px;line-height:1.5;display:none}
.upload-warn.show{display:block}

textarea.scratchpad{width:100%;min-height:110px;resize:vertical;background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:6px;color:var(--ui-text);font-size:13px;padding:10px;font-family:inherit;line-height:1.5}
textarea.scratchpad:focus{outline:none;border-color:var(--ui-accent)}
.scratch-saved{font-size:11px;color:var(--ui-text-muted);margin-top:6px;opacity:0;transition:opacity .3s}
.scratch-saved.show{opacity:1}
.scratch-section{flex:0 0 auto;border-top:1px solid var(--ui-border)}
.scratch-toggle{width:100%;background:transparent;border:none;padding:11px 16px;font-size:12px;text-transform:uppercase;letter-spacing:.08em;font-weight:700;color:var(--ui-text-muted);cursor:pointer;text-align:left;display:flex;justify-content:space-between;align-items:center}
.scratch-toggle:hover{color:var(--ui-text)}
.scratch-body{display:none;padding:0 16px 14px}
.scratch-body.show{display:block}

.tips-body{display:none}
.tips-body.show{display:block}
.tip-chip{background:var(--ui-panel);border:1px solid var(--ui-border);border-radius:7px;padding:8px 10px;font-size:12px;margin-bottom:6px;cursor:pointer;line-height:1.4}
.tip-chip:hover{border-color:var(--ui-accent)}

.preview-wrap{flex:1;display:flex;flex-direction:column;padding:18px 22px;min-height:0}
.preview-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;flex-wrap:wrap;gap:8px}
.preview-head .lbl{font-size:12px;color:var(--ui-text-muted);text-transform:uppercase;letter-spacing:.08em}
.preview-head .right{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.page-select{background:var(--ui-panel2);border:1px solid var(--ui-border);color:var(--ui-text);padding:8px 12px;border-radius:7px;font-size:12px;font-weight:600;cursor:pointer}
.page-select:hover{border-color:var(--ui-accent)}
.device-toggle{display:flex;gap:4px;background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:7px;padding:3px}
.device-btn{background:transparent;border:none;color:var(--ui-text-muted);padding:6px 10px;border-radius:5px;font-size:12px;font-weight:600;cursor:pointer}
.device-btn:hover{color:var(--ui-text)}
.device-btn.active{background:var(--ui-accent);color:@@ON_ACCENT@@}
#section-content .preview-frame{flex:1;background:#000;border-radius:10px;overflow:hidden;border:1px solid var(--ui-border);min-height:0;display:flex;align-items:stretch;justify-content:center}
.device-frame{width:100%;height:100%;transition:max-width .18s ease;display:flex}
.device-frame.tablet{max-width:768px;border-left:1px solid var(--ui-border);border-right:1px solid var(--ui-border)}
.device-frame.mobile{max-width:390px;border-left:1px solid var(--ui-border);border-right:1px solid var(--ui-border)}
#section-content .preview-frame iframe{width:100%;height:100%;border:0;display:block;background:#0b0d11}

.chat-col{--chat-fs:13.5px}
.chat-pane,.code-pane,.prompt-pane{flex:1 1 0;min-height:0;display:flex;flex-direction:column;border-bottom:1px solid var(--ui-border)}
.prompt-pane{border-bottom:none}
.pane-head{display:flex;align-items:center;justify-content:space-between;padding:12px 16px 6px;flex-shrink:0}
.pane-head .lbl{font-size:12px;color:var(--ui-text-muted);text-transform:uppercase;letter-spacing:.08em}
.pane-actions{display:flex;gap:6px}
.fontsize-toggle{display:flex;gap:2px;background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:6px;padding:2px}
.fs-btn{background:transparent;border:none;color:var(--ui-text-muted);width:22px;height:22px;border-radius:4px;font-size:11px;font-weight:700;cursor:pointer}
.fs-btn:hover{color:var(--ui-text)}
.fs-btn.active{background:var(--ui-accent);color:@@ON_ACCENT@@}
.chat-messages{flex:1;overflow-y:auto;padding:4px 16px 12px;display:flex;flex-direction:column;gap:10px;min-height:0}
.msg{max-width:92%;padding:9px 13px;border-radius:10px;font-size:var(--chat-fs);line-height:1.5}
.msg.ai{background:var(--ui-panel2);border:1px solid var(--ui-border);align-self:flex-start;border-bottom-left-radius:2px}
.msg.ai.pending{opacity:.6}
.msg.ai.pending.typing{opacity:1;display:flex;gap:4px;align-items:center;padding:12px 16px}
.tdot{width:6px;height:6px;border-radius:50%;background:var(--ui-text-muted);animation:tbounce 1s infinite;display:inline-block}
.tdot:nth-child(2){animation-delay:.16s}
.tdot:nth-child(3){animation-delay:.32s}
.msg.user{background:var(--ui-accent);color:@@ON_ACCENT@@;align-self:flex-end;border-bottom-right-radius:2px;font-weight:600}

.code-box{flex:1;width:100%;resize:none;background:var(--ui-panel2);border:none;border-top:1px solid var(--ui-border);color:var(--ui-text);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:calc(var(--chat-fs) - 1px);padding:10px 16px;line-height:1.5}
.code-box:focus{outline:none}
.code-box::placeholder{color:var(--ui-text-muted)}
.prompt-box{flex:1;width:100%;resize:none;background:var(--ui-panel2);border:none;border-top:1px solid var(--ui-border);color:var(--ui-text);font-size:var(--chat-fs);padding:10px 16px;line-height:1.5;font-family:inherit}
.prompt-box:focus{outline:none}
.prompt-actions{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 16px 14px;flex-shrink:0}
.prompt-actions .chat-note{font-size:11px;color:var(--ui-text-muted)}

.snackbar{position:fixed;left:50%;bottom:24px;transform:translate(-50%,120%);background:var(--ui-panel);border:1px solid var(--ui-border);border-radius:10px;padding:12px 16px;display:flex;align-items:center;gap:14px;box-shadow:0 8px 24px rgba(0,0,0,.4);z-index:50;transition:transform .4s var(--ease-spring);overflow:hidden}
.snackbar.show{transform:translate(-50%,0)}
.snackbar span{font-size:13px;color:var(--ui-text)}
.snackbar-undo{background:transparent;border:none;color:var(--ui-accent);font-weight:700;font-size:13px;cursor:pointer;flex-shrink:0}
.snackbar-undo:hover{text-decoration:underline}
.snackbar-bar{position:absolute;left:0;bottom:0;height:2px;background:var(--ui-accent);width:100%;transform-origin:left;transition:transform 8s linear}
.snackbar-bar.drain{transform:scaleX(0)}

.color-row{transition:transform .3s var(--ease-spring)}
.color-row.pop{transform:scale(1.02)}

#section-style .layout{display:grid;grid-template-columns:320px 1fr;min-height:calc(100vh - 89px)}
#section-style .sidebar{background:var(--ui-panel);border-right:1px solid var(--ui-border);padding:18px;overflow-y:auto;max-height:calc(100vh - 89px)}
#section-style .main{padding:22px;overflow-y:auto;max-height:calc(100vh - 89px)}

.font-search{width:100%;padding:8px 10px;border-radius:6px;border:1px solid var(--ui-border);background:var(--ui-panel2);color:var(--ui-text);font-size:13px;margin-bottom:8px}
.font-current{background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:6px;padding:10px 12px;margin-bottom:8px;font-size:20px}
.font-current .meta{font-size:11px;color:var(--ui-text-muted);font-family:-apple-system,Segoe UI,sans-serif;margin-top:4px}
.font-list{max-height:150px;overflow-y:auto;border:1px solid var(--ui-border);border-radius:6px;background:var(--ui-panel2)}
.font-item{padding:8px 10px;cursor:pointer;font-size:14px;border-bottom:1px solid var(--ui-border)}
.font-item:last-child{border-bottom:none}
.font-item:hover{background:#262b35}
.font-item.active{background:var(--ui-accent);color:@@ON_ACCENT@@;font-weight:700}
.font-item .cat{float:right;font-size:10px;color:var(--ui-text-muted);text-transform:uppercase}
.font-item.active .cat{color:@@ON_ACCENT@@;opacity:.7}
.device-btn,.quick-btn,.font-item{transition:transform .15s var(--ease-spring),background .15s ease,border-color .15s ease}
.device-btn:active,.quick-btn:active,.font-item:active{transform:scale(.97)}

.color-row{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.color-row input[type=color]{width:36px;height:36px;border:1px solid var(--ui-border);border-radius:6px;padding:0;background:none;cursor:pointer}
.color-row .cinfo{flex:1;min-width:0}
.color-row .cname{font-size:12.5px;font-weight:600}
.color-row .cdesc{font-size:11px;color:var(--ui-text-muted)}
.color-row input[type=text]{width:78px;padding:6px 7px;border-radius:5px;border:1px solid var(--ui-border);background:var(--ui-panel2);color:var(--ui-text);font-size:12px;font-family:monospace}

#section-style .preview-frame{background:#000;border-radius:10px;overflow:hidden;border:1px solid var(--ui-border)}
.preview-label{font-size:12px;color:var(--ui-text-muted);margin:0 0 8px;text-transform:uppercase;letter-spacing:.08em}

.output-wrap{margin-top:22px}
.style-summary{background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:8px;padding:16px;font-size:13px;line-height:1.7;color:var(--ui-text);white-space:pre-line}

#section-elements .elements-wrap{padding:26px;display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;align-content:start}
.elements-cat{grid-column:1/-1;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ui-text-muted);margin:18px 0 -2px;padding-top:10px;border-top:1px solid var(--ui-border)}
.elements-cat:first-child{margin-top:0;padding-top:0;border-top:none}
.element-card{background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:10px;overflow:hidden;display:flex;flex-direction:column;transition:transform .15s var(--ease-spring),border-color .15s ease}
.element-card:hover{border-color:var(--ui-accent)}
.el-stage{background:var(--ui-bg);border-bottom:1px solid var(--ui-border);min-height:80px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;padding:10px}
.el-body{padding:14px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.el-body-head{display:flex;align-items:center;gap:8px}
.element-card .el-icon{display:inline-flex;flex-shrink:0;color:var(--ui-text-muted)}
.element-card .el-icon svg{display:block}
.element-card h3{font-size:13px;margin:0;color:var(--ui-text)}
.element-card p{font-size:11.5px;color:var(--ui-text-muted);line-height:1.5;margin:0;flex:1}
.element-card button{align-self:flex-start;margin-top:4px}

.el-demo-btn{background:var(--ui-accent);color:@@ON_ACCENT@@;border:none;padding:7px 13px;border-radius:6px;font-size:11.5px;font-weight:700;cursor:pointer;transition:transform .15s var(--ease-spring),filter .15s ease}
.el-demo-btn:hover{filter:brightness(1.08)}
.el-demo-btn:active{transform:scale(.96)}
.el-ripple-wrap{position:relative;overflow:hidden}
.el-ripple{position:absolute;border-radius:50%;background:rgba(255,255,255,.5);transform:scale(0);animation:elripple .6s ease-out forwards;pointer-events:none}
@keyframes elripple{to{transform:scale(3);opacity:0}}
.el-demo-link{color:var(--ui-text);font-size:12.5px;text-decoration:none;position:relative;padding-bottom:2px}
.el-demo-link::after{content:'';position:absolute;left:0;bottom:0;width:100%;height:2px;background:var(--ui-accent);transform:scaleX(0);transform-origin:left;transition:transform .2s ease}
.el-demo-link:hover::after{transform:scaleX(1)}
.el-fillsweep{position:relative;overflow:hidden;background:transparent;border:1.5px solid var(--ui-accent);color:var(--ui-text);border-radius:6px;padding:8px 16px;font-size:12px;font-weight:700;cursor:pointer}
.el-fillsweep::before{content:'';position:absolute;inset:0;background:var(--ui-accent);transform:scaleX(0);transform-origin:left;transition:transform .25s var(--ease-spring);z-index:0}
.el-fillsweep:hover::before{transform:scaleX(1)}
.el-fillsweep span{position:relative;z-index:1}
.el-borderdraw{position:relative;display:inline-flex;align-items:center;justify-content:center;padding:9px 20px;font-size:12px;font-weight:700;color:var(--ui-text);cursor:pointer}
.el-bd-svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.el-bd-svg rect{fill:none;stroke:var(--ui-accent);stroke-width:2;stroke-dasharray:320;stroke-dashoffset:320;transition:stroke-dashoffset .5s var(--ease-spring)}
.el-borderdraw:hover .el-bd-svg rect{stroke-dashoffset:0}
.el-borderdraw span{position:relative;z-index:1}
.el-arrow{display:inline-block;transition:transform .2s var(--ease-spring)}
.el-arrowbtn:hover .el-arrow{transform:translateX(4px)}
.el-lift{transition:transform .18s var(--ease-spring),box-shadow .18s ease}
.el-lift:hover{transform:translateY(-3px);box-shadow:0 8px 18px rgba(0,0,0,.35)}
.el-lift:active{transform:translateY(0);box-shadow:0 2px 6px rgba(0,0,0,.25)}
.el-float-wrap{position:relative;padding-top:14px}
.el-float-wrap input{background:transparent;border:none;border-bottom:1px solid var(--ui-border);color:var(--ui-text);font-size:12.5px;padding:6px 2px;width:120px;outline:none}
.el-float-wrap input:focus{border-color:var(--ui-accent)}
.el-float-wrap label{position:absolute;left:2px;top:20px;color:var(--ui-text-muted);font-size:12.5px;pointer-events:none;transition:transform .18s var(--ease-spring),color .15s ease;transform-origin:left top}
.el-float-wrap input:focus + label,.el-float-wrap input:not(:placeholder-shown) + label{transform:translateY(-18px) scale(.78);color:var(--ui-accent)}
.el-stepper{display:flex;align-items:center;gap:10px}
.el-stepper button{width:24px;height:24px;border-radius:6px;border:1px solid var(--ui-border);background:var(--ui-panel2);color:var(--ui-text);cursor:pointer;font-size:13px;line-height:1}
.el-stepper .qty{font-size:13px;font-weight:700;min-width:14px;text-align:center;display:inline-block}
.el-pop{animation:pillpop .3s var(--ease-spring)}
.el-acc{width:100%;font-size:12px}
.el-acc-head{display:flex;justify-content:space-between;align-items:center;cursor:pointer;color:var(--ui-text);font-weight:600;gap:6px}
.el-acc-head .chev{transition:transform .25s var(--ease-spring);color:var(--ui-text-muted);flex-shrink:0}
.el-acc-head.open .chev{transform:rotate(180deg)}
.el-acc-body{max-height:0;overflow:hidden;transition:max-height .3s var(--ease-spring);color:var(--ui-text-muted)}
.el-acc-body p{margin:8px 0 0;font-size:11px}
.el-mcard{width:100%;cursor:pointer}
.el-mcard-top{display:flex;justify-content:space-between;color:var(--ui-text);font-size:12px;font-weight:600}
.el-mcard-desc{max-height:0;overflow:hidden;transition:max-height .3s var(--ease-spring);color:var(--ui-text-muted);font-size:11px}
.el-mcard-desc p{margin:6px 0 0}
.el-chip{display:inline-block;padding:5px 9px;border-radius:999px;border:1px solid var(--ui-border);background:var(--ui-panel2);color:var(--ui-text-muted);font-size:10.5px;cursor:pointer;margin:2px;transition:transform .15s var(--ease-spring),background .15s ease,color .15s ease}
.el-chip.active{background:var(--ui-accent);color:@@ON_ACCENT@@;border-color:var(--ui-accent)}
.el-tabs{position:relative;display:inline-flex;gap:3px;background:var(--ui-panel);border:1px solid var(--ui-border);border-radius:7px;padding:3px}
.el-tab-pill{position:absolute;top:3px;bottom:3px;left:3px;background:var(--ui-accent);border-radius:5px;transition:transform .35s var(--ease-spring),width .35s var(--ease-spring)}
.el-tab-btn{position:relative;z-index:1;background:transparent;border:none;color:var(--ui-text-muted);padding:5px 9px;border-radius:5px;font-size:10.5px;font-weight:700;cursor:pointer}
.el-tab-btn.active{color:@@ON_ACCENT@@}
.el-skel{width:100%;height:12px;border-radius:4px;background:linear-gradient(90deg,var(--ui-panel2) 25%,#2b303a 50%,var(--ui-panel2) 75%);background-size:200% 100%;animation:elshimmer 1.4s infinite}
.el-skel + .el-skel{margin-top:6px;width:65%}
@keyframes elshimmer{to{background-position:-200% 0}}
.el-stars{font-size:15px;letter-spacing:2px;cursor:pointer;color:var(--ui-border)}
.el-star{transition:transform .15s var(--ease-spring)}
.el-star.filled{color:var(--ui-accent)}
.el-star.pop{transform:scale(1.3)}
.el-toast-demo{position:absolute;left:50%;bottom:8px;transform:translate(-50%,140%);background:var(--ui-panel);border:1px solid var(--ui-border);border-radius:8px;padding:5px 11px;font-size:10.5px;color:var(--ui-text);transition:transform .4s var(--ease-spring);white-space:nowrap}
.el-toast-demo.show{transform:translate(-50%,0)}
.el-banner-demo{position:absolute;top:0;left:0;right:0;background:var(--ui-accent);color:@@ON_ACCENT@@;font-size:10.5px;font-weight:600;padding:5px 8px;text-align:center;transform:translateY(-140%);transition:transform .4s var(--ease-spring)}
.el-banner-demo.show{transform:translateY(0)}
.el-badge-dot{width:9px;height:9px;border-radius:50%;background:var(--ui-accent);position:relative;display:inline-block}
.el-badge-dot::after{content:'';position:absolute;inset:0;border-radius:50%;background:var(--ui-accent);animation:pulse 1.4s infinite}
.el-ring{transform:rotate(-90deg)}
.el-ring circle{fill:none;stroke-width:4}
.el-ring .track{stroke:var(--ui-border)}
.el-ring .fill{stroke:var(--ui-accent);stroke-dasharray:113;animation:eldrain 4s linear infinite}
@keyframes eldrain{0%{stroke-dashoffset:0}100%{stroke-dashoffset:113}}
.el-countup{font-size:20px;font-weight:700;color:var(--ui-text)}
.el-stagger{display:flex;gap:6px}
.el-stagger span{width:13px;height:13px;border-radius:4px;background:var(--ui-accent);opacity:0;transform:translateY(8px)}
.el-stagger span.show{animation:elstagger .4s var(--ease-spring) forwards}
@keyframes elstagger{to{opacity:1;transform:translateY(0)}}
.el-type{font-size:12.5px;color:var(--ui-text);font-family:monospace}
.el-type::after{content:'|';animation:elblink 1s step-end infinite}
@keyframes elblink{50%{opacity:0}}
.el-burger{width:20px;height:14px;position:relative;cursor:pointer}
.el-burger span{position:absolute;left:0;width:100%;height:2px;background:var(--ui-text);transition:transform .25s var(--ease-spring),opacity .2s ease}
.el-burger span:nth-child(1){top:0}
.el-burger span:nth-child(2){top:6px}
.el-burger span:nth-child(3){top:12px}
.el-burger.open span:nth-child(1){transform:translateY(6px) rotate(45deg)}
.el-burger.open span:nth-child(2){opacity:0}
.el-burger.open span:nth-child(3){transform:translateY(-6px) rotate(-45deg)}
.el-fab-wrap{position:relative;display:flex;flex-direction:column-reverse;align-items:center;gap:7px}
.el-fab{width:30px;height:30px;border-radius:50%;background:var(--ui-accent);color:@@ON_ACCENT@@;border:none;font-size:13px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.el-fab-mini{width:24px;height:24px;border-radius:50%;background:var(--ui-panel);border:1px solid var(--ui-border);color:var(--ui-text);font-size:10px;display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.4) translateY(6px);transition:transform .3s var(--ease-spring),opacity .2s ease}
.el-fab-mini.show{opacity:1;transform:scale(1) translateY(0)}
.el-tip-chip{background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:6px;padding:5px 9px;font-size:10.5px;color:var(--ui-text);cursor:default;position:relative}
.el-tip-bubble{position:absolute;bottom:130%;left:50%;transform:translateX(-50%) translateY(4px);background:var(--ui-bg);border:1px solid var(--ui-border);padding:4px 7px;border-radius:5px;font-size:10px;color:var(--ui-text-muted);white-space:nowrap;opacity:0;transition:opacity .15s ease,transform .15s ease;pointer-events:none}
.el-tip-bubble.show{opacity:1;transform:translateX(-50%) translateY(0)}
.el-marquee-wrap{width:100%;overflow:hidden}
.el-marquee-track{display:inline-flex;gap:18px;white-space:nowrap;animation:elmarquee 9s linear infinite;font-size:10.5px;color:var(--ui-text-muted)}
.el-marquee-wrap:hover .el-marquee-track{animation-play-state:paused}
@keyframes elmarquee{to{transform:translateX(-50%)}}

.el-neon{font-weight:800;font-size:19px;letter-spacing:.04em;color:var(--ui-accent);text-shadow:0 0 4px var(--ui-accent),0 0 11px var(--ui-accent),0 0 22px var(--ui-accent);animation:elneon 2.8s infinite}
@keyframes elneon{0%,3%,6%,100%{opacity:1}4%{opacity:.35}5%{opacity:.85}7%{opacity:.5}8%{opacity:1}50%{opacity:1}51%{opacity:.4}52%{opacity:1}}
.el-mesh{position:relative;width:100%;height:64px;border-radius:8px;overflow:hidden;background:var(--ui-bg)}
.el-mesh span{position:absolute;border-radius:50%;filter:blur(16px);animation:elmeshdrift 6s ease-in-out infinite alternate}
.el-mesh span:nth-child(1){width:52px;height:52px;background:var(--ui-accent);opacity:.5;top:-14px;left:-4px}
.el-mesh span:nth-child(2){width:44px;height:44px;background:var(--ui-accent);opacity:.3;bottom:-16px;right:6px;animation-duration:7.5s}
.el-mesh span:nth-child(3){width:34px;height:34px;background:var(--ui-text);opacity:.14;top:8px;right:38px;animation-duration:5.5s}
@keyframes elmeshdrift{from{transform:translate(0,0) scale(1)}to{transform:translate(9px,-7px) scale(1.18)}}
.el-grad-wrap{width:100%;display:flex;flex-direction:column;gap:8px;align-items:center}
.el-grad-preview{width:100%;height:34px;border-radius:7px;transition:background .2s ease}
.el-grad-preview[data-style="flow"]{background:linear-gradient(120deg,var(--ui-accent),var(--ui-panel2),var(--ui-accent));background-size:220% 220%;animation:elgradflow 5s ease infinite}
.el-grad-preview[data-style="radial"]{background:radial-gradient(ellipse at 30% 30%,var(--ui-accent) 0%,var(--ui-panel2) 60%,var(--ui-bg) 100%)}
.el-grad-preview[data-style="diagonal"]{background:linear-gradient(135deg,var(--ui-accent) 0%,var(--ui-panel2) 50%,var(--ui-bg) 100%)}
.el-grad-preview[data-style="conic"]{background:conic-gradient(from 0deg,var(--ui-accent),var(--ui-panel2),var(--ui-accent))}
@keyframes elgradflow{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.el-grad-swatches{display:flex;gap:6px}
.el-grad-sw{width:20px;height:20px;border-radius:50%;border:2px solid transparent;cursor:pointer;padding:0}
.el-grad-sw[data-style="flow"]{background:linear-gradient(120deg,var(--ui-accent),var(--ui-panel2))}
.el-grad-sw[data-style="radial"]{background:radial-gradient(circle at 35% 35%,var(--ui-accent),var(--ui-panel2))}
.el-grad-sw[data-style="diagonal"]{background:linear-gradient(135deg,var(--ui-accent),var(--ui-panel2))}
.el-grad-sw[data-style="conic"]{background:conic-gradient(from 0deg,var(--ui-accent),var(--ui-panel2),var(--ui-accent))}
.el-grad-sw.active{border-color:var(--ui-text)}
.el-scatter{position:relative;width:100%;height:64px;display:flex;align-items:center;justify-content:center}
.el-scatter-card{position:absolute;width:44px;height:56px;border-radius:6px;background:linear-gradient(160deg,var(--ui-accent),var(--ui-panel2));border:2px solid var(--ui-panel);box-shadow:0 3px 8px rgba(0,0,0,.35);transition:transform .25s var(--ease-spring)}
.el-scatter-card.c0{transform:rotate(-10deg) translateX(-16px);z-index:1}
.el-scatter-card.c1{transform:rotate(4deg);z-index:2}
.el-scatter-card.c2{transform:rotate(13deg) translateX(16px);z-index:1}
.el-scatter-card:hover{transform:rotate(0deg) translateY(-6px) scale(1.08);z-index:3}
.el-orbit{width:100%;height:66px;display:flex;align-items:center;justify-content:center}
.el-orbit-ring{position:relative;width:56px;height:56px;animation:elorbitspin 7s linear infinite}
.el-orbit:hover .el-orbit-ring{animation-play-state:paused}
.el-orbit-dot{position:absolute;width:14px;height:14px;border-radius:50%;background:var(--ui-accent);top:50%;left:50%;margin:-7px}
.el-orbit-dot.d0{transform:translate(0,-24px)}
.el-orbit-dot.d1{transform:translate(24px,0)}
.el-orbit-dot.d2{transform:translate(0,24px)}
.el-orbit-dot.d3{transform:translate(-24px,0)}
@keyframes elorbitspin{to{transform:rotate(360deg)}}

#section-activity .activity-wrap{padding:26px;max-width:760px}
.activity-empty{font-size:13px;color:var(--ui-text-muted);background:var(--ui-panel2);border:1px dashed var(--ui-border);border-radius:8px;padding:20px;text-align:center}
.activity-item{background:var(--ui-panel2);border:1px solid var(--ui-border);border-radius:8px;padding:14px 16px;margin-bottom:10px}
.activity-top{display:flex;align-items:center;gap:8px;justify-content:space-between}
.activity-top .left{display:flex;align-items:center;gap:8px}
.activity-dot{width:8px;height:8px;border-radius:50%;background:var(--ui-text-muted);flex-shrink:0}
.activity-dot.ok{background:var(--ui-green)}
.activity-dot.err{background:var(--ui-red)}
.activity-time{font-size:11px;color:var(--ui-text-muted)}
.activity-request{font-weight:700;font-size:13.5px;margin:8px 0 4px}
.activity-detail{font-size:12.5px;color:var(--ui-text-muted);line-height:1.5}
.activity-actions{margin-top:10px}

#pv{font-family:var(--p-font-body);color:var(--p-cream);background:var(--p-bg-deep)}
#pv *{box-sizing:border-box}
#pv h1,#pv h2,#pv h3{font-family:var(--p-font-head);margin:0;line-height:1.15}
#pv .pv-nav{display:flex;align-items:center;justify-content:space-between;padding:14px 26px;background:var(--p-panel)}
#pv .pv-brand{font-family:var(--p-font-head);font-weight:700;font-size:18px;color:var(--p-cream)}
#pv .pv-nav-links{display:flex;gap:18px;font-size:12.5px;color:var(--p-cream-muted)}
#pv .pv-hero{background:radial-gradient(ellipse at 70% 30%,var(--p-primary) 0%,var(--p-primary-bright) 55%,var(--p-primary-deep) 100%);padding:40px 26px}
#pv .pv-badge{display:inline-block;background:var(--p-accent);color:var(--p-on-accent);font-size:11px;font-weight:700;padding:5px 12px;border-radius:999px;margin-bottom:14px}
#pv .pv-hero h1{font-size:30px;color:var(--p-cream)}
#pv .pv-hero p{font-size:13px;color:var(--p-cream-muted);margin-top:10px;max-width:420px}
#pv .pv-btns{margin-top:18px;display:flex;gap:10px}
#pv .pv-btn{display:inline-block;padding:11px 20px;border-radius:6px;font-weight:700;font-size:13px;cursor:pointer}
#pv .pv-btn-primary{background:var(--p-accent);color:var(--p-on-accent)}
#pv .pv-btn-ghost{background:transparent;color:var(--p-cream);border:1px solid rgba(255,255,255,.35)}
#pv .pv-trust{display:flex;gap:0;background:var(--p-bg-deep);padding:20px 26px;border-bottom:1px solid rgba(255,255,255,.08)}
#pv .pv-trust-item{flex:1;text-align:center}
#pv .pv-trust-item .num{font-weight:700;font-family:var(--p-font-head);color:var(--p-cream)}
#pv .pv-trust-item .lbl{font-size:10.5px;color:var(--p-cream-muted);margin-top:2px}
#pv .pv-section{padding:30px 26px;background:var(--p-bg-deep)}
#pv .pv-tag{color:var(--p-accent);font-weight:700;letter-spacing:.12em;font-size:11px;text-transform:uppercase}
#pv .pv-section h2{font-size:22px;color:var(--p-cream);margin-top:6px}
#pv .pv-cards{display:flex;gap:14px;margin-top:18px}
#pv .pv-card{flex:1;background:var(--p-panel);border-radius:10px;padding:16px}
#pv .pv-card h3{font-size:14px;color:var(--p-cream)}
#pv .pv-card p{font-size:11.5px;color:var(--p-cream-muted);margin-top:6px}
#pv .pv-card .price{color:var(--p-accent);font-weight:700;font-size:12px;margin-top:8px}
#pv .pv-cta{background:linear-gradient(135deg,var(--p-primary),var(--p-primary-bright));text-align:center;padding:38px 26px}
#pv .pv-cta h2{color:var(--p-cream);font-size:24px}
#pv .pv-cta p{color:var(--p-cream-muted);font-size:12.5px;margin-top:8px}
#pv .pv-foot{background:var(--p-ink);padding:24px 26px;font-size:11.5px;color:var(--p-cream-muted)}
</style>
</head>
<body>

<div class="pin-gate" id="pinGate">
<div class="pin-box">
<h2>@@BUSINESS_NAME@@ &mdash; Admin Styles</h2>
<p>Enter your access PIN to continue.</p>
<input type="password" inputmode="numeric" autocomplete="off" id="pinInput" placeholder="PIN">
<button class="ui-btn primary" id="pinSubmitBtn">Unlock</button>
<div class="pin-error" id="pinError">That PIN isn't right. Try again.</div>
</div>
</div>

<div id="appContent" style="display:none">
<div class="topbar">
<div class="topbar-left">
<h1>Admin Styles <span>@@BUSINESS_NAME@@ &mdash; manage content &amp; style in one place</span></h1>
<div class="tab-switch" id="tabSwitch">
<div class="tab-pill" id="tabPill"></div>
<button class="tab-btn active" data-tab="content">Content &amp; Preview</button>
<button class="tab-btn" data-tab="style">Style Editor</button>
<button class="tab-btn" data-tab="elements">Add-ons</button>
<button class="tab-btn" data-tab="activity">Activity</button>
</div>
<div class="status-pill" id="statusPill"><span class="sdot"></span><span id="statusPillText">No AI edits yet</span></div>
</div>
<div class="topbar-actions" id="contentActions">
<span class="save-status" id="saveStatus">All changes saved</span>
<button class="ui-btn" id="draftBtn">Save Draft</button>
<button class="ui-btn primary" id="publishBtn">Publish</button>
</div>
<div class="topbar-actions" id="styleActions" style="display:none">
<button class="ui-btn" id="resetBtn">Reset to current site</button>
<button class="ui-btn primary" id="publishStyleBtn">Publish style changes</button>
</div>
<div class="topbar-actions" id="activityActions" style="display:none">
<button class="ui-btn small danger" id="clearLogBtn">Clear log</button>
</div>
</div>

<div class="snackbar" id="undoSnackbar">
<span id="snackbarText">Change applied</span>
<button class="snackbar-undo" id="snackbarUndoBtn">Undo</button>
<div class="snackbar-bar" id="snackbarBar"></div>
</div>

<div class="section active" id="section-content">
<div class="layout">
<div class="sidebar chat-col">
<div class="chat-pane">
<div class="pane-head">
<span class="lbl">Ask the site assistant</span>
<div class="fontsize-toggle" id="fontSizeToggle">
<button class="fs-btn" data-size="sm" title="Small text">S</button>
<button class="fs-btn active" data-size="md" title="Medium text">M</button>
<button class="fs-btn" data-size="lg" title="Large text">L</button>
</div>
</div>
<div class="chat-messages" id="chatMessages">
<div class="msg ai">Hi! Tell me what you'd like to change on your site, and I'll take care of it. No coding needed.</div>
</div>
</div>
<div class="code-pane">
<div class="pane-head">
<span class="lbl">Code to add</span>
<div class="pane-actions">
<button class="ui-btn small" id="codeClearBtn">Clear</button>
</div>
</div>
<textarea class="code-box" id="codeBox" placeholder="Pick something from Quick Actions or Add-ons and the exact instructions land here -- separate from your message below, so your note stays short and the technical detail stays precise. You can also type or edit this directly."></textarea>
</div>
<div class="prompt-pane">
<div class="pane-head"><span class="lbl">Your message</span></div>
<textarea class="prompt-box" id="chatInput" placeholder="Describe the change you want... (Enter to send, Shift+Enter for a new line)"></textarea>
<div class="prompt-actions">
<span class="chat-note">Connects to the live AI Update Pipeline (och-ai-site-editor Worker).</span>
<button class="ui-btn primary" id="sendBtn">Send</button>
</div>
</div>
<div class="scratch-section">
<button class="scratch-toggle" id="scratchToggle"><span>Scratchpad</span><span id="scratchChevron">&#9660;</span></button>
<div class="scratch-body" id="scratchBody">
<textarea class="scratchpad" id="scratchpad" placeholder="Jot down ideas, TODOs, or notes for next time... (autosaves)"></textarea>
<div class="scratch-saved" id="scratchSaved">Saved</div>
</div>
</div>
</div>
<div class="main">
<div class="preview-wrap">
<div class="preview-head">
<span class="lbl" id="previewLabel">Live preview &mdash; Home</span>
<div class="right">
<select class="page-select" id="pageSelect">
@@PAGE_LIST@@
</select>
<div class="device-toggle" id="deviceToggle">
<button class="device-btn active" data-device="desktop">Desktop</button>
<button class="device-btn" data-device="tablet">Tablet</button>
<button class="device-btn" data-device="mobile">Mobile</button>
</div>
<button class="ui-btn" id="refreshBtn">Refresh</button>
<button class="ui-btn" id="openBtn">Open in new tab</button>
<div class="tb-item">
<button class="ui-btn" id="quickActionsBtn">Quick Actions</button>
<div class="popover" id="quickActionsPopover">
<div class="quick-grid" id="quickGrid"></div>
<div class="quick-form" id="quickForm"></div>
</div>
</div>
<div class="tb-item">
<button class="ui-btn" id="uploadPhotosBtn">Upload Photos</button>
<div class="popover" id="uploadPhotosPopover">
<div class="drop-zone" id="dropZone">
<div class="ic">&#128247;</div>
<div class="txt">Drop images here or click to browse</div>
<input type="file" id="fileInput" accept="image/*" multiple>
</div>
<div class="upload-list" id="uploadList"></div>
<div class="upload-hint">Uploaded photos are saved to this browser and available to reference in chat by name &mdash; e.g. "use hero.jpg for the hero slideshow."</div>
<div class="upload-warn" id="uploadWarn">Photo library is getting large &mdash; the oldest photo was removed to make room. Consider keeping fewer, smaller images.</div>
</div>
</div>
<div class="tb-item">
<button class="ui-btn" id="tipsBtn">Tips</button>
<div class="popover" id="tipsPopover">
<div class="tips-body show" id="tipsBody"></div>
</div>
</div>
</div>
</div>
<div class="preview-frame">
<div class="device-frame" id="deviceFrame">
<iframe id="previewFrame" src="@@FIRST_PAGE_URL@@" title="Site preview"></iframe>
</div>
</div>
</div>
</div>
</div>
</div>

<div class="section" id="section-style">
<div class="layout">
<div class="sidebar">
<div class="panel-section">
<h2>Heading font</h2>
<div class="font-current" id="headCurrent" style="font-family:'@@FONT_HEAD@@',Georgia,serif">@@FONT_HEAD@@
<div class="meta">Used for all headings and the nav wordmark.</div>
</div>
<input type="text" class="font-search" id="headSearch" placeholder="Search fonts...">
<div class="font-list" id="headList"></div>
</div>
<div class="panel-section">
<h2>Body font</h2>
<div class="font-current" id="bodyCurrent" style="font-family:'@@FONT_BODY@@',system-ui,sans-serif;font-size:16px">@@FONT_BODY@@
<div class="meta">Used for paragraphs, nav links, and buttons.</div>
</div>
<input type="text" class="font-search" id="bodySearch" placeholder="Search fonts...">
<div class="font-list" id="bodyList"></div>
</div>
<div class="panel-section">
<h2>Colors</h2>
<div id="colorRows"></div>
</div>
</div>
<div class="main">
<p class="preview-label">Live preview (mirrors the actual homepage sections)</p>
<div class="preview-frame">
<div id="pv">
<div class="pv-nav">
<div class="pv-brand">@@BRAND_SHORT@@</div>
<div class="pv-nav-links">@@NAV_LINKS@@</div>
</div>
<div class="pv-hero">
<span class="pv-badge">@@HERO_BADGE@@</span>
<h1>@@HERO_HEADING@@</h1>
<p>@@HERO_SUB@@</p>
<div class="pv-btns">
<span class="pv-btn pv-btn-primary">@@ORDER_LABEL@@</span>
<span class="pv-btn pv-btn-ghost">View full menu</span>
</div>
</div>
<div class="pv-trust">
@@TRUST_ROWS@@
</div>
<div class="pv-section">
<span class="pv-tag">@@FAVORITES_TAG@@</span>
<h2>@@FAVORITES_TITLE@@</h2>
<div class="pv-cards">
@@FAVORITES_CARDS@@
</div>
</div>
<div class="pv-cta">
<h2>Ready when you are</h2>
<p>@@ADDRESS_FULL@@ &middot; @@PHONE_DISPLAY@@</p>
<div class="pv-btns" style="justify-content:center">
<span class="pv-btn pv-btn-primary">@@ORDER_LABEL@@</span>
<span class="pv-btn pv-btn-ghost">Call @@PHONE_DISPLAY@@</span>
</div>
</div>
<div class="pv-foot">
<div class="fh">@@BRAND_SHORT@@</div>
@@ADDRESS_FULL@@ &middot; @@PHONE_DISPLAY@@
</div>
</div>
</div>
<div class="output-wrap">
<p class="preview-label" style="margin:0 0 8px">This is what will be sent to your site assistant when you hit "Publish style changes"</p>
<div class="style-summary" id="styleSummary"></div>
</div>
</div>
</div>
</div>

<div class="section" id="section-elements">
<div class="elements-wrap">
<p class="preview-label" style="grid-column:1/-1;margin:0 0 4px">Pick something below to add to your live site. Clicking "Add to my site" fills in a request for the site assistant on the Content &amp; Preview tab &mdash; review it, then hit Send.</p>
<div id="elementsGrid" style="display:contents"></div>
</div>
</div>

<div class="section" id="section-activity">
<div class="activity-wrap">
<p class="preview-label">Every request sent to the site assistant, with its outcome. Use "Ask AI to undo" to reverse a change through the same assistant &mdash; there's no separate rollback system, this just sends a new request.</p>
<div class="activity-empty" id="activityEmpty">No activity yet. Changes you request in the chat on the Content &amp; Preview tab will show up here.</div>
<div class="activity-list" id="activityList"></div>
</div>
</div>

<script>
// Page-view PIN gate. This is a deterrent, not real security -- the PIN is
// sitting in this static file's source, so anyone who opens dev tools can
// read it. It stops someone from casually opening or stumbling on this URL
// and poking around. The actual security boundary (whether a change can be
// applied to the live site at all) is the AI_ACCESS_KEY code checked by the
// och-ai-site-editor Worker itself on every Send, further down this script --
// that one is validated server-side and isn't in this file.
const ADMIN_PIN = "@@ADMIN_STYLES_PIN@@";
const PIN_UNLOCK_KEY = "@@STORAGE_KEY@@_unlocked";
const pinGate = document.getElementById('pinGate');
const appContent = document.getElementById('appContent');
const pinInput = document.getElementById('pinInput');
const pinError = document.getElementById('pinError');
function unlockAdminStyles(){
pinGate.style.display = 'none';
appContent.style.display = '';
try { localStorage.setItem(PIN_UNLOCK_KEY, '1'); } catch(e){}
}
function tryPinUnlock(){
if (pinInput.value.trim() === ADMIN_PIN) {
unlockAdminStyles();
} else {
pinError.classList.add('show');
pinInput.value = '';
pinInput.focus();
}
}
let alreadyUnlocked = false;
try { alreadyUnlocked = localStorage.getItem(PIN_UNLOCK_KEY) === '1'; } catch(e){}
if (alreadyUnlocked) {
unlockAdminStyles();
} else {
pinInput.focus();
}
document.getElementById('pinSubmitBtn').addEventListener('click', tryPinUnlock);
pinInput.addEventListener('keydown', e => { if (e.key === 'Enter') tryPinUnlock(); });

const TAB_SECTIONS = ['content','style','elements','activity'];
const tabPill = document.getElementById('tabPill');
function positionTabPill(){
const active = document.querySelector('.tab-btn.active');
if (!active || !tabPill) return;
tabPill.style.width = active.offsetWidth + 'px';
tabPill.style.transform = 'translateX(' + active.offsetLeft + 'px)';
}
document.querySelectorAll('.tab-btn').forEach(btn => {
btn.addEventListener('click', () => switchTab(btn.dataset.tab));
});
function switchTab(tab){
document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tab));
TAB_SECTIONS.forEach(t => document.getElementById('section-' + t).classList.toggle('active', t === tab));
document.getElementById('contentActions').style.display = tab === 'content' ? 'flex' : 'none';
document.getElementById('styleActions').style.display = tab === 'style' ? 'flex' : 'none';
document.getElementById('activityActions').style.display = tab === 'activity' ? 'flex' : 'none';
positionTabPill();
}
positionTabPill();
window.addEventListener('resize', positionTabPill);

const previewFrame = document.getElementById('previewFrame');
const previewLabel = document.getElementById('previewLabel');
const openBtn = document.getElementById('openBtn');
const refreshBtn = document.getElementById('refreshBtn');
const pageSelect = document.getElementById('pageSelect');
// Tracks which page is showing in the preview so sendMessage() can tell the
// assistant what the owner is looking at -- e.g. typing "change the price of
// Root Beer" while viewing Menu now tells the AI it's on the Menu page,
// instead of the request landing with zero page context. The AI Worker never
// receives a page/URL field on its own; this is folded into the message text.
let currentPageName = '@@FIRST_PAGE_NAME@@';
function setActivePageFromSelect(){
const opt = pageSelect.options[pageSelect.selectedIndex];
const url = opt.value, name = opt.dataset.name;
currentPageName = name;
previewFrame.src = url;
previewLabel.textContent = 'Live preview — ' + name;
openBtn.onclick = () => window.open(url, '_blank', 'noopener');
}
pageSelect.addEventListener('change', setActivePageFromSelect);
openBtn.onclick = () => window.open(previewFrame.src, '_blank', 'noopener');
refreshBtn.onclick = () => { previewFrame.src = previewFrame.src; };

const deviceFrame = document.getElementById('deviceFrame');
const deviceToggleEl = document.getElementById('deviceToggle');
deviceToggleEl.querySelectorAll('.device-btn').forEach(btn => {
btn.addEventListener('click', () => {
deviceToggleEl.querySelectorAll('.device-btn').forEach(b => b.classList.remove('active'));
btn.classList.add('active');
deviceFrame.className = 'device-frame ' + (btn.dataset.device === 'desktop' ? '' : btn.dataset.device);
});
});

// Popover buttons (Quick Actions / Upload Photos / Scratchpad / Tips) --
// each toggles a small floating panel anchored under its top-toolbar button.
// Only one open at a time; clicking outside any .tb-item closes them all.
const POPOVERS = [
['quickActionsBtn','quickActionsPopover'],
['uploadPhotosBtn','uploadPhotosPopover'],
['tipsBtn','tipsPopover'],
];
function closeAllPopovers(){
POPOVERS.forEach(([, popId]) => document.getElementById(popId).classList.remove('show'));
}
POPOVERS.forEach(([btnId, popId]) => {
const btn = document.getElementById(btnId);
const pop = document.getElementById(popId);
btn.addEventListener('click', e => {
e.stopPropagation();
const willShow = !pop.classList.contains('show');
closeAllPopovers();
if (willShow) pop.classList.add('show');
});
});
document.addEventListener('click', e => { if (!e.target.closest('.tb-item')) closeAllPopovers(); });

// Chat text-size toggle (S/M/L) -- scales the messages, code, and prompt
// panes together via the --chat-fs CSS variable on .chat-col, persisted
// per site so it sticks between visits.
const FS_MAP = { sm:'12px', md:'13.5px', lg:'15.5px' };
const FS_KEY = '@@STORAGE_KEY@@_chat_fontsize';
const chatColEl = document.querySelector('.chat-col');
function applyFontSize(size){
chatColEl.style.setProperty('--chat-fs', FS_MAP[size] || FS_MAP.md);
document.querySelectorAll('#fontSizeToggle .fs-btn').forEach(b => b.classList.toggle('active', b.dataset.size === size));
try { localStorage.setItem(FS_KEY, size); } catch(e){}
}
document.querySelectorAll('#fontSizeToggle .fs-btn').forEach(b => b.addEventListener('click', () => applyFontSize(b.dataset.size)));
applyFontSize(localStorage.getItem(FS_KEY) || 'md');

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadList = document.getElementById('uploadList');
const uploadWarn = document.getElementById('uploadWarn');
const PHOTO_KEY = '@@PHOTO_KEY@@';
const PHOTO_MAX_COUNT = 20;
const PHOTO_MAX_TOTAL_CHARS = 6000000;

function loadPhotos(){
try { return JSON.parse(localStorage.getItem(PHOTO_KEY)) || []; } catch(e){ return []; }
}
function savePhotos(list){
try { localStorage.setItem(PHOTO_KEY, JSON.stringify(list)); } catch(e){}
}
function renderPhotos(){
const list = loadPhotos();
uploadList.innerHTML = '';
list.forEach(p => {
const row = document.createElement('div');
row.className = 'upload-item';
row.innerHTML = `<img src="${p.dataUrl}" alt=""><span class="nm">${p.name}</span><span class="cp" title="Copy filename to reference in chat">Copy</span><span class="rm">&times;</span>`;
row.querySelector('.cp').onclick = () => {
navigator.clipboard.writeText(p.name);
const cp = row.querySelector('.cp');
const old = cp.textContent;
cp.textContent = 'Copied';
setTimeout(() => { cp.textContent = old; }, 1200);
};
row.querySelector('.rm').onclick = () => {
const updated = loadPhotos().filter(x => x.id !== p.id);
savePhotos(updated);
renderPhotos();
};
uploadList.appendChild(row);
});
}

dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag'));
dropZone.addEventListener('drop', e => {
e.preventDefault();
dropZone.classList.remove('drag');
handleFiles(e.dataTransfer.files);
});
fileInput.addEventListener('change', () => handleFiles(fileInput.files));

function handleFiles(files){
Array.from(files).forEach(file => {
if (!file.type.startsWith('image/')) return;
const reader = new FileReader();
reader.onload = e => {
let list = loadPhotos();
list.push({ id: 'p' + Date.now() + Math.random().toString(36).slice(2,7), name: file.name, dataUrl: e.target.result, addedAt: Date.now() });
let trimmed = false;
while ((list.length > PHOTO_MAX_COUNT || JSON.stringify(list).length > PHOTO_MAX_TOTAL_CHARS) && list.length > 1) {
list.shift();
trimmed = true;
}
savePhotos(list);
renderPhotos();
if (trimmed) {
uploadWarn.classList.add('show');
setTimeout(() => uploadWarn.classList.remove('show'), 4000);
}
};
reader.readAsDataURL(file);
});
}
renderPhotos();

const scratchToggle = document.getElementById('scratchToggle');
const scratchBody = document.getElementById('scratchBody');
scratchToggle.addEventListener('click', () => {
scratchBody.classList.toggle('show');
document.getElementById('scratchChevron').innerHTML = scratchBody.classList.contains('show') ? '&#9650;' : '&#9660;';
});

const SCRATCH_KEY = '@@STORAGE_KEY@@_scratchpad';
const scratchpad = document.getElementById('scratchpad');
const scratchSaved = document.getElementById('scratchSaved');
scratchpad.value = localStorage.getItem(SCRATCH_KEY) || '';
let scratchTimer;
scratchpad.addEventListener('input', () => {
clearTimeout(scratchTimer);
scratchTimer = setTimeout(() => {
localStorage.setItem(SCRATCH_KEY, scratchpad.value);
scratchSaved.classList.add('show');
setTimeout(() => scratchSaved.classList.remove('show'), 1200);
}, 500);
});

const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const codeBox = document.getElementById('codeBox');
const sendBtn = document.getElementById('sendBtn');
document.getElementById('codeClearBtn').addEventListener('click', () => { codeBox.value = ''; codeBox.focus(); });
const AI_WORKER_URL = "https://och-ai-site-editor.odd-breeze-0195.workers.dev";
const AI_CLIENT_SLUG = "@@AI_CLIENT_SLUG@@";
const AI_ACCESS_KEY = "@@AI_ACCESS_KEY@@";
let aiAccessCode = localStorage.getItem(AI_ACCESS_KEY) || "";

const undoSnackbar = document.getElementById('undoSnackbar');
const snackbarText = document.getElementById('snackbarText');
const snackbarBar = document.getElementById('snackbarBar');
const snackbarUndoBtn = document.getElementById('snackbarUndoBtn');
let snackbarTimer;
function showUndoSnackbar(requestText){
clearTimeout(snackbarTimer);
snackbarText.textContent = 'Change applied';
snackbarBar.classList.remove('drain');
void snackbarBar.offsetWidth;
undoSnackbar.classList.add('show');
requestAnimationFrame(() => snackbarBar.classList.add('drain'));
snackbarUndoBtn.onclick = () => {
switchTab('content');
chatInput.value = 'Please undo this change: "' + requestText + '"';
chatInput.focus();
hideSnackbar();
};
snackbarTimer = setTimeout(hideSnackbar, 8000);
}
function hideSnackbar(){
undoSnackbar.classList.remove('show');
clearTimeout(snackbarTimer);
}

function setBtnState(btn, state){
if (state === 'loading') {
if (!btn.dataset.label) btn.dataset.label = btn.textContent;
btn.innerHTML = '<span class="btn-dots"><span></span><span></span><span></span></span>';
} else if (state === 'success') {
btn.innerHTML = '<svg class="btn-check" viewBox="0 0 24 24" width="14" height="14"><path d="M4 12l5 5L20 6" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>';
} else {
btn.textContent = btn.dataset.label || btn.textContent;
}
}

function addMsg(text, who){
const div = document.createElement('div');
div.className = 'msg ' + who;
div.textContent = text;
chatMessages.appendChild(div);
chatMessages.scrollTop = chatMessages.scrollHeight;
return div;
}
function addTypingIndicator(){
const div = document.createElement('div');
div.className = 'msg ai pending typing';
div.innerHTML = '<span class="tdot"></span><span class="tdot"></span><span class="tdot"></span>';
chatMessages.appendChild(div);
chatMessages.scrollTop = chatMessages.scrollHeight;
return div;
}

function ensureAccessCode(){
if (aiAccessCode) return true;
const code = window.prompt("Enter your site's access code to send this change:");
if (!code) return false;
aiAccessCode = code.trim();
localStorage.setItem(AI_ACCESS_KEY, aiAccessCode);
return true;
}

async function sendMessage(){
const userText = chatInput.value.trim();
const codeText = codeBox.value.trim();
const text = userText && codeText ? (userText + '\\n\\n' + codeText) : (userText || codeText);
if (!text) return;
if (!ensureAccessCode()) return;
addMsg(userText || codeText, 'user');
chatInput.value = '';
codeBox.value = '';
sendBtn.disabled = true;
setBtnState(sendBtn, 'loading');
const pending = addTypingIndicator();
try {
const taggedMessage = '[Admin Styles preview is currently showing the ' + currentPageName + ' page]\\n' + text;
const res = await fetch(AI_WORKER_URL, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ client: AI_CLIENT_SLUG, message: taggedMessage, code: aiAccessCode })
});
const data = await res.json();
pending.remove();
if (res.status === 401) {
addMsg('Your access code was rejected. Please refresh and re-enter it.', 'ai');
localStorage.removeItem(AI_ACCESS_KEY);
aiAccessCode = '';
logActivity(text, 'err', 'Access code rejected.');
setBtnState(sendBtn, 'idle');
return;
}
if (!data.success) {
addMsg(data.error || 'Something went wrong.', 'ai');
logActivity(text, 'err', data.error || 'Something went wrong.');
setBtnState(sendBtn, 'idle');
return;
}
addMsg(data.summary, 'ai');
if (data.note) addMsg(data.note, 'ai');
logActivity(text, 'ok', data.summary + (data.note ? ' ' + data.note : ''));
setBtnState(sendBtn, 'success');
setTimeout(() => setBtnState(sendBtn, 'idle'), 1400);
statusPill.className = 'status-pill syncing';
statusPillText.textContent = 'Redeploying your site…';
showUndoSnackbar(text);
setTimeout(() => { previewFrame.src = previewFrame.src; updateStatusPill(); }, 65000);
} catch (err) {
pending.remove();
addMsg('Could not reach the editor. Check your connection and try again.', 'ai');
logActivity(text, 'err', 'Could not reach the editor.');
setBtnState(sendBtn, 'idle');
} finally {
sendBtn.disabled = false;
}
}
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } });

document.getElementById('draftBtn').addEventListener('click', () => {
document.getElementById('saveStatus').textContent = 'Draft saved';
const b = document.getElementById('draftBtn');
setBtnState(b, 'success');
setTimeout(() => setBtnState(b, 'idle'), 1400);
});
document.getElementById('publishBtn').addEventListener('click', () => {
document.getElementById('saveStatus').textContent = 'Published (prototype — no live deploy wired)';
const b = document.getElementById('publishBtn');
setBtnState(b, 'success');
setTimeout(() => setBtnState(b, 'idle'), 1400);
});

const QUICK_ACTIONS = [
{ id:'hours', label:'Update hours', icon:'&#128337;', fields:[
{ key:'day', label:'Day', type:'select', options:['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Every day'] },
{ key:'open', label:'Opening time', type:'text', placeholder:'e.g. 11:00 AM' },
{ key:'close', label:'Closing time', type:'text', placeholder:'e.g. 10:00 PM' },
], compose:(v) => `Please update the hours for ${v.day} to ${v.open} to ${v.close}.` },
{ id:'phone', label:'Update phone number', icon:'&#128222;', fields:[
{ key:'phone', label:'New phone number', type:'text', placeholder:'@@PHONE_DISPLAY@@' },
], compose:(v) => `Please update the phone number to ${v.phone}.` },
{ id:'address', label:'Update address', icon:'&#128205;', fields:[
{ key:'address', label:'New address', type:'text', placeholder:'@@ADDRESS_FULL@@' },
], compose:(v) => `Please update the business address to ${v.address}.` },
{ id:'price', label:'Change a price', icon:'&#128181;', fields:[
{ key:'item', label:'Menu item', type:'text', placeholder:'e.g. an item currently on the menu' },
{ key:'price', label:'New price', type:'text', placeholder:'e.g. 18' },
], compose:(v) => `Please update the price of ${v.item} to $${v.price}.` },
{ id:'menuitem', label:'Add a menu item', icon:'&#127860;', fields:[
{ key:'name', label:'Item name', type:'text', placeholder:'' },
{ key:'desc', label:'Description', type:'text', placeholder:'' },
{ key:'price', label:'Price', type:'text', placeholder:'e.g. 18' },
], compose:(v) => `Please add a new menu item called "${v.name}": ${v.desc}, priced at $${v.price}.` },
];

const quickGrid = document.getElementById('quickGrid');
const quickForm = document.getElementById('quickForm');

QUICK_ACTIONS.forEach(action => {
const btn = document.createElement('button');
btn.className = 'quick-btn';
btn.type = 'button';
btn.innerHTML = `<span class="ic">${action.icon}</span>${action.label}`;
btn.addEventListener('click', () => openQuickForm(action));
quickGrid.appendChild(btn);
});

function openQuickForm(action){
if (quickForm.classList.contains('show') && quickForm.dataset.action === action.id) {
quickForm.classList.remove('show');
quickForm.dataset.action = '';
return;
}
quickForm.dataset.action = action.id;
quickForm.innerHTML = '';
const values = {};
action.fields.forEach(f => {
const label = document.createElement('label');
label.textContent = f.label;
quickForm.appendChild(label);
let input;
if (f.type === 'select') {
input = document.createElement('select');
f.options.forEach(opt => {
const o = document.createElement('option');
o.value = opt; o.textContent = opt;
input.appendChild(o);
});
} else {
input = document.createElement('input');
input.type = 'text';
if (f.placeholder) input.placeholder = f.placeholder;
}
input.addEventListener('input', () => { values[f.key] = input.value; });
input.addEventListener('keydown', e => { if (e.key === 'Enter') submitBtn.click(); });
values[f.key] = f.type === 'select' ? f.options[0] : '';
quickForm.appendChild(input);
});
const actionsRow = document.createElement('div');
actionsRow.className = 'qf-actions';
const submitBtn = document.createElement('button');
submitBtn.className = 'ui-btn primary small';
submitBtn.type = 'button';
submitBtn.textContent = 'Fill code field';
submitBtn.addEventListener('click', () => {
codeBox.value = action.compose(values);
chatInput.focus();
quickForm.classList.remove('show');
quickForm.dataset.action = '';
closeAllPopovers();
});
const cancelBtn = document.createElement('button');
cancelBtn.className = 'ui-btn small';
cancelBtn.type = 'button';
cancelBtn.textContent = 'Cancel';
cancelBtn.addEventListener('click', () => {
quickForm.classList.remove('show');
quickForm.dataset.action = '';
});
actionsRow.appendChild(submitBtn);
actionsRow.appendChild(cancelBtn);
quickForm.appendChild(actionsRow);
quickForm.classList.add('show');
}

// =============================================================================
// ADD-ONS (ELEMENTS) -- optional site touches the owner can request with one
// click. Each one fills the chat with a precise, pre-written instruction
// instead of a vague label, so the AI's edit is consistent every time.
// =============================================================================
const ELEMENTS = [
{ id:'bouncebuttons', cat:'Buttons & Links', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg>', title:'Bouncy buttons', desc:'A springy hover/press effect on your call-to-action buttons (Order Online, Call, View Menu).',
compose:() => `Please add a springy hover/press effect to the main call-to-action buttons on my site (things like Order Online, Call, View Menu). On hover, brighten the button slightly. On press/click, scale it down to about 96% using this easing curve: cubic-bezier(0.34, 1.56, 0.64, 1), over roughly 150ms, via a CSS transition on transform. Do not change any button colors, sizes, fonts, or text -- only add this hover/press motion.`,
demo:(s) => { s.innerHTML = '<button class="el-demo-btn">Order Online</button>'; } },
{ id:'ripple', cat:'Buttons & Links', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="19" r="1"/><path d="M8.5 15.5a5 5 0 0 1 7 0"/><path d="M5.5 12a9 9 0 0 1 13 0"/></svg>', title:'Ripple click feedback', desc:'A circle ripples outward from the exact spot a button or link is clicked, then fades.',
compose:() => `Please add a material-style ripple effect to my site's buttons and clickable nav links: when clicked, a circle should expand outward from the exact point clicked and fade out, using a light semi-transparent version of my accent color. Do not change button colors, sizes, or text -- only add this click ripple.`,
demo:(s) => {
s.innerHTML = '<button class="el-demo-btn el-ripple-wrap">Tap me</button>';
const btn = s.querySelector('button');
btn.addEventListener('click', e => {
const r = document.createElement('span');
r.className = 'el-ripple';
const rect = btn.getBoundingClientRect();
const size = Math.max(rect.width, rect.height);
r.style.width = r.style.height = size + 'px';
r.style.left = (e.clientX - rect.left - size/2) + 'px';
r.style.top = (e.clientY - rect.top - size/2) + 'px';
btn.appendChild(r);
setTimeout(() => r.remove(), 650);
});
} },
{ id:'underline', cat:'Buttons & Links', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 15l6-6"/><path d="M11 6l.5-.5a4 4 0 0 1 5.5 5.5l-.5.5"/><path d="M13 18l-.5.5a4 4 0 0 1-5.5-5.5l.5-.5"/></svg>', title:'Hover underline on links', desc:'A thin underline smoothly draws in under a text link when someone hovers over it.',
compose:() => `Please add an animated underline to my site's text links (nav links and in-page links): on hover, a thin underline should draw in smoothly from left to right beneath the link text, in my accent color, over about 200ms. Don't add this to buttons, only plain text links.`,
demo:(s) => { s.innerHTML = '<a class="el-demo-link" href="javascript:void(0)">Hover this link</a>'; } },
{ id:'fillsweep', cat:'Buttons & Links', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 4h6v16H4z" fill="currentColor" stroke="none"/></svg>', title:'Color fill sweep', desc:'A button\\'s outline fills solid with your accent color, sweeping in from the left as someone hovers over it.',
compose:() => `Please add a fill-sweep hover effect to my secondary/outline-style buttons: on hover, a solid background in my accent color should sweep in from the left edge to fully fill the button over about 250ms, and the text color should adjust for contrast against the fill. On mouse-leave, reverse the sweep. Don't change button sizes or text, and don't apply this to already-solid primary buttons.`,
demo:(s) => { s.innerHTML = '<button class="el-fillsweep"><span>Reserve</span></button>'; } },
{ id:'borderdraw', cat:'Buttons & Links', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" stroke-dasharray="4 3"/></svg>', title:'Border draw-in', desc:'An outline button\\'s border traces itself in around the edge on hover, instead of just appearing.',
compose:() => `Please add a "border draw-in" hover effect to my outline-style buttons: on hover, the border should animate as if being traced around the button's perimeter (using an SVG rect with stroke-dasharray/stroke-dashoffset transitioning to 0 over about 400-500ms), rather than the border simply becoming visible instantly. Use my accent color for the traced border. Don't change the button's size, text, or fill.`,
demo:(s) => { s.innerHTML = '<div class="el-borderdraw"><svg class="el-bd-svg" viewBox="0 0 120 44" preserveAspectRatio="none"><rect x="1" y="1" width="118" height="42" rx="8"></rect></svg><span>Hover me</span></div>'; } },
{ id:'arrowslide', cat:'Buttons & Links', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h14"/><path d="M13 6l6 6-6 6"/></svg>', title:'Sliding arrow icon', desc:'A small arrow next to a link or button label slides to the right on hover, instead of sitting still.',
compose:() => `Please add a small arrow icon after the label on my "Learn More" / "View Menu" style buttons or links, and make it slide slightly to the right (a few pixels) on hover with a smooth transition, while the label text itself stays in place. Don't change the button's size, color, or text.`,
demo:(s) => { s.innerHTML = '<button class="el-demo-btn el-arrowbtn">View Menu <span class="el-arrow">&#8594;</span></button>'; } },
{ id:'liftshadow', cat:'Buttons & Links', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="12" height="12" rx="2"/><path d="M4 20h16" stroke-opacity=".4"/></svg>', title:'Lift & shadow on hover', desc:'Buttons rise slightly and gain a soft drop shadow on hover, then settle flat again on click.',
compose:() => `Please add a lift effect to my buttons: on hover, the button should rise slightly (a few pixels up) and gain a soft drop shadow beneath it; on click/press, it should return flat with a smaller, tighter shadow. Use a quick, smooth transition for both. Don't change button colors, sizes, or text -- only add this hover/press motion.`,
demo:(s) => { s.innerHTML = '<button class="el-demo-btn el-lift">Order Now</button>'; } },

{ id:'submitstates', cat:'Forms', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.2 2.2 4.8-4.8"/></svg>', title:'Form submit animation', desc:'Your contact/order form button shows a brief loading animation, then a checkmark, when someone submits it.',
compose:() => `Please add a submit animation to my contact/order form's submit button: when clicked, show three small bouncing dots in place of the button label while the form is submitting, then briefly show a checkmark icon to confirm it went through, then return to normal. Keep the button's size and color the same -- only change what's inside it during submit.`,
demo:(s) => {
s.innerHTML = '<button class="el-demo-btn">Submit</button>';
const btn = s.querySelector('button');
btn.dataset.label = 'Submit';
btn.addEventListener('click', () => {
if (btn.classList.contains('el-busy')) return;
btn.classList.add('el-busy');
setBtnState(btn, 'loading');
setTimeout(() => {
setBtnState(btn, 'success');
setTimeout(() => { setBtnState(btn, 'idle'); btn.classList.remove('el-busy'); }, 1200);
}, 900);
});
} },
{ id:'floatinglabel', cat:'Forms', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20l1-4L15 6l3 3L8 19z"/><path d="M13 8l3 3"/></svg>', title:'Floating form labels', desc:'Field labels start as placeholder text and smoothly float up above the field once someone starts typing.',
compose:() => `Please update the text input fields on my contact or catering request form so their labels start as placeholder text inside the field, then smoothly float up and shrink above the field once the visitor starts typing or the field has a value. Keep the same fields and validation, just change how the labels animate.`,
demo:(s) => { s.innerHTML = '<div class="el-float-wrap"><input type="text" placeholder=" "><label>Your name</label></div>'; } },
{ id:'quantitystepper', cat:'Forms', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h6"/><path d="M14 6h6"/><circle cx="11" cy="6" r="2"/><path d="M4 12h10"/><path d="M18 12h2"/><circle cx="16" cy="12" r="2"/><path d="M4 18h6"/><path d="M14 18h6"/><circle cx="11" cy="18" r="2"/></svg>', title:'Quantity stepper', desc:'A minus/plus stepper for any quantity field (like a catering headcount), with a little pop when the number changes.',
compose:() => `If my site has a quantity field anywhere (like a catering headcount or an order quantity), please style it as a stepper with minus and plus buttons on either side of the number, and make the number briefly pop/scale when it changes. Don't let the quantity go below 1.`,
demo:(s) => {
s.innerHTML = '<div class="el-stepper"><button class="minus">&minus;</button><span class="qty">1</span><button class="plus">+</button></div>';
let n = 1;
const qtyEl = s.querySelector('.qty');
function bump(){ qtyEl.textContent = n; qtyEl.classList.remove('el-pop'); void qtyEl.offsetWidth; qtyEl.classList.add('el-pop'); }
s.querySelector('.minus').addEventListener('click', () => { if (n > 1) { n--; bump(); } });
s.querySelector('.plus').addEventListener('click', () => { n++; bump(); });
} },
{ id:'copybtn', cat:'Forms', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="4" width="12" height="14" rx="2"/><path d="M4 8v10a2 2 0 0 0 2 2h8"/></svg>', title:'Copy-to-clipboard button', desc:'A button next to your phone number, address, or a promo code that copies it with one click and shows a quick checkmark.',
compose:() => `Please add a small "copy" button next to my phone number and address that copies the text to the clipboard when clicked, and briefly shows a checkmark icon confirming it copied, then reverts back to normal.`,
demo:(s) => {
s.innerHTML = '<button class="el-demo-btn">Copy</button>';
const btn = s.querySelector('button');
btn.addEventListener('click', () => {
if (btn.dataset.busy) return;
btn.dataset.busy = '1';
const old = btn.textContent;
btn.textContent = 'Copied ✓';
setTimeout(() => { btn.textContent = old; delete btn.dataset.busy; }, 1200);
});
} },

{ id:'accordion', cat:'Menu & Content', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16"/><path d="M4 13h16"/><path d="M9 18l3 3 3-3"/></svg>', title:'Smooth expand/collapse sections', desc:'For FAQ, allergen info, or catering details &mdash; click a heading to smoothly expand and reveal the content below it.',
compose:() => `Please make any FAQ, allergen info, or catering details section on my site expandable -- clicking the heading should smoothly expand to reveal the content below it (and collapse it back when clicked again), instead of showing everything at once.`,
demo:(s) => {
s.innerHTML = '<div class="el-acc"><div class="el-acc-head">Do you deliver? <span class="chev">&#9660;</span></div><div class="el-acc-body"><p>Yes, within 5 miles.</p></div></div>';
const head = s.querySelector('.el-acc-head'), body = s.querySelector('.el-acc-body');
head.addEventListener('click', () => {
const open = head.classList.toggle('open');
body.style.maxHeight = open ? body.scrollHeight + 'px' : '0px';
});
} },
{ id:'cardresize', cat:'Menu & Content', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9V4h5"/><path d="M4 4l6 6"/><path d="M20 9V4h-5"/><path d="M20 4l-6 6"/><path d="M4 15v5h5"/><path d="M4 20l6-6"/><path d="M20 15v5h-5"/><path d="M20 20l-6-6"/></svg>', title:'Expandable menu items', desc:'Click a menu item card to smoothly grow it and reveal more detail, like a longer description.',
compose:() => `Please make my menu item cards expandable: clicking a menu item should smoothly grow the card to reveal more detail (like a longer description or ingredients, if I add one), and clicking again should smoothly collapse it back down. Keep the current menu layout and styling otherwise unchanged.`,
demo:(s) => {
s.innerHTML = '<div class="el-mcard"><div class="el-mcard-top"><span>Margherita</span><span>$18</span></div><div class="el-mcard-desc"><p>San Marzano tomatoes, fresh mozzarella, basil.</p></div></div>';
const card = s.querySelector('.el-mcard'), desc = s.querySelector('.el-mcard-desc');
card.addEventListener('click', () => {
const open = desc.style.maxHeight && desc.style.maxHeight !== '0px';
desc.style.maxHeight = open ? '0px' : desc.scrollHeight + 'px';
});
} },
{ id:'choicechips', cat:'Menu & Content', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16l-6 8v6l-4-2v-4z"/></svg>', title:'Menu filter chips', desc:'Clickable filter chips above your menu (like Vegetarian, Gluten-Free, Spicy) that highlight when selected.',
compose:() => `Please add filter chips above my menu (things like "Vegetarian", "Gluten-Free", "Spicy" -- use whatever tags actually make sense for my menu items) that visitors can click to filter which items are shown. Selected chips should pop slightly and highlight in my accent color. Showing all items should be the default with no filter selected.`,
demo:(s) => {
s.innerHTML = '<div><span class="el-chip">Veg</span><span class="el-chip">GF</span><span class="el-chip">Spicy</span></div>';
s.querySelectorAll('.el-chip').forEach(c => c.addEventListener('click', () => c.classList.toggle('active')));
} },
{ id:'tabglide', cat:'Menu & Content', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="10" height="6" rx="2"/></svg>', title:'Gliding menu tabs', desc:'If your menu is split into categories (like Appetizers, Entrees, Drinks), the highlighted tab glides smoothly between them instead of just switching.',
compose:() => `If my menu page has category tabs/sections (like Appetizers, Entrees, Drinks), please add a smooth gliding highlight behind the active tab that animates to the new tab's position and width when someone switches categories, instead of the highlight just appearing instantly. Use this easing curve: cubic-bezier(0.34, 1.56, 0.64, 1).`,
demo:(s) => {
s.innerHTML = '<div class="el-tabs"><div class="el-tab-pill"></div><button class="el-tab-btn active">Apps</button><button class="el-tab-btn">Entrees</button><button class="el-tab-btn">Drinks</button></div>';
const pill = s.querySelector('.el-tab-pill');
const btns = s.querySelectorAll('.el-tab-btn');
function place(){ const a = s.querySelector('.el-tab-btn.active'); pill.style.width = a.offsetWidth + 'px'; pill.style.transform = 'translateX(' + a.offsetLeft + 'px)'; }
btns.forEach(b => b.addEventListener('click', () => { btns.forEach(x => x.classList.remove('active')); b.classList.add('active'); place(); }));
setTimeout(place, 0);
} },
{ id:'skeleton', cat:'Menu & Content', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="M21 15l-5-5-4 4-3-3-5 5"/></svg>', title:'Soft image loading', desc:'Photos show a gentle shimmering placeholder while they load instead of a blank gap or a flash.',
compose:() => `Please add a soft shimmering placeholder (skeleton loading effect) that shows in place of my site's photos while they're loading, so visitors see a gentle animated placeholder instead of a blank gap or a flash of a broken image icon.`,
demo:(s) => { s.innerHTML = '<div style="width:100%"><div class="el-skel"></div><div class="el-skel"></div></div>'; } },
{ id:'starrating', cat:'Menu & Content', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.6 5.6 6.1.6-4.6 4 1.3 6-5.4-3.2L6.6 19.2l1.3-6-4.6-4 6.1-.6z"/></svg>', title:'Star rating display', desc:'If you show customer testimonials or reviews, the stars pop in with a little bounce when scrolled into view.',
compose:() => `If my site has customer testimonials or reviews, please display a 5-star rating for each one, where the stars pop in with a little bounce when they scroll into view. Use my accent color for filled stars.`,
demo:(s) => {
s.innerHTML = '<div class="el-stars">' + [1,2,3,4,5].map(i => '<span class="el-star" data-v="'+i+'">&#9733;</span>').join('') + '</div>';
const stars = s.querySelectorAll('.el-star');
let locked = 0;
function paint(v){ stars.forEach(st => st.classList.toggle('filled', +st.dataset.v <= v)); }
stars.forEach(st => {
st.addEventListener('mouseenter', () => paint(+st.dataset.v));
st.addEventListener('click', () => { locked = +st.dataset.v; st.classList.add('pop'); setTimeout(() => st.classList.remove('pop'), 300); });
});
s.querySelector('.el-stars').addEventListener('mouseleave', () => paint(locked));
} },

{ id:'toast', cat:'Notifications & Badges', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8.5 8.5 0 0 1-12.3 7.6L4 21l1.4-4.7A8.5 8.5 0 1 1 21 12z"/></svg>', title:'Confirmation toast', desc:'A small message slides up from the bottom confirming an action, like "Message sent!" after someone submits a form.',
compose:() => `Please add a small confirmation toast/banner that slides up from the bottom of the screen after someone successfully submits my contact or order form, overshooting slightly as it settles into place, saying something like "Thanks, we got it!" and then fades away automatically after a few seconds. It shouldn't block anything else on the page.`,
demo:(s) => {
s.style.position = 'relative';
s.innerHTML = '<button class="el-demo-btn">Trigger</button><div class="el-toast-demo">Thanks, we got it!</div>';
const toast = s.querySelector('.el-toast-demo');
s.querySelector('button').addEventListener('click', () => {
toast.classList.add('show');
setTimeout(() => toast.classList.remove('show'), 1800);
});
} },
{ id:'bannerslide', cat:'Notifications & Badges', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10v4a1 1 0 0 0 1 1h2l9 5V4L6 9H4a1 1 0 0 0-1 1z"/><path d="M17 9a3 3 0 0 1 0 6"/></svg>', title:'Announcement banner', desc:'A dismissible banner drops down from the top of the site for things like a holiday catering announcement.',
compose:() => `Please add a dismissible announcement banner that drops down from the top of my site with a slight bounce, showing this message: [YOUR ANNOUNCEMENT TEXT HERE -- e.g. "Now taking holiday catering orders"]. Include a small close button. Use my accent color for the banner background.`,
demo:(s) => {
s.style.position = 'relative';
s.innerHTML = '<button class="el-demo-btn">Trigger</button><div class="el-banner-demo">Now taking holiday orders!</div>';
const banner = s.querySelector('.el-banner-demo');
s.querySelector('button').addEventListener('click', () => {
banner.classList.add('show');
setTimeout(() => banner.classList.remove('show'), 2200);
});
} },
{ id:'pulsebadge', cat:'Notifications & Badges', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9a6 6 0 0 1 12 0c0 5 2 6 2 6H4s2-1 2-6"/><path d="M10 20a2 2 0 0 0 4 0"/></svg>', title:'"New" badge pulse', desc:'A small badge with gently expanding rings to flag a new menu item or limited-time section.',
compose:() => `Please add a small pulsing "New" badge (a colored dot that gently emits expanding rings) next to this menu item or section: [NAME THE ITEM OR SECTION HERE]. Use my accent color for the badge.`,
demo:(s) => { s.innerHTML = '<span class="el-badge-dot"></span>'; } },
{ id:'countdown', cat:'Notifications & Badges', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>', title:'Limited-time countdown', desc:'A circular ring that visually drains as it counts down to the end of an offer.',
compose:() => `Please add a small countdown timer using a circular ring that visually drains as time passes, counting down to: [DATE/TIME OR OFFER END -- e.g. "this Sunday at 9pm"]. Show it near: [WHERE ON THE SITE -- e.g. the specials section]. Use my accent color for the ring.`,
demo:(s) => { s.innerHTML = '<svg class="el-ring" width="46" height="46" viewBox="0 0 40 40"><circle class="track" cx="20" cy="20" r="18"></circle><circle class="fill" cx="20" cy="20" r="18"></circle></svg>'; } },

{ id:'oddcountup', cat:'Navigation & Hero', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M17 7h4v4"/></svg>', title:'Animated trust numbers', desc:'The numbers in your trust/stats section count up from 0 when scrolled into view, instead of just appearing.',
compose:() => `Please animate the numbers in my trust/stats section (things like years in business, items served, or similar) so each number counts up from 0 to its real value when a visitor scrolls it into view, instead of just appearing. Keep the actual numbers and labels the same, only add the count-up animation.`,
demo:(s) => {
s.innerHTML = '<button class="el-demo-btn" style="margin-bottom:6px">Trigger</button><div class="el-countup">0</div>';
const numEl = s.querySelector('.el-countup');
s.querySelector('button').addEventListener('click', () => {
let n = 0; const target = 500;
const t = setInterval(() => { n += 25; if (n >= target) { n = target; clearInterval(t); } numEl.textContent = n + '+'; }, 30);
});
} },
{ id:'staggerreveal', cat:'Navigation & Hero', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v4"/><path d="M12 17v4"/><path d="M3 12h4"/><path d="M17 12h4"/><path d="M6 6l2.5 2.5"/><path d="M15.5 15.5L18 18"/><path d="M18 6l-2.5 2.5"/><path d="M8.5 15.5L6 18"/></svg>', title:'Scroll-in reveal', desc:'Menu and feature cards fade in and rise up one after another as a visitor scrolls down the page.',
compose:() => `Please make the cards/items in my menu and feature sections fade in and rise up slightly, one after another in a quick stagger, as a visitor scrolls them into view, instead of all appearing at once. Keep the layout and content exactly the same, only add this scroll-in animation.`,
demo:(s) => {
s.innerHTML = '<button class="el-demo-btn" style="margin-bottom:8px">Replay</button><div class="el-stagger"><span></span><span></span><span></span><span></span></div>';
const spans = s.querySelectorAll('.el-stagger span');
function play(){ spans.forEach((sp,i) => { sp.classList.remove('show'); void sp.offsetWidth; setTimeout(() => sp.classList.add('show'), i*90); }); }
s.querySelector('button').addEventListener('click', play);
setTimeout(play, 200);
} },
{ id:'typewriter', cat:'Navigation & Hero', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v16"/><path d="M9 4h1"/><path d="M14 4h1"/><path d="M9 20h1"/><path d="M14 20h1"/></svg>', title:'Rotating hero tagline', desc:'Your hero subtitle types out a few different short phrases in sequence instead of showing one static line.',
compose:() => `Please make my hero section's subtitle cycle through a few short phrases with a typewriter effect (typing each one out, pausing, then deleting it before typing the next) instead of showing one static line. Use these phrases: [LIST 2-4 SHORT PHRASES HERE -- e.g. "Fresh daily." / "Family owned." / "Est. 2015."].`,
demo:(s) => {
s.innerHTML = '<span class="el-type"></span>';
const el = s.querySelector('.el-type');
const words = ['Fresh daily.', 'Family owned.', 'Est. 2015.'];
let wi = 0, ci = 0, deleting = false;
function tick(){
const w = words[wi];
el.textContent = deleting ? w.slice(0, ci--) : w.slice(0, ci++);
let delay = deleting ? 40 : 80;
if (!deleting && ci > w.length) { deleting = true; delay = 900; }
else if (deleting && ci < 0) { deleting = false; wi = (wi+1) % words.length; ci = 0; delay = 300; }
setTimeout(tick, delay);
}
tick();
} },
{ id:'iconmorph', cat:'Navigation & Hero', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/></svg>', title:'Mobile menu icon morph', desc:'The mobile nav icon smoothly morphs from a hamburger into an X when the menu opens, instead of swapping instantly.',
compose:() => `Please make my mobile navigation menu icon smoothly morph from a hamburger icon into an X (and back) when the mobile menu is opened and closed, instead of just swapping instantly.`,
demo:(s) => {
s.innerHTML = '<div class="el-burger"><span></span><span></span><span></span></div>';
s.querySelector('.el-burger').addEventListener('click', function(){ this.classList.toggle('open'); });
} },
{ id:'speeddial', cat:'Navigation & Hero', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v8"/><path d="M8 12h8"/></svg>', title:'Floating quick-action button', desc:'A round floating button on mobile that fans out into Call, Directions, and Order buttons when tapped.',
compose:() => `Please add a floating round button in the bottom corner of the screen on mobile that, when tapped, fans out into a few small quick-action buttons: Call, Get Directions, and Order Online (use whichever of these actually apply to my site). Each mini-button should pop out with a slight stagger.`,
demo:(s) => {
s.innerHTML = '<div class="el-fab-wrap"><div class="el-fab-mini">&#9742;</div><div class="el-fab-mini">&#128205;</div><div class="el-fab-mini">&#127860;</div><button class="el-fab">+</button></div>';
const minis = s.querySelectorAll('.el-fab-mini');
let open = false;
s.querySelector('.el-fab').addEventListener('click', () => {
open = !open;
minis.forEach((m,i) => setTimeout(() => m.classList.toggle('show', open), i*60));
});
} },
{ id:'tooltip', cat:'Navigation & Hero', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 .8-1 1.7"/><path d="M12 17h.01"/></svg>', title:'Delayed helpful tooltip', desc:'A small hover tooltip that only appears after a brief pause, so it doesn\\'t flash for every passing cursor.',
compose:() => `Please add small hover tooltips to: [NAME WHAT NEEDS EXPLAINING -- e.g. allergen icons on the menu, or a special term]. They should only appear after hovering for about half a second (not instantly), and disappear right away when the visitor moves away.`,
demo:(s) => {
s.innerHTML = '<span class="el-tip-chip">Hover me<span class="el-tip-bubble">Contains gluten</span></span>';
const chip = s.querySelector('.el-tip-chip'), bubble = s.querySelector('.el-tip-bubble');
let timer;
chip.addEventListener('mouseenter', () => { timer = setTimeout(() => bubble.classList.add('show'), 500); });
chip.addEventListener('mouseleave', () => { clearTimeout(timer); bubble.classList.remove('show'); });
} },
{ id:'marquee', cat:'Navigation & Hero', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h18"/><path d="M7 8l-4 4 4 4"/><path d="M17 8l4 4-4 4"/></svg>', title:'Scrolling highlights marquee', desc:'A horizontally scrolling strip -- for customer quotes, press mentions, or menu highlights -- that pauses on hover.',
compose:() => `Please add a horizontally scrolling marquee strip (things like customer quotes, press mentions, or menu highlights -- tell me which) that scrolls continuously and smoothly pauses when a visitor hovers over it.`,
demo:(s) => { s.innerHTML = '<div class="el-marquee-wrap"><div class="el-marquee-track">"Best pizza in town!" &nbsp;&#8226;&nbsp; Featured on local news &nbsp;&#8226;&nbsp; "A true neighborhood gem" &nbsp;&#8226;&nbsp; "Best pizza in town!" &nbsp;&#8226;&nbsp; Featured on local news &nbsp;&#8226;&nbsp; "A true neighborhood gem"</div></div>'; } },

{ id:'neonflicker', cat:'Hero & Signage', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a6 6 0 0 0-4 10.5c.7.7 1 1.3 1 2.5h6c0-1.2.3-1.8 1-2.5A6 6 0 0 0 12 2z"/></svg>', title:'Neon sign flicker', desc:'Your hero heading or a key word flickers and glows like a buzzing neon sign, in your accent color.',
compose:() => `Please make my hero heading (or a specific banner word/phrase I'll point out) flicker like a neon sign: use a CSS keyframe animation with a few quick, irregular opacity dips rather than one smooth steady pulse, plus a soft multi-layer text-shadow glow in my accent color. Keep the text content, size, and font exactly as they are now -- only add the neon flicker and glow.`,
demo:(s) => { s.innerHTML = '<span class="el-neon">OPEN</span>'; } },
{ id:'meshbg', cat:'Hero & Signage', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 18a4 4 0 0 1 0-8 5 5 0 0 1 9.6-1.5A4.5 4.5 0 0 1 17 18z"/></svg>', title:'Soft mesh background glow', desc:'A few large, blurred color blobs drift slowly behind your hero section for a soft, modern backdrop &mdash; gentle enough that text stays easy to read.',
compose:() => `Please add a soft, slow-drifting mesh-gradient glow behind my hero section: a few large, heavily blurred, softly-colored blobs (using my primary and accent colors at low opacity) positioned behind the hero text and buttons, drifting very slowly and continuously. Keep it subtle enough that the hero heading and text stay fully readable -- this sits behind the existing hero content, don't add any new foreground elements.`,
demo:(s) => { s.innerHTML = '<div class="el-mesh"><span></span><span></span><span></span></div>'; } },
{ id:'gradientstyle', cat:'Hero & Signage', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a9 9 0 1 0 0 18c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.4-.3-.4-.5-.8-.5-1.3 0-1 .8-1.8 1.8-1.8H17a4 4 0 0 0 4-4c0-4.4-4-7.5-9-7.5z"/><circle cx="7.5" cy="10.5" r="1"/><circle cx="10.5" cy="7.5" r="1"/><circle cx="14.5" cy="7.5" r="1"/><circle cx="17" cy="10.5" r="1"/></svg>', title:'Animated gradient hero styles', desc:'Preview a few different animated gradient looks for your hero background, then request the one you like &mdash; all built from your own brand colors.',
compose:() => { const d = { flow:"a smoothly flowing, slowly shifting linear gradient (the color positions drift back and forth over several seconds)", radial:"a radial swirl -- an off-center radial gradient glow, like a soft spotlight", diagonal:"a clean diagonal gradient sweep from one corner to the other", conic:"a conic gradient that wraps around like a color wheel, for a bolder, more graphic look" }; return `Please update my hero section's background to use ${d[window.__elGradChosen || 'flow']}, built from my existing primary and accent brand colors (don't introduce new colors). Keep the hero text, buttons, and layout exactly as they are -- only change the background treatment.`; },
demo:(s) => {
s.innerHTML = '<div class="el-grad-wrap"><div class="el-grad-preview" data-style="flow"></div><div class="el-grad-swatches">' +
['flow','radial','diagonal','conic'].map((st,i) => `<button class="el-grad-sw${i===0?' active':''}" data-style="${st}" title="${st}"></button>`).join('') +
'</div></div>';
const preview = s.querySelector('.el-grad-preview');
const swatches = s.querySelectorAll('.el-grad-sw');
window.__elGradChosen = 'flow';
swatches.forEach(sw => sw.addEventListener('click', () => {
swatches.forEach(x => x.classList.remove('active'));
sw.classList.add('active');
window.__elGradChosen = sw.dataset.style;
preview.setAttribute('data-style', sw.dataset.style);
}));
} },
{ id:'photoscatter', cat:'Galleries', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="13" height="13" rx="2" transform="rotate(-6 12 12)"/><rect x="5" y="5" width="13" height="13" rx="2"/></svg>', title:'Scattered photo gallery', desc:'Photos fan out in a loose, slightly-rotated stack instead of a strict grid &mdash; each one lifts and straightens on hover.',
compose:() => `Please restyle my photo gallery (or food/work photos section) so the images are laid out in a loose, slightly overlapping, randomly-rotated "scattered polaroid" arrangement instead of a strict grid. On hover, the hovered photo should lift slightly, straighten out (rotate to 0deg), and come to the front. Use my existing photos -- don't need new images, just restyle the layout.`,
demo:(s) => { s.innerHTML = '<div class="el-scatter">' + [0,1,2].map(i=>`<div class="el-scatter-card c${i}"></div>`).join('') + '</div>'; } },
{ id:'imageorbit', cat:'Galleries', icon:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1.5"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(35 12 12)"/><circle cx="19.5" cy="9.5" r="1.5"/></svg>', title:'Orbiting photo gallery', desc:'Photos slowly circle around a center point &mdash; great for team photos or a rotating showcase of dishes &mdash; pausing on hover.',
compose:() => `Please add a circular "orbiting" photo gallery: arrange a set of photos (team photos, dishes, or work samples -- tell the assistant which) in a circle that slowly auto-rotates around a center point, and pause the rotation when a visitor hovers over the gallery. Keep photos evenly spaced around the circle.`,
demo:(s) => { s.innerHTML = '<div class="el-orbit"><div class="el-orbit-ring">' + [0,1,2,3].map(i=>`<div class="el-orbit-dot d${i}"></div>`).join('') + '</div></div>'; } },
];
const elementsGrid = document.getElementById('elementsGrid');
let lastElCat = '';
ELEMENTS.forEach(el => {
if (el.cat !== lastElCat) {
lastElCat = el.cat;
const head = document.createElement('div');
head.className = 'elements-cat';
head.textContent = el.cat;
elementsGrid.appendChild(head);
}
const card = document.createElement('div');
card.className = 'element-card';
const stage = document.createElement('div');
stage.className = 'el-stage';
card.appendChild(stage);
const body = document.createElement('div');
body.className = 'el-body';
body.innerHTML = `<div class="el-body-head"><span class="el-icon">${el.icon}</span><h3>${el.title}</h3></div><p>${el.desc}</p>`;
const btn = document.createElement('button');
btn.className = 'ui-btn small primary';
btn.type = 'button';
btn.textContent = 'Add to my site';
btn.addEventListener('click', () => {
switchTab('content');
codeBox.value = el.compose();
chatInput.focus();
});
body.appendChild(btn);
card.appendChild(body);
elementsGrid.appendChild(card);
if (el.demo) { try { el.demo(stage); } catch(e) {} }
});

const TIPS = [
'Make the hero background a little darker',
'Add a new item to the @@FAVORITES_TITLE@@ section',
'Change our Sunday hours',
'Swap the hero photo for the one I just uploaded',
'Update the phone number',
];
const tipsBody = document.getElementById('tipsBody');
TIPS.forEach(tip => {
const chip = document.createElement('div');
chip.className = 'tip-chip';
chip.textContent = tip;
chip.addEventListener('click', () => { chatInput.value = tip; chatInput.focus(); closeAllPopovers(); });
tipsBody.appendChild(chip);
});

const LOG_KEY = '@@LOG_KEY@@';
const activityList = document.getElementById('activityList');
const activityEmpty = document.getElementById('activityEmpty');
const statusPill = document.getElementById('statusPill');
const statusPillText = document.getElementById('statusPillText');

function loadLog(){
try { return JSON.parse(localStorage.getItem(LOG_KEY)) || []; } catch(e){ return []; }
}
function saveLog(list){
try { localStorage.setItem(LOG_KEY, JSON.stringify(list)); } catch(e){}
}
function relTime(ts){
const diff = Date.now() - ts;
const min = Math.floor(diff / 60000);
if (min < 1) return 'just now';
if (min < 60) return min + ' min ago';
const hr = Math.floor(min / 60);
if (hr < 24) return hr + ' hr ago';
const days = Math.floor(hr / 24);
if (days < 7) return days + ' day' + (days === 1 ? '' : 's') + ' ago';
return new Date(ts).toLocaleDateString();
}
function logActivity(request, status, detail){
const list = loadLog();
list.unshift({ id: 'a' + Date.now(), ts: Date.now(), request, status, detail });
saveLog(list.slice(0, 100));
renderActivity();
updateStatusPill();
}
function renderActivity(){
const list = loadLog();
activityList.innerHTML = '';
activityEmpty.style.display = list.length ? 'none' : 'block';
list.forEach(entry => {
const item = document.createElement('div');
item.className = 'activity-item';
const dotClass = entry.status === 'ok' ? 'ok' : entry.status === 'err' ? 'err' : '';
item.innerHTML = `
<div class="activity-top">
<div class="left"><span class="activity-dot ${dotClass}"></span><span class="activity-time">${relTime(entry.ts)}</span></div>
</div>
<div class="activity-request">${escapeHtml(entry.request)}</div>
<div class="activity-detail">${escapeHtml(entry.detail || '')}</div>
`;
if (entry.status === 'ok') {
const actions = document.createElement('div');
actions.className = 'activity-actions';
const undoBtn = document.createElement('button');
undoBtn.className = 'ui-btn small';
undoBtn.type = 'button';
undoBtn.textContent = 'Ask AI to undo this';
undoBtn.addEventListener('click', () => {
switchTab('content');
chatInput.value = `Please undo this change: "${entry.request}"`;
chatInput.focus();
});
actions.appendChild(undoBtn);
item.appendChild(actions);
}
activityList.appendChild(item);
});
}
function updateStatusPill(){
const list = loadLog();
if (!list.length) {
statusPill.className = 'status-pill';
statusPillText.textContent = 'No AI edits yet';
return;
}
const last = list[0];
statusPill.className = 'status-pill pop ' + (last.status === 'ok' ? 'ok' : last.status === 'err' ? 'err' : '');
statusPillText.textContent = (last.status === 'ok' ? 'Last edit applied ' : 'Last edit failed ') + relTime(last.ts);
setTimeout(() => statusPill.classList.remove('pop'), 400);
}
function escapeHtml(s){
const d = document.createElement('div');
d.textContent = s;
return d.innerHTML;
}
document.getElementById('clearLogBtn').addEventListener('click', () => {
if (!confirm('Clear the activity log? This only clears what is shown here, it does not undo any site changes.')) return;
saveLog([]);
renderActivity();
updateStatusPill();
});
renderActivity();
updateStatusPill();

const FONTS = [
{n:"Bevan", c:"display"}, {n:"Playfair Display", c:"serif"}, {n:"Merriweather", c:"serif"},
{n:"Lora", c:"serif"}, {n:"Georgia", c:"serif", web:true}, {n:"Cormorant Garamond", c:"serif"},
{n:"Libre Baskerville", c:"serif"}, {n:"Crimson Text", c:"serif"}, {n:"Bitter", c:"serif"},
{n:"PT Serif", c:"serif"}, {n:"Domine", c:"serif"}, {n:"EB Garamond", c:"serif"},
{n:"Cormorant", c:"serif"}, {n:"Vollkorn", c:"serif"}, {n:"Zilla Slab", c:"serif"},
{n:"Noto Serif", c:"serif"}, {n:"Frank Ruhl Libre", c:"serif"},
{n:"Poppins", c:"sans-serif"}, {n:"Montserrat", c:"sans-serif"}, {n:"Raleway", c:"sans-serif"},
{n:"Inter", c:"sans-serif"}, {n:"Nunito", c:"sans-serif"}, {n:"Work Sans", c:"sans-serif"},
{n:"Open Sans", c:"sans-serif"}, {n:"Roboto", c:"sans-serif"}, {n:"Lato", c:"sans-serif"},
{n:"Rubik", c:"sans-serif"}, {n:"DM Sans", c:"sans-serif"}, {n:"Karla", c:"sans-serif"},
{n:"Manrope", c:"sans-serif"}, {n:"Sora", c:"sans-serif"}, {n:"Josefin Sans", c:"sans-serif"},
{n:"Oswald", c:"sans-serif"}, {n:"Barlow", c:"sans-serif"}, {n:"Mulish", c:"sans-serif"},
{n:"Outfit", c:"sans-serif"}, {n:"Plus Jakarta Sans", c:"sans-serif"}, {n:"Urbanist", c:"sans-serif"},
{n:"Figtree", c:"sans-serif"}, {n:"Public Sans", c:"sans-serif"}, {n:"Epilogue", c:"sans-serif"},
{n:"Be Vietnam Pro", c:"sans-serif"}, {n:"Barlow Condensed", c:"sans-serif"}, {n:"Archivo Narrow", c:"sans-serif"},
{n:"Bebas Neue", c:"display"}, {n:"Anton", c:"display"}, {n:"Alfa Slab One", c:"display"},
{n:"Fredoka", c:"display"}, {n:"Titan One", c:"display"}, {n:"Lilita One", c:"display"},
{n:"Caprasimo", c:"display"}, {n:"Ultra", c:"display"}, {n:"Chonburi", c:"display"},
{n:"Tilt Warp", c:"display"}, {n:"Righteous", c:"display"}, {n:"Passion One", c:"display"},
{n:"Abril Fatface", c:"display"}, {n:"Pathway Gothic One", c:"display"}, {n:"Staatliches", c:"display"},
{n:"Archivo Black", c:"display"}, {n:"Baloo 2", c:"display"}, {n:"Kanit", c:"display"},
{n:"Bungee", c:"display"}, {n:"Luckiest Guy", c:"display"}, {n:"Bungee Shade", c:"display"},
{n:"Bowlby One", c:"display"}, {n:"Monoton", c:"display"}, {n:"Fjalla One", c:"display"},
{n:"Big Shoulders Display", c:"display"},
{n:"Fraunces", c:"serif"}, {n:"Space Grotesk", c:"sans-serif"},
{n:"Pacifico", c:"script"}, {n:"Caveat", c:"script"}, {n:"Dancing Script", c:"script"},
{n:"Great Vibes", c:"script"}, {n:"Satisfy", c:"script"}, {n:"Sacramento", c:"script"},
{n:"Kalam", c:"script"}, {n:"Shadows Into Light", c:"script"}, {n:"Parisienne", c:"script"},
{n:"Allura", c:"script"}, {n:"Alex Brush", c:"script"}, {n:"Yellowtail", c:"script"},
{n:"Courgette", c:"script"}, {n:"Lobster", c:"script"},
{n:"Cinzel", c:"serif"}, {n:"Marcellus", c:"serif"}, {n:"Spectral", c:"serif"},
{n:"Source Serif 4", c:"serif"}, {n:"IBM Plex Sans", c:"sans-serif"},
{n:"IBM Plex Mono", c:"monospace"}, {n:"JetBrains Mono", c:"monospace"}, {n:"Roboto Mono", c:"monospace"},
{n:"Space Mono", c:"monospace"}, {n:"Fira Code", c:"monospace"}, {n:"Source Code Pro", c:"monospace"},
];

const DEFAULTS = @@DEFAULTS_JSON@@;
const COLOR_META = [
["primary","Primary","Hero &amp; CTA gradient start"],
["primary_bright","Primary bright","Gradient mid-stop"],
["primary_deep","Primary deep","Hero gradient outer edge"],
["glow","Glow","Highlight accent"],
["accent","Accent","Buttons, tags, prices, badges"],
["accent_deep","Accent (hover)","Button hover state"],
["on_accent","Text on accent","Text sitting on accent buttons"],
["cream","Text","Main body/heading text color"],
["cream_muted","Muted text","Secondary/muted text"],
["bg_deep","Background","Page background"],
["panel","Panel","Card &amp; nav background"],
["ink","Ink","Footer background"],
];
let state = JSON.parse(JSON.stringify(DEFAULTS));
const STORAGE_KEY = "@@STORAGE_KEY@@";
function loadState(){ try{ const s = localStorage.getItem(STORAGE_KEY); if (s) state = JSON.parse(s); }catch(e){} }
function saveState(){ try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }catch(e){} }
function loadGoogleFont(name){
if (!name) return;
const id = "gf-" + name.replace(/\s+/g,'-');
if (document.getElementById(id)) return;
const link = document.createElement('link');
link.id = id; link.rel = 'stylesheet';
link.href = 'https://fonts.googleapis.com/css2?family=' + encodeURIComponent(name).replace(/%20/g,'+') + ':wght@400;700&display=swap';
document.head.appendChild(link);
}
function renderFontList(container, searchVal, currentName, onPick){
const q = (searchVal || "").toLowerCase();
container.innerHTML = "";
const filtered = FONTS.filter(f => f.n.toLowerCase().includes(q));
filtered.forEach(f => {
const div = document.createElement('div');
div.className = 'font-item' + (f.n === currentName ? ' active' : '');
div.innerHTML = f.n + '<span class="cat">' + f.c + '</span>';
div.style.fontFamily = "'" + f.n + "'," + (f.c === 'serif' ? 'Georgia,serif' : f.c === 'monospace' ? 'monospace' : 'sans-serif');
div.addEventListener('click', () => onPick(f.n));
container.appendChild(div);
});
if (filtered.length === 0) container.innerHTML = '<div class="font-item" style="color:var(--ui-text-muted);cursor:default">No fonts match</div>';
}
function applyPreview(){
const pv = document.getElementById('pv');
const c = state.colors;
pv.style.setProperty('--p-primary', c.primary);
pv.style.setProperty('--p-primary-bright', c.primary_bright);
pv.style.setProperty('--p-primary-deep', c.primary_deep);
pv.style.setProperty('--p-glow', c.glow);
pv.style.setProperty('--p-accent', c.accent);
pv.style.setProperty('--p-accent-deep', c.accent_deep);
pv.style.setProperty('--p-on-accent', c.on_accent);
pv.style.setProperty('--p-cream', c.cream);
pv.style.setProperty('--p-cream-muted', c.cream_muted);
pv.style.setProperty('--p-bg-deep', c.bg_deep);
pv.style.setProperty('--p-panel', c.panel);
pv.style.setProperty('--p-ink', c.ink);
pv.style.setProperty('--p-font-head', "'" + state.fontHead + "',Georgia,serif");
pv.style.setProperty('--p-font-body', "'" + state.fontBody + "',system-ui,Arial,sans-serif");
}
function updateFontCurrent(){
const hc = document.getElementById('headCurrent');
hc.style.fontFamily = "'" + state.fontHead + "',Georgia,serif";
hc.firstChild.textContent = state.fontHead;
const bc = document.getElementById('bodyCurrent');
bc.style.fontFamily = "'" + state.fontBody + "',system-ui,sans-serif";
bc.firstChild.textContent = state.fontBody;
}
function renderColorRows(){
const wrap = document.getElementById('colorRows');
wrap.innerHTML = "";
COLOR_META.forEach(([key, label, desc]) => {
const row = document.createElement('div');
row.className = 'color-row';
row.innerHTML = `<input type="color" data-key="${key}" value="${state.colors[key]}">
<div class="cinfo"><div class="cname">${label}</div><div class="cdesc">${desc}</div></div>
<input type="text" data-key="${key}" value="${state.colors[key]}">`;
wrap.appendChild(row);
});
wrap.querySelectorAll('input[type=color]').forEach(inp => {
inp.addEventListener('input', e => {
const key = e.target.dataset.key;
state.colors[key] = e.target.value;
wrap.querySelector('input[type=text][data-key="' + key + '"]').value = e.target.value;
const row = e.target.closest('.color-row');
row.classList.remove('pop'); void row.offsetWidth; row.classList.add('pop');
onChange();
});
});
wrap.querySelectorAll('input[type=text]').forEach(inp => {
inp.addEventListener('change', e => {
let v = e.target.value.trim();
if (!v.startsWith('#')) v = '#' + v;
if (!/^#[0-9a-fA-F]{6}$/.test(v)) { e.target.value = state.colors[e.target.dataset.key]; return; }
const key = e.target.dataset.key;
state.colors[key] = v;
wrap.querySelector('input[type=color][data-key="' + key + '"]').value = v;
const row = e.target.closest('.color-row');
row.classList.remove('pop'); void row.offsetWidth; row.classList.add('pop');
onChange();
});
});
}
// Builds a plain-English description of the staged style (colors + fonts) --
// this is what actually gets sent to the AI Update Pipeline when the owner
// hits Publish, and also what's shown in the on-screen summary. No code or
// brand_config.py internals are ever shown to the client; the assistant
// (or George, if it gets flagged for review) is the one who translates this
// into the actual file edit.
let styleRequestText = '';
function buildOutput(){
const c = state.colors;
const headFamily = state.fontHead, bodyFamily = state.fontBody;
const isGoogle = (name) => FONTS.some(f => f.n === name && !f.web);
const families = [];
if (isGoogle(headFamily)) families.push(headFamily + ':wght@400;700');
if (isGoogle(bodyFamily) && bodyFamily !== headFamily) families.push(bodyFamily + ':wght@400;700');
const href = families.length ? "https://fonts.googleapis.com/css2?" + families.map(f => "family=" + encodeURIComponent(f).replace(/%20/g,'+')).join('&') + "&display=swap" : "";
const lines = [];
lines.push('Heading font: ' + headFamily);
lines.push('Body font: ' + bodyFamily);
COLOR_META.forEach(([key, label]) => { lines.push(label + ': ' + c[key]); });
if (href) lines.push('Google Fonts URL: ' + href);
styleRequestText = lines.join('\\n');
document.getElementById('styleSummary').textContent = styleRequestText;
}
function onChange(){ applyPreview(); updateFontCurrent(); saveState(); buildOutput(); }
function initStyleEditor(){
loadState();
loadGoogleFont(state.fontHead);
if (FONTS.some(f => f.n === state.fontBody && !f.web)) loadGoogleFont(state.fontBody);
["Poppins","Playfair Display","Montserrat","Bebas Neue","Pacifico","Oswald"].forEach(loadGoogleFont);
const headSearch = document.getElementById('headSearch'), bodySearch = document.getElementById('bodySearch');
const headList = document.getElementById('headList'), bodyList = document.getElementById('bodyList');
function refreshHeadList(){ renderFontList(headList, headSearch.value, state.fontHead, (name) => { state.fontHead = name; loadGoogleFont(name); refreshHeadList(); onChange(); }); }
function refreshBodyList(){ renderFontList(bodyList, bodySearch.value, state.fontBody, (name) => { state.fontBody = name; loadGoogleFont(name); refreshBodyList(); onChange(); }); }
headSearch.addEventListener('input', refreshHeadList);
bodySearch.addEventListener('input', refreshBodyList);
refreshHeadList(); refreshBodyList();
renderColorRows(); applyPreview(); updateFontCurrent(); buildOutput();
document.getElementById('resetBtn').addEventListener('click', () => {
state = JSON.parse(JSON.stringify(DEFAULTS));
loadGoogleFont(state.fontHead);
refreshHeadList(); refreshBodyList(); renderColorRows(); onChange();
});
document.getElementById('publishStyleBtn').addEventListener('click', () => {
switchTab('content');
codeBox.value = "Please update my site's brand style (colors and fonts) to match these settings from the Style Editor:\\n\\n" + styleRequestText;
chatInput.focus();
});
}
initStyleEditor();
</script>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    build()
