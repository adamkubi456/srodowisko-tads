import csv

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

def policz_wskazniki(sciezka, region=None):
    zamowienia = wczytaj_zamowienia(sciezka)
    
    if region is not None:
        zamowienia = [z for z in zamowienia if z['region'] == region]
        
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

def zapisz_raport(rok, region):
    lista_RAPORTY.append({"rok": rok, "region": region})

def raporty_roku(rok):
    return [r for r in lista_RAPORTY if r["rok"] == rok]