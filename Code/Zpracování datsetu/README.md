# Zpracování datasetu

Tato složka obsahuje skript pro automatické rozdělení videí s chirurgickým šitím na kratší úseky podle časových anotací (tzv. _tagů_) exportovaných z nástroje [CVAT](https://cvat.org/). Součástí skriptu je i uložení jednotlivých snímků těchto úseků pro další použití.

## ✅ Požadavky na vstupní data

Každé video musí mít odpovídající anotaci ve formátu `Datumaro`, exportovanou z CVATu. Konkrétně:

- **Video:** `nazev.mp4`
- **Anotace:** `nazev.json`  
  ve formátu _Datumaro 1.0_, který obsahuje pouze **tagy** (časové značky začátku a konce akcí).


