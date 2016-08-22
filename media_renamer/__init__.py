#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from media_renamer.renamer import Renamer

LARGE_FONT = ("Verdana", 12)


# ext_list = [".jpg", ".jpeg", ".mov", ".mts", ".mp4"]

# for file in sys.argv[1:]:
#     if os.path.splitext(file)[1].lower() in ext_list:
#         Renamer.rename(file)


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

        for F in (MainView, SettingsView):
            frame = F(container, self, padding="10")
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # the menu
        # menubar = tk.Menu(container)
        # filemenu = tk.Menu(menubar, tearoff=0)
        # filemenu.add_command(label="Settings", command=self.show_frame(SettingsView))
        # filemenu.add_separator()
        # filemenu.add_command(label="Exit", command=quit)
        # menubar.add_cascade(label="File", menu=filemenu)

        # tk.Tk.config(self, menu=menubar)

        self.show_frame(MainView)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainView(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        self.directory_path = tk.StringVar()

        directory_lbl = ttk.Label(self, text="Ordner:", anchor="e")
        directory_entry = ttk.Entry(self, textvariable=self.directory_path)
        directory_btn = ttk.Button(self, text="Durchsuchen", command=lambda: self.open_folderpicker())

        # TODO Table
        table_frame = ttk.Frame(self, padding="5")

        settings_btn = ttk.Button(self, text="Settings",
                                  command=lambda: controller.show_frame(SettingsView), padding="5")

        preview_btn = ttk.Button(self, text="Vorschau", command=lambda: print("Vorschau"), padding="5")
        start_btn = ttk.Button(self, text="Umbennen", command=lambda: print("Umbennen"), padding="5")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        directory_lbl.grid(row=0, column=0, sticky="nw")
        directory_entry.grid(row=0, column=1, columnspan=2, sticky="nwe")
        directory_btn.grid(row=0, column=3, sticky="ne")

        table_frame.grid(row=1, column=0, columnspan=4, sticky="nwe")

        settings_btn.grid(row=2, column=0, sticky="sw")
        preview_btn.grid(row=2, column=2, sticky="se")
        start_btn.grid(row=2, column=3, sticky="se")

    def open_folderpicker(self):
        print(self.directory_path.get())
        directory = filedialog.askdirectory()
        print(directory)


class SettingsView(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        label = ttk.Label(self, text="This is the settings page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Speichern",
                            command=lambda: controller.show_frame(MainView))
        button.pack()

        button2 = ttk.Button(self, text="Abbrechen",
                             command=lambda: controller.show_frame(MainView))
        button2.pack()


def main():
    app = MediaRenamerApp()
    app.geometry("800x600")
    app.mainloop()


if __name__ == '__main__':
    main()
