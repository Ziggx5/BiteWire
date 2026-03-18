from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from server_modules.data_manipulation import local_data_file, copy_to_data_dir

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bitwire server")
        self.setStyleSheet("background-color : #0e1117;")
        self.setFixedSize(400, 500)
        local_data_file()
        
        layout = QVBoxLayout(self)

        ssl_box = QGroupBox("SSL Certificate Files")
        ssl_box_layout = QVBoxLayout()
        certificate_file_layout = QHBoxLayout()
        key_file_layout = QHBoxLayout()

        database_box = QGroupBox("Database Management")
        database_box_layout = QHBoxLayout()

        server_control_box = QGroupBox("Server Control")
        server_control_box_layout = QVBoxLayout()
        server_status_layout = QHBoxLayout()
        server_uptime_layout = QHBoxLayout()
        server_buttons_layout = QHBoxLayout()

        certificate_file_label = QLabel("Certificate file:")
        self.certificate_file_input = QLineEdit()
        certificate_file_button = QPushButton("Browse...")
        certificate_file_button.clicked.connect(self.send_file_path)

        key_file_label = QLabel("Key file:")
        self.key_file_input = QLineEdit()
        key_file_button = QPushButton("Browse...")
        key_file_button.clicked.connect(self.send_file_path)

        import_database_button = QPushButton("Import Database")
        export_database_button = QPushButton("Export Database")
        clear_database_button = QPushButton("Clear Database")

        start_server_button = QPushButton("Start Server")
        stop_server_button = QPushButton("Stop Server")

        server_status_label = QLabel("Server Status:")
        server_status_state = QLabel("Stopped")

        server_uptime_label = QLabel("Server Uptime")
        server_uptime_time = QLabel("Time")

        certificate_file_layout.addWidget(certificate_file_label)
        certificate_file_layout.addWidget(self.certificate_file_input)
        certificate_file_layout.addWidget(certificate_file_button)

        key_file_layout.addWidget(key_file_label)
        key_file_layout.addWidget(self.key_file_input)
        key_file_layout.addWidget(key_file_button)

        ssl_box_layout.addLayout(certificate_file_layout)
        ssl_box_layout.addLayout(key_file_layout)

        ssl_box.setLayout(ssl_box_layout)

        database_box_layout.addWidget(import_database_button)
        database_box_layout.addWidget(export_database_button)
        database_box_layout.addWidget(clear_database_button)

        database_box.setLayout(database_box_layout)

        server_status_layout.addWidget(server_status_label)
        server_status_layout.addWidget(server_status_state)

        server_uptime_layout.addWidget(server_uptime_label)
        server_uptime_layout.addWidget(server_uptime_time)

        server_buttons_layout.addWidget(start_server_button)
        server_buttons_layout.addWidget(stop_server_button)

        server_control_box_layout.addLayout(server_status_layout)
        server_control_box_layout.addLayout(server_uptime_layout)
        server_control_box_layout.addLayout(server_buttons_layout)

        server_control_box.setLayout(server_control_box_layout)

        layout.addWidget(ssl_box)
        layout.addWidget(database_box)
        layout.addWidget(server_control_box)

    def send_file_path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "SSL files (*.crt *.key)")
        copied_file_path, extension = copy_to_data_dir(file_path)

        if extension == ".crt":
            self.certificate_file_input.setText(copied_file_path)
        elif extension == ".key":
            self.key_file_input.setText(copied_file_path)
        