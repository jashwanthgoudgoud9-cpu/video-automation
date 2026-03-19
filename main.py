import os
import requests

# =========================
# CREATE REQUIRED FOLDERS
# =========================
os.makedirs("clips", exist_ok=True)
os.makedirs("audio", exist_ok=True)
os.makedirs("output", exist_ok=True)

# =========================
# STEP 1: GET SCRIPT FROM GOOGLE SHEET
# =========================
sheet_url = "https://docs.google.com/spreadsheets/d/1pwlfl9ATEVSSrKskSdUVKbHbNG51KppQZw5IJClxIc0/export?format=csv"

try:
    response = requests.get(sheet_url)
    data = response.text.split("\n")

    # remove header + empty rows
    rows = [r.strip() for r in data[1:] if r.strip()]

    if not rows:
        raise Exception("No data found in sheet")

    # take first script
    script = rows[0]

except Exception as e:
    print("Error reading Google Sheet:", e)
    script = "This is fallback script because sheet failed."

print("Using script:", script)

# =========================
# STEP 2: SPLIT INTO SCENES
# =========================
scenes = [s.strip() for s in script.split('.') if s.strip()]

if len(scenes) == 0:
    scenes = [script]

print("Scenes:", scenes)

# =========================
# STEP 3: GENERATE VOICE
# =========================
for i, scene in enumerate(scenes):
    command = f'edge-tts --text "{scene}" --voice en-US-AriaNeural --write-media audio/voice_{i}.mp3'
    os.system(command)

# =========================
# STEP 4: CREATE SIMPLE VIDEO CLIPS
# =========================
for i in range(len(scenes)):
    command = f'ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=3 clips/clip_{i}.mp4'
    os.system(command)

# =========================
# STEP 5: MERGE CLIP + AUDIO
# =========================
for i in range(len(scenes)):
    command = f'ffmpeg -y -i clips/clip_{i}.mp4 -i audio/voice_{i}.mp3 -shortest -c:v libx264 -c:a aac output/scene_{i}.mp4'
    os.system(command)

# =========================
# STEP 6: COMBINE ALL SCENES
# =========================
with open("list.txt", "w") as f:
    for i in range(len(scenes)):
        f.write(f"file 'output/scene_{i}.mp4'\n")

os.system("ffmpeg -y -f concat -safe 0 -i list.txt -c copy output/final.mp4")

print("✅ FINAL VIDEO CREATED SUCCESSFULLY")
