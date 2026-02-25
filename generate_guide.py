#!/usr/bin/env python3
"""Generate a dark-themed Claude Code guide PDF with Anthropic branding."""

import os
from datetime import date

import yaml
from fpdf import FPDF

_HERE = os.path.dirname(os.path.abspath(__file__))

# ── Anthropic Brand Colors ───────────────────────────────────────────────
BG       = (20, 20, 19)       # #141413  - page background
BG_LIGHT = (30, 30, 28)       # slightly lighter for cards/boxes
SURFACE  = (40, 40, 37)       # code block / card backgrounds
BORDER   = (60, 60, 55)       # subtle borders
TEXT     = (250, 249, 245)    # #faf9f5 - primary text
TEXT_DIM = (176, 174, 165)    # #b0aea5 - secondary/muted text
TEXT_HINT= (120, 118, 110)    # dimmer text for footnotes
ORANGE   = (217, 119, 87)    # #d97757 - primary accent
BLUE     = (106, 155, 204)   # #6a9bcc - secondary accent
GREEN    = (120, 140, 93)    # #788c5d - tertiary accent
GREEN_L  = (90, 120, 70)     # darker green for tip bg


class DarkPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)

    def _bg(self):
        """Fill current page with dark background."""
        self.set_fill_color(*BG)
        self.rect(0, 0, self.w, self.h, "F")

    def header(self):
        self._bg()
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 7.5)
            self.set_text_color(*TEXT_HINT)
            self.cell(0, 8, "Claude Code  |  Tips & Best Practices", align="C")
            self.ln(9)
            # thin accent line - centered, below text
            self.set_draw_color(*ORANGE)
            self.set_line_width(0.3)
            y = self.get_y()
            line_w = 70
            cx = self.w / 2
            self.line(cx - line_w / 2, y, cx + line_w / 2, y)
            self.ln(3)

    def footer(self):
        self.set_y(-18)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*TEXT_HINT)
        self.cell(0, 8, f"{self.page_no()}/{{nb}}", align="C")

    # ── Cover page ───────────────────────────────────────────────────────
    def cover_page(self, tb_brand):
        self.add_page()
        self._bg()

        # Trailblaze brand (mark + wordmark)
        brand_w = 100
        brand_x = (self.w - brand_w) / 2
        self.image(tb_brand, x=brand_x, y=45, w=brand_w)

        self.set_y(62)
        self.ln(10)

        # Title
        self.set_font("Helvetica", "B", 36)
        self.set_text_color(*TEXT)
        self.cell(0, 16, "Claude Code", align="C")
        self.ln(18)

        # Subtitle
        self.set_font("Helvetica", "", 18)
        self.set_text_color(*ORANGE)
        self.cell(0, 10, "Tips & Best Practices", align="C")
        self.ln(16)

        # Accent line
        self.set_draw_color(*ORANGE)
        self.set_line_width(0.8)
        lw = 60
        self.line((self.w - lw) / 2, self.get_y(), (self.w + lw) / 2, self.get_y())
        self.ln(18)

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT_HINT)
        self.cell(0, 6, date.today().strftime("%Y-%m-%d"), align="C")

    # ── Section title ────────────────────────────────────────────────────
    def section_title(self, title):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*ORANGE)
        self.ln(4)
        self.cell(0, 11, title)
        self.ln(9)
        self.set_draw_color(*BORDER)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    # ── Subsection ───────────────────────────────────────────────────────
    def subsection(self, title):
        # Keep-with-next: need room for header + at least some content
        if self.get_y() > self.h - self.b_margin - 45:
            self.add_page()
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*BLUE)
        self.ln(4)
        self.cell(0, 7, title)
        self.ln(8)

    # ── Section break (new section, only breaks page if needed) ──────
    def section_break(self):
        """Start new section: only add page if less than 30% of page remains."""
        remaining = self.h - self.b_margin - self.get_y()
        if remaining < (self.h - self.t_margin - self.b_margin) * 0.30:
            self.add_page()
        else:
            self.ln(10)
            self.set_draw_color(*BORDER)
            self.set_line_width(0.3)
            y = self.get_y()
            self.line(self.l_margin + 30, y, self.w - self.r_margin - 30, y)
            self.ln(10)

    # ── Body text ────────────────────────────────────────────────────────
    def body(self, text):
        self.set_font("Helvetica", "", 10.5)
        self.set_text_color(*TEXT_DIM)
        self.multi_cell(0, 6, text)
        self.ln(2)

    # ── Bullet ───────────────────────────────────────────────────────────
    def bullet(self, text, indent=10):
        x = self.get_x()
        self.set_font("Helvetica", "", 10.5)
        self.set_text_color(*TEXT_DIM)
        self.set_x(x + indent)
        # Use orange dash for bullet
        self.set_text_color(*ORANGE)
        self.cell(5, 6, "-")
        self.set_text_color(*TEXT_DIM)
        self.multi_cell(0, 6, text)
        self.ln(1)

    # ── Code block ───────────────────────────────────────────────────────
    def code(self, text):
        x = self.l_margin + 3
        w = self.w - self.l_margin - self.r_margin - 6

        lines = text.split("\n")
        h = len(lines) * 5.5 + 10

        # If it won't fit, start new page
        if self.get_y() + h > self.h - self.b_margin:
            self.add_page()

        y_start = self.get_y()
        self.set_fill_color(*SURFACE)
        self.set_draw_color(*BORDER)
        self.set_line_width(0.3)
        self.rect(x, y_start, w, h, "DF")

        self.set_font("Courier", "", 9)
        self.set_text_color(*GREEN)
        self.set_y(y_start + 4)
        for line in lines:
            self.set_x(x + 6)
            self.cell(0, 5.5, line)
            self.ln(5.5)
        self.set_y(y_start + h + 4)

    # ── Tip box ──────────────────────────────────────────────────────────
    def tip(self, text):
        x = self.l_margin + 3
        w = self.w - self.l_margin - self.r_margin - 6
        inner_w = w - 10

        # Measure actual height needed by rendering to a scratch position
        self.set_font("Helvetica", "", 10)
        # Estimate lines: chars per line at inner_w ~= inner_w / 2.1 for 10pt Helvetica
        chars_per_line = max(1, int(inner_w / 2.1))
        import math
        nlines = 0
        for paragraph in text.split("\n"):
            nlines += max(1, math.ceil(len(paragraph) / chars_per_line))
        h = nlines * 5.5 + 20  # TIP label + padding

        # If it won't fit, start new page
        if self.get_y() + h > self.h - self.b_margin:
            self.add_page()

        y_start = self.get_y()

        self.set_fill_color(30, 42, 28)
        self.set_draw_color(*GREEN)
        self.set_line_width(0.6)
        self.rect(x, y_start, w, h, "DF")

        self.set_xy(x + 5, y_start + 4)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GREEN)
        self.cell(0, 5.5, "TIP")
        self.ln(7)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(160, 190, 140)
        self.set_x(x + 5)
        self.multi_cell(inner_w, 5.5, text)
        self.set_y(y_start + h + 4)

    # ── Quote box ────────────────────────────────────────────────────────
    def quote(self, text, author="Boris Cherny, Claude Code creator"):
        # Estimate height needed for keep-together
        import math
        chars_per_line = max(1, int((self.w - self.l_margin - self.r_margin - 16) / 2.2))
        nlines = max(1, math.ceil(len(text) / chars_per_line)) + 1
        h_est = nlines * 6 + 14
        if self.get_y() + h_est > self.h - self.b_margin:
            self.add_page()

        x = self.l_margin + 3
        y_start = self.get_y()

        self.set_draw_color(*ORANGE)
        self.set_line_width(2.5)

        self.set_font("Helvetica", "I", 10.5)
        self.set_text_color(*TEXT)
        self.set_x(x + 8)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 16, 6, f'"{text}"')

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*ORANGE)
        self.set_x(x + 8)
        self.cell(0, 6, f"-- {author}")
        self.ln(6)

        y_end = self.get_y()
        self.line(x, y_start, x, y_end)
        self.set_line_width(0.5)
        self.ln(5)


# ── Content renderers ────────────────────────────────────────────────────

def render_heading(pdf, text):
    """Render a numbered heading (bold 11pt, TEXT color)."""
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 7, text)
    pdf.ln(7)


def render_prompts(pdf, prompts):
    """Render good/bad prompt comparison pairs."""
    for pair in prompts:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(200, 100, 100)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 5.5, pair["bad"])
        pdf.set_text_color(*GREEN)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 5.5, pair["good"])
        pdf.ln(4)


def render_content(pdf, items):
    """Render a list of mixed content elements."""
    for item in items:
        if "body" in item:
            pdf.body(item["body"])
        elif "bullet" in item:
            pdf.bullet(item["bullet"])
        elif "code" in item:
            pdf.code(item["code"].rstrip("\n"))
        elif "tip" in item:
            pdf.tip(item["tip"])
        elif "subsection" in item:
            pdf.subsection(item["subsection"])
        elif "heading" in item:
            render_heading(pdf, item["heading"])
        elif "quote" in item:
            q = item["quote"]
            if "attribution" in q:
                pdf.quote(q["text"], q["attribution"])
            else:
                pdf.quote(q["text"])
        elif "prompts" in item:
            render_prompts(pdf, item["prompts"])


def render_tips(pdf, section):
    """Render the top-10 tips list with custom title style."""
    # Custom title (22pt TEXT) — differs from section_title's 18pt ORANGE
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 12, section["title"])
    pdf.ln(14)
    pdf.ln(2)

    for tip in section["tips"]:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*ORANGE)
        pdf.cell(10, 7, tip["num"] + ".")
        pdf.set_text_color(*TEXT)
        pdf.cell(0, 7, tip["title"])
        pdf.ln(7)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*TEXT_DIM)
        pdf.set_x(pdf.l_margin + 14)
        pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 14, 5.5, tip["desc"])
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*BLUE)
        pdf.set_x(pdf.l_margin + 14)
        pdf.cell(0, 5.5, tip["ref"])
        pdf.ln(8)


def render_pitfalls(pdf, pitfalls):
    """Render the pitfalls list with problem/fix pairs."""
    for p in pitfalls:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*ORANGE)
        pdf.cell(0, 7, p["title"])
        pdf.ln(7)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*TEXT_DIM)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 5.5, f"Problem: {p['problem']}")
        pdf.ln(1)
        pdf.set_text_color(*GREEN)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 5.5, f"Fix: {p['fix']}")
        pdf.ln(5)


def render_sources(pdf, sources):
    """Render the sources footer."""
    pdf.ln(6)
    pdf.set_draw_color(*BORDER)
    pdf.set_line_width(0.4)
    w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.line(pdf.l_margin + w * 0.3, pdf.get_y(), pdf.l_margin + w * 0.7, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*TEXT_HINT)
    text = "Sources: " + sources[0] + "\n" + "\n".join(sources[1:])
    pdf.multi_cell(0, 4.5, text, align="C")


def build_guide():
    with open(os.path.join(_HERE, "content.yaml")) as f:
        data = yaml.safe_load(f)

    pdf = DarkPDF()
    pdf.alias_nb_pages()
    pdf.cover_page(os.path.join(_HERE, data["cover"]["brand_image"]))

    for section in data["sections"]:
        if section.get("new_page"):
            pdf.add_page()
        else:
            pdf.section_break()

        stype = section.get("type")
        if stype == "tips_list":
            render_tips(pdf, section)
        elif stype == "pitfalls_list":
            pdf.section_title(section["title"])
            render_pitfalls(pdf, section["pitfalls"])
        else:
            pdf.section_title(section["title"])
            render_content(pdf, section["content"])

    render_sources(pdf, data["sources"])
    return pdf


if __name__ == "__main__":
    pdf = build_guide()
    out = os.path.join(_HERE, "Claude_Code_Tips_and_Best_Practices.pdf")
    pdf.output(out)
    print(f"PDF generated: {out}")
