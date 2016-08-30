# -*- coding: utf-8 -*-

import sys, os
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    os.environ["TCL_LIBRARY"] = "C:\\tools\\python3\\tcl\\tcl8.6"
    os.environ["TK_LIBRARY"] = "C:\\tools\\python3\\tcl\\tk8.6"

executables = [
    Executable("media_renamer/__init__.py",
               base=base,
               targetName="MediaRenamer.exe",
               icon="media_renamer/resources/icon.ico"
               )
]

setup(name="media_renamer",
      version="0.0.1",
      description="A simple tool for renaming media files as their creation date",
      executables=executables
      )
