# Meadow Shell Market Tote — Pattern (Fixed & Rebuilt)

A crochet pattern for a shell-mesh market tote, rebuilt so that the written
instructions, the diagrams, and the photos all match the reference sample bag
(solid sage green, straps included) exactly.

## Structure

| Path | Contents |
|---|---|
| `pattern/meadow-shell-market-tote.html` | The full 18-page pattern (HTML + inline SVG diagrams) |
| `assets/photos/` | Pattern photography (all-sage, consistent with the reference bag) |
| `assets/fonts/` | Playfair Display & Lora (SIL Open Font License) |
| `output/Meadow_Shell_Market_Tote_FIXED.pdf` | The final print-ready A4 PDF |

## Rebuilding the PDF

Use the build script (recommended). It finds Chrome/Chromium, renders the
pattern, and exits as soon as the PDF is written:

```bash
scripts/build-pdf.sh
# or write elsewhere: scripts/build-pdf.sh /tmp/preview.pdf
```

Equivalent raw command:

```bash
google-chrome --headless=new --no-sandbox \
  --print-to-pdf=output/Meadow_Shell_Market_Tote_FIXED.pdf \
  --no-pdf-header-footer \
  "file:///$(pwd)/pattern/meadow-shell-market-tote.html"
```

> In sandboxed/CI environments headless Chrome writes the PDF within a second
> or two but often does not exit on its own; the raw command can appear to hang.
> `scripts/build-pdf.sh` handles this by stopping Chrome once the PDF is
> complete, so prefer it there.

## Development environment (Cloud Agents)

`.cursor/environment.json` configures the Cloud Agent environment. There are no
package dependencies — the only tool required is Chrome/Chromium, which the base
image already provides. `install` simply verifies Chrome is present and makes
the build script executable. Edit `pattern/meadow-shell-market-tote.html`, then
run `scripts/build-pdf.sh` to regenerate the PDF.

## Fixes applied vs. the previous version

1. **Photos matched to the reference bag.** The cover, three-sizes, and
   materials photos showed a two-tone bag (cream straps + edge); the reference
   sample is solid sage. All three photos were replaced with all-sage versions
   in the same style.
2. **Colourways corrected.** "Sage & Cream" (two-tone) was listed as the
   pictured colourway; the pictured bag is one solid colour. The three
   colourways are now solid shades with Sage marked *as pictured*, and the
   two-tone look moved to an optional tip.
3. **Strap construction corrected to match the photos.** The text said to
   anchor the chained strap back into *the very same rim stitch* (a single
   anchor point), but every photo shows each handle rising from **two anchor
   points** spaced apart. The strap section now chains up, anchors 10 (12, 14)
   rim sts along, hdc's back, and then works the rim sts beneath the arch —
   nothing skipped. Counts verified: 11+10+23+10+12 = 66 (S), and 78 / 90 for
   M / L. The strap diagram was redrawn to match.
4. **Gauge corrected.** "3 shells + 3 mesh sc = 10 cm" was impossible with
   66 sts ≈ 61 cm circumference; now "2 shells + 2 mesh sc ≈ 11 cm".
5. **Size chart corrected.** "Strap drop 28/32/36 cm" contradicted the short
   handles in the photos; now "Strap rise above rim ≈ 12/13/14 cm".
6. **Diagrams redrawn as clean vector art** (cover bag at-a-glance, three
   sizes, base top-down view, stitch chart, top-edge band, strap) in the sage
   palette of the reference bag.
7. **Caption fixes** (e.g. the base photo shows one base, not "all three
   sizes").

All stitch counts in the base (48→54→60→66), body (66 ÷ 3 = 22 ch-3 sps,
11 shells × 6 sts = 66), top edge, and straps were re-verified round by round.
