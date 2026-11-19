import csv
import io

def wczytaj_zamowienia(sciezka):
    zamowienia = []
    with open(sciezka, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            zamowienia.append({
                'data': row['data'],
                'region': row['region'],
                'przychod': float(row['przychod']),
                'koszt': float(row['koszt'])
            })
    return zamowienia

def dostepne_regiony(sciezka):
    zamowienia = wczytaj_zamowienia(sciezka)
    regiony = {row['region'] for row in zamowienia}
    return sorted(list(regiony))

def policz_wskazniki(sciezka, region=None, rok=None):
    zamowienia = wczytaj_zamowienia(sciezka)
    
    if region is not None:
        zamowienia = [z for z in zamowienia if z['region'] == region]
    if rok is not None:
        zamowienia = [z for z in zamowienia if z['data'].startswith(str(rok))]
        
    liczba_zamowien = len(zamowienia)
    przychod = sum(z['przychod'] for z in zamowienia)
    koszt = sum(z['koszt'] for z in zamowienia)
    
    if przychod == 0:
        marza = 0.0
    else:
        marza = (przychod - koszt) / przychod
        
    # Zwracamy słownik z zaokrąglonymi wartościami
    return {
        'region': region,
        'liczba_zamowien': liczba_zamowien,
        'przychod': round(przychod, 2),
        'koszt': round(koszt, 2),
        'marza': round(marza, 4)
    }

lista_RAPORTY = []

def zapisz_raport(rok, region, uwagi=""):
    lista_RAPORTY.append({"rok": rok, "region": region, "uwagi": uwagi})

def wykaz_raportow():
    return list(lista_RAPORTY)

def raporty_roku(rok):
    return [r for r in lista_RAPORTY if r["rok"] == rok]

def zestawienie_regionow(sciezka):
    regiony = dostepne_regiony(sciezka)
    return [policz_wskazniki(sciezka, kod) for kod in sorted(regiony)]

def wczytaj_zbior(strumien):
    tresc = strumien.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(tresc))
    wymagane = {"data", "region", "przychod", "koszt"}
    kolumny = set(reader.fieldnames or ())
    brakujace = wymagane - kolumny
    if brakujace:
        raise ValueError(f"brak kolumn: {', '.join(sorted(brakujace))}")
    return sum(1 for _ in reader)