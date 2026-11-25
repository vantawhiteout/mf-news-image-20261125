"""Validate and copy the 25 November 2026 world-news poster to the output path."""
import os, zlib
from pathlib import Path
blob = Path(__file__).with_name("entry.png").read_bytes()
w, h = (int.from_bytes(blob[i:i+4], "big") for i in (16, 20))
magic = b"\x89PNG\r\n\x1a\n"
if (len(blob) < 33 or len(blob) > 1048576 or blob[:8] != magic
        or blob[12:16] != b"IHDR" or blob[-8:-4] != b"IEND"
        or not (1 <= w <= 1024 and 1 <= h <= 1024)):
    raise ValueError("invalid PNG")
if blob[24:26] != b"\x08\x03" or blob.count(b"\n") != 2:
    raise ValueError("expected a paletted PNG with no stray newline bytes")
pos, kinds = 8, []
while pos < len(blob):
    n = int.from_bytes(blob[pos:pos+4], "big")
    end = pos + 12 + n
    if end > len(blob) or zlib.crc32(blob[pos+4:pos+8+n]) != int.from_bytes(blob[pos+8+n:end], "big"):
        raise ValueError("bad PNG chunk")
    kinds.append(blob[pos+4:pos+8])
    pos = end
if b"PLTE" not in kinds or b"IDAT" not in kinds:
    raise ValueError("incomplete PNG")
root = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output").strip() or "/output"
target = Path(root).expanduser() / "entry.png"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_bytes(blob)
