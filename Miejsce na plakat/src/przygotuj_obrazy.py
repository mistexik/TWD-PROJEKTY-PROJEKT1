"""Przygotowuje obrazy wykresów do plakatu (wymaga Pillow). Uruchom: python przygotuj_obrazy.py
- wykresy z ../../wykresy_plakat: przycina puste (przezroczyste) marginesy -> ../wykresy/
- kartogram ../../kartogram_plakat_R.png: tło (253,254,253) -> przezroczyste, wycina tytuł
  wpisany w obraz (jest nagłówkiem karty na plakacie), przycina marginesy -> ../mapa/kartogram.png
"""
import os
from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.normpath(os.path.join(here, "..", ".."))
plakat = os.path.normpath(os.path.join(here, ".."))


def przytnij(im, pad=30):
    x0, y0, x1, y1 = im.getchannel("A").getbbox()
    return im.crop((max(x0 - pad, 0), max(y0 - pad, 0), min(x1 + pad, im.width), min(y1 + pad, im.height)))


os.makedirs(os.path.join(plakat, "wykresy"), exist_ok=True)
for n in ("01_wynagrodzenia.png", "04_akcje_gpw.png", "06_ceny_mieszkan_pln.png"):
    im = Image.open(os.path.join(repo, "wykresy_plakat", n)).convert("RGBA")
    przytnij(im).save(os.path.join(plakat, "wykresy", n))

BG = (253, 254, 253)
im = Image.open(os.path.join(repo, "kartogram_plakat_R.png")).convert("RGBA")
im.putdata([
    (r, g, b, 0) if max(abs(r - BG[0]), abs(g - BG[1]), abs(b - BG[2])) <= 1 and (r, g, b) != (255, 255, 255)
    else (r, g, b, a)
    for r, g, b, a in im.getdata()
])
im = im.crop((0, 300, im.width, im.height))  # bez tytułu i podtytułu z R
os.makedirs(os.path.join(plakat, "mapa"), exist_ok=True)
przytnij(im).save(os.path.join(plakat, "mapa", "kartogram.png"))
print("ok")
