# Kódy k bakalářské práci

Tato složka obsahuje zdrojové kódy k bakalářské práci _Detekce klíčových událostí během chirurgického šití z videa pomocí metod strojového učení_. Kódy jsou rozděleny podle jednotlivých fází zpracování dat a trénování modelů.

## Struktura složek

- **Možné použití neuronové sítě**  
  Ukázky využití vytrénovaných modelů pro detekci a klasifikaci chirurgických akcí ve videích.

- **Rozdělení datasetu**  
  Skripty pro rozdělení anotovaných dat do trénovací, validační a testovací části.

- **Trénování 3D konvoluční sítě**  
  Kód pro návrh a trénování vlastních 3D konvolučních neuronových sítí na sekvencích chirurgických videí.

- **Trénování sítí YOLO**  
  Soubory potřebné pro trénování a inference modelu YOLO11 pro detekci a klasifikaci snímků.

- **Zpracování datasetu**  
  Skripty pro zpracování anotací z nástroje CVAT (včetně dělení videí podle tagů a ukládání snímků).

## Poznámky

- Trénování bylo prováděno v prostředí Google Colab s využitím GPU.
- Kód je kompatibilní s knihovnami TensorFlow, PyTorch a Ultralytics YOLO.
- Dataset použitý k trénování není součástí repozitáře z důvodu ochrany osobních údajů.
