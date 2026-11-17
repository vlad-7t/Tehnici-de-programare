import re
import sys
from collections import Counter
#A1---------------
TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")
 
def esec(linie):
    
    m = TIPAR.search(linie)
    # TODO: daca m e None, intoarce None;
    #       altfel intoarce (m.group(1), m.group(2))
    
    if m == None:
        return None
    else:
        return (m.group(1), m.group(2))
 
print(esec("... Failed password for root from 203.0.113.9 port 51230 ssh2"))
print(esec("<linie stricata fara structura>"))
#A2---------------
def citeste_esecuri(cale):
    esecuri = []
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri
    with f:
        for linie in f:
            r = esec(linie)
            # TODO: daca r nu e None, adauga {"user": r[0], "ip": r[1]}
            if r is not None:
                esecuri.append({
                    "user": r[0],
                    "ip": r[1]
                })

    return esecuri
 
esecuri = citeste_esecuri("arsenal/aparare/start/auth.log")
print("esecuri:", len(esecuri))
#A3---------------
from collections import Counter
 
def pe_ip(esecuri):
    # TODO: intoarce un Counter al adreselor din esecuri
    #       (Counter(e["ip"] for e in esecuri))
    
    nr=Counter(e["ip"] for e in esecuri)
    return nr
counts = pe_ip(esecuri)
for ip, n in counts.most_common():
    print(f"  {ip}: {n}")
#A4---------------
#python -m arsenal.aparare.parse_auth arsenal/aparare/start/auth.log
def main():
    cale = sys.argv[1]
    lista = citeste_esecuri(cale)
    print(f"Esecuri de autentificare:{len(lista)}")
    counts=pe_ip(esecuri)
    for ip, n in counts.most_common():
        print(f" {ip}:{n}")
    


if __name__ == "__main__":
    main()