# SPDX-License-Identifier: MIT
"""Build-time artwork generator for the 25 November 2026 news poster.

Pillow is needed only here. The graded main.py uses the standard library and
copies the committed PNG. Run ``python render.py`` to rebuild entry.png.
"""
import math
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIDE = 1000
PAPER = (247, 244, 235)
INK = (17, 38, 54)
CRIMSON = (184, 48, 42)
OCEAN = (20, 101, 112)
GOLD = (224, 166, 54)
STEEL = (137, 151, 159)
WHITE = (255, 255, 255)
FLAME = (215, 92, 38)
PALE_BLUE = (230, 238, 243)
PALE_SAND = (251, 239, 222)
PALE_TEAL = (228, 241, 240)
PALE_RED = (250, 234, 229)

BOLD = (r"C:\Windows\Fonts\arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
DISPLAY = (r"C:\Windows\Fonts\Anton-Regular.ttf", r"C:\Windows\Fonts\impact.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


def face(names, size):
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def fit(draw, text, names, size, room):
    while size > 12:
        font = face(names, size)
        if draw.textlength(text, font=font) <= room:
            return font
        size -= 2
    return face(names, 12)


def centred(draw, y, text, font, colour, left, right):
    width = draw.textlength(text, font=font)
    draw.text(((left + right - width) / 2, y), text, font=font, fill=colour)


def fire(d, x, y, scale=1):
    d.polygon([(x - 18 * scale, y), (x + 18 * scale, y),
               (x + 8 * scale, y - 22 * scale), (x + 22 * scale, y - 30 * scale),
               (x, y - 62 * scale), (x - 20 * scale, y - 28 * scale),
               (x - 8 * scale, y - 20 * scale)], fill=FLAME)
    d.polygon([(x - 8 * scale, y), (x + 8 * scale, y),
               (x + 3 * scale, y - 24 * scale), (x, y - 34 * scale),
               (x - 7 * scale, y - 20 * scale)], fill=GOLD)


def drone(d, cx, cy, spread=40):
    d.line((cx - spread, cy - 6, cx + spread, cy - 6), fill=INK, width=6)
    d.line((cx - 12, cy - 6, cx - 4, cy + 10), fill=INK, width=5)
    d.line((cx + 12, cy - 6, cx + 4, cy + 10), fill=INK, width=5)
    for dx in (-spread, spread):
        d.ellipse((cx + dx - 18, cy - 14, cx + dx + 18, cy - 2),
                  outline=INK, width=4)
        d.line((cx + dx - 13, cy - 8, cx + dx + 13, cy - 8), fill=STEEL, width=3)
    d.ellipse((cx - 17, cy - 15, cx + 17, cy + 9), fill=OCEAN, outline=INK, width=3)
    d.rectangle((cx - 3, cy + 8, cx + 3, cy + 18), fill=CRIMSON)


def badge(d, x, y, label):
    d.rounded_rectangle((x, y, x + 62, y + 40), radius=7,
                        fill=CRIMSON, outline=INK, width=3)
    centred(d, y + 5, label, face(BOLD, 26), WHITE, x, x + 62)


def icon_tariffs(d, box):
    x, y, xr, _ = box
    for dx, dy in ((18, 76), (74, 76), (130, 76), (46, 122), (102, 122)):
        d.rectangle((x + dx, y + dy, x + dx + 44, y + dy + 36),
                    fill=WHITE, outline=INK, width=3)
        d.line((x + dx + 22, y + dy, x + dx + 22, y + dy + 36), fill=STEEL, width=2)
    badge(d, xr - 74, y + 14, "14")
    line = [(x + 18, y + 172), (x + 62, y + 158), (x + 100, y + 166),
            (x + 144, y + 140), (xr - 12, y + 154)]
    d.line(line, fill=CRIMSON, width=8, joint="curve")
    d.polygon([(xr - 30, y + 144), (xr - 8, y + 152), (xr - 18, y + 170)],
              fill=CRIMSON)


def icon_hormuz(d, box):
    x, y, xr, _ = box
    for row in range(2):
        for k in range(4):
            d.arc((x + 12 + k * 52, y + 158 + row * 18 - 12,
                   x + 60 + k * 52, y + 158 + row * 18 + 12),
                  180, 360, fill=OCEAN, width=4)
    d.polygon([(x + 18, y + 108), (xr - 52, y + 108), (xr - 28, y + 136),
               (x + 18, y + 136)], fill=WHITE, outline=INK)
    d.rectangle((x + 24, y + 82, x + 116, y + 108), fill=STEEL, outline=INK, width=3)
    d.rectangle((x + 118, y + 92, x + 142, y + 108), fill=CRIMSON, outline=INK, width=3)
    for k in range(4):
        d.rectangle((x + 32 + k * 22, y + 86, x + 44 + k * 22, y + 102), fill=WHITE)
    fire(d, xr - 56, y + 104, 0.75)
    mx, my = x + 56, y + 166
    d.ellipse((mx - 13, my - 13, mx + 13, my + 13), fill=INK)
    for angle in range(0, 360, 45):
        dx = 17 * math.cos(math.radians(angle))
        dy = 17 * math.sin(math.radians(angle))
        d.line((mx + dx * 0.7, my + dy * 0.7, mx + dx, my + dy), fill=INK, width=3)
    d.line((mx, my - 35, mx, my - 20), fill=CRIMSON, width=4)


def icon_jets(d, box):
    x, y, xr, _ = box
    d.rectangle((x + 14, y + 168, xr - 14, y + 180), fill=STEEL)
    for j in range(2):
        jx = x + 38 + j * 92
        d.polygon([(jx, y + 132), (jx + 60, y + 132), (jx + 72, y + 148),
                   (jx + 60, y + 160), (jx, y + 160), (jx + 12, y + 146)],
                  fill=WHITE, outline=INK)
        d.polygon([(jx + 8, y + 132), (jx + 18, y + 112), (jx + 28, y + 132)],
                  fill=OCEAN, outline=INK)
    drone(d, x + 110, y + 52, 36)
    d.line((x + 110, y + 68, x + 92, y + 112), fill=CRIMSON, width=5)
    d.polygon([(x + 92, y + 112), (x + 82, y + 104), (x + 98, y + 100)],
              fill=CRIMSON)
    badge(d, xr - 74, y + 12, "5")


def icon_heat(d, box):
    x, y, xr, _ = box
    d.ellipse((x + 20, y + 54, x + 122, y + 156), fill=OCEAN, outline=INK, width=3)
    d.polygon([(x + 44, y + 72), (x + 74, y + 64), (x + 86, y + 88),
               (x + 62, y + 104), (x + 40, y + 96)], fill=GOLD)
    d.polygon([(x + 78, y + 112), (x + 104, y + 122), (x + 96, y + 148),
               (x + 66, y + 142)], fill=GOLD)
    d.rounded_rectangle((x + 144, y + 36, x + 172, y + 138), radius=13,
                        fill=WHITE, outline=INK, width=3)
    d.rectangle((x + 153, y + 70, x + 163, y + 138), fill=CRIMSON)
    d.ellipse((x + 138, y + 122, x + 178, y + 162), fill=CRIMSON, outline=INK, width=3)
    d.line([(x + 20, y + 174), (x + 72, y + 166), (xr - 12, y + 144)],
           fill=CRIMSON, width=7, joint="curve")
    badge(d, xr - 78, y + 4, "2°C")


def icon_sudan(d, box):
    x, y, xr, _ = box
    d.rectangle((x + 12, y + 174, xr - 12, y + 190), fill=PALE_SAND)
    for i in range(3):
        bx = x + 22 + i * 56
        d.rectangle((bx, y + 128, bx + 42, y + 174), fill=WHITE, outline=INK, width=3)
        d.rectangle((bx + 12, y + 146, bx + 26, y + 174), fill=STEEL)
    d.polygon([(x + 104, y + 128), (x + 148, y + 102), (x + 168, y + 128)],
              fill=CRIMSON, outline=INK, width=2)
    drone(d, x + 92, y + 58, 40)
    d.line((x + 92, y + 74, x + 116, y + 106), fill=CRIMSON, width=4)
    d.polygon([(x + 116, y + 106), (x + 106, y + 100), (x + 112, y + 114)],
              fill=CRIMSON)


def icon_huawei(d, box):
    x, y, xr, _ = box
    d.rectangle((x + 18, y + 158, xr - 18, y + 174), fill=STEEL)
    d.rounded_rectangle((x + 72, y + 66, x + 132, y + 104), radius=8,
                        fill=GOLD, outline=INK, width=3)
    d.line((x + 102, y + 100, x + 142, y + 156), fill=INK, width=10)
    d.ellipse((x + 126, y + 150, x + 186, y + 168), fill=WHITE, outline=INK, width=3)
    d.rectangle((x + 22, y + 92, x + 62, y + 132), fill=PALE_BLUE, outline=INK, width=3)
    for k in range(3):
        d.line((x + 28 + k * 12, y + 84, x + 28 + k * 12, y + 92), fill=INK, width=3)
        d.line((x + 28 + k * 12, y + 132, x + 28 + k * 12, y + 140), fill=INK, width=3)


def icon_space(d, box):
    x, y, xr, _ = box
    d.rectangle((x + 88, y + 104, x + 132, y + 156), fill=WHITE, outline=INK, width=3)
    for dx in (-52, 46):
        d.rectangle((x + 88 + dx, y + 116, x + 132 + dx, y + 144),
                    fill=OCEAN, outline=INK, width=3)
        for k in range(3):
            d.line((x + 94 + dx + k * 12, y + 116,
                    x + 94 + dx + k * 12, y + 144), fill=WHITE, width=2)
    d.line((x + 110, y + 104, x + 110, y + 56), fill=INK, width=4)
    d.line((x + 110, y + 56, x + 140, y + 56), fill=INK, width=4)
    d.polygon([(x + 110, y + 56), (x + 82, y + 40), (x + 82, y + 72)], fill=GOLD)
    rx = x + 42
    d.polygon([(rx, y + 24), (rx + 16, y + 54), (rx + 16, y + 104),
               (rx - 16, y + 104), (rx - 16, y + 54)], fill=WHITE, outline=INK)
    d.ellipse((rx - 16, y + 54, rx + 16, y + 76), fill=OCEAN, outline=INK, width=3)
    d.polygon([(rx - 16, y + 94), (rx - 34, y + 122), (rx - 16, y + 116)], fill=CRIMSON)
    d.polygon([(rx + 16, y + 94), (rx + 34, y + 122), (rx + 16, y + 116)], fill=CRIMSON)
    fire(d, rx, y + 118, 0.55)


def icon_colombia(d, box):
    x, y, xr, _ = box
    d.rectangle((x + 20, y + 86, xr - 18, y + 162), fill=WHITE, outline=INK, width=3)
    for k in range(6):
        bx = x + 20 + k * 25
        d.rectangle((bx, y + 72, bx + 25, y + 88),
                    fill=CRIMSON if k % 2 == 0 else WHITE, outline=INK, width=2)
    d.rectangle((x + 54, y + 108, x + 82, y + 162), fill=PALE_BLUE, outline=INK, width=2)
    d.rectangle((x + 108, y + 108, x + 136, y + 162), fill=PALE_BLUE, outline=INK, width=2)
    for k in range(3):
        px = x + 34 + k * 44
        d.ellipse((px, y + 168, px + 16, y + 184), fill=GOLD, outline=INK, width=2)
        d.line((px + 8, y + 184, px + 8, y + 200), fill=INK, width=4)
        d.line((px + 8, y + 200, px + 1, y + 206), fill=INK, width=3)
        d.line((px + 8, y + 200, px + 15, y + 206), fill=INK, width=3)
    cx, cy = xr - 40, y + 42
    d.polygon([(cx, cy - 26), (cx + 22, cy - 16), (cx + 22, cy + 8),
               (cx, cy + 26), (cx - 22, cy + 8), (cx - 22, cy - 16)],
              fill=OCEAN, outline=INK, width=3)
    centred(d, cy - 12, "+", face(BOLD, 28), WHITE, cx - 22, cx + 22)


CARDS = [
    ("TARIFFS", "14 PARTNERS", "SHARES FALL", icon_tariffs, PALE_RED),
    ("HORMUZ", "IRAN: TANKER", "HITS A MINE", icon_hormuz, PALE_BLUE),
    ("UKRAINE", "KYIV: 5 JETS", "HIT AIRFIELD", icon_jets, PALE_SAND),
    ("CLIMATE", "6 DAYS OVER 2°C", "PRE-INDUSTRIAL", icon_heat, PALE_TEAL),
    ("SUDAN", "19 DEAD IN", "RSF STRIKES", icon_sudan, PALE_SAND),
    ("HUAWEI", "US JURY GUILTY", "TRADE SECRETS", icon_huawei, PALE_BLUE),
    ("SHENZHOU-24", "FIRST PAKISTANI", "ASTRONAUT", icon_space, PALE_TEAL),
    ("COLOMBIA", "20 HOSTAGES", "RESCUED", icon_colombia, PALE_SAND),
]


def card(draw, x, y, w, h, entry):
    title, upper, lower, icon, tint = entry
    draw.rounded_rectangle((x, y, x + w, y + h), radius=11,
                           fill=WHITE, outline=INK, width=3)
    draw.rounded_rectangle((x + 8, y + 8, x + w - 8, y + 196), radius=7, fill=tint)
    icon(draw, (x + 8, y + 8, x + w - 8, y + 196))
    draw.rounded_rectangle((x + 8, y + 204, x + w - 8, y + h - 8), radius=6, fill=INK)
    centred(draw, y + 214, title, fit(draw, title, BOLD, 36, w - 28),
            WHITE, x + 8, x + w - 8)
    centred(draw, y + 264, upper, fit(draw, upper, BOLD, 25, w - 28),
            (224, 237, 244), x + 8, x + w - 8)
    centred(draw, y + 296, lower, fit(draw, lower, BOLD, 25, w - 28),
            (224, 237, 244), x + 8, x + w - 8)


def poster():
    image = Image.new("RGB", (SIDE, SIDE), PAPER)
    d = ImageDraw.Draw(image)
    d.rectangle((0, 0, SIDE, 10), fill=CRIMSON)
    d.text((28, 18), "WEDNESDAY  /  WORLD NEWS", font=face(BOLD, 26), fill=OCEAN)
    date = "25 NOVEMBER 2026"
    d.text((24, 48), date, font=fit(d, date, DISPLAY, 100, SIDE - 48), fill=INK)
    d.rectangle((26, 164, SIDE - 26, 170), fill=CRIMSON)
    lead = "TARIFFS / HORMUZ / UKRAINE / HEAT / SUDAN / HUAWEI / SPACE / RESCUE"
    d.text((26, 178), lead, font=fit(d, lead, BOLD, 21, SIDE - 52), fill=OCEAN)
    margin, gutter, w, h = 24, 10, 232, 344
    for index, entry in enumerate(CARDS):
        col, row = index % 4, index // 4
        card(d, margin + col * (w + gutter), 214 + row * (h + gutter), w, h, entry)
    d.line((26, 926, SIDE - 26, 926), fill=STEEL, width=2)
    source = "FILED 25 NOV 2026  /  BBC  -  GUARDIAN  -  AL JAZEERA  -  CNBC"
    d.text((26, 938), source, font=fit(d, source, BOLD, 19, SIDE - 52), fill=INK)
    return image


def chunk(kind, payload):
    return (struct.pack(">I", len(payload)) + kind + payload
            + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))


def write_png(image, target):
    indexed = image.quantize(colors=192, method=Image.Quantize.MEDIANCUT)
    rows = indexed.tobytes()
    palette = bytes(indexed.getpalette()[:768])
    scan = bytearray()
    for row in range(SIDE):
        scan.append(0)
        scan.extend(rows[row * SIDE:(row + 1) * SIDE])
    packer = zlib.compressobj(level=9, wbits=15)
    stream = packer.compress(bytes(scan)) + packer.flush()
    header = struct.pack(">IIBBBBB", SIDE, SIDE, 8, 3, 0, 0, 0)
    payload = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
               + chunk(b"PLTE", palette) + chunk(b"IDAT", stream)
               + chunk(b"IEND", b""))
    if len(payload) > 1048576:
        raise ValueError("poster exceeds the one-megabyte cap")
    target.write_bytes(payload)
    return len(payload)


if __name__ == "__main__":
    destination = Path(__file__).resolve().parent / "entry.png"
    print("wrote", destination, write_png(poster(), destination), "bytes")
