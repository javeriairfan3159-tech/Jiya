#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
python3 generate_slides.py
mkdir -p images video
CHROME="${CHROME:-google-chrome}"
i=0
for html in slides/*.html; do
  i=$((i + 1))
  base="$(basename "$html" .html)"
  png="images/${base}.png"
  jpg="images/${base}.jpg"
  echo "Rendering $base"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-sandbox \
    --force-device-scale-factor=1 --window-size=2000,2000 \
    --run-all-compositor-stages-before-draw --virtual-time-budget=8000 \
    --screenshot="$png" "file://${ROOT}/${html}"
  ffmpeg -y -hide_banner -loglevel error -i "$png" -q:v 3 "$jpg"
  echo "saved $jpg"
done
echo "Building video"
ffmpeg -y -hide_banner -loglevel error \
  -framerate 10/18 \
  -pattern_type glob -i 'images/0*.jpg' \
  -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p" \
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart \
  video/listing-video.mp4
ls -lh images video
echo "Done"
