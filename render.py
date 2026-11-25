"""Build-time renderer for entry.png (Pillow is not needed by main.py).

Draws a dated, eight-story newspaper poster from reporting filed on
Wednesday 25 November 2026. Run once when changing the artwork.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (246, 242, 232)
NAVY = (15, 38, 58)
RED = (191, 54, 45)
TEAL = (24, 110, 111)
GOLD = (229, 170, 54)
WHITE = (255, 255, 255)
INK = (43, 58, 72)
GREY = (111, 123, 133)

FONT_DIR = Path("C:/Windows/Fonts")
BOLD = [str(FONT_DIR / "arialbd.ttf"), "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
DATE = [str(FONT_DIR / "Anton-Regular.ttf"), str(FONT_DIR / "Impact.ttf")]


def face(paths, size):
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fitted(draw, text, paths, size, max_width):
    for point in range(size, 16, -1):
        font = face(paths, point)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return font
    return face(paths, 16)


def centre(draw, box, text, font, fill, y, gap=0):
    x0, _, x1, _ = box
    width = draw.textbbox((0, 0), text, font=font)[2]
    draw.text(((x0 + x1 - width) // 2, y), text, font=font, fill=fill)


def icon_tariffs(d, b, c):
    x0, y0, x1, y1 = b
    d.polygon([(x0 + 28, y0 + 158), (x1 - 28, y0 + 158),
               (x1 - 48, y0 + 188), (x0 + 48, y0 + 188)], fill=NAVY)
    for x, y, col in ((x0 + 46, y0 + 122, TEAL), (x0 + 108, y0 + 122, GOLD),
                      (x0 + 46, y0 + 86, RED), (x0 + 108, y0 + 86, TEAL)):
        d.rectangle((x, y, x + 56, y + 34), fill=col, outline=NAVY, width=3)
        d.line((x + 18, y + 3, x + 18, y + 31), fill=NAVY, width=2)
        d.line((x + 38, y + 3, x + 38, y + 31), fill=NAVY, width=2)
    ax = x1 - 42
    d.line((ax, y0 + 150, ax, y0 + 40), fill=RED, width=11)
    d.polygon([(ax - 18, y0 + 66), (ax, y0 + 28), (ax + 18, y0 + 66)], fill=RED)


def icon_ukraine(d, b, c):
    x0, y0, x1, y1 = b
    for x, h in ((x0 + 24, 52), (x0 + 62, 86), (x0 + 104, 44), (x0 + 146, 72)):
        d.rectangle((x, y0 + 158 - h, x + 30, y0 + 158), fill=GREY)
        d.rectangle((x + 7, y0 + 158 - h + 10, x + 14, y0 + 158 - h + 19), fill=CREAM)
    d.line((x0 + 30, y0 + 118, x0 + 76, y0 + 92), fill=NAVY, width=6)
    d.line((x0 + 114, y0 + 92, x0 + 162, y0 + 118), fill=NAVY, width=6)
    d.line((x0 + 76, y0 + 92, x0 + 96, y0 + 108), fill=RED, width=6)
    d.polygon([(x0 + 112, y0 + 26), (x0 + 76, y0 + 100), (x0 + 106, y0 + 94),
               (x0 + 92, y0 + 150), (x0 + 144, y0 + 74), (x0 + 116, y0 + 80)], fill=GOLD)


def icon_huawei(d, b, c):
    x0, y0, x1, y1 = b
    d.rounded_rectangle((x0 + 28, y0 + 44, x0 + 118, y0 + 166), radius=5,
                        fill=WHITE, outline=NAVY, width=5)
    for yy in (76, 96, 116, 136):
        d.line((x0 + 44, y0 + yy, x0 + 102, y0 + yy), fill=GREY, width=4)
    d.line((x0 + 92, y0 + 152, x0 + 158, y0 + 66), fill=(139, 94, 55), width=13)
    d.rounded_rectangle((x0 + 134, y0 + 34, x0 + 194, y0 + 76), radius=7,
                        fill=GREY, outline=NAVY, width=4)
    d.ellipse((x0 + 62, y0 + 112, x0 + 114, y0 + 164), outline=RED, width=7)
    d.line((x0 + 70, y0 + 156, x0 + 106, y0 + 120), fill=RED, width=7)


def icon_space(d, b, c):
    x0, y0, x1, y1 = b
    for sx, sy in ((x0 + 28, y0 + 30), (x1 - 40, y0 + 52), (x0 + 48, y0 + 100)):
        d.ellipse((sx, sy, sx + 6, sy + 6), fill=GOLD)
    d.polygon([(x0 + 112, y0 + 20), (x0 + 142, y0 + 72),
               (x0 + 142, y0 + 132), (x0 + 112, y0 + 158),
               (x0 + 82, y0 + 132), (x0 + 82, y0 + 72)], fill=WHITE, outline=NAVY)
    d.polygon([(x0 + 112, y0 + 20), (x0 + 128, y0 + 50),
               (x0 + 96, y0 + 50)], fill=RED)
    d.ellipse((x0 + 101, y0 + 68, x0 + 123, y0 + 90), fill=TEAL, outline=NAVY, width=3)
    d.polygon([(x0 + 82, y0 + 126), (x0 + 54, y0 + 158), (x0 + 82, y0 + 150)], fill=RED)
    d.polygon([(x0 + 142, y0 + 126), (x0 + 170, y0 + 158), (x0 + 142, y0 + 150)], fill=RED)
    d.ellipse((x0 + 24, y0 + 128, x0 + 74, y0 + 178), fill=GREEN)
    d.ellipse((x0 + 34, y0 + 137, x0 + 64, y0 + 167), fill=GREEN)
    d.polygon([(x0 + 51, y0 + 138), (x0 + 55, y0 + 148), (x0 + 66, y0 + 148),
               (x0 + 57, y0 + 155), (x0 + 61, y0 + 165), (x0 + 51, y0 + 159),
               (x0 + 41, y0 + 165), (x0 + 45, y0 + 155), (x0 + 36, y0 + 148),
               (x0 + 47, y0 + 148)], fill=WHITE)


def icon_sudan(d, b, c):
    x0, y0, x1, y1 = b
    d.rectangle((x0 + 12, y0 + 166, x1 - 12, y0 + 184), fill=(203, 173, 125))
    cx, cy = (x0 + x1) // 2 - 12, y0 + 82
    for dx, dy in ((-52, -30), (52, -30), (-52, 30), (52, 30)):
        d.line((cx, cy, cx + dx, cy + dy), fill=NAVY, width=7)
        d.ellipse((cx + dx - 20, cy + dy - 8, cx + dx + 20, cy + dy + 8),
                  outline=NAVY, width=5)
    d.ellipse((cx - 26, cy - 17, cx + 26, cy + 17), fill=TEAL, outline=NAVY, width=4)
    d.line((cx, cy + 18, cx, cy + 66), fill=RED, width=8)
    for r in (18, 34):
        d.arc((x1 - 90 - r, y0 + 96 - r, x1 - 90 + r, y0 + 96 + r),
              0, 360, fill=RED, width=6)
    d.line((x1 - 44, y0 + 152, x1 - 44, y0 + 122), fill=RED, width=5)


def icon_colombia(d, b, c):
    x0, y0, x1, y1 = b
    for i in range(6):
        x = x0 + 18 + i * 34
        d.rectangle((x, y0 + 56, x + 34, y0 + 78),
                    fill=RED if i % 2 else WHITE, outline=NAVY, width=2)
    d.rectangle((x0 + 20, y0 + 80, x1 - 20, y0 + 164), fill=(224, 233, 239),
                outline=NAVY, width=4)
    d.rectangle((x0 + 84, y0 + 94, x0 + 136, y0 + 164), fill=WHITE, outline=NAVY, width=3)
    for px in (x0 + 50, x0 + 158, x0 + 178):
        d.ellipse((px - 10, y0 + 112, px + 10, y0 + 132), fill=GOLD, outline=NAVY, width=2)
        d.rectangle((px - 9, y0 + 132, px + 9, y0 + 166), fill=TEAL)
    d.ellipse((x0 + 38, y0 + 34, x0 + 56, y0 + 52), fill=RED)
    d.ellipse((x0 + 60, y0 + 34, x0 + 78, y0 + 52), fill=(52, 96, 200))


def icon_solomons(d, b, c):
    x0, y0, x1, y1 = b
    for yy in (y0 + 146, y0 + 172):
        d.arc((x0 + 10, yy - 30, x1 - 10, yy + 20), 0, 180, fill=TEAL, width=6)
    d.ellipse((x0 + 20, y0 + 122, x0 + 92, y0 + 156), fill=GOLD, outline=NAVY, width=3)
    d.ellipse((x1 - 100, y0 + 122, x1 - 22, y0 + 156), fill=GOLD, outline=NAVY, width=3)
    d.line((x0 + 52, y0 + 132, x0 + 52, y0 + 40), fill=NAVY, width=5)
    d.rectangle((x0 + 54, y0 + 42, x0 + 116, y0 + 78), fill=(28, 55, 118), outline=NAVY, width=3)
    d.ellipse((x0 + 78, y0 + 52, x0 + 92, y0 + 66), fill=WHITE)
    d.line((x1 - 62, y0 + 132, x1 - 62, y0 + 40), fill=NAVY, width=5)
    d.rectangle((x1 - 122, y0 + 42, x1 - 60, y0 + 78), fill=RED, outline=NAVY, width=3)
    d.polygon([(x1 - 104, y0 + 52), (x1 - 100, y0 + 62), (x1 - 90, y0 + 62),
               (x1 - 96, y0 + 69), (x1 - 94, y0 + 78), (x1 - 104, y0 + 72),
               (x1 - 114, y0 + 78), (x1 - 112, y0 + 69), (x1 - 118, y0 + 62),
               (x1 - 108, y0 + 62)], fill=GOLD)
    d.line((x1 - 118, y0 + 96, x1 - 64, y0 + 30), fill=RED, width=8)
    d.line((x1 - 118, y0 + 30, x1 - 64, y0 + 96), fill=RED, width=8)


def icon_spain(d, b, c):
    x0, y0, x1, y1 = b
    for i in range(3):
        d.line((x0 + 8, y0 + 52 + i * 22, x0 + 66, y0 + 52 + i * 22),
               fill=GREY, width=4)
    d.polygon([(x0 + 66, y0 + 104), (x1 - 30, y0 + 104), (x1 - 20, y0 + 122),
               (x1 - 30, y0 + 138), (x0 + 66, y0 + 138), (x0 + 92, y0 + 170),
               (x0 + 72, y0 + 170), (x0 + 44, y0 + 130), (x0 + 28, y0 + 130)],
              fill=WHITE, outline=NAVY)
    d.polygon([(x0 + 66, y0 + 104), (x1 - 30, y0 + 104), (x1 - 20, y0 + 122),
               (x0 + 48, y0 + 122)], fill=TEAL)
    d.ellipse((x1 - 46, y0 + 32, x1 - 18, y0 + 60), fill=WHITE, outline=NAVY, width=3)
    d.line((x1 - 52, y0 + 60, x1 - 52, y0 + 154), fill=NAVY, width=5)
    d.rectangle((x1 - 48, y0 + 62, x1 - 10, y0 + 98), fill=RED)
    d.rectangle((x1 - 48, y0 + 70, x1 - 10, y0 + 90), fill=GOLD)


GREEN = (62, 133, 90)

CARDS = [
    ("US TARIFFS", "CHINA AND EU HIT", icon_tariffs, RED, (249, 234, 231)),
    ("RUSSIAN STRIKES", "UKRAINE POWER CUT", icon_ukraine, NAVY, (231, 238, 244)),
    ("HUAWEI GUILTY", "US TRADE-SECRET THEFT", icon_huawei, TEAL, (229, 240, 238)),
    ("SHENZHOU-24", "PAKISTAN IN SPACE", icon_space, GOLD, (235, 242, 250)),
    ("SUDAN DRONES", "19 KILLED IN BLUE NILE", icon_sudan, RED, (249, 238, 226)),
    ("COLOMBIA", "20 HOSTAGES FREED", icon_colombia, TEAL, (231, 242, 244)),
    ("SOLOMON ISLANDS", "AUSTRALIA PACT SIGNED", icon_solomons, NAVY, (234, 240, 232)),
    ("ABREGO GARCIA", "LANDS IN SPAIN", icon_spain, GOLD, (249, 236, 231)),
]


def card(draw, x, y, w, h, item):
    line1, line2, icon, accent, tint = item
    draw.rounded_rectangle((x, y, x + w, y + h), radius=11,
                           fill=WHITE, outline=NAVY, width=3)
    panel = (x + 9, y + 9, x + w - 9, y + 216)
    draw.rounded_rectangle(panel, radius=7, fill=tint)
    icon(draw, panel, accent)
    band = (x + 9, y + 226, x + w - 9, y + h - 9)
    draw.rounded_rectangle(band, radius=6, fill=NAVY)
    f1 = fitted(draw, line1, BOLD, 27, w - 38)
    f2 = fitted(draw, line2, BOLD, 24, w - 38)
    centre(draw, band, line1, f1, WHITE, y + 252)
    centre(draw, band, line2, f2, (223, 232, 240), y + 292)


def poster():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 12), fill=RED)
    d.text((28, 28), "WEDNESDAY  /  WORLD NEWS", font=face(BOLD, 32), fill=TEAL)
    title = "25 NOVEMBER 2026"
    tf = fitted(d, title, DATE, 104, W - 56)
    d.text((26, 40), title, font=tf, fill=NAVY)
    d.rectangle((28, 176, W - 28, 181), fill=RED)

    margin, gap = 26, 14
    w = (W - 2 * margin - 3 * gap) // 4
    h = 364
    for index, item in enumerate(CARDS):
        col, row = index % 4, index // 4
        card(d, margin + col * (w + gap), 196 + row * (h + gap), w, h, item)

    d.line((28, 952, W - 28, 952), fill=GREY, width=2)
    d.text((28, 962), "BBC NEWS  /  AL JAZEERA   -   REPORTS FILED 25 NOV 2026",
           font=face(BOLD, 21), fill=INK)
    return img


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "entry.png"
    poster().save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes")
