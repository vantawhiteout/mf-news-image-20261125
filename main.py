# SPDX-License-Identifier: MIT
"""Copy the committed 25 November 2026 world-news poster to the output path."""
import os
import struct
import zlib
from pathlib import Path

MAX_BYTES = 1048576
SOURCE = Path(__file__).resolve().with_name("entry.png")


def load_poster(source):
    """Return the committed PNG only when it is a whole, capped 8-bit image."""
    blob = source.read_bytes()
    if not 33 <= len(blob) <= MAX_BYTES or blob[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("poster is not a small PNG")
    width, height, depth, colour, _, _, _ = struct.unpack(">IIBBBBB", blob[16:29])
    if not (1 <= width <= 1024 and 1 <= height <= 1024):
        raise ValueError("poster dimensions exceed the cap")
    if (depth, colour) != (8, 3):
        raise ValueError("poster must be an 8-bit paletted image")
    position, kinds, compressed, palette, ending = 8, [], [], None, None
    while position < len(blob):
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
    if not palette or palette % 3 or palette > 768 or ending != 0:
        raise ValueError("palette or end marker is malformed")
    if not compressed:
        raise ValueError("poster is missing image data")
    # Every scanline has one filter byte and one index per pixel. Checking the
    # inflated length catches a truncated stream whose header still looks fine.
    inflated = zlib.decompress(b"".join(compressed))
    if len(inflated) != height * (1 + width):
        raise ValueError("image data does not match the header")
    return blob


def main():
    root = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output").strip() or "/output"
    target = Path(root).expanduser() / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(load_poster(SOURCE))


if __name__ == "__main__":
    main()
