import os.path

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import base64
from client_modules.add_server_ui import AddServerUi
from client_modules.data_manipulation import server_loader, save_server_icon, app_directory, update_user_count
from client_modules.networking import ChatHandler
from client_modules.tray_manager import TrayManager
from client_modules.path_finder import file_root
from client_modules.login_ui import Login
from client_modules.update_checker import UpdateChecker
from client_modules.profile_cache import ProfileCache
from client_modules.chat_ui import ChatUi

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BiteWire")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
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

        self.image_path = file_root()
        self.profile_cache = ProfileCache()
        self.add_server_window = AddServerUi(self.add_server_window_show_main_ui)
        self.chat_handler = ChatHandler(self.profile_cache)
        self.login_server_window = Login(self.login_server_window_show_main_ui, self.on_success_login, self.chat_handler)
        self.tray = TrayManager(self)
        self.update_checker = UpdateChecker(self.image_path, self.update_window_show_main_ui)
        self.chat_ui = ChatUi(self.image_path, self.chat_handler, self.profile_cache, self.clear_chat_widget)
        self.custom_title_bar = CustomTitleBar(self)

        self.chat_handler.history_message_received.connect(self.chat_ui.display_old_chat_history)
        self.chat_handler.first_history_message_received.connect(self.chat_ui.display_first_chat_history)
        self.chat_handler.message_received.connect(self.chat_ui.display_new_message)
        self.chat_handler.users_received.connect(self.chat_ui.add_users)
        self.chat_handler.server_status.connect(self.server_close_message)
        self.update_checker.update_found.connect(self.update_button_updater)
        self.profile_cache.profile_picture.connect(self.chat_ui.update_profile_pictures)
        self.chat_ui.own_profile_picture.connect(self.update_own_profile_picture)
        self.chat_handler.users_count_signal.connect(self.update_users_count)
        self.chat_handler.server_icon_signal.connect(self.update_server_icon)
        self.current_server_ip = None
        self.server_buttons = {}

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

        main_root_vertical_layout = QVBoxLayout(self)
        main_root_vertical_layout.setSpacing(0)
        main_root_vertical_layout.setContentsMargins(0, 0, 0, 0)

        main_root_horizontal_layout = QHBoxLayout()
        main_root_horizontal_layout.setSpacing(0)
        main_root_horizontal_layout.setContentsMargins(0, 0, 0, 0)

        main_root_vertical_layout.addWidget(self.custom_title_bar)
        main_root_vertical_layout.addLayout(main_root_horizontal_layout)

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

        main_root_horizontal_layout.addLayout(left_container, 1)
        main_root_horizontal_layout.addWidget(main_frame, 5)

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
        self.server_buttons.clear()
        for server in server_list:
            server_button = ServerButton(server["name"], server["ip_address"], server["user_count"], self.login_page_popup)
            self.server_buttons[server["ip_address"]] = server_button
            if server['ip_address'] == self.current_server_ip:
                server_button.connected_server()
            self.server_layout.addWidget(server_button)

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
        self.chat_ui.set_username(username)
        self.chat_ui.set_server_name(server_name)

        self.main_layout_horizontal.addWidget(self.chat_ui)
        self.chat_ui.show()

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

    def server_close_message(self, message):
        QMessageBox.warning(self, "Server Message", message)
        self.message_input.setEnabled(False)
        pixmap = QPixmap(f"{self.image_path}/disconnected.png").scaled(20, 20, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.status_icon.setPixmap(pixmap)
        self.connection_status_label.setText("Disconnected")

    def update_button_updater(self, update):
        if update:
            self.update_client_button.setVisible(True)
        
    def update_own_profile_picture(self, picture):
        self.user_picture.setPixmap(picture)
    
    def clear_chat_widget(self):
        self.chat_ui.hide()
        self.main_layout_horizontal.removeWidget(self.chat_ui)
    
    def update_users_count(self, value):
        button = self.server_buttons.get(self.current_server_ip)

        button.set_users_value(value)

    def update_server_icon(self, icon_base64):
        decoded_bytes = base64.b64decode(icon_base64)

        button = self.server_buttons.get(self.current_server_ip)
        button.set_server_icon(decoded_bytes, button.name)

class ServerButton(QFrame):
    def __init__(self, name, ip, user_count, on_click):
        super().__init__()

        self.name = name
        self.ip = ip
        self.user_count = user_count
        self.on_click = on_click
        self.connected = False

        self.setFixedHeight(60)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border-radius: 10px;
                border none;
            }

            QFrame:hover {
                background-color: #333333;
            }

            QFrame[current_server="true"] {
                background-color: #333333;
            }
        """)

        layout = QHBoxLayout(self)
        vertical_layout = QVBoxLayout()

        self.server_icon = QLabel()
        self.server_icon.setFixedSize(40, 40)
        self.server_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.server_icon.setStyleSheet("""
        QLabel {
            background-color: transparent;
            border: none;
            }
        """)
        if os.path.exists(f"{app_directory()}/server_icons/{self.name}.png"):
            pixmap = QPixmap(f"{app_directory()}/server_icons/{self.name}.png").scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        else:
            pixmap = QPixmap(f"{file_root()}/server_image_placeholder.png").scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        rounded_image = QPixmap(40, 40)
        rounded_image.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded_image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        path = QPainterPath()
        path.addEllipse(0, 0, 40, 40)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self.server_icon.setPixmap(rounded_image)

        self.label = QLabel()
        self.label.setFixedWidth(180)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                border: none;
                background: transparent;
                font-size: 15px;
            }
        """)

        self.users_count = QLabel(f"{self.user_count} Members")
        self.users_count.setStyleSheet("""
            QLabel{
                color: #a5a8ad;
                border: none;
                background: transparent;
                font-size: 10px;
            }
        """)

        self.resize_server_name()

        self.active_server_pointer = QLabel(">")
        self.active_server_pointer.setFixedSize(20, 20)
        self.active_server_pointer.setVisible(False)
        self.active_server_pointer.setStyleSheet("""
            QLabel{
                border: none;
                color: white;
                background: transparent;
            }
        """)

        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(self.users_count)

        layout.addWidget(self.server_icon)
        layout.addLayout(vertical_layout)
        layout.addStretch()
        layout.addWidget(self.active_server_pointer)

        self.mousePressEvent = self.frame_clicked
    
    def resize_server_name(self):
        metrics = QFontMetrics(self.label.font())
        resize_name = metrics.elidedText(self.name, Qt.ElideRight, self.label.width())
        self.label.setText(resize_name)

    def frame_clicked(self, event):
        if self.connected:
            return

        self.on_click(self)

    def connected_server(self):
        self.connected = True
        self.setProperty("current_server", True)
        self.active_server_pointer.setVisible(True)

    def set_users_value(self, value):
        self.users_count.setText(f"{value} members")
        update_user_count(self.ip, value)

    def set_server_icon(self, decoded_bytes, server_name):
        pixmap = QPixmap()
        pixmap.loadFromData(decoded_bytes)
        pixmap_scaled = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        rounded_image = QPixmap(40, 40)
        rounded_image.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded_image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        path = QPainterPath()
        path.addEllipse(0, 0, 40, 40)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap_scaled)
        painter.end()

        save_server_icon(rounded_image, server_name)

        self.server_icon.setPixmap(rounded_image)

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setFixedHeight(35)
        self.setAutoFillBackground(True)
        self.setObjectName("customtitlebar")
        self.setStyleSheet("""
            QWidget#customtitlebar {
                background-color: #161b22;
            }
        """)

        button_style_sheet = """
        QPushButton {
            background: transparent;
            color: #9ca3af;
            border: none;
            font-size: 14px;
            border-radius: 0px;
        }

        QPushButton:hover {
            color: #f3f4f6;
            background-color: #1f2937;
        }
        """

        self.parent = parent
        
        layout = QHBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 0, 0, 0)

        title = QLabel("BiteWire")
        title.setStyleSheet("""
        QLabel {
            color: #e5e7eb;
            font-weight: 600;
            font-size: 12px
        }
        """)

        minimize_button = QPushButton("-")
        minimize_button.setFixedSize(35, 35)
        minimize_button.setStyleSheet(button_style_sheet)
        minimize_button.clicked.connect(lambda: self.parent.showMinimized())

        maximize_button = QPushButton("□")
        maximize_button.setFixedSize(35, 35)
        maximize_button.setStyleSheet(button_style_sheet)
        maximize_button.clicked.connect(lambda: self.toggle_maximize())

        close_button = QPushButton("x")
        close_button.setFixedSize(35, 35)
        close_button.setStyleSheet(button_style_sheet.replace("#1f2937", "#ef4444"))
        close_button.clicked.connect(lambda: self.parent.close())

        layout.addWidget(title)
        layout.addWidget(minimize_button)
        layout.addWidget(maximize_button)
        layout.addWidget(close_button)

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            handle = self.window().windowHandle()
            if handle:
                handle.startSystemMove()