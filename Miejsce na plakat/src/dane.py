"""Liczy dane do wykresów plakatu (tylko biblioteka standardowa) i zapisuje dane.js."""
import csv, json, os
from collections import defaultdict
D = os.path.join(os.path.dirname(__file__), "..", "..", "projekt1km2")
PL, UE = "Poland", "European Union - 27 countries (from 2020)"

def rd(name, **kw):
    with open(os.path.join(D, name), encoding=kw.pop("enc", "utf-8"), newline="") as f:
        return list(csv.reader(f, **kw))

# 1. wynagrodzenia (średnie roczne)
m = defaultdict(list)
for r in rd("wynagrodzenia_miesieczne.csv")[1:]:
    m[int(r[0])].append(float(r[2]))
q = defaultdict(list)
for r in rd("zatrudnienie_wynagrodzenia_kwartalne.csv")[1:]:
    if r and r[4].strip(): q[int(r[0])].append(float(r[4]))
lata = sorted(set(m) & set(q))
wyn = {"rok": lata,
       "przeds": [round(sum(m[y]) / len(m[y])) for y in lata],
       "gosp": [round(sum(q[y]) / len(q[y])) for y in lata]}

# indeks + zmiana r/r
idx, zm = defaultdict(dict), defaultdict(dict)
for r in rd("indeks_cen_mieszkan.csv")[1:]:
    if r[2]: idx[r[0]][int(r[1])] = float(r[2])
for r in rd("zmiana_cen_mieszkan.csv")[1:]:
    if r[2]: zm[r[0]][int(r[1])] = float(r[2])
cpi = {}
for r in rd("inflacja_skumulowana.csv", enc="cp1250", delimiter=";")[1:]:
    cpi[int(r[3])] = float(r[4].replace(",", "."))
rok = list(range(2015, 2026))
idx[PL][2015] = idx[UE][2015] = 100.0
wsp, acc = [], 1.0
for y in rok:
    if y > 2015: acc *= cpi[y] / 100
    wsp.append(acc)
mieszk = {"rok": rok,
          "pl": [idx[PL][y] for y in rok],
          "ue": [idx[UE][y] for y in rok],
          "pl_nom": [round(idx[PL][y] * w, 1) for y, w in zip(rok, wsp)],
          "cpi_skum": [round(100 * w, 1) for w in wsp]}
rok2 = list(range(2016, 2026))
dyn = {"rok": rok2,
       "pl": [zm[PL][y] for y in rok2],
       "ue": [zm[UE][y] for y in rok2],
       "cpi": [round(cpi[y] - 100, 1) for y in rok2]}
out = {"wyn": wyn, "mieszk": mieszk, "dyn": dyn}
with open(os.path.join(os.path.dirname(__file__), "dane.js"), "w", encoding="utf-8") as f:
    f.write("const DANE = " + json.dumps(out) + ";\n")
print(json.dumps(out, indent=1))
