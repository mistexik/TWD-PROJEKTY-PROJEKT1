// Wspólne teksty, ikony i rysowanie wykresów (SVG) dla wszystkich wariantów plakatu.
const TEKSTY = {
  t1: "PORTFEL",
  t2: "POLAKA",
  pod: "Na co wydajemy, ile zarabiamy i oszczędzamy?",
  zrodla: "Źródła: ..., ..., ..",
  wnioski: "Najważniejsze wnioski",
  autorzy: "Autorzy:",
  wyn: {
    t: "Wynagrodzenia",
    d: "Przeciętne wynagrodzenia w Polsce w latach 2010–2025 rosły systematycznie, osiągając zbliżony poziom w sektorze przedsiębiorstw i całej gospodarce narodowej (niecałe 9 tys. zł w 2025 r.). Po 2021 roku można zaobserwować wyraźne przyspieszenie tempa wzrostu płac nominalnych.",
  },
  infl: {
    t: "Ceny mieszkań a inflacja",
    d: "Skorygowanie nominalnego wzrostu cen mieszkań o poziom inflacji pokazuje, że realny wzrost wartości nieruchomości był znacznie łagodniejszy niż sugerują to same kwoty w złotówkach. Mimo to, od 2015 roku nieruchomości w Polsce realnie zyskały na wartości ponad 41%, skutecznie chroniąc kapitał przed utratą siły nabywczej.",
  },
  dyn: {
    t: "Dynamika cen mieszkań a inflacja",
    d: "W 2024 roku polski rynek nieruchomości zanotował bardzo gwałtowny skok realnych cen o 11,2% rok do roku. W roku 2025 sytuacja uległa ustabilizowaniu, a dynamika wzrostu spadła do 1,5%, zbliżając się do średniej unijnej.",
  },
  ue: {
    t: "Ceny mieszkań – Polska vs UE",
    d: "Realne ceny mieszkań w Polsce rosły znacznie szybciej niż średnia unijna, osiągając w 2025 roku indeks na poziomie blisko 142 pkt (względem roku bazowego 2015). Podczas gdy rynek w UE-27 ustabilizował się po 2021 roku, w Polsce po chwilowym spowolnieniu nastąpił kolejny silny wzrost.",
  },
};

// Wypełnia elementy z atrybutem data-t="klucz" lub "klucz.pole".
function wstawTeksty() {
  document.querySelectorAll("[data-t]").forEach((el) => {
    const v = el.dataset.t.split(".").reduce((o, k) => o[k], TEKSTY);
    el.textContent = v;
  });
}

// Ikona portfela z monetami (bez tekstu poza "zł" z oryginału).
function ikonaPortfela(c) {
  const g = c.gold, d = c.goldDark, bg = c.bg || "none";
  return `<svg viewBox="0 0 240 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="pg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${g}"/><stop offset="1" stop-color="${d}"/></linearGradient>
    <linearGradient id="pg2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${g}"/><stop offset="1" stop-color="${d}"/></linearGradient>
  </defs>
  <rect x="30" y="38" width="170" height="118" rx="20" fill="${bg}" stroke="url(#pg1)" stroke-width="7"/>
  <path d="M48 38 L150 10 L172 38" fill="none" stroke="url(#pg1)" stroke-width="6" stroke-linejoin="round"/>
  <rect x="146" y="74" width="66" height="46" rx="12" fill="${bg}" stroke="url(#pg1)" stroke-width="6"/>
  <circle cx="168" cy="97" r="7" fill="url(#pg1)"/>
  <g>
    <ellipse cx="78" cy="186" rx="38" ry="10" fill="url(#pg2)"/>
    <rect x="40" y="168" width="76" height="18" fill="url(#pg2)"/>
    <ellipse cx="78" cy="168" rx="38" ry="10" fill="${g}" stroke="${d}" stroke-width="2"/>
    <rect x="40" y="152" width="76" height="16" fill="url(#pg2)"/>
    <ellipse cx="78" cy="152" rx="38" ry="10" fill="${g}" stroke="${d}" stroke-width="2"/>
    <circle cx="70" cy="118" r="34" fill="url(#pg1)" stroke="${d}" stroke-width="3"/>
    <circle cx="70" cy="118" r="26" fill="none" stroke="${d}" stroke-width="2" opacity=".7"/>
    <text x="70" y="128" text-anchor="middle" font-family="Georgia, serif" font-weight="700" font-size="28" fill="${d}">zł</text>
  </g>
</svg>`;
}

// Ikona słupków (sekcja wniosków).
function ikonaSlupkow(color) {
  return `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="${color}" stroke-width="4" stroke-linecap="round">
  <circle cx="50" cy="50" r="46"/>
  <rect x="27" y="55" width="11" height="20" rx="2"/><rect x="44.5" y="43" width="11" height="32" rx="2"/><rect x="62" y="30" width="11" height="45" rx="2"/>
</svg>`;
}

// ---------- wykresy ----------
const NS = "http://www.w3.org/2000/svg";
let _gid = 0;
function el(tag, attrs, parent, text) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (text !== undefined) e.textContent = text;
  if (parent) parent.appendChild(e);
  return e;
}
function niceStep(range, n) {
  const raw = range / n, p = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / p;
  return (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * p;
}
const fmtPL = (v) => v.toLocaleString("pl-PL").replace(/ /g, " ");
const fmt1 = (v) => v.toLocaleString("pl-PL", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

/*
 opt: {
   x: [lata], series: [{name, values, color, width, dash, area, type:'line'|'bar', dots}],
   band: {from, to, color}  // wypełnienie między dwiema seriami
   ref: liczba (linia odniesienia), yFmt, endLabels, legend, theme
 }
 theme: {text, muted, grid, axis, font, fs, glow, dotFill}
*/
function wykres(container, opt) {
  if (!container) return; // np. wykres usunięty z danego układu
  const th = opt.theme;
  const W = container.clientWidth, H = container.clientHeight;
  container.innerHTML = "";
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, style: "display:block;overflow:visible" }, container);
  const defs = el("defs", {}, svg);
  const fs = th.fs || 15;
  const m = { l: opt.ml || 58, r: opt.endLabels ? 66 : 14, t: 12, b: fs * 2.2 };
  if (opt.legend !== false) {
    let lx = m.l, row = 0;
    opt.series.forEach((s) => {
      const sw = s.type === "bar" ? fs * 0.9 : fs * 1.5;
      const g = el("g", {}, svg);
      const t = el("text", { x: 0, y: 0, fill: th.text, "font-size": fs, "font-family": th.font }, g, s.name);
      const wItem = sw + 7 + t.getComputedTextLength();
      if (lx > m.l && lx + wItem > W - 4) { lx = m.l; row++; }
      const ly = fs * 0.9 + row * fs * 1.6;
      t.setAttribute("x", lx + sw + 7); t.setAttribute("y", ly + fs * 0.35);
      if (s.type === "bar") el("rect", { x: lx, y: ly - fs * 0.45, width: fs * 0.9, height: fs * 0.9, rx: 2, fill: s.color }, g);
      else {
        const l = el("line", { x1: lx, x2: lx + fs * 1.5, y1: ly, y2: ly, stroke: s.color, "stroke-width": 3.5, "stroke-linecap": "round" }, g);
        if (s.dash) l.setAttribute("stroke-dasharray", s.dash);
      }
      lx += wItem + fs * 1.3;
    });
    m.t = fs * 2.6 + row * fs * 1.6;
  }
  const iw = W - m.l - m.r, ih = H - m.t - m.b;
  const all = opt.series.flatMap((s) => s.values).concat(opt.ref !== undefined ? [opt.ref] : []);
  const hasBar = opt.series.some((s) => s.type === "bar");
  let lo = Math.min(...all), hi = Math.max(...all);
  if (hasBar) { lo = Math.min(lo, 0); hi = Math.max(hi, 0); }
  if (opt.yMin !== undefined) lo = opt.yMin;
  const step = niceStep(hi - lo, opt.ticks || 4);
  lo = Math.floor(lo / step) * step; hi = Math.ceil(hi / step) * step;
  const n = opt.x.length;
  const band = iw / n;
  const X = (i) => m.l + band * (i + 0.5);
  const Y = (v) => m.t + ih - ((v - lo) / (hi - lo)) * ih;
  const yFmt = opt.yFmt || fmtPL;

  if (th.glow) {
    const f = el("filter", { id: "glow" + _gid, x: "-20%", y: "-20%", width: "140%", height: "140%" }, defs);
    el("feGaussianBlur", { stdDeviation: th.glow, result: "b" }, f);
    const mg = el("feMerge", {}, f);
    el("feMergeNode", { in: "b" }, mg); el("feMergeNode", { in: "SourceGraphic" }, mg);
  }
  const glowId = "glow" + _gid;

  // siatka + oś Y
  for (let v = lo; v <= hi + 1e-9; v += step) {
    const y = Y(v);
    el("line", { x1: m.l, x2: m.l + iw, y1: y, y2: y, stroke: th.grid, "stroke-width": 1, "stroke-dasharray": th.gridDash || "3 5" }, svg);
    el("text", { x: m.l - 10, y: y + fs * 0.35, "text-anchor": "end", fill: th.muted, "font-size": fs, "font-family": th.font }, svg, yFmt(Math.round(v * 100) / 100));
  }
  if (opt.ref !== undefined || hasBar) {
    const rv = opt.ref !== undefined ? opt.ref : 0;
    el("line", { x1: m.l, x2: m.l + iw, y1: Y(rv), y2: Y(rv), stroke: th.axis, "stroke-width": 1.4 }, svg);
  }
  // oś X
  let every = 1; while (band * every < fs * 3.4) every++;
  opt.x.forEach((yr, i) => {
    if ((n - 1 - i) % every) return;
    el("text", { x: X(i), y: m.t + ih + fs * 1.6, "text-anchor": "middle", fill: th.muted, "font-size": fs, "font-family": th.font }, svg, yr);
  });

  // pasmo między seriami
  if (opt.band) {
    const a = opt.series[opt.band.from].values, b = opt.series[opt.band.to].values;
    const pts = a.map((v, i) => `${X(i)},${Y(v)}`).concat(b.map((v, i) => `${X(i)},${Y(v)}`).reverse());
    el("polygon", { points: pts.join(" "), fill: opt.band.color }, svg);
  }

  // słupki
  const bars = opt.series.filter((s) => s.type === "bar");
  const bw = (band * 0.72) / Math.max(bars.length, 1);
  bars.forEach((s, k) => {
    s.values.forEach((v, i) => {
      const x = X(i) - (band * 0.72) / 2 + k * bw;
      const y0 = Y(0), y1 = Y(v);
      el("rect", { x: x + 1, y: Math.min(y0, y1), width: bw - 2, height: Math.max(Math.abs(y1 - y0), 1), rx: Math.min(3, bw / 4), fill: s.color, opacity: s.opacity || 1 }, svg);
    });
  });

  // linie
  opt.series.filter((s) => s.type !== "bar").forEach((s) => {
    const d = s.values.map((v, i) => `${i ? "L" : "M"}${X(i)},${Y(v)}`).join("");
    if (s.area) {
      const id = "ga" + _gid++;
      const lg = el("linearGradient", { id, x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
      el("stop", { offset: 0, "stop-color": s.color, "stop-opacity": s.area }, lg);
      el("stop", { offset: 1, "stop-color": s.color, "stop-opacity": 0 }, lg);
      el("path", { d: d + `L${X(n - 1)},${m.t + ih}L${X(0)},${m.t + ih}Z`, fill: `url(#${id})` }, svg);
    }
    const p = el("path", { d, fill: "none", stroke: s.color, "stroke-width": s.width || 3, "stroke-linejoin": "round", "stroke-linecap": "round" }, svg);
    if (s.dash) p.setAttribute("stroke-dasharray", s.dash);
    if (th.glow && !s.noGlow) p.setAttribute("filter", `url(#${glowId})`);
    if (s.dots) s.values.forEach((v, i) => el("circle", { cx: X(i), cy: Y(v), r: s.dots, fill: th.dotFill || s.color, stroke: s.color, "stroke-width": 2 }, svg));
    if (opt.endLabels && !s.noLabel) {
      const v = s.values[n - 1];
      el("circle", { cx: X(n - 1), cy: Y(v), r: 5, fill: s.color }, svg);
      el("text", { x: X(n - 1) + 10, y: Y(v) + fs * 0.35 + (s.labelDy || 0), fill: s.color, "font-size": fs, "font-weight": 700, "font-family": th.font }, svg, (s.labelFmt || yFmt)(v));
    }
  });
  _gid++;
}

// Rysuje cztery standardowe wykresy plakatu w elementach #w-wyn, #w-infl, #w-dyn, #w-ue.
function rysujWszystkie(th, kol, extra = {}) {
  const D = DANE;
  const wynRok = D.wyn.rok.filter((r) => r <= 2025);
  const k = wynRok.length;
  const tys = (v) => (v / 1000).toLocaleString("pl-PL", { maximumFractionDigits: 1 }) + " tys.";
  wykres(document.getElementById("w-wyn"), {
    theme: th, x: wynRok, endLabels: true, ml: 70,
    yFmt: (v) => fmtPL(v) + (extra.zl === false ? "" : " zł"),
    series: [
      { name: "Sektor przedsiębiorstw", values: D.wyn.przeds.slice(0, k), color: kol.a, width: 3.5, area: 0.28, labelDy: -8, labelFmt: tys },
      { name: "Gospodarka narodowa", values: D.wyn.gosp.slice(0, k), color: kol.b, width: 3, dash: "7 5", noLabel: true },
    ],
  });
  wykres(document.getElementById("w-infl"), {
    theme: th, x: D.mieszk.rok, endLabels: true, ref: 100,
    band: { from: 0, to: 1, color: kol.bandFill },
    series: [
      { name: "Cena nominalna", values: D.mieszk.pl_nom, color: kol.b, width: 3.5, labelFmt: fmt1 },
      { name: "Cena realna", values: D.mieszk.pl, color: kol.a, width: 3.5, labelFmt: fmt1 },
      { name: "Inflacja CPI", values: D.mieszk.cpi_skum, color: kol.c, width: 2.5, dash: "4 5", noLabel: true, noGlow: true },
    ],
  });
  wykres(document.getElementById("w-dyn"), {
    theme: th, x: D.dyn.rok, yFmt: (v) => fmtPL(v) + "%",
    series: [
      { name: "Polska", values: D.dyn.pl, color: kol.a, type: "bar" },
      { name: "UE-27", values: D.dyn.ue, color: kol.ue, type: "bar", opacity: 0.85 },
      { name: "Inflacja CPI", values: D.dyn.cpi, color: kol.c, width: 3, dots: 4 },
    ],
  });
  wykres(document.getElementById("w-ue"), {
    theme: th, x: D.mieszk.rok, endLabels: true, ref: 100,
    series: [
      { name: "Polska", values: D.mieszk.pl, color: kol.a, width: 3.5, area: 0.25, dots: 3.5, labelFmt: fmt1 },
      { name: "UE-27", values: D.mieszk.ue, color: kol.ue, width: 3.5, dots: 3.5, labelFmt: fmt1 },
    ],
  });
}

function start(th, kol, extra) {
  wstawTeksty();
  document.fonts.ready.then(() => rysujWszystkie(th, kol, extra));
}
