from flask import Flask, request, abort, jsonify
from services import dostepne_regiony, policz_wskazniki

app = Flask(__name__)

@app.get("/")
def index():
    return "Panel wskaźników"

@app.route("/kpi")
def kpi():
    sciezka = "dane/dane_zamowienia.csv"
    region = request.args.get("region")
    
    if region is not None:
        dozwolone_regiony = dostepne_regiony(sciezka)
        if region not in dozwolone_regiony:
            abort(404, description=f"Nieznany region: {region}")
            
    wskazniki = policz_wskazniki(sciezka, region=region)
    marza = wskazniki['marza']
    
    tytul = region if region else "Wszystkie regiony"
    return f"<h1>{tytul}</h1>\n<p>Marża: {marza:.2%}</p>"

@app.route("/api/kpi")
def api_kpi():
    sciezka = "dane/dane_zamowienia.csv"
    region = request.args.get("region")
    
    # To samo sprawdzenie regionu
    if region is not None:
        dozwolone_regiony = dostepne_regiony(sciezka)
        if region not in dozwolone_regiony:
            abort(404, description=f"Nieznany region: {region}")
            
    # Obliczenie wskaźników (ta sama funkcja)
    wskazniki = policz_wskazniki(sciezka, region=region)
    
    # Zwrócenie wyniku jako JSON
    return jsonify(wskazniki)

if __name__ == '__main__':
    app.run(debug=True)