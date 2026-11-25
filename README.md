# 25 November 2026, in one image

`entry.png` is a 1024x1024 dated poster for Wednesday 25 November 2026. Its
eight pictograms and short labels cover the main stories reported that day,
across five continents:

- Iran war: an oil tanker hit a naval mine and caught fire in the Strait of Hormuz (Al Jazeera).
- US tariff plan: new tariffs aimed at major partners, including China and the EU (BBC).
- AI sell-off: Nvidia shares fell 7% and Asian markets dived (BBC, Al Jazeera).
- UK energy: the Ofgem cap is set to rise 26% from January (BBC).
- Ukraine: Russian strikes killed five and cut power in five regions (Al Jazeera).
- Shenzhou-24 docked with Tiangong carrying Pakistan's first astronaut (BBC, Al Jazeera).
- Sudan: RSF drone attacks killed at least 19 people in Blue Nile state (Al Jazeera).
- Colombia: police freed hostages seized at a Cartagena supermarket (BBC).

## Running

`main.py` is the entrypoint. It uses only the Python standard library, validates
the bundled PNG and writes its bytes to `$MAKEFUN_OUTPUT_DIR/entry.png`, or to
`/output/entry.png` when the variable is unset. Both graded runs produce the
same bytes in well under a second.

`render.py` is the offline build tool that draws the poster with Pillow. The
graded program does not import it. Regenerate the artwork with `python render.py`.

MIT licensed; see LICENSE.
