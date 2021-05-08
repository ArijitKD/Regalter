'''
Regalter: A simple utility for changing the registered owner and
registered organization names without messing with Windows registry.
This source code is for the 64-bit version of Regalter, created
exclusively for running on 64-bit Windows.

This file is a part of Regalter.

Copyright (C) 2021 Arijit Kumar Das (Github: @ArijitKD)

Regalter is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Regalter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Regalter.  If not, see <https://www.gnu.org/licenses/>.
'''

# This is the setup file which builds the executable for Regalter.
# Invoke this script as "python setup.py build" (without quotes)
# in the directory of regalter using a terminal. This setup script
# must be in the same directory as the other source files in this
# repository.

import sys
from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but it might need find tuning
build_exe_options = {"packages": ["tkinter", "ctypes", "os", "sys"], "include_files": ["assets\\"]}

setup  (name = "Regalter (64-bit)",
        target_name = "regalter_x64",
        copyright = "Copyright (c) 2021 Arijit Kumar Das.",
        description = "Regalter: A simple utility for changing the registered owner and registered organization names without messing with Windows registry.",
        options = {"build_exe": build_exe_options},
        executables = [Executable(script="main.py", base="Win32GUI",
                                  icon="assets\\icon.ico")])
