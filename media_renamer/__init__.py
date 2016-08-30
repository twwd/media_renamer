#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from media_renamer.frames.mainframe import MainFrame
from media_renamer.frames.settingsframe import SettingsFrame


class MediaRenamerApp(tk.Tk):
    """The graphical user interface for Media Renamer"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="resources/icon.ico")
        tk.Tk.wm_title(self, "Media Renamer")

        # create container for widgets
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # the different views
        self.frames = {}

        for F in [MainFrame, SettingsFrame]:
            frame = F(container, self, padding="10")
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

        self.show_main()

    def show_main(self):
        self.show_frame(MainFrame)

    def show_settings(self):
        self.show_frame(SettingsFrame)

    def show_frame(self, f):
        frame = self.frames[f]
        frame.tkraise()


def main():
    app = MediaRenamerApp()
    app.geometry("800x600")
    app.mainloop()


if __name__ == "__main__":
    main()
