import requests
import os

sheet_url = "https://docs.google.com/spreadsheets/d/1pwlfl9ATEVSSrKskSdUVKbHbNG51KppQZw5IJClxIc0/export?format=csv"

data = requests.get(sheet_url).text.split("\n")
rows = [r.strip() for r in data[1:] if r.strip()]

# track which script used
if os.path.exists("index.txt"):
    with open("index.txt", "r") as f:
        index = int(f.read().strip())
else:
    index = 0

# get script
script = rows[index]

# update index
with open("index.txt", "w") as f:
    f.write(str((index + 1) % len(rows)))

print("Using script:", script)

# STEP 2: Scene split
scenes = [s.strip() for s in script.split('.') if s.strip()]

# STEP 3: Voice
for i, scene in enumerate(scenes):
    os.system(f'edge-tts --text "{scene}" --voice en-US-AriaNeural --write-media audio/voice_{i}.mp3')

# STEP 4: Create simple clips
for i in range(len(scenes)):
    os.system(f'ffmpeg -f lavfi -i color=c=black:s=1280x720:d=3 clips/clip_{i}.mp4')

# STEP 5: Merge clip + voice
for i in range(len(scenes)):
    os.system(f'ffmpeg -i clips/clip_{i}.mp4 -i audio/voice_{i}.mp3 -shortest -c:v libx264 -c:a aac output/scene_{i}.mp4')

# STEP 6: Combine all
with open("list.txt", "w") as f:
    for i in range(len(scenes)):
        f.write(f"file 'output/scene_{i}.mp4'\n")

os.system("ffmpeg -f concat -safe 0 -i list.txt -c copy output/final.mp4")

print("DONE")
