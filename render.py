"""Offline artwork generator for the 25 November 2026 world news poster.

Only this build tool needs Pillow. The graded main.py copies the PNG produced
here and imports nothing beyond the standard library. Regenerate with:
python render.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
PAPER = (248, 244, 234)
INK = (16, 39, 56)
CRIMSON = (190, 55, 46)
OCEAN = (20, 103, 110)
SUN = (226, 168, 60)
STONE = (104, 118, 129)
WHITE = (255, 255, 255)
STEEL = (139, 152, 160)

BOLD = (
    r"C:\Windows\Fonts\arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)
DISPLAY = (
    r"C:\Windows\Fonts\Anton-Regular.ttf",
    r"C:\Windows\Fonts\impact.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)


def face(names, points):
    for name in names:
        try:
            return ImageFont.truetype(name, points)
        except OSError:
            continue
    return ImageFont.load_default()


def fit(draw, words, names, points, room):
    size = points
    while size > 13:
        f = face(names, size)
        if draw.textlength(words, font=f) <= room:
            return f
        size -= 2
    return face(names, 13)


def centred(draw, y, words, f, colour, left, right):
    width = draw.textlength(words, font=f)
    draw.text(((left + right - width) / 2, y), words, font=f, fill=colour)


def mine(d, cx, cy, colour):
    for angle in range(0, 360, 45):
        import math
        dx = math.cos(math.radians(angle)) * 17
        dy = math.sin(math.radians(angle)) * 17
        d.line((cx, cy, cx + dx, cy + dy), fill=colour, width=6)
    d.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), fill=colour)


def icon_iran(d, b):
    x, y, xr, _ = b
    for yy in (y + 172, y + 188):
        d.arc((x + 4, yy - 24, xr - 4, yy + 16), 0, 180, fill=OCEAN, width=5)
    d.polygon([(x + 22, y + 146), (xr - 18, y + 146),
               (xr - 34, y + 172), (x + 38, y + 172)], fill=INK)
    for i in range(3):
        cx = x + 50 + i * 46
        d.rectangle((cx, y + 108, cx + 40, y + 144), fill=OCEAN if i != 1 else CRIMSON,
                    outline=INK, width=3)
    d.polygon([(x + 78, y + 108), (x + 62, y + 74), (x + 84, y + 86),
               (x + 96, y + 48), (x + 112, y + 84), (x + 134, y + 70),
               (x + 116, y + 108)], fill=SUN)
    d.polygon([(x + 88, y + 104), (x + 78, y + 82), (x + 100, y + 92),
               (x + 104, y + 68), (x + 114, y + 104)], fill=CRIMSON)
    mine(d, x + 36, y + 184, INK)


def icon_tariffs(d, b):
    x, y, xr, _ = b
    d.polygon([(x + 16, y + 158), (xr - 12, y + 158),
               (xr - 30, y + 184), (x + 34, y + 184)], fill=INK)
    palette = (CRIMSON, OCEAN, SUN, STEEL)
    for i in range(4):
        cx = x + 28 + i * 44
        d.rectangle((cx, y + 92 + (i % 2) * 24, cx + 40, y + 116 + (i % 2) * 24),
                    fill=palette[i], outline=INK, width=3)
    d.polygon([(x + 20, y + 72), (xr - 20, y + 50), (xr - 20, y + 86),
               (x + 20, y + 108)], fill=WHITE, outline=CRIMSON, width=5)
    d.line((xr - 48, y + 118, xr - 48, y + 160), fill=CRIMSON, width=12)
    d.polygon([(xr - 62, y + 148), (xr - 48, y + 176), (xr - 34, y + 148)],
              fill=CRIMSON)


def icon_markets(d, b):
    x, y, xr, _ = b
    d.rounded_rectangle((x + 26, y + 42, x + 116, y + 132), radius=7,
                        fill=WHITE, outline=INK, width=5)
    for i in range(3):
        for j in range(3):
            d.ellipse((x + 42 + i * 22, y + 58 + j * 22,
                       x + 50 + i * 22, y + 66 + j * 22), fill=STEEL)
    for k in range(4):
        d.line((x + 36 + k * 20, y + 36, x + 36 + k * 20, y + 42), fill=INK, width=5)
        d.line((x + 36 + k * 20, y + 132, x + 36 + k * 20, y + 138), fill=INK, width=5)
    points = [(x + 36, y + 86), (x + 62, y + 76), (x + 88, y + 96),
              (x + 112, y + 92), (xr - 18, y + 156)]
    d.line(points, fill=CRIMSON, width=11, joint="curve")
    for px, py in points[:-1]:
        d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=CRIMSON)


def icon_energy(d, b):
    x, y, xr, _ = b
    d.polygon([(x + 14, y + 92), (x + 78, y + 38), (x + 142, y + 92)], fill=INK)
    d.rectangle((x + 26, y + 92, x + 130, y + 168), fill=WHITE, outline=INK, width=5)
    d.rectangle((x + 62, y + 112, x + 104, y + 152), fill=SUN, outline=INK, width=4)
    d.line((x + 76, y + 122, x + 66, y + 136, x + 82, y + 136, x + 72, y + 148),
           fill=CRIMSON, width=5)
    for i, h in enumerate((20, 38, 58)):
        bx = x + 148 + i * 21
        d.rectangle((bx, y + 168 - h, bx + 16, y + 168), fill=CRIMSON,
                    outline=INK, width=2)
    d.line((x + 142, y + 172, xr - 8, y + 172), fill=INK, width=5)


def icon_ukraine(d, b):
    x, y, xr, _ = b
    for i, h in enumerate((44, 70, 52)):
        bx = x + 14 + i * 52
        d.rectangle((bx, y + 160 - h, bx + 44, y + 160), fill=STEEL, outline=INK, width=3)
        d.rectangle((bx + 8, y + 174 - h, bx + 19, y + 186 - h), fill=WHITE)
    d.line((x + 24, y + 116, x + 78, y + 88), fill=INK, width=6)
    d.line((x + 120, y + 88, xr - 14, y + 116), fill=INK, width=6)
    d.polygon([(x + 92, y + 24), (x + 66, y + 96), (x + 90, y + 96),
               (x + 78, y + 152), (x + 126, y + 78), (x + 102, y + 78)], fill=SUN)
    d.line((x + 116, y + 160, xr - 10, y + 160), fill=INK, width=5)


def icon_space(d, b):
    x, y, xr, _ = b
    d.rounded_rectangle((xr - 96, y + 40, xr - 40, y + 76), radius=6,
                        fill=STEEL, outline=INK, width=4)
    d.rectangle((xr - 128, y + 48, xr - 100, y + 68), fill=OCEAN, outline=INK, width=3)
    d.rectangle((xr - 36, y + 48, xr - 8, y + 68), fill=OCEAN, outline=INK, width=3)
    d.polygon([(x + 74, y + 18), (x + 108, y + 74), (x + 108, y + 132),
               (x + 74, y + 158), (x + 40, y + 132), (x + 40, y + 74)],
              fill=WHITE, outline=INK, width=4)
    d.polygon([(x + 74, y + 18), (x + 90, y + 48), (x + 58, y + 48)], fill=CRIMSON)
    d.ellipse((x + 62, y + 70, x + 86, y + 94), fill=OCEAN, outline=INK, width=3)
    d.polygon([(x + 40, y + 122), (x + 14, y + 158), (x + 40, y + 150)], fill=CRIMSON)
    d.polygon([(x + 108, y + 122), (x + 134, y + 158), (x + 108, y + 150)], fill=CRIMSON)
    d.ellipse((x + 132, y + 116, x + 186, y + 170), fill=(46, 125, 79), outline=INK, width=3)
    d.ellipse((x + 154, y + 128, x + 166, y + 140), fill=WHITE)


def icon_sudan(d, b):
    x, y, xr, _ = b
    d.rectangle((x + 8, y + 176, xr - 8, y + 192), fill=(205, 174, 126))
    cx, cy = x + 72, y + 76
    for dx, dy in ((-46, -26), (46, -26), (-46, 26), (46, 26)):
        d.line((cx, cy, cx + dx, cy + dy), fill=INK, width=7)
        d.ellipse((cx + dx - 23, cy + dy - 7, cx + dx + 23, cy + dy + 7),
                  outline=INK, width=5)
    d.ellipse((cx - 25, cy - 16, cx + 25, cy + 16), fill=OCEAN, outline=INK, width=4)
    d.rectangle((cx - 6, cy + 16, cx + 6, cy + 58), fill=CRIMSON)
    for r in (18, 36):
        d.arc((xr - 70 - r, y + 134 - r, xr - 70 + r, y + 134 + r), 0, 360,
              fill=CRIMSON, width=6)
    d.line((xr - 70, y + 134, xr - 70, y + 134), fill=CRIMSON, width=7)


def icon_colombia(d, b):
    x, y, xr, _ = b
    d.rectangle((x + 12, y + 70, xr - 12, y + 166), fill=(230, 237, 241),
                outline=INK, width=4)
    d.polygon([(x + 8, y + 70), (xr - 8, y + 70), (xr - 26, y + 48),
               (x + 26, y + 48)], fill=WHITE, outline=INK, width=4)
    d.rectangle((x + 82, y + 96, x + 138, y + 166), fill=WHITE, outline=INK, width=3)
    for px in (x + 42, xr - 40):
        d.ellipse((px - 12, y + 112, px + 12, y + 136), fill=SUN, outline=INK, width=3)
        d.rectangle((px - 10, y + 136, px + 10, y + 166), fill=OCEAN)
    for i, colour in enumerate((CRIMSON, SUN, (44, 84, 176))):
        d.rectangle((x + 30 + i * 56, y + 30, x + 78 + i * 56, y + 42), fill=colour)
    d.arc((x + 132, y + 128, x + 182, y + 170), 200, 340, fill=CRIMSON, width=7)
    d.line((x + 138, y + 142, x + 128, y + 128), fill=CRIMSON, width=7)


CARDS = [
    ("IRAN WAR", "TANKER HIT BY MINE", icon_iran, CRIMSON, (250, 232, 228)),
    ("US TARIFF PLAN", "CHINA AND EU NAMED", icon_tariffs, OCEAN, (229, 240, 241)),
    ("AI SELL-OFF", "ASIA MARKETS DIVE", icon_markets, CRIMSON, (249, 235, 231)),
    ("UK ENERGY", "BILLS +26% IN JAN", icon_energy, OCEAN, (252, 240, 219)),
    ("UKRAINE", "5 DEAD, POWER CUT", icon_ukraine, CRIMSON, (231, 238, 244)),
    ("SHENZHOU-24", "PAKISTAN IN ORBIT", icon_space, OCEAN, (229, 240, 240)),
    ("SUDAN DRONES", "AT LEAST 19 DEAD", icon_sudan, CRIMSON, (251, 238, 226)),
    ("COLOMBIA", "HOSTAGES FREED", icon_colombia, OCEAN, (232, 241, 245)),
]


def card(draw, x, y, w, h, entry):
    headline, detail, pictogram, colour, tint = entry
    draw.rounded_rectangle((x, y, x + w, y + h), radius=12,
                           fill=WHITE, outline=INK, width=3)
    panel = (x + 8, y + 8, x + w - 8, y + 214)
    draw.rounded_rectangle(panel, radius=8, fill=tint)
    pictogram(draw, panel)
    band = (x + 8, y + 222, x + w - 8, y + h - 8)
    draw.rounded_rectangle(band, radius=7, fill=INK)
    top = fit(draw, headline, BOLD, 29, w - 28)
    bottom = fit(draw, detail, BOLD, 24, w - 28)
    centred(draw, y + 246, headline, top, WHITE, x + 8, x + w - 8)
    centred(draw, y + 294, detail, bottom, (219, 231, 239), x + 8, x + w - 8)


def poster():
    picture = Image.new("RGB", (SIDE, SIDE), PAPER)
    d = ImageDraw.Draw(picture)
    d.rectangle((0, 0, SIDE, 10), fill=CRIMSON)
    d.text((28, 18), "WEDNESDAY  /  WORLD NEWS", font=face(BOLD, 27), fill=OCEAN)
    date = "25 NOVEMBER 2026"
    d.text((26, 48), date, font=fit(d, date, DISPLAY, 98, SIDE - 52), fill=INK)
    d.rectangle((28, 168, SIDE - 28, 173), fill=CRIMSON)
    d.text((28, 180), "IRAN WAR LEADS A DAY OF MARKETS AND TARIFFS",
           font=fit(d, "IRAN WAR LEADS A DAY OF MARKETS AND TARIFFS", BOLD, 23, SIDE - 56),
           fill=STONE)

    margin, gutter = 26, 12
    w = (SIDE - 2 * margin - 3 * gutter) // 4
    h = 352
    for index, entry in enumerate(CARDS):
        col, row = index % 4, index // 4
        card(d, margin + col * (w + gutter), 212 + row * (h + gutter), w, h, entry)

    d.line((28, 944, SIDE - 28, 944), fill=STONE, width=2)
    d.text((28, 952), "REPORTS FILED 25 NOV 2026  /  BBC  /  AL JAZEERA  /  REUTERS",
           font=fit(d, "REPORTS FILED 25 NOV 2026  /  BBC  /  AL JAZEERA  /  REUTERS",
                    BOLD, 20, SIDE - 56), fill=INK)
    return picture


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "entry.png"
    poster().save(target, optimize=True)
    print("wrote", target, target.stat().st_size, "bytes")
