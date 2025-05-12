import cv2
import json
import os
from collections import defaultdict

INPUT_DIR = "D:/Škola/Bakalářka/Datasets/CVAT-Dataset"
OUTPUT_DIR = "output_clips"

def load_annotations(path):
    with open(path, 'r') as f:
        data = json.load(f)
    label_map = {i: label['name'] for i, label in enumerate(data["categories"]["label"]["labels"])}

    tag_frames = defaultdict(list)
    for item in data["items"]:
        frame_number = item["attr"]["frame"]
        for ann in item.get("annotations", []):
            tag = label_map[ann["label_id"]]
            tag_frames[tag].append(frame_number)
    return tag_frames

def validate_annotation_pairs(tag_frames, json_filename):
    valid = True
    for tag, frames in tag_frames.items():
        if len(frames) % 2 != 0:
            print(f"❌ Varování: Tag '{tag}' v souboru '{json_filename}' má lichý počet snímků ({len(frames)}).")
            valid = False
    if valid:
        print(f"✅ {json_filename} – anotace v pořádku.")
    return valid

def pair_frames_by_tag(tag_frames):
    tag_pairs = defaultdict(list)
    for tag, frames in tag_frames.items():
        frames.sort()
        if len(frames) < 2:
            continue
        i = 0
        while i < len(frames) - 1:
            start = frames[i]
            end = frames[i + 1]
            tag_pairs[tag].append((start, end))
            i += 2
    return tag_pairs

def extract_video_segments(video_path, tag_pairs):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    for tag, segments in tag_pairs.items():
        tag_folder = os.path.join(OUTPUT_DIR, "clips", tag)
        os.makedirs(tag_folder, exist_ok=True)
        for idx, (start, end) in enumerate(segments):
            cap.set(cv2.CAP_PROP_POS_FRAMES, start)
            out_path = os.path.join(tag_folder, f"{tag}_{start:05d}_{end:05d}.mp4")
            out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

            for i in range(start, end + 1):
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
            out.release()
    cap.release()

def save_frames_between_tags(video_path, tag_pairs):
    cap = cv2.VideoCapture(video_path)

    for tag, ranges in tag_pairs.items():
        tag_folder = os.path.join(OUTPUT_DIR, "frames", tag)
        os.makedirs(tag_folder, exist_ok=True)
        for (start, end) in ranges:
            for i in range(start, end + 1):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if not ret:
                    break
                filename = os.path.join(tag_folder, f"{tag}_{i:05d}.jpg")
                cv2.imwrite(filename, frame)

    cap.release()

def process_all_videos(input_dir):
    files = os.listdir(input_dir)
    videos = [f for f in files if f.lower().endswith('.mp4')]

    print("🔎 Kontroluji správnost anotací všech souborů...\n")
    validation_results = {}

    # První fáze – validace všech JSONů
    for video_file in videos:
        basename = os.path.splitext(video_file)[0]
        json_file = f"{basename}.json"
        json_path = os.path.join(input_dir, json_file)

        if not os.path.exists(json_path):
            print(f"⚠️ Chybí JSON k videu {video_file} – bude přeskočeno.")
            validation_results[basename] = False
            continue

        tag_frames = load_annotations(json_path)
        is_valid = validate_annotation_pairs(tag_frames, json_file)
        validation_results[basename] = is_valid

    print("\n📦 Spouštím zpracování videí se správnými anotacemi...\n")

    # Druhá fáze – zpracování pouze validních souborů
    for video_file in videos:
        basename = os.path.splitext(video_file)[0]
        if not validation_results.get(basename, False):
            print(f"⛔ {video_file} nebude zpracováno kvůli nevalidním anotacím.")
            continue

        video_path = os.path.join(input_dir, video_file)
        json_path = os.path.join(input_dir, f"{basename}.json")

        print(f"🟢 Zpracovávám {video_file}...")

        tag_frames = load_annotations(json_path)
        tag_pairs = pair_frames_by_tag(tag_frames)

        extract_video_segments(video_path, tag_pairs)
        save_frames_between_tags(video_path, tag_pairs)

    print("\n✅ Hotovo. Výstupy najdeš v složce:", OUTPUT_DIR)

if __name__ == "__main__":
    process_all_videos(INPUT_DIR)
