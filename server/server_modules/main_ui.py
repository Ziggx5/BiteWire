from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import threading
from server_modules.data_manipulation import local_data_file, copy_to_data_dir, files_check, server_info_input_fill, server_info
from server_modules.server import start_receive_connection_thread, stop_receive_connection_thread

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bitwire server")
        self.setStyleSheet("background-color : #0e1117;")
        self.setFixedSize(400, 500)
        local_data_file()
        server_address = server_info_input_fill()
        self.files = files_check()

        layout = QVBoxLayout(self)

        server_info_box = QGroupBox("Server Information")
        server_info_layout = QVBoxLayout()
        server_address_layout = QHBoxLayout()
        server_port_layout = QHBoxLayout()

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

        server_address_label = QLabel("Address:")
        self.server_address_input = QLineEdit()
        self.server_address_input.setText(server_address)

        server_port_label = QLabel("Port:")
        self.server_port_input = QLineEdit()
        self.server_port_input.setText("50505")
        self.server_port_input.setEnabled(False)

        certificate_file_label = QLabel("Certificate file:")
        self.certificate_file_input = QLineEdit()
        certificate_file_button = QPushButton("Browse...")
        certificate_file_button.clicked.connect(lambda: self.send_file_path(".crt"))

        key_file_label = QLabel("Key file:")
        self.key_file_input = QLineEdit()
        key_file_button = QPushButton("Browse...")
        key_file_button.clicked.connect(lambda: self.send_file_path(".key"))

        view_database_button = QPushButton("View Database")
        import_database_button = QPushButton("Import Database")
        export_database_button = QPushButton("Export Database")
        clear_database_button = QPushButton("Clear Database")

        self.start_server_button = QPushButton("Start Server")
        self.start_server_button.clicked.connect(lambda: self.start_server())
        self.stop_server_button = QPushButton("Stop Server")
        self.stop_server_button.clicked.connect(lambda: self.stop_server())
        self.stop_server_button.setEnabled(False)

        server_status_label = QLabel("Server Status:")
        self.server_status_state = QLabel("Stopped")

        server_uptime_label = QLabel("Server Uptime")
        self.server_uptime_time = QLabel("Time")

        server_address_layout.addWidget(server_address_label)
        server_address_layout.addWidget(self.server_address_input)

        server_port_layout.addWidget(server_port_label)
        server_port_layout.addWidget(self.server_port_input)

        server_info_layout.addLayout(server_address_layout)
        server_info_layout.addLayout(server_port_layout)

        server_info_box.setLayout(server_info_layout)

        certificate_file_layout.addWidget(certificate_file_label)
        certificate_file_layout.addWidget(self.certificate_file_input)
        certificate_file_layout.addWidget(certificate_file_button)

        key_file_layout.addWidget(key_file_label)
        key_file_layout.addWidget(self.key_file_input)
        key_file_layout.addWidget(key_file_button)

        ssl_box_layout.addLayout(certificate_file_layout)
        ssl_box_layout.addLayout(key_file_layout)

        ssl_box.setLayout(ssl_box_layout)

        database_box_layout.addWidget(view_database_button)
        database_box_layout.addWidget(import_database_button)
        database_box_layout.addWidget(export_database_button)
        database_box_layout.addWidget(clear_database_button)

        database_box.setLayout(database_box_layout)

        server_status_layout.addWidget(server_status_label)
        server_status_layout.addWidget(self.server_status_state)

        server_uptime_layout.addWidget(server_uptime_label)
        server_uptime_layout.addWidget(self.server_uptime_time)

        server_buttons_layout.addWidget(self.start_server_button)
        server_buttons_layout.addWidget(self.stop_server_button)

        server_control_box_layout.addLayout(server_status_layout)
        server_control_box_layout.addLayout(server_uptime_layout)
        server_control_box_layout.addLayout(server_buttons_layout)

        server_control_box.setLayout(server_control_box_layout)

        layout.addWidget(server_info_box)
        layout.addWidget(ssl_box)
        layout.addWidget(database_box)
        layout.addWidget(server_control_box)

        self.fill_certificate_inputs(self.files)

    def fill_certificate_inputs(self, files):
        for file_path in files:
            if file_path.endswith(".crt"):
                self.certificate_file_input.setText(file_path)
            elif file_path.endswith(".key"):
                self.key_file_input.setText(file_path)

    def send_file_path(self, file_type):
        if file_type == ".crt":
            file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "Certificate files (*.crt)")
        elif file_type == ".key":
            file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "Key files (*.key)")

        if not file_path:
            return

        copied_file_path = copy_to_data_dir(file_path)

        if file_type == ".crt":
            self.certificate_file_input.setText(copied_file_path)
        else:
            self.key_file_input.setText(copied_file_path)

    def start_server(self):
        if not server_info(self.server_address_input.text(), self.server_port_input.text()):
            return
        start_receive_connection_thread(self.update_timer)
        self.server_status_state.setText("Running")
        self.start_server_button.setEnabled(False)
        self.stop_server_button.setEnabled(True)

    def stop_server(self):
        stop_receive_connection_thread()
        self.server_status_state.setText("Stopped")
        self.start_server_button.setEnabled(True)
        self.stop_server_button.setEnabled(False)
    
    def update_timer(self, seconds):
        self.server_uptime_time.setText(str(seconds))