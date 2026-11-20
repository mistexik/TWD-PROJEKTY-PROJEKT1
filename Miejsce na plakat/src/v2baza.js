// Wspólny skrypt wersji „wariant 2 + zdjęcie miasta”: zdjęcie w nagłówku, ikony, wykresy.
(function () {
  const q = new URLSearchParams(location.search);
  const foto = document.getElementById("foto");
  foto.style.backgroundImage = `url("../zdjecia/${q.get("foto") || "Obraz1.jpg"}")`;
  foto.style.backgroundPosition = q.get("pos") || "50% 45%";
  document.getElementById("ikona").innerHTML = ikonaPortfela({ gold: "#ecca7c", goldDark: "#8f6a26", bg: "#0f1a3d" });
  const ik2 = document.getElementById("ik2");
  if (ik2) ik2.innerHTML = ikonaSlupkow("#d9b25f");
  start({ text: "#e9e7f0", muted: "#8f98b8", grid: "rgba(154,162,192,.16)", axis: "rgba(217,178,95,.6)", font: "Raleway", fs: 14 },
        { a: "#e5bd62", b: "#7fb2ff", c: "#ff7a8a", ue: "#7fb2ff", bandFill: "rgba(127,178,255,.13)" });
})();
