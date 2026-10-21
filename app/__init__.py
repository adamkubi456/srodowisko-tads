import logging
from flask import Flask
from app.config import KONFIGURACJE

def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)
    
    # Wczytanie konfiguracji
    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])
    
    # Utrzymanie kolejności w JSON dla weryfikatora (z poprzedniego zadania)
    app.json.sort_keys = False
    
    # Ustawienie poziomu dziennika
    app.logger.setLevel(logging.INFO)
    
    # Importowanie blueprintów wewnątrz funkcji zapobiega tzw. importom cyklicznym
    from app.routes_panel import panel_bp
    from app.routes_api import api_bp
    
    # Rejestracja blueprintów
    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app