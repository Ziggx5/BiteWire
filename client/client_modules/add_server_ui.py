from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from client_modules.save_server import save_server_data
from client_modules.load_servers import server_loader
from client_modules.networking import ChatHandler

class AddServerUi(QWidget):
    def __init__(self, on_cancel):
        super().__init__()

        self.on_cancel = on_cancel
        self.stacked = QStackedLayout(self)
        self.chat_handler = ChatHandler(self)

        self.add_page = QWidget()
        add_layout = QVBoxLayout(self.add_page)

        add_server_title = QLabel("Add server")
        add_server_title.setFont(QFont("Courier New", 20))
        add_server_title.setStyleSheet("color: #a5a8ad;")

        server_name_title = QLabel("Server name:")
        server_name_title.setFont(QFont("Courier New", 20))
        server_name_title.setStyleSheet("color: #a5a8ad;")

        server_address_title = QLabel("Server address:")
        server_address_title.setFont(QFont("Courier New", 20))
        server_address_title.setStyleSheet("color: #a5a8ad;")

        self.server_name_input = QLineEdit()
        self.ip_address_input = QLineEdit()

        self.cancel_server = QPushButton("Cancel")
        self.cancel_server.clicked.connect(self.reset)
        self.confirm_server = QPushButton("Confirm")
        self.confirm_server.clicked.connect(self.add_server_check_entries)

        add_layout.addWidget(add_server_title)
        add_layout.addWidget(server_name_title)
        add_layout.addWidget(self.server_name_input)
        add_layout.addWidget(server_address_title)
        add_layout.addWidget(self.ip_address_input)
        add_layout.addWidget(self.cancel_server)
        add_layout.addWidget(self.confirm_server)
        self.stacked.addWidget(self.add_page)

        self.register_page = QWidget()
        register_layout = QVBoxLayout(self.register_page)

        register_label = QLabel("Register")
        register_label.setFont(QFont("Courier New", 20))
        register_label.setStyleSheet("color: #a5a8ad;")

        username_label = QLabel("Username")
        username_label.setFont(QFont("Courier New", 20))
        username_label.setStyleSheet("color: #a5a8ad;")

        self.username_input = QLineEdit()

        password_label = QLabel("Password")
        password_label.setFont(QFont("Courier New", 20))
        password_label.setStyleSheet("color: #a5a8ad;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.cancel_register = QPushButton("Cancel")
        self.cancel_register.clicked.connect(self.reset)
        self.confirm_register = QPushButton("Confirm")
        self.confirm_register.clicked.connect(self.register_check_entries)

        register_layout.addWidget(register_label)
        register_layout.addWidget(username_label)
        register_layout.addWidget(self.username_input)
        register_layout.addWidget(password_label)
        register_layout.addWidget(self.password_input)
        register_layout.addWidget(self.cancel_register)
        register_layout.addWidget(self.confirm_register)
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
                self.stacked.setCurrentWidget(self.add_page)
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
        self.stacked.setCurrentWidget(self.add_page)
        self.server_name_input.clear()
        self.ip_address_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.on_cancel()