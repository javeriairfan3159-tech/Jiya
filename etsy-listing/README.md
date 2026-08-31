# Jiya — Desi Wedding Planner (Etsy pack)

Eye-catching mockups, a vertical promo video, and a copy-paste SEO listing for the Jiya wedding app.

## Folders

- `mockups/` — upload-ready listing photos (start with `01-hero-three-phones.jpg`)
- `video/jiya-desi-wedding-planner-vertical.mp4` — 9:16 ~18s
- `ETSY_LISTING.md` — title, tags, description, category, Pinterest copy
- `screenshots/` — original app screens
- `assets/` — lifestyle backgrounds used to build the mockups
- `build_assets.py` — regenerates mockups + video

## Rebuild

```bash
python3 etsy-listing/build_assets.py
```

Requires Pillow, OpenCV, ffmpeg.
