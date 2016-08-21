#!/usr/bin/env python3
import os
import sys
import tkinter as tk

from media_renamer.renamer import Renamer

if sys.version_info[0] < 3:
    raise Exception("Media Renamer should be run with Python 3")
elif sys.version_info[1] < 5:
    raise Exception("Media Renamer requires Python 3.5+")

ext_list = [".jpg", ".jpeg", ".mov", ".mts", ".mp4"]

for file in sys.argv[1:]:
    if os.path.splitext(file)[1].lower() in ext_list:
        Renamer.rename(file)


class MediaRenamerApp(tk.Frame):
    """The graphical user interface for Media Renamer"""

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    @staticmethod
    def say_hi():
        print("hi there, everyone!")


root = tk.Tk()
app = MediaRenamerApp(master=root)
app.mainloop()
