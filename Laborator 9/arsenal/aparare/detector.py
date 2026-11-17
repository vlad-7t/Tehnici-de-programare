import argparse, json

from datetime import datetime
from collections import Counter
from arsenal.aparare.parse_auth import citeste_esecuri
#B1---------
def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    # TODO: intoarce lista de (ip, n) cu n >= prag,
    #       sortata descrescator dupa n
    return [(ip,n) for ip,n in counts.most_common() if n >= prag]
        

#c = Counter({"203.0.113.9": 13, "198.51.100.7": 2})
#print(suspecti(c))
#print(suspecti(c, prag=2))
 #B2---------
 #python -c "from arsenal.aparare.detector import suspecti; suspecti({}, 0)"
#B3---------
def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    p.add_argument("--top", type=int, default=None, help="afiseaza doar primele N adrese")
    a = p.parse_args()
    if a.top is not None and a.top < 1:
        raise ValueError(f"top invalid: {a.top} (cel putin 1)")
    esecuri = citeste_esecuri(a.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, a.prag)
    rez = counts.most_common(a.top)
    rezultat = {ip:n for ip ,n in rez}
    # TODO: cu --json, scoate json.dumps cu {esecuri, pe_ip, suspecti};
    #       fara, un rezumat cu "BRUTE FORCE" pe fiecare suspect

    if a.json:
        raport={
            "esecuri": esecuri,
            "pe_ip":rezultat,
            "suspecti":sus
        }
        
        print(json.dumps(raport, indent=2))
    else:
        print(f"Esecuri de autentificare: {len(esecuri)}")
        for ip, n in rezultat.items():
            print(f"  {ip}: {n}")
        print(f"Suspecti (prag {a.prag}):")
        for ip, n in sus:
            print(f"  {ip}  ({n} incercari)  BRUTE FORCE")

if __name__ == "__main__": main()

