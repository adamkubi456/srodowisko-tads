from datetime import date
from flask import Blueprint, request, abort, current_app, redirect, url_for, render_template, flash
from app.services import dostepne_regiony, policz_wskazniki, raporty_roku, zapisz_raport, zestawienie_regionow

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
    
    current_app.logger.info("Obliczono wskaźniki dla regionu %s", w["region"])
    
    return render_template(
        "panel.html",
        wskazniki=w, 
        zestawienie=zestawienie_regionow(sciezka),
        dzisiaj=date.today()
    )

@panel_bp.get("/regiony/<region:kod>")
def region(kod):
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    if kod not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {kod}")
    
    w = policz_wskazniki(sciezka, region=kod)
    
    return render_template(
        "panel.html",
        wskazniki=w, 
        zestawienie=zestawienie_regionow(sciezka),
        dzisiaj=date.today()
    )

ROK_DOMYSLNY = 2026

@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok):
    return render_template("report.html", rok=rok, zapisane=raporty_roku(rok))

@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
def nowy_raport():
    if request.method == "GET":
        return "Podaj rok i region, aby zapisać raport."
    
    rok = request.form.get("rok", type=int)
    region = request.form.get("region")
    
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    if rok is None or region not in dostepne_regiony(sciezka):
        abort(400, description="Niepoprawne dane formularza")
        
    if rok < 2020 or rok > 2030:
        abort(422, description="Rok poza zakresem 2020-2030")
        
    zapisz_raport(rok, region)
    flash(f"Raport za rok {rok} został zapisany", "sukces")
    return redirect(url_for("panel.raport", rok=rok), 303)

@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), 301)