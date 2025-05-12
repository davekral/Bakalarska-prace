import os
import shutil
import random

def split_dataset(input_dir, output_base, split_ratios):
    assert sum(split_ratios) == 1.0, "Poměry musí dávat dohromady 1.0"

    tags = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

    for tag in tags:
        tag_path = os.path.join(input_dir, tag)
        files = os.listdir(tag_path)
        files = [f for f in files if os.path.isfile(os.path.join(tag_path, f))]
        random.shuffle(files)

        total = len(files)
        train_end = int(total * split_ratios[0])
        val_end = train_end + int(total * split_ratios[1])

        splits = {
            "train": files[:train_end],
            "val": files[train_end:val_end],
            "test": files[val_end:]
        }

        for split_name, split_files in splits.items():
            split_folder = os.path.join(output_base, split_name, tag)
            os.makedirs(split_folder, exist_ok=True)

            for filename in split_files:
                src = os.path.join(tag_path, filename)
                dst = os.path.join(split_folder, filename)
                shutil.copy2(src, dst)

            print(f"✅ {tag} – {split_name}: {len(split_files)} souborů")

    print("\n📦 Dataset rozdělen do složek:", output_base)

if __name__ == "__main__":
    # 📂 Složka se vstupními daty (např. frames nebo clips)
    INPUT_DIR = "D:/Škola/Bakalářka/Datasets/output_clips/clips"  # nebo "output_clips/clips"
    # 📁 Složka, kam se rozdělí výstup
    OUTPUT_DIR = "dataset_clips"
    # ⚖️ Poměry pro train, val, test (např. 70 % trénink, 15 % validace, 15 % test)
    SPLIT_RATIOS = (0.80, 0.10, 0.10)

    split_dataset(INPUT_DIR, OUTPUT_DIR, SPLIT_RATIOS)
