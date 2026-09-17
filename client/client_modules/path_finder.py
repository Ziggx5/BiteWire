import os
import sys

def updater_executable_path():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.join(os.path.dirname(__file__), "..", "..", "updater")

def bitewire_executable_path():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.join(os.path.dirname(__file__), "..")

def resource_path():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS

    return os.path.join(os.path.dirname(__file__), "..")

def app_icon():
    resources = resource_path()

    if sys.platform.startswith("win"):
        icon_path = os.path.join(f"{resources}/client_pictures", "icon.ico")
    
    else:
        icon_path = os.path.join(f"{resources}/client_pictures", "icon.png")

    return icon_path