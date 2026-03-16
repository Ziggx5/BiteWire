from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bitwire server")
        self.setStyleSheet("background-color : #0e1117;")
        self.setFixedSize(400, 500)
        
        layout = QVBoxLayout(self)

        ssl_box = QGroupBox("SSL Certificate Files")
        ssl_box_layout = QVBoxLayout()
        certificate_file_layout = QHBoxLayout()
        key_file_layout = QHBoxLayout()

        database_box = QGroupBox("Database Management")
        database_box_layout = QHBoxLayout()

        certificate_file_label = QLabel("Certificate file:")
        certificate_file_input = QLineEdit()
        certificate_file_button = QPushButton("Browse...")

        key_file_label = QLabel("Key file:")
        key_file_input = QLineEdit()
        key_file_button = QPushButton("Browse...")

        import_database_button = QPushButton("Import Database")
        export_database_button = QPushButton("Export Database")
        clear_database_button = QPushButton("Clear Database")

        certificate_file_layout.addWidget(certificate_file_label)
        certificate_file_layout.addWidget(certificate_file_input)
        certificate_file_layout.addWidget(certificate_file_button)

        key_file_layout.addWidget(key_file_label)
        key_file_layout.addWidget(key_file_input)
        key_file_layout.addWidget(key_file_button)

        ssl_box_layout.addLayout(certificate_file_layout)
        ssl_box_layout.addLayout(key_file_layout)

        ssl_box.setLayout(ssl_box_layout)

        database_box_layout.addWidget(import_database_button)
        database_box_layout.addWidget(export_database_button)
        database_box_layout.addWidget(clear_database_button)

        database_box.setLayout(database_box_layout)

        layout.addWidget(ssl_box)
        layout.addWidget(database_box)

