import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    return f"https://{host}{path}"










def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    is_https = url.startswith("https://")
    return is_https



def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    request = requests.get(url)
    print(f"URL: {url}")
    print(f"Status: {request.status_code}")
    print(f"Content-Type: {request.headers.get('Content-Type')}")




def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except:
        return {"status": None, "error": "site de neexistent sau nu răspunde"}




def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
def scan_sites():
    results = []

    for url in SITES:
        info = check_site(url)
        results.append({"url": url, **info})

    successful = [site for site in results if site.get("status") == 200]
    successful.sort(key=lambda item: item.get("length", 0), reverse=True)

    for site in successful:
        print(f"URL: {site['url']}")
        print(f"status: {site['status']}")
        print(f"content_type: {site['content_type']}")
        print(f"length: {site['length']}")
        print(f"server: {site['server']}")
        print()

    print(f"Rezumat: {len(successful)} site-uri au mers, {len(results) - len(successful)} au eșuat.")



def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        raspuns = requests.get(url, timeout=5)
    except Exception:
        return {"status": None, "error": "Eroare de conexiune sau timeout"}

    prezente = []
    lipsa = []

    for antet in SECURITY_HEADERS:
        if antet in raspuns.headers:
            prezente.append(antet)
        else:
            lipsa.append(antet)

    scor = len(prezente) * 25

    return {
        "present": prezente,
        "missing": lipsa,
        "score": scor
    }
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass
