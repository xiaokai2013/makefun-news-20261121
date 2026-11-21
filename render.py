#!/usr/bin/env python3
"""Render the front page for Saturday 21 November 2026.

Build tool for the make.fun bounty news-image-20261121, "Sum up
21 November's world news in one image". It reads news.json (seven
headlines verified against reporting dated 21 November 2026) and draws
a 1024x1024 newspaper front page with Pillow. The output, entry.png,
is written next to this script (override with the OUT env var).

This is only the build tool. The graded entrypoint is main.py, which
copies the committed entry.png to /output/entry.png using only the
standard library — the grader's bare python:3.13-slim container has no
Pillow and no system fonts.

Deterministic: no clock, no randomness, no network, fixed fonts, so
the same news.json always produces identical PNG bytes.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE = (1024, 1024)
MARGIN = 48
PAPER = (248, 245, 238)   # newsprint off-white
INK = (17, 17, 17)        # near-black ink
ACCENT = (185, 28, 28)    # accent red
GREY = (92, 88, 80)       # deck / footer grey
HAIR = (200, 196, 186)    # hairline grey
WHITE = (255, 255, 255)

FONT_DIRS = ("/usr/share/fonts/truetype/liberation",
             "/usr/share/fonts/truetype/dejavu")


def locate(names):
    """Return the first candidate font file that exists on disk."""
    for folder in FONT_DIRS:
        for name in names:
            candidate = os.path.join(folder, name)
            if os.path.isfile(candidate):
                return candidate
    raise FileNotFoundError("no font among %r under %r" % (names, FONT_DIRS))


SERIF_BOLD = locate(["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"])
SERIF = locate(["LiberationSerif-Regular.ttf", "DejaVuSerif.ttf"])
SANS_BOLD = locate(["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"])
SANS = locate(["LiberationSans-Regular.ttf", "DejaVuSans.ttf"])


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, width):
    """Greedy word wrap: lines that each fit inside width pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class FrontPage:
    """Draws the whole front page onto one 1024x1024 image."""

    def __init__(self, news):
        self.news = news
        self.img = Image.new("RGB", PAGE, PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.left = MARGIN
        self.right = PAGE[0] - MARGIN
        self.inner = self.right - self.left

    def rule(self, y, fill, width):
        self.d.line([(self.left, y), (self.right, y)], fill=fill, width=width)

    def lines(self, text, x, y, font, fill, leading):
        """Draw wrapped text starting at (x, y); return y below it."""
        for line in text:
            self.d.text((x, y), line, font=font, fill=fill, anchor="la")
            y += leading
        return y

    def masthead(self, y):
        d = self.d
        d.text((PAGE[0] // 2, y), self.news["masthead"],
               font=load(SERIF_BOLD, 92), fill=INK, anchor="ma")
        y += 96
        self.rule(y, INK, 3)
        y += 13
        d.text((self.left, y), self.news["dateline_left"],
               font=load(SANS_BOLD, 20), fill=INK, anchor="la")
        d.text((self.right, y), self.news["dateline_right"],
               font=load(SANS_BOLD, 20), fill=ACCENT, anchor="ra")
        y += 29
        self.rule(y, ACCENT, 4)
        return y + 24

    def lead(self, y):
        d = self.d
        lead = self.news["lead"]
        d.text((self.left, y), lead["kicker"],
               font=load(SANS_BOLD, 19), fill=ACCENT, anchor="la")
        y += 29
        head = load(SERIF_BOLD, 44)
        y = self.lines(wrap_text(d, lead["headline"], head, self.inner),
                       self.left, y, head, INK, 52)
        y += 6
        deck = load(SERIF, 23)
        y = self.lines(wrap_text(d, lead["deck"], deck, self.inner),
                       self.left, y, deck, INK, 30)
        y += 20
        self.rule(y, INK, 2)
        return y + 22

    def story_height(self, story, width):
        """Pixel height of one grid story (badge row + headline + deck)."""
        text_w = width - 40
        head = wrap_text(self.d, story["headline"],
                         load(SERIF_BOLD, 24), text_w)
        deck = wrap_text(self.d, story["deck"], load(SERIF, 18), text_w)
        return 25 + len(head) * 29 + 3 + len(deck) * 23

    def story(self, item, number, x, y, width):
        """Draw one numbered grid story at (x, y); return height used."""
        d = self.d
        top = y
        d.ellipse([x, y + 1, x + 28, y + 29], fill=ACCENT)
        d.text((x + 14, y + 15), str(number),
               font=load(SANS_BOLD, 18), fill=WHITE, anchor="mm")
        tx, tw = x + 40, width - 40
        d.text((tx, y), item["kicker"], font=load(SANS_BOLD, 15),
               fill=ACCENT, anchor="la")
        y += 25
        head = load(SERIF_BOLD, 24)
        y = self.lines(wrap_text(d, item["headline"], head, tw),
                       tx, y, head, INK, 29)
        y += 3
        deck = load(SERIF, 18)
        y = self.lines(wrap_text(d, item["deck"], deck, tw),
                       tx, y, deck, GREY, 23)
        return y - top

    def grid(self, y):
        d = self.d
        gutter = 36
        col = (self.inner - gutter) // 2
        footer_top = PAGE[1] - 84
        stories = self.news["stories"]
        # Measure each row first (a row is as tall as its taller story),
        # then spread any leftover space evenly between the rows so the
        # grid fills the page instead of leaving a gap at the bottom.
        row_h = []
        for r in range(3):
            pair = stories[r * 2:(r + 1) * 2]
            row_h.append(max(self.story_height(s, col) for s in pair))
        gap = 26 + max(0, (footer_top - y) - (sum(row_h) + 2 * 26)) // 2
        for r in range(3):
            for i, item in enumerate(stories[r * 2:(r + 1) * 2]):
                cx = self.left + i * (col + gutter)
                self.story(item, r * 2 + i + 1, cx, y, col)
            # Vertical hairline between the two columns.
            mid = self.left + col + gutter // 2
            d.line([(mid, y + 4), (mid, y + row_h[r] - 4)],
                   fill=HAIR, width=1)
            y += row_h[r]
            if r < 2:
                d.line([(self.left, y + gap // 2),
                        (self.right, y + gap // 2)], fill=HAIR, width=1)
                y += gap

    def footer(self):
        d = self.d
        y = PAGE[1] - 84
        self.rule(y, INK, 2)
        y += 12
        sans = load(SANS, 14)
        for line in wrap_text(d, self.news["footer"], sans, self.inner):
            d.text((PAGE[0] // 2, y), line, font=sans, fill=GREY,
                   anchor="ma")
            y += 19
        y += 4
        d.text((PAGE[0] // 2, y), self.news["credit"], font=sans,
               fill=GREY, anchor="ma")

    def build(self):
        y = self.masthead(26)
        y = self.lead(y)
        self.grid(y)
        self.footer()
        return self.img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "news.json"), encoding="utf-8") as fh:
        news = json.load(fh)
    page = FrontPage(news)
    out = os.environ.get("OUT", os.path.join(here, "entry.png"))
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    page.build().save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
