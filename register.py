# add ./Wallpaper-Changer-py.py to system startup

import os
import sys


file_path_rel = "Wallpaper-Changer-py.py"
file_path_abs = os.path.abspath(file_path_rel)

operating_system = os.name

if operating_system == "nt":
    # copy file to C:/Python39/Scripts
    
    if not os.path.exists("C:/Python39/Scripts"):
        os.mkdir("C:/Python39/Scripts")
        print("path created")
    else:
        print("path exists")
    
    if os.path.exists("C:/Python39/Scripts/Wallpaper-Changer-py.py"):
        print("file exists")
    else:
        os.system(f"copy {file_path_rel} C:\Python39\Scripts")
        print("copied file")
    
    
    # add to startup
    
    username = os.getlogin()
    
    startup_path = f'"C:/Users/{username}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"'

    
    bat_path = os.path.abspath("Wallpaper-Changer.bat")
    
    if os.path.exists(startup_path + "/Wallpaper-Changer.bat"):
        print("bat file exists")
    else:
        os.system(f"copy Wallpaper-Changer.bat {startup_path}")
        print("copied bat file")