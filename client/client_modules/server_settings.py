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
        self.status = None

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
        main_screen_layout = QGridLayout(main_screen)
        main_screen_layout.setVerticalSpacing(20)

        server_name_label = QLabel("Server Name")
        server_name_label.setStyleSheet("""
            QLabel {
                color: #e5e7eb;
                font-size: 15px;
                font-weight: 600;
            }
        """)

        self.server_name_input = QLineEdit()
        self.server_name_input.setStyleSheet("""
            QLineEdit {
                background-color: #151a24;
                color: #e5e7eb;
                border: 1px solid #2b3448;
                border-radius: 6px;
                padding: 8px;
            }
            
            QLineEdit:focus {
                border: 1px solid #5865f2;
            }
        """)

        server_address_label = QLabel("Server Address")
        server_address_label.setStyleSheet("""
            QLabel {
                color: #e5e7eb;
                font-size: 15px;
                font-weight: 600;
            }
        """)

        self.server_address_input = QLineEdit()
        self.server_address_input.setReadOnly(True)
        self.server_address_input.setStyleSheet("""
            QLineEdit {
                background-color: #151a24;
                color: #e5e7eb;
                border: 1px solid #2b3448;
                border-radius: 6px;
                padding: 8px;
            }
        """)

        copy_button = QPushButton("Copy")
        copy_button.setIcon(QIcon(f"{file_root()}/clipboard.png"))
        copy_button.setIconSize(QSize(20, 20))
        copy_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e5e7eb;
                border: 1px solid #343f56;
                border-radius: 6px;
                padding: 5px;
            }
        """)

        server_port_label = QLabel("Server Port")
        server_port_label.setStyleSheet("""
            QLabel {
                color: #e5e7eb;
                font-size: 15px;
                font-weight: 600;
            }
        """)

        server_port_input = QLineEdit("50505")
        server_port_input.setReadOnly(True)
        server_port_input.setStyleSheet("""
            QLineEdit {
                background-color: #151a24;
                color: #e5e7eb;
                border: 1px solid #2b3448;
                border-radius: 6px;
                padding: 8px;
            }
        """)

        save_button = QPushButton("Save Changes")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #5865f2;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                padding: 10px
            }
        """)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(save_button)

        main_screen_layout.addWidget(server_name_label, 0, 0)
        main_screen_layout.addWidget(self.server_name_input, 1, 0)
        main_screen_layout.addWidget(server_address_label, 2, 0)
        main_screen_layout.addWidget(self.server_address_input, 3, 0)
        main_screen_layout.addWidget(copy_button, 3, 1)
        main_screen_layout.addWidget(server_port_label, 4, 0)
        main_screen_layout.addWidget(server_port_input, 5, 0)
        main_screen_layout.setRowStretch(6, 1)
        main_screen_layout.addLayout(buttons_layout, 7, 0, 1, 2)
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
        self.sidebar_server_stat_connection_status = QLabel("Status")
        self.sidebar_server_stat_connection_status.setStyleSheet("""
            QLabel {
                color: #86d48a;
                font-size: 13px;
                font-weight: 500;
            }
        """)

        sidebar_server_stat_grid.addWidget(self.sidebar_server_stat_icon, 0, 0, 2, 1)
        sidebar_server_stat_grid.addWidget(self.sidebar_server_stat_name, 0, 1)
        sidebar_server_stat_grid.addWidget(self.sidebar_server_stat_connection_status, 1, 1)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(180)
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
        remove_server_button.clicked.connect(self.remove_server)
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
        container_layout.addSpacing(10)
        container_layout.addWidget(main_screen)

        layout.addLayout(header_layout)
        layout.addLayout(container_layout)

    def get_server_info(self, server_name, server_address, status):
        self.server_name = server_name
        self.server_address = server_address
        self.status = status
        self.fill_server_info()

    def fill_server_info(self):
        self.sidebar_server_stat_name.setText(self.server_name)
        self.sidebar_server_stat_icon.setPixmap(QPixmap(f"{app_directory()}/server_icons/{self.server_name}.png").scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.server_name_input.setText(self.server_name)
        self.server_address_input.setText(self.server_address)
        self.sidebar_server_stat_connection_status.setText(self.status)

    def remove_server(self):
        reply = QMessageBox.information(self, "Remove Server", "Remove Server", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            print("Removing Server")
        else:
            print("No")