# Blush & Sky — gender reveal baby shower suite

Original stationery suite for a combined **gender reveal + baby shower**. Dusty rose peonies on the left, powder-blue hydrangeas on the right, and a watercolor balloon pair whose gold ribbons form a heart. Champagne-gold frame. Editorial type. Not clipart footprints, glitter stars, or a Canva watermark.

Demo: **The Walker Baby** · Saturday 12 September 2026 · two o’clock · The Garden House, 48 Willow Lane.

## What’s in the suite

| Piece | Size | File |
| --- | --- | --- |
| Print invitation | 5×7 in @ 600 dpi | `exports/invite-5x7.png` |
| Phone / evite | 1080×1920 | `exports/invite-mobile.png` |
| Details card | 5×7 in | `exports/details-card.png` |
| Welcome sign | 18×24 ratio | `exports/welcome-sign.png` |
| Favor tag | 3 in round | `exports/favor-tag.png` |
| Books for baby insert | square | `exports/books-for-baby.png` |
| Diaper raffle ticket | 5×3 in | `exports/diaper-raffle.png` |

Editable sources live in `designs/`. Swap the placeholder name, date, and address before listing or sending.

## How this beats a typical competitor listing

- **Bundle vs. one card.** Most competing gender-reveal listings sell a single 5×7. This set includes print + phone, details, welcome sign, favor tag, books-for-baby, and a diaper raffle ticket.
- **Different silhouette in search.** Split botanicals (blush peony / sky hydrangea) + balloon heart, not watercolor footprints, confetti dots, and a clipart ribbon.
- **Muted 2026 palette.** Dusty rose, powder blue, and champagne gold on ivory paper — not candy pink / baby blue glitter.
- **One question, one title.** “He or She” once, then the event name. Details sit in a labeled DATE / TIME / PLACE panel so guests can actually read them.
- **Matching extras that raise AOV.** Books-for-baby and diaper raffle are the inserts hosts actually need, so the listing is worth more than a lone invite.

This is an original layout and illustration set. Do not copy another seller’s wording, artwork, or mockup photo.

## Preview locally

Open any file in `designs/` in Chrome. To re-export print PNGs:

```bash
node scripts/render.mjs
python3 scripts/make_listing.py
```

## Customize

In each HTML file, edit:

- Baby / family name (`The Walker Baby`)
- Date, time, venue
- RSVP line
- Details-card timeline, dress, games, registry

Brand tokens (hex + fonts) are documented in `listing/canva-recreate.md` if you rebuild the set as a Canva template.

## Etsy listing copy

See `listing/etsy-copy.md` for title, tags, and description drafted for this suite.
