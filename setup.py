import cx_Freeze
import sys
import os

build_exe_options = {
    "packages": ["tkinter", "selenium", "requests", "bs4", "threading", "time", "random", "re"],
    "excludes": ["unittest"],
    "include_files": [],
    "optimize": 2
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cx_Freeze.setup(
    name="CursorAutoRegister",
    version="1.0",
    description="Automated Cursor account registration tool",
    options={"build_exe": build_exe_options},
    executables=[cx_Freeze.Executable("cursor_auto_register.py", base=base, target_name="CursorAutoRegister.exe")]
)