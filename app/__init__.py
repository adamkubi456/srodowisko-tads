import logging
from flask import Flask, g, request
from app.config import KONFIGURACJE
from app.converters import RegionConverter
import time
from app.errors import zarejestruj_obsluge_bledow

def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)

    zarejestruj_obsluge_bledow(app)
    
    # Wczytanie konfiguracji
    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])

    app.url_map.converters["region"] = RegionConverter

    # Utrzymanie kolejności w JSON dla weryfikatora (z poprzedniego zadania)
    app.json.sort_keys = False

    @app.before_request
    def start_timer():
        g.start = time.perf_counter()

    @app.after_request
    def dodaj_czas(response):
        if hasattr(g, 'start'):
            czas_ms = (time.perf_counter() - g.start) * 1000
            response.headers["X-Czas-Ms"] = f"{czas_ms:.2f}"
        return response
    
    # Ustawienie poziomu dziennika
    app.logger.setLevel(logging.INFO)
    
    # Importowanie blueprintów wewnątrz funkcji zapobiega tzw. importom cyklicznym
    from app.routes_panel import panel_bp
    from app.routes_api import api_bp
    
    # Rejestracja blueprintów
    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(api_bp, url_prefix="/api/v2", name="api_v2")
    return app