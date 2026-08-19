#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
CHROME="${CHROME:-google-chrome}"
USER_DATA="$(mktemp -d /tmp/chrome-play-XXXXXX)"
PORT=9450
render() {
  local html="$1" out="$2"
  PORT=$((PORT + 1))
  echo "Rendering $html -> $out"
  timeout 18s "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-sandbox \
    --user-data-dir="$USER_DATA" \
    --remote-debugging-port="$PORT" \
    --disable-background-networking --disable-sync \
    --force-device-scale-factor=1 --window-size=1024,500 \
    --virtual-time-budget=3000 \
    --screenshot="$out" "file://${ROOT}/${html}" || true
  python3 - <<PY
from pathlib import Path
p = Path("$out")
print(p, p.exists(), p.stat().st_size if p.exists() else 0)
PY
}
render feature-graphic.html feature-graphic.png
# Exact 1024x500 JPEG fallback under 15MB
ffmpeg -y -hide_banner -loglevel error -i feature-graphic.png -q:v 2 feature-graphic.jpg
file feature-graphic.png feature-graphic.jpg
identify feature-graphic.png 2>/dev/null || python3 - <<'PY'
from struct import unpack
from pathlib import Path
data = Path('feature-graphic.png').read_bytes()
w, h = unpack('>II', data[16:24])
print(f'PNG {w}x{h}')
PY
ls -lh feature-graphic.png feature-graphic.jpg
