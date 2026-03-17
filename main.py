import os
print("🚀 Automation Started")

os.makedirs("output", exist_ok=True)

with open("output/result.txt", "w") as f:
    f.write("Automation is working!")

print("✅ Done")
