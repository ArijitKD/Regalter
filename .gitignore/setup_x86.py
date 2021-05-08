import sys
from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["tkinter", "ctypes", "os", "sys"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

script = "regalter_x86.py"

## The image and sound files are added manually into the zip file
## A fix for this would be released

setup(  name = "Regalter (32-bit)",
	#icon = "assets\\icon.ico",
        description = "Regalter: GUI modifier for Windows owner and organization (32-bit)",
        options = {"build_exe": build_exe_options},
        executables = [Executable(script=script, base=base,
                                  icon="assets\\icon.ico"
                                  )]
)
