#!/usr/bin/env python3
"""Draw the news-image entry for make.fun: a one-page newspaper summing up
the world news of Wednesday 25 November 2026. 35 verified stories: 3 leads
with drawn illustrations, 8 secondaries with drawn illustrations, 24
numbered briefs, a UTC timeline, a region bar and a DATE CHECK box naming
the excluded stories from 24, 23 and 22 November.

Output: entry.png in this directory (PNG, at most 1 MiB, 1024x1024).
Run: python3 main.py
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 233)
INK = (24, 22, 18)
NAVY = (30, 58, 95)
RED = (176, 32, 32)
GOLD = (200, 150, 40)
MUTED = (110, 105, 95)
LINE = (200, 192, 172)
WHITE = (255, 255, 255)
BLUE = (43, 108, 176)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
_cache = {}


def font(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONT_DIR + name, size)
    return _cache[key]


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

REGION_COLORS = {
    "ASIA": (190, 90, 30), "EUROPE": (43, 108, 176), "AMERICAS": (60, 140, 90),
    "AFRICA": (150, 110, 30), "MIDDLE EAST": (150, 60, 120), "OCEANIA": (60, 130, 150),
    "GLOBAL": (120, 60, 160),
}

# (region, topic, headline, summary, source)
LEADS = [
    ("AFRICA", "DISASTER", "Fuel tanker blast kills 31 on Cairo ring road",
     "Tanker overturns and explodes above a tunnel in Giza, torching 27 vehicles; 21 injured.",
     "REUTERS \u00b7 AP"),
    ("MIDDLE EAST", "HORMUZ", "Iran says tankers hit mines in Hormuz",
     "IRGC claims oil tankers struck naval mines and caught fire; the US military disputes the claim.",
     "REUTERS"),
    ("ASIA", "SPACE", "China launches Pakistan's first astronaut",
     "Shenzhou-24 lifts off with Muhammad Zeeshan Ali, the first Pakistani in space, bound for China's station.",
     "REUTERS \u00b7 XINHUA"),
]

SECONDARIES = [
    ("MIDDLE EAST", "GULF", "Houthis claim strike on Saudi refinery",
     "Houthis say they hit Ras Tanura; oil climbs.", "REUTERS"),
    ("MIDDLE EAST", "GAZA", "Israel kills Hamas security chief in Gaza",
     "Abuelouf killed with wife and two children.", "AP"),
    ("EUROPE", "UKRAINE", "Russian strike kills two in Odesa region",
     "Missiles hit Odesa and Kyiv; child hurt.", "AP"),
    ("AFRICA", "SUDAN", "RSF drone strikes kill 19 civilians",
     "Drones hit two cities; 20 more wounded.", "AP"),
    ("OCEANIA", "PACIFIC", "Solomons sign pact barring foreign bases",
     "Solomons, Australia sign pact barring bases.", "AP"),
    ("AMERICAS", "TECH", "Nvidia brings back Huang as chief",
     "Huang returns as CEO; AI shares slide.", "REUTERS"),
    ("AMERICAS", "TRADE", "US unveils tariffs on 14 partners",
     "Rates of 20-40% proposed; hearing 25 January.", "REUTERS"),
    ("EUROPE", "FOOTBALL", "Lille stun Bayern as Liverpool cruise",
     "Lille end Bayern's run 2-1; Liverpool win 3-0.", "UEFA"),
]

BRIEFS = [
    ("Vatican", "Pope Leo decries COP31 failure"),
    ("New York", "S&P falls 2.2% in AI sell-off"),
    ("Washington", "CIA, ODNI hit by cyber breach"),
    ("Iowa", "Army destroys 5t of old explosives"),
    ("Dhaka", "Garment wage up 36% to $139"),
    ("Madrid", "Sanchez, Feijoo spar in TV debate"),
    ("Geneva", "30+ nations urge Russia to halt chem arms"),
    ("Phnom Penh", "China, Cambodia open drills"),
    ("Budapest", "Hungary, Ukraine make fresh start"),
    ("Turin", "Sinner has knee surgery, out long-term"),
    ("Los Angeles", "Doncic 28 as Lakers beat Jazz"),
    ("Hong Kong", "Fire survivors mourn, one year on"),
    ("Riyadh", "Coalition condemns tower strike"),
    ("Washington", "US: Beijing did not direct Alice Huang"),
    ("Beijing", "Huang linked to Chinese spy official"),
    ("The Hague", "Wang Yi urges Dutch to guard trade ties"),
    ("London", "Wang Yi urges Britain to back free trade"),
    ("Taipei", "Comedian gets guards over China jokes"),
    ("London", "UK watchdog warns on AI as Meta ships Muse"),
    ("Singapore", "Airports court private cash for upgrades"),
    ("London", "Museum to reopen in Victorian market"),
    ("Tokyo", "Data centre boom faces resident revolt"),
    ("Ottawa", "Student curbs test Carney talent push"),
    ("Baku", "Gordon double as Barcelona win 4-1"),
]

BRIEF_REGIONS = [
    "GLOBAL", "AMERICAS", "AMERICAS", "AMERICAS",
    "ASIA", "EUROPE", "GLOBAL", "ASIA",
    "EUROPE", "EUROPE", "AMERICAS", "ASIA",
    "MIDDLE EAST", "AMERICAS", "ASIA", "EUROPE",
    "EUROPE", "ASIA", "EUROPE", "GLOBAL",
    "EUROPE", "ASIA", "AMERICAS", "EUROPE",
]

TIMELINE = [
    ("OVERNIGHT", "Houthis claim refinery hit"),
    ("MORNING", "Shenzhou-24 lifts off"),
    ("MIDDAY", "US unveils tariffs"),
    ("AFTERNOON", "Wall Street slides"),
    ("16:08 UTC", "Cairo tanker blast"),
    ("EVENING", "Lille stun Bayern"),
    ("NIGHT", "Barcelona win 4-1"),
    ("LATE", "IRGC claims Hormuz mines"),
]


def region_counts():
    counts = {}
    for region, *_ in LEADS + SECONDARIES:
        counts[region] = counts.get(region, 0) + 1
    for r in BRIEF_REGIONS:
        counts[r] = counts.get(r, 0) + 1
    return counts


def text_block(draw, x, y, text, fnt, fill, max_w, line_h, max_lines):
    """Draw wrapped text, return the y just below the last line."""
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=1000) or [""])
    wrapped = []
    for ln in lines:
        while draw.textlength(ln, font=fnt) > max_w and len(ln) > 1:
            cut = len(ln) - 1
            while cut > 0 and draw.textlength(ln[:cut], font=fnt) > max_w:
                cut -= 1
            while cut > 0 and ln[cut] != " ":
                cut -= 1
            wrapped.append(ln[:cut].rstrip())
            ln = ln[cut:].strip()
        wrapped.append(ln)
    wrapped = wrapped[:max_lines]
    for i, ln in enumerate(wrapped):
        draw.text((x, y + i * line_h), ln, font=fnt, fill=fill)
    return y + len(wrapped) * line_h


# ---------- illustrations (all drawn in code) ----------

def illo_cairo(draw, x, y, w, h):
    # night highway in Giza: dark sky, ring road, overturned tanker, fire, smoke
    draw.rectangle([x, y, x + w, y + h], fill=(25, 22, 35))
    for sx, sy in [(30, 14), (90, 8), (160, 18), (230, 10), (290, 16)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(200, 200, 220))
    # road
    draw.rectangle([x, y + 78, x + w, y + h], fill=(70, 68, 72))
    for lx in range(0, w, 34):
        draw.rectangle([x + lx, y + 96, x + lx + 18, y + 100], fill=(255, 230, 100))
    # overturned tanker (on its side)
    draw.rectangle([x + 60, y + 62, x + 200, y + 84], fill=(180, 170, 150))
    draw.ellipse([x + 60, y + 62, x + 82, y + 84], fill=(150, 140, 120))
    for wx in (80, 120, 165):
        draw.ellipse([x + wx, y + 84, x + wx + 12, y + 96], fill=(30, 30, 30))
    # flames
    for fx, fh in [(80, 34), (120, 46), (165, 38), (205, 28)]:
        draw.polygon([(x + fx, y + 62), (x + fx + 12, y + 62 - fh),
                      (x + fx + 24, y + 62)], fill=(255, 150, 30))
        draw.polygon([(x + fx + 6, y + 62), (x + fx + 12, y + 62 - fh + 16),
                      (x + fx + 18, y + 62)], fill=(255, 220, 120))
    # smoke
    for sx, sy, r in [(130, 12, 12), (160, 6, 14), (190, 12, 10)]:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(80, 80, 90))
    # burnt cars
    for cx in (230, 275):
        draw.rectangle([x + cx, y + h - 26, x + cx + 40, y + h - 12], fill=(40, 40, 45))
    draw.rectangle([x + 8, y + 6, x + 150, y + 24], fill=RED)
    draw.text((x + 12, y + 8), "31 KILLED \u00b7 21 INJURED", font=font(SANS_B, 9), fill=WHITE)
    draw.text((x + 8, y + h - 18), "GIZA \u00b7 RING ROAD FIRE", font=font(SANS_B, 9), fill=WHITE)


def illo_hormuz(draw, x, y, w, h):
    # Strait of Hormuz at dusk: sea, two tankers, mine blasts, smoke
    draw.rectangle([x, y, x + w, y + h], fill=(200, 120, 60))
    draw.ellipse([x + w - 60, y + 8, x + w - 20, y + 48], fill=(255, 220, 150))
    draw.rectangle([x, y + h - 40, x + w, y + h], fill=(30, 70, 110))
    for wx in range(0, w, 42):
        draw.arc([x + wx, y + h - 34, x + wx + 32, y + h - 18], start=180, end=360,
                 fill=(150, 190, 220), width=2)
    # two tankers
    for tx in (30, 180):
        draw.rectangle([x + tx, y + h - 62, x + tx + 110, y + h - 40], fill=(140, 40, 35))
        draw.rectangle([x + tx + 80, y + h - 76, x + tx + 100, y + h - 62], fill=(210, 210, 210))
        draw.rectangle([x + tx, y + h - 62, x + tx + 110, y + h - 56], fill=(200, 200, 200))
    # mine blasts on the first tanker
    for ex, ey, r in [(60, h - 62, 14), (95, h - 66, 11)]:
        draw.ellipse([x + ex - r, y + ey - r, x + ex + r, y + ey + r], fill=(255, 150, 40))
        draw.ellipse([x + ex - r // 2, y + ey - r // 2, x + ex + r // 2, y + ey + r // 2],
                     fill=(255, 230, 150))
    for sx, sy, r in [(75, 22, 12), (105, 14, 14), (135, 22, 10)]:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(70, 70, 80))
    draw.rectangle([x + 8, y + 6, x + 170, y + 24], fill=RED)
    draw.text((x + 12, y + 8), "IRGC: MINES HIT TANKERS", font=font(SANS_B, 9), fill=WHITE)
    draw.text((x + 8, y + h - 18), "STRAIT OF HORMUZ \u00b7 US DISPUTES IT", font=font(SANS_B, 9), fill=WHITE)


def illo_shenzhou(draw, x, y, w, h):
    # rocket launch at dawn: blue sky, stars, rising rocket, exhaust, launch tower
    draw.rectangle([x, y, x + w, y + h], fill=(30, 60, 120))
    for sx, sy in [(40, 12), (120, 20), (200, 10), (280, 18), (320, 30)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(220, 220, 240))
    # launch tower
    draw.rectangle([x + 200, y + 20, x + 214, y + h - 10], fill=(90, 90, 100))
    for gy in range(30, h - 20, 16):
        draw.line([(x + 200, y + gy), (x + 214, y + gy + 10)], fill=(60, 60, 70), width=2)
    # rocket
    draw.polygon([(x + 120, y + 14), (x + 132, y + 30), (x + 108, y + 30)], fill=RED)
    draw.rectangle([x + 108, y + 30, x + 132, y + 78], fill=WHITE)
    draw.rectangle([x + 108, y + 52, x + 132, y + 62], fill=RED)
    draw.polygon([(x + 100, y + 78), (x + 108, y + 62), (x + 108, y + 78)], fill=RED)
    draw.polygon([(x + 132, y + 78), (x + 132, y + 62), (x + 140, y + 78)], fill=RED)
    # exhaust flame and smoke
    draw.polygon([(x + 108, y + 78), (x + 120, y + 108), (x + 132, y + 78)], fill=(255, 180, 60))
    for sx, sy, r in [(90, 100, 12), (120, 110, 14), (150, 100, 11)]:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(200, 200, 210))
    draw.text((x + 8, y + 6), "SHENZHOU-24", font=font(SANS_B, 11), fill=WHITE)
    draw.rectangle([x + 8, y + h - 18, x + 215, y + h - 4], fill=(20, 40, 80))
    draw.text((x + 12, y + h - 16), "PAKISTAN'S FIRST ASTRONAUT", font=font(SANS_B, 10), fill=GOLD)


def illo_refinery(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(50, 50, 70))
    # refinery towers
    for tx in (16, 66, 116):
        draw.polygon([(x + tx, y + h - 6), (x + tx + 8, y + 18), (x + tx + 28, y + 18),
                      (x + tx + 36, y + h - 6)], fill=(160, 160, 170))
        draw.ellipse([x + tx + 8, y + 14, x + tx + 28, y + 22], fill=(130, 130, 140))
    # flame on the third tower (right side, clear of the top label)
    draw.polygon([(x + 168, y + 18), (x + 176, y + 2), (x + 184, y + 18)], fill=(255, 150, 30))
    # smoke
    for sx, sy, r in [(212, 12, 10), (232, 8, 11)]:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(90, 90, 100))
    draw.text((x + 8, y + 4), "RAS TANURA HIT", font=font(SANS_B, 14), fill=WHITE)
    draw.text((x + 150, y + h - 16), "OIL UP", font=font(SANS_B, 9), fill=GOLD)


def illo_gaza(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(150, 130, 110))
    # city skyline
    for bx, bw, bh in [(10, 40, 30), (60, 34, 44), (104, 44, 26), (158, 36, 38), (204, 30, 32)]:
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(90, 80, 70))
    # smoke column
    for sx, sy, r in [(120, 8, 10), (135, 16, 12), (150, 6, 9)]:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(80, 80, 85))
    draw.text((x + 8, y + 4), "ABUELOUF KILLED", font=font(SANS_B, 13), fill=WHITE)
    draw.text((x + 8, y + h - 16), "GAZA \u00b7 FAMILY ALSO DEAD", font=font(SANS_B, 9), fill=(255, 220, 200))


def illo_odesa(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(40, 55, 85))
    # apartment blocks
    for bx, bw, bh in [(14, 50, 34), (74, 44, 44), (128, 54, 30), (192, 40, 40)]:
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(120, 120, 135))
        for wy in range(h - bh + 6, h - 4, 10):
            for wx in range(bx + 6, bx + bw - 6, 12):
                draw.rectangle([x + wx, y + wy, x + wx + 5, y + wy + 5], fill=(255, 220, 130))
    # explosion flash on the second block (low, clear of the top label)
    draw.ellipse([x + 82, y + 20, x + 112, y + 46], fill=(255, 150, 40))
    draw.ellipse([x + 90, y + 27, x + 104, y + 40], fill=(255, 230, 150))
    draw.text((x + 8, y + 4), "2 KILLED \u00b7 CHILD HURT", font=font(SANS_B, 12), fill=WHITE)
    draw.text((x + 8, y + h - 16), "ODESA \u00b7 KYIV", font=font(SANS_B, 9), fill=(200, 210, 230))


def illo_sudan(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(210, 180, 130))
    draw.rectangle([x, y, x + w, y + 26], fill=(180, 200, 230))
    draw.ellipse([x + 200, y + 4, x + 226, y + 30], fill=(255, 240, 180))
    # dunes
    draw.polygon([(x, y + h), (x + 90, y + 34), (x + 180, y + h)], fill=(190, 160, 110))
    draw.polygon([(x + 140, y + h), (x + 210, y + 40), (x + w, y + h)], fill=(180, 150, 100))
    # drone silhouette (right side, clear of the top label)
    draw.ellipse([x + 168, y + 24, x + 200, y + 34], fill=(40, 40, 45))
    draw.line([(x + 160, y + 26), (x + 208, y + 26)], fill=(40, 40, 45), width=2)
    draw.ellipse([x + 156, y + 22, x + 164, y + 30], fill=(40, 40, 45))
    draw.ellipse([x + 204, y + 22, x + 212, y + 30], fill=(40, 40, 45))
    # dust clouds
    for dx, dy, r in [(60, 44, 9), (80, 48, 11), (170, 46, 10)]:
        draw.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=(160, 140, 110))
    draw.text((x + 8, y + 4), "19 CIVILIANS DEAD", font=font(SANS_B, 12), fill=INK)
    draw.text((x + 8, y + h - 16), "RSF DRONES \u00b7 TWO CITIES", font=font(SANS_B, 9), fill=(90, 70, 50))


def illo_solomons(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(60, 140, 180))
    draw.rectangle([x, y + h - 18, x + w, y + h], fill=(30, 110, 160))
    # island
    draw.ellipse([x + 20, y + h - 30, x + 150, y + h - 6], fill=(90, 160, 90))
    # palm (low, fronds stay clear of the top label)
    draw.line([(x + 70, y + h - 28), (x + 70, y + 30)], fill=(120, 90, 50), width=4)
    for ang in (-40, -15, 10, 35):
        import math
        ex = 70 + int(16 * math.cos(math.radians(ang - 90)))
        ey = 30 + int(16 * math.sin(math.radians(ang - 90)))
        draw.line([(x + 70, y + 30), (x + ex, y + ey)], fill=(40, 120, 60), width=3)
    # treaty document
    draw.rectangle([x + 160, y + 8, x + 220, y + 44], fill=WHITE)
    draw.line([(x + 166, y + 16), (x + 214, y + 16)], fill=INK, width=1)
    draw.line([(x + 166, y + 24), (x + 214, y + 24)], fill=INK, width=1)
    draw.line([(x + 166, y + 32), (x + 196, y + 32)], fill=INK, width=1)
    draw.ellipse([x + 204, y + 34, x + 214, y + 44], fill=RED)
    # waves
    for wx in range(0, w, 30):
        draw.arc([x + wx, y + h - 14, x + wx + 24, y + h - 4], start=180, end=360,
                 fill=(200, 230, 250), width=2)
    draw.text((x + 8, y + 4), "NO FOREIGN BASES", font=font(SANS_B, 13), fill=WHITE)
    draw.text((x + 160, y + h - 16), "PACIFIC PACT", font=font(SANS_B, 9), fill=(200, 230, 250))


def illo_nvidia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(20, 40, 30))
    # chip (right side, clear of the top label)
    draw.rectangle([x + 150, y + 6, x + 230, y + 40], fill=(40, 160, 80))
    draw.rectangle([x + 164, y + 14, x + 216, y + 32], fill=(20, 90, 50))
    draw.text((x + 168, y + 18), "NVDA", font=font(SANS_B, 11), fill=WHITE)
    for px in range(158, 224, 14):
        draw.line([(x + px, y + 2), (x + px, y + 6)], fill=(120, 200, 150), width=2)
        draw.line([(x + px, y + 40), (x + px, y + 44)], fill=(120, 200, 150), width=2)
    # falling chart line (left of the chip)
    pts = [(10, 22), (40, 28), (70, 24), (100, 36), (130, 32), (145, 44)]
    draw.line([(x + px, y + py) for px, py in pts], fill=(255, 100, 100), width=3)
    draw.text((x + 8, y + 4), "HUANG IS BACK", font=font(SANS_B, 13), fill=WHITE)
    draw.text((x + 8, y + h - 16), "SHARES SLIDE", font=font(SANS_B, 9), fill=(170, 230, 190))


def illo_tariffs(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(120, 140, 170))
    # cranes (below the top label)
    for cx in (30, 130):
        draw.line([(x + cx, y + 20), (x + cx, y + h - 8)], fill=(60, 60, 70), width=4)
        draw.line([(x + cx, y + 20), (x + cx + 60, y + 30)], fill=(60, 60, 70), width=3)
    # containers
    for cx, cy, cc in [(20, 26, (200, 60, 40)), (70, 26, (40, 120, 180)), (120, 26, (60, 160, 80)),
                       (170, 26, (200, 150, 40)), (45, 38, (180, 140, 60)), (145, 38, (150, 60, 120))]:
        draw.rectangle([x + cx, y + cy, x + cx + 44, y + cy + 11], fill=cc)
    draw.text((x + 8, y + 4), "20-40% TARIFFS", font=font(SANS_B, 13), fill=WHITE)
    draw.rectangle([x, y + h - 16, x + w, y + h], fill=(40, 50, 70))
    draw.text((x + 8, y + h - 14), "14 PARTNERS \u00b7 HEARING 25 JAN", font=font(SANS_B, 9), fill=WHITE)


def illo_football(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(20, 100, 50))
    # pitch lines
    draw.rectangle([x + 8, y + 8, x + w - 8, y + h - 8], outline=WHITE, width=1)
    draw.line([(x + w // 2, y + 8), (x + w // 2, y + h - 8)], fill=WHITE, width=1)
    draw.ellipse([x + w // 2 - 10, y + h // 2 - 10, x + w // 2 + 10, y + h // 2 + 10],
                 outline=WHITE, width=1)
    # ball
    draw.ellipse([x + 30, y + 14, x + 52, y + 36], fill=WHITE)
    draw.polygon([(x + 41, y + 20), (x + 46, y + 25), (x + 41, y + 30), (x + 36, y + 25)],
                 fill=INK)
    draw.text((x + 66, y + 6), "LILLE 2-1 BAYERN", font=font(SANS_B, 15), fill=WHITE)
    draw.text((x + 66, y + 26), "LIVERPOOL 3-0 BRUGGE", font=font(SANS_B, 10), fill=(170, 230, 190))
    draw.text((x + 66, y + h - 16), "UCL MATCHDAY 5", font=font(SANS_B, 9), fill=(170, 230, 190))


LEAD_ILLOS = [illo_cairo, illo_hormuz, illo_shenzhou]
SEC_ILLOS = [illo_refinery, illo_gaza, illo_odesa, illo_sudan,
             illo_solomons, illo_nvidia, illo_tariffs, illo_football]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((8, 6), "THE WORLD IN ONE DAY", font=font(SANS_B, 12), fill=RED)
    d.text((W - 8, 6), "WEDNESDAY'S NEWS \u00b7 ONE PAGE \u00b7 35 STORIES",
           font=font(SANS_B, 11), fill=MUTED, anchor="ra")
    d.line([(8, 26), (W - 8, 26)], fill=INK, width=2)
    d.text((8, 30), "Wednesday 25 November 2026", font=font(SERIF_B, 54), fill=INK)
    # calendar badge
    d.rectangle([W - 66, 30, W - 8, 84], outline=RED, width=2)
    d.text((W - 37, 32), "25", font=font(SANS_B, 26), fill=RED, anchor="ma")
    d.text((W - 37, 62), "NOV", font=font(SANS_B, 12), fill=RED, anchor="ma")
    d.text((8, 92), "Cairo tanker blast kills 31 \u00b7 Hormuz mines claimed \u00b7 Pakistan's first astronaut",
           font=font(SERIF, 15), fill=RED)
    d.line([(8, 116), (W - 8, 116)], fill=INK, width=2)

    # ---- region bar
    counts = region_counts()
    total = sum(counts.values())
    assert total == 35, f"story count {total} != 35"
    order = ["ASIA", "EUROPE", "AMERICAS", "AFRICA", "MIDDLE EAST", "OCEANIA", "GLOBAL"]
    x = 8
    for region in order:
        label = f"{region} {counts[region]}"
        tw = d.textlength(label, font=font(SANS_B, 10)) + 16
        d.rectangle([x, 118, x + tw, 132], fill=REGION_COLORS[region])
        d.text((x + 8, 119), label, font=font(SANS_B, 10), fill=WHITE)
        x += tw + 2

    # ---- timeline strip (two rows of four)
    d.rectangle([0, 134, W, 172], fill=(235, 230, 215))
    d.text((14, 138), "THE DAY IN UTC", font=font(SANS_B, 11), fill=RED)
    for row_i in range(2):
        tx = 130 if row_i == 0 else 14
        ty = 138 if row_i == 0 else 155
        for time, label in TIMELINE[row_i * 4:(row_i + 1) * 4]:
            d.text((tx, ty), time, font=font(SANS_B, 10), fill=RED)
            tw = d.textlength(time, font=font(SANS_B, 10))
            d.text((tx + tw + 5, ty), label, font=font(SANS, 10), fill=INK)
            tx += tw + 5 + d.textlength(label, font=font(SANS, 10)) + 22
    d.line([(0, 172), (W, 172)], fill=LINE, width=1)

    # ---- three leads
    lw = 330
    for i, (region, topic, head, summ, src) in enumerate(LEADS):
        lx = 8 + i * (lw + 4)
        ly = 176
        LEAD_ILLOS[i](d, lx, ly, lw, 120)
        d.text((lx, ly + 124), f"{i + 1}  {region} \u00b7 {topic}",
               font=font(SANS_B, 10), fill=REGION_COLORS[region])
        y = text_block(d, lx, ly + 140, head, font(SERIF_B, 20), INK, lw, 23, max_lines=2)
        text_block(d, lx, y + 2, summ, font(SANS, 12), INK, lw, 15, max_lines=2)
        d.text((lx, 460), src, font=font(SANS_B, 9), fill=MUTED)

    d.line([(8, 468), (W - 8, 468)], fill=INK, width=2)

    # ---- eight secondaries, two rows of four (124px pitch, one-line summaries)
    sw = 248
    for row in range(2):
        for col in range(4):
            i = row * 4 + col
            region, topic, head, summ, src = SECONDARIES[i]
            sx = 8 + col * (sw + 4)
            sy = 472 + row * 124
            SEC_ILLOS[i](d, sx, sy, sw, 58)
            d.text((sx, sy + 62), f"{i + 4}  {region} \u00b7 {topic}",
                   font=font(SANS_B, 9), fill=REGION_COLORS[region])
            y = text_block(d, sx, sy + 76, head, font(SERIF_B, 14), INK, sw, 16, max_lines=2)
            text_block(d, sx, y + 1, summ, font(SANS, 10), MUTED, sw, 13, max_lines=1)

    d.line([(8, 724), (W - 8, 724)], fill=INK, width=2)

    # ---- briefs
    d.text((8, 730), "ALSO ON WEDNESDAY 25 NOVEMBER", font=font(SANS_B, 12), fill=NAVY)
    bw = 330
    for col in range(3):
        bx = 8 + col * (bw + 6)
        for r in range(8):
            i = col * 8 + r
            place, brief = BRIEFS[i]
            by = 750 + r * 25
            d.text((bx, by), str(12 + i), font=font(SANS_B, 11), fill=REGION_COLORS[BRIEF_REGIONS[i]])
            d.text((bx + 24, by), f"{place}: ", font=font(SANS_B, 11), fill=INK)
            pw = d.textlength(f"{place}: ", font=font(SANS_B, 11))
            text_block(d, bx + 24 + pw, by, brief, font(SANS, 11), INK, bw - 24 - pw, 14, max_lines=1)

    # ---- date check box
    d.rectangle([8, 942, W - 8, 988], outline=RED, width=2)
    d.text((16, 946), "DATE CHECK", font=font(SANS_B, 11), fill=RED)
    dc = ("Left out: Monday 24 November: Huawei's US conviction \u00b7 the Riyadh tower strike \u00b7 "
          "Champions League day one. Sunday 23 November: the Wellington Test draw \u00b7 Spain's Puigdemont amnesty. "
          "Saturday 22 November: COP31 collapses \u00b7 the Bahrain strikes \u00b7 El Chapo Isidro captured.")
    text_block(d, 16, 962, dc, font(SANS, 10), INK, W - 32, 13, max_lines=2)

    # ---- footer
    d.text((8, 996), "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 UEFA \u00b7 USGS \u00b7 Xinhua \u00b7 Just Security",
           font=font(SANS, 9), fill=MUTED)
    d.text((W - 8, 996), "Reads at three sizes: date and leads at thumbnail size \u00b7 all stories at full size.",
           font=font(SANS, 9), fill=MUTED, anchor="ra")

    img.save("entry.png", "PNG", optimize=True)
    print(f"wrote entry.png, size {img.size}, region counts {counts}")


if __name__ == "__main__":
    main()
