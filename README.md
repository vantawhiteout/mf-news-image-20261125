# 25 November 2026, in one image

`entry.png` is a 1000x1000 dated poster for Wednesday 25 November 2026. The
large date names the day; eight pictograms and short labels cover stories
reported that day in Europe, the Middle East, Africa, Asia and the Americas:

- Strait of Hormuz: two oil tankers struck naval mines and caught fire.
- Ukraine: drones hit two Russian oil refineries in the Samara region.
- Ras Tanura: the Houthis claimed a drone strike on the Saudi refinery; the
  coalition said it intercepted four drones.
- Trade: Washington prepared tariffs on China, the EU and 14 other economies;
  global shares fell.
- Sudan: a rights group reported 19 civilians killed in RSF drone strikes.
- China: the Shanghai party chief was placed under investigation.
- Space: Shenzhou-24 launched with the first Pakistani crew member on Tiangong.
- Venezuela: the government disclosed $237.5bn of public debt.

The source line credits the reporting behind those items: Reuters, AP, AFP,
Al Jazeera, the FT and the WSJ. Disputed claims are labelled as claims.

## Running

`main.py` is the graded entrypoint. It uses only the Python standard library:
it checks the committed PNG's header, palette, chunk checksums, inflated scanline
length, dimensions and size, then writes the identical bytes to
`$MAKEFUN_OUTPUT_DIR/entry.png`, or to `/output/entry.png` when the variable is
unset. Two graded runs produce identical bytes in well under a second.

`render.py` is the offline build tool; the graded program does not import it.
Regenerate the artwork with `python render.py`. It writes an 8-bit indexed PNG
with stored DEFLATE blocks and palette indices chosen to keep the file a
complete PNG under 1 MiB and byte-for-byte reproducible.

MIT licensed; see LICENSE.

SPDX-License-Identifier: MIT
