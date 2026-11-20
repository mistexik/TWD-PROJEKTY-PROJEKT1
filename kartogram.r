library(sf)
library(ggplot2)
library(dplyr)
library(scales)

# 1. Wczytanie danych
df <- read.csv("Kopia Kopia ceny_mieszkan_polska_2026.csv", 
               check.names = FALSE, 
               fileEncoding = "UTF-8")

# 2. Mapowanie miast na województwa
mapa_miast <- c(
  "Warszawa" = "mazowieckie", "Radom" = "mazowieckie",
  "Kraków" = "małopolskie",
  "Gdańsk" = "pomorskie", "Gdynia" = "pomorskie",
  "Wrocław" = "dolnośląskie",
  "Poznań" = "wielkopolskie",
  "Szczecin" = "zachodniopomorskie",
  "Katowice" = "śląskie", "Częstochowa" = "śląskie", "Sosnowiec" = "śląskie",
  "Gliwice" = "śląskie", "Zabrze" = "śląskie",
  "Rzeszów" = "podkarpackie",
  "Lublin" = "lubelskie",
  "Łódź" = "łódzkie",
  "Opole" = "opolskie",
  "Białystok" = "podlaskie",
  "Bydgoszcz" = "kujawsko-pomorskie", "Toruń" = "kujawsko-pomorskie",
  "Olsztyn" = "warmińsko-mazurskie",
  "Kielce" = "świętokrzyskie",
  "Gorzów Wielkopolski" = "lubuskie"
)

# 3. Agregacja średniej ceny
woj_ceny <- df %>%
  mutate(wojewodztwo = mapa_miast[Miasto]) %>%
  group_by(wojewodztwo) %>%
  summarise(srednia_cena = mean(`Średnia cena za m² (PLN)`, na.rm = TRUE))

# 4. Pobranie granic województw
url_geojson <- "https://raw.githubusercontent.com/ppatrzyk/polska-geojson/master/wojewodztwa/wojewodztwa-min.geojson"
mapa <- st_read(url_geojson, quiet = TRUE)

mapa_dane <- mapa %>%
  left_join(woj_ceny, by = c("nazwa" = "wojewodztwo"))

etykiety <- st_point_on_surface(mapa_dane)

# 5. Rysowanie kartogramu w stylu plakatu (Złoto + Biel + Przezroczyste tło)
wykres <- ggplot(mapa_dane) +
  geom_sf(aes(fill = srednia_cena), color = "#0E1624", linewidth = 0.7) +
  # Czyste białe liczby z lekkim ciemnym cieniem/obrysem dla czytelności (bez białych ramek)
  geom_sf_text(
    data = etykiety,
    aes(label = number(srednia_cena, accuracy = 1, big.mark = " ")),
    size = 5.2,
    fontface = "bold",
    color = "#FFFFFF"
  ) +
  # Skala od przygaszonego ciemnego złota/brązu po jasne, nasycone złoto
  scale_fill_gradient(
    low = "#78622E",    # Jaśniejszy ciepły odcień dla najniższych cen (było #4A3B22)
    high = "#FFE066",   # Jasny, żywy złoto-żółty dla najwyższych cen (było #E6B84C)
    name = "Cena za m² (PLN)",
    labels = label_number(big.mark = " ")
  ) + +
  labs(
    title = "ŚREDNIE CENY MIESZKAŃ (X 2026)",
    subtitle = "Średnia z badanych miast w województwie (PLN/m²)"
  ) +
  theme_void() +
  theme(
    # Całkowicie przezroczyste tło
    plot.background = element_rect(fill = "transparent", color = NA),
    panel.background = element_rect(fill = "transparent", color = NA),
    legend.background = element_rect(fill = "transparent", color = NA),
    # Złoty tytuł dopasowany do nagłówków na plakacie
    plot.title = element_text(size = 19, face = "bold", color = "#E6B84C", hjust = 0.5, margin = margin(t = 10, b = 4)),
    plot.subtitle = element_text(size = 12, color = "#D0D7E5", hjust = 0.5, margin = margin(b = 10)),
    # Legenda w bieli i złocie
    legend.position = "right",
    legend.title = element_text(size = 12, face = "bold", color = "#E6B84C"),
    legend.text = element_text(size = 11, color = "#FFFFFF", face = "bold"),
    legend.key.height = unit(1.1, "cm")
  )

print(wykres)

# Zapis PNG z przezroczystym tłem (bg = "transparent")
ggsave("kartogram_plakat_R.png", plot = wykres, width = 10, height = 9, dpi = 300, bg = "transparent")