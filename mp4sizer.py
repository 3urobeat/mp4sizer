#!/usr/bin/python3

# Imports
import os
import sys
import moviepy
from moviepy.video.io.VideoFileClip import VideoFileClip


# Config
version = "1.1"
folder = "./files/"
out_folder = "./compressed/"
arguments = sys.argv


# Entry point
print(f"mp4sizer by 3urobeat v{version} powered by moviepy")


# Helper func to print diagnostic messages
def printDiagnostics(msg):
    if "--diagnostics" in arguments:
        print(msg)


# Helper function to print help menu
def printHelp():
    print("    --fps Number       | Changes the fps of the output clip.")
    print("    --res WidthxHeight | Changes the resolution of the output clip. Seperate Width and Height with a 'x'. Example: 1920x1080")
    print("    --retries Number   | Changes the amount of max retries. Default: 5")
    print("    --no-retry         | The script won't retry to compress further even if the first run didn't reach the target size.")
    print("    --diagnostics      | Shows what the script is calculating.\n")


# Check if user did not provide an argument and ask for input
if len(arguments) < 2:
    print("\nPlease provide a target file size in MB as number to start\n(and other optional arguments if you wish. Type help to see all options.):")
    userinput = input().split(" ") # Wait for new input

    # Check if user requested help menu
    if "help" in userinput:
        print("\nPlease provide a file size in MB as number as the first argument.\nOptional arguments:")
        printHelp()
        userinput = input().split(" ") # Wait for new input

    # Push all new arguments
    for e in userinput:
        arguments.append(e)

    if len(arguments) < 2:
        print("Please provide a target filesize in Megabytes as the first argument!")
        sys.exit()


# Remove the first argument if it is the file name
if "mp4sizer" in arguments[0]: arguments.pop(0)


# Check if user only asked for help menu
if "--help" in arguments or "-h" in arguments:
    print("")
    printHelp()
    sys.exit()


# Check if targetsize is a valid number
try:
    targetsize = float(arguments[0])
except:
    print("Your targetsize argument doesn't seem to be a valid number.")
    sys.exit() # stop here


# Check if user set a custom amount of retries
if "--retries" in arguments: 
    maxretries = int(arguments[arguments.index("--fps") + 1])
else: 
    maxretries = 5


# Define the export part as a function to be able to call it again if we didn't reach our targetsize on the first run
def exportvideo(goalbitrate, iteration, difference):
    if iteration > 5: # abort after 5 tries to not cause an endless loop
        print("I wasn't able to reach the target file size in 5 attempts. Please try a higher target size.\nAborting to not cause an endless loop...")
        return

    try:
        # Export video with the calculated goalbitrate into the compressed folder and change fps if user wishes
        newfps = None
        if "--fps" in arguments:
            newfps = int(arguments[arguments.index("--fps") + 1])
            print(f"Changing the framerate from {origclip.fps} to {newfps}...")


        # Compress file
        origclip.write_videofile('./compressed/' + file, bitrate=f"{goalbitrate * 1000}k", preset="fast", fps=newfps)


        # Get new size to determine how close we got to our target size
        newsize = os.path.getsize('./compressed/' + file) / 1000000 # in MB


        # Calculate difference of new size to target size and adjust bitrate accordingly
        


        # Calculate difference of new size to size we want to reach
        difference = newsize / targetsize


        # Either retry with changed bitrate or exit if are close enough to our target size
        if difference > 0.9 and difference < 0.99999: # tolerance
            print(f"\n'{file}' was successfully compressed from {origsize} MB to {newsize} MB in {iteration} try/tries.")
        elif "--no-retry" in arguments:
            print(f"\n'{file}' was compressed from {origsize} MB to {newsize} MB. No retries will be made as '--no-retry' flag is set.")
        else:
            print(f"\n'{file}' is {newsize} MB and didn't reach {targetsize} in try {iteration}.\nTrying again with a slightly changed bitrate...")
            exportvideo(goalbitrate, iteration + 1, difference) # check again

    except:
        print(f"Couldn't export '{file}'. Please try again.")


# Iterate over all files in files folder
for file in os.listdir(folder):
    print("") # print empty line

    if "mp4" not in file: # check if file is not a valid video file
        if file != ".input" and file != ".output": print(f"File '{file}' is not a mp4! Skipping...")
        continue

    # Get a few values to be able to calculate the bitrate we would like to reach
    origsize = os.path.getsize('./files/' + file) / 1000000 # in MB
    origclip = VideoFileClip('./files/' + file)

    # Resize if the user wishes
    if "--res" in arguments:
        newres = arguments[arguments.index("--res") + 1].split("x")
        print(f"Resizing the clip from {origclip.size[0]}x{origclip.size[1]} to {newres[0]}x{newres[1]}")

        # RESIZE!
        import moviepy.video.fx.all as vfx
        origclip = vfx.resize(origclip, (newres[0], newres[1])) # pylint: disable=no-member

    # Calculate goalbitrate and export
    goalbitrate = 8 * targetsize / origclip.duration # estimated bitrate we need to have to reach the provided filesize
    goalbitrate = goalbitrate - 0.15 # subtract a little bit for good measures to maybe avoid unnecessary retries

    printDiagnostics(f"Calculated bitrate of {goalbitrate} for current clip with length of {origclip.duration} seconds to reach a size of {targetsize} MB\n")

    exportvideo(goalbitrate, 1, 0)