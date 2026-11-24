import pandas as pd

#WYKRES 1
miesieczne = pd.read_csv("wynagrodzenia_miesieczne.csv")
kwartalne = pd.read_csv("zatrudnienie_wynagrodzenia_kwartalne.csv")
kwartalne.columns = kwartalne.columns.str.strip()

wykres1_zarobki = (
    miesieczne.groupby("rok")["wynagrodzenie_sektor_przedsiebiorstw_zl"].mean().reset_index()
    .merge(
        kwartalne.groupby("rok")["wynagrodzenie_gospodarka_narodowa_zl"].mean().reset_index(),
        on="rok"
    )
)
wykres1_zarobki = wykres1_zarobki[wykres1_zarobki["rok"] <= 2025]

#WYKRES 2
baza = pd.read_csv("baza_akcje_2020_2026.csv")
baza["Suma_Obrotu"] = baza[[f"Obrót_{r}" for r in range(2020, 2027)]].sum(axis=1)

wykres2_akcje = (
    baza[["Nazwa_2026", "Kurs zamknięcia_2020", "Kurs zamknięcia_2026", "Suma_Obrotu"]]
    .dropna()
    .sort_values("Suma_Obrotu", ascending=False)
    .head(10)
    .copy()
)
# Korekta splitu 1:10 dla DINOPL
wykres2_akcje.loc[wykres2_akcje["Nazwa_2026"] == "DINOPL", "Kurs zamknięcia_2026"] *= 10
wykres2_akcje["zmiana_proc"] = (
    (wykres2_akcje["Kurs zamknięcia_2026"] / wykres2_akcje["Kurs zamknięcia_2020"]) - 1
) * 100

#WYKRES 3
mieszkania = pd.read_csv("indeks_cen_mieszkan.csv")
mieszkania_pl = mieszkania[mieszkania["kraj"] == "Poland"][["rok", "indeks_2015_100"]].copy()
mieszkania_pl = pd.concat(
    [pd.DataFrame({"rok": [2015], "indeks_2015_100": [100.0]}), mieszkania_pl],
    ignore_index=True
)

inflacja = pd.read_csv("inflacja_skumulowana.csv", sep=";", decimal=",", encoding="cp1250", usecols=[3, 4])
inflacja.columns = ["rok", "cpi_r_r"]
inflacja = inflacja[inflacja["rok"].between(2016, 2025)].sort_values("rok")
inflacja["wsp_inflacji_2015"] = (inflacja["cpi_r_r"] / 100).cumprod()

wykres3_mieszkania = mieszkania_pl.merge(inflacja[["rok", "wsp_inflacji_2015"]], on="rok", how="left")
wykres3_mieszkania.loc[wykres3_mieszkania["rok"] == 2015, "wsp_inflacji_2015"] = 1.0
wykres3_mieszkania["indeks_nominalny"] = (
    wykres3_mieszkania["indeks_2015_100"] * wykres3_mieszkania["wsp_inflacji_2015"]
)

ceny_2026 = pd.read_csv("Kopia Kopia ceny_mieszkan_polska_2026.csv")
srednia_cena_2026 = ceny_2026["Średnia cena za m² (PLN)"].mean()

cena_bazowa_2015 = srednia_cena_2026 / (wykres3_mieszkania["indeks_nominalny"].iloc[-1] / 100)
wykres3_mieszkania["cena_nominalna_m2"] = cena_bazowa_2015 * (wykres3_mieszkania["indeks_nominalny"] / 100)
wykres3_mieszkania["cena_realna_m2"] = cena_bazowa_2015 * (wykres3_mieszkania["indeks_2015_100"] / 100)