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

import ctypes, sys, win32mboxconsts as mboxconst, tkinter as tk, winreg
from time import sleep
import regalter as rg

APP_NAME = rg.APP_NAME

# Now to be able to make changes to the Registry, Regalter must be run with administrative previleges. The check
# below ensures that the user starting Regalter is an administrator.

if (not ctypes.windll.shell32.IsUserAnAdmin()):
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

else:
    # Now we will try to extract the values of RegisteredOwner and RegisteredOrganization from the Windows Registry.
    # The required values are under HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\.

    regkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion',
                            0, winreg.KEY_ALL_ACCESS) # Opening the required Registry key.
    
    # Sometimes, from my personal experience, I've seen that either or both of the values (RegisteredOwner and
    # RegisteredOrganization) are missing from the Registry, especially in the recent releases of Windows 10.
    # This is because Windows 10 doesn't ask for owner and organization unlike its predecessors and previous
    # releases. These infomation is gathered from the user's Microsoft account instead. In case a user doesn't
    # have a Microsoft account yet or chooses to skip signing in to his/her MS account while installing Windows 10,
    # that is when the either/both of the values may be missing. The code below will ensure that the program
    # doesn't crash if the values are missing.

    try:
       Initial_RegisteredOwner = winreg.QueryValueEx(regkey, "RegisteredOwner")[0] # QueryValueEx() returns a tuple whose first
                                                                                   # element is the required value.
                                                                 
    # If the RegisteredOwner value is not found then Python will raise FileNotFoundError.
    except FileNotFoundError:
        print ("Warning: Missing RegisteredOwner value. Creating it.") # Just to notify that RegisteredOwner is missing
                                                                       # and that it will be created.

        winreg.SetValueEx(regkey, 'RegisteredOwner', 0, winreg.REG_SZ, 'user name') # 'user name' is the value which
                                                                                # is shown by defaultin winver.exe
                                                                                # when the RegisteredOwner value
                                                                                # is missing from the Registry.
        Initial_RegisteredOwner = winreg.QueryValueEx(regkey, "RegisteredOwner")[0]

    try:
        Initial_RegisteredOrganization = winreg.QueryValueEx(regkey, "RegisteredOrganization")[0]
    except FileNotFoundError:
        print ("Warning: Missing RegisteredOrganization value. Creating it.") # Just to notify that RegisteredOrganization is missing
                                                                              # and that it will be created.
                                                                          
        winreg.SetValueEx(regkey, 'RegisteredOrganization', 0, winreg.REG_SZ, 'org name') # 'org name' is the value which
                                                                                          # is shown by default in winver.exe 
                                                                                          # when the RegisteredOrganization
                                                                                          # value is missing from the Registry.
        Initial_RegisteredOrganization = winreg.QueryValueEx(regkey, "RegisteredOrganization")[0]
    winreg.CloseKey(regkey) # Closing the Registry key

    # Now we will try to extract the values of RegisteredOwner and RegisteredOrganization for 32-bit programs.
    # The required values are under HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows NT\CurrentVersion\.

    regkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Microsoft\Windows NT\CurrentVersion',
                            0, winreg.KEY_ALL_ACCESS) # Opening the required Registry key.

    try:
       Initial_RegisteredOwner_x86 = winreg.QueryValueEx(regkey, "RegisteredOwner")[0] # QueryValueEx() returns a tuple whose first
                                                                                       # element is the required value.
                                                                 
    # If the RegisteredOwner value is not found then Python will raise FileNotFoundError.
    except FileNotFoundError:
       print ("Warning: Missing RegisteredOwner value. Creating it.") # Just to notify that RegisteredOwner is missing
                                                                      # and that it will be created.

       winreg.SetValueEx(regkey, 'RegisteredOwner', 0, winreg.REG_SZ, 'user name') # 'user name' is the value which
                                                                                   # is shown by defaultin winver.exe
                                                                                   # when the RegisteredOwner value
                                                                                   # is missing from the Registry.
       Initial_RegisteredOwner_x86 = winreg.QueryValueEx(regkey, "RegisteredOwner")[0]

    try:
       Initial_RegisteredOrganization_x86 = winreg.QueryValueEx(regkey, "RegisteredOrganization")[0]
    except FileNotFoundError:
       print ("Warning: Missing RegisteredOrganization value. Creating it.") # Just to notify that RegisteredOrganization is missing
                                                                             # and that it will be created.
                                                                          
       winreg.SetValueEx(regkey, 'RegisteredOrganization', 0, winreg.REG_SZ, 'org name') # 'org name' is the value which
                                                                                         # is shown by default in winver.exe 
                                                                                         # when the RegisteredOrganization
                                                                                         # value is missing from the Registry.
       Initial_RegisteredOrganization_x86 = winreg.QueryValueEx(regkey, "RegisteredOrganization")[0]
    winreg.CloseKey(regkey) # Closing the Registry key

    
    # Initalize Regalter window and create an object of Regalter class
    gui = rg.Regalter(Initial_RegisteredOwner = Initial_RegisteredOwner,
                      Initial_RegisteredOrganization = Initial_RegisteredOrganization,
                      Initial_RegisteredOwner_x86 = Initial_RegisteredOwner_x86,
                      Initial_RegisteredOrganization_x86 = Initial_RegisteredOrganization_x86)

    gui.root_window.focus_force()
    gui.root_window.lift()

    # We will not use tkinter's mainloop() function as it simply blocks program execution instead of iterating it.
    # The while loop below would serve as the mainloop of the program.
    while (1):
        try:       
           #gui.force_center_window() # Force the window to stay at the center of the screen
            
           gui.update_x86_entries()
            
           gui.update_update_names_button_state() # Update the state of the Update Names button
            
           gui.root_window.update() # Force tkinter to apply the above updates

           sleep(0.01) # This would prevent high CPU usage because of the main loop

        except KeyboardInterrupt: # The program must not be interrupted
           print ("Warning: KeyboardInterrupt has been raised. Execution will continue, however.")
           continue

        # When the root window has been destroyed but this while loop is still running, tkinter.TclError will be
        # raised in the try block. The except block below will ensure that the program exits safely.
        except tk.TclError:
           print ("Closed "+APP_NAME[0:APP_NAME.index(" ")]+" without any errors.")
           raise SystemExit
