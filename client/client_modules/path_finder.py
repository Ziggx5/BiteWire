import os
import sys

def file_root():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return root_path

def app_icon():
    root_path = file_root()

    if sys.platform.startswith("win"):
        icon_path = os.path.join(f"{root_path}/client_pictures", "icon.ico")
    
    else:
        icon_path = os.path.join(f"{root_path}/client_pictures", "icon.png")

    return icon_path