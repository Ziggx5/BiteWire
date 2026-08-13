from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class ServerSettings(QWidget):
    def __init__(self):
        super().__init__()

        self.server_name = None
        self.server_address = None

        self.setFixedSize(500, 350)
        self.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout(self)

        server_icon = QLabel("Server Icon")

        server_name = QLabel("Server Name")

        delete_button = QPushButton("Delete Server")

        cancel_button = QPushButton("Cancel")

        confirm_button = QPushButton("Confirm")

        layout.addWidget(server_icon)
        layout.addWidget(server_name)
        layout.addWidget(delete_button)
        layout.addWidget(cancel_button)
        layout.addWidget(confirm_button)

    def get_server_info(self, server_name, server_address):
        self.server_name = server_name
        self.server_address = server_address
        print(self.server_name)
        print(self.server_address)