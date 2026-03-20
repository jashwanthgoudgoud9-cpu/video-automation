import os
import requests
from gtts import gTTS

os.makedirs("output", exist_ok=True)

sheet_url = "https://docs.google.com/spreadsheets/d/1pwlfl9ATEVSSrKskSdUVKbHbNG51KppQZw5IJClxIc0/export?format=csv"

script = "This is fallback script because sheet read failed."

try:
    response = requests.get(sheet_url, timeout=30)
    response.raise_for_status()
    lines = [line.strip() for line in response.text.splitlines() if line.strip()]
    if len(lines) > 1:
        first_data_row = lines[1]
        if "," in first_data_row:
            script = first_data_row.split(",", 1)[0].strip().strip('"')
        else:
            script = first_data_row.strip().strip('"')
        if not script:
            script = "This is fallback script because sheet row was empty."
except Exception as e:
    print("Sheet read failed:", e)

print("SCRIPT:", script)

try:
    tts = gTTS(text=script, lang="en")
    tts.save("output/voice.mp3")
    print("Voice generated successfully")
except Exception as e:
    print("gTTS failed:", e)
    raise

cmd = (
    'ffmpeg -y '
    '-f lavfi -i color=c=black:s=1280x720:d=15 '
    '-i output/voice.mp3 '
    '-shortest '
    '-c:v libx264 -pix_fmt yuv420p '
    '-c:a aac '
    'output/final.mp4'
)

exit_code = os.system(cmd)
print("FFmpeg exit code:", exit_code)

if not os.path.exists("output/final.mp4"):
    raise FileNotFoundError("final.mp4 was not created")

print("DONE")
