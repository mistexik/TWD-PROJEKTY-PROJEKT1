#!/bin/sh
# Renderuje kartogramN.html (zdjęcie: Obraz1) do plakat_kartogramN.png.
cd "$(dirname "$0")/.."
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
for n in "$@"; do
  "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1240,1754 \
    --virtual-time-budget=8000 --allow-file-access-from-files \
    --screenshot="$(cygpath -w "$PWD/plakat_kartogram$n.png")" "file:///$(cygpath -m "$PWD/src/kartogram$n.html")?foto=Obraz1.jpg" 2>/dev/null
done
