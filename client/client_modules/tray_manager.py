from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction
from client_modules.path_finder import file_root
import webbrowser

class TrayManager:
    def __init__(self, parent):
        self.parent = parent

        picture_path = file_root()

        self.tray_icon = QSystemTrayIcon(QIcon(f"{picture_path}/tray.png"), parent)
        self.tray_icon.setToolTip("BiteWire")

        tray_menu = QMenu()
        
        github_link_action = QAction("Github Repository", self.tray_icon)
        github_link_action.triggered.connect(self.open_link)

        open_action = QAction("Open BiteWire", self.tray_icon)
        open_action.triggered.connect(self.parent.show)

        exit_action = QAction("Exit BiteWire", self.tray_icon)
        exit_action.triggered.connect(self.exit_app)

        tray_menu.addAction(github_link_action)
        tray_menu.addSeparator()
        tray_menu.addAction(open_action)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.parent.show)
        self.tray_icon.show()

    def exit_app(self):
        self.tray_icon.hide()
        QApplication.exit()
    
    def open_link(self):
        webbrowser.open("https://github.com/Ziggx5/BiteWire")