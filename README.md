# Detekce klíčových událostí během chirurgického šití z videa pomocí metod strojového učení

Tento repozitář obsahuje veškerý kód, skripty a konfigurace použité v rámci bakalářské práce obhájené na Fakultě aplikovaných věd ZČU v Plzni v roce 2025.

## 🎯 Cíl práce

Cílem bylo navrhnout, implementovat a porovnat různé metody strojového učení pro automatickou detekci a klasifikaci klíčových chirurgických akcí ve videích chirurgického šití, a to s využitím:

- objektové detekce pomocí modelu **YOLOv11**,
- klasifikace snímků pomocí upravené verze YOLOv11,
- sekvenční klasifikace pomocí vlastních **3D konvolučních neuronových sítí**.

## 🧠 Použité modely

| Model                   | Úloha                         | Přesnost             |
|------------------------|-------------------------------|----------------------|
| YOLOv11s – Detekce     | Lokalizace akcí (bounding box) | mAP@50 = 94,7 %      |
| YOLOv11s – Klasifikace | Klasifikace snímků            | Top-1 = 98,5 %       |
| LiteRes3DNet           | Klasifikace videosekvencí     | Přesnost ≈ 39 %      |


## 🛠️ Použité technologie

- **Python 3.11**, **PyTorch 2.6**, **TensorFlow 2.13**
- **Ultralytics YOLOv11**
- **Google Colab** – GPU akcelerace (Tesla T4)
- **CVAT, OpenCV** – anotace a práce s videi
- **Weights & Biases** – monitoring tréninku

## 📊 Dataset

Datasety vznikly z videí online kurzu chirurgického šití vedeného prof. Utou Dahmen (Universitätsklinikum Jena). Obsahují:
- 6000 anotovaných snímků pro detekci
- 18 000 snímků pro klasifikaci
- 380 videosekvencí pro trénink 3D CNN

Anotace zahrnují 7 tříd:
- `pierce`, `needle_extraction`, `needle_on_skin`, `pull`, `knot_preparation`, `knot_valid`, `cut_valid`

## 🧪 Výsledky

Detekční model YOLO11s dosáhl vysoké přesnosti mAP@50 přes 94 %. Klasifikační verze dosáhla Top-1 přesnosti 98,5 %. Vlastní 3D konvoluční síť LiteRes3DNet byla optimalizována pro Google Colab a ukázala potenciál pro zpracování videí s časovou strukturou.

