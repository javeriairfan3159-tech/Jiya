# Kite Master store pack

Everything you need to list **Kite Master** on Google Play and the App Store.

## Upload map

### Google Play
| Console field | File |
| --- | --- |
| High-res icon | `icon/kite-master-icon-512.png` (512×512, 32-bit PNG) — new flying patang kite |
| Feature graphic | `banners/play-store-feature-1024x500.png` (1024×500) |
| Phone screenshots | `play-console/phone-screenshots/01`–`05-phone-*.png` (1080×1920, 9:16) — **Play Console → Phone assets** |
| Promo video | Upload `videos/kite-master-promo-16x9.mp4` to YouTube, paste the URL |
| Short / full description | `copy/STORE_LISTING.md` |

### App Store
| Field | File |
| --- | --- |
| App icon | `icon/kite-master-icon-1024.png` |
| 6.7" screenshots | Same `screenshots/01`–`05` set |
| Preview video | `videos/kite-master-promo-9x16.mp4` |
| Subtitle / description | `copy/STORE_LISTING.md` |

## Extra marketing
- `banners/promo-banner-1920x1080.png` — web / social hero
- `banners/youtube-thumbnail.png`
- `banners/lifestyle-kite-dusk.png` — lifestyle still
- `videos/kite-master-promo-9x16.mp4` — Reels / Shorts / TikTok (15s)
- `videos/kite-master-screens-tour-9x16.mp4` — UI walkthrough (10s)
- `icon/kite-master-icon-alt-1024.png` — alternate diamond-kite icon

`promo-shot-*.png` files are cinematic extras. Do **not** use them as the main store screenshots; they are not the live app UI.

## Play Console — Phone screenshots

Google Play Console → **Store listing** → **Phone assets** → **Phone screenshots** pe ye 5 files drop karo (2–8 chahiye, 9:16, 1080×1920):

- [Download ZIP (5 PNGs)](downloads/Play-Console-Phone-Screenshots.zip)
- Or folder: `play-console/phone-screenshots/`

## Download videos

Open `preview.html` and tap **Download** under each player, or grab the ZIP:

- [Download all 3 videos (ZIP)](downloads/Kite-Master-Promo-Videos.zip)
- [9:16 Reels / Shorts](videos/kite-master-promo-9x16.mp4)
- [16:9 YouTube / Play Store](videos/kite-master-promo-16x9.mp4)
- [Screens tour](videos/kite-master-screens-tour-9x16.mp4)

On GitHub, click a file → the **Download** button, or use Raw.

## Preview
Open `preview.html` locally. Videos section has a download button on every clip.

## Rebuild
```bash
python3 store-assets/build_pack.py
```
Needs Python 3, Pillow, and ffmpeg. Original captures live in `source/app-screens/`.
