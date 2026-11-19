import os
from pathlib import Path

# Wyznaczenie ścieżki do głównego katalogu projektu (dwa poziomy wyżej niż config.py)
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'domyslny-klucz-zapasowy')
    SCIEZKA_DANYCH = BASE_DIR / "dane" / "dane_zamowienia.csv"
    DEBUG = False
    WTF_I18N_ENABLED = False
    MAX_CONTENT_LENGTH = 1024 * 1024

class RozwojowaConfig(Config):
    DEBUG = True

KONFIGURACJE = {
    "rozwojowa": RozwojowaConfig,
    "produkcyjna": Config
}