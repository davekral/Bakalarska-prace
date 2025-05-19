# Zpracování datasetu

Tato složka obsahuje skript pro automatické rozdělení videí s chirurgickým šitím na kratší úseky podle časových anotací (tzv. _tagů_) exportovaných z nástroje [CVAT](https://cvat.org/). Součástí skriptu je i uložení jednotlivých snímků těchto úseků pro další použití.

## Požadavky na vstupní data

Každé video musí mít odpovídající anotaci ve formátu `Datumaro`, exportovanou z CVATu. Konkrétně:

- **Video:** `nazev.mp4`
- **Anotace:** `nazev.json`  
  ve formátu _Datumaro 1.0_, který obsahuje pouze **tagy** (časové značky začátku a konce akcí).
  
## Výstup

Po spuštění skriptu bude výstup uložen do složky `output_clips`, kde vzniknou dvě hlavní větve:

- `output_clips/clips/` — krátké videosekvence jednotlivých akcí
- `output_clips/frames/` — jednotlivé snímky z těchto sekvencí

Každá třída akcí má vlastní složku a názvy souborů obsahují název akce a rozsah snímků.

## Co skript dělá

1. Načte videa a jejich odpovídající `.json` soubory.
2. Z validních anotací vyhledá páry snímků, které vymezují každou akci.
3. Pro každou akci:
   - Uloží daný úsek videa jako `.mp4`
   - Uloží jednotlivé snímky jako `.jpg`
4. Pokud jsou v anotaci nesprávné nebo liché počty snímků, dané video nebude zpracováno.
