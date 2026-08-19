#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/exports"
mkdir -p "$OUT"

CHROME="${CHROME:-/usr/local/bin/google-chrome}"
run_chrome() {
  local profile="$OUT/.chrome-$1"
  mkdir -p "$profile"
  timeout 35s "$CHROME" \
    --headless=new \
    --disable-gpu \
    --no-sandbox \
    --hide-scrollbars \
    --allow-file-access-from-files \
    --user-data-dir="$profile" \
    --crash-dumps-dir="$profile" \
    --virtual-time-budget=8000 \
    --run-all-compositor-stages-before-draw \
    --font-render-hinting=none \
    --disable-extensions \
    --disable-background-networking \
    --disable-sync \
    --disable-translate \
    --metrics-recording-only \
    --mute-audio \
    --no-first-run \
    "${@:2}" || true
  rm -rf "$profile"
}

# 5in × 7in at 96 CSS px = 480 × 672
# scale 4 → 1920 × 2688 (~384 dpi)
render_card() {
  local name="$1"
  local file="$2"
  run_chrome "$name" \
    --force-device-scale-factor=4 \
    --window-size=480,672 \
    --screenshot="$OUT/${name}.png" \
    "file://$ROOT/print/${file}"
  echo "wrote $OUT/${name}.png ($(wc -c < "$OUT/${name}.png") bytes)"
}

render_pdf() {
  local name="$1"
  local file="$2"
  run_chrome "pdf-$name" \
    --no-pdf-header-footer \
    --print-to-pdf="$OUT/${name}.pdf" \
    "file://$ROOT/print/${file}"
  echo "wrote $OUT/${name}.pdf"
}

render_card "nocturne" "nocturne.html"
render_card "forest" "forest.html"
render_card "ivory" "ivory.html"
render_card "ivory-garden" "ivory-garden.html"
render_card "ivory-blank" "ivory-blank.html"

render_pdf "nocturne" "nocturne.html"
render_pdf "forest" "forest.html"
render_pdf "ivory" "ivory.html"
render_pdf "ivory-blank" "ivory-blank.html"

ls -la "$OUT"
