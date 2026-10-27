# Raport Forensics și Steganografie
## Lucrarea A: Decoderul universal
- **mesaj.txt**: Text clar `FLAG{straturi_de_encoding}` sub două straturi de Base64 și un strat Hex.
- **xor.bin**: Cheia este `128` (`0x80`). Text: `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`.
- **hashuri.txt**: MD5, parola `password`.

## Lucrarea B: Forensics pe fișiere
- **Semnături**: `foto.jpg` -> JPEG (`\xff\xd8`), `ascuns.png` -> PNG (`\x89PNG`).
- **GPS EXIF**: Chișinău (`47.0 N, 28.8575 E`).
- **File carving**: ZIP ascuns recuperat (`FLAG{ascuns_prin_carving}`).
- **Steganografie LSB**: Mesaj decodat `FLAG{ascuns_in_pixeli}`.
