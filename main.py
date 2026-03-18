import os
from moviepy.editor import ColorClip

os.makedirs("output", exist_ok=True)

# Create simple color video (NO ERROR)
clip = ColorClip(size=(1280,720), color=(0, 0, 0))
clip = clip.set_duration(5)

clip.write_videofile("output/video.mp4", fps=24)
