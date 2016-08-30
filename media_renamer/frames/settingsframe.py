# -*- coding: utf-8 -*-
from tkinter import ttk


class SettingsFrame(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        label = ttk.Label(self, text="Einstellungen")
        label.pack(pady=10, padx=10)

        save_btn = ttk.Button(self, text="Speichern",
                              command=controller.show_main)
        save_btn.pack()

        cancel_btn = ttk.Button(self, text="Abbrechen",
                                command=controller.show_main)
        cancel_btn.pack()
