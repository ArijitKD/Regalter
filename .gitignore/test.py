import tkinter as tk
import tkinter.ttk as ttk

root = tk.Toplevel()
root.focus_force()
root.grab_set()
root.attributes("-toolwindow", True)
root.geometry("350x200")
root.resizable(0,0)
i = tk.IntVar() #Basically Links Any Radiobutton With The Variable=i.
r1 = ttk.Checkbutton(root, text="option 1", variable=i)
#r2 = ttk.Radiobutton(root, text="option 2", value=2, variable=i)
#
"""
If both values where equal, when one of the buttons
are pressed all buttons would be pressed.
If a button is pressed its value is true, or 1.
If you want to acess the data from the
radiobuttons, use a if statment like
"""
r1.pack()

while (1):
    try:
        if (i.get() == 1):
            print("you picked option1")
            while (i.get() == 1):
                root.update()
        else:
            print("you picked option2")
            while (i.get() != 1):
                root.update()
    except tk.TclError:
        pass
# :)
'''
class CheckButtonMsgBox:
    def __init__(self, master=tk.Tk(), attributes={"topmost": False, "fixed_size": True}, geometry={"x":"300", "y":"250", "shift_x":"0", "shift_y":"0"}, 
                 message="Message", title="Title", cbmessage="Checkbox message", cbcommand=None):

        self.msgbox = tk.Toplevel(master = master)
        self.msgbox.focus_set()
        self.msgbox.grab_set()
        self.msgbox.attributes("-toolwindow", True)
        if (attributes["topmost"]):
            self.msgbox.attributes("-topmost", True)
        self.msgbox.geometry(geometry["x"]+"x"+geometry["y"]+"+"+geometry["shift_x"]+"+"+geometry["shift_y"])
        if (attributes["fixed_size"]):
            self.msgbox.resizable(0,0)
        self.msgbox.title(title)
        self.message = message
        #self.title = title
        self.cbmessage = cbmessage
        self.cbcommand = cbcommand

if (__name__ == "__main__"):
    #root = tk.Tk()
    cbmb = CheckButtonMsgBox()

'''
