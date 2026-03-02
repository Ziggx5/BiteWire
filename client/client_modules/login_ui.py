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

        self.login_page = QVBoxLayout(self)

        login_label = QLabel("Login")
        login_label.setFont(QFont("Courier New", 20))
        login_label.setStyleSheet("color: #a5a8ad;")

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.cancel = QPushButton("Cancel")
        self.confirm = QPushButton("Confirm")
        self.cancel.clicked.connect(self.reset)
        self.confirm.clicked.connect(self.login_check_entries)

        self.login_page.addWidget(login_label)
        self.login_page.addWidget(self.username_input)
        self.login_page.addWidget(self.password_input)
        self.login_page.addWidget(self.cancel)
        self.login_page.addWidget(self.confirm)

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