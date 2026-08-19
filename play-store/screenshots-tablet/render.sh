#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
python3 generate.py
mkdir -p out
CHROME="${CHROME:-google-chrome}"
USER_DATA="$(mktemp -d /tmp/chrome-play-tab-XXXXXX)"
PORT=9600
for html in html/*.html; do
  base="$(basename "$html" .html)"
  png="out/${base}.png"
  jpg="out/${base}.jpg"
  PORT=$((PORT + 1))
  echo "Rendering $base"
  timeout 20s "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-sandbox \
    --user-data-dir="$USER_DATA" \
    --remote-debugging-port="$PORT" \
    --disable-background-networking --disable-sync \
    --force-device-scale-factor=2 --window-size=1920,1080 \
    --virtual-time-budget=3000 \
    --screenshot="$png" "file://${ROOT}/${html}" || true
  if [[ ! -f "$png" ]]; then
    echo "FAILED $base" >&2
    exit 1
  fi
  ffmpeg -y -hide_banner -loglevel error -i "$png" -q:v 3 "$jpg"
  echo "saved $jpg"
done
python3 - <<'PY'
from pathlib import Path
from struct import unpack
for p in sorted(Path("out").glob("*.png")):
    w,h = unpack(">II", p.read_bytes()[16:24])
    print(f"{p.name:24} {w}x{h}  {p.stat().st_size/1024/1024:.2f}MB")
PY
ls -lh out/*.jpg
