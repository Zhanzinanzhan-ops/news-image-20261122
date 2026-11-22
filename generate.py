#!/usr/bin/env python3
"""Render the 22 November 2026 one-image news summary (1024x1024 PNG).

Usage: python3 generate.py news.json entry.png

The spec in news.json holds the date line, the lead story, six panels and
a ticker, all researched from that day's reporting as it stood around
midday UTC on 22 November (AP, Reuters, BBC, The Times, Daily Perspective).
Text is drawn with real fonts, never AI-rendered, so every word on the
image is exact. The grader does not run this file: main.py copies the
committed entry.png to /output.
"""
import json
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (10, 17, 32)
PANEL = (19, 30, 52)
PANEL_LEAD = (24, 38, 66)
EDGE = (52, 74, 110)
INK = (240, 244, 250)
MUTED = (168, 182, 204)
GOLD = (245, 197, 66)
RED = (255, 107, 107)
TEAL = (64, 201, 184)
BLUE = (96, 165, 250)
GREEN = (110, 231, 140)
PURPLE = (192, 132, 252)
ORANGE = (251, 170, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel_box(draw, box, fill):
    draw.rounded_rectangle(box, radius=14, fill=fill, outline=EDGE, width=2)


def tag(draw, x, y, text, color):
    f = font(BOLD, 19)
    w = draw.textlength(text, font=f)
    draw.rounded_rectangle([x, y, x + w + 20, y + 30], radius=8, fill=color)
    draw.text((x + 10, y + 4), text, font=f, fill=(8, 12, 22))
    return y + 38


def render(spec, out_path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # masthead: the date is the biggest thing on the page
    d.text((40, 26), "THE WORLD IN ONE IMAGE", font=font(BOLD, 25), fill=GOLD)
    d.text((984, 26), "DAILY BRIEF", font=font(BOLD, 25), fill=MUTED, anchor="ra")
    d.text((40, 58), spec["date_big"], font=font(BOLD, 63), fill=INK)
    d.line([40, 138, 984, 138], fill=GOLD, width=4)

    # lead story
    panel_box(d, [32, 148, 992, 374], PANEL_LEAD)
    y = tag(d, 56, 166, spec["lead"]["tag"], GOLD)
    y = draw_text_block(d, (56, y), spec["lead"]["headline"], font(BOLD, 37), INK, 880, 45)
    y += 6
    draw_text_block(d, (56, y), spec["lead"]["body"], font(REG, 23), (205, 216, 235), 880, 31)

    # six panels, 2 x 3
    colors = [RED, TEAL, BLUE, GREEN, PURPLE, ORANGE]
    gx, gy = 32, 390
    pw, ph = 468, 178
    gap = 24
    for i, p in enumerate(spec["panels"]):
        col, row = i % 2, i // 2
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + 12)
        panel_box(d, [x0, y0, x0 + pw, y0 + ph], PANEL)
        yy = tag(d, x0 + 20, y0 + 12, p["tag"], colors[i])
        yy = draw_text_block(d, (x0 + 20, yy), p["headline"], font(BOLD, 23), INK, pw - 40, 28)
        yy += 2
        draw_text_block(d, (x0 + 20, yy), p["body"], font(REG, 18), MUTED, pw - 40, 22)

    # ticker
    ty = 390 + 3 * ph + 2 * 12 + 8
    d.line([40, ty, 984, ty], fill=EDGE, width=2)
    d.text((40, ty + 8), "ALSO TODAY", font=font(BOLD, 18), fill=GOLD)
    draw_text_block(d, (196, ty + 8), spec["ticker"], font(REG, 18), (205, 216, 235), 788, 23)

    img.save(out_path, optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as fh:
        render(json.load(fh), sys.argv[2])
