

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  

import time as t
import requests

# ==========================================
# Exercitiul 9
# ==========================================
raspuns9 = requests.get(BASE_URL, timeout=TIMEOUT)
print(raspuns9.status_code) 
print(raspuns9.ok)           
print(raspuns9.url)          
print(raspuns9.encoding)    
t.sleep(1)

# ==========================================
# Exercitiul 10
# ==========================================
try:
    raspuns10 = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    raspuns10.raise_for_status()
except requests.HTTPError:
    print("Pagina cautata nu exista")
t.sleep(1)

# ==========================================
# Exercitiul 11
# ==========================================
for nume, valoare in raspuns9.headers.items():
    print(f"{nume}: {valoare}")
t.sleep(1)

# ==========================================
# Exercitiul 12
# ==========================================
print(raspuns9.headers.get("Server", "lipseste"))
print(raspuns9.headers.get("Content-Type", "lipseste"))
print(raspuns9.headers.get("content-type", "lipseste"))
t.sleep(1)
# Dictionarul de antete din requests este case-insensitive (nu tine cont de litere mari/mici).

# ==========================================
# Exercitiul 13
# ==========================================
# Putem inlantui metodele pentru ca .lower() returneaza un string,
# pe care putem apela direct metoda .count().
print(raspuns9.text.lower().count("cyber"))
t.sleep(1)

# ==========================================
# Exercitiul 14
# ==========================================
raspuns14 = requests.get(BASE_URL, timeout=TIMEOUT)
start = raspuns14.text.find("<title>") + len("<title>")
end = raspuns14.text.find("</title>")
print(raspuns14.text[start:end].strip())
t.sleep(1)

# ==========================================
# Exercitiul 15
# ==========================================
respuns15 = requests.get(BASE_URL, timeout=TIMEOUT)
lines = respuns15.text.splitlines()
print("Număr total de linii:", len(lines))
cea_mai_lunga = max(lines, key=len)
print("Lungimea celei mai lungi linii:", len(cea_mai_lunga))
t.sleep(1)

# ==========================================
# Exercitiul 16
# ==========================================
raspuns16 = requests.get(ECHO_URL + "/get", timeout=TIMEOUT)
if raspuns16.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")
t.sleep(1)

# ==========================================
# Exercitiul 17
# ==========================================
raspuns17 = requests.get("http://cybercor.org", timeout=TIMEOUT)
for r in raspuns17.history:
    print(r.status_code, r.url)
print("URL final:", raspuns17.url)
t.sleep(1)

# ==========================================
# Exercitiul 18
# ==========================================
raspuns18a = requests.get(ECHO_URL + "/get", timeout=TIMEOUT)
t.sleep(1)
raspuns18b = requests.head(ECHO_URL + "/get", timeout=TIMEOUT)
print(len(raspuns18a.content))
print(len(raspuns18b.content))
# Cererea GET descarca intregul corp, pe cand HEAD cere doar antetele (lungime 0).
t.sleep(1)

# ==========================================
# Exercitiul 19
# ==========================================
raspuns19 = requests.get(ECHO_URL + "/get", timeout=TIMEOUT)
if len(raspuns19.cookies) == 0:
    print("Niciun cookie setat")
else:
    for cookie in raspuns19.cookies:
        print(f"{cookie.name}: {cookie.secure}")
t.sleep(1)

# ==========================================
# Exercitiul 20
# ==========================================
sesiune = requests.Session()
sesiune.headers.update({"User-Agent": "WebLab-CemortanVladislav"})
raspuns20 = sesiune.get(ECHO_URL + "/headers", timeout=TIMEOUT)
date_server = raspuns20.json()
print("Antetele văzute de server:")
print(date_server["headers"])
# response.text este un atribut (variabila stocata), iar response.json() este o metoda (functie care proceseaza textul).
