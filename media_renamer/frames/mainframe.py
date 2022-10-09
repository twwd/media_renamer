# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from media_renamer.logic.renamer import Directory


class MainFrame(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller

        # Directory controls
        self.directory_path = tk.StringVar()
        self.dir = None

        directory_lbl = ttk.Label(self, text="Ordner:", anchor="e")
        directory_entry = ttk.Entry(self, textvariable=self.directory_path)
        directory_btn = ttk.Button(self, text="Durchsuchen", command=self.open_folderpicker)

        directory_entry.bind('<Control-KeyRelease-a>', func=MainFrame.select_all)
        self.directory_path.trace_add(mode="write",
                                      callback=lambda name, index, mode, var=self.directory_path: self.read_dir())

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

        # table_progress = ttk.Progressbar(table_frame, orient=tk.HORIZONTAL, mode='indeterminate')

        self.table = table

        # Footer buttons
        # settings_btn = ttk.Button(self, text="Einstellungen",
        #                          command=controller.show_settings, padding="5")

        self.ignore_already_renamed = tk.BooleanVar(value=True)
        ignore_already_renamed_checkbox = tk.Checkbutton(self, text='Bereits umbenannte Dateien ignorieren?',
                                                         variable=self.ignore_already_renamed,
                                                         onvalue=True, offvalue=False, command=self.re_enable_preview)
        preview_btn = ttk.Button(self, text="Vorschau", command=self.generate_new_file_names, padding="5",
                                 state=tk.DISABLED)
        start_btn = ttk.Button(self, text="Umbennen", command=self.rename, padding="5", state=tk.DISABLED)
        self.preview_btn = preview_btn
        self.start_btn = start_btn

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
        # table_progress.grid(row=1, column=0, columnspan="2", sticky="we", pady=(5, 5))

        # settings_btn.grid(row=2, column=0, sticky="sw")
        ignore_already_renamed_checkbox.grid(row=2, column=0, sticky="sw")
        preview_btn.grid(row=2, column=2, sticky="se")
        start_btn.grid(row=2, column=3, sticky="se", padx=(5, 0))

    def open_folderpicker(self):
        directory = filedialog.askdirectory(initialdir=self.directory_path.get())
        if directory != "":
            self.directory_path.set(directory)
            self.read_dir()

    def read_dir(self):
        try:
            self.dir = Directory(self.directory_path.get())
        except NotADirectoryError:
            return
        self.load_table()
        self.set_enabled_state(self.preview_btn, True)
        self.set_enabled_state(self.start_btn, False)

    def generate_new_file_names(self):
        if self.dir is None:
            return
        self.set_status("Vorschau generieren...")
        self.dir.generate_new_file_names(self.ignore_already_renamed.get())
        self.load_table()
        self.set_status("Vorschau generieren abgeschlossen")
        self.set_enabled_state(self.start_btn, True)

    def rename(self):
        self.set_status("Umbennen...")
        self.dir.rename()
        self.clear_table()
        self.set_status("Umbennen abgeschlossen")

    def load_table(self):
        self.clear_table()
        odd = False
        for old_file_name, new_file_name in self.dir.file_names:

            odd_even = "odd" if odd else "even"

            if old_file_name == new_file_name:
                tags = ("nochanges", odd_even)
            else:
                tags = (odd_even,)
            self.table.insert("", 'end', text=old_file_name, values=(new_file_name,), tags=tags)
            odd = not odd

    def clear_table(self):
        self.set_enabled_state(self.preview_btn, False)
        self.set_enabled_state(self.start_btn, False)
        for widget in self.table.get_children():
            self.table.delete(widget)

    def set_status(self, text):
        self.controller.status["text"] = text

    def re_enable_preview(self):
        self.set_enabled_state(self.preview_btn, True)
        self.set_enabled_state(self.start_btn, False)

    @staticmethod
    def set_enabled_state(btn, enabled=False):
        if enabled:
            btn.state(["!disabled"])
        else:
            btn.state(["disabled"])

    @staticmethod
    def select_all(event):
        # select text
        event.widget.select_range(0, 'end')
        # move cursor to the end
        event.widget.icursor('end')
