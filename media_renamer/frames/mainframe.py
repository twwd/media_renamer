import os
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog

from media_renamer import renamer


class MainFrame(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # Directory controls
        self.directory_path = tk.StringVar()

        directory_lbl = ttk.Label(self, text="Ordner:", anchor="e")
        directory_entry = ttk.Entry(self, textvariable=self.directory_path)
        directory_btn = ttk.Button(self, text="Durchsuchen", command=self.open_folderpicker)

        # TODO Table
        table_frame = ttk.Frame(self)
        table = ttk.Treeview(table_frame, columns="new_filename")
        table.heading("#0", text="Ursprünglicher Dateiname", anchor="w")
        table.column("#0", anchor="w")
        table.heading("new_filename", text="Neuer Dateiname", anchor="w")
        table.column("new_filename", anchor="w")
        table.tag_configure('even', background='#EFEFEF')
        table.tag_configure('odd', background='#FFFFFF')
        table.tag_configure('nochanges', foreground="#888888")

        table_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
        table['yscrollcommand'] = table_scroll.set

        self.table = table

        # Footer buttons
        # settings_btn = ttk.Button(self, text="Einstellungen",
        #                          command=controller.show_settings, padding="5")

        preview_btn = ttk.Button(self, text="Vorschau", command=self.read_files, padding="5")
        start_btn = ttk.Button(self, text="Umbennen", command=lambda: print("Umbennen"), padding="5")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Display widgets
        directory_lbl.grid(row=0, column=0, sticky="nw", padx=(0, 5), pady=(2, 2))
        directory_entry.grid(row=0, column=1, columnspan=2, sticky="nwe", padx=5, pady=(2, 2))
        directory_btn.grid(row=0, column=3, sticky="ne", padx=(5, 0))

        table_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", pady=10)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        table.grid(row=0, column=0, sticky="nswe")
        table_scroll.grid(row=0, column=1, sticky="nse")

        # settings_btn.grid(row=2, column=0, sticky="sw")
        preview_btn.grid(row=2, column=2, sticky="se")
        start_btn.grid(row=2, column=3, sticky="se", padx=(5, 0))

        # TODO Testing
        self.directory_path.set(os.path.normpath("D:\\Tim\\Pictures\Fotos\\unsortiert Handy 2016"))
        self.read_files()

    def open_folderpicker(self):
        directory = filedialog.askdirectory(initialdir=self.directory_path.get())
        if directory != "":
            self.directory_path.set(directory)
            self.read_files()

    def read_files(self):
        for widget in self.table.get_children():
            self.table.delete(widget)
        self.load_table(renamer.read_dir(self.directory_path.get()))

    def load_table(self, file_list):
        odd = False
        for file in file_list:
            if odd:
                tag = "odd"
            else:
                tag = "even"
            self.table.insert("", 'end', text=file[0], values=(file[1],), tags=(tag,))
            odd = not odd
