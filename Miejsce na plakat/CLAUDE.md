# Plakat „Portfel Polaka” – instrukcja dla agenta

Plakat na zajęcia z wizualizacji danych (ceny mieszkań, inflacja, wynagrodzenia w Polsce).
Plakat to strona HTML 1240×1754 px (proporcje A4, 150 dpi). Wykresy rysuje własny kod JS jako SVG,
a headless Chrome robi z tego PNG. Komunikuj się z użytkownikiem po polsku.

## Stan prac i wybrany kierunek

1. Najpierw powstało 5 stylów (`src/wariant1-5.html`). Wybrany został **wariant 2**: granat i złoto, art déco,
   czcionki Cinzel (nagłówki) i Raleway (tekst).
2. Do wariantu 2 dodano zdjęcie miasta nocą za tytułem (`src/wariant2_foto.html`). Wybrane zostało **zdjęcie `Obraz1.jpg`**.
3. **Aktualny etap:** wykres „Dynamika cen mieszkań a inflacja” został usunięty, a w jego miejsce weszło
   miejsce na kartogram (mapa Polski z kolorami). Kartogramu jeszcze nie ma, więc są tylko trzy puste ciemne pola:
   `.mapa` (duże pole na mapę), `.legenda` (małe pole na legendę) i `.pole-tekst` (opis, około połowy zwykłego opisu).
   Jest 5 propozycji układu: `src/kartogram1-5.html` → `plakat_kartogram1-5.png`.
   Kolejno: 1 zygzak, 2 kolumna mapy, 3 tryptyk, 4 mapa w nagłówku, 5 przekątna.
   **Właściciel jeszcze nie wybrał układu.** Zapytaj, nad którym pracujesz.

Na plakacie zostają 3 wykresy: Wynagrodzenia, Ceny mieszkań a inflacja, Ceny mieszkań – Polska vs UE.

**Układ 5 (stan na 20.11.2026):** kolejność 1 Wynagrodzenia, 2 Akcje, 3 Ceny mieszkań (nominalne vs realne), 4 Kartogram.
Wykresy to gotowe PNG (rysuje je `kody_i_csv/przygotowaniewykresow.py`), a nie silnik JS.
`src/przygotuj_obrazy.py` przycina je do `wykresy/` i robi `mapa/kartogram.png` z `kartogram_plakat_R.png`
(przezroczyste tło, wycięty tytuł z R, bo tytuł jest nagłówkiem karty). Po zmianie PNG uruchom go ponownie.
Opisy `TEKSTY.akcje.d` i `TEKSTY.mapa.d` napisał Claude na prośbę właściciela, na podstawie liczb z wykresów;
autorzy mają je sprawdzić.

## Zasady ustalone z autorami (przestrzegaj ich)

- **Nie dodawaj żadnych tekstów spoza oryginalnego plakatu.** Dozwolone są tylko: tytuł, podtytuł, „Źródła: …”,
  tytuły i opisy wykresów, „Najważniejsze wnioski” z punktami 1… 2… 3…, „Autorzy:”. Na wykresach mogą być
  tylko legenda, osie i wartości z ostatniego roku. Bez numeracji sekcji, etykiet, haseł i podpisów.
- Wszystkie teksty są w jednym miejscu: obiekt `TEKSTY` w `src/common.js`. Zmieniaj je tylko tam.
- Wykresy mają tło wtopione w ciemny plakat, nigdy białe.
- Przed generowaniem większej rzeczy albo instalowaniem czegokolwiek zapytaj użytkownika.
  Wcześniej przerwał instalację pakietów pip, więc nie instaluj nic bez zgody.
- **Znana niezgodność do zgłoszenia, nie do cichego poprawiania:** w opisie dynamiki (obecnie nieużywanym) jest
  „spadła do 1,5%”, a w danych za 2025 jest 1,0%.

## Pliki

```
Miejsce na plakat/
  CLAUDE.md               ten plik
  zdjecia/Obraz1-3.jpg    zdjęcia miasta. Małe (516–738 px szer.), więc na wydruku A3+ będą miękkie.
                          Obraz3 to najpewniej Nowy Jork, nie polskie miasto.
  plakat_*.png            wyrenderowane podglądy
  druk/                   PDF A4 i PNG 3× dla wariantów 1–5 (stara seria, NIESPRAWDZONE wizualnie)
  src/
    common.js             TEKSTY, ikony SVG (portfel, słupki) i silnik wykresów: wykres(), rysujWszystkie(), start()
    dane.js               gotowe dane wykresów (const DANE). Plakaty działają bez CSV.
    dane.py               przelicza dane.js z CSV w ../../projekt1km2 (tego folderu może nie być u Ciebie)
    v2baza.css / .js      wspólny styl i skrypt wersji „wariant 2 + zdjęcie” (używane przez kartogram*.html)
    gen_kartogram.py      GENERATOR kartogram1-5.html. Edytuj ten plik, nie wygenerowane HTML-e.
    kartogram1-5.html     wygenerowane układy z miejscem na kartogram (aktualny etap)
    wariant1-5.html       pierwsza seria stylów (archiwum, wariant 2 to baza)
    wariant2_foto.html    wariant 2 ze zdjęciem (pełne 4 wykresy, stary etap)
    druk.css              styl wydruku: strona A4 bez marginesów, skalowanie 0.64
    render.sh             wariantN.html → plakat_wariantN.png
    render_kartogram.sh   kartogramN.html → plakat_kartogramN.png (zawsze z Obraz1.jpg)
    render_druk.sh        wariantN.html → druk/*.pdf i *_300dpi.png
```

## Jak pracować

Wymagania: Git Bash (skrypty używają `sh` i `cygpath`), Google Chrome, Python 3 (tylko biblioteka standardowa),
internet (czcionki z Google Fonts; bez sieci będą czcionki zastępcze).
Ścieżka do Chrome jest wpisana w skryptach `render*.sh` (`/c/Program Files/Google/Chrome/Application/chrome.exe`).
Jeśli Chrome jest gdzie indziej albo system nie jest Windowsem, popraw zmienną `CH`.

```sh
cd "Miejsce na plakat/src"
python gen_kartogram.py              # po zmianie układów kartogramu
sh render_kartogram.sh 1 2 3 4 5     # PNG do ../plakat_kartogramN.png
```

Po każdej zmianie wyrenderuj PNG i **obejrzyj go** (Read na pliku PNG). Sprawdź, czy nic nie wychodzi poza plakat,
czy legenda się nie nakłada i czy tekst opisów się mieści. Plakat ma stały rozmiar 1240×1754 i `overflow:hidden`,
więc nadmiar treści po prostu znika.

Zdjęcie i jego kadr ustawia się parametrami adresu: `kartogram2.html?foto=Obraz1.jpg&pos=50%25%2045%25`.

## Silnik wykresów (src/common.js)

`wykres(kontener, opt)` rysuje SVG o rozmiarze kontenera, więc rozmiar wykresu zależy od CSS układu.
Opcje: `x` (lata), `series` [{name, values, color, width, dash, area (krycie gradientu), type:'bar', dots, labelFmt, noLabel}],
`band` (wypełnienie między seriami), `ref` (linia odniesienia), `endLabels`, `yFmt`, `theme`.
`rysujWszystkie()` szuka elementów `#w-wyn`, `#w-infl`, `#w-dyn`, `#w-ue` i pomija te, których brak.
Wykres wynagrodzeń jest przycięty do 2025 r. (w danych jest też niepełny 2026).

Paleta wariantu 2 (w `v2baza.css` / `v2baza.js`):
- tło: `linear-gradient(180deg, #0f1a3d 0%, #070d22 55%)` plus poświata `radial-gradient(900px 600px at 50% 0%, #1b2a5c, transparent 70%)`
- złoto `#d9b25f` (ciemne `#8f6a26`), tekst `#e9e7f0`, przygaszony `#9aa2c0`
- serie: złota `#e5bd62`, niebieska `#7fb2ff`, różowa (inflacja) `#ff7a8a`
- siatka `rgba(154,162,192,.16)` przerywana, linia odniesienia `rgba(217,178,95,.6)`

## Wstawianie kartogramu, gdy będzie gotowy

Mapę najlepiej wstawić jako obraz z przezroczystym tłem (PNG lub SVG), np. do `zdjecia/` albo nowego `mapa/`.
W `gen_kartogram.py` wstaw `<img>` do `<div class="mapa">` (np. `object-fit:contain`, 100% wymiarów), to samo
zrób z legendą, potem wygeneruj i wyrenderuj od nowa. Pole tekstowe wypełnij przez `TEKSTY` w `common.js`
(dodaj nowy klucz) i atrybut `data-t`. Treść tekstu musi pochodzić od autorów, nie wymyślaj jej.
Najlepiej pasują układy 2, 3 i 5, bo pole mapy jest tam prawie kwadratowe, jak kształt Polski.

## Druk

`druk.css` jest podpięty do wariantów i do kartogramów; przy drukowaniu skaluje plakat do strony A4.
Do kartogramów nie ma jeszcze skryptu druku: skopiuj `render_druk.sh` i podmień nazwy plików.
PDF zachowuje wektorowe wykresy i tekst. Przed oddaniem do druku obejrzyj PDF, bo pliki w `druk/` nie były sprawdzane.
