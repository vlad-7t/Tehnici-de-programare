from PIL import Image

img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}\x00"
biti = "".join(f"{x:08b}" for x in mesaj)

px_nou = []
bit_idx = 0
for r, g, b in px:
    if bit_idx < len(biti): r = (r & ~1) | int(biti[bit_idx]); bit_idx += 1
    if bit_idx < len(biti): g = (g & ~1) | int(biti[bit_idx]); bit_idx += 1
    if bit_idx < len(biti): b = (b & ~1) | int(biti[bit_idx]); bit_idx += 1
    px_nou.append((r, g, b))

img.putdata(px_nou)
img.save("stego.png")

px_citit = list(Image.open("stego.png").convert("RGB").getdata())
biti_cititi = "".join(str(r & 1) + str(g & 1) + str(b & 1) for r, g, b in px_citit)

mesaj_extras = []
for idx in range(0, len(biti_cititi), 8):
    octet = int(biti_cititi[idx:idx+8], 2)
    if octet == 0: break
    mesaj_extras.append(octet)

print("Dezvăluit:", bytes(mesaj_extras).decode())
