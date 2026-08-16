from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from client_modules.data_manipulation import app_directory
from client_modules.path_finder import file_root

class ServerSettings(QWidget):
    def __init__(self):
        super().__init__()

        self.server_name = None
        self.server_address = None

        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 10)
        header_label = QLabel("Server Settings")
        header_label.setStyleSheet("""
            QLabel {
                color: #f3f4f6;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        exit_button = QPushButton("×")
        exit_button.setFixedSize(35, 35)

        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(exit_button)

        main_screen = QFrame()
        main_screen.setObjectName("main_screen")
        main_screen.setStyleSheet("""
            QFrame#main_screen {
                background-color: #1a1f2c;
                border: 1px solid #252d40;
                border-radius: 10px;
            }
        """)
        main_screen_layout = QVBoxLayout(main_screen)
        server_icon = QLabel("Server Icon")
        server_name = QLabel("Server Name")
        confirm_button = QPushButton("Apply changes")

        main_screen_layout.addWidget(server_icon)
        main_screen_layout.addWidget(server_name)
        main_screen_layout.addWidget(confirm_button)

        sidebar_server_stat = QFrame()
        sidebar_server_stat_grid = QGridLayout(sidebar_server_stat)
        sidebar_server_stat_grid.setHorizontalSpacing(15)
        sidebar_server_stat_grid.setContentsMargins(0, 0, 0, 0)

        self.sidebar_server_stat_icon = QLabel()
        self.sidebar_server_stat_icon.setFixedSize(60, 60)
        self.sidebar_server_stat_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_server_stat_icon.setStyleSheet("""
            QLabel {
                background-color: #1e2233;
                border: 1px solid #30364d;
                border-radius: 10px;
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
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar.setContentsMargins(0, 0, 0, 0)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        general_button = QPushButton("General")
        general_button.setIcon(QIcon(f"{file_root()}/settings.png"))
        general_button.setIconSize(QSize(20, 20))
        general_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d1d5db;
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #1d2638;
                color: white;
            }
        """)
        appearance_button = QPushButton("Appearance")
        appearance_button.setIcon(QIcon(f"{file_root()}/pallete.png"))
        appearance_button.setIconSize(QSize(20, 20))
        appearance_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d1d5db;
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }

            QPushButton:hover {
                background-color: #1d2638;
                color: white;
            }
        """)
        notification_button = QPushButton("Notification")
        notification_button.setIcon(QIcon(f"{file_root()}/notification.png"))
        notification_button.setIconSize(QSize(20, 20))
        notification_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d1d5db;
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }

            QPushButton:hover {
                background-color: #1d2638;
                color: white;
            }
        """)

        remove_server_button = QPushButton("Remove Server")
        remove_server_button.setIcon(QIcon(f"{file_root()}/trash.png"))
        remove_server_button.setIconSize(QSize(20, 20))
        remove_server_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d65e60;
                border: none;
                text-align: left;
                padding: 10px;
                font-weight: 600;
            }
            
            QPushButton:hover {
                background-color: #2a1820;
                border-radius: 6px;
            }
        """)
        sidebar_layout.addWidget(sidebar_server_stat)
        sidebar_layout.addSpacing(10)
        sidebar_layout.addWidget(general_button)
        sidebar_layout.addWidget(appearance_button)
        sidebar_layout.addWidget(notification_button)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(remove_server_button)

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