import os
import csv
import requests
from io import StringIO
from gtts import gTTS

os.makedirs("output", exist_ok=True)

sheet_url = "https://docs.google.com/spreadsheets/d/1pwlfl9ATEVSSrKskSdUVKbHbNG51KppQZw5IJClxIc0/export?format=csv"

script = "This is fallback script because sheet read failed."

try:
    response = requests.get(sheet_url, timeout=30)
    response.raise_for_status()

    csv_text = response.text
    reader = csv.reader(StringIO(csv_text))
    rows = list(reader)

    if len(rows) > 1:
        header = rows[0]
        first_data_row = rows[1]

        print("HEADER:", header)
        print("FIRST DATA ROW:", first_data_row)

        # Try to find a script column
        script_col_index = None
        possible_names = ["script", "full_script", "video_script", "content", "text"]

        for i, col in enumerate(header):
            if col.strip().lower() in possible_names:
                script_col_index = i
                break

        # If no matching header found, use the longest cell in the row
        if script_col_index is not None and script_col_index < len(first_data_row):
            script = first_data_row[script_col_index].strip()
        else:
            longest_cell = max(first_data_row, key=lambda x: len(x.strip())) if first_data_row else ""
            script = longest_cell.strip()

        if not script:
            script = "This is fallback script because script cell was empty."
    else:
        script = "This is fallback script because no data rows found."

except Exception as e:
    print("Sheet read failed:", e)

print("FINAL SCRIPT:", script)
print("SCRIPT LENGTH:", len(script))

# gTTS works better with chunks for long text
def split_text(text, max_chars=4000):
    parts = []
    current = ""

    sentences = text.replace("\n", " ").split(". ")
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        piece = sentence + "."
        if len(current) + len(piece) <= max_chars:
            current += (" " if current else "") + piece
        else:
            if current:
                parts.append(current.strip())
            current = piece

    if current:
        parts.append(current.strip())

    return parts

parts = split_text(script)

if not parts:
    parts = ["This is fallback voice text."]

print("TOTAL PARTS:", len(parts))

mp3_files = []

for i, part in enumerate(parts):
    mp3_path = f"output/voice_part_{i}.mp3"
    print(f"Generating part {i+1}/{len(parts)}")
    tts = gTTS(text=part, lang="en")
    tts.save(mp3_path)
    mp3_files.append(mp3_path)

# Create concat file for ffmpeg
with open("output/audio_list.txt", "w", encoding="utf-8") as f:
    for mp3_file in mp3_files:
        f.write(f"file '{os.path.abspath(mp3_file)}'\n")

# Merge all mp3 parts into one
merge_audio_cmd = (
    'ffmpeg -y -f concat -safe 0 -i output/audio_list.txt '
    '-c copy output/voice_full.mp3'
)
audio_merge_exit = os.system(merge_audio_cmd)
print("Audio merge exit code:", audio_merge_exit)

if not os.path.exists("output/voice_full.mp3"):
    raise FileNotFoundError("voice_full.mp3 was not created")

# Create final video with full voice
video_cmd = (
    'ffmpeg -y '
    '-f lavfi -i color=c=black:s=1280x720:r=30 '
    '-i output/voice_full.mp3 '
    '-shortest '
    '-c:v libx264 -pix_fmt yuv420p '
    '-c:a aac '
    'output/final.mp4'
)
video_exit = os.system(video_cmd)
print("Video ffmpeg exit code:", video_exit)

if not os.path.exists("output/final.mp4"):
    raise FileNotFoundError("final.mp4 was not created")

print("DONE")
