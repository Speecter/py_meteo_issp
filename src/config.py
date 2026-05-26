import os
import sys
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env (jeśli istnieje)
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

def get_api_key():
    """
    Pobiera klucz API. Jeśli go nie ma, zwraca None, co zostanie obsłużone w UI lub Kliencie.
    """
    key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not key or key == "twoj_klucz_api_tutaj":
        return None
    return key
