# SPDX-License-Identifier: MIT
"""Copy the committed 25 November 2026 world-news poster to the output path."""
import os
import struct
import zlib
from pathlib import Path

MAX_BYTES = 1048576
MAX_SIDE = 1024
SIGNATURE = b"\x89PNG\r\n\x1a\n"
SOURCE = Path(__file__).resolve().with_name("entry.png")


def load_poster(source):
    """Return the committed PNG only when it is a whole, capped 8-bit image."""
    blob = source.read_bytes()
    if not 33 <= len(blob) <= MAX_BYTES or not blob.startswith(SIGNATURE):
        raise ValueError("poster is not a small PNG")
    width, height, depth, colour, _, _, _ = struct.unpack(">IIBBBBB", blob[16:29])
    if not (1 <= width <= MAX_SIDE and 1 <= height <= MAX_SIDE):
        raise ValueError("poster dimensions exceed the cap")
    if (depth, colour) != (8, 3):
        raise ValueError("poster must be an 8-bit paletted image")
    position, kinds, compressed, palette, ending = 8, [], [], None, None
    while position < len(blob):
        if len(blob) - position < 12:
            raise ValueError("trailing bytes after the PNG stream")
        length = struct.unpack(">I", blob[position:position + 4])[0]
        end = position + 12 + length
        if end > len(blob):
            raise ValueError("truncated PNG chunk")
        kind = blob[position + 4:position + 8]
        checksum = struct.unpack(">I", blob[end - 4:end])[0]
        if zlib.crc32(blob[position + 4:end - 4]) != checksum:
            raise ValueError("PNG checksum mismatch")
        kinds.append(kind)
        if kind == b"IDAT":
            compressed.append(blob[position + 8:end - 4])
        elif kind == b"PLTE":
            palette = length
        elif kind == b"IEND":
            ending = length
        position = end
    if position != len(blob) or kinds[0] != b"IHDR" or kinds[-1] != b"IEND":
        raise ValueError("incomplete PNG stream")
    if kinds.count(b"IHDR") != 1 or kinds.count(b"IEND") != 1:
        raise ValueError("duplicate header or end marker")
    if not palette or palette % 3 or palette > 768 or ending != 0:
        raise ValueError("palette or end marker is malformed")
    if not compressed:
        raise ValueError("poster is missing image data")
    if kinds.index(b"PLTE") > next(i for i, k in enumerate(kinds) if k == b"IDAT"):
        raise ValueError("palette follows the image data")
    # Every scanline has one filter byte and one index per pixel. A bounded
    # inflate caps memory and catches a truncated or overlong stream.
    expected = height * (1 + width)
    inflater = zlib.decompressobj()
    inflated = inflater.decompress(b"".join(compressed), expected + 1)
    if (len(inflated) != expected or not inflater.eof
            or inflater.unconsumed_tail or inflater.unused_data):
        raise ValueError("image data does not match the header")
    return blob


def main():
    root = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output").strip() or "/output"
    target = Path(root).expanduser() / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(load_poster(SOURCE))


if __name__ == "__main__":
    main()
