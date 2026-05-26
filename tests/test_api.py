import pytest
import requests
from src.api.weather_client import WeatherClient, WeatherAPIError

@pytest.fixture
def weather_client():
    return WeatherClient("dummy_api_key")

def test_get_weather_success(mocker, weather_client):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Warsaw",
        "sys": {"country": "PL"},
        "main": {"temp": 15.5, "humidity": 60},
        "weather": [{"description": "clear sky", "icon": "01d"}],
        "wind": {"speed": 3.5}
    }
    mocker.patch("requests.get", return_value=mock_response)
    
    data = weather_client.get_weather("Warsaw")
    
    assert data.city == "Warsaw"
    assert data.country == "PL"
    assert data.temperature == 15.5
    assert data.description == "Clear sky"
    assert data.humidity == 60
    assert data.wind_speed == 3.5

def test_get_weather_invalid_key(mocker, weather_client):
    mock_response = mocker.Mock()
    mock_response.status_code = 401
    mocker.patch("requests.get", return_value=mock_response)
    
    with pytest.raises(WeatherAPIError, match="Błędny klucz API"):
        weather_client.get_weather("Warsaw")

def test_get_weather_city_not_found(mocker, weather_client):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)
    
    with pytest.raises(WeatherAPIError, match="Nie znaleziono miasta: NieznaneMiasto"):
        weather_client.get_weather("NieznaneMiasto")

def test_get_weather_timeout(mocker, weather_client):
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)
    
    with pytest.raises(WeatherAPIError, match="Przekroczono czas oczekiwania"):
        weather_client.get_weather("Warsaw")

def test_missing_api_key():
    client = WeatherClient(None)
    with pytest.raises(WeatherAPIError, match="Brak klucza API"):
        client.get_weather("Warsaw")
