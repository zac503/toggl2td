import tkinter as tk
import os


currentdir = os.path.dirname(__file__)
mypath = os.path.join(currentdir, 'Configurations')

onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]


window = tk.Tk()
header = tk.Label(text="Toggl2TD - Automated Time Entry System")
header.pack()
variable = tk.StringVar(window)
variable = set(onlyfiles[0])

w = tk.OptionMenu(window,
                  variable,
                  *onlyfiles)
w.configure(width=20)
w.pack()


window.mainloop()