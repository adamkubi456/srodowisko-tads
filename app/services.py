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


print(policz_wskazniki("dane/dane_zamowienia.csv", "PL"))
{'region': 'PL', 'liczba_zamowien': 3, 'przychod': 37900.0,
'koszt': 27900.0, 'marza': 0.2639}
print(dostepne_regiony("dane/dane_zamowienia.csv"))
['CZ', 'DE', 'PL']
