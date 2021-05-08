'''
Regalter: A simple utility for changing the registered owner and
registered organization names without messing with Windows registry.
This source code is for the 64-bit version of Regalter, created
exclusively for running on 64-bit Windows.

This program is a part of Regalter.

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

# Importing required modules
import tkinter as tk, tkinter.ttk as ttk, wmi, winreg, sys, ctypes
from time import sleep
from os import startfile, path, environ
from platform import architecture
import win32mboxconsts as mboxconst # This module contain all the constants related to messagebox functions
                                    # in Windows



mbox = ctypes.windll.user32.MessageBoxW # It's really a pain to write a long function name again and again, so we will
                                            # store it in a variable with a short name.                                        
# Constant(s)
APP_NAME = "Regalter (64-bit)" # The default title for Regalter that
                               # will appear on the title bar.
WINDIR = environ['windir']


    
class Regalter:


    '''[INITIALIZATION]'''
    def __init__(self, Initial_RegisteredOwner, Initial_RegisteredOrganization, Initial_RegisteredOwner_x86, Initial_RegisteredOrganization_x86):

        self.change_btn_is_disabled = False
        self.org_entry_x86_is_disabled = True
        self.owner_entry_x86_is_disabled = True
        self.show_change_info = True

        self.Initial_RegisteredOwner = Initial_RegisteredOwner
        self.Initial_RegisteredOrganization = Initial_RegisteredOrganization
        self.Initial_RegisteredOwner_x86 = Initial_RegisteredOwner_x86
        self.Initial_RegisteredOrganization_x86 = Initial_RegisteredOrganization_x86
        
        # Creating the root window
        self.root_window = tk.Tk()
        #self.root_window.lift()
        #self.root_window.focus_set()
        # Screen dimensions
        self.screen_width = self.root_window.winfo_screenwidth()
        self.screen_height = self.root_window.winfo_screenheight()

        # Fixed dimensions of the root window (640x480)
        self.root_winwidth = 640
        self.root_winheight = 480

        # The code fragment below will position the root window at the centre of the screen
        center_x = int((self.screen_width/2) - (self.root_winwidth/2))
        center_y = int((self.screen_height/2) - (self.root_winheight/2))
        self.root_window.geometry(str(self.root_winwidth)+"x"+str(self.root_winheight)+"+"+str(center_x)+"+"+str(center_y))

        # Since the root window has only a few widgets, so it would be better if we disable the maximization
        # of the window. Also, it won't appear great when maximized on displays with higher resolutions.
        self.root_window.resizable(0,0)

        # Setting the default window title
        self.root_window.title(APP_NAME)

        # When the window-close event is triggered, function close_root_window(self) is executed
        self.root_window.protocol("WM_DELETE_WINDOW", self.close_root_window)

        # Setting the window icon. If the check below fails then the icon must have been moved or renamed, and in that case
        # the icon will be loaded from tkinter's default directory.
        if (path.isfile("assets\\icon.png")):
            icon_ob = tk.PhotoImage(file = "assets\\icon.png")
            self.root_window.iconphoto(False, icon_ob)

        # The code fragment below is no longer required
        '''
        # We are storing the co-ordinates of the root window's position when it is created in the two variables below.
        # This will be used later in function fto prevent the user from re-positioning the window on the screen.
        self.fixed_rootwinpos_x = self.root_window.winfo_x()
        self.fixed_rootwinpos_y = self.root_window.winfo_y()
        '''
        
        # If the shield icon (which appears beside tasklinks/buttons/context menu options in Windows for tasks which requires administrative
        # privileges) has been moved or renamed, then the program may crash. The check below will ensure that doesn't happen.
        if (path.isfile('assets\\uac_16x16.png')):
            icon = tk.PhotoImage(file = 'assets\\uac_16x16.png')
            self.change_btn=ttk.Button(self.root_window, text = 'Change values', command = self.change_button, image = icon, compound = 'left', cursor='hand2')
            self.update_btn=ttk.Button(self.root_window, text = 'Update Names', command = self.update_names_button, image = icon, compound = 'left', state = 'disabled', cursor='arrow')
            self.change_btn.image = icon

        # If the shield icon (uac_16x16.png) is not found then a warning message will be printed to the console and the buttons will be created
        # without the shield icon.
        else:
            print ("Warning: File assets\\uac_16x16.png is missing. Skipping addition of image to button.")
            self.change_btn=ttk.Button(self.root_window, text = 'Change values', command = self.change_button, cursor='hand2')
            self.update_btn=ttk.Button(self.root_window, text = 'Update Names', command = self.update_names_button, state = 'disabled', cursor='arrow')

        self.about_btn=ttk.Button(self.root_window, text = 'About Regalter', command = self.about_button, cursor='hand2') # About button


        '''[START: x64]'''
        # Creating the Launch winver.exe button with appropriate attributes
        self.winver_button = ttk.Button(self.root_window, text="Launch winver.exe", command = self.launch_winver_button, cursor='hand2')
        
        self.owner_var=tk.StringVar() # This variable will keep a track of the string values entered in the entry for the RegisteredOwner
        self.org_var=tk.StringVar() # This variable will keep a track of the string values entered in the entry for the RegisteredOrganization

        self.owner_var.set(self.Initial_RegisteredOwner) # The initial value appearing in the RegisteredOwner entry will be the current value of
                                                    # RegisteredOwner from the Registry
                                                    
        self.org_var.set(self.Initial_RegisteredOrganization) # The initial value appearing in the RegisteredOrganization entry will be the current value of
                                                         # RegisteredOrganization from the Registry

        # The following two variables wil be required later in the function update_names_button(self) to modify the Registry values. They are being initialized
        # with the current values in the Registry so that the Update names button remains disabled.
        self.regowner = self.Initial_RegisteredOwner
        self.regorg = self.Initial_RegisteredOrganization

        # Creating the "Registered Owner" label with appropriate attributes
        self.owner_label = ttk.Label(self.root_window, text = 'Registered Owner', font=('segoe ui', 11, 'bold'))

        # Creating the "Registered Organization" label with appropriate attributes
        self.org_label = ttk.Label(self.root_window, text = 'Registered Organization', font = ('segoe ui', 11,'bold'))

        # Creating the entry for RegisteredOwner with appropriate attributes. The entry will initially be disabled, but will be enabled once the user presses
        # the Change button
        self.owner_entry = ttk.Entry(self.root_window, textvariable = self.owner_var, font=('segoe ui', 11,'normal'), state='disabled', cursor='arrow')

        # Creating the entry for RegisteredOrganization with appropriate attributes. The entry will initially be disabled, but will be enabled once the user
        # presses the Change button
        self.org_entry=ttk.Entry(self.root_window, textvariable = self.org_var, font = ('segoe ui', 11,'normal'), state='disabled', cursor='arrow')
        '''[END: x64]'''


        '''[START: x86]'''
        # Creating the Launch winver.exe button with appropriate attributes
        self.winver_button_x86 = ttk.Button(self.root_window, text="Launch winver.exe (x86)", command = self.launch_winver_button_x86, cursor='hand2')
        
        self.owner_var_x86=tk.StringVar() # This variable will keep a track of the string values entered in the entry for the RegisteredOwner
        self.org_var_x86=tk.StringVar() # This variable will keep a track of the string values entered in the entry for the RegisteredOrganization

        self.owner_var_x86.set(self.Initial_RegisteredOwner_x86) # The initial value appearing in the RegisteredOwner entry will be the current value of
                                                    # RegisteredOwner from the Registry
                                                    
        self.org_var_x86.set(self.Initial_RegisteredOrganization_x86) # The initial value appearing in the RegisteredOrganization entry will be the current value of
                                                         # RegisteredOrganization from the Registry

        # The following two variables wil be required later in the function update_names_button(self) to modify the Registry values. They are being initialized
        # with the current values in the Registry so that the Update names button remains disabled.
        self.regowner_x86 = self.Initial_RegisteredOwner_x86
        self.regorg_x86 = self.Initial_RegisteredOrganization_x86

        # Creating the "Registered Owner" label with appropriate attributes
        self.owner_label_x86 = ttk.Label(self.root_window, text = 'Registered Owner(x86)', font=('segoe ui', 11, 'bold'))

        # Creating the "Registered Organization" label with appropriate attributes
        self.org_label_x86 = ttk.Label(self.root_window, text = 'Registered\nOrganization(x86)', font = ('segoe ui', 11,'bold'))

        # Creating the entry for RegisteredOwner with appropriate attributes. The entry will initially be disabled, but will be enabled once the user presses
        # the Change button
        self.owner_entry_x86 = ttk.Entry(self.root_window, textvariable = self.owner_var_x86, font=('segoe ui', 11,'normal'), state='disabled', cursor='arrow')

        # Creating the entry for RegisteredOrganization with appropriate attributes. The entry will initially be disabled, but will be enabled once the user
        # presses the Change button
        self.org_entry_x86 = ttk.Entry(self.root_window, textvariable = self.org_var_x86, font = ('segoe ui', 11,'normal'), state='disabled', cursor='arrow')
        '''[END: x86]'''



        # Placing all the buttons, labels and entries at appropriate positions on the window
        '''[WIDGETS_x64]'''
        self.winver_button.place(x=10, y=20, width=150)    
        self.owner_label.place(x=10, y=60+30)
        self.owner_entry.place(x=200, y=60+30, width = 420)
        self.org_label.place(x=10, y=110+30)
        self.org_entry.place(x=200, y=110+30, width = 420)

        '''[WIDGETS_x86]'''
        self.winver_button_x86.place(x=170, y=20, width=150)    
        self.owner_label_x86.place(x=10, y=200+10)
        self.owner_entry_x86.place(x=200, y=200+10, width = 420)
        self.org_label_x86.place(x=10, y=250+10)
        self.org_entry_x86.place(x=200, y=260+10, width = 420)
        
        '''[WIDGETS_BOTH]'''
        self.change_btn.place(x=497, y=320+10, width = 125)
        self.update_btn.place(x=300, y=320+10, width = 125)
        self.about_btn.place(x=470, y=20, width = 150)



    '''[BUTTONS]'''
    def about_button(self):
        mbox(0,'''
Regalter (64-bit)
Version 1.0.0
Copyright (C) 2021 Arijit Kumar Das (Github: @ArijitKD)


Regalter: A simple utility for changing the registered owner and
registered organization names without messing with Windows registry.
Regalter (64-bit) is exclusively for running on 64-bit Windows.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

For any suggestions or for reporting bugs, please send an e-mail to
arijitkdgit.official@gmail.com.
''', "About Regalter",
                mboxconst.MB_OK | mboxconst.MB_TASKMODAL)
    # The function below gets executed whenever the Launch winver.exe button is pressed. This function starts
    # winver.exe if its not running, or restarts it if it was previously running.
    def launch_winver_button(self):
        
        self.winver_button.configure(state='disabled', cursor='arrow')
        
        # Tkinter does not update the state of the Launch winver.exe button even after the line above has executed.
        # The line below will force Tkinter to update the button's state
        self.root_window.update()

        # We will notify the user that the winver.exe will be launched if the OK button is pressed.
        # The check below will prompt the user if he/she wanted to launch winver.exe. If the Cancel button is pressed
        # then the if-block below will execute, and make the Launch winever.exe button active, and return from the
        # function launch_winver_button(self).
        if (mbox(0,
                "We will try to launch winver.exe. Please be patient. This will take a while.\n\nIf it takes a long time then manually start winver.exe using the following steps:\ni)   Open Command prompt\nii)  Type this: winver.exe && exit\niii) Press Enter/Return key",
                "Delay alert",
                mboxconst.MB_OKCANCEL | mboxconst.MB_ICONINFORMATION | mboxconst.MB_TASKMODAL) == mboxconst.IDCANCEL):
            self.winver_button.configure(state='normal', cursor='hand2') # Setting the original Launch winver.exe button attributes
            return

        # If the user clicks the OK button then code below will execute.
        self.root_window.title("Starting winver.exe. Please wait...") # The window title will notify the user what is
                                                                      # happening in the background      
        winver_proc_count = 0
        self.wmi_ob = wmi.WMI()
        wmi_ob = self.wmi_ob
        all_processes = wmi_ob.Win32_Process()

        # The code fragment commented out below is unoptimized, so has been discarded. The one following it is a
        # better approach
        '''
        for process in all_processes:
            if (process.name == 'winver.exe'):
                winver_proc_count+=1  
        if (winver_proc_count == 0):
            startfile('winver.exe')
        else:
            print("Found "+str(winver_proc_count)+" running instance(s) of winver.exe.")
            print ("Attempting to terminate all instances of winver.exe...",end=': ')
            for process in all_processes:
                if (process.name == 'winver.exe'):
                    process.Terminate()
            print ("PASS")
            print ("Restarting winver.exe...", end=": ")
            startfile('winver.exe')
            print ("PASS")
        '''
        
        for process in all_processes:
                
            # The check below will count how many running instances of winver.exe are there, and also terminate its
            # every running instance.
            if (process.name == 'winver.exe'):
                winver_proc_count+=1
                print ("Found a running instance of winver.exe. Attempting to terminate it...", end=": ")
                process.Terminate()
                print ("PASS")
                
        # If no running instances of winver.exe is found, then the if-block below will get executed and winver.exe
        # will be started. A success message will be printed to the console.
        if (winver_proc_count == 0):
            print ("Starting winver.exe...", end=": ")
            startfile('winver.exe')
            print ("PASS")

        # If one or more instances of winver.exe were found and terminated, in the else-block below, a single instance
        # of winver.exe is started again. A success message will be printed to the console.
        else:
            # Show how many instances of winver.exe were terminated
            print("\n"+str(winver_proc_count)+" running instance(s) of winver.exe were terminated successfully.")
            print ("Restarting winver.exe...", end=": ")
            startfile('winver.exe')
            print ("PASS")
            
        self.root_window.title(APP_NAME) # Setting the original window title
        self.winver_button.configure(state='normal', cursor='hand2') # Setting the original Launch winver.exe button attributes



    # The function below gets executed whenever the Launch winver.exe (x86) button is pressed. This function starts
    # winver.exe if its not running, or restarts it if it was previously running.
    def launch_winver_button_x86(self):
        
        self.winver_button_x86.configure(state='disabled', cursor='arrow')
        
        # Tkinter does not update the state of the Launch winver.exe (x86) button even after the line above has executed.
        # The line below will force Tkinter to update the button's state
        self.root_window.update()

        # We will notify the user that the winver.exe will be launched if the OK button is pressed.
        # The check below will prompt the user if he/she wanted to launch winver.exe (32-bit). If the Cancel button is pressed
        # then the if-block below will execute, and make the Launch winever.exe (x86) button active, and return from the
        # function launch_winver_button_x86(self).
        if (mbox(0,
                "We will try to launch 32-bit version of winver.exe. Please be patient. This will take a while.\n\nIf it takes a long time then manually start winver.exe using the following steps:\ni)   Open Command prompt\nii)  Type this: %windir%\SysWOW64\winver.exe && exit\niii) Press Enter/Return key",
                "Delay alert",
                mboxconst.MB_OKCANCEL | mboxconst.MB_ICONINFORMATION | mboxconst.MB_TASKMODAL) == mboxconst.IDCANCEL):
            self.winver_button_x86.configure(state='normal', cursor='hand2') # Setting the original Launch winver.exe (x86) button attributes
            return

        # If the user clicks the OK button then code below will execute.
        self.root_window.title("Starting winver.exe (x86). Please wait...") # The window title will notify the user what is
                                                                      # happening in the background      
        winver_proc_count = 0
        self.wmi_ob = wmi.WMI()
        wmi_ob = self.wmi_ob
        all_processes = wmi_ob.Win32_Process()
        
        for process in all_processes:
                
            # The check below will count how many running instances of winver.exe are there, and also terminate its
            # every running instance.
            if (process.name == 'winver.exe'):
                winver_proc_count+=1
                print ("Found a running instance of winver.exe. Attempting to terminate it...", end=": ")
                process.Terminate()
                print ("PASS")
                
        # If no running instances of winver.exe is found, then the if-block below will get executed and winver.exe
        # will be started. A success message will be printed to the console.
        if (winver_proc_count == 0):
            print ("Starting winver.exe (x86)...", end=": ")
            startfile(WINDIR+"\\SysWOW64\\winver.exe")
            print ("PASS")

        # If one or more instances of winver.exe were found and terminated, in the else-block below, a single instance
        # of winver.exe is started again. A success message will be printed to the console.
        else:
            # Show how many instances of winver.exe were terminated
            print("\n"+str(winver_proc_count)+" running instance(s) of winver.exe were terminated successfully.")
            print ("Restarting winver.exe (x86)...", end=": ")
            startfile(WINDIR+'\\SysWOW64\\winver.exe')
            print ("PASS")
            
        self.root_window.title(APP_NAME) # Setting the original window title
        self.winver_button_x86.configure(state='normal', cursor='hand2') # Setting the original Launch winver.exe (x86) button attributes


        
    # The function below is executed whenever the Change button is pressed. The RegisteredOwner and RegisteredOrganization
    # entry boxes, which were disabled before, will now be enabled. The Change button will be disabled.
    def change_button(self):
        self.owner_entry.configure(state='normal', cursor='ibeam')
        self.org_entry.configure(state='normal', cursor='ibeam')
        self.change_btn.configure(text = "Change x86 values", command = self.change_button_x86)
        self.change_btn.place_forget()
        self.change_btn.place(x=470, y=320, width = 150)



    def change_button_x86(self):
        if (mbox(0,
                "Are you sure you want to change the values of RegisteredOwner and RegisteredOrganization for 32-bit registry keys?\n\n"+
                "It is not recommended to have different values of RegisteredOwner and RegisteredOrganization for 64-bit and 32-bit registry keys. If you do so, "+
                "32-bit applications requiring these values will fail to get the correct results.\n\nIf you still wish to proceed with your changes, click OK.",
                "Confirm change",
                mboxconst.MB_OKCANCEL | mboxconst.MB_ICONWARNING | mboxconst.MB_DEFBUTTON2 | mboxconst.MB_TASKMODAL) == mboxconst.IDCANCEL):
            return
        else:
            self.owner_entry_x86.configure(state='normal', cursor='ibeam')
            self.org_entry_x86.configure(state='normal', cursor='ibeam')
            self.change_btn.configure(state = 'disabled', cursor='arrow')
            self.change_btn_is_disabled = True



    # The function below is executed whenever the Update Names button is pressed.
    def update_names_button(self):
        
        # Extracting the current string values from the corresponding entry boxes
        self.regowner = self.owner_var.get()
        self.regorg = self.org_var.get()
        self.regowner_x86 = self.owner_var_x86.get()
        self.regorg_x86 = self.org_var_x86.get()

        # Opening the Registry key HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion', 0, winreg.KEY_WRITE)

        # Writing the corresponding values to the Registry
        winreg.SetValueEx(key, "RegisteredOwner", 0, winreg.REG_SZ, self.regowner)
        winreg.SetValueEx(key, "RegisteredOrganization", 0, winreg.REG_SZ, self.regorg)
        
        #Closing the opened registry key
        winreg.CloseKey(key)


        # Opening the Registry key HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows NT\CurrentVersion\
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Microsoft\Windows NT\CurrentVersion', 0, winreg.KEY_WRITE)

        # Writing the corresponding values to the Registry
        winreg.SetValueEx(key, "RegisteredOwner", 0, winreg.REG_SZ, self.regowner_x86)
        winreg.SetValueEx(key, "RegisteredOrganization", 0, winreg.REG_SZ, self.regorg_x86)

        #Closing the opened registry key
        winreg.CloseKey(key)

        
        # Notifying the user about the update/changes made
        mbox(0,
                "Registered owner and registered organization names have been successfully changed. Click the \'Launch winver.exe\' or \'Launch winver.exe (x86)\' button to view the changes made.",
                "Update successful",
                mboxconst.MB_OK | mboxconst.MB_ICONINFORMATION | mboxconst.MB_TASKMODAL)
        



    '''[WM_DELETE_WINDOW]'''
    # The function below will be called when the window-closing event is triggered. This function attempts to close all
    # running instances of winver.exe which may make the screen cluttered up, or in case the user forgets to close
    # winver.exe after it has been opened (either by clicking on Launch winver.exe or by launching winver.exe manually
    # through the command-line), it will be closed automatically for the user.
    def close_root_window(self):
        
        '''
        if(mbox(0, "Are you sure you want to close Regalter?", "Confirm exit",
        mboxconst.MB_YESNO | mboxconst.MB_DEFBUTTON2 | mboxconst.MB_ICONEXCLAMATION | mboxconst.MB_TASKMODAL)
        == mboxconst.IDYES):
        '''
        # The above check is not so important and may be irritating for some
        
        self.root_window.title("Closing Regalter. Please wait...")
        winver_proc_count = 0
            
        # The try-except block implements an algorithm that speeds up the process of closing the root window
        # when the user tries to close Regalter. Technically, within the try block we assign wmi_ob the
        # reference to self.wmi_ob. Note that self.wmi_ob reference was created in the function launch_winver_button(self).
        # or launch_winver_button_x86(self). Now, if the function close_root_window(self) is executed before function
        # launch_winver_button(self) or launch_winver_button(self)_x86, Python will raise an AttributeError because
        # it will not be able to find the reference to the wmi.WMI() object, i.e, self.wmi_ob. This will cause the code
        # in the except block to be executed. The except block simply destroys the root window and returns from the function
        # close_root_window(self).
        try:
            wmi_ob = self.wmi_ob
            all_processes = wmi_ob.Win32_Process() # If self.wmi_ob has been declared (launch_winver_button(self)
                                                   # or launch_winver_button_x86(self) has beenexecuted) then get
                                                   # all the currently running processes.
        except AttributeError:
            self.root_window.destroy()
            return
        
        '''
        for process in all_processes:
                
            # The check below will count how many running instances of winver.exe are there.
            if (process.name == 'winver.exe'): 
                winver_proc_count+=1
            
        if (winver_proc_count != 0):
            print("Found "+str(winver_proc_count)+" running instance(s) of winver.exe.")
            print ("Attempting to terminate all instances of winver.exe...",end=': ')
            for process in all_processes:
                if (process.name == 'winver.exe'):
                    process.Terminate()
            print ("PASS")
        '''
        # The code fragment above is not a good implementation and may make the program unresponsive if there
        # are too many running processes. The implementation below would be better.
        
        for process in all_processes:
                
            # The check below will count how many running instances of winver.exe are there, and also terminate its
            # every running instance.
            if (process.name == 'winver.exe'):
                winver_proc_count+=1
                print ("Found a running instance of winver.exe. Attempting to terminate it...", end=": ")
                process.Terminate()
                print ("PASS")
                
        # Show how many instances of winver.exe were terminated
        if (winver_proc_count != 0):
            print("\n"+str(winver_proc_count)+" running instance(s) of winver.exe were terminated successfully.")

        # When everything has been done, destroy the root window finally
        self.root_window.destroy()



    '''[LOOP FUNCTIONS]'''
    # The function below, when placed inside a loop, will force the root window to appear at the center
    # of the screen whenever the user tries to change the window position (Maybe this is not required but
    # I personally like central windows very much 😅). 
    def force_center_window(self):
        # The code fragment below will position the root window at the centre of the screen
        center_x = int((self.screen_width/2) - (self.root_winwidth/2))
        center_y = int((self.screen_height/2) - (self.root_winheight/2))
        self.root_window.geometry(str(self.root_winwidth)+"x"+str(self.root_winheight)+"+"+str(center_x)+"+"+str(center_y))


        
    # The function below, when placed inside a loop, will update the current state of the Update names button
    # (enabled or disabled) by checking whether current string values in the entry boxes are same as that already
    # in the Registry. If they are same, the Update Names button will be disabled, if not, then the button will
    # enabled for the names to be updated.
    def update_update_names_button_state(self):
        if ((self.regowner != self.owner_var.get() or self.regorg != self.org_var.get()) or (self.regowner_x86 != self.owner_var_x86.get() or self.regorg_x86 != self.org_var_x86.get())):
            self.update_btn.configure(state='normal', cursor='hand2')
        else:
            self.update_btn.configure(state='disabled', cursor='arrow')

            

    def update_x86_entries(self):
        if (not self.change_btn_is_disabled and (self.regowner_x86 != self.owner_var_x86.get() or self.regorg_x86 != self.org_var_x86.get() or self.regowner != self.owner_var.get() or self.regorg != self.org_var.get())):
            self.owner_var_x86.set(self.owner_var.get())
            self.org_var_x86.set(self.org_var.get())




'''[MAIN BLOCK]'''
if (__name__ == '__main__'):

    '''
    # Regalter is OS-architecture-specific, and this code is for the 64-bit version of Windows, so we will perform
    # an architecture checking below (Alhough this is not required because Windows(32-bit) automatically performs 
    # an arcitecture check before executing a program, and Windows(64-bit) will obviously execute it. This is just
    # for the sake of clarity about how Regalter works).

    if (architecture()[0] != '64bit'):
        mbox(0, APP_NAME[0:APP_NAME.index(":")]+" cannot run properly on the version of Windows you\'re running. \
        Check your computer's system information to see whether you need an x86 (32-bit) or x64 (64-bit) version of "+APP_NAME[0:APP_NAME.index(":")]+", \
        and then reinstall the correct version of "+APP_NAME[0:APP_NAME.index(":")]+".", "Error: Architechture Mismatch", mboxconst.MB_OK | mboxconst.MB_ICONERROR | mboxconst.MB_TASKMODAL)
        print ("Closed "+APP_NAME[0:APP_NAME.index(":")]+" without any errors.")
        raise SystemExit # Will close Regalter if the Regalter's architecture and OS architecture doesn't match
    '''
    # The commented out code fragment above does not work properly

    # Now to be able to make changes to the Registry, Regalter must be run with administrative previleges. The check
    # below ensures that the user starting Regalter is an administrator.

    if (not ctypes.windll.shell32.IsUserAnAdmin()):
        mbox(0,
            "You must be an administrator to change the names of the registered owner and registered organization. Try running Regalter as administrator to solve this problem.",
            "Error",
            mboxconst.MB_OK | mboxconst.MB_ICONSTOP | mboxconst.MB_SYSTEMMODAL)
        print ("Closed "+APP_NAME[0:APP_NAME.index(" ")]+" without any errors.")
        raise SystemExit # Will close Regalter if the user is not an admin


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
    gui = Regalter(Initial_RegisteredOwner = Initial_RegisteredOwner,
                   Initial_RegisteredOrganization = Initial_RegisteredOrganization,
                   Initial_RegisteredOwner_x86 = Initial_RegisteredOwner_x86,
                   Initial_RegisteredOrganization_x86 = Initial_RegisteredOrganization_x86)

    # We will not use tkinter's mainloop() function as it simply blocks program execution instead of iterating it.
    # The while loop below would serve as the mainloop of the program.
    while (1):
        
        try:
            #gui.force_center_window() # Force the window to stay at the center of the screen
            
            gui.update_x86_entries()
            
            gui.update_update_names_button_state() # Update the state of the Update Names button
            
            gui.root_window.update() # Force tkinter to apply the above updates. If this line is missing, the root
                                     # window will not be visible

        except KeyboardInterrupt: # The program must not be interrupted
            print ("Warning: KeyboardInterrupt has been raised.")
            continue

        # When the root window has been destroyed but this while loop is still running, tkinter.TclError will be
        # raised in the try block. The except block below will ensure that the program exits safely.
        except tk.TclError:
            print ("Closed "+APP_NAME[0:APP_NAME.index(" ")]+" without any errors.")
            raise SystemExit

        sleep(0.01) # This would prevent high CPU usage because of the main loop
