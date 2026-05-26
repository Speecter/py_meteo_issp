import requests
from dataclasses import dataclass
from typing import Optional

@dataclass
class WeatherData:
    city: str
    country: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    icon: str

class WeatherAPIError(Exception):
    pass

class WeatherClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
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
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            
            if response.status_code == 401:
                raise WeatherAPIError("Błędny klucz API.")
            elif response.status_code == 404:
                raise WeatherAPIError(f"Nie znaleziono miasta: {city_name}.")
            
            response.raise_for_status()
            data = response.json()
            
            return WeatherData(
                city=data["name"],
                country=data["sys"]["country"],
                temperature=data["main"]["temp"],
                description=data["weather"][0]["description"].capitalize(),
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                icon=data["weather"][0]["icon"]
            )
            
        except requests.exceptions.Timeout:
            raise WeatherAPIError("Przekroczono czas oczekiwania na odpowiedź serwera (Timeout).")
        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("Błąd połączenia. Sprawdź dostęp do Internetu.")
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Wystąpił błąd podczas pobierania danych: {str(e)}")
