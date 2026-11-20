#!/bin/sh
# Wersje do druku: PDF A4 (wektorowy) i PNG 3720x5262 (A4 ~450 dpi / A3 ~300 dpi) w folderze druk/.
cd "$(dirname "$0")/.."
mkdir -p druk
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
for n in "${@:-1 2 3 4 5}"; do
  URL="file:///$(cygpath -m "$PWD/src/wariant$n.html")"
  "$CH" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 \
    --window-size=1240,1754 --print-to-pdf="$(cygpath -w "$PWD/druk/plakat_wariant$n.pdf")" "$URL" 2>/dev/null
  "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=3 \
    --window-size=1240,1754 --virtual-time-budget=8000 \
    --screenshot="$(cygpath -w "$PWD/druk/plakat_wariant${n}_300dpi.png")" "$URL" 2>/dev/null
done
