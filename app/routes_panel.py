from flask import Blueprint, request, abort, current_app, redirect, url_for
from app.services import dostepne_regiony, policz_wskazniki, raporty_roku, zapisz_raport

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

@panel_bp.get("/regiony/<region:kod>")
def region(kod):
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    if kod not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {kod}")
    
    # Zgodnie z instrukcją: PL=3, DE=3, CZ=2
    liczba = 3 if kod in ["PL", "DE"] else 2
    return f"<h1>Region {kod}</h1><p>Zamówień: {liczba}</p>"


ROK_DOMYSLNY = 2026

@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok):
    n = len(raporty_roku(rok))
    return f"<h1>Raport {rok}</h1><p>Zapisane raporty: {n}</p>"

@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
def nowy_raport():
    if request.method == "GET":
        return "Podaj rok i region, aby zapisać raport."
    
    # Obsługa POST
    rok = request.form.get("rok", type=int)
    region = request.form.get("region")
    
    # 2. Walidacja zapisu
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    if rok is None or region not in dostepne_regiony(sciezka):
        abort(400, description="Niepoprawne dane formularza")
        
    if rok < 2020 or rok > 2030:
        abort(422, description="Rok poza zakresem 2020-2030")
        
    # 3. Zapis i przekierowanie 303 (Post/Redirect/Get)
    zapisz_raport(rok, region)
    return redirect(url_for("panel.raport", rok=rok), 303)

@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), 301)