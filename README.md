# Kite Master — Store assets

High-quality Play Store / App Store pack for **Kite Master**, the dark neon utility app for kite flyers (live wind, pech tactics, safety & knots).

## Quick start

| Need | File |
| --- | --- |
| App icon (Play Store) | `store-assets/icon/kite-master-icon-512.png` (new patang kite) |
| App icon (hi-res) | `store-assets/icon/kite-master-icon-1024.png` |
| Feature graphic | `store-assets/banners/play-store-feature-1024x500.png` |
| YouTube thumbnail | `store-assets/banners/youtube-thumbnail.png` |
| Phone screenshots (Play Console) | `store-assets/play-console/phone-screenshots/` or [ZIP](store-assets/downloads/Play-Console-Phone-Screenshots.zip) |
| Vertical promo | `store-assets/videos/kite-master-promo-9x16.mp4` |
| Landscape promo | `store-assets/videos/kite-master-promo-16x9.mp4` |
| Listing copy | `store-assets/copy/STORE_LISTING.md` |

Open `store-assets/preview.html` in a browser to review everything. Har video ke neeche **Download** button hai.

**Videos download:**
- All 3 clips ZIP: `store-assets/downloads/Kite-Master-Promo-Videos.zip`
- 9:16: `store-assets/videos/kite-master-promo-9x16.mp4`
- 16:9: `store-assets/videos/kite-master-promo-16x9.mp4`
- Screens tour: `store-assets/videos/kite-master-screens-tour-9x16.mp4`

Use `screenshots/01`–`05` on the store listing — those wrap the **real app UI** (ads cropped). Files named `promo-shot-*` are extra cinematic frames, not the live app.

## Rebuild

```bash
python3 store-assets/build_pack.py
```

Requires Python 3, Pillow, and ffmpeg.
