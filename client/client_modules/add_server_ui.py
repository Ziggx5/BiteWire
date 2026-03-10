from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from client_modules.data_manipulation import save_server_data
from client_modules.load_servers import server_loader
from client_modules.networking import ChatHandler

class AddServerUi(QWidget):
    def __init__(self, on_cancel):
        super().__init__()

        self.setWindowTitle("BitWire")
        self.setStyleSheet("background-color: #161b22")
        self.setFixedSize(500, 300)

        self.on_cancel = on_cancel
        self.stacked = QStackedLayout(self)
        self.chat_handler = ChatHandler(self)

        self.add_server_page = QWidget()
        add_server_layout = QVBoxLayout(self.add_server_page)
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
        server_name_title.setFont(QFont("Courier New", 12))
        server_name_title.setFixedHeight(30)
        server_name_title.setStyleSheet("color: #a5a8ad;")

        server_address_title = QLabel("Server address")
        server_address_title.setFont(QFont("Courier New", 12))
        server_address_title.setFixedHeight(30)
        server_address_title.setStyleSheet("color: #a5a8ad;")

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

        self.confirm_add_server_button = QPushButton("Confirm")
        self.confirm_add_server_button.setFixedSize(110, 35)
        self.confirm_add_server_button.setStyleSheet(confirm_button_style)
        self.confirm_add_server_button.clicked.connect(self.add_server_check_entries)

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

        self.register_page = QWidget()
        register_layout = QVBoxLayout(self.register_page)
        register_layout.setSpacing(0)

        register_option_buttons_layout = QHBoxLayout()

        register_top_line = QFrame()
        register_top_line.setFrameShape(QFrame.HLine)
        register_top_line.setStyleSheet("color: #30363d;")

        register_bot_line = QFrame()
        register_bot_line.setFrameShape(QFrame.HLine)
        register_bot_line.setStyleSheet("color: #30363d;")

        register_label = QLabel("Register")
        register_label.setFixedHeight(30)
        register_label.setStyleSheet(main_title)

        register_subtitle = QLabel("Enter username and password")
        register_subtitle.setFixedHeight(20)
        register_subtitle.setStyleSheet("color: #8b949e; font-size: 13px;")

        username_label = QLabel("Username")
        username_label.setFont(QFont("Courier New", 12))
        username_label.setFixedHeight(30)
        username_label.setStyleSheet("color: #a5a8ad;")

        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(40)

        self.username_input.setStyleSheet(input_style)

        password_label = QLabel("Password")
        password_label.setFont(QFont("Courier New", 12))
        password_label.setFixedHeight(30)
        password_label.setStyleSheet("color: #a5a8ad;")

        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet(input_style)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.cancel_register = QPushButton("Cancel")
        self.cancel_register.setStyleSheet(cancel_button_style)
        self.cancel_register.clicked.connect(self.reset)
        self.cancel_register.setFixedSize(110, 35)

        self.confirm_register = QPushButton("Confirm")
        self.confirm_register.setStyleSheet(confirm_button_style)
        self.confirm_register.clicked.connect(self.register_check_entries)
        self.confirm_register.setFixedSize(110, 35)

        register_option_buttons_layout.addStretch()
        register_option_buttons_layout.addWidget(self.cancel_register)
        register_option_buttons_layout.addSpacing(10)
        register_option_buttons_layout.addWidget(self.confirm_register)

        register_layout.addWidget(register_label)
        register_layout.addWidget(register_subtitle)
        register_layout.addSpacing(10)
        register_layout.addWidget(register_top_line)
        register_layout.addSpacing(10)
        register_layout.addWidget(username_label)
        register_layout.addWidget(self.username_input)
        register_layout.addSpacing(10)
        register_layout.addWidget(password_label)
        register_layout.addWidget(self.password_input)
        register_layout.addStretch()
        register_layout.addWidget(register_bot_line)
        register_layout.addSpacing(10)
        register_layout.addLayout(register_option_buttons_layout)
        self.stacked.addWidget(self.register_page)

    def add_server_check_entries(self):
        self.name = self.server_name_input.text()
        self.ip_address = self.ip_address_input.text()

        if self.name and self.ip_address:
            self.stacked.setCurrentWidget(self.register_page)
            server_loader()
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Please enter server name and IP address."
            )

    def register_check_entries(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            try:
                return_message = self.chat_handler.register(username, password, self.ip_address)
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Server is not online. \n{str(e)}"
                )
                return
            if return_message["type"] == "register" and return_message["status"] == "ok":
                save_server_data(self.name, self.ip_address)
                self.reset()
                self.stacked.setCurrentWidget(self.add_server_page)
                self.close()
            elif return_message["type"] == "register" and return_message["status"] == "fail":
                QMessageBox.warning(
                self,
                "Error",
                "Username already taken, try another one."
                )
            else:
                QMessageBox.warning(
                self,
                "Error",
                f"Something went wrong, try again.\n {return_message}"
                )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Please enter username and password."
            )
    
    def reset(self):
        self.stacked.setCurrentWidget(self.add_server_page)
        self.server_name_input.clear()
        self.ip_address_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.on_cancel()