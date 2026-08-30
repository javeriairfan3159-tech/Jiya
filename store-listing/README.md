# Store listing assets

Ready-to-upload Play Store / App Store files for **V380 Pro Guide**.

```
store-listing/
├── STORE_LISTING.md          # Short + long descriptions (EN + UR)
├── icon/
│   ├── ic_launcher_512.png   # Play Store icon
│   └── ic_launcher_1024.png  # High-res master
├── banner/
│   ├── banner_playstore_1024x500.png   # Play feature graphic
│   ├── banner_youtube_1920x1080.png    # YouTube / ads
│   └── banner_strip_1920x600.png       # Wide web/header strip
├── feature-graphic/
│   └── feature_graphic_1024x500.png    # same as Play banner
├── screenshots/              # 6 phone shots, 1080×1920
├── video/
│   ├── v380-pro-guide-promo-16x9.mp4   # ~18s YouTube / Play promo
│   └── v380-pro-guide-promo-9x16.mp4   # ~18s Reels / Shorts / Status
├── source/                   # Original UI captures
├── build_screenshots.py
└── build_promo.py            # Rebuild banners + videos
```

**Download everything:** `V380-Pro-Guide-Store-Assets.zip`

Copy-paste the text from `STORE_LISTING.md` into Play Console.

Play promo video: upload the 16:9 MP4 to YouTube (unlisted is fine), then paste the YouTube URL in Play Console.
