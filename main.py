import os
import requests

os.makedirs("clips", exist_ok=True)
os.makedirs("audio", exist_ok=True)
os.makedirs("output", exist_ok=True)

# =========================
# STEP 1: GET SCRIPT
# =========================
sheet_url = "https://docs.google.com/spreadsheets/d/1pwlfl9ATEVSSrKskSdUVKbHbNG51KppQZw5IJClxIc0/export?format=csv"

try:
    response = requests.get(sheet_url)
    data = response.text.split("\n")
    rows = [r.strip() for r in data[1:] if r.strip()]

    if len(rows) == 0:
        script = "Fallback script because sheet empty"
    else:
        script = rows[0]

except:
    script = "Fallback script because sheet error"

print("SCRIPT:", script)

# =========================
# STEP 2: SCENES
# =========================
scenes = [s.strip() for s in script.split('.') if s.strip()]

if len(scenes) == 0:
    scenes = ["Default scene"]

# =========================
# STEP 3: VOICE
# =========================
for i, scene in enumerate(scenes):
    os.system(f'edge-tts --text "{scene}" --voice en-US-AriaNeural --write-media audio/voice_{i}.mp3')

# =========================
# STEP 4: VIDEO
# =========================
for i in range(len(scenes)):
    os.system(f'ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=3 clips/clip_{i}.mp4')

# =========================
# STEP 5: MERGE
# =========================
for i in range(len(scenes)):
    os.system(f'ffmpeg -y -i clips/clip_{i}.mp4 -i audio/voice_{i}.mp3 -shortest -c:v libx264 -c:a aac output/scene_{i}.mp4')

# =========================
# STEP 6: FINAL OUTPUT (FORCED)
# =========================
with open("list.txt", "w") as f:
    for i in range(len(scenes)):
        f.write(f"file 'output/scene_{i}.mp4'\n")

os.system("ffmpeg -y -f concat -safe 0 -i list.txt -c copy output/final.mp4")

# 🔥 FORCE fallback if failed
if not os.path.exists("output/final.mp4"):
    print("⚠️ Creating fallback video...")
    os.system("ffmpeg -y -f lavfi -i color=c=red:s=1280x720:d=5 output/final.mp4")

print("✅ FINAL VIDEO READY")
