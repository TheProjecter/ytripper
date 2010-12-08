import Tkinter
import Tkconstants
import ytripper_base
from Tkconstants import *

def start():
    print cConvert.get()
    instance = ytripper_base.YT_ripper()
    
    if cConvert: instance.modes["mp3-conversion"] = True
    if cCheckplaylist: instance.modes["check-playlist"] = True
    if cKeepTmp: instance.modes["keep-files-tmp"] = True
    
    instance.links.append(cLink.get())
    instance.process()

tk = Tkinter.Tk()

gui_interface = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
gui_interface.pack(fill=BOTH,expand=1)

cConvert = Tkinter.IntVar()
cConvertBox = Tkinter.Checkbutton(gui_interface,text="Convert to mp3?", variable=cConvert)
cConvertBox.pack()

cCheckplaylist = Tkinter.IntVar()
cCheckplaylistBox = Tkinter.Checkbutton(gui_interface,text="Check playlist?", variable=cCheckplaylist)
cCheckplaylistBox.pack()

cKeepTmp = Tkinter.IntVar()
cKeepTmpBox = Tkinter.Checkbutton(gui_interface,text="Keep tmp-files?", variable=cKeepTmp)
cKeepTmpBox.pack()

cLink = Tkinter.StringVar()
textbox = Tkinter.Entry(tk, textvariable=cLink)
textbox.pack()

button = Tkinter.Button(gui_interface,text="Start",command=start)
button.pack()

tk.mainloop()
