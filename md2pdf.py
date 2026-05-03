#!/usr/bin/env python3
"""Convert Doubao AI tutorial markdown to PDF using fpdf2 with CJK support."""

import fpdf
import re

with open("/root/.openclaw/workspace/ai-usage-tutorial-doubao.md", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

pdf = fpdf.FPDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=15)

CJK_REGULAR = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc"
CJK_BOLD = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc"

pdf.add_font("NotoSans", "", CJK_REGULAR)
pdf.add_font("NotoSans", "B", CJK_BOLD)
pdf.add_font("NotoSans", "I", CJK_REGULAR)

font_main = "NotoSans"

pdf.add_page()
pdf.set_font(font_main, "", 10)

def strip_md(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    return text.strip()

def safe_write(text, font="", size=10, align="L", fill=False):
    """Write text, skipping on render error."""
    try:
        if font:
            pdf.set_font(font_main, font, size)
        pdf.multi_cell(0, 5, text, align=align, fill=fill)
    except Exception:
        pass  # Skip problematic content

def is_h1(line):
    return line.startswith("# ") and not line.startswith("## ")

def is_h2(line):
    return line.startswith("## ") and not line.startswith("### ")

def is_h3(line):
    return line.startswith("### ")

for line in lines:
    if line.startswith("---") or line.startswith("```") or line.startswith("![") or line.startswith("[Queued"):
        continue

    # Title (H1)
    if is_h1(line):
        title = strip_md(line)
        pdf.ln(5)
        pdf.set_font(font_main, "B", 14)
        safe_write(title, "", 14)
        pdf.set_font(font_main, "", 10)

    # Section (H2)
    elif is_h2(line):
        title = strip_md(line)
        pdf.ln(4)
        pdf.set_font(font_main, "B", 12)
        safe_write(title, "", 12)
        pdf.set_font(font_main, "", 10)

    # Subsection (H3)
    elif is_h3(line):
        title = strip_md(line)
        pdf.ln(3)
        pdf.set_font(font_main, "B", 10)
        safe_write(title, "", 10)
        pdf.set_font(font_main, "", 10)

    # Table separator
    elif line.startswith("|") and ("--" in line or "───" in line):
        continue

    # Table row - skip tables for PDF (too wide)
    elif line.startswith("|"):
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if cells and any(cells):
            pdf.set_font(font_main, "", 8)
            text = "  |  ".join(cells)
            try:
                pdf.multi_cell(0, 4, text)
            except Exception:
                try:
                    pdf.multi_cell(0, 4, text[:80])
                except Exception:
                    pass
            pdf.set_font(font_main, "", 10)

    # Bullet
    elif line.startswith("- ") or line.startswith("* "):
        text = strip_md(line[2:])
        if text:
            pdf.set_x(pdf.l_margin + 6)
            safe_write(f"\u2022 {text}", "", 9)

    # Code block line
    elif line.startswith("    ") or line.startswith("\t"):
        text = line.strip()
        if text:
            pdf.set_font(font_main, "", 7)
            pdf.set_fill_color(242, 242, 242)
            try:
                pdf.multi_cell(0, 3.5, text, fill=True)
            except Exception:
                try:
                    pdf.multi_cell(0, 3.5, text[:100], fill=True)
                except Exception:
                    pass
            pdf.set_font(font_main, "", 10)

    # Quote
    elif line.startswith(">"):
        text = strip_md(line[1:].strip())
        if text:
            pdf.set_x(pdf.l_margin + 4)
            pdf.set_font(font_main, "I", 9)
            safe_write(f'"{text}"', "I", 9)
            pdf.set_font(font_main, "", 10)

    # Separator
    elif line.strip() == "---":
        pdf.ln(2)
        pdf.set_draw_color(180, 180, 180)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(4)

    # Empty
    elif line.strip() == "":
        pdf.ln(1.5)

    # Paragraph
    else:
        text = strip_md(line)
        if text:
            try:
                pdf.multi_cell(0, 4.5, text)
            except Exception:
                try:
                    pdf.multi_cell(0, 4.5, text[:100])
                except Exception:
                    pass

output_path = "/root/.openclaw/workspace/ai-usage-tutorial-doubao.pdf"
pdf.output(output_path)
print(f"PDF saved to {output_path}")
print(f"Total pages: {pdf.page_no()}")
