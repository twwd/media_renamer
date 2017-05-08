# -*- coding: utf-8 -*-

import sys
import os
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    os.environ["TCL_LIBRARY"] = "C:\\tools\\python3\\tcl\\tcl8.6"
    os.environ["TK_LIBRARY"] = "C:\\tools\\python3\\tcl\\tk8.6"

build_exe_options = {
    "include_files": ["media_renamer/resources", "C:\\tools\\python3\\DLLs\\tcl86t.dll",
                      "C:\\tools\\python3\\DLLs\\tk86t.dll"],
    "bin_path_excludes": ["E:\\Program Files\\MiKTeX 2.9\\miktex"],
    "optimize": 2
}

executables = [
    Executable("app.py",
               base=base,
               targetName="MediaRenamer.exe",
               icon="media_renamer/resources/icon.ico"
               )
]

setup(name="media_renamer",
      version="0.0.1",
      description="A simple tool for renaming media files as their creation date",
      options={"build_exe": build_exe_options},
      executables=executables
      )
