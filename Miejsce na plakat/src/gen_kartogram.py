"""Generuje kartogram1..5.html: wariant 2 ze zdjęciem miasta, bez wykresu dynamiki,
z miejscem na kartogram (mapa + legenda + krótki opis). Uruchom: python gen_kartogram.py"""
import os

HEAD = """<!doctype html>
<html lang="pl"><head><meta charset="utf-8">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Raleway:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="v2baza.css">
<link rel="stylesheet" href="druk.css">
<style>
{css}
</style></head>
<body>
<div class="foto" id="foto"><div class="tint"></div></div>
<div class="ramka"></div>
"""
TAIL = """<script src="dane.js"></script><script src="common.js"></script><script src="v2baza.js"></script>
</body></html>
"""
HEADER = """<header>
  <div class="ikona" id="ikona"></div>
  <h1><span data-t="t1"></span> <span data-t="t2"></span></h1>
  <div class="pod" data-t="pod"></div>
  <div class="orn"><i></i><b></b><i></i></div>
  <div class="zr" data-t="zrodla"></div>
</header>
"""
WNIOSKI = """<section class="wnioski">
  <div class="ik" id="ik2"></div>
  <div><h3 data-t="wnioski"></h3><ul><li>1...</li><li>2...</li><li>3...</li></ul></div>
</section>
"""
FOOTER = '<footer data-t="autorzy"></footer>\n'


def karta(k, cls=""):
    return (f'<section class="karta k-{k} {cls}"><h2 data-t="{k}.t"></h2>'
            f'<div class="w" id="w-{k}"></div><p data-t="{k}.d"></p></section>')


def rzad(k, odw=False):
    """Wiersz: wykres + opis obok (jak w wariancie 2)."""
    return (f'<section class="rz{" odw" if odw else ""}"><div class="w" id="w-{k}"></div>'
            f'<div class="opis"><h2 data-t="{k}.t"></h2><p data-t="{k}.d"></p></div></section>')


RZ_CSS = """.rz{display:grid;grid-template-columns:1.45fr 1fr;gap:30px;min-height:0;padding:14px 0;border-top:1px solid var(--line)}
.rz.odw{grid-template-columns:1fr 1.45fr}
.rz.odw .w{order:2;border-left:none;border-right:3px solid var(--gold)}
.opis{display:flex;flex-direction:column;justify-content:center;gap:12px}"""

UKLADY = {}

# 1. Zygzak – jak dotychczas, kartogram jako szerszy wiersz
UKLADY[1] = ("Kartogram 1 – zygzak", RZ_CSS + """
main{display:grid;grid-template-rows:1fr 1fr 1.45fr 1fr;gap:12px}
.rz-mapa{display:grid;grid-template-columns:1fr 1fr;gap:30px;padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);min-height:0}
.rz-mapa .bok{display:flex;flex-direction:column;justify-content:center;gap:18px}
.rz-mapa .legenda{height:120px;width:70%}
.rz-mapa .pole-tekst{height:84px}
""", HEADER + "<main>\n" + rzad("wyn") + rzad("infl", True)
     + '<section class="rz-mapa"><div class="mapa"></div><div class="bok"><div class="legenda"></div><div class="pole-tekst"></div></div></section>'
     + rzad("ue", True) + "</main>\n" + WNIOSKI + FOOTER)

# 2. Bento – kolumna mapy z wnioskami po lewej, trzy wykresy po prawej
UKLADY[2] = ("Kartogram 2 – kolumna mapy", """
main{display:grid;grid-template-columns:1.08fr 1fr;gap:34px;margin-bottom:6px}
.lewa{display:flex;flex-direction:column;gap:16px;min-height:0}
.lewa .mapa{flex:none;aspect-ratio:1/0.98}
.lewa .pod-mapa{display:grid;grid-template-columns:.8fr 1.2fr;gap:16px;height:96px}
.lewa .wnioski{flex:1;height:auto;padding:22px 28px}
.prawa{display:grid;grid-template-rows:1fr 1fr 1fr;gap:18px;min-height:0}
.prawa .karta{border-top:1px solid var(--line);padding-top:14px;gap:8px}
.prawa .karta:first-child{border-top:none;padding-top:0}
.prawa h2{font-size:24px}
.prawa p{font-size:14.5px;line-height:1.5}
""", HEADER + '<main><div class="lewa"><div class="mapa"></div><div class="pod-mapa"><div class="legenda"></div><div class="pole-tekst"></div></div>'
     + WNIOSKI + '</div><div class="prawa">' + karta("wyn") + karta("infl") + karta("ue") + "</div></main>\n" + FOOTER)

# 3. Tryptyk – dwa wykresy obok siebie, pas z mapą pośrodku, wykres UE na dole
UKLADY[3] = ("Kartogram 3 – tryptyk", RZ_CSS + """
.ikona{width:118px}
h1{font-size:86px;letter-spacing:12px}
.pod{font-size:25px;margin-top:10px}
.orn{margin:10px auto 6px}
body{--foto-h:400px}
main{display:grid;grid-template-rows:1.2fr 1.25fr .85fr;gap:20px}
.gora{display:grid;grid-template-columns:1fr 1fr;gap:34px;min-height:0}
.gora h2{font-size:24px}.gora p{font-size:14.5px;line-height:1.5}
.gora .karta{gap:8px}
.pas{display:grid;grid-template-columns:1fr 1.5fr 1fr;gap:30px;align-items:center;padding:20px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);min-height:0;
 background:radial-gradient(ellipse 50% 60% at 50% 50%,rgba(217,178,95,.07),transparent)}
.pas .mapa{height:100%}
.pas .legenda{height:150px}
.pas .pole-tekst{height:110px}
.rz{border-top:none;padding:0}
.wnioski{height:150px}
""", HEADER + '<main><div class="gora">' + karta("wyn") + karta("infl") + "</div>"
     + '<section class="pas"><div class="legenda"></div><div class="mapa"></div><div class="pole-tekst"></div></section>'
     + rzad("ue") + "</main>\n" + WNIOSKI + FOOTER)

# 4. Mapa w nagłówku – tytuł po lewej, kartogram na zdjęciu po prawej, trzy wykresy w kolumnach
UKLADY[4] = ("Kartogram 4 – mapa w nagłówku", """
body{--foto-h:860px;--tint-x:28%}
.foto .tint{background:linear-gradient(90deg,rgba(7,13,34,.72) 0%,rgba(7,13,34,.25) 55%,rgba(7,13,34,.55) 100%),
 linear-gradient(180deg,rgba(15,26,61,.35) 0%,rgba(15,26,61,.15) 30%,rgba(15,26,61,.55) 70%,rgba(15,26,61,.9) 100%)}
.top{display:grid;grid-template-columns:1fr 440px;gap:34px;height:760px;position:relative}
.pod{font-size:25px}
header{text-align:left;display:flex;flex-direction:column;justify-content:center}
.ikona{margin:0 0 18px;width:140px}
h1{font-size:112px;letter-spacing:10px;line-height:1.02}
.orn{margin:18px 0 10px;width:100%}
.orn i:first-child{display:none}
.blok-mapy{display:flex;flex-direction:column;justify-content:center;gap:14px}
.blok-mapy .mapa{flex:1;max-height:520px;background:radial-gradient(ellipse at 50% 45%,rgba(20,32,72,.5),rgba(3,6,18,.8));backdrop-filter:blur(6px)}
.blok-mapy .dol{display:grid;grid-template-columns:.85fr 1.15fr;gap:14px;height:96px}
main{display:grid;grid-template-columns:1fr 1fr 1fr;gap:30px;margin-top:26px}
.karta{gap:10px}
main h2{font-size:23px}
main p{font-size:14.5px;line-height:1.5}
.wnioski{height:200px}
""", '<div class="top">' + HEADER.replace("<h1><span data-t=\"t1\"></span> <span", "<h1><span data-t=\"t1\"></span><br><span")
     + '<div class="blok-mapy"><div class="mapa"></div><div class="dol"><div class="legenda"></div><div class="pole-tekst"></div></div></div></div>\n'
     + "<main>" + karta("wyn") + karta("infl") + karta("ue") + "</main>\n" + WNIOSKI + FOOTER)

def karta_img(k, plik):
    """Karta z gotowym wykresem PNG (z przezroczystym tłem) zamiast wykresu rysowanego w JS."""
    return (f'<section class="karta k-{k}"><h2 data-t="{k}.t"></h2>'
            f'<div class="w"><img src="{plik}" alt=""></div><p data-t="{k}.d"></p></section>')


# 5. Przekątna – kolejność: 1 Wynagrodzenia, 2 Akcje, 3 Ceny mieszkań, 4 Kartogram.
#    Obrazy przygotowuje przygotuj_obrazy.py (przycięte wykresy w ../wykresy, kartogram w ../mapa).
UKLADY[5] = ("Kartogram 5 – przekątna", """
main{display:grid;grid-template-rows:1fr 1.15fr;gap:20px}
.rzad{display:grid;gap:34px;min-height:0}
.rzad.r1{grid-template-columns:1.2fr 1fr}
.rzad.r2{grid-template-columns:1fr 1.2fr;padding-top:18px;border-top:1px solid var(--line)}
.w img{width:100%;height:100%;object-fit:contain;display:block}
.k-mapa .w{padding:12px 10px 8px;background:radial-gradient(ellipse at 45% 50%,rgba(217,178,95,.07),transparent 70%)}
.karta{gap:10px}
h2{font-size:24px}
p{font-size:14.5px;line-height:1.5}
.wnioski{height:160px}
""", HEADER + '<main><div class="rzad r1">'
     + karta_img("wyn", "../wykresy/01_wynagrodzenia.png")
     + karta_img("akcje", "../wykresy/04_akcje_gpw.png")
     + '</div><div class="rzad r2">'
     + karta_img("infl", "../wykresy/06_ceny_mieszkan_pln.png")
     + karta_img("mapa", "../mapa/kartogram.png")
     + "</div></main>\n" + WNIOSKI + FOOTER)

here = os.path.dirname(os.path.abspath(__file__))
for n, (title, css, body) in UKLADY.items():
    with open(os.path.join(here, f"kartogram{n}.html"), "w", encoding="utf-8") as f:
        f.write(HEAD.format(title=title, css=css.strip()) + body + TAIL)
print("ok", len(UKLADY))
