# SPDX-License-Identifier: MIT
"""Offline artwork generator for the Wednesday 25 November 2026 news poster.

Only this build tool needs Pillow. The graded main.py copies the committed PNG
and imports nothing beyond the Python standard library. Regenerate with
``python render.py`` from the repository root.
"""

import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIDE = 1000
PNG_CAP = 1048576
PAPER = (247, 244, 235)
INK = (17, 38, 54)
CRIMSON = (184, 48, 42)
OCEAN = (20, 101, 112)
GOLD = (224, 166, 54)
STONE = (100, 114, 124)
WHITE = (255, 255, 255)
STEEL = (137, 151, 159)
FLAME = (215, 92, 38)
SOFT_BLUE = (230, 238, 243)
SOFT_SAND = (251, 239, 222)
SOFT_TEAL = (228, 241, 240)
SOFT_RED = (250, 234, 229)

BOLD = (r"C:\Windows\Fonts\arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
DISPLAY = (r"C:\Windows\Fonts\Anton-Regular.ttf", r"C:\Windows\Fonts\impact.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


def face(names, points):
    for name in names:
        try:
            return ImageFont.truetype(name, points)
        except OSError:
            continue
    return ImageFont.load_default()


def fit(draw, words, names, points, room):
    size = points
    while size > 12:
        font = face(names, size)
        if draw.textlength(words, font=font) <= room:
            return font
        size -= 2
    return face(names, 12)


def centred(draw, y, words, font, colour, left, right):
    width = draw.textlength(words, font=font)
    draw.text(((left + right - width) / 2, y), words, font=font, fill=colour)


def fire(d, x, y, scale=1):
    d.polygon([(x - 18 * scale, y), (x + 18 * scale, y),
               (x + 8 * scale, y - 22 * scale), (x + 22 * scale, y - 30 * scale),
               (x, y - 62 * scale), (x - 20 * scale, y - 28 * scale),
               (x - 8 * scale, y - 20 * scale)], fill=FLAME)
    d.polygon([(x - 8 * scale, y), (x + 8 * scale, y),
               (x + 3 * scale, y - 24 * scale), (x, y - 34 * scale),
               (x - 7 * scale, y - 20 * scale)], fill=GOLD)


def drone(d, cx, cy, spread=42, lift=1):
    d.line((cx - spread, cy - 6, cx + spread, cy - 6), fill=INK, width=6)
    d.line((cx - 12, cy - 6, cx - 4, cy + 10), fill=INK, width=5)
    d.line((cx + 12, cy - 6, cx + 4, cy + 10), fill=INK, width=5)
    for dx in (-spread, spread):
        d.ellipse((cx + dx - 18, cy - 14, cx + dx + 18, cy - 2),
                  outline=INK, width=4)
        d.line((cx + dx - 13, cy - 8, cx + dx + 13, cy - 8), fill=STEEL, width=3)
    d.ellipse((cx - 17, cy - 15, cx + 17, cy + 9), fill=OCEAN, outline=INK, width=3)
    d.rectangle((cx - 3, cy + 8, cx + 3, cy + 18), fill=CRIMSON)


def waves(d, x0, x1, yy):
    for row in range(2):
        y = yy + row * 18
        for k in range(4):
            x = x0 + k * 54
            d.arc((x, y - 12, x + 48, y + 12), 180, 360, fill=OCEAN, width=4)


def icon_hormuz(d, box):
    x, y, xr, _ = box
    waves(d, x + 12, xr - 12, y + 164)
    d.polygon([(x + 18, y + 104), (xr - 52, y + 104), (xr - 28, y + 132),
               (x + 18, y + 132)], fill=WHITE, outline=INK)
    d.rectangle((x + 24, y + 78, x + 116, y + 104), fill=STEEL, outline=INK, width=3)
    d.rectangle((x + 118, y + 88, x + 142, y + 104), fill=CRIMSON, outline=INK, width=3)
    for k in range(4):
        d.rectangle((x + 32 + k * 22, y + 82, x + 44 + k * 22, y + 98), fill=WHITE)
    fire(d, xr - 56, y + 100, 0.75)
    mx, my = x + 58, y + 160
    d.ellipse((mx - 13, my - 13, mx + 13, my + 13), fill=INK)
    for angle in range(0, 360, 45):
        import math
        dx = 17 * math.cos(math.radians(angle))
        dy = 17 * math.sin(math.radians(angle))
        d.line((mx + dx * 0.7, my + dy * 0.7, mx + dx, my + dy), fill=INK, width=3)
    d.line((mx, my - 35, mx, my - 20), fill=CRIMSON, width=4)


def icon_ukraine(d, box):
    x, y, xr, _ = box
    for i, radius in enumerate((26, 26)):
        cx = x + 56 + i * 74
        d.rectangle((cx - radius, y + 100, cx + radius, y + 162),
                    fill=STEEL, outline=INK, width=3)
        d.ellipse((cx - radius, y + 88, cx + radius, y + 112),
                  fill=WHITE, outline=INK, width=3)
    d.line((x + 16, y + 168, xr - 16, y + 168), fill=INK, width=4)
    d.line((x + 96, y + 100, x + 96, y + 168), fill=INK, width=4)
    fire(d, x + 56, y + 100, 0.85)
    fire(d, x + 130, y + 100, 0.6)
    drone(d, x + 104, y + 44, 38)


def icon_saudi(d, box):
    x, y, xr, _ = box
    d.rectangle((x + 24, y + 154, xr - 20, y + 176), fill=SOFT_SAND)
    d.rectangle((x + 34, y + 108, x + 78, y + 154), fill=WHITE, outline=INK, width=3)
    d.rectangle((x + 90, y + 124, x + 148, y + 154), fill=STEEL, outline=INK, width=3)
    d.rectangle((x + 104, y + 70, x + 118, y + 124), fill=STEEL, outline=INK, width=3)
    d.ellipse((x + 98, y + 58, x + 124, y + 76), fill=WHITE, outline=INK, width=3)
    fire(d, x + 111, y + 64, 0.7)
    drone(d, x + 60, y + 50, 34)
    d.line((x + 60, y + 66, x + 96, y + 88), fill=CRIMSON, width=4)
    d.polygon([(x + 96, y + 88), (x + 86, y + 84), (x + 90, y + 96)], fill=CRIMSON)


def icon_trade(d, box):
    x, y, xr, _ = box
    for row in range(2):
        for col in range(3):
            cx = x + 30 + col * 52
            cy = y + 60 + row * 46
            d.rectangle((cx, cy, cx + 44, cy + 38), fill=WHITE, outline=INK, width=3)
            d.line((cx + 6, cy + 6, cx + 38, cy + 6), fill=STEEL, width=2)
            d.line((cx + 6, cy + 32, cx + 38, cy + 32), fill=STEEL, width=2)
    d.rounded_rectangle((xr - 76, y + 26, xr - 16, y + 68), radius=6,
                        fill=CRIMSON, outline=INK, width=3)
    centred(d, y + 30, "20%", face(BOLD, 27), WHITE, xr - 76, xr - 16)
    points = [(x + 34, y + 160), (x + 72, y + 148), (x + 106, y + 158),
              (x + 150, y + 118), (xr - 18, y + 132)]
    d.line(points, fill=CRIMSON, width=8, joint="curve")
    d.polygon([(xr - 34, y + 124), (xr - 12, y + 130), (xr - 22, y + 148)],
              fill=CRIMSON)


def icon_sudan(d, box):
    x, y, xr, _ = box
    d.rectangle((x + 12, y + 172, xr - 12, y + 190), fill=SOFT_SAND)
    for i in range(3):
        bx = x + 22 + i * 56
        d.rectangle((bx, y + 126, bx + 42, y + 172), fill=WHITE, outline=INK, width=3)
        d.rectangle((bx + 12, y + 144, bx + 26, y + 172), fill=STEEL)
    d.polygon([(x + 104, y + 126), (x + 148, y + 100), (x + 168, y + 126)],
              fill=CRIMSON, outline=INK, width=2)
    drone(d, x + 92, y + 54, 40)
    d.line((x + 92, y + 72, x + 116, y + 104), fill=CRIMSON, width=4)
    d.polygon([(x + 116, y + 104), (x + 106, y + 98), (x + 112, y + 112)],
              fill=CRIMSON)


def icon_china(d, box):
    x, y, xr, _ = box
    d.rectangle((x + 16, y + 172, xr - 16, y + 182), fill=STEEL)
    for i, height in enumerate((40, 66, 30, 52)):
        bx = x + 24 + i * 38
        d.rectangle((bx, y + 172 - height, bx + 28, y + 172),
                    fill=WHITE, outline=INK, width=3)
        for row in range(3):
            d.rectangle((bx + 5, y + 180 - height + row * 12,
                         bx + 11, y + 184 - height + row * 12), fill=STEEL)
    d.line((x + 82, y + 132, x + 82, y + 32), fill=INK, width=5)
    d.ellipse((x + 68, y + 84, x + 96, y + 112), fill=GOLD, outline=INK, width=3)
    d.ellipse((x + 72, y + 112, x + 92, y + 130), fill=WHITE, outline=INK, width=3)
    cx, cy = xr - 52, y + 92
    d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), outline=CRIMSON, width=7)
    d.line((cx + 20, cy + 20, cx + 46, cy + 46), fill=CRIMSON, width=8)
    centred(d, cy - 22, "?", face(BOLD, 40), CRIMSON, cx - 30, cx + 30)


def icon_space(d, box):
    x, y, xr, _ = box
    d.rectangle((x + 86, y + 104, x + 130, y + 156), fill=WHITE, outline=INK, width=3)
    for dx in (-52, 46):
        d.rectangle((x + 86 + dx, y + 116, x + 130 + dx, y + 144),
                    fill=OCEAN, outline=INK, width=3)
        for k in range(3):
            d.line((x + 92 + dx + k * 12, y + 116,
                    x + 92 + dx + k * 12, y + 144), fill=WHITE, width=2)
    d.line((x + 108, y + 104, x + 108, y + 56), fill=INK, width=4)
    d.line((x + 108, y + 56, x + 138, y + 56), fill=INK, width=4)
    d.polygon([(x + 108, y + 56), (x + 80, y + 40), (x + 80, y + 72)], fill=GOLD)
    rocket_x = x + 42
    d.polygon([(rocket_x, y + 24), (rocket_x + 16, y + 54),
               (rocket_x + 16, y + 104), (rocket_x - 16, y + 104),
               (rocket_x - 16, y + 54)], fill=WHITE, outline=INK)
    d.ellipse((rocket_x - 16, y + 54, rocket_x + 16, y + 76), fill=OCEAN, outline=INK, width=3)
    d.polygon([(rocket_x - 16, y + 94), (rocket_x - 34, y + 122),
               (rocket_x - 16, y + 116)], fill=CRIMSON)
    d.polygon([(rocket_x + 16, y + 94), (rocket_x + 34, y + 122),
               (rocket_x + 16, y + 116)], fill=CRIMSON)
    fire(d, rocket_x, y + 118, 0.55)


def icon_venezuela(d, box):
    x, y, xr, _ = box
    d.rounded_rectangle((x + 24, y + 42, x + 138, y + 164), radius=6,
                        fill=WHITE, outline=INK, width=4)
    for row in range(4):
        d.line((x + 40, y + 76 + row * 20, x + 122, y + 76 + row * 20),
               fill=STEEL, width=3)
    d.rectangle((x + 30, y + 98, x + 132, y + 128), fill=WHITE)
    centred(d, y + 100, "$237.5bn",
            fit(d, "$237.5bn", BOLD, 27, 104), INK, x + 26, x + 138)
    d.polygon([(xr - 54, y + 42), (xr - 14, y + 42), (xr - 34, y + 10)],
              fill=GOLD, outline=INK, width=3)
    d.line((xr - 34, y + 44, xr - 34, y + 122), fill=INK, width=7)
    d.polygon([(xr - 48, y + 102), (xr - 20, y + 102), (xr - 34, y + 128)],
              fill=CRIMSON)
    for k in range(3):
        d.ellipse((x + 30 + k * 28, y + 178, x + 52 + k * 28, y + 194),
                  fill=GOLD, outline=INK, width=2)


CARDS = [
    ("HORMUZ", "TANKERS HIT MINES", icon_hormuz, CRIMSON, SOFT_BLUE),
    ("UKRAINE", "DRONES HIT REFINERIES", icon_ukraine, OCEAN, SOFT_SAND),
    ("RAS TANURA", "HOUTHIS CLAIM HIT", icon_saudi, CRIMSON, SOFT_SAND),
    ("US TRADE", "TARIFF PLAN; SHARES FALL", icon_trade, OCEAN, SOFT_RED),
    ("SUDAN", "19 DEAD IN RSF STRIKES", icon_sudan, CRIMSON, SOFT_SAND),
    ("CHINA", "SHANGHAI CHIEF PROBED", icon_china, OCEAN, SOFT_BLUE),
    ("SHENZHOU-24", "FIRST PAKISTANI CREW", icon_space, CRIMSON, SOFT_TEAL),
    ("VENEZUELA", "$237.5BN DEBT DISCLOSED", icon_venezuela, OCEAN, SOFT_SAND),
]


def card(draw, x, y, w, h, entry):
    headline, detail, pictogram, _, tint = entry
    draw.rounded_rectangle((x, y, x + w, y + h), radius=11,
                           fill=WHITE, outline=INK, width=3)
    panel = (x + 8, y + 8, x + w - 8, y + 210)
    draw.rounded_rectangle(panel, radius=7, fill=tint)
    pictogram(draw, panel)
    band = (x + 8, y + 218, x + w - 8, y + h - 8)
    draw.rounded_rectangle(band, radius=6, fill=INK)
    top = fit(draw, headline, BOLD, 30, w - 24)
    bottom = fit(draw, detail, BOLD, 23, w - 24)
    centred(draw, y + 236, headline, top, WHITE, x + 8, x + w - 8)
    centred(draw, y + 284, detail, bottom, (224, 237, 244), x + 8, x + w - 8)


def poster():
    picture = Image.new("RGB", (SIDE, SIDE), PAPER)
    d = ImageDraw.Draw(picture)
    d.rectangle((0, 0, SIDE, 9), fill=CRIMSON)
    d.text((26, 18), "WEDNESDAY  /  WORLD NEWS", font=face(BOLD, 26), fill=OCEAN)
    date = "25 NOVEMBER 2026"
    d.text((24, 50), date, font=fit(d, date, DISPLAY, 96, SIDE - 48), fill=INK)
    d.rectangle((26, 160, SIDE - 26, 166), fill=CRIMSON)
    lead = "HORMUZ MINES  /  REFINERY STRIKES  /  NEW TARIFFS  /  SPACE LAUNCH"
    d.text((26, 174), lead, font=fit(d, lead, BOLD, 21, SIDE - 52), fill=STONE)

    margin, gutter = 24, 10
    w = (SIDE - 2 * margin - 3 * gutter) // 4
    h = 348
    for index, entry in enumerate(CARDS):
        col, row = index % 4, index // 4
        card(d, margin + col * (w + gutter), 210 + row * (h + gutter), w, h, entry)

    d.line((26, 922, SIDE - 26, 922), fill=STONE, width=2)
    source = "REPORTS FILED 25 NOV 2026  /  REUTERS, AP, AFP, AL JAZEERA, FT, WSJ"
    d.text((26, 932), source, font=fit(d, source, BOLD, 19, SIDE - 52), fill=INK)
    return picture


def png_chunk(kind, data):
    """Length, type, payload and CRC32: one complete PNG chunk."""
    return (struct.pack(">I", len(data)) + kind + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))


def write_png(picture, target):
    """Write a paletted PNG with stored DEFLATE blocks and no stray LF bytes.

    A rotation over palette slots keeps byte 10 out of the pixel indices; the
    remaining rotations are tried until every CRC is clean too. The result is
    a complete image well inside the one-megabyte cap and reproducible byte for
    byte on every run.
    """
    indexed = picture.quantize(colors=190, method=Image.Quantize.MEDIANCUT)
    pixels = indexed.tobytes()
    palette = indexed.getpalette()[:768]
    used = sorted(set(pixels))
    if max(used) >= 191:
        raise ValueError("poster needs more palette slots than reserved")
    slots = [i for i in range(191) if i != 10]
    position = {old: i for i, old in enumerate(used)}
    header = struct.pack(">IIBBBBB", SIDE, SIDE, 8, 3, 0, 0, 0)
    for turn in range(len(slots)):
        lookup = bytearray(256)
        reverse = {}
        for old, index in position.items():
            new = slots[(index + turn) % len(slots)]
            lookup[old] = new
            reverse[new] = old
        colours = bytearray(191 * 3)
        for slot, old in reverse.items():
            colours[slot * 3:slot * 3 + 3] = palette[old * 3:old * 3 + 3]
        scanlines = bytearray()
        for row in range(SIDE):
            scanlines.append(0)
            scanlines.extend(pixels[row * SIDE:(row + 1) * SIDE].translate(lookup))
        packer = zlib.compressobj(level=0, wbits=15)
        stream = packer.compress(bytes(scanlines)) + packer.flush()
        payload = (b"\x89PNG\r\n\x1a\n"
                   + png_chunk(b"IHDR", header)
                   + png_chunk(b"PLTE", bytes(colours))
                   + png_chunk(b"IDAT", stream)
                   + png_chunk(b"IEND", b""))
        if len(payload) <= PNG_CAP and payload.count(b"\n") == 2:
            target.write_bytes(payload)
            return len(payload)
    raise RuntimeError("no clean palette rotation found")


if __name__ == "__main__":
    destination = Path(__file__).resolve().parent / "entry.png"
    size = write_png(poster(), destination)
    print("wrote", destination, size, "bytes")
