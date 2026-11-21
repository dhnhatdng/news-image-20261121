"""Draw the front page for Saturday, 21 November 2026.

Renders a newspaper front page (1024x1024) from the day's verified
world news and saves it next to this file as entry.png. Uses only
Pillow and the DejaVu fonts shipped with the system. The drawing is
fully deterministic: the same run always writes the same bytes.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 239, 227)
INK = (18, 18, 18)
RED = (155, 28, 28)
GRAY = (96, 92, 84)
NAVY = (13, 25, 46)
NIGHT = (5, 8, 14)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def rule(draw, y, x0, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def burst(draw, cx, cy, outer, inner, points, fill):
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def night_panel(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    rng = random.Random(21)
    for _ in range(46):
        sx = rng.randint(x0 + 8, x1 - 8)
        sy = rng.randint(y0 + 8, y0 + 90)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(210, 215, 230))
    # moon
    draw.ellipse([x1 - 108, y0 + 22, x1 - 62, y0 + 68], fill=(235, 230, 208))
    # missile streak
    mx0, my0 = x0 + 70, y0 + 26
    mx1, my1 = x0 + 610, y0 + 118
    draw.line([(mx0, my0), (mx1, my1)], fill=(255, 196, 90), width=11)
    draw.line([(mx0, my0), (mx1, my1)], fill=(255, 244, 200), width=4)
    # explosion burst where the streak ends
    burst(draw, mx1, my1, 52, 20, 8, (255, 138, 42))
    burst(draw, mx1, my1, 30, 12, 8, (255, 196, 80))
    draw.ellipse([mx1 - 15, my1 - 15, mx1 + 15, my1 + 15], fill=(255, 226, 130))
    # rooftops along the bottom
    base = y1
    x = x0
    heights = [46, 66, 38, 78, 52, 88, 44, 70, 58, 40, 84, 48]
    i = 0
    while x < x1:
        w = 78
        h = heights[i % len(heights)]
        draw.rectangle([x, base - h, x + w, base], fill=NIGHT)
        draw.polygon([(x, base - h), (x + w // 2, base - h - 26),
                      (x + w, base - h)], fill=NIGHT)
        x += w
        i += 1


STORIES = [
    ("JUSTICE",
     "THE HAGUE VERDICT ECHOES",
     "The world reacts after the ICJ finds Myanmar guilty of genocide "
     "against the Rohingya. Myanmar calls the ruling unfair."),
    ("UNITED STATES",
     "235 MONTHS FOR PLOT",
     "A US court sentences Nikhil Gupta to 235 months over a plot to "
     "kill a Sikh separatist leader in New York."),
    ("SCIENCE",
     "A MACHINE PROVES RIEMANN?",
     "An Anthropic researcher says its Claude chatbot proved the "
     "Riemann Hypothesis. The proof now awaits scrutiny."),
    ("CLIMATE",
     "COP31: NO DEAL IN SIGHT",
     "Climate talks reach crunch time with no agreement in sight as "
     "negotiators run out of road."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 44
    right = W - m
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)

    y = 24
    d.text((W // 2, y), "THE WORLD TODAY", font=font(SERIF_B, 70),
           fill=INK, anchor="ma")
    y += 84
    d.text((W // 2, y), "SATURDAY, 21 NOVEMBER 2026",
           font=font(SANS_B, 26), fill=INK, anchor="ma")
    y += 40
    rule(d, y, m, right, 4)
    y += 8
    rule(d, y, m, right, 1)
    y += 16

    # hero
    d.text((m, y), "EUROPE  •  NATO", font=font(SANS_B, 22), fill=RED)
    y += 30
    for line in ["RUSSIAN MISSILES LAND", "IN POLAND"]:
        d.text((m, y), line, font=font(SERIF_B, 58), fill=INK)
        y += 66
    y += 6
    sub = ("Two cruise missiles and a suspected drone crash near allied "
           "drills; Warsaw calls it a deliberate provocation and NATO "
           "condemns a grave violation of Polish airspace.")
    for line in wrap(d, sub, font(SANS, 24), right - m):
        d.text((m, y), line, font=font(SANS, 24), fill=INK)
        y += 31
    y += 8
    night_panel(d, m, y, right, y + 150)
    y += 150
    y += 8
    cap = ("A Kh-101 cruise missile came down near Nowy Lipowiec, about "
           "50 km from the Ukraine border. No injuries were reported.")
    for line in wrap(d, cap, font(SERIF, 18), right - m):
        d.text((m, y), line, font=font(SERIF, 18), fill=GRAY)
        y += 22
    y += 4
    rule(d, y, m, right, 2)
    y += 12

    # supporting stories, two columns
    col_w = (right - m - 32) // 2
    cols = [m, m + col_w + 32]
    row_y = y
    for row in range(2):
        max_y = row_y
        for col in range(2):
            kicker, head, body = STORIES[row * 2 + col]
            x = cols[col]
            yy = row_y
            d.text((x, yy), kicker, font=font(SANS_B, 18), fill=RED)
            yy += 24
            for line in wrap(d, head, font(SERIF_B, 24), col_w)[:2]:
                d.text((x, yy), line, font=font(SERIF_B, 24), fill=INK)
                yy += 30
            yy += 2
            for line in wrap(d, body, font(SANS, 18), col_w)[:3]:
                d.text((x, yy), line, font=font(SANS, 18), fill=INK)
                yy += 21
            max_y = max(max_y, yy)
        row_y = max_y + 12
        if row == 0:
            rule(d, row_y - 4, m, right, 1, fill=GRAY)

    y = row_y + 2
    rule(d, y, m, right, 2)
    y += 10
    d.text((m, y), "ALSO TODAY", font=font(SANS_B, 18), fill=RED)
    y += 22
    also = ("Houthis claim strikes on Saudi Arabia  •  Mongolia's "
            "president resigns  •  Fresh arson in Bangladesh.")
    for line in wrap(d, also, font(SANS, 18), right - m):
        d.text((m, y), line, font=font(SANS, 18), fill=INK)
        y += 21
    y += 4
    rule(d, y, m, right, 1, fill=GRAY)
    y += 8
    d.text((W // 2, y), "Compiled from wire reports: AP  •  Al Jazeera  •  "
           "UN News  •  Le Monde  •  The Times",
           font=font(SANS, 15), fill=GRAY, anchor="ma")
    print("final y:", y)

    img.save("entry.png", format="PNG")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
