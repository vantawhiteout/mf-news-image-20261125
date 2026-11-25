"""Copy the shipped 25 November 2026 world news poster to the output path."""
import os
from pathlib import Path

blob = Path(__file__).with_name("entry.png").read_bytes()
if len(blob) < 33 or len(blob) > 1048576 or blob[:8] != b"\x89PNG\r\n\x1a\n" or blob[-8:-4] != b"IEND":
    raise ValueError("invalid PNG")
width = int.from_bytes(blob[16:20], "big")
height = int.from_bytes(blob[20:24], "big")
if not (1 <= width <= 1024 and 1 <= height <= 1024):
    raise ValueError("bad dimensions")
root = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output").strip() or "/output"
target = Path(root).expanduser() / "entry.png"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_bytes(blob)
