import os
import pytest
from src.config import get_api_key

def test_get_api_key_valid(monkeypatch):
    monkeypatch.setenv("OPENWEATHERMAP_API_KEY", "real_key")
    assert get_api_key() == "real_key"

def test_get_api_key_missing(monkeypatch):
    monkeypatch.delenv("OPENWEATHERMAP_API_KEY", raising=False)
    assert get_api_key() is None

def test_get_api_key_default(monkeypatch):
    monkeypatch.setenv("OPENWEATHERMAP_API_KEY", "twoj_klucz_api_tutaj")
    assert get_api_key() is None
