import requests
from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import datetime

@dataclass
class WeatherData:
    city: str
    country: str
    temperature: float
    temperature_min: float
    temperature_max: float
    description: str
    humidity: int
    wind_speed: float
    wind_deg: int
    icon: str
    sunrise_str: str
    sunset_str: str
    precipitation_sum: float
    uv_index: float
    hourly_forecast: List[Dict]
    daily_forecast: List[Dict]

class WeatherAPIError(Exception):
    pass

class WeatherClient:
    BASE_URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
    BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def get_weather(self, city_name: str) -> WeatherData:
        if not self.api_key:
            raise WeatherAPIError("Brak klucza API. Uzupełnij plik .env.")
            
        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric",
            "lang": "pl"
        }
        
        try:
            # 1. Pobieranie danych bieżących
            resp_weather = requests.get(self.BASE_URL_WEATHER, params=params, timeout=10)
            if resp_weather.status_code == 401:
                raise WeatherAPIError("Błędny klucz API.")
            elif resp_weather.status_code == 404:
                raise WeatherAPIError(f"Nie znaleziono miasta: {city_name}.")
            resp_weather.raise_for_status()
            data_weather = resp_weather.json()
            
            # 2. Pobieranie prognozy (5 dni / 3 godziny)
            resp_forecast = requests.get(self.BASE_URL_FORECAST, params=params, timeout=10)
            resp_forecast.raise_for_status()
            data_forecast = resp_forecast.json()
            
            # Przetwarzanie wschodu i zachodu
            sunrise_dt = datetime.fromtimestamp(data_weather["sys"]["sunrise"])
            sunset_dt = datetime.fromtimestamp(data_weather["sys"]["sunset"])
            
            # Przetwarzanie opadów (ostatnie 1h jeśli dostępne, w przeciwnym razie mock)
            rain_1h = data_weather.get("rain", {}).get("1h", 0.0)
            
            # Prognoza godzinowa (najbliższe 8 elementów = 24h)
            hourly = []
            for item in data_forecast["list"][:8]:
                dt = datetime.fromtimestamp(item["dt"])
                hourly.append({
                    "time": dt.strftime("%H:00"),
                    "temp": item["main"]["temp"],
                    "icon": item["weather"][0]["icon"]
                })
                
            # Prognoza dzienna (agregacja po dniach)
            daily_dict = {}
            for item in data_forecast["list"]:
                dt = datetime.fromtimestamp(item["dt"])
                date_str = dt.strftime("%d.%m")
                
                if date_str not in daily_dict:
                    daily_dict[date_str] = {
                        "date": date_str,
                        "day_name": dt.strftime("%A")[:2].capitalize(), # Mock Dni
                        "temp_min": item["main"]["temp_min"],
                        "temp_max": item["main"]["temp_max"],
                        "icon": item["weather"][0]["icon"],
                        "pop": int(item.get("pop", 0) * 100) # probability of precipitation
                    }
                else:
                    daily_dict[date_str]["temp_min"] = min(daily_dict[date_str]["temp_min"], item["main"]["temp_min"])
                    daily_dict[date_str]["temp_max"] = max(daily_dict[date_str]["temp_max"], item["main"]["temp_max"])
            
            daily = list(daily_dict.values())
            
            # Mockowanie UV
            uv_mock = 4.0 # Umiarkowany
            
            return WeatherData(
                city=data_weather["name"],
                country=data_weather["sys"]["country"],
                temperature=data_weather["main"]["temp"],
                temperature_min=data_weather["main"]["temp_min"],
                temperature_max=data_weather["main"]["temp_max"],
                description=data_weather["weather"][0]["description"].capitalize(),
                humidity=data_weather["main"]["humidity"],
                wind_speed=data_weather["wind"]["speed"],
                wind_deg=data_weather["wind"].get("deg", 0),
                icon=data_weather["weather"][0]["icon"],
                sunrise_str=sunrise_dt.strftime("%H:%M"),
                sunset_str=sunset_dt.strftime("%H:%M"),
                precipitation_sum=rain_1h, # Uproszczenie dla darmowego API
                uv_index=uv_mock,
                hourly_forecast=hourly,
                daily_forecast=daily
            )
            
        except requests.exceptions.Timeout:
            raise WeatherAPIError("Przekroczono czas oczekiwania na odpowiedź serwera (Timeout).")
        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("Błąd połączenia. Sprawdź dostęp do Internetu.")
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Wystąpił błąd podczas pobierania danych: {str(e)}")
