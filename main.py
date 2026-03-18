import os

# create output folder
os.makedirs("output", exist_ok=True)

# use ffmpeg to create video
os.system(
    "ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=3 -vf \"format=yuv420p\" output/video.mp4"
)

print("✅ Video created successfully")
