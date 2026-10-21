import os
from pathlib import Path

# Wyznaczenie ścieżki do głównego katalogu projektu (dwa poziomy wyżej niż config.py)
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'domyslny-klucz-zapasowy')
    # Używamy ścieżki z Pathlib
    SCIEZKA_DANYCH = BASE_DIR / "dane" / "zamowienia.csv"
    DEBUG = False

class RozwojowaConfig(Config):
    DEBUG = True

KONFIGURACJE = {
    "rozwojowa": RozwojowaConfig,
    "produkcyjna": Config
}