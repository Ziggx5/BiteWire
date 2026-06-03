from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import base64
from client_modules.add_server_ui import AddServerUi
from client_modules.data_manipulation import delete_server, server_loader
from client_modules.networking import ChatHandler
from client_modules.tray_manager import TrayManager
from client_modules.path_finder import file_root
from client_modules.login_ui import Login
from client_modules.update_checker import UpdateChecker
from client_modules.profile_cache import ProfileCache

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BiteWire")
        self.setStyleSheet("""
        QWidget {
            background-color: #0e1117;
        }
        
        QScrollBar:vertical {
            background-color: transparent;
            width: 6px;
        }

        QScrollBar::handle:vertical {
            background-color: #374151;     
            border-radius: 3px;      
        }

        QScrollBar::handle:vertical:hover {
            background-color: #4b5563;
        }
        """)
        self.showMaximized()

        self.image_path = file_root()
        self.profile_cache = ProfileCache()
        self.add_server_window = AddServerUi(self.add_server_window_show_main_ui)
        self.chat_handler = ChatHandler(self.profile_cache)
        self.login_server_window = Login(self.login_server_window_show_main_ui, self.on_success_login, self.chat_handler)
        self.tray = TrayManager(self)
        self.update_checker = UpdateChecker(self.image_path, self.update_window_show_main_ui)

        self.chat_handler.message_received.connect(self.client_display_message)
        self.chat_handler.users_received.connect(self.add_users)
        self.chat_handler.server_status.connect(self.server_close_message)
        self.update_checker.update_found.connect(self.update_button_updater)
        self.profile_cache.profile_picture.connect(self.update_profile_pictures)

        self.user_widgets = {}
        self.current_server_ip = None

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        self.overlay.setGeometry(0, 0, self.width(), self.height())

        self.overlay_layout = QVBoxLayout(self.overlay)

        popup_background_container = QWidget()
        popup_background_container.setObjectName("container")
        popup_background_container.setStyleSheet("""
            QWidget#container {
                    background-color: #161b22;
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)
        self.popup_background_container_layout = QVBoxLayout(popup_background_container)

        self.overlay_layout.addWidget(popup_background_container, alignment = Qt.AlignCenter)

        main_root_layout = QHBoxLayout(self)
        main_root_layout.setSpacing(0)
        main_root_layout.setContentsMargins(0, 0, 0, 0)

        left_container = QVBoxLayout()

        server_frame = QFrame(self)
        server_frame.setStyleSheet("background-color: #111827; border: none;")

        self.server_layout = QVBoxLayout(server_frame)
        self.server_layout.setAlignment(Qt.AlignTop)
        self.server_layout.setSpacing(3)

        user_frame = QFrame(self)
        user_frame.setObjectName("container")
        user_frame.setStyleSheet("""
            QFrame#container {
                background: transparent;
                border: 1px solid #30363d;
            }
        """)
        self.user_frame_layout = QHBoxLayout(user_frame)

        main_frame = QFrame(self)
        main_frame.setStyleSheet("background: transparent; border: none;")

        self.main_layout_horizontal = QHBoxLayout(main_frame)
        self.main_layout_horizontal.setContentsMargins(0, 0, 0, 0)

        self.main_layout_vertical = QVBoxLayout()
        self.main_layout_vertical.setSpacing(8)
        self.main_layout_horizontal.addLayout(self.main_layout_vertical)

        upper_frame = QFrame(self)
        upper_frame.setStyleSheet("background-color: #111827; border-bottom: 1px solid rgba(255, 255, 255, 0.05);")

        self.upper_layout = QHBoxLayout(upper_frame)

        logo_frame = QFrame(self)
        logo_frame.setStyleSheet("background: #111827; border: none;")

        self.logo_layout = QHBoxLayout(logo_frame)

        self.BiteWire_label = QLabel("BiteWire")
        self.BiteWire_label.setStyleSheet("color: #a5a8ad; border: none; font-size: 30px;")
        
        self.logo_layout.addWidget(self.BiteWire_label, alignment = Qt.AlignCenter)

        self.add_server_label = QLabel("All servers")
        self.add_server_label.setStyleSheet("color: white; border: none; font-size: 17px;")

        self.add_button = QPushButton()
        self.add_button.setIcon(QIcon(f"{self.image_path}/plus.png"))
        self.add_button.setIconSize(QSize(15, 15))
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                border-radius: 8px;
                border: 2px solid #ffffff;
            }
            
            QPushButton:hover {
                background-color: #2563eb;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        self.add_button.setFixedSize(35, 35)
        self.add_button.clicked.connect(lambda: self.show_popup(self.add_server_window))
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.reload_servers()

        self.upper_layout.addWidget(self.add_server_label)
        self.upper_layout.addStretch()
        self.upper_layout.addWidget(self.add_button)

        self.username_label = QLabel("User")

        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(f"{self.image_path}/settings.png"))
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }

            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)

        self.settings_button.setIconSize(QSize(18, 18))
        self.settings_button.setFixedSize(30, 30)
        self.settings_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.user_picture = QLabel()
        self.user_picture.setFixedSize(30, 30)
        self.user_picture.setStyleSheet("background-color: white; border-radius: 15px")
        self.user_pixmap = QPixmap(f"{self.image_path}/user_picture_placeholder.png").scaled(30, 30, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.user_picture.setPixmap(self.user_pixmap)

        self.update_client_button = QPushButton()
        self.update_client_button.setFixedSize(30, 30)
        self.update_client_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_client_button.setIcon(QIcon(f"{self.image_path}/update.png"))
        self.update_client_button.setIconSize(QSize(18, 18))
        self.update_client_button.setVisible(False)
        self.update_client_button.clicked.connect(lambda: self.show_popup(self.update_checker))
        self.update_client_button.setStyleSheet("""
            QPushButton {
                background-color: #f59e0b;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: #d97706;
            }

            QPushButton:pressed {
                background-color: #b45309;
            }
        """)
        self.update_checker.check_update()

        self.user_frame_layout.addWidget(self.user_picture)
        self.user_frame_layout.addWidget(self.username_label)
        self.user_frame_layout.addWidget(self.update_client_button)
        self.user_frame_layout.addWidget(self.settings_button)

        left_container.addWidget(logo_frame)
        left_container.addWidget(upper_frame)
        left_container.addWidget(server_frame, 1)
        left_container.addWidget(user_frame)

        main_root_layout.addLayout(left_container, 1)
        main_root_layout.addWidget(main_frame, 5)

    def add_server_window_show_main_ui(self):
        self.add_server_window.hide()
        self.overlay.hide()
        self.reload_servers()

    def login_server_window_show_main_ui(self):
        self.login_server_window.hide()
        self.overlay.hide()
        self.reload_servers()
    
    def update_window_show_main_ui(self):
        self.update_checker.hide()
        self.overlay.hide()

    def reload_servers(self):
        while self.server_layout.count():
            item = self.server_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        server_list = server_loader()
        for server in server_list:
            server_button = ServerButton(server["name"], server["ip_address"], self.login_page_popup, self.server_delete_data)
            if server['ip_address'] == self.current_server_ip:
                server_button.connected_server()
            self.server_layout.addWidget(server_button)

    def client_display_message(self, username, content, time):
        cached_picture = self.profile_cache.get(username, "message_profile_picture")

        if cached_picture:
            message_widget = MessageWidget(username, content, time, cached_picture)
        else:
            message_widget = MessageWidget(username, content, time, f"{self.image_path}/user_picture_placeholder.png")

        self.chat_layout.addWidget(message_widget)
        QTimer.singleShot(5, lambda: self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()))

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

    def login_page_popup(self, item):
        server_address = item.ip
        server_name = item.name
        self.login_server_window.get_server_info(server_address, server_name)
        self.show_popup(self.login_server_window)
    
    def on_success_login(self, username, server_name):
        self.username_label.setText(username)
        self.current_server_ip = self.login_server_window.ip_address
        self.reload_servers()

        header = QFrame()
        header.setObjectName("header_container")
        header.setStyleSheet("""
            QFrame#header_container {
                background-color: #161b22;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)
        header.setFixedHeight(45)

        header_layout = QHBoxLayout(header)

        self.server_name_label = QLabel(server_name)
        self.server_name_label.setStyleSheet("""
            color: #e6edf3;
            font-size: 16px;
            font-weight: 600;
        """)

        self.disconnect_button = QPushButton()
        self.disconnect_button.setIcon(QIcon(f"{self.image_path}/leave_server.png"))
        self.disconnect_button.setIconSize(QSize(20, 20))
        self.disconnect_button.setFixedSize(30, 30)
        self.disconnect_button.setCursor(Qt.PointingHandCursor)
        self.disconnect_button.clicked.connect(self.disconnect_button_handler)
        self.disconnect_button.setStyleSheet("""
        QPushButton {
                background-color: transparent;
                border-radius: 8px;
            }
        
        QPushButton:hover {
            background-color: #dc2626;
        }

        QPushButton:pressed {
            background-color: #991b1b;
        }
        """)

        self.connection_status_label = QLabel("Connected")
        self.connection_status_label.setStyleSheet("""
            QLabel {
                color: #e6edf3;
                font-size: 12px;
                font-weight: 400;
            }
        """)

        self.status_icon = QLabel()
        pixmap = QPixmap(f"{self.image_path}/online.png").scaled(20, 20, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.status_icon.setPixmap(pixmap)
        self.status_icon.setFixedSize(20, 20)

        header_layout.addWidget(self.server_name_label)
        header_layout.addStretch()
        header_layout.addWidget(self.status_icon)
        header_layout.addWidget(self.connection_status_label)
        header_layout.addSpacing(30)
        header_layout.addWidget(self.disconnect_button)

        self.chat_container = QFrame()

        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setSpacing(12)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        self.scroll = QScrollArea()
        self.scroll.setStyleSheet("border: none;")
        self.scroll.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.chat_container)

        scroll_container = QWidget()
        scroll_container.setStyleSheet("border: none;")
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(12, 12, 12, 12)

        scroll_layout.addWidget(self.scroll)

        input_container = QFrame()
        input_container.setFixedHeight(60)
        input_container.setStyleSheet("""
            QFrame {
                    border-radius: 10px;
                    border: 1px solid #1e293b;
                    background-color: #0f172a;
            }
        """)

        input_layout = QHBoxLayout(input_container)
        input_layout.setSpacing(5)

        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(30)
        self.message_input.setStyleSheet("""
        QTextEdit {
            color: #e6edf3; 
            border: none;
        }
        """)
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.installEventFilter(self)

        file_button = QPushButton()
        file_button.setIcon(QIcon(f"{self.image_path}/paperclip.png"))
        file_button.setFixedSize(40, 40)
        file_button.setCursor(Qt.PointingHandCursor)

        emoji_button = QPushButton()
        emoji_button.setIcon(QIcon(f"{self.image_path}/emoji.png"))
        emoji_button.setIconSize(QSize(20, 20))
        emoji_button.setFixedSize(40, 40)
        emoji_button.setCursor(Qt.PointingHandCursor)

        send_button = QPushButton()
        send_button.setIcon(QIcon(f"{self.image_path}/send.png"))
        send_button.setFixedSize(40, 40)
        send_button.clicked.connect(self.client_send_message)
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        send_button.setCursor(Qt.PointingHandCursor)

        input_layout.addWidget(self.message_input, 1)
        input_layout.addWidget(file_button)
        input_layout.addWidget(emoji_button)
        input_layout.addWidget(send_button)

        chat_wrapper = QFrame()

        chat_wrapper_layout = QVBoxLayout(chat_wrapper)
        chat_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        chat_wrapper_layout.setSpacing(0)
        
        chat_wrapper_layout.addWidget(header)
        chat_wrapper_layout.addWidget(scroll_container)
        chat_wrapper_layout.addWidget(input_container)

        all_users_wrapper = QFrame()
        all_users_wrapper.setObjectName("all_users_wrapper")
        all_users_wrapper.setStyleSheet("""
            QFrame#all_users_wrapper {
                border-left: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)

        all_users_wrapper_layout = QVBoxLayout(all_users_wrapper)

        all_users_container = QWidget()

        self.all_users_layout = QVBoxLayout(all_users_container)
        self.all_users_layout.setSpacing(5)
        self.all_users_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        all_users_label_container = QWidget()
        all_users_label_layout = QHBoxLayout(all_users_label_container)
        all_users_label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        all_users_label = QLabel("All members")
        all_users_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.6);
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
            }
        """)

        all_users_label_layout.addWidget(all_users_label)

        all_users_scroll = QScrollArea()
        all_users_scroll.setWidget(all_users_container)
        all_users_scroll.setWidgetResizable(True)

        all_users_wrapper_layout.addWidget(all_users_label_container, 1)
        all_users_wrapper_layout.addWidget(all_users_scroll, 30)

        self.main_layout_horizontal.addWidget(chat_wrapper, 5)
        self.main_layout_horizontal.addWidget(all_users_wrapper, 1)
        self.message_input.setFocus()

    def server_delete_data(self, item):
        self.server_address = item.ip
        delete_server(self.server_address)
        self.reload_servers()

    def show_popup(self, widget):
        while self.popup_background_container_layout.count():
            item = self.popup_background_container_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        self.popup_background_container_layout.addWidget(widget)
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.raise_()
        self.overlay.show()
        widget.show()

    def add_users(self, users):
        while self.all_users_layout.count():
            item = self.all_users_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
        for user in users:
            if user['status']:
                user_widget = UserWidget(user['username'], f"{self.image_path}/user_picture_placeholder.png", "Online")
            else:
                user_widget = UserWidget(user['username'], f"{self.image_path}/user_picture_placeholder.png", "Offline")

            self.all_users_layout.addWidget(user_widget)

            self.user_widgets[user['username']] = user_widget
    
    def eventFilter(self, obj, event):
        if obj == self.message_input and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.client_send_message()
                return True
        return False     

    def server_close_message(self, message):
        QMessageBox.warning(self, "Server Message", message)
        self.message_input.setEnabled(False)
        pixmap = QPixmap(f"{self.image_path}/disconnected.png").scaled(20, 20, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.status_icon.setPixmap(pixmap)
        self.connection_status_label.setText("Disconnected")

    def disconnect_button_handler(self):
        self.chat_handler.handle_disconnect()
        self.message_input.setEnabled(False)
        pixmap = QPixmap(f"{self.image_path}/disconnected.png").scaled(20, 20, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.status_icon.setPixmap(pixmap)
        self.connection_status_label.setText("Disconnected")

    def on_scroll(self):
        scrollbar = self.scroll.verticalScrollBar()

        if scrollbar.value() == scrollbar.minimum():
            print("send message history")

    def update_button_updater(self, update):
        if update:
            self.update_client_button.setVisible(True)

    def update_profile_pictures(self, username):
        picture = self.profile_cache.get(username, "list_profile_picture")

        if picture:
            self.user_widgets[username].set_profile_picture(picture)

        if username == self.username_label.text():
            self.user_picture.setPixmap(picture)

class ServerButton(QFrame):
    def __init__(self, name, ip, on_click, on_delete):
        super().__init__()

        self.name = name
        self.ip = ip
        self.on_click = on_click
        self.on_delete = on_delete

        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e2f;
                border-radius: 10px;
                border: 1px solid #3f3f4a;
            }

            QFrame:hover {
                background-color: #333333;
            }

            QFrame[current_server="true"] {
                background-color: #333333;
            }
        """)

        layout = QHBoxLayout(self)

        self.label = QLabel()
        self.label.setFixedWidth(180)
        self.label.setStyleSheet("""
            QLabel {
                color: #a5a8ad;
                border: none;
                background: transparent;
                font-size: 15px;
            }
        """)

        self.resize_server_name()

        self.delete_button = QPushButton("X")
        self.delete_button.setFixedSize(20, 20)
        self.delete_button.setVisible(False)
        self.delete_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #8c8c8c;
                background: transparent;
            }

            QPushButton:hover {
                color: #bababa;
            }
        """)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.delete_button)

        self.mousePressEvent = self.frame_clicked
        self.delete_button.clicked.connect(self.delete_button_clicked)
    
    def resize_server_name(self):
        metrics = QFontMetrics(self.label.font())
        resize_name = metrics.elidedText(self.name, Qt.ElideRight, self.label.width())
        self.label.setText(resize_name)

    def frame_clicked(self, event):
        self.on_click(self)

    def delete_button_clicked(self):
        self.on_delete(self)

    def enterEvent(self, event):
        self.delete_button.setVisible(True)

    def leaveEvent(self, event):
        self.delete_button.setVisible(False)

    def connected_server(self):
        self.setProperty("current_server", True)
        self.setEnabled(False)

class MessageWidget(QWidget):
    def __init__(self, username, data, time, image):
        super().__init__() 
        self.setObjectName("message_container")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #message_container {
                background-color: #111827;
                border-radius: 12px;
            }
        """)

        layout = QHBoxLayout(self)
        
        icon = QLabel()
        icon.setStyleSheet("background-color: transparent; border: none;")
        icon.setFixedSize(35, 35)

        pixmap = QPixmap(image).scaled(35, 35, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        mask = QBitmap(35, 35)
        mask.fill(Qt.color0)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, 35, 35)
        painter.end()
        pixmap.setMask(mask)
        icon.setPixmap(pixmap)

        right_layout = QVBoxLayout()

        left_layout = QVBoxLayout()

        top_row = QHBoxLayout()

        username = QLabel(username)
        username.setStyleSheet("color: #58a6ff; font-weight: 500; font-size: 15px;")

        time = QLabel(time)
        time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time.setStyleSheet("color: #58a6ff; font-weight: 500; font-size: 11px;")

        message = QTextBrowser()
        message.setReadOnly(True)
        message.setText(data)
        message.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        message.setOpenExternalLinks(True)
        message.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        message.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        message.setStyleSheet("color: #e6edf3;")

        QTimer.singleShot(1, lambda: self.adjust_message_height(message))

        right_layout.addLayout(top_row)
        right_layout.addWidget(message)

        left_layout.addWidget(icon, alignment = Qt.AlignTop)

        top_row.addWidget(username, alignment = Qt.AlignmentFlag.AlignCenter)
        top_row.addWidget(time, alignment = Qt.AlignmentFlag.AlignCenter)
        top_row.addStretch()

        layout.addLayout(left_layout)
        layout.addSpacing(10)
        layout.addLayout(right_layout)
    
    def adjust_message_height(self, message):
        message.document().setTextWidth(message.viewport().width())
        message_height = message.document().size().height()
        message.setFixedHeight(int(message_height))

class UserWidget(QWidget):
    def __init__(self, username, image, status):
        super().__init__()

        self.username = username

        self.setObjectName("userwidget")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setStyleSheet("""
            #userwidget {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 5px; 
                border: none;           
            }

            #userwidget:hover {
                background-color: #1f2933;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(8, 8, 8, 8)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)

        self.icon = QLabel("icon")
        self.icon.setStyleSheet("background-color: transparent; border: none;")
        self.icon.setFixedSize(30, 30)

        pixmap = QPixmap(image).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        mask = QBitmap(30, 30)
        mask.fill(Qt.color0)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, 30, 30)
        painter.end()

        pixmap.setMask(mask)

        self.icon.setPixmap(pixmap)

        username_label = QLabel(self.username)
        username_label.setStyleSheet("font-size: 15px; border: none;")

        status_label = QLabel(status)

        text_layout.addWidget(username_label)
        text_layout.addWidget(status_label)

        main_layout.addWidget(self.icon)
        main_layout.addLayout(text_layout)

    def set_profile_picture(self, pixmap):
        self.icon.setPixmap(pixmap)