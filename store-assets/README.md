# Kite Master store pack

Everything you need to list **Kite Master** on Google Play and the App Store.

## Upload map

### Google Play
| Console field | File |
| --- | --- |
| High-res icon | `icon/kite-master-icon-512.png` (512×512, 32-bit PNG) |
| Feature graphic | `banners/play-store-feature-1024x500.png` (1024×500) |
| Phone screenshots | `screenshots/01-home-wind.png` … `05-achievements.png` (1080×1920) |
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

## Preview
Open `preview.html` locally.

## Rebuild
```bash
python3 store-assets/build_pack.py
```
Needs Python 3, Pillow, and ffmpeg. Original captures live in `source/app-screens/`.
