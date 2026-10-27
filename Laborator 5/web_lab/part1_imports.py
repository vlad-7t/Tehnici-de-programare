

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time
import requests
import urllib.request

# ==========================================
# Exercitiul 1
# ==========================================
print(requests.__version__)
time.sleep(1)
# Explicatie:
# 'requests' este o biblioteca externa si nu face parte din pachetul de baza,
# deci trebuie instalata manual folosind pip.
# 'urllib' (inclusiv 'urllib.request') face parte din Python Standard Library
# si vine preinstalata implicit odata cu Python.

# ==========================================
# Exercitiul 2
# ==========================================
# 1. import normal
raspuns1 = requests.get(BASE_URL, timeout=TIMEOUT)
print(raspuns1.status_code)
time.sleep(1)

# 2. import specific
from requests import get
raspuns2 = get(BASE_URL, timeout=TIMEOUT)
print(raspuns2.status_code)
time.sleep(1)
# Avantaj 'import requests': stii clar de unde vine functia (evita conflictele de nume).
# Avantaj 'from requests import get': scrii mai putin cod cand o apelezi des.

# ==========================================
# Exercitiul 3
# ==========================================
import requests as rq
raspuns3 = rq.get(BASE_URL, timeout=TIMEOUT)
print(raspuns3.status_code)
# Explicatie alias: ajuta cand numele bibliotecii este prea lung, dar incurca daca
# folosesti un alias neclar pe care nu il mai intelegi peste o luna.
time.sleep(1)

# ==========================================
# Exercitiul 4
# ==========================================
cerere = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
raspuns4 = urllib.request.urlopen(cerere, timeout=TIMEOUT)
print(raspuns4.status)
corp = raspuns4.read().decode("utf-8")
print(corp[:200])
time.sleep(1)

# ==========================================
# Exercitiul 5
# ==========================================
print("EXERCITIUL 5")
print(dir(requests))
# 1. 'get' - este o functie (descarca date).
# 2. 'Session' - este o clasa (mentine o sesiune HTTP).
# 3. 'exceptions' - este un modul (contine erorile).
time.sleep(1)

# ==========================================
# Exercitiul 6
# ==========================================
# Poti rula help(requests.request) in consola interactiva.
# Parametrul gasit in documentatie este "timeout".

# ==========================================
# Exercitiul 7
# ==========================================
start = time.perf_counter()
raspuns7 = requests.get(BASE_URL, timeout=TIMEOUT)
stop = time.perf_counter()

durata_masurata = stop - start
durata_requests = raspuns7.elapsed.total_seconds()

print("Timp masurat de time.perf_counter:", durata_masurata)
print("Timp masurat de response.elapsed: ", durata_requests)
# time.perf_counter() masoara tot timpul executiei in Python,
# iar response.elapsed masoara strict timpul pana la primirea antetelor.
time.sleep(1)

# ==========================================
# Exercitiul 8
# ==========================================
try:
    import bs4
    print("Modulul bs4 este deja instalat.")
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4.")
