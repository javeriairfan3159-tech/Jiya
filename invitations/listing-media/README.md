# Etsy thumbnail mockups — Ready Set Go card

These composites use the **exact invitation file** (`originals/alex-ready-set-go.png` — ALEX Ready Set Go card). They do not redraw the design.

Size: **2000 × 2000** (Etsy search crop)

## Where to upload

Shop Manager → Listings → Photos and video

| Order | File | Why |
| --- | --- | --- |
| Photo 1 | `01-etsy-thumb-asphalt-2000.jpg` | Search thumbnail. Asphalt + flags + cone + toy car. |
| Photo 2 | `02-etsy-thumb-redflag-2000.jpg` | Red silk + checkered flag — luxury listing photo. |
| Photo 3 | `03-etsy-thumb-square-card-2000.jpg` | Straight-on so buyers can read the invite. |
| Photo 4 | `../listing-jpg/03-leo-ready-set-go-5x7-300dpi.jpg` | The print card, uncropped. |

Do **not** attach mockups as the digital download. Buyers would print the asphalt photo instead of the invitation.

## Rebuild after the card changes

```bash
python3 invitations/listing-media/make_etsy_thumbnail.py
```
