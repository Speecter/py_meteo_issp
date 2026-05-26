import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Dodajemy src do ścieżki, żeby działały importy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import get_api_key
from src.api.weather_client import WeatherClient, WeatherAPIError

# Próbujemy zaimportować sv_ttk dla nowoczesnego wyglądu
try:
    import sv_ttk
    HAS_SV_TTK = True
except ImportError:
    HAS_SV_TTK = False

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Meteo App - Pogoda na Świecie")
        self.geometry("450x600")
        self.minsize(400, 500)
        
        # Nowoczesny wygląd z sv_ttk
        if HAS_SV_TTK:
            sv_ttk.set_theme("dark")
            
        self.api_key = get_api_key()
        self.client = WeatherClient(self.api_key) if self.api_key else None
        
        self._build_ui()
        
    def _build_ui(self):
        # Główny kontener
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sekcja wyszukiwania
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.search_var, 
            font=("Segoe UI", 12)
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.fetch_weather())
        
        search_btn = ttk.Button(search_frame, text="Szukaj", command=self.fetch_weather)
        search_btn.pack(side=tk.RIGHT)
        
        # Ostrzeżenie o braku klucza
        if not self.api_key:
            warning_lbl = ttk.Label(
                main_frame, 
                text="Brak klucza API w pliku .env!\nUzupełnij go, by pobierać dane.", 
                foreground="red",
                justify=tk.CENTER
            )
            warning_lbl.pack(pady=10)
            search_btn.config(state="disabled")
            self.search_entry.config(state="disabled")
        
        # Sekcja wyników
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.city_lbl = ttk.Label(self.result_frame, text="", font=("Segoe UI", 24, "bold"))
        self.city_lbl.pack(pady=(10, 5))
        
        self.temp_lbl = ttk.Label(self.result_frame, text="", font=("Segoe UI", 48, "bold"))
        self.temp_lbl.pack(pady=5)
        
        self.desc_lbl = ttk.Label(self.result_frame, text="", font=("Segoe UI", 16))
        self.desc_lbl.pack(pady=5)
        
        # Szczegóły (wiatr, wilgotność)
        self.details_frame = ttk.Frame(self.result_frame)
        self.details_frame.pack(fill=tk.X, pady=20)
        
        self.humidity_lbl = ttk.Label(self.details_frame, text="", font=("Segoe UI", 12))
        self.humidity_lbl.pack(side=tk.LEFT, expand=True)
        
        self.wind_lbl = ttk.Label(self.details_frame, text="", font=("Segoe UI", 12))
        self.wind_lbl.pack(side=tk.RIGHT, expand=True)
        
    def fetch_weather(self):
        city = self.search_var.get().strip()
        if not city:
            return
            
        if not self.client:
            messagebox.showerror("Błąd konfiguracji", "Brak klucza API.")
            return
            
        try:
            # Wstawienie stanu ładowania
            self.city_lbl.config(text="Szukam...")
            self.temp_lbl.config(text="")
            self.desc_lbl.config(text="")
            self.humidity_lbl.config(text="")
            self.wind_lbl.config(text="")
            self.update()
            
            data = self.client.get_weather(city)
            
            # Aktualizacja UI
            self.city_lbl.config(text=f"{data.city}, {data.country}")
            self.temp_lbl.config(text=f"{int(data.temperature)}°C")
            self.desc_lbl.config(text=data.description)
            self.humidity_lbl.config(text=f"Wilgotność: {data.humidity}%")
            self.wind_lbl.config(text=f"Wiatr: {data.wind_speed} m/s")
            
        except WeatherAPIError as e:
            self.city_lbl.config(text="Błąd")
            messagebox.showerror("Błąd pobierania danych", str(e))
        except Exception as e:
            self.city_lbl.config(text="Błąd")
            messagebox.showerror("Nieoczekiwany Błąd", f"Wystąpił problem:\n{str(e)}")

def main():
    app = WeatherApp()
    app.mainloop()

if __name__ == "__main__":
    main()
