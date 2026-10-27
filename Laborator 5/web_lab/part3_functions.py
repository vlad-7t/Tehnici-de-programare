

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time as t
import requests

def fetch(url, timeout=10):
    return requests.get(url, timeout=timeout)

def get_status(url: str) -> int:
    return requests.get(url, timeout=TIMEOUT).status_code

def get_title(html: str) -> str:
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()

def page_exists(url: str) -> bool:
    try:
        raspuns = requests.get(url, timeout=TIMEOUT)
        raspuns.raise_for_status()
        return True
    except requests.RequestException:
        return False

def check_paths(base: str, paths: list) -> dict:
    results = {}
    for c in paths:
        url_complet = base + c
        results[c] = get_status(url_complet)
        t.sleep(1)
    return results

def get_header(url: str, name: str, default: str = "lipsește") -> str:
    raspuns = requests.get(url, timeout=TIMEOUT)
    return raspuns.headers.get(name, default)

def security_headers(url):
    raspuns = requests.get(url, timeout=TIMEOUT)
    headers = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]
    rezultat = {}
    for nume in headers:
        rezultat[nume] = nume in raspuns.headers
    return rezultat

def score_headers(results):
    scor = 0
    for nume in results:
        if results[nume] == True:
            scor = scor + 1
    return f"{scor}/{len(results)}"

def fetch_robots(base):
    try:
        raspuns = requests.get(base + "/robots.txt", timeout=10)
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

def response_times(*urls):
    timp = {}
    for u in urls:
        respuns = requests.get(u, timeout=TIMEOUT)
        timp[u] = respuns.elapsed.total_seconds()
        t.sleep(1)
    return timp

def log(message, **details):
    elemente = [message]
    for cheie, valoare in details.items():
        elemente.append(f"{cheie}={valoare}")
    print(" | ".join(elemente))