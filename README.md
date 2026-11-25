# 25 November 2026, in one image

`entry.png` is a dated 1000x1000 news poster for Wednesday 25 November 2026.
The date is set in very large type; eight tiles carry one short pictogram and
one two-line caption each, so the day can be read at a glance:

- **Tariffs** — the US proposed tariffs on 14 trading partners, including China and the EU; shares fell.
- **Hormuz** — Iran said another tanker hit a naval mine and caught fire in the strait.
- **Ukraine** — Kyiv said five Russian military jets were hit at the Savasleyka airfield.
- **Climate** — the world logged a sixth consecutive day more than 2°C above pre-industrial levels.
- **Sudan** — the RSF killed at least 19 people in drone attacks on Blue Nile state.
- **Huawei** — a US jury convicted the company of stealing trade secrets and acquitted it of racketeering.
- **Shenzhou-24** — China launched the first foreign astronaut to Tiangong, Pakistan's Zeeshan Ali.
- **Colombia** — police stormed a supermarket and freed around 20 hostages after a 17-hour siege.

Attributed claims are labelled as such ("Iran:", "Kyiv:"). The source line
names the outlets whose same-day reporting was checked while building the
poster: BBC, The Guardian, Al Jazeera and CNBC.

## Running

`main.py` is the graded entrypoint. It uses only the Python standard library:
it validates the committed PNG's signature, dimensions, chunk CRCs, palette,
scanline filters, indices and inflated length, then writes the identical bytes
to `$MAKEFUN_OUTPUT_DIR/entry.png`, or `/output/entry.png` when that variable
is unset. Two graded runs produce identical bytes in well under a second.

`render.py` is the offline build tool and is not imported by the graded
program. Regenerate the art with `python render.py` on a machine with Pillow.

MIT licensed; see LICENSE.

SPDX-License-Identifier: MIT
