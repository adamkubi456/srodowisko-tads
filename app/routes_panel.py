from datetime import date
from werkzeug.utils import secure_filename
from flask import Blueprint, request, abort, current_app, redirect, url_for, render_template, flash
from app.forms import FiltrForm, RaportForm, ZbiorForm
from app.services import (
    dostepne_regiony,
    policz_wskazniki,
    raporty_roku,
    wykaz_raportow,
    zapisz_raport,
    zestawienie_regionow,
    wczytaj_zbior,
)
panel_bp = Blueprint('panel', __name__)

@panel_bp.route("/")
def index():
    return "Panel wskaźników"

@panel_bp.get("/kpi")
def kpi():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    formularz = FiltrForm(request.args)
    formularz.region.choices = [("", "wszystkie")] + [
        (r, r) for r in dostepne_regiony(sciezka)
    ]
    region = rok = None
    if formularz.validate():
        region = formularz.region.data or None
        rok = formularz.rok.data
    else:
        flash("Kryteria zawężenia zostały pominięte", "warning")

    w = policz_wskazniki(sciezka, region, rok)

    current_app.logger.info("Obliczono wskaźniki dla regionu %s", w["region"])

    return render_template(
        "panel.html",
        formularz=formularz,
        wskazniki=w,
        zestawienie=zestawienie_regionow(sciezka),
        dzisiaj=date.today(),
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
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    istniejace = {(r["rok"], r["region"]) for r in wykaz_raportow()}
    formularz = RaportForm(istniejace=istniejace)
    formularz.region.choices = [(r, r) for r in dostepne_regiony(sciezka)]

    if formularz.validate_on_submit():
        zapisz_raport(
            formularz.rok.data,
            formularz.region.data,
            formularz.uwagi.data or "",
        )
        flash(f"Raport za rok {formularz.rok.data} zapisany", "success")
        return redirect(url_for("panel.raport", rok=formularz.rok.data), 303)

    status = 422 if formularz.errors else 200
    return render_template("new_report.html", formularz=formularz), status

@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), 301)

@panel_bp.route("/wczytaj", methods=["GET", "POST"])
def wczytaj():
    formularz = ZbiorForm()
    if formularz.validate_on_submit():
        plik = formularz.plik.data
        nazwa = secure_filename(plik.filename)
        try:
            liczba = wczytaj_zbior(plik.stream)
        except ValueError as blad:
            formularz.plik.errors.append(f"Niepoprawna zawartość: {blad}")
        else:
            flash(f"Wczytano {liczba} zamówień z pliku {nazwa}", "success")
            return redirect(url_for("panel.wczytaj"), 303)

    status = 422 if formularz.errors else 200
    return render_template("upload.html", formularz=formularz), status