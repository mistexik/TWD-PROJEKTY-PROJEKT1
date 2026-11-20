from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
import agregacjafinalna as dane

OUTPUT = Path("wykresy_plakat")
OUTPUT.mkdir(exist_ok=True)

GOLD = "#F2C94C"
BLUE_LIGHT = "#6CA6CD"
WHITE = "#FFFFFF"
MUTED = "#A0AEC0"
GRID = "#2A3B55"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "text.color": WHITE,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "xtick.major.pad": 12,
    "ytick.major.pad": 12,
    "legend.frameon": False,
    "legend.fontsize": 11,
})


def pl(val, digits=0, signed=False):
    fmt = f"{val:+,.{digits}f}" if signed else f"{val:,.{digits}f}"
    return fmt.replace(",", " ").replace(".", ",")


def nowa_figura(figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    return fig, ax


# --- 1. WYKRES 01: WYNAGRODZENIA (oś Y od 0) ---
def generuj_wynagrodzenia():
    w = dane.wykres1_zarobki
    fig, ax = nowa_figura((10, 6))
    ax.grid(axis="y", color=GRID, linewidth=0.7, alpha=0.6)

    ax.plot(w["rok"], w["wynagrodzenie_sektor_przedsiebiorstw_zl"], color=GOLD, lw=3, label="Sektor przedsiębiorstw")
    ax.plot(w["rok"], w["wynagrodzenie_gospodarka_narodowa_zl"], color=BLUE_LIGHT, lw=2.5, ls="--", label="Gospodarka narodowa")

    for col, color, dy in [
        ("wynagrodzenie_sektor_przedsiebiorstw_zl", GOLD, -14),
        ("wynagrodzenie_gospodarka_narodowa_zl", BLUE_LIGHT, 14),
    ]:
        val = w[col].iloc[-1]
        ax.scatter([2025], [val], s=50, color=color, zorder=5)
        ax.annotate(f"{pl(val)} zł", xy=(2025, val), xytext=(10, dy),
                    textcoords="offset points", color=color, fontsize=12, weight="bold", va="center")

    ax.set_xlabel("Rok", fontsize=11, labelpad=12)
    ax.set_ylabel("Przeciętne miesięczne wynagrodzenie (zł)", fontsize=11, labelpad=14)
    # Oś Y od 0, a lewy margines osi X (2008.6) odsuwa rok 2010 od zera
    ax.set(xlim=(2008.6, 2026.8), ylim=(0, 10000), xticks=[2010, 2013, 2016, 2019, 2022, 2025])
    ax.yaxis.set_major_locator(MultipleLocator(2000))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: pl(x)))
    ax.legend(loc="upper left", ncol=2, labelcolor=WHITE)

    plt.tight_layout()
    plt.savefig(OUTPUT / "01_wynagrodzenia.png", dpi=300, transparent=True)
    plt.close(fig)


# --- 2. WYKRES 04: AKCJE GPW ---
def generuj_akcje():
    s = dane.wykres2_akcje.sort_values("zmiana_proc")
    fig, ax = nowa_figura((10, 6.5))
    ax.grid(axis="x", color=GRID, linewidth=0.7, alpha=0.6)

    bars = ax.barh(s["Nazwa_2026"], s["zmiana_proc"], height=0.62, color=GOLD)
    ax.axvline(0, color=MUTED, lw=1.2)

    for bar, val in zip(bars, s["zmiana_proc"]):
        offset = 10 if val >= 0 else -10
        ha = "left" if val >= 0 else "right"
        ax.text(val + offset, bar.get_y() + bar.get_height() / 2,
                f"{pl(val, 1, True)}%", va="center", ha=ha, color=WHITE, fontsize=11, weight="bold")

    ax.set_xlabel("Zmiana kursu od 16.10.2020 do 30.10.2026 (%)", fontsize=11, labelpad=12)
    ax.set_ylabel("Spółka (nazwa w 2026 r.)", fontsize=11, labelpad=14)
    ax.set(xlim=(-130, 565))
    ax.xaxis.set_major_locator(MultipleLocator(100))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{pl(x)}%"))
    ax.tick_params(axis="y", colors=WHITE, labelsize=11)

    plt.tight_layout()
    plt.savefig(OUTPUT / "04_akcje_gpw.png", dpi=300, transparent=True)
    plt.close(fig)


# --- 3. WYKRES 06: CENY MIESZKAŃ W ZŁ/M² (oś Y od 0) ---
def generuj_mieszkania():
    h = dane.wykres3_mieszkania
    fig, ax = nowa_figura((10, 6))
    ax.grid(axis="y", color=GRID, linewidth=0.7, alpha=0.6)

    ax.plot(h["rok"], h["cena_nominalna_m2"], color=BLUE_LIGHT, lw=2.8, ls="--", label="Cena nominalna")
    ax.plot(h["rok"], h["cena_realna_m2"], color=GOLD, lw=3, label="Cena realna (po korekcie inflacji)")

    for col, color in [("cena_nominalna_m2", BLUE_LIGHT), ("cena_realna_m2", GOLD)]:
        val = h[col].iloc[-1]
        ax.scatter([2025], [val], s=50, color=color, zorder=5)
        ax.annotate(f"{pl(val)} zł", xy=(2025, val), xytext=(10, 0),
                    textcoords="offset points", color=color, fontsize=12, weight="bold", va="center")

    ax.set_xlabel("Rok", fontsize=11, labelpad=12)
    ax.set_ylabel("Uśredniona cena mieszkania (zł/m²)", fontsize=11, labelpad=14)
    # Oś Y od 0, a lewy margines osi X (2013.8) odsuwa rok 2015 od zera
    ax.set(xlim=(2013.8, 2026.8), ylim=(0, 14000), xticks=range(2015, 2026, 2))
    ax.yaxis.set_major_locator(MultipleLocator(2000))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: pl(x)))
    ax.legend(loc="upper left", ncol=2, labelcolor=WHITE)

    plt.tight_layout()
    plt.savefig(OUTPUT / "06_ceny_mieszkan_pln.png", dpi=300, transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    generuj_wynagrodzenia()
    generuj_akcje()
    generuj_mieszkania()
    print("Gotowe! Wykresy zapisane w folderze:", OUTPUT.resolve())