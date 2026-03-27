from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from client_modules.networking import ChatHandler

class Login(QWidget):
    def __init__(self, on_cancel, on_success, chat_handler):
        super().__init__()

        self.on_cancel = on_cancel
        self.on_success = on_success
        self.chat_handler = chat_handler

        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: transparent;")

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

        login_page_layout = QVBoxLayout(self)
        login_page_layout.setContentsMargins(10, 10, 10, 10)
        login_page_layout.setSpacing(0)

        option_buttons = QHBoxLayout()

        top_line = QFrame()
        top_line.setFrameShape(QFrame.HLine)
        top_line.setStyleSheet("color: #30363d;")

        bot_line = QFrame()
        bot_line.setFrameShape(QFrame.HLine)
        bot_line.setStyleSheet("color: #30363d;")

        login_title = QLabel("Login")
        login_title.setFixedHeight(30)
        login_title.setStyleSheet("""
            QLabel {
                color: #e6edf3;
                font-size: 20px;
                font-weight: 600;
            }
        """)

        subtitle = QLabel("Enter user details")
        subtitle.setFixedHeight(20)
        subtitle.setStyleSheet("color: #8b949e; font-size: 13px;")

        username_title = QLabel("Username")
        username_title.setFixedHeight(30)
        username_title.setStyleSheet("color: #a5a8ad; font-size: 15px;")

        password_title = QLabel("Password")
        password_title.setFixedHeight(30)
        password_title.setStyleSheet("color: #a5a8ad; font-size: 15px;")

        self.username_input = QLineEdit(self)
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet(input_style)

        self.password_input = QLineEdit(self)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet(input_style)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.cancel = QPushButton("Cancel")
        self.cancel.setStyleSheet(cancel_button_style)
        self.cancel.setFixedSize(110, 35)
        self.cancel.clicked.connect(self.reset)

        self.confirm = QPushButton("Confirm")
        self.confirm.setStyleSheet(confirm_button_style)
        self.confirm.setFixedSize(110, 35)
        self.confirm.clicked.connect(self.login_check_entries)

        option_buttons.addStretch()
        option_buttons.addWidget(self.cancel)
        option_buttons.addSpacing(10)
        option_buttons.addWidget(self.confirm)

        login_page_layout.addWidget(login_title)
        login_page_layout.addWidget(subtitle)
        login_page_layout.addSpacing(10)
        login_page_layout.addWidget(top_line)
        login_page_layout.addSpacing(10)
        login_page_layout.addWidget(username_title)
        login_page_layout.addWidget(self.username_input)
        login_page_layout.addSpacing(10)
        login_page_layout.addWidget(password_title)
        login_page_layout.addWidget(self.password_input)
        login_page_layout.addStretch()
        login_page_layout.addWidget(bot_line)
        login_page_layout.addSpacing(10)
        login_page_layout.addLayout(option_buttons)

    def login_check_entries(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if username and password:
            try:
                return_message = self.chat_handler.login(username, password, self.ip_address)
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Server is not online. \n{str(e)}"
                )
                return
            if return_message["type"] == "login" and return_message["status"] == "ok":
                self.on_success(username, self.ip_address)
                self.on_cancel()
                self.close()
            elif return_message["type"] == "login" and return_message["status"] == "fail":
                QMessageBox.warning(
                    self,
                    "Error",
                    "Incorrect username or password."
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

    def get_ip_address(self, ip_address):
        self.ip_address = ip_address
    
    def reset(self):
        self.username_input.clear()
        self.password_input.clear()
        self.on_cancel()