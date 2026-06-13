import os
import sys

def file_root():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    picture_path = os.path.join(root, "client_pictures")
        
    return picture_path

def app_icon():
    picture_path = file_root()

    if sys.platform.startswith("win"):
        icon_path = os.path.join(picture_path, "icon.ico")
    
    else:
        icon_path = os.path.join(picture_path, "icon.png")

    return icon_path