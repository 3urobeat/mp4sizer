# mp4sizer
Automatically let a python script compress a folder full of mp4 files for you.  
Just provide a file size in MB which your video files should reach and the script will take care of the rest.  
It is also possible to easily change the framerate and resolution of all clips.  

**Use case example:** Get a bunch of video clips below 8 MB to be able to send them on Discord.  

&nbsp;

## Download & Install:  
You can either use a build (easy) or use it from source (a bit more complicated).  

### Use a build:  
[Download the latest release](https://github.com/3urobeat/mp4sizer/releases) for your platform and extract the folder.  
> On Linux you have to run the executable from/in a Terminal.  

### Use from Source:  
Make sure to have [Python 3](https://www.python.org/downloads/) (`Windows x86-64 executeable installer`) installed.  
If you are using Linux then you should be able to download python3 from your distribution's packet manager.  

[Download this script](https://github.com/3urobeat/mp4sizer/archive/master.zip) and extract the folder.  
Open up a terminal in the new folder and install the dependencies using pip, preferably inside a python virtual environment:  
```bash
python -m venv ./venv
# On Linux
./venv/bin/pip install moviepy opencv-python colorama
# On Windows
.\venv\Scripts\pip.exe install moviepy opencv-python colorama
```

&nbsp;

## Usage:  
Put all your mp4 files to compress into the `files` folder.  
> Note: Please avoid putting clips into the folder that are already below your target size as they can get bigger after compressing.  
  
Start the script and input the file size in MB you would like your clips to have.  
To see more options type `help`. This will show how you can also change the framerate and resolution of your files for example.  

When running the binary from a terminal (which you do on Linux), the syntax looks like this:  
`./mp4sizer <size_in_MB> [options]`, e.g. `./mp4sizer 8 --res 1920x1080`  
When not running the binary but the source file, make sure to use the venv python binary from the previous step instead:  
`./venv/bin/python mp4sizer.py <size_in_MB> [options]`, e.g. `./venv/bin/python mp4sizer.py 8 --res 1920x1080`

The script will now try to get all your clips as close to the target file size you chose and output them into the `compressed` folder.  
> Disclaimer: If your output files look bad afterwards please consider cutting them shorter or raising your target file size.  

&nbsp;

## Additional information:  
`moviepy` does seem to only support CPU Encoding (at least for me on Linux) so bigger files might take longer.  
