import requests
import json
import urllib.parse
import socket
import ssl
import re
from datetime import datetime
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {"User-Agent": "WebLab-Vladislav"}
TIMEOUT = 10

def fetch(url, timeout=10):
    """Returnează obiectul răspuns complet pentru adresa url."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    raspuns = requests.get(url, timeout=TIMEOUT)
    return raspuns.status_code

def get_title(html: str) -> str:
    """Returnează titlul paginii extras dintr-un șir HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return None

def get_title_bs4(html):
    """Extrage titlul paginii folosind BeautifulSoup."""
    soup = BeautifulSoup(html, 'html.parser')
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return None

def extract_links(html):
    """Extrage legăturile unice din etichetele <a> folosind BeautifulSoup."""
    soup = BeautifulSoup(html, 'html.parser')
    toate_legaturile = [tag['href'] for tag in soup.find_all('a', href=True)]
    return list(set(toate_legaturile))

def split_links(links, domain):
    """Împarte o listă de legături în interne și externe."""
    internal_links = []
    external_links = []
    domeniu_principal = urllib.parse.urlparse(domain).netloc
    for link in links:
       url_absolut = urllib.parse.urljoin(domain, link)
       domeniu_curent = urllib.parse.urlparse(url_absolut).netloc
       if domeniu_curent == domeniu_principal:
           internal_links.append(url_absolut)
       else:
           external_links.append(url_absolut)
    return internal_links, external_links

def resolve(hostname):
    """Rezolvă un nume de domeniu în adresa IP corespunzătoare."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def cert_days_left(hostname):
    """Returnează numărul de zile rămase până la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                cert = ssl_sock.getpeercert()
        expirare_secunde = ssl.cert_time_to_seconds(cert["notAfter"])
        timp_curent = datetime.now().timestamp()
        return int((expirare_secunde - timp_curent) / (24 * 3600))
    except Exception:
        return 0

def security_headers(url):
    """Verifică prezența a cinci antete de securitate pentru adresa url."""
    raspuns = requests.get(url, timeout=TIMEOUT)
    headers = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]
    rezultat = {}
    for nume in headers:
        rezultat[nume] = nume in raspuns.headers
    return rezultat

def score_headers(results):
    """Calculează scorul antetelor de securitate."""
    scor = sum(1 for v in results.values() if v)
    return f"{scor}/{len(results)}"

def fetch_robots(base):
    try:
        raspuns = requests.get(base + "/robots.txt", timeout=TIMEOUT)
        if raspuns.status_code == 200:
            return raspuns.text
        return None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text):
    if not robots_text:
        return []
    cai = []
    for linie in robots_text.splitlines():
        if linie.lower().startswith("disallow:"):
            cale = linie.split(":", 1)[1].strip()
            if cale:
                cai.append(cale)
    return cai

def check_paths(base: str, paths: list) -> dict:
    """Primește o listă de căi și returnează un dicționar {path: status_code}."""
    results = {}
    for c in paths:
        results[c] = get_status(base + c)
    return results

def site_report(url):
    """
    Colectează informațiile site-ului folosind funcțiile din modul, 
    afișează raportul în consolă și salvează datele în report.json.
    """
    domeniu = urllib.parse.urlparse(url).netloc
    
    raspuns = fetch(url)
    html = raspuns.text
    
    status = raspuns.status_code
    titlu = get_title_bs4(html) or get_title(html)
    ip = resolve(domeniu)
    
    url_http = "http://" + domeniu
    raspuns_http = fetch(url_http)
    if raspuns_http.history:
        istoric_url = [r.url for r in raspuns_http.history]
        istoric_url.append(raspuns_http.url)
        redirectionari = " -> ".join(istoric_url)
    else:
        redirectionari = raspuns_http.url

    scor_securitate = score_headers(security_headers(url))
    zile_certificat = cert_days_left(domeniu)
    
    toate_legaturile = extract_links(html)
    interne, externe = split_links(toate_legaturile, url)
    
    text_robots = fetch_robots(url)
    cai_interzise = disallowed_paths(text_robots)
    
    date_json = {
        "url": url,
        "status": status,
        "titlu": titlu,
        "ip": ip,
        "redirectionari": redirectionari,
        "scor_securitate": scor_securitate,
        "certificat_zile": zile_certificat,
        "legaturi_interne": len(interne),
        "legaturi_externe": len(externe),
        "cai_interzise": cai_interzise
    }
    
    with open("report.json", "w") as fisier_json:
        json.dump(date_json, fisier_json, indent=2)
        
    cai_afisare = ", ".join(cai_interzise) if cai_interzise else "Niciuna"
    
    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {status}")
    print(f"Titlu:             {titlu}")
    print(f"Adresă IP:         {ip}")
    print(f"Redirecționări:    {redirectionari}")
    print(f"Scor securitate:   {scor_securitate}")
    print(f"Certificat:        {zile_certificat} de zile rămase")
    print(f"Legături:          {len(interne)} interne, {len(externe)} externe")
    print(f"Căi interzise:     {cai_afisare}")
    print("Salvat în report.json")

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))