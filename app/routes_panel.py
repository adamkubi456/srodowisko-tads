from flask import Blueprint, request, abort, current_app
from app.services import dostepne_regiony, policz_wskazniki

panel_bp = Blueprint('panel', __name__)

@panel_bp.route("/")
def index():
    return "Panel wskaźników"

@panel_bp.route("/kpi")
def kpi():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    region = request.args.get("region")
    
    if region is not None:
        dozwolone_regiony = dostepne_regiony(sciezka)
        if region not in dozwolone_regiony:
            abort(404, description=f"Nieznany region: {region}")
            
    w = policz_wskazniki(sciezka, region=region)
    
    # Punkt 6: Zapis do dziennika (loggera)
    current_app.logger.info("Obliczono wskaźniki dla regionu %s", w["region"])
    
    marza = w['marza']
    tytul = region if region else "Wszystkie regiony"
    return f"<h1>{tytul}</h1>\n<p>Marża: {marza:.2%}</p>"