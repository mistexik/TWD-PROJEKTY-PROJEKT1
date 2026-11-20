#!/bin/sh
# Renderuje src/wariantN.html do PNG (1240x1754 = A4 przy 150 dpi) headless Chrome.
cd "$(dirname "$0")/.."
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
for n in "$@"; do
  "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=1240,1754 --virtual-time-budget=8000 --allow-file-access-from-files \
    --screenshot="$(cygpath -w "$PWD/plakat_wariant$n.png")" "file:///$(cygpath -m "$PWD/src/wariant$n.html")" 2>/dev/null
done
