#!/usr/bin/env python3
import os
from tkinter import *
from tkinter.ttk import *
import tkinter as tk

from media_renamer.mediarenamergui import MediaRenamerGui
from media_renamer.renamer import Renamer

if sys.version_info[0] < 3:
    raise Exception("Media Renamer should be run with Python 3")
elif sys.version_info[1] < 5:
    raise Exception("Media Renamer requires Python 3.5+")

ext_list = [".jpg", ".jpeg", ".mov", ".mts", ".mp4"]

for file in sys.argv[1:]:
    if os.path.splitext(file)[1].lower() in ext_list:
        Renamer.rename(file)


