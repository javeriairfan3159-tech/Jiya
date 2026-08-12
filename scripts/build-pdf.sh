#!/usr/bin/env bash
#
# Render the Meadow Shell Market Tote HTML pattern into the print-ready A4 PDF.
#
# Usage:
#   scripts/build-pdf.sh [output.pdf]
#
# With no argument the PDF is written to output/Meadow_Shell_Market_Tote_FIXED.pdf.
#
# Notes:
#   Headless Chrome finishes writing the PDF within a second or two, but in
#   sandboxed/container environments it often does not exit on its own (its
#   background networking keeps the process alive). We therefore run it under
#   `timeout` and then verify the PDF was actually produced, rather than relying
#   on Chrome's own exit code.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
html="$repo_root/pattern/meadow-shell-market-tote.html"
out="${1:-$repo_root/output/Meadow_Shell_Market_Tote_FIXED.pdf}"

# Locate a Chrome/Chromium binary.
chrome_bin=""
for c in google-chrome google-chrome-stable chromium chromium-browser; do
  if command -v "$c" >/dev/null 2>&1; then
    chrome_bin="$c"
    break
  fi
done
if [[ -z "$chrome_bin" ]]; then
  echo "error: no Chrome/Chromium binary found (need google-chrome or chromium)." >&2
  exit 1
fi

if [[ ! -f "$html" ]]; then
  echo "error: pattern HTML not found at $html" >&2
  exit 1
fi

mkdir -p "$(dirname "$out")"
rm -f "$out"

profile_dir="$(mktemp -d)"
chrome_pid=""
cleanup() {
  if [[ -n "$chrome_pid" ]] && kill -0 "$chrome_pid" 2>/dev/null; then
    kill "$chrome_pid" 2>/dev/null || true
    sleep 1
    kill -9 "$chrome_pid" 2>/dev/null || true
  fi
  rm -rf "$profile_dir"
}
trap cleanup EXIT

echo "Rendering $html -> $out using $chrome_bin ..."
# Chrome writes the PDF within a second or two but frequently does not exit on
# its own in sandboxed environments, so run it in the background and stop it
# once the output file has been written and its size has stabilised.
"$chrome_bin" \
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --no-first-run \
  --no-default-browser-check \
  --disable-background-networking \
  --user-data-dir="$profile_dir" \
  --print-to-pdf="$out" \
  --no-pdf-header-footer \
  "file://$html" >/dev/null 2>&1 &
chrome_pid=$!

deadline=$((SECONDS + 120))
last_size=-1
stable=0
while (( SECONDS < deadline )); do
  if ! kill -0 "$chrome_pid" 2>/dev/null; then
    break
  fi
  if [[ -s "$out" ]]; then
    cur_size="$(stat -c %s "$out" 2>/dev/null || echo 0)"
    if [[ "$cur_size" == "$last_size" ]]; then
      stable=$((stable + 1))
      # Two consecutive stable, non-zero readings means the write is complete.
      if (( stable >= 2 )); then
        break
      fi
    else
      stable=0
      last_size="$cur_size"
    fi
  fi
  sleep 1
done

if [[ ! -s "$out" ]]; then
  echo "error: PDF was not produced at $out" >&2
  exit 1
fi

size="$(stat -c %s "$out")"
echo "OK: wrote $out ($size bytes)."
