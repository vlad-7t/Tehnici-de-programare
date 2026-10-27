import re
import base64
import hashlib
import argparse
import json
from urllib.parse import unquote

def ghici_strat(s):
    if "%" in s: return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0: return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s): return "base64"
    return "necunoscut"

def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64": return strat, base64.b64decode(s)
    elif strat == "hex": return strat, bytes.fromhex(s)
    elif strat == "url": return strat, unquote(s).encode()
    return strat, s.encode()

def citibil(b):
    return all(32 <= c < 127 for c in b)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare", nargs="?", default="")
    p.add_argument("--fisier", action="store_true")
    p.add_argument("--xor", action="store_true")
    p.add_argument("--hash", action="store_true")
    a = p.parse_args()

    if a.xor:
        date = open("probe/xor.bin", "rb").read()
        for k in range(256):
            clar = bytes(b ^ k for b in date)
            if citibil(clar):
                print("cheie:", k, clar.decode())
        exit(0)

    if a.hash:
        tinta = open("probe/hashuri.txt").readline().strip()
        for cuv in open("probe/wordlist.txt", encoding="latin1"):
            cuv = cuv.strip()
            if hashlib.md5(cuv.encode()).hexdigest() == tinta:
                print("gasit:", cuv)
                break
        exit(0)

    if not a.intrare: exit(0)

    val = open(a.intrare, "r").read().strip() if a.fisier else a.intrare
    straturi_gasite = []
    rezultat = None
    for _ in range(8):
        strat, b = desfa(val)
        straturi_gasite.append(strat)
        if citibil(b):
            rezultat = b.decode()
            if ghici_strat(rezultat) == "necunoscut": break
            val = rezultat
            continue
        try: val = b.decode()
        except UnicodeDecodeError: break

    fisa = {"strat": straturi_gasite, "rezultat": rezultat or b.decode(errors="ignore")}
    with open("arsenal/forensics/fisa.json", "w") as f:
        json.dump(fisa, f)
    print("Salvat în fisa.json")
