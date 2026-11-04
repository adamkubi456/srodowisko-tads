from flask import request, jsonify, render_template
from werkzeug.exceptions import HTTPException

def zarejestruj_obsluge_bledow(app):
    @app.errorhandler(HTTPException)
    def obsluga(blad):
        # Błędy z prefiksem /api formatujemy jako JSON
        if request.path.startswith("/api"):
            return jsonify(blad=blad.description, kod=blad.code), blad.code
            
        # Pozostałe błędy formatujemy jako HTML z użyciem szablonu
        return render_template("errors/error.html", kod=blad.code, opis=blad.description), blad.code