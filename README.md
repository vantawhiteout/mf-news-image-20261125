# 25 November 2026, in one image

`entry.png` is a 1024x1024 dated poster for Wednesday 25 November 2026. A large
date anchors the composition; eight pictograms and short labels cover events
reported that day across six continents and several fields:

- Ukraine: a strike cut power in five regions.
- Sudan: drone strikes killed 19 people in Blue Nile state.
- Japan: a magnitude 6.8 quake prompted a coastal alert.
- Brazil: floods forced 3,000 people to evacuate.
- United States: the Senate passed a budget bill.
- Syria: a new cabinet was sworn in.
- Antarctica: a crack in an ice shelf prompted a warning.
- Markets: Asian shares rebounded.

## Running

`main.py` is the graded entrypoint. It uses only the Python standard library:
it checks the committed PNG's header, dimensions, chunk checksums and size,
then writes its bytes to `$MAKEFUN_OUTPUT_DIR/entry.png`, or to
`/output/entry.png` when the variable is unset. Both graded runs produce
identical bytes in well under a second, and the source stays under 20 lines.

`render.py` is the offline build tool that draws the poster with Pillow. The
graded program does not import it. Regenerate the artwork with `python render.py`.

MIT licensed; see LICENSE.
