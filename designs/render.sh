#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/exports"
mkdir -p "$OUT"

CHROME="${CHROME:-/usr/bin/google-chrome-stable}"
COMMON=(--headless=new --disable-gpu --no-sandbox --hide-scrollbars --allow-file-access-from-files)

render_png() {
  local name="$1"
  local file="$2"
  "$CHROME" "${COMMON[@]}" \
    --force-device-scale-factor=3 \
    --window-size=816,1056 \
    --screenshot="$OUT/${name}.png" \
    "file://$ROOT/$file"
  echo "wrote $OUT/${name}.png"
}

render_pdf() {
  local name="$1"
  local file="$2"
  "$CHROME" "${COMMON[@]}" \
    --no-pdf-header-footer \
    --print-to-pdf="$OUT/${name}.pdf" \
    "file://$ROOT/$file"
  echo "wrote $OUT/${name}.pdf"
}

render_png "primary-filled" "primary-filled.html"
render_png "primary-blank" "primary-blank.html"
render_png "heritage-filled" "heritage-filled.html"

render_pdf "primary-filled" "primary-filled.html"
render_pdf "primary-blank" "primary-blank.html"
render_pdf "heritage-filled" "heritage-filled.html"

"$CHROME" "${COMMON[@]}" \
  --force-device-scale-factor=1 \
  --window-size=2000,2000 \
  --screenshot="$OUT/listing-mockup.png" \
  "file://$ROOT/listing-mockup.html"
echo "wrote $OUT/listing-mockup.png"

ls -la "$OUT"
