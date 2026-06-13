from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from client_modules.data_manipulation import save_server_data
from client_modules.identity_ui import AddIdentityUi

class AddServerUi(QWidget):
    def __init__(self, on_cancel):
        super().__init__()
        
        self.setFixedSize(500, 350)
        self.setStyleSheet("background-color: transparent;")
        self.on_cancel = on_cancel
        self.stacked = QStackedLayout(self)
        self.register = AddIdentityUi(self.reset, self.add_server_no_register, self.reset)

        self.add_server_page = QWidget()
        add_server_layout = QVBoxLayout(self.add_server_page)
        add_server_layout.setContentsMargins(10, 10, 10, 10)
        add_server_layout.setSpacing(0)

        add_server_option_buttons = QHBoxLayout()

        add_server_top_line = QFrame()
        add_server_top_line.setFrameShape(QFrame.HLine)
        add_server_top_line.setStyleSheet("color: #30363d;")

        add_server_bot_line = QFrame()
        add_server_bot_line.setFrameShape(QFrame.HLine)
        add_server_bot_line.setStyleSheet("color: #30363d;")

        input_style = """
        QLineEdit {
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 8px;
            color: #e6edf3;
            font-size: 15px;
        }
        """

        confirm_button_style = """
        QPushButton {
            background-color: #175723;
            font-weight: 600;
            border-radius: 5px;
            border: 1px solid #30363d;
        }

        QPushButton:hover {
            background-color: #1e732e;
        }
        """

        cancel_button_style = """
        QPushButton {
            background-color: #6e6e6e;
            font-weight: 600;
            border-radius: 5px;
            border: 1px solid #30363d;
        }
        QPushButton:hover {
            background-color: #878787;
        }
        """

        main_title = """
        QLabel {
            color: #e6edf3;
            font-size: 20px;
            font-weight: 600;
        }
        """

        add_server_title = QLabel("Add server")
        add_server_title.setFixedHeight(30)
        add_server_title.setStyleSheet(main_title)

        add_server_subtitle = QLabel("Enter server details")
        add_server_subtitle.setFixedHeight(20)
        add_server_subtitle.setStyleSheet("color: #8b949e; font-size: 13px;")

        server_name_title = QLabel("Server name")
        server_name_title.setFixedHeight(30)
        server_name_title.setStyleSheet("color: #a5a8ad; font-size: 15px;")

        server_address_title = QLabel("Server address")
        server_address_title.setFixedHeight(30)
        server_address_title.setStyleSheet("color: #a5a8ad; font-size: 15px;")

        self.server_name_input = QLineEdit()
        self.server_name_input.setFixedHeight(40)
        self.server_name_input.setStyleSheet(input_style)

        self.ip_address_input = QLineEdit()
        self.ip_address_input.setFixedHeight(40)
        self.ip_address_input.setStyleSheet(input_style)

        self.cancel_add_server_button = QPushButton("Cancel")
        self.cancel_add_server_button.setStyleSheet(cancel_button_style)
        self.cancel_add_server_button.clicked.connect(self.reset)
        self.cancel_add_server_button.setFixedSize(110, 35)
        self.cancel_add_server_button.setCursor(Qt.PointingHandCursor)

        self.confirm_add_server_button = QPushButton("Confirm")
        self.confirm_add_server_button.setFixedSize(110, 35)
        self.confirm_add_server_button.setStyleSheet(confirm_button_style)
        self.confirm_add_server_button.clicked.connect(self.add_server_check_entries)
        self.confirm_add_server_button.setCursor(Qt.PointingHandCursor)

        add_server_option_buttons.addStretch()
        add_server_option_buttons.addWidget(self.cancel_add_server_button)
        add_server_option_buttons.addSpacing(10)
        add_server_option_buttons.addWidget(self.confirm_add_server_button)

        add_server_layout.addWidget(add_server_title)
        add_server_layout.addWidget(add_server_subtitle)
        add_server_layout.addSpacing(10)
        add_server_layout.addWidget(add_server_top_line)
        add_server_layout.addSpacing(10)
        add_server_layout.addWidget(server_name_title)
        add_server_layout.addWidget(self.server_name_input)
        add_server_layout.addSpacing(10)
        add_server_layout.addWidget(server_address_title)
        add_server_layout.addWidget(self.ip_address_input)
        add_server_layout.addStretch()
        add_server_layout.addWidget(add_server_bot_line)
        add_server_layout.addSpacing(10)
        add_server_layout.addLayout(add_server_option_buttons)
        self.stacked.addWidget(self.add_server_page)
        self.stacked.addWidget(self.register)

    def add_server_no_register(self):
        self.name = self.server_name_input.text()
        self.ip_address = self.ip_address_input.text()

        save_server_data(self.name, self.ip_address)
        self.reset()

    def add_server_check_entries(self):
        self.name = self.server_name_input.text()
        self.ip_address = self.ip_address_input.text()

        if self.name and self.ip_address:
            self.stacked.setCurrentWidget(self.register)
            self.register.send_ip_address(self.ip_address, self.name)

        else:
            QMessageBox.warning(
                self,
                "Error",
                "Please enter server name and IP address."
            )
    
    def reset(self):
        self.stacked.setCurrentWidget(self.add_server_page)
        self.server_name_input.clear()
        self.ip_address_input.clear()
        self.on_cancel()