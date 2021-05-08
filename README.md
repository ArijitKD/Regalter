# regalter-utility

Regalter: A simple utility for changing the registered owner and registered organization names without messing with Windows registry.

# Description
The recent releases of Windows 10 does not allow the user to enter the user and organization names during installation. Instead it
asks the user to sign in with his/her Microsoft account. The user and organization names are extracted from the user's Microsoft
account information. However, if the user skips signing in to his/her Microsoft account then the organization name is not written
to the Windows Registry. That is when you need a simple tool like Regalter. Again, when the user wishes to transfer his/her Windows
PC's ownership to someone else and he/she wishes to change the registered owner and organization names, Regalter makes the work easy
for the user.

# Notes
This source code available here is for the 64-bit version of Regalter, created exclusively for running on 64-bit Windows. I will be 
uploading the code for the 32-bit version very soon, with some minor changes to the 64-bit source file (regalter.py). This code has
only been tested on Windows 7 and Windows 10, but it should work on the previous versions of Windows too (although I'm not sure about
the previous ones), just informing this in the highly unlikely event someone might be interested in rigorously test out my code's
compatibility. Please note that you may need to install some of the modules used first before you run the program. You can install
them through pip, using the command: pip install <module_name> through a terminal. You also must have Python 3.x.x installed on your
system.

# Copyright notice
Here is the notice which has been included with all the source code files:

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
along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Contact
For any suggestions or for reporting bugs, please send an e-mail to arijitkdgit.official@gmail.com.
