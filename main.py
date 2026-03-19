import os
import requests

os.makedirs("output", exist_ok=True)

# =========================
# GET SCRIPT FROM SHEET
# =========================
sheet_url = "https://docs.google.com/spreadsheets/d/1pwlfl9ATEVSSrKskSdUVKbHbNG51KppQZw5IJClxIc0/export?format=csv"

try:
    data = requests.get(sheet_url).text.split("\n")
    rows = [r.strip() for r in data[1:] if r.strip()]
    script = rows[0] if rows else "This is a fallback script"
except:
    script = "This is a fallback script"

print("SCRIPT:", script)

# =========================
# VOICE (STABLE)
# =========================
voice_url = f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={script}"
audio = requests.get(voice_url).content

with open("output/voice.mp3", "wb") as f:
    f.write(audio)

# =========================
# VIDEO (ONE COMMAND - NO FAIL)
# =========================
os.system(
    'ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=10 -i output/voice.mp3 '
    '-shortest -c:v libx264 -c:a aac output/final.mp4'
)

print("✅ FINAL VIDEO CREATED")
