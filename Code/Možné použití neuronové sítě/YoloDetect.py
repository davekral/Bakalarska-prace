from ultralytics import YOLO
import os
import cv2
import json
from moviepy.editor import VideoFileClip

# ---------------- Nastavení ----------------
model_path = "best1.pt"
video_path = "video.avi"

conf_threshold = 0.6
iou_threshold = 0.4

output_project = "vystupy1"
output_name = "video_pred"

event_labels = ['pierce', 'pull', 'knot_valid', 'needle_on_skin', 'knot_preparation', 'cut_valid','needle_extraction']
event_frame_threshold = 10      # kolik snímků po sobě považujeme za událost
gap_tolerance = 3              # kolik snímků jiné třídy mezi "shodou" ještě považujeme za pokračování

# ---------------- Kontrola vstupů ----------------
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model nebyl nalezen: {model_path}")
if not os.path.exists(video_path):
    raise FileNotFoundError(f"Video nebylo nalezeno: {video_path}")

# ---------------- Načtení FPS videa ----------------
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS) or 25  # fallback
cap.release()
print(f"🎞️ FPS videa: {fps:.2f}")

# ---------------- Predikce ----------------
model = YOLO(model_path)
results = model.predict(
    source=video_path,
    conf=conf_threshold,
    iou=iou_threshold,
    save=True,
    project=output_project,
    name=output_name
)

# ---------------- Sběr detekcí ----------------
frame_events = []
for frame in results:
    labels_in_frame = [model.names[int(cls)] for cls in frame.boxes.cls]
    frame_events.append(labels_in_frame)

# ---------------- Detekce událostí ----------------
events = []
for label in event_labels:
    active = False
    start_idx = None
    count = 0
    gap = 0

    for i, detected in enumerate(frame_events):
        if label in detected:
            if not active:
                start_idx = i
                count = 1
                gap = 0
                active = True
            else:
                count += 1
                gap = 0
        else:
            if active:
                gap += 1
                if gap <= gap_tolerance:
                    count += 1  # stále pokračujeme
                else:
                    if count >= event_frame_threshold:
                        time_sec = start_idx / fps
                        events.append({
                            "label": label,
                            "frame": start_idx,
                            "time": round(time_sec, 2)
                        })
                    active = False
                    count = 0
                    gap = 0

    # případně přidat poslední detekci na konci
    if active and count >= event_frame_threshold:
        time_sec = start_idx / fps
        events.append({
            "label": label,
            "frame": start_idx,
            "time": round(time_sec, 2)
        })

events = sorted(events, key=lambda x: x["time"])


# ---------------- Uložení JSON ----------------
output_dir = os.path.join(output_project, output_name)
os.makedirs(output_dir, exist_ok=True)

json_path = os.path.join(output_dir, "events.json")
with open(json_path, "w") as f:
    json.dump(events, f, indent=2)

# ---------------- Převod videa do MP4 ----------------
avi_path = os.path.join(output_dir, "video.avi")
mp4_path = os.path.join(output_dir, "video.mp4")

if os.path.exists(avi_path) and not os.path.exists(mp4_path):
    print("🔄 Převádím video do MP4...")
    clip = VideoFileClip(avi_path)
    clip.write_videofile(mp4_path, codec="libx264", audio_codec="aac")
    clip.close()

# ---------------- HTML přehrávač ----------------
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>YOLO Video Viewer</title>
    <style>
        body {{ font-family: sans-serif; }}
        button {{ margin: 4px; padding: 4px 8px; }}
    </style>
</head>
<body>
    <h2>Video s událostmi</h2>
    <video id="video" width="640" controls>
        <source src="video.mp4" type="video/mp4">
        Tvůj prohlížeč nepodporuje video tag.
    </video>
    <h3>Události:</h3>
    <ul>
"""

for event in events:
    html_content += f"""
        <li>
            <button onclick="document.getElementById('video').currentTime = {event['time']}">
                {event['label']} @ {event['time']}s
            </button>
        </li>
    """

html_content += """
    </ul>
</body>
</html>
"""

html_path = os.path.join(output_dir, "player.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Vše hotovo.")
print(f"📂 Výstupy: {output_dir}")
print(f"🌐 HTML přehrávač: {html_path}")
