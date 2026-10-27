import re
from PIL import Image
from PIL.ExifTags import TAGS

def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"): return "pdf"
    if cap.startswith(b"\x89PNG"): return "png"
    if cap.startswith(b"\xff\xd8"): return "jpeg"
    if cap.startswith(b"PK\x03\x04"): return "zip/docx"
    return cap.hex()

print("Tip real:", tip_real("probe/foto.jpg"))
print("Tip real:", tip_real("probe/ascuns.png"))

date_ascuns = open("probe/ascuns.png", "rb").read()
print("\n[Strings în ascuns.png]")
for m in re.findall(rb"[ -~]{4,}", date_ascuns)[-5:]:
    print(m.decode())

print("\n[Metadate GPS foto.jpg]")
exif = Image.open("probe/foto.jpg")._getexif() or {}
for id, val in exif.items():
    if id == 34853:
        print("Coordonate GPS:", val)

i = date_ascuns.find(b"PK\x03\x04")
if i != -1:
    open("gasit.zip", "wb").write(date_ascuns[i:])
    print("\nArhivă extrasă la octetul", i)
