import argparse
import csv
from datetime import datetime
import webtools

# ==========================================
# Exercitiul 47
# ==========================================
# Explicație: Dacă main.py ar avea propria funcție get_title, ultima definită sau 
# importată în fișier ar suprascrie-o pe cealaltă, cauzând un conflict de nume.

# ==========================================
# Exercitiul 48
# ==========================================
parser = argparse.ArgumentParser()
parser.add_argument("url", help="Adresa web pe care vrei să o analizezi")
args = parser.parse_args()

print(f"Analizăm adresa: {args.url}")
print("Antetele implicite:", webtools.DEFAULT_HEADERS)

# ==========================================
# Exercitiul 49
# ==========================================
cai_de_verificat = ["/", "/robots.txt", "/sitemap.xml"]
rezultate = webtools.check_paths(args.url, cai_de_verificat)

with open("report.csv", "w", newline="") as fisier:
    scriitor = csv.writer(fisier)
    scriitor.writerow(["path", "status", "checked_at"])
    
    for cale, stare in rezultate.items():
        ora_curenta = datetime.now().isoformat()
        scriitor.writerow([cale, stare, ora_curenta])

# ==========================================
# Exercitiul 50
# ==========================================
webtools.site_report(args.url)