from PySide6.QtWidgets import QApplication
from client_modules.loading_ui import LoadingScreen

def main():
    app = QApplication()
    window = LoadingScreen()
    window.show()
    window.update_progress_bar()
    app.exec()

if __name__ == "__main__":
    main()