import os

# create output folder
os.makedirs("output", exist_ok=True)

# create simple test file
with open("output/result.txt", "w") as f:
    f.write("SUCCESS - Automation is working perfectly!")
