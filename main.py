"""Copy the shipped 25 November 2026 news poster to the output path."""
import os
from pathlib import Path

SOURCE = Path(__file__).with_name("entry.png")
DEST = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")


def main():
    payload = SOURCE.read_bytes()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n") or len(payload) > 1048576:
        raise ValueError("invalid entry.png")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(payload)


if __name__ == "__main__":
    main()
