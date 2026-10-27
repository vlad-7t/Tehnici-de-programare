

BASE_URL = "https://cybercor.org"
TIMEOUT = 10  # secunde

import time as t
import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
import requests
from datetime import datetime

# ==========================================
# Exercitiul 35, 36, 37, 38
# ==========================================
desc = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
t.sleep(1)

lista_url=["/about", "contact.html", "../index.html"]
for url in lista_url:
    print(f"URL complet pentru {url}: {urllib.parse.urljoin(BASE_URL, url)}")

def extract_links(html):
    toate_legaturile = re.findall(r'href="([^"]+)"', html)
    legaturi_unice = []
    for link in toate_legaturile:
        if link not in legaturi_unice:
            legaturi_unice.append(link)
    return legaturi_unice

def split_links(links, domain):
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

# ==========================================
# Exercitiul 39
# ==========================================
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            sursa = dict(attrs).get("src")
            if sursa is not None:
                self.images.append(sursa)

# ==========================================
# Exercitiul 40
# ==========================================
def page_fingerprint(url):
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()

amprenta1 = page_fingerprint(BASE_URL)
t.sleep(1)  
amprenta2 = page_fingerprint(BASE_URL)

# ==========================================
# Exercitiul 41, 42, 43
# ==========================================
def ex41_salvare_json():
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    antete = dict(response.headers)
    with open("headers.json", "w") as file:
        json.dump(antete, file, indent=2)
    with open("headers.json", "r") as file:
        antete_incarcate = json.load(file)
    print("Content-Type încărcat din JSON:", antete_incarcate.get("Content-Type"))

ex41_salvare_json()

def resolve(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

print("IP cybercor.org:", resolve("cybercor.org"))

def cert_days_left(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
            cert = ssl_sock.getpeercert()
            
    expirare_secunde = ssl.cert_time_to_seconds(cert["notAfter"])
    timp_curent = datetime.now().timestamp()
    secunde_ramase = expirare_secunde - timp_curent
    
    return int(secunde_ramase / (24 * 3600))