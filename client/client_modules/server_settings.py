from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from client_modules.data_manipulation import app_directory

class ServerSettings(QWidget):
    def __init__(self):
        super().__init__()

        self.server_name = None
        self.server_address = None

        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        header_label = QLabel("Server Settings")
        exit_button = QPushButton("Exit_icon")

        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(exit_button)

        main_screen = QFrame()
        main_screen_layout = QVBoxLayout(main_screen)
        server_icon = QLabel("Server Icon")
        server_name = QLabel("Server Name")
        delete_button = QPushButton("Delete Server")
        confirm_button = QPushButton("Confirm")

        main_screen_layout.addWidget(server_icon)
        main_screen_layout.addWidget(server_name)
        main_screen_layout.addWidget(delete_button)
        main_screen_layout.addWidget(confirm_button)

        sidebar_server_stat = QFrame()
        sidebar_server_stat_grid = QGridLayout(sidebar_server_stat)
        sidebar_server_stat_grid.setContentsMargins(10, 10, 10, 10)
        sidebar_server_stat_grid.setVerticalSpacing(5)
        sidebar_server_stat_grid.setHorizontalSpacing(15)

        self.sidebar_server_stat_icon = QLabel()
        self.sidebar_server_stat_icon.setFixedSize(80, 80)
        self.sidebar_server_stat_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_server_stat_icon.setStyleSheet("""
            QLabel {
                background-color: #1e2233;
                border: 1px solid #30364d;
                border-radius: 12px;
            }
        """)
        self.sidebar_server_stat_name = QLabel("Server_name")
        self.sidebar_server_stat_name.setStyleSheet("""
            QLabel {
                color: #f3f4f6;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        sidebar_server_stat_connection_status = QLabel("Status")
        sidebar_server_stat_connection_status.setStyleSheet("""
            QLabel {
                color: #86d48a;
                font-size: 13px;
                font-weight: 500;
            }
        """)

        sidebar_server_stat_grid.addWidget(self.sidebar_server_stat_icon, 0, 0, 2, 1)
        sidebar_server_stat_grid.addWidget(self.sidebar_server_stat_name, 0, 1)
        sidebar_server_stat_grid.addWidget(sidebar_server_stat_connection_status, 1, 1)

        sidebar = QFrame()
        sidebar_layout = QVBoxLayout(sidebar)

        sidebar_layout.addWidget(sidebar_server_stat)
        sidebar_layout.addStretch()

        container_layout = QHBoxLayout()
        container_layout.addWidget(sidebar)
        container_layout.addWidget(main_screen)

        layout.addLayout(header_layout)
        layout.addLayout(container_layout)

    def get_server_info(self, server_name, server_address):
        self.server_name = server_name
        self.server_address = server_address
        self.fill_server_info()

    def fill_server_info(self):
        self.sidebar_server_stat_name.setText(self.server_name)
        self.sidebar_server_stat_icon.setPixmap(QPixmap(f"{app_directory()}/server_icons/{self.server_name}.png").scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))