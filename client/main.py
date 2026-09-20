from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory
from PySide6.QtGui import QIcon
from client_modules.loading_ui import LoadingScreen
from client_modules.path_finder import app_icon
import sys

shared_memory = QSharedMemory("BiteWire")

def main():
    if not shared_memory.create(1):
        sys.exit(0)
        
    app = QApplication()
    app.setWindowIcon(QIcon(app_icon()))
    window = LoadingScreen()
    window.show()
    window.update_progress_bar()
    app.exec()

if __name__ == "__main__":
    main()