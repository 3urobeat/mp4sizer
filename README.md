# mp4sizer
Automatically let a python script compress a folder full of mp4 files for you.  
Just provide a file size in MB which your video files should reach and the script will take care of the rest.  
It is also possible to easily change the framerate and resolution of all clips.  

**Use case example:** Get a bunch of video clips below 8 MB to be able to send them on Discord.  

## Download & Install:  
You can either use a build (easy) or use it from source (a bit more complicated).  

### Use a build:  
[Download the latest release](https://github.com/HerrEurobeat/mp4sizer/releases) for your platform and extract the folder.  
> On Linux you have to run the executable from/in a Terminal.  

### Use from Source:  
Make sure to have [Python 3](https://www.python.org/downloads/) (`Windows x86-64 executeable installer`) installed.  
If you are using Linux then you should be able to download python3 from your distribution's packet manager.  

[Download this script](https://github.com/HerrEurobeat/mp4sizer/archive/master.zip) and extract the folder.  
Open up a terminal in the new folder and install `moviepy` using pip: `python3 -m pip install moviepy`.  

## Usage:  
Put all your mp4 files to compress into the `files` folder.  
Open the script and input the file size in MB you would like your clips to have.  
To see more options type `help`. This will show how you can also change the framerate and resolution of your files for example.  

The script will now try to get all your clips as close to the target file size you chose and output them into the `compressed` folder.  
> Disclaimer: If your output files look bad afterwards please consider cutting them shorter or raising your target file size.  

### Additional information:  
`moviepy` does seem to only support CPU Encoding (at least for me on Linux) so bigger files might take longer.  