from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap
from client_modules.add_server_ui import AddServerUi
from client_modules.load_servers import server_loader
from client_modules.save_server import delete_server
from client_modules.networking import ChatHandler
from client_modules.tray_manager import TrayManager
from client_modules.path_finder import file_root
from client_modules.login_ui import Login

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.active_server = None

        self.add_server_window = AddServerUi(self.add_server_window_show_main_ui)
        self.chat_handler = ChatHandler(self.client_display_message)
        self.login_server_window = Login(self.login_server_window_show_main_ui, self.on_success_login, self.chat_handler)
        self.tray = TrayManager(self)
        image_path = file_root()

        self.setWindowTitle("BitWire")
        self.setStyleSheet("background-color : #0e1117;")
        self.setFixedSize(900, 600)

        self.server_frame = QFrame(self)
        self.server_frame.setGeometry(0, 100, 200, 450)
        self.server_frame.setStyleSheet("background: #1a1a24; border-right: 1px solid #30363d")

        self.server_layout = QVBoxLayout(self.server_frame)
        self.server_layout.setAlignment(Qt.AlignTop)
        self.server_layout.setSpacing(3)

        self.user_frame = QFrame(self)
        self.user_frame.setGeometry(0, 550, 200, 50)

        self.user_frame_layout = QHBoxLayout(self.user_frame)

        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(200, 0, 700, 600)
        self.main_frame.setStyleSheet("background: transparent; border: 1px solid #737373")

        self.main_layout = QVBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)

        self.upper_frame = QFrame(self)
        self.upper_frame.setGeometry(0, 50, 200, 50)
        self.upper_frame.setStyleSheet("background: #232338; border-right: 1px solid #30363d")

        self.upper_layout = QHBoxLayout(self.upper_frame)

        self.logo_frame = QFrame(self)
        self.logo_frame.setGeometry(0, 0, 200, 50)
        self.logo_frame.setStyleSheet("background: transparent; border-right: 1px solid #30363d")

        self.logo_layout = QHBoxLayout(self.logo_frame)

        self.server_button_group = QButtonGroup(self)
        self.server_button_group.setExclusive(True)

        self.bitwire_label = QLabel("BitWire")
        self.bitwire_label.setFont(QFont("Courier New", 17))
        self.bitwire_label.setStyleSheet("color: #a5a8ad; border: none")
        
        self.logo_layout.addWidget(self.bitwire_label, alignment = Qt.AlignCenter)

        self.add_server_label = QLabel("All servers")
        self.add_server_label.setFont(QFont("Courier New", 11))
        self.add_server_label.setStyleSheet("color: white; border: none")

        self.add_button = QPushButton("+")
        self.add_button.setFont(QFont("Courier New", 15))
        self.add_button.setStyleSheet("""
            QPushButton {
            color: white;
            background-color: #1f6feb;
            border-radius: 10px;
            font-weight: 700;
            border: 2px solid #ffffff;
            }
            
            QPushButton:hover {
                border-color: #58a6ff;
            }

            QPushButton:pressed {
            background-color: #1a5fd1;
            border-color: #1a5fd1;
            }
            
        """)
        self.add_button.setFixedSize(40, 32)
        self.add_button.clicked.connect(self.open_add_server)
        self.reload_servers()

        self.upper_layout.addWidget(self.add_server_label)
        self.upper_layout.addStretch()
        self.upper_layout.addWidget(self.add_button)

        self.username_label = QLabel("User")

        self.new_user_button = QPushButton("+")
        self.new_user_button.setFixedSize(30, 30)
        self.new_user_button.setStyleSheet("font-weight: 500; font-size: 15px")

        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(f"{image_path}/settings.png"))
        self.settings_button.setIconSize(QSize(18, 18))
        self.settings_button.setFixedSize(30, 30)

        self.user_picture = QLabel()
        self.user_picture.setFixedSize(30, 30)
        self.user_picture.setStyleSheet("background-color: white; border-radius: 15px")
        self.pixmap = QPixmap(f"{image_path}/user_picture_placeholder.png")
        self.pixmap = self.pixmap.scaled(30, 30, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.user_picture.setPixmap(self.pixmap)
        self.user_frame_layout.addWidget(self.user_picture)
        self.user_frame_layout.addWidget(self.username_label)
        self.user_frame_layout.addWidget(self.new_user_button)
        self.user_frame_layout.addWidget(self.settings_button)

    def open_add_server(self):
        self.add_server_window.show()
        self.hide()

    def add_server_window_show_main_ui(self):
        self.add_server_window.close()
        self.show()
        self.reload_servers()

    def login_server_window_show_main_ui(self):
        self.login_server_window.close()
        self.show()
        self.reload_servers()

    def reload_servers(self):
        while self.server_layout.count():
            item = self.server_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        server_list = server_loader()
        for server in server_list:
            server_button = ServerButton(server["name"], server["ip_address"], self.login_page, self.server_delete_data)
            self.server_layout.addWidget(server_button)

    def client_display_message(self, message):
        self.chat_view.append(message)

    def client_send_message(self):
        message = self.message_input.toPlainText().strip()
        if not message:
            self.message_input.setFocus()
            return
        self.chat_handler.send_message(message)
        self.message_input.clear()
        self.message_input.setFocus()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def login_page(self, item):
        self.server_address = item.ip
        self.login_server_window.get_ip_address(self.server_address)
        self.login_server_window.show() 
        self.hide()
    
    def on_success_login(self, username, ip_address):
        self.chat_view = QTextBrowser()
        self.chat_view.verticalScrollBar().setSingleStep(10)
        self.chat_view.setStyleSheet("""
            QTextBrowser {
                background-color: #0d1117;
                color: #e6edf3;
                padding: 10px;
                font-size: 14px;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 15px;
                border-radius: 6px;
            }

            QScrollBar:handle:vertical {
                background-color: #333e4f;
                border-radius: 6px;
            }

            QScrollBar:handle:vertical:hover {
                background-color: #4d5d75;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background-color: transparent;
                border: transparent;
            }
        """)

        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(40)
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.setStyleSheet("""
            QTextEdit {
                border-radius: 10px;
                background-color: #1a1e24;
                color: #e6edf3;
                padding: 5px 5px;
                border: 1px solid #3b4657;
            }

            QTextEdit:focus {
                border: 1px solid #505f75;
            }
        """)

        self.send_message = QPushButton(">")
        self.send_message.setFixedSize(30, 30)
        self.send_message.clicked.connect(self.client_send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_message)

        self.main_layout.addWidget(self.chat_view)
        self.main_layout.addLayout(input_layout)
        self.message_input.setFocus()

    def server_delete_data(self, item):
        self.server_address = item.ip
        delete_server(self.server_address)
        self.reload_servers()

class ServerButton(QFrame):
    def __init__(self, name, ip, on_click, on_delete):
        super().__init__()

        self.name = name
        self.ip = ip
        self.on_click = on_click
        self.on_delete = on_delete

        self.setFixedHeight(40)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e2f;
                border-radius: 10px;
                border: 1px solid #3f3f4a;
            }

            QFrame:hover {
                background-color: #333333;
            }
        """)

        layout = QHBoxLayout(self)

        self.label = QLabel(name)
        self.label.setFixedWidth(130)
        self.label.setFont(QFont("Courier New", 13))
        self.label.setStyleSheet("""
            QLabel {
                color: #a5a8ad;
                border: none;
                background: transparent
            }
        """)

        self.delete_button = QPushButton("X")
        self.delete_button.setFixedSize(20, 20)
        self.delete_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #1e1e2f;
                background: transparent
            }

            QPushButton:hover {
                color: white;
                border: 1px solid white;
                border-radius: 5px
            }
        """)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.delete_button)

        self.mousePressEvent = self.frame_clicked
        self.delete_button.clicked.connect(self.delete_button_clicked)
    
    def frame_clicked(self, event):
        self.on_click(self)

    def delete_button_clicked(self):
        self.on_delete(self)