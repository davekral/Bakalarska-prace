import shutil
import random
from pathlib import Path

# Cesty ke složkám
images_dir = Path("D:/Škola/Bakalářka/Datasets/YoloFull/images/train")
labels_dir = Path("D:/Škola/Bakalářka/Datasets/YoloFull/labels/train")

# Výstupní složky
output_base = Path(".")
splits = ["train", "valid", "test"]
split_ratios = [0.8, 0.1, 0.1]  # 80 % train, 10 % valid, 10 % test

# Vytvoření výstupních složek
for split in splits:
    (output_base / split / "images").mkdir(parents=True, exist_ok=True)
    (output_base / split / "labels").mkdir(parents=True, exist_ok=True)

# Najdi odpovídající páry obrázek–label
valid_pairs = []

# Vytvoř slovník labelů podle názvu bez přípony
label_dict = {f.stem: f for f in labels_dir.glob("*.txt")}

for img_file in images_dir.iterdir():
    if img_file.suffix.lower() != ".png":
        continue  # přeskoč soubory, které nejsou PNG

    label_file = label_dict.get(img_file.stem)
    if label_file and label_file.exists():
        valid_pairs.append((img_file, label_file))
    else:
        print(f"⚠️ Nenalezen label pro {img_file.name}")

# Zamíchej data a rozděl podle poměrů
random.shuffle(valid_pairs)
total = len(valid_pairs)
train_end = int(split_ratios[0] * total)
valid_end = train_end + int(split_ratios[1] * total)

datasets = {
    "train": valid_pairs[:train_end],
    "valid": valid_pairs[train_end:valid_end],
    "test": valid_pairs[valid_end:]
}

# Zkopíruj soubory do výstupních složek
for split, pairs in datasets.items():
    for img_path, label_path in pairs:
        shutil.copy(img_path, output_base / split / "images" / img_path.name)
        shutil.copy(label_path, output_base / split / "labels" / label_path.name)

print(f"✅ Hotovo! Zpracováno: {total} dvojic.")
