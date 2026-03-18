import os
from moviepy.video.VideoClip import ColorClip

# create output folder
os.makedirs("output", exist_ok=True)

# create simple video
clip = ColorClip(size=(1280, 720), color=(0, 0, 255))
clip = clip.set_duration(3)

# export video
clip.write_videofile("output/video.mp4", fps=24)
