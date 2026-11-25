"""Validate and copy the 25 November 2026 world-news poster to the output path."""
import os, zlib
from pathlib import Path
blob = Path(__file__).with_name("entry.png").read_bytes()
w, h = (int.from_bytes(blob[i:i+4], "big") for i in (16, 20))
if len(blob) < 33 or len(blob) > 1048576 or blob[:8] != b"\x89PNG\r\n\x1a\n" or blob[12:16] != b"IHDR" or blob[-8:-4] != b"IEND" or not (1 <= w <= 1024 and 1 <= h <= 1024):
    raise ValueError("invalid PNG")
pos = 8
while pos < len(blob):
    n = int.from_bytes(blob[pos:pos+4], "big")
    end = pos + 12 + n
    if end > len(blob) or zlib.crc32(blob[pos+4:pos+8+n]) != int.from_bytes(blob[pos+8+n:end], "big"):
        raise ValueError("bad PNG chunk")
    pos = end
root = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output").strip() or "/output"
target = Path(root).expanduser() / "entry.png"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_bytes(blob)
