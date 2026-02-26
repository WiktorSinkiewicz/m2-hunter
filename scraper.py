import requests
from bs4 import BeautifulSoup
import time
import random
import re

def clean_string_to_int(raw_text: str) -> int | None:
    if not raw_text:
        return None
    
    clean_digits = re.sub(r'\D', '', str(raw_text))
    
    if not clean_digits:
        return None
        
    return int(clean_digits)

def clean_area_to_float(raw_text: str) -> float | None:
    if not raw_text:
        return None
    
    text_with_dot = raw_text.replace(',', '.')
    match = re.search(r'\d+(\.\d+)?', text_with_dot)
    
    if match:
        return float(match.group())
        
    return None

def pobierz_ogloszenia(url):
    naglowki = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }

    print(f"Łączenie ze stroną: {url} ...")
    
    opoznienie = random.uniform(1.5, 3.5)
    print(f"Czekam {opoznienie:.2f} sekundy, aby ominąć systemy anty-botowe...")
    time.sleep(opoznienie)


    odpowiedz = requests.get(url, headers=naglowki)

    if odpowiedz.status_code != 200:
        print(f"Błąd - Serwer zwrócił kod: {odpowiedz.status_code}")
        return

    zupa = BeautifulSoup(odpowiedz.text, 'html.parser')

    karty_ogloszen = zupa.find_all('div', {'data-cy': 'l-card'})
    
    print(f"Znaleziono {len(karty_ogloszen)} potencjalnych ogłoszeń na stronie.\n")

    for karta in karty_ogloszen:
        tytul_element = karta.find('h4')
        tytul = tytul_element.text.strip() if tytul_element else "Brak tytułu"

        cena_element = karta.find('p', {'data-testid': 'ad-price'})
        cena_tekst = cena_element.text if cena_element else ""
        cena = clean_string_to_int(cena_tekst)

        span_metraz = karta.find('span', {'data-nx-name': 'P5'})
        metraz_tekst = span_metraz.text.strip() if span_metraz else ""
        metraz = clean_area_to_float(metraz_tekst)

        print(f"Tytuł: {tytul}")
        print(f"Cena: {cena} zł")
        print(f"Metraż: {metraz} m^2")
        print("-" * 40)

if __name__ == "__main__":
    adres_docelowy = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/poznan/"
    pobierz_ogloszenia(adres_docelowy)