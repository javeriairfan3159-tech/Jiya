#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
python3 generate_slides.py
mkdir -p images video
CHROME="${CHROME:-google-chrome}"
USER_DATA="$(mktemp -d /tmp/chrome-etsy-XXXXXX)"
PORT=9333
for html in slides/*.html; do
  base="$(basename "$html" .html)"
  png="images/${base}.png"
  jpg="images/${base}.jpg"
  if [[ -f "$jpg" ]]; then
    echo "skip $base (jpg exists)"
    continue
  fi
  echo "Rendering $base"
  PORT=$((PORT + 1))
  timeout 18s "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-sandbox \
    --user-data-dir="$USER_DATA" \
    --remote-debugging-port="$PORT" \
    --disable-background-networking --disable-sync \
    --force-device-scale-factor=1 --window-size=2000,2000 \
    --virtual-time-budget=2500 \
    --screenshot="$png" "file://${ROOT}/${html}" || true
  if [[ ! -f "$png" ]]; then
    echo "FAILED $base" >&2
    exit 1
  fi
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
ls -lh images/*.jpg video
echo "Done"
