import os
from moviepy.editor import TextClip, CompositeVideoClip

os.makedirs("output", exist_ok=True)

# Create simple video
clip = TextClip("Your Automation Working 🚀", fontsize=70, size=(1280,720))
clip = clip.set_duration(5)

video = CompositeVideoClip([clip])
video.write_videofile("output/video.mp4", fps=24)
