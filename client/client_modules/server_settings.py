from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from client_modules.data_manipulation import app_directory, delete_server, change_server_name
from client_modules.path_finder import file_root
import os

class ServerSettings(QWidget):
    def __init__(self, close_page, reload_servers):
        super().__init__()

        self.server_name = None
        self.server_address = None
        self.status = None
        self.theme_color = None
        self.border_color = None
        self.server_picture_path = None
        self.placeholder_image_path = f"{file_root()}/server_image_placeholder.png"
        self.appearance_page = None

        self.close_page = close_page
        self.reload_servers = reload_servers

        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout(self)
        self.stack = QStackedLayout()

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 10)
        header_label = QLabel("Server Settings")
        header_label.setStyleSheet("""
            QLabel {
                color: #f3f4f6;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        exit_button = QPushButton("×")
        exit_button.setFixedSize(35, 35)
        exit_button.clicked.connect(self.close_page)

        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(exit_button)

        main_page_container = QFrame()
        main_page_container.setObjectName("main_page_container")
        main_page_container.setStyleSheet("""
            QFrame#main_page_container {
                background-color: #1a1f2c;
                border: 1px solid #252d40;
                border-radius: 10px;
            }
        """)

        main_page_container_layout = QVBoxLayout(main_page_container)
        main_page_container_layout.addLayout(self.stack)

        main_screen = QFrame()

        main_screen_layout = QGridLayout(main_screen)
        main_screen_layout.setVerticalSpacing(10)

        general_title = QLabel("General")
        general_title.setStyleSheet("""
            QLabel {
                color: #f3f4f6;
                font-size: 20px;
                font-weight: 600;
            }
        """)

        general_description = QLabel("Basic information about this server.")
        general_description.setStyleSheet("""
            QLabel {
                color: #8b93a7;
                font-size: 12px;
            }
        """)

        server_name_label = QLabel("Server Name")
        server_name_label.setStyleSheet("""
            QLabel {
                color: #e5e7eb;
                font-size: 15px;
                font-weight: 600;
            }
        """)

        self.server_name_input = QLineEdit()
        self.server_name_input.textChanged.connect(self.update_save_button)
        self.server_name_input.setStyleSheet("""
            QLineEdit {
                background-color: #151a24;
                color: #e5e7eb;
                border: 1px solid #2b3448;
                border-radius: 6px;
                padding: 8px;
            }
            
            QLineEdit:focus {
                border: 1px solid #5865f2;
            }
        """)

        server_address_label = QLabel("Server Address")
        server_address_label.setStyleSheet("""
            QLabel {
                color: #e5e7eb;
                font-size: 15px;
                font-weight: 600;
            }
        """)

        self.server_address_input = QLineEdit()
        self.server_address_input.setReadOnly(True)
        self.server_address_input.setStyleSheet("""
            QLineEdit {
                background-color: #151a24;
                color: #e5e7eb;
                border: 1px solid #2b3448;
                border-radius: 6px;
                padding: 8px;
            }
        """)

        copy_button = QPushButton("Copy")
        copy_button.setIcon(QIcon(f"{file_root()}/clipboard.png"))
        copy_button.setIconSize(QSize(20, 20))
        copy_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e5e7eb;
                border: 1px solid #343f56;
                border-radius: 6px;
                padding: 5px;
            }
        """)

        server_port_label = QLabel("Server Port")
        server_port_label.setStyleSheet("""
            QLabel {
                color: #e5e7eb;
                font-size: 15px;
                font-weight: 600;
            }
        """)

        server_port_input = QLineEdit("50505")
        server_port_input.setReadOnly(True)
        server_port_input.setStyleSheet("""
            QLineEdit {
                background-color: #151a24;
                color: #e5e7eb;
                border: 1px solid #2b3448;
                border-radius: 6px;
                padding: 8px;
            }
        """)

        self.save_button = QPushButton("Save Changes")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_changes)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #5865f2;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                padding: 9px 18px;
                font-size: 13px;
            }
            
            QPushButton:hover {
                background-color: #4752c4;
            }
            
            QPushButton:pressed {
                background-color: #3c45a5;
            }
            
            QPushButton:disabled {
                background-color: #3a3f4b;
                color: #8b93a7;
            }
        """)

        seperator = QFrame()
        seperator.setFrameShape(QFrame.Shape.HLine)
        seperator.setStyleSheet("""
            QFrame {
                border: none;
                background-color: #2b3448;
                max-height: 1px;
            }
        """)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)

        main_screen_layout.addWidget(general_title, 0, 0)
        main_screen_layout.addWidget(general_description, 1, 0)
        main_screen_layout.addWidget(server_name_label, 2, 0)
        main_screen_layout.addWidget(self.server_name_input, 3, 0)
        main_screen_layout.addWidget(server_address_label, 4, 0)
        main_screen_layout.addWidget(self.server_address_input, 5, 0)
        main_screen_layout.addWidget(copy_button, 5, 1)
        main_screen_layout.addWidget(server_port_label, 6, 0)
        main_screen_layout.addWidget(server_port_input, 7, 0)
        main_screen_layout.setRowStretch(8, 1)
        main_screen_layout.addWidget(seperator, 9, 0, 1, 2)
        main_screen_layout.addLayout(buttons_layout, 10, 0, 1, 2)

        sidebar_server_stat = QFrame()
        sidebar_server_stat_grid = QGridLayout(sidebar_server_stat)
        sidebar_server_stat_grid.setHorizontalSpacing(15)
        sidebar_server_stat_grid.setContentsMargins(0, 0, 0, 0)

        self.sidebar_server_stat_icon = QLabel()
        self.sidebar_server_stat_icon.setFixedSize(60, 60)
        self.sidebar_server_stat_icon.setScaledContents(True)
        self.sidebar_server_stat_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_server_stat_icon.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: 1px solid #30364d;
                border-radius: 10px;
            }
        """)
        self.sidebar_server_stat_name = QLabel("Server_name")
        self.sidebar_server_stat_name.setStyleSheet("""
            QLabel {
                color: #f3f4f6;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        self.sidebar_server_stat_connection_status = QLabel("Status")
        self.sidebar_server_stat_connection_status.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: 500;
            }
        """)

        sidebar_server_stat_grid.addWidget(self.sidebar_server_stat_icon, 0, 0, 2, 1)
        sidebar_server_stat_grid.addWidget(self.sidebar_server_stat_name, 0, 1)
        sidebar_server_stat_grid.addWidget(self.sidebar_server_stat_connection_status, 1, 1)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(180)
        sidebar.setContentsMargins(0, 0, 0, 0)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        self.general_button = QPushButton("General")
        self.general_button.setIcon(QIcon(f"{file_root()}/settings.png"))
        self.general_button.setIconSize(QSize(20, 20))
        self.general_button.clicked.connect(lambda: (self.set_active_button(self.general_button), self.stack.setCurrentWidget(main_screen)))
        self.general_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d1d5db;
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #1d2638;
            }
            
            QPushButton[active="true"] {
                background-color: #293452;
            }
        """)

        self.appearance_button = QPushButton("Appearance")
        self.appearance_button.setIcon(QIcon(f"{file_root()}/pallete.png"))
        self.appearance_button.setIconSize(QSize(20, 20))
        self.appearance_button.clicked.connect(lambda: (self.set_active_button(self.appearance_button), self.stack.setCurrentWidget(self.appearance_page)))
        self.appearance_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d1d5db;
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }

            QPushButton:hover {
                background-color: #1d2638;
            }
            
            QPushButton[active="true"] {
                background-color: #293452;
            }
        """)
        self.notification_button = QPushButton("Notifications")
        self.notification_button.setIcon(QIcon(f"{file_root()}/notification.png"))
        self.notification_button.setIconSize(QSize(20, 20))
        self.notification_button.clicked.connect(lambda: self.set_active_button(self.notification_button))
        self.notification_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d1d5db;
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }

            QPushButton:hover {
                background-color: #1d2638;
            }
            
            QPushButton[active="true"] {
                background-color: #293452;
            }
        """)

        remove_server_button = QPushButton("Remove Server")
        remove_server_button.setIcon(QIcon(f"{file_root()}/trash.png"))
        remove_server_button.clicked.connect(self.remove_server)
        remove_server_button.setIconSize(QSize(20, 20))
        remove_server_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d65e60;
                border: none;
                text-align: left;
                padding: 10px;
                font-weight: 600;
            }
            
            QPushButton:hover {
                background-color: #2a1820;
                border-radius: 6px;
            }
        """)
        sidebar_layout.addWidget(sidebar_server_stat)
        sidebar_layout.addSpacing(10)
        sidebar_layout.addWidget(self.general_button)
        sidebar_layout.addWidget(self.appearance_button)
        sidebar_layout.addWidget(self.notification_button)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(remove_server_button)

        container_layout = QHBoxLayout()
        container_layout.addWidget(sidebar)
        container_layout.addSpacing(10)
        container_layout.addWidget(main_page_container)

        layout.addLayout(header_layout)
        layout.addLayout(container_layout)

        self.set_active_button(self.general_button)

        self.stack.addWidget(main_screen)
        self.stack.setCurrentWidget(main_screen)

    def get_server_info(self, server_name, server_address, theme_color, border_color, status):
        self.server_name = server_name
        self.server_picture_path = f"{app_directory()}/server_icons/{self.server_name}.png"
        self.server_address = server_address
        self.theme_color = theme_color
        self.border_color = border_color
        self.status = status

        self.fill_server_info()
        self.appearance_page = AppearancePage(self.get_theme_color, self.get_border_color)
        self.stack.addWidget(self.appearance_page)

    def fill_server_info(self):
        self.sidebar_server_stat_name.setText(self.server_name)
        self.server_name_input.setText(self.server_name)
        self.server_address_input.setText(self.server_address)
        self.sidebar_server_stat_connection_status.setText(self.status)

        if self.status == "Offline":
            self.sidebar_server_stat_connection_status.setStyleSheet("""
                QLabel {
                    color: #d65e60;
                }
            """)
        else:
            self.sidebar_server_stat_connection_status.setStyleSheet("""
                QLabel {
                    color: #86d48a;
                }
            """)

        if self.server_picture_path and os.path.exists(self.server_picture_path):
            self.sidebar_server_stat_icon.setPixmap(QPixmap(self.server_picture_path))
        else:
            self.sidebar_server_stat_icon.setPixmap(QPixmap(self.placeholder_image_path))

    def remove_server(self):
        reply = QMessageBox.information(self, "Remove Server", "Remove Server", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            delete_server(self.server_address)
            self.close_page()

    def update_save_button(self):
        if self.server_name != self.server_name_input.text():
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def save_changes(self):
        new_server_name = self.server_name_input.text()
        self.server_name = new_server_name

        self.sidebar_server_stat_name.setText(new_server_name)
        change_server_name(new_server_name, self.server_address, self.server_picture_path)
        self.server_picture_path = f"{app_directory()}/server_icons/{new_server_name}.png"
        self.reload_servers()

        self.save_button.setEnabled(False)

    def set_active_button(self, button):
        buttons = [self.general_button, self.appearance_button, self.notification_button]

        for current_button in buttons:
            current_button.setProperty("active", current_button == button)
            current_button.style().unpolish(current_button)
            current_button.style().polish(current_button)

    def get_theme_color(self):
        return self.theme_color

    def get_border_color(self):
        return self.border_color

class AppearancePage(QWidget):
    def __init__(self, theme_color, border_color):
        super().__init__()

        self.theme_color = theme_color
        self.border_color = border_color

        grid_layout = QGridLayout(self)
        grid_layout.setVerticalSpacing(10)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        general_title = QLabel("Appearance")
        general_title.setStyleSheet("""
            QLabel {
                color: #f3f4f6;
                font-size: 22px;
                font-weight: 600;
            }
        """)

        general_description = QLabel("Customize how this server looks in the application.")
        general_description.setStyleSheet("""
            QLabel {
                color: #8b93a7;
                font-size: 14px;
            }
        """)

        theme_color_label = QLabel("Theme Color")
        theme_color_label.setStyleSheet("""
            QLabel {
                color: #f3f4f6;
                font-size: 15px;
                font-weight: 600;
            }
        """)

        border_color_label = QLabel("Border Color")
        border_color_label.setStyleSheet("""
            QLabel {
                color: #f3f4f6;
                font-size: 15px;
                font-weight: 600;
            }
        """)

        seperator = QFrame()
        seperator.setFrameShape(QFrame.Shape.HLine)
        seperator.setStyleSheet("""
            QFrame {
                border: none;
                background-color: #2b3448;
                max-height: 1px;
            }
        """)

        self.save_button = QPushButton("Save Changes")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_changes)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #5865f2;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                padding: 9px 18px;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #4752c4;
            }

            QPushButton:pressed {
                background-color: #3c45a5;
            }

            QPushButton:disabled {
                background-color: #3a3f4b;
                color: #8b93a7;
            }
        """)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)

        grid_layout.addWidget(general_title, 0, 0)
        grid_layout.addWidget(general_description, 1, 0)
        grid_layout.addWidget(theme_color_label, 2, 0)
        grid_layout.addWidget(ThemeColors(self.theme_color()), 3, 0)
        grid_layout.addWidget(border_color_label, 4, 0)
        grid_layout.addWidget(ThemeColors(self.border_color()), 5, 0)
        grid_layout.setRowStretch(6, 1)
        grid_layout.addWidget(seperator, 7, 0)
        grid_layout.addLayout(buttons_layout, 8, 0)

    def save_changes(self):
        pass

class ThemeColors(QWidget):
    def __init__(self, color):
        super().__init__()

        self.color = color

        self.layout = QHBoxLayout(self)

        self.transparent_button = self.create_color_button("X", "transparent", False)
        self.blue_button = self.create_color_button(None , "#5865F2", False)
        self.green_button = self.create_color_button(None, "#57D681", False)
        self.red_button = self.create_color_button(None, "#F25555", False)
        self.yellow_button = self.create_color_button(None, "#F5B942", False)
        self.purple_button = self.create_color_button(None, "#8B5CF6", False)
        self.pink_button = self.create_color_button(None, "#D946A8", False)
        self.cyan_button = self.create_color_button(None, "#35C5E5", False)
        self.custom_button = self.create_color_button(None, "transparent", True)

        self.layout.addWidget(self.transparent_button)
        self.layout.addWidget(self.blue_button)
        self.layout.addWidget(self.green_button)
        self.layout.addWidget(self.red_button)
        self.layout.addWidget(self.yellow_button)
        self.layout.addWidget(self.purple_button)
        self.layout.addWidget(self.pink_button)
        self.layout.addWidget(self.cyan_button)
        self.layout.addWidget(self.custom_button)

        self.buttons = [self.transparent_button, self.blue_button, self.green_button, self.red_button, self.yellow_button, self.purple_button, self.pink_button, self.cyan_button, self.custom_button]

        self.set_color()

    def create_color_button(self, text, color, image):
        color_button = QPushButton()
        color_button.setFixedSize(26, 26)
        color_button.setProperty("color", color)
        color_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 13px;
            }}

            QPushButton:hover {{
                border: 2px solid white;
            }}
            
            QPushButton[active="true"] {{
                border: 2px solid white;
            }}
        """)

        if text:
            color_button.setText(text)
        if image:
            color_button.setIcon(QIcon(f"{file_root()}/pen.png"))
            color_button.setIconSize(QSize(15, 15))

        color_button.clicked.connect(lambda: self.select_color(color_button))

        return color_button

    def select_color(self, button):
        for current_button in self.buttons:
            current_button.setProperty("active", button == current_button)
            current_button.style().unpolish(current_button)
            current_button.style().polish(current_button)

    def set_color(self):
        for button in self.buttons:
            if self.color == button.property("color"):
                button.setProperty("active", True)
                button.style().unpolish(button)
                button.style().polish(button)

                break