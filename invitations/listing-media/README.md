# Where to upload (Etsy)

Three different slots. Do not put the same file in all three.

## 1. Photos — search + listing gallery

Shop Manager → Listings → your listing → **Photos and video**

| Order | File | Why |
| --- | --- | --- |
| Photo 1 | `04-exact-card-mockup-2000.jpg` | Search thumbnail. This mockup uses the **exact card file**, not an AI redraw. |
| Photo 2 | `02-etsy-card-square-2000.jpg` | The real 5x7 design, uncropped, so buyers can read the invite. |
| Photo 3 | `listing-jpg/03-aria-listing-hero-5x7-300dpi.jpg` | Vertical card as they will print it. |

Drag Photo 1 to the first slot. Etsy crops the first photo to a square in search — that is why the mockup is already 2000×2000.

## 2. Video — listing video (separate from photos)

Same **Photos and video** row → click the **blank video icon** (not a photo slot).

Upload: `03-etsy-listing-video-6s.mp4`

- 6.0 seconds, 1080×1080, MP4, 2.8 MB (under 100 MB)
- Etsy strips audio automatically — that is normal
- Do not upload the video as a digital download

## 3. Digital files — what the buyer actually receives

Listing → **Digital files** / Instant download (not Photos).

Upload the print card only:

- `5x7-print/03-aria-listing-hero-5x7-600dpi.png` (best print)
- optional: `listing-jpg/03-aria-listing-hero-5x7-300dpi.jpg`

Never attach the mockup or the video here. Buyers would print the marble table photo instead of the invitation.

## Exact-card mockup (changed artwork)

The marble mockup composites **your real invitation pixels**. It does not redraw the design.

1. Save the changed card as `invitations/client-card.png` (or `.jpg`)
2. Run: `python3 invitations/listing-media/make_exact_card_mockup.py`
3. New thumbnail: `listing-media/04-exact-card-mockup-2000.jpg`

If `client-card.png` is missing, the script uses the Version 3 print file.
