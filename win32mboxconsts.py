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

# This script defines some constants related to the win32 MessageBox functions.
# These constants specify how each win32 messagebox should behave. For more details
# about these, refer to the link assigned as the value of DESCRIPTION_LINK below.

DESCRIPTION_LINK = "docs.microsoft.com/en-gb/windows/win32/api/winuser/nf-winuser-messagebox?redirectedfrom=MSDN"

print ("\nModule win32mboxconsts")
print ("Refer to", DESCRIPTION_LINK, "for a complete description of the constants defined here.\n")

# Buttons
MB_ABORTRETRYIGNORE = 0x00000002
MB_CANCELTRYCONTINUE = 0x00000006
MB_HELP = 0x00004000
MB_OK = 0x00000000
MB_OKCANCEL = 0x00000001
MB_RETRYCANCEL = 0x00000005
MB_YESNO = 0x00000004
MB_YESNOCANCEL = 0x00000003

# Icons
MB_ICONEXCLAMATION = 0x00000030
MB_ICONWARNING = 0x00000030
MB_ICONINFORMATION = 0x00000040
MB_ICONASTERISK = 0x00000040
MB_ICONQUESTION = 0x00000020
MB_ICONSTOP = 0x00000010
MB_ICONERROR = 0x00000010
MB_ICONHAND = 0x00000010

# Default buttons
MB_DEFBUTTON1 = 0x00000000
MB_DEFBUTTON2 = 0x00000100
MB_DEFBUTTON3 = 0x00000200
MB_DEFBUTTON4 = 0x00000300

# Modality
MB_APPLMODAL = 0x00000000
MB_SYSTEMMODAL = 0x00001000
MB_TASKMODAL = 0x00002000

# Other options
MB_DEFAULT_DESKTOP_ONLY = 0x00020000
MB_RIGHT = 0x00080000
MB_RTLREADING = 0x00100000
MB_SETFOREGROUND = 0x00010000
MB_TOPMOST = 0x00040000
MB_SERVICE_NOTIFICATION = 0x00200000

# Return values
IDABORT = 3
IDCANCEL = 2
IDCONTINUE = 11
IDIGNORE = 5
IDNO = 7
IDOK = 1
IDRETRY = 4
IDTRYAGAIN = 10
IDYES = 6
