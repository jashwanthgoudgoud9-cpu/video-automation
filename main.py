import os
from moviepy.editor import ColorClip

os.makedirs("output", exist_ok=True)

clip = ColorClip(size=(1280,720), color=(255, 0, 0))
clip = clip.set_duration(5)

clip.write_videofile("output/video.mp4", fps=24)
