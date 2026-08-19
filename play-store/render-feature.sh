#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
CHROME="${CHROME:-google-chrome}"
USER_DATA="$(mktemp -d /tmp/chrome-play-XXXXXX)"
PORT=9460

echo "Rendering 4K master (4096x2000)"
timeout 25s "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-sandbox \
  --user-data-dir="$USER_DATA" \
  --remote-debugging-port="$PORT" \
  --disable-background-networking --disable-sync \
  --force-device-scale-factor=4 --window-size=1024,500 \
  --virtual-time-budget=4000 \
  --screenshot="feature-graphic-4k.png" "file://${ROOT}/feature-graphic.html" || true

python3 - <<'PY'
from struct import unpack
from pathlib import Path
p = Path('feature-graphic-4k.png')
assert p.exists() and p.stat().st_size > 1000, '4K render failed'
w, h = unpack('>II', p.read_bytes()[16:24])
print(f'4K PNG {w}x{h}  {p.stat().st_size/1024:.0f} KB')
PY

# Play Console requires exactly 1024x500 — downscale from 4K for extra sharpness
ffmpeg -y -hide_banner -loglevel error -i feature-graphic-4k.png \
  -vf "scale=1024:500:flags=lanczos" -frames:v 1 feature-graphic.png
ffmpeg -y -hide_banner -loglevel error -i feature-graphic-4k.png \
  -vf "scale=1024:500:flags=lanczos" -q:v 2 feature-graphic.jpg
# Also keep a true 4K JPEG
ffmpeg -y -hide_banner -loglevel error -i feature-graphic-4k.png -q:v 2 feature-graphic-4k.jpg

file feature-graphic-4k.png feature-graphic.png
python3 - <<'PY'
from struct import unpack
from pathlib import Path
for name in ['feature-graphic-4k.png','feature-graphic.png']:
    data = Path(name).read_bytes()
    w, h = unpack('>II', data[16:24])
    print(name, f'{w}x{h}', f'{Path(name).stat().st_size/1024:.0f}KB')
PY
ls -lh feature-graphic-4k.png feature-graphic-4k.jpg feature-graphic.png feature-graphic.jpg
