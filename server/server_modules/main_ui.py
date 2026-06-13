from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import threading
from server_modules.data_manipulation import local_data_file, files_check
from server_modules.server import ChatServer
from server_modules.system_tray import TrayManager
from server_modules.load_assets import file_root

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BiteWire Server")
        self.setObjectName("main_ui")
        self.setStyleSheet("""
            QWidget#main_ui {
                background-color : #0e1117;
            }
        """)
        self.setFixedSize(600, 500)
        self.tray = TrayManager(self)
        self.chat_server = ChatServer()
        self.chat_server.uptime_signal.connect(self.update_timer)
        self.local_file = local_data_file()
        image_path = file_root()
        self.files = files_check()

        layout = QVBoxLayout(self)

        cards_layout = QHBoxLayout()

        cards_layout.addWidget(StatCard("Server Status", "Stopped"))
        cards_layout.addWidget(StatCard("Connected Clients", "0", "View all >"))
        cards_layout.addWidget(StatCard("Total Messages", "0"))
        cards_layout.addWidget(StatCard("Uptime", "0"))

        ssl_box = QGroupBox("SSL Certificate Files")
        ssl_box_layout = QVBoxLayout()
        certificate_file_layout = QHBoxLayout()
        key_file_layout = QHBoxLayout()

        databases_box = QGroupBox("Database files")
        database_files_layout = QVBoxLayout()
        users_database_layout = QHBoxLayout()
        messages_database_layout = QHBoxLayout()

        server_control_box = QGroupBox("Server Control")
        server_control_box_layout = QVBoxLayout()
        server_status_layout = QHBoxLayout()
        server_uptime_layout = QHBoxLayout()
        server_buttons_layout = QHBoxLayout()

        server_folder_layout = QHBoxLayout()

        certificate_file_label = QLabel("Certificate file:")
        self.certificate_file_input = QLineEdit()

        key_file_label = QLabel("Key file:")
        self.key_file_input = QLineEdit()

        users_database_file_label = QLabel("Users database file:")
        self.users_database_file_input = QLineEdit()

        messages_database_file_label = QLabel("Messages database file:")
        self.messages_database_file_input = QLineEdit()

        self.start_server_button = QPushButton("Start Server")
        self.start_server_button.clicked.connect(self.start_server)
        self.stop_server_button = QPushButton("Stop Server")
        self.stop_server_button.clicked.connect(self.stop_server)
        self.stop_server_button.setEnabled(False)

        server_status_label = QLabel("Server Status:")
        self.server_status_state = QLabel("Stopped")

        server_uptime_label = QLabel("Server Uptime")
        self.server_uptime_time = QLabel("Time")

        server_folder_button = QPushButton()
        server_folder_button.setIcon(QIcon(f"{image_path}/folder.png"))
        server_folder_button.setIconSize(QSize(15, 15))
        server_folder_button.setFixedSize(35, 35)
        server_folder_button.clicked.connect(self.open_server_folder)

        certificate_file_layout.addWidget(certificate_file_label)
        certificate_file_layout.addWidget(self.certificate_file_input)

        key_file_layout.addWidget(key_file_label)
        key_file_layout.addWidget(self.key_file_input)

        ssl_box_layout.addLayout(certificate_file_layout)
        ssl_box_layout.addLayout(key_file_layout)

        ssl_box.setLayout(ssl_box_layout)

        users_database_layout.addWidget(users_database_file_label)
        users_database_layout.addWidget(self.users_database_file_input)

        messages_database_layout.addWidget(messages_database_file_label)
        messages_database_layout.addWidget(self.messages_database_file_input)

        database_files_layout.addLayout(users_database_layout)
        database_files_layout.addLayout(messages_database_layout)

        databases_box.setLayout(database_files_layout)

        server_status_layout.addWidget(server_status_label)
        server_status_layout.addWidget(self.server_status_state)

        server_uptime_layout.addWidget(server_uptime_label)
        server_uptime_layout.addWidget(self.server_uptime_time)

        server_buttons_layout.addWidget(self.start_server_button)
        server_buttons_layout.addWidget(self.stop_server_button)

        server_control_box_layout.addLayout(server_status_layout)
        server_control_box_layout.addLayout(server_uptime_layout)
        server_control_box_layout.addLayout(server_buttons_layout)

        server_folder_layout.addStretch()
        server_folder_layout.addWidget(server_folder_button)

        server_control_box.setLayout(server_control_box_layout)

        layout.addLayout(cards_layout)
        layout.addWidget(ssl_box)
        layout.addWidget(databases_box)
        layout.addWidget(server_control_box)
        layout.addLayout(server_folder_layout)

        self.certificate_file_input.setEnabled(False)
        self.key_file_input.setEnabled(False)
        self.users_database_file_input.setEnabled(False)
        self.messages_database_file_input.setEnabled(False)

        self.fill_inputs(self.files)

    def fill_inputs(self, files):
        for file_path in files:
            if file_path.endswith(".crt"):
                self.certificate_file_input.setText(file_path)

            elif file_path.endswith(".key"):
                self.key_file_input.setText(file_path)

            elif file_path.endswith("users.db"):
                self.users_database_file_input.setText(file_path)
                
            elif file_path.endswith("messages.db"):
                self.messages_database_file_input.setText(file_path)

    def start_server(self):
        if not self.certificate_file_input.text() or not self.key_file_input.text():
            return

        threading.Thread(target = self.chat_server.start, daemon = True).start()

        self.server_status_state.setText("Running")
        self.start_server_button.setEnabled(False)
        QTimer.singleShot(2000, lambda: self.stop_server_button.setEnabled(True))

        self.tray.set_server_status("Running")

    def stop_server(self):
        self.chat_server.stop()
        self.server_status_state.setText("Stopped")
        self.stop_server_button.setEnabled(False)
        QTimer.singleShot(2000, lambda: self.start_server_button.setEnabled(True))

        self.tray.set_server_status("Stopped")

        self.update_timer(0, 0, 0)
    
    def update_timer(self, hours, minutes, seconds):
        self.server_uptime_time.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
        self.tray.set_server_uptime(hours, minutes, seconds)
        
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def open_server_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.local_file))

class StatCard(QFrame):
    def __init__(self, title, value, subtitle = None):
        super().__init__()

        self.setObjectName("statcard")

        self.setStyleSheet("""
            QFrame#statcard {
                background-color: #111827;
                border: 1px solid #23304a;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #d1d5db;
                font-size: 12px;
            }
        """)

        value_label = QLabel(value)
        value_label.setStyleSheet("""
            QLabel {
                color: #4ade80;
                font-size: 23px;
                font-weight: 700px;
            }
        """)

        layout.addWidget(title_label)
        layout.addSpacing(10)
        layout.addWidget(value_label)
        layout.addStretch()

        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("""
                QLabel {
                    color: #60a5fa;
                    font-size: 11px;
                }
            """)
            layout.addWidget(subtitle_label)