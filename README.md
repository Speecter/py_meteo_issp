# Meteo Dashboard 

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flet (Flutter)](https://img.shields.io/badge/Flet-02569B?style=for-the-badge&logo=flutter&logoColor=white)
![OpenWeatherMap API](https://img.shields.io/badge/OpenWeatherMap-E96E50?style=for-the-badge&logo=openweathermap&logoColor=white)
![Material Design 3](https://img.shields.io/badge/Material_3-EADDFF?style=for-the-badge&logo=materialdesign&logoColor=black)

Meteo Dashboard to nowoczesna aplikacja pogodowa na komputery osobiste, zbudowana w 100% w Pythonie z wykorzystaniem frameworka **Flet** (opartego na silniku Flutter). Jej design został zainspirowany interfejsem Microsoft Weather z Windows 11 oraz wytycznymi Google Material Design 3.

## Główne funkcjonalności

- **Prawdziwy Desktop Dashboard**: Stały panel boczny (Sidebar) oraz dynamiczny pulpit ze statystykami.
- **W pełni responsywna siatka (ResponsiveRow)**: Zmień rozmiar okna, a karty ułożą się w 1, 2 lub 4 kolumnach bez ucinania zawartości!
- **Silnik Material 3 (Tryby Jasny / Ciemny)**: Automatyczne zarządzanie "miękką" paletą kolorów (np. łagodne szarości i głębokie czernie), które nie męczą oczu. Ustawienia zapisywane są bezpośrednio w pamięci aplikacji (`client_storage`).
- **Interaktywny Tutorial (Wyspa)**: Pływająca w przestrzeni (na warstwie `Stack`) wyspa oprowadzająca nowych użytkowników po interfejsie.
- **Szybkość i stabilność**: Bezpośrednie i błyskawiczne ładownie ikon prosto z sieci z wykorzystaniem pamięci podręcznej frameworka Flet.

---

## Zrzuty ekranu

*(Podmień poniższe ścieżki na własne zrzuty zrobione podczas działania aplikacji na prezentację!)*

### Tryb Ciemny (AMOLED & Deep Blue-Grey)
> ![Tryb Ciemny](assets/screenshot_dark.png)

### Tryb Jasny (Soft Material 3)
> ![Tryb Jasny](assets/screenshot_light.png)

---

## Uruchomienie lokalne

1. Sklonuj repozytorium na swój dysk.
2. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```
3. Stwórz plik `.env` w głównym katalogu projektu i wklej swój klucz API z OpenWeatherMap:
```env
OPENWEATHERMAP_API_KEY=twoj_klucz_tutaj
```
4. Uruchom aplikację:
```bash
python src/main.py
```

##  Architektura i Technologie
- **[Flet](https://flet.dev/)**: Główny framework użyty do budowy UI. Konwertuje kod Pythona w locie na natywny interfejs we Flutterze (Dart).
- **Requests**: Do bezproblemowej i bezpiecznej komunikacji z serwerami pogodowymi.
- **Python-Dotenv**: Do zarządzania zmiennymi środowiskowymi i bezpieczeństwem kluczy API.
- Wzorzec projektowy w pełni oddzielający logikę zapytania o dane (`WeatherClient`) od warstwy wyświetlającej (`app.py`).
