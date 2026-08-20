# Velvet Garden — luxury birthday invitation suite

Print-ready **5×7** birthday invitations. Hero colorway is **light blush pink**, plus the original dark suite.

Painterly peonies and rose-gold botanicals. Editorial type. Asymmetric layouts — not clipart roses in every corner.

## Colorways

| File | Look |
|---|---|
| **Blush Atelier** | Light pink parchment, dusty-rose cascade down the right edge |
| **Blush Garden** | Powder-pink silk, peonies climbing the left |
| **Blush Blank** | Write-in template for hand-lettering |
| Nocturne | Oxblood velvet, ivory type, antique gold |
| Forest | Emerald soirée, blush peony, gold leaf |
| Ivory Atelier | Cream parchment, terracotta cascade |

Demo guest of honour: **Amara** · Saturday 24 August · seven o’clock · The Conservatory, Villa Céleste.

## Print

- `print-png/` — 5×7 at **600 DPI** (3000×4200)
- `print-jpg/` — 5×7 at **300 DPI** (1500×2100)
- `exports/*.pdf` — 5×7, no margins

Print at 100% on 110–130 lb / 300 gsm cardstock. Trim to 5×7.

```bash
./render.sh
python3 make_listing.py
```

## Listing media

`listing/` — Etsy thumbnails, lifestyle mockups, square card photos.

**Paste-ready SEO:** `listing/ETSY-SEO.md` (title, 13 tags, description, attributes). Thumbnail: `00b-etsy-thumbnail-blush-2000.jpg`.
