#A1---------
import argparse, json, os ,subprocess
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce lista liniilor .strip(), fara cele goale si fara cele cu #
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
#cai = citeste_linii("arsenal/privesc/start/suid.txt")
#print("linii SUID:", len(cai))
#A2---------
def nume(cale):
    # TODO: intoarce ce e dupa ultimul "/"  (vezi rsplit)
    return cale.rsplit("/", 1)[-1]

#nume_unice = {nume(c) for c in cai}    # set comprehension
#print("SUID distincte:", len(nume_unice))
#A3---------
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}
 
def suid_constatari(cale):
    cai = citeste_linii(cale)
    rezultat=[]
    # TODO: pentru fiecare cale UNICA, in ordine sortata, un dict:
    #   {"cale": c, 
     #   "nume": nume(c),
    #    "risc": "mare" daca nume(c) in GTFO, altfel "normal"}
    for c in sorted(set(cai)):
        nume_fisier=nume(c)
        if nume_fisier in GTFO:
            risc_curent = "mare"
        else:
            risc_curent= "normal"
        rezultat.append({
            "cale":c,
            "nume":nume_fisier,
            "risc":risc_curent
        })
    return rezultat


#suid = suid_constatari("arsenal/privesc/start/suid.txt")
#mari = [c for c in suid if c["risc"] == "mare"]
#print(len(suid), "SUID,", len(mari), "cu risc mare")
#print(sorted(c["nume"] for c in mari))

#A4---------
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)   # despachetare in tuplu
        # TODO: adauga {"user": user.strip(), 
        #               "drept": drept.strip(),
        #               "risc": "mare" daca "NOPASSWD" in drept, altfel "normal"}
        out.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal"
        })
    return out
        
 
def cron_constatari(cale):
    # TODO: campuri = ln.split(); user = campuri[5];
    #   comanda = " ".join(campuri[6:]); dict cu user si comanda
    out=[]
    for ln in citeste_linii(cale):
        campuri=ln.split()
        user=campuri[5]
        comanda = " ".join(campuri[6:])
        out.append({
           "user":user,
           "comanda":comanda
        })
    return out
def enumereaza(d):
    return {
        "suid": suid_live(),
        
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }
def suid_live():
    """Scanează sistemul live pentru fișiere SUID."""
  
    comanda = ["find", "/", "-perm", "-4000", "-type", "f"]
    rezultat = subprocess.run(
        comanda,
        stdout=subprocess.PIPE,
        text=True,
        stderr=subprocess.DEVNULL
    )

    
    linii = rezultat.stdout.strip().split("\n")
    rezultat = []
    for c in linii:
        if c:  
            nume_fisier = c.split("/")[-1]
            
            
            if nume_fisier in GTFO:
                risc_curent = "mare"
            else:
                risc_curent = "normal"
                
            
            rezultat.append({
                "nume": nume_fisier,
                "cale": c,
                "risc": risc_curent
            })
            
    return rezultat
    #A5---------
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    p.add_argument("--risc-mare", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    raport_grupat={}
    for lista in raport.values():
        for item in lista:
            riscul = item.get("risc")
            nume = item.get("nume", item.get("user"))
            raport_grupat.setdefault(riscul, []).append(nume)
    if a.risc_mare:
        raport = {
            categorie: [item for item in lista if item.get("risc") == "mare"]
            for categorie, lista in raport.items()
        }
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False)); return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
    # TODO: utilizatorii implicati = multimea userilor din sudo REUNITA cu cei din cron
    sudo_unic = {item["user"] for item in raport["sudo"]}
    cron_unic = {item["user"] for item in raport["cron"]}
    grup=sudo_unic | cron_unic
    text_final = ", ".join(sorted(grup))
    print(f"utilizatori implicati: {text_final}")
    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")
    print("\nRaport grupat după risc:")
    print(json.dumps(raport_grupat, indent=2)) 
 
if __name__ == "__main__":
    main()


#A6---------
