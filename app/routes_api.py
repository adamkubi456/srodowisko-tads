from flask import Blueprint, request, abort, jsonify, current_app
from app.services import dostepne_regiony, policz_wskazniki
from app.validators import parametr_int
from app.services import raporty_roku
from app.decorators import wymagany_parametr

api_bp = Blueprint('api', __name__)

@api_bp.route("/kpi")
def kpi():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    region = request.args.get("region")
    
    if region is not None:
        dozwolone_regiony = dostepne_regiony(sciezka)
        if region not in dozwolone_regiony:
            abort(404, description=f"Nieznany region: {region}")
            
    w = policz_wskazniki(sciezka, region=region)
    return jsonify(w)

@api_bp.get("/raporty")
@wymagany_parametr("rok")

def raporty():
    rok = parametr_int("rok", 2020, 2030)
    return jsonify(rok=rok, raporty=raporty_roku(rok))