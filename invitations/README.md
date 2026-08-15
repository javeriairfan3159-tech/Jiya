# Racing Birthday Invitation — 5×7

Original racing-themed birthday invitations designed to outclass typical “movie cars” competitor listings. Characters, logo, and layout are original (star-hood racer #07, navy stripes #12, yellow compact #21 — not franchise character art), so the listing is more unique and safer to sell.

Print size: **5 × 7 inches**  
Print files: **1500 × 2100 px (300 DPI)** and **3000 × 4200 px (600 DPI)**

Sample party details (swap before selling):

- **Name / age:** Leo’s 5th birthday
- **Headline options:** Start Your Engines! · Race On Over! · Ready Set Go! · Need Speed
- **When:** Saturday, June 14 · 4:00 PM
- **Where:** 123 Speedway Lane, Any City, ST 12345
- **RSVP:** Mom · 555-123-4567

## Versions

| File | Look | Best for |
| --- | --- | --- |
| `01-leo-start-your-engines` | Stadium track, giant asphalt **5**, gold script name, date/time pills | Main Etsy listing / most cinematic |
| `02-leo-race-on-over` | Clean white stationery, watercolor car cluster, rust slab-serif name | Closest “elevated competitor” layout |
| `03-leo-ready-set-go` | Championship shield logo, desert highway, 3-column details | Bold thumbnail / high-energy listing photo |
| `04-leo-need-speed` | White card, road-textured 5, red speed swooshes, script + block type | Alternate listing image |
| `html/01-white-luxury.html` | Same white layout with **live, editable type** over the car illustration | Custom name/date before print |
| `html/02-asphalt-gold.html` | Dark asphalt + gold script, editable type | Second customizable option |

## Folders

- `originals/` — master artwork
- `5x7-print/` — cropped to exact 5:7 for print
- `listing-jpg/` — 1500 × 2100 (300 DPI) JPEGs plus a 2000px Etsy mockup
- `html/` — print-ready HTML (Chrome → Print → 5×7, margins none)

## Print

1. Open an HTML file in Chrome, **or** send a `5x7-print` PNG to the print shop.
2. Paper size **5 × 7 in**, margins **None**, scale **100%**.
3. Rebuild print crops after replacing an original:

```bash
python3 invitations/scripts/make_print_assets.py
```

Do **not** use Disney, Pixar, Lightning McQueen, Mater, or “Cars movie” in the Etsy title, tags, or description. Rank on the same buyer intent with safer keywords: race car birthday, racing invitation, start your engines invite. See `03-etsy-seo.md`.
