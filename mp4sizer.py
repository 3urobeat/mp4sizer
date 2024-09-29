'''
File: mp4sizer.py
Project: mp4sizer
Created Date: 2021-01-29 22:27:00
Author: 3urobeat

Last Modified: 2024-09-29 13:26:14
Modified By: 3urobeat

Copyright (c) 2021 - 2024 3urobeat <https://github.com/3urobeat>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
'''


#!/usr/bin/python3

# Imports
import os
import sys
import moviepy
from moviepy.video.io.VideoFileClip import VideoFileClip
from colorama import just_fix_windows_console


# Config
version = "1.2"
folder = "./files/"
out_folder = "./compressed/"
arguments = sys.argv


# Ask colorama to fix colors if on Windows because it doesn't work otherwise for some stupid reason (I hate Windows)
if sys.platform == "win32":
    just_fix_windows_console()


# Dict to quickly get color codes
colors = { "reset": "\x1b[0m", "red": "\x1b[31m", "cyan": "\x1b[36m", "green": "\x1b[32m" }


# Entry point
print(f"{colors['cyan']}mp4sizer{colors['reset']} by 3urobeat v{version} powered by moviepy & ffmpeg")


# Helper function to keep terminal window open on Windows when exiting so that the user has a chance to read any error messages
def sysExit():
    if sys.platform == "win32":
        print("\nPress any key to exit...")
        input()

    sys.exit()


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
    print("\nPlease provide a target file size in MB as number to start and other optional arguments if you wish. Type help to see all options:")
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
        print(f"{colors['red']}Please provide a target filesize in Megabytes as the first argument!{colors['reset']}")
        sysExit()


# Remove the first argument if it is the file name
if "mp4sizer" in arguments[0]: arguments.pop(0)


# Check if user only asked for help menu
if "--help" in arguments or "-h" in arguments:
    print("")
    printHelp()
    sysExit()


# Check if targetsize is a valid number
try:
    targetsize = float(arguments[0])
except:
    print(f"{colors['red']}Your targetsize argument doesn't seem to be a valid number!{colors['reset']}")
    sysExit() # stop here


# Check if user set a custom amount of retries
if "--retries" in arguments: 
    maxretries = int(arguments[arguments.index("--retries") + 1])
else: 
    maxretries = 5


# Define the export part as a function to allow for recursion
def exportvideo(goalbitrate, iteration, difference):
    print("") # Empty line time

    if iteration > maxretries: # abort after maxretries tries to not cause an endless loop
        if "--retries" in arguments:
            print(f"{colors['red']}Ignoring retry to not exceed the specified amount of {maxretries} max retry attempt(s).{colors['reset']}")
        else:
            print(f"{colors['red']}I wasn't able to reach the target file size in {maxretries} attempts. Please try a higher target size.\nAborting to avoid an endless loop...{colors['reset']}")
        return

    try:
        # Export video with the calculated goalbitrate into the compressed folder and change fps if user wishes
        newfps = None
        if "--fps" in arguments:
            newfps = int(arguments[arguments.index("--fps") + 1])
            print(f"{colors['cyan']}Changing the framerate from {origclip.fps} to {newfps}...{colors['reset']}")

        # Compress file
        origclip.write_videofile('./compressed/' + file, bitrate=f"{goalbitrate * 1000}k", preset="medium", fps=newfps)

        print("") # Empty line time (again)

        # Get new size to determine how close we got to our target size
        newsize = os.path.getsize('./compressed/' + file) / 1000000 # in MB

        # Calculate difference of new size to size we want to reach
        difference = newsize / targetsize

        printDiagnostics(f"Difference of newsize to targetsize is {difference}. Accepting diff if between 0.9 & 1.0")

        # Either retry with changed bitrate or exit if are close enough to our target size
        if difference > 0.925 and difference < 1: # Check if we are within tolerance
            print(f"'{file}' {colors['green']}was successfully compressed{colors['reset']} from {origsize} MB to {newsize} MB in {iteration} try/tries.")

        elif "--no-retry" in arguments: # Check if we should not retry
            print(f"'{file}' {colors['green']}was compressed{colors['reset']} from {origsize} MB to {newsize} MB. No retries will be made as '--no-retry' flag is set.")

        else: # Retry
            print(f"'{file}' is {newsize} MB and didn't reach {targetsize} in try {iteration}.\n{colors['cyan']}Trying again with a slightly changed bitrate...{colors['reset']}")

            # Manipulate bitrate based on difference
            goalbitrate += (8 * (targetsize - newsize) / origclip.duration) # Calculate bitrate of difference between old and new size and subtract it from goalbitrate
            goalbitrate *= 0.975                                            # Subtract 2.5% for good measures to maybe avoid unnecessary retries

            # Check if goalbitrate is negative and abort as we won't be able to reach the targetsize for this file
            if goalbitrate < 0:
                print(f"'{file}' {colors['red']}is unable to reach {colors['reset']}{targetsize} MB. {colors['red']}Please try again with a higher target file size.{colors['reset']}")
                return

            printDiagnostics(f"Calculated bitrate of {goalbitrate} for try {iteration + 1}...")

            # Run again with modified bitrate
            exportvideo(goalbitrate, iteration + 1, difference)

    except:
        print(f"{colors['red']}Couldn't export {colors['reset']}'{file}'{colors['red']}. Please try again.{colors['reset']}")


# Iterate over all files in files folder
for file in os.listdir(folder):
    print("") # print empty line

    if "mp4" not in file: # check if file is not a valid video file
        if file != ".input" and file != ".output": print(f"{colors['red']}File {colors['reset']}'{file}' {colors['red']}is not a mp4! Skipping...{colors['reset']}")
        continue

    # Get a few values to be able to calculate the bitrate we would like to reach
    origsize = os.path.getsize('./files/' + file) / 1000000 # in MB
    origclip = VideoFileClip('./files/' + file)

    # Resize if the user wishes
    if "--res" in arguments:
        newres = arguments[arguments.index("--res") + 1].split("x")
        print(f"{colors['cyan']}Resizing the clip from{colors['reset']} {origclip.size[0]}x{origclip.size[1]} to {newres[0]}x{newres[1]}")

        # RESIZE!
        import moviepy.video.fx.all as vfx
        origclip = vfx.resize(origclip, (newres[0], newres[1])) # pylint: disable=no-member

    # Calculate goalbitrate and export
    goalbitrate = 8 * targetsize / origclip.duration # Estimated bitrate we need to use to reach the provided filesize
    goalbitrate *= 0.975                             # Subtract 2.5% for good measures to maybe avoid unnecessary retries

    printDiagnostics(f"Calculated bitrate of {goalbitrate} for {origsize} MB file with length of {origclip.duration} seconds to reach a size of {targetsize} MB")

    exportvideo(goalbitrate, 1, 0)