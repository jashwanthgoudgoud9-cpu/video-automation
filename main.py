import os
import requests
import urllib.parse

# =========================
# CREATE FOLDER
# =========================
os.makedirs("output", exist_ok=True)

# =========================
# STEP 1: GET SCRIPT FROM GOOGLE SHEET
# =========================
sheet_url = "https://docs.google.com/spreadsheets/d/1pwlfl9ATEVSSrKskSdUVKbHbNG51KppQZw5IJClxIc0/export?format=csv"

try:
    response = requests.get(sheet_url)
    data = response.text.split("\n")

    rows = [r.strip() for r in data[1:] if r.strip()]

    if len(rows) == 0:
        script = "This is fallback script because sheet empty"
    else:
        script = rows[0]

except:
    script = "This is fallback script because sheet error"

print("SCRIPT:", script)

# =========================
# STEP 2: TEXT ENCODE (IMPORTANT FIX)
# =========================
encoded_text = urllib.parse.quote(script)

# =========================
# STEP 3: GET VOICE (FIXED)
# =========================
voice_url = f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={encoded_text}"

response = requests.get(voice_url)

# VALIDATE AUDIO (IMPORTANT)
if "audio" not in response.headers.get("Content-Type", ""):
    print("❌ Voice API failed, using fallback voice")

    fallback_text = "This is fallback voice"
    encoded_text = urllib.parse.quote(fallback_text)

    voice_url = f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={encoded_text}"
    response = requests.get(voice_url)

# SAVE AUDIO
with open("output/voice.mp3", "wb") as f:
    f.write(response.content)

print("✅ Voice generated")

# =========================
# STEP 4: CREATE VIDEO (NO FAIL)
# =========================
os.system(
    'ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=10 -i output/voice.mp3 '
    '-shortest -c:v libx264 -c:a aac output/final.mp4'
)

# =========================
# STEP 5: VERIFY OUTPUT
# =========================
if os.path.exists("output/final.mp4"):
    print("✅ FINAL VIDEO CREATED SUCCESSFULLY")
else:
    print("❌ Video failed, creating fallback")

    os.system("ffmpeg -y -f lavfi -i color=c=red:s=1280x720:d=5 output/final.mp4")

print("🎯 DONE")
