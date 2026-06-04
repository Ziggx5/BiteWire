from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class ChatUi(QWidget):
    own_profile_picture = Signal(object)
    def __init__(self, image_path, chat_handler, profile_cache):
        super().__init__()

        self.image_path = image_path
        self.chat_handler = chat_handler
        self.profile_cache = profile_cache
        self.username = None

        self.user_widgets = {}

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

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

        self.server_name_label = QLabel()
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

        chat_container = QFrame()

        self.chat_layout = QVBoxLayout(chat_container)
        self.chat_layout.setSpacing(12)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.scroll = QScrollArea()
        self.scroll.setStyleSheet("border: none;")
        self.scroll.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(chat_container)

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
        file_button.setIconSize(QSize(20, 20))
        file_button.setFixedSize(40, 40)
        file_button.setCursor(Qt.PointingHandCursor)

        emoji_button = QPushButton()
        emoji_button.setIcon(QIcon(f"{self.image_path}/emoji.png"))
        emoji_button.setIconSize(QSize(25, 25))
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

        main_layout.addWidget(chat_wrapper, 5)
        main_layout.addWidget(all_users_wrapper, 1)
        self.message_input.setFocus()

    def set_server_name(self, server_name):
        self.server_name_label.setText(server_name)
    
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

    def client_send_message(self):
        message = self.message_input.toPlainText().strip()
        if not message:
            self.message_input.setFocus()
            return
        self.chat_handler.send_message(message)
        self.message_input.clear()
        self.message_input.setFocus()

    def client_display_message(self, username, content, time):
        cached_picture = self.profile_cache.get(username, "message_profile_picture")

        if cached_picture:
            message_widget = MessageWidget(username, content, time, cached_picture)
        else:
            message_widget = MessageWidget(username, content, time, f"{self.image_path}/user_picture_placeholder.png")

        self.chat_layout.addWidget(message_widget)
        QTimer.singleShot(5, lambda: self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()))

    def eventFilter(self, obj, event):
        if obj == self.message_input and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.client_send_message()
                return True
        return False

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
    
    def update_profile_pictures(self, username):
        picture = self.profile_cache.get(username, "list_profile_picture")

        if picture:
            self.user_widgets[username].set_profile_picture(picture)

        if username == self.username:
            self.own_profile_picture.emit(picture)
    
    def set_username(self, username):
        self.username = username

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