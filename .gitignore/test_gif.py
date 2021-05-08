'''
import tkinter
from PIL import Image
from PIL import GifImagePlugin
root = tkinter.Tk()
root.configure(bg='black')
photo = tkinter.PhotoImage(file="assets\\load\\frame1.gif")
gif_index = 1
def next_frame():
    global gif_index
    try:
        #XXX: Move to the next frame
        photo.configure(file="assets\\load\\frame{}.gif".format(gif_index))
        gif_index += 1
    except tkinter.TclError:
        gif_index = 1
        return next_frame()
    else:
        root.after(30, next_frame) # XXX: Fixed animation speed
label = tkinter.Label(root, image=photo, borderwidth=0)
label.pack()
label2 = tkinter.Label(root, text="Please wait", bg='black', fg='white', font=('seoge ui', 11))
label2.place(x=85, y=180)
root.after_idle(next_frame)
root.mainloop()
'''
import tkinter as tk
import tkinter.ttk as ttk
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master, relief='groove', activebackground='#8DCDFF', background='gainsboro', 
                      borderwidth=2, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']
    def on_leave(self, e):
        self['background'] = self.defaultBackground

root = tk.Tk()
'''Border = tk.LabelFrame(root,
                    bd=1.4, #<- Borderwidth.
                    bg="#0078d7", #<- Border color.
                    relief='flat')
Border.pack()'''
classButton = HoverButton(root,text="Classy Button")
classButton.pack()

root.mainloop()
