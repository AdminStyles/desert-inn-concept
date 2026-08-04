# -*- coding: utf-8 -*-
"""
Shared styling + visual-component module for the client guide PDFs.
Palette comes from brand_config.COLORS, so the guides automatically match the
site's colors. Adapted from the Fat Tony's / Miracle Greens guide module.
Runs in Linux (Liberation/DejaVu fonts) or Windows (Arial/Georgia fallback).
Needs reportlab:  pip install reportlab
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_config as CFG
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether,
    CondPageBreak, Image, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def _c(key):
    return colors.HexColor(CFG.COLORS[key])

BG_DEEP     = _c("bg_deep")
PANEL       = _c("panel")
GREEN       = _c("primary")
GREEN_BRIGHT= _c("primary_bright")
GREEN_GLOW  = _c("glow")
ORANGE      = _c("accent")
ORANGE_DEEP = _c("accent_deep")
CREAM       = _c("cream")
CREAM_MUTED = _c("cream_muted")
ALT_ROW     = colors.HexColor("#101012")   # neutral alternating table row

FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Optional cover badge: assets/guide-badge.png, else the logo if it's a local file.
_badge_candidates = [os.path.join(FOLDER, "assets", "guide-badge.png")]
if CFG.LOGO_IMAGE and not CFG.LOGO_IMAGE.startswith("http"):
    _badge_candidates.append(os.path.join(FOLDER, CFG.LOGO_IMAGE))
LOGO_BADGE = next((p for p in _badge_candidates if os.path.exists(p)), None)


def _register(name, *candidates):
    for p in candidates:
        if os.path.exists(p):
            pdfmetrics.registerFont(TTFont(name, p))
            return
    raise RuntimeError("No font found for %s" % name)

_register("LibSans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", r"C:\Windows\Fonts\arial.ttf")
_register("LibSans-Bold", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", r"C:\Windows\Fonts\arialbd.ttf")
_register("LibSans-Italic", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf", r"C:\Windows\Fonts\ariali.ttf")
_register("HeadFont", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", r"C:\Windows\Fonts\georgiab.ttf")

PAGE_W, PAGE_H = letter

styles = {
    "Tag": ParagraphStyle("Tag", fontName="LibSans-Bold", fontSize=10, leading=13,
                           textColor=ORANGE, alignment=TA_CENTER, spaceAfter=6),
    "DocTitle": ParagraphStyle("DocTitle", fontName="HeadFont", fontSize=30, leading=34,
                                textColor=CREAM, alignment=TA_CENTER, spaceAfter=8),
    "DocSubtitle": ParagraphStyle("DocSubtitle", fontName="LibSans", fontSize=13, leading=18,
                                   textColor=GREEN_GLOW, alignment=TA_CENTER, spaceAfter=4),
    "H1": ParagraphStyle("H1", fontName="HeadFont", fontSize=16, leading=20,
                          textColor=ORANGE, spaceBefore=18, spaceAfter=8),
    "H2": ParagraphStyle("H2", fontName="LibSans-Bold", fontSize=12.5, leading=16,
                          textColor=GREEN_GLOW, spaceBefore=10, spaceAfter=4),
    "Body": ParagraphStyle("Body", fontName="LibSans", fontSize=10.3, leading=15,
                            textColor=CREAM, spaceAfter=6),
    "BodyTan": ParagraphStyle("BodyTan", fontName="LibSans-Italic", fontSize=9.5, leading=13,
                               textColor=CREAM_MUTED, spaceAfter=6),
    "Bullet": ParagraphStyle("Bullet", fontName="LibSans", fontSize=10.3, leading=15,
                              textColor=CREAM, leftIndent=14, bulletIndent=2, spaceAfter=4),
    "Code": ParagraphStyle("Code", fontName="Courier", fontSize=9, leading=13,
                            textColor=GREEN_GLOW, backColor=PANEL,
                            borderPadding=8, leftIndent=4, spaceAfter=8),
    "Caption": ParagraphStyle("Caption", fontName="LibSans-Italic", fontSize=8.5, leading=11,
                               textColor=CREAM_MUTED),
    "CardTitle": ParagraphStyle("CardTitle", fontName="LibSans-Bold", fontSize=12, leading=15,
                                 textColor=BG_DEEP, spaceAfter=4),
    "CardBadge": ParagraphStyle("CardBadge", fontName="LibSans-Bold", fontSize=8.5, leading=11,
                                 textColor=BG_DEEP, alignment=TA_CENTER),
    "CardBullet": ParagraphStyle("CardBullet", fontName="LibSans", fontSize=9.3, leading=13,
                                  textColor=BG_DEEP, leftIndent=10, spaceAfter=2),
}


def make_title_block(title, subtitle, tag):
    flow = [Spacer(1, 0.2 * inch)]
    if LOGO_BADGE:
        img = Image(LOGO_BADGE, width=0.95 * inch, height=0.95 * inch)
        img.hAlign = "CENTER"
        flow.append(img); flow.append(Spacer(1, 0.12 * inch))
    flow.extend([
        Paragraph(tag.upper(), styles["Tag"]),
        Paragraph(title, styles["DocTitle"]),
        Paragraph(subtitle, styles["DocSubtitle"]),
        Spacer(1, 10),
        HRFlowable(width="100%", thickness=1.4, color=ORANGE, spaceAfter=16),
    ])
    return flow

def page_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG_DEEP); canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(ORANGE); canvas.rect(0, PAGE_H - 6, PAGE_W, 6, fill=1, stroke=0)
    canvas.restoreState()

def footer(canvas, doc):
    page_background(canvas, doc)
    canvas.saveState()
    canvas.setFont("LibSans", 8); canvas.setFillColor(CREAM_MUTED)
    canvas.drawString(0.75 * inch, 0.5 * inch, CFG.FOOTER_LABEL)
    canvas.drawRightString(PAGE_W - 0.75 * inch, 0.5 * inch, "Page %d" % doc.page)
    canvas.setStrokeColor(ORANGE); canvas.setLineWidth(0.6)
    canvas.line(0.75 * inch, 0.65 * inch, PAGE_W - 0.75 * inch, 0.65 * inch)
    canvas.restoreState()

def section_table(rows, col_widths):
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "LibSans-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "LibSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 0), (-1, 0), BG_DEEP),
        ("BACKGROUND", (0, 0), (-1, 0), ORANGE),
        ("TEXTCOLOR", (0, 1), (-1, -1), CREAM),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PANEL, ALT_ROW]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2E5C40")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


class PipelineDiagram(Flowable):
    """A horizontal row of numbered boxes connected by arrows."""
    def __init__(self, steps, width=6.5 * inch, height=0.95 * inch, box_color=None):
        Flowable.__init__(self)
        self.steps = steps; self.width = width; self.height = height
        self.box_color = box_color or ORANGE
    def wrap(self, aw, ah):
        return (self.width, self.height)
    def draw(self):
        c = self.canv; n = len(self.steps)
        gap = 0.28 * inch if n >= 5 else 0.32 * inch
        box_w = (self.width - gap * (n - 1)) / n
        box_h = self.height * 0.74; y = self.height * 0.12
        label_size = min(9.3, max(7.0, box_w / 11.8))
        sub_size = max(6.2, label_size - 1.1)
        badge_r = min(9, max(6.0, box_w / 14))
        c.saveState()
        for i, step in enumerate(self.steps):
            x = i * (box_w + gap); box_cx = x + box_w / 2.0
            if i < n - 1:
                ay = y + box_h / 2; ax0 = x + box_w; ax1 = ax0 + gap
                c.setStrokeColor(ORANGE); c.setLineWidth(1.6)
                c.line(ax0 + 3, ay, ax1 - 7, ay)
                c.setFillColor(ORANGE); p = c.beginPath()
                p.moveTo(ax1 - 7, ay + 4); p.lineTo(ax1 - 7, ay - 4); p.lineTo(ax1, ay); p.close()
                c.drawPath(p, fill=1, stroke=0)
            c.setFillColor(PANEL); c.setStrokeColor(self.box_color); c.setLineWidth(1.3)
            c.roundRect(x, y, box_w, box_h, 6, fill=1, stroke=1)
            badge_cx = box_cx; badge_cy = y + box_h - badge_r - 7
            c.setFillColor(self.box_color); c.circle(badge_cx, badge_cy, badge_r, fill=1, stroke=0)
            c.setFillColor(BG_DEEP); c.setFont("LibSans-Bold", badge_r + 1.2)
            c.drawCentredString(badge_cx, badge_cy - (badge_r * 0.36), str(i + 1))
            line1, line2 = (step + (None,))[:2] if len(step) == 1 else step
            label_top = badge_cy - badge_r - 12
            c.setFillColor(CREAM); c.setFont("LibSans-Bold", label_size)
            if line2:
                c.drawCentredString(box_cx, label_top, line1)
                c.setFont("LibSans", sub_size); c.setFillColor(GREEN_GLOW)
                c.drawCentredString(box_cx, label_top - (label_size + 2), line2)
            else:
                c.drawCentredString(box_cx, label_top - 3, line1)
        c.restoreState()


def two_card_row(card_a, card_b, width=6.5 * inch):
    def build_card(card):
        rows = []
        badge_bg = ORANGE if card.get("recommended") else GREEN_BRIGHT
        rows.append([Paragraph(card.get("badge", ""), styles["CardBadge"])])
        rows.append([Paragraph(card["title"], styles["CardTitle"])])
        for line in card["body"]:
            rows.append([Paragraph(line, styles["CardBullet"])])
        t = Table(rows, colWidths=[width / 2 - 0.15 * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), badge_bg),
            ("BACKGROUND", (0, 1), (-1, -1), CREAM),
            ("TOPPADDING", (0, 0), (-1, 0), 4), ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
            ("TOPPADDING", (0, 1), (-1, -1), 5), ("BOTTOMPADDING", (0, 1), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("BOX", (0, 0), (-1, -1), 1.4, badge_bg), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        return t
    outer = Table([[build_card(card_a), build_card(card_b)]], colWidths=[width / 2, width / 2])
    outer.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (0, 0), 0), ("RIGHTPADDING", (0, 0), (0, 0), 7),
        ("LEFTPADDING", (1, 0), (1, 0), 7), ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return outer

def keep_headings_with_next(flowables, frame_width=6.5 * inch):
    out = []; i = 0; n = len(flowables)
    while i < n:
        f = flowables[i]
        style_name = getattr(getattr(f, "style", None), "name", None)
        if style_name in ("H1", "H2") and i + 1 < n:
            nxt = flowables[i + 1]
            _, head_h = f.wrap(frame_width, 10000)
            _, nxt_h = nxt.wrap(frame_width, 10000)
            out.append(CondPageBreak(head_h + nxt_h + 8)); out.append(f); out.append(nxt)
            i += 2
        else:
            out.append(f); i += 1
    return out

print("Guide module ready for", CFG.BUSINESS_NAME)
