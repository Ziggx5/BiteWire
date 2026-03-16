from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory
from server_modules.main_ui import MainUi
import sys

shared_memory = QSharedMemory("Bitwire_server")

def main():
    if not shared_memory.create(1):
        sys.exit(0)

    app = QApplication()
    window = MainUi()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()