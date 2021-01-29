#!/usr/bin/python

import os
import sys
import moviepy
from moviepy.video.io.VideoFileClip import VideoFileClip

version = "1.0"
folder = "./files/"
out_folder = "./compressed/"
arguments = sys.argv

# Check if user has provided an argument (ask for arguments because the user can't provide flags when starting from a build)
if len(arguments) < 2:
    print("Please provide a target file size in MB as number to start\n(and other optional arguments if you wish. Type help to see all options.):")
    userinput = input().split(" ")

    if "help" in userinput:
        print("\nPlease provide a file size in MB as number as the first argument.\nOptional arguments:")
        print("    -fps Number       | Changes the fps of the output clip.")
        print("    -res WidthxHeight | Changes the resolution of the output clip. Seperate Width and Height with a 'x'. Example: 1920x1080")
        print("    -no-retry         | The script won't retry to compress further even if the first run didn't reach the target size.\n")
        userinput = input().split(" ")

    # Push all new arguments
    for e in userinput:
        arguments.append(e)

    if len(arguments) < 2:
        print("Please provide a target filesize in Megabytes as the first argument!")
        sys.exit()

# Remove the first argument if it is the file name
if "mp4sizer" in arguments[0]: arguments.pop(0)

# Check if targetsize is a valid number
try:
    targetsize = float(arguments[0])
except:
    print("Your targetsize argument doesn't seem to be a valid number.")
    sys.exit() # stop here

print(f"mp4sizer by 3urobeat version {version}.")
print(f"Starting to compress files in ./files/ to {targetsize} MB...\n")

# Define the export part as a function to be able to call it again if we didn't reach our targetsize on the first run
def exportvideo(goalbitrate, iteration):
    if iteration > 5: # abort after 5 tries to not cause an endless loop
        print("I wasn't able to reach the target file size in 5 attempts. Please try a higher target size.\nAborting to not cause an endless loop...")
        sys.exit()

    try:
        # Export video with the calculated goalbitrate into the compressed folder and change fps if user wishes
        newfps = None
        if "-fps" in arguments:
            newfps = int(arguments[arguments.index("-fps") + 1])
            print(f"Changing the framerate from {origclip.fps} to {newfps}...")

        origclip.write_videofile('./compressed/' + file, bitrate=f"{goalbitrate * 1000}k", preset="fast", fps=newfps)

        # Check if the goal was reached and if not call again
        newsize = os.path.getsize('./compressed/' + file) / 1000000 # in MB

        if newsize > targetsize and "--no-retry" not in arguments:
            print(f"\n'{file}' is {newsize} MB and didn't reach {targetsize} in try {iteration}.\nTrying again with a slightly lower bitrate...")
            goalbitrate = goalbitrate - 0.2 # subtract a little bit from the bitrate
            exportvideo(goalbitrate, iteration + 1) # try again
        else:
            print(f"\n'{file}' was successfully compressed from {origsize} MB to {newsize} MB in {iteration} try/tries.")
    except:
        print(f"Couldn't export '{file}'. Please try again.")

# Iterate over all files in files folder
for file in os.listdir(folder):
    if "mp4" not in file: # check if file is not a valid video file
        print(f"File '{file}' is not a mp4! Skipping...")
        continue

    # Get a few values to be able to calculate the bitrate we would like to reach
    origsize = os.path.getsize('./files/' + file) / 1000000 # in MB
    origclip = VideoFileClip('./files/' + file)
    origduration = origclip.duration

    # Resize if the user wishes
    if "-res" in arguments:
        newres = arguments[arguments.index("-res") + 1].split("x")
        print(f"Resizing the clip from {origclip.size[0]}x{origclip.size[1]} to {newres[0]}x{newres[1]}")

        # RESIZE!
        import moviepy.video.fx.all as vfx
        origclip = vfx.resize(origclip, (newres[0], newres[1])) # pylint: disable=no-member

    # Calculate goalbitrate and export
    goalbitrate = 8 * targetsize / origduration # estimated bitrate we need to have to reach the provided filesize
    goalbitrate = goalbitrate - 0.15 # subtract a little bit for good measures to maybe avoid unnecessary retries
    exportvideo(goalbitrate, 1)