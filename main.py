# SPDX-License-Identifier: MIT
"""Copy the committed 25 November 2026 news poster to the output directory."""
import os
import struct
import zlib
from pathlib import Path

BITS = b"\x89PNG\r\n\x1a\n"
CEILING = 1048576
SOURCE = Path(__file__).resolve().with_name("entry.png")


def checked(blob):
    """Only copy a complete, capped, 8-bit paletted PNG."""
    if not 33 <= len(blob) <= CEILING or not blob.startswith(BITS):
        raise ValueError("poster is not a small PNG")
    width, height, depth, colour, _, _, _ = struct.unpack(">IIBBBBB", blob[16:29])
    if not (1 <= width <= 1024 and 1 <= height <= 1024):
        raise ValueError("poster dimensions exceed 1024")
    if depth != 8 or colour != 3:
        raise ValueError("poster must be 8-bit paletted")
    at, kinds, streams, palette = 8, [], [], None
    while at < len(blob):
        if len(blob) - at < 12:
            raise ValueError("bytes after the PNG stream")
        size = struct.unpack(">I", blob[at:at + 4])[0]
        stop = at + 12 + size
        if stop > len(blob):
            raise ValueError("truncated PNG chunk")
        kind = blob[at + 4:at + 8]
        if zlib.crc32(kind + blob[at + 8:stop - 4]) != struct.unpack(">I", blob[stop - 4:stop])[0]:
            raise ValueError("PNG checksum mismatch")
        kinds.append(kind)
        if kind == b"PLTE":
            palette = size
        elif kind == b"IDAT":
            streams.append(blob[at + 8:stop - 4])
        at = stop
    if at != len(blob) or kinds[0] != b"IHDR" or kinds[-1] != b"IEND":
        raise ValueError("incomplete PNG stream")
    if kinds.count(b"IHDR") != 1 or kinds.count(b"IEND") != 1:
        raise ValueError("duplicate header or end")
    if not palette or palette % 3 or palette > 768 or not streams:
        raise ValueError("bad palette or missing image data")
    if kinds.index(b"PLTE") > kinds.index(b"IDAT"):
        raise ValueError("palette appears after image data")
    need = height * (1 + width)
    flow = zlib.decompressobj()
    raw = flow.decompress(b"".join(streams), need + 1)
    if len(raw) != need or not flow.eof or flow.unconsumed_tail or flow.unused_data:
        raise ValueError("image data does not match the header")
    stride = width + 1
    for row in range(height):
        line = raw[row * stride:(row + 1) * stride]
        if line[0] > 4 or max(line[1:]) >= palette // 3:
            raise ValueError("bad scanline filter or pixel index")
    return blob


def main():
    root = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output").strip() or "/output"
    target = Path(root).expanduser() / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(checked(SOURCE.read_bytes()))


if __name__ == "__main__":
    main()
