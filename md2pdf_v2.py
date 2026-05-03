#!/usr/bin/env python3
"""Generate PDF from Doubao AI tutorial using ReportLab with CJK font support."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import re

# Register CJK font
FONT_PATH = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc"
FONT_BOLD_PATH = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc"

# Register the font (index 0 for TTC files)
pdfmetrics.registerFont(TTFont("NotoSans", FONT_PATH, subfontIndex=0))
pdfmetrics.registerFont(TTFont("NotoSans-Bold", FONT_BOLD_PATH, subfontIndex=0))

# Read markdown
with open("/root/.openclaw/workspace/ai-usage-tutorial-doubao.md", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

# Define styles
styles = {
    "title": ParagraphStyle(
        "MyTitle",
        fontName="NotoSans-Bold",
        fontSize=22,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=10,
    ),
    "subtitle": ParagraphStyle(
        "MySubtitle",
        fontName="NotoSans",
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=6,
        textColor=colors.HexColor("#666666"),
    ),
    "h1": ParagraphStyle(
        "MyH1",
        fontName="NotoSans-Bold",
        fontSize=16,
        leading=20,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor("#1a1a2e"),
    ),
    "h2": ParagraphStyle(
        "MyH2",
        fontName="NotoSans-Bold",
        fontSize=13,
        leading=17,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor("#16213e"),
    ),
    "h3": ParagraphStyle(
        "MyH3",
        fontName="NotoSans-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=4,
        textColor=colors.HexColor("#0f3460"),
    ),
    "body": ParagraphStyle(
        "MyBody",
        fontName="NotoSans",
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
    ),
    "bullet": ParagraphStyle(
        "MyBullet",
        fontName="NotoSans",
        fontSize=10,
        leading=14,
        leftIndent=16,
        spaceAfter=2,
    ),
    "code": ParagraphStyle(
        "MyCode",
        fontName="Courier",
        fontSize=7,
        leading=10,
        leftIndent=16,
        spaceAfter=2,
        backColor=colors.HexColor("#f5f5f5"),
    ),
    "quote": ParagraphStyle(
        "MyQuote",
        fontName="NotoSans",
        fontSize=9,
        leading=13,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=4,
        textColor=colors.HexColor("#555555"),
    ),
    "center": ParagraphStyle(
        "MyCenter",
        fontName="NotoSans",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
    ),
}

def strip_md(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    return text.strip()

def is_h1(line):
    return line.startswith("# ") and not line.startswith("## ")

def is_h2(line):
    return line.startswith("## ") and not line.startswith("### ")

def is_h3(line):
    return line.startswith("### ")

def is_separator(line):
    return line.strip() == "---"

def is_table_line(line):
    return line.startswith("|")

def is_table_sep(line):
    return line.startswith("|") and ("--" in line or "───" in line)

def is_bullet(line):
    return line.startswith("- ") or line.startswith("* ")

def is_code(line):
    return line.startswith("    ") or line.startswith("\t")

def is_quote(line):
    return line.startswith(">")

story = []
in_table = False
table_rows = []

for i, line in enumerate(lines):
    # Skip frontmatter, images, code fences
    if line.startswith("---"):
        continue
    if line.startswith("```"):
        continue
    if line.startswith("![") or line.startswith("[Queued"):
        continue

    # H1
    if is_h1(line):
        if in_table:
            # Finish current table
            t = Table(table_rows, colWidths=[1.5*cm, 5*cm, 4*cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "NotoSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))
            table_rows = []
            in_table = False

        title = strip_md(line)
        story.append(Paragraph(title, styles["h1"]))

    # H2
    elif is_h2(line):
        if in_table:
            t = Table(table_rows, colWidths=[1.5*cm, 5*cm, 4*cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "NotoSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))
            table_rows = []
            in_table = False

        title = strip_md(line)
        story.append(Paragraph(title, styles["h2"]))

    # H3
    elif is_h3(line):
        if in_table:
            t = Table(table_rows, colWidths=[1.5*cm, 5*cm, 4*cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "NotoSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))
            table_rows = []
            in_table = False

        title = strip_md(line)
        story.append(Paragraph(title, styles["h3"]))

    # Separator
    elif is_separator(line):
        if in_table:
            t = Table(table_rows, colWidths=[1.5*cm, 5*cm, 4*cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "NotoSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))
            table_rows = []
            in_table = False

    # Table separator row - skip
    elif is_table_sep(line):
        continue

    # Table row
    elif is_table_line(line):
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if cells and any(c.strip() for c in cells):
            # Clean markdown from cells
            cleaned = [strip_md(c) for c in cells]
            table_rows.append(cleaned)
            in_table = True
        else:
            in_table = False

    # Bullet
    elif is_bullet(line):
        if in_table:
            t = Table(table_rows, colWidths=[1.5*cm, 5*cm, 4*cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "NotoSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))
            table_rows = []
            in_table = False

        text = strip_md(line[2:])
        if text:
            story.append(Paragraph(f"\u2022 {text}", styles["bullet"]))

    # Code block
    elif is_code(line):
        if in_table:
            t = Table(table_rows, colWidths=[1.5*cm, 5*cm, 4*cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "NotoSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))
            table_rows = []
            in_table = False

        text = line.strip()
        if text:
            story.append(Paragraph(text, styles["code"]))

    # Quote
    elif is_quote(line):
        if in_table:
            t = Table(table_rows, colWidths=[1.5*cm, 5*cm, 4*cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "NotoSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))
            table_rows = []
            in_table = False

        text = strip_md(line[1:].strip())
        if text:
            story.append(Paragraph(f'"{text}"', styles["quote"]))

    # Empty line
    elif line.strip() == "":
        if in_table:
            pass  # Don't break table for empty lines
        else:
            story.append(Spacer(1, 4))

    # Paragraph
    else:
        if in_table:
            t = Table(table_rows, colWidths=[1.5*cm, 5*cm, 4*cm])
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "NotoSans"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))
            table_rows = []
            in_table = False

        text = strip_md(line)
        if text:
            story.append(Paragraph(text, styles["body"]))

# Flush any remaining table
if table_rows:
    t = Table(table_rows, colWidths=[1.5*cm, 5*cm, 4*cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "NotoSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t)

# Build PDF
output_path = "/root/.openclaw/workspace/ai-usage-tutorial-doubao.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=2*cm,
    rightMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
)
doc.build(story)

print(f"PDF saved: {output_path}")
print(f"Check the file to verify CJK rendering")
