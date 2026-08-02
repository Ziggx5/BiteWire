from math import trunc

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import threading
from server_modules.data_manipulation import local_data_file, files_check, validate_certificate, resouce_statistic
from server_modules.server import ChatServer
from server_modules.system_tray import TrayManager
from server_modules.load_assets import file_root

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BiteWire Server")
        self.setObjectName("main_ui")
        self.setStyleSheet("""
            QWidget#main_ui {
                background-color : #0e1117;
            }
        """)
        self.setFixedSize(900, 580)
        self.tray = TrayManager(self)
        self.chat_server = ChatServer()
        self.chat_server.uptime_signal.connect(self.update_timer)
        self.chat_server.first_clients_signal.connect(self.refresh_first_clients)
        self.chat_server.active_clients_count_signal.connect(self.refresh_active_clients_count)
        self.local_file = local_data_file()
        image_path = file_root()
        self.settings_page = SettingsPage(self.local_file, image_path)
        self.users_page = UsersPage()

        self.files = files_check()
        self.settings_page.fill_inputs(self.files)
        expiry_date, remaining_days, cert_issued, cert_status = validate_certificate()

        self.cpu_usage = "0"
        self.ram_usage = "0"
        self.incoming = "0"
        self.outgoing = "0"
        self.recv_speed = "0"
        self.sent_speed = "0"

        self.resource_timer = QTimer()
        self.resource_timer.timeout.connect(self.update_server_resource_values)
        self.resource_timer.start(1000)

        self.stack = QStackedLayout()

        self.server_status_card = StatCard("Server Status", "Stopped", "#3b82f6")
        self.total_users_card = StatCard("Total Users", "0", "#60a5fa")
        self.total_messages_card = StatCard("Total Messages", "0", "#a78bfa")
        self.server_uptime_card = StatCard("Uptime", "00:00:00", "#2dd4bf")

        self.chat_server.client_count_signal.connect(self.total_users_card.set_value)
        self.chat_server.message_count_signal.connect(self.total_messages_card.set_value)

        self.chat_server.get_message_count()
        self.chat_server.get_client_count()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        main_screen = QWidget()
        main_screen_layout = QVBoxLayout(main_screen)
        main_screen_layout.setContentsMargins(10, 10, 10, 10)

        dashboard_button = SideButtons("Dashboard", f"{image_path}/home.png")
        dashboard_button.clicked.connect(lambda: self.stack.setCurrentWidget(main_screen))
        users_button = SideButtons("Users", f"{image_path}/users.png")
        users_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.users_page))
        logs_button = SideButtons("Logs", f"{image_path}/logs.png")
        logs_button.setToolTip("Currently not available")
        settings_button = SideButtons("Settings", f"{image_path}/settings.png")
        settings_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        about_button = SideButtons("About", f"{image_path}/about.png")
        about_button.setToolTip("Currently not available")

        cards_layout = QHBoxLayout()

        cards_layout.addWidget(self.server_status_card)
        cards_layout.addSpacing(5)
        cards_layout.addWidget(self.total_users_card)
        cards_layout.addSpacing(5)
        cards_layout.addWidget(self.total_messages_card)
        cards_layout.addSpacing(5)
        cards_layout.addWidget(self.server_uptime_card)

        server_info = QWidget()
        server_info.setStyleSheet("""
            QWidget {
                background-color: #111827;
                border: 1px solid #23304a;
                border-radius: 7px;
            }
        """)
        server_info_layout = QGridLayout(server_info)
        server_info_layout.setSpacing(5)

        server_info_label = QLabel("Server Info")
        server_info_label.setStyleSheet("""
            QLabel {
                color: #f3f4f6;
                font-size: 15px;
                font-weight: 600px;
                border: none;
            }
        """)

        port_label = QLabel("Port")
        port_label.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                border: none;
            }
        """)
        port_placeholder_label = QLabel("50505")
        port_placeholder_label.setStyleSheet("""
            QLabel {
                color: #e5e7eb;
                font-weight: 600;
                border: none;
            }        
        """)

        ssl_status_label = QLabel("Certificate Status")
        ssl_status_label.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                border: none;
            }
        """)
        ssl_status_placeholder_label = QLabel(cert_status)
        ssl_status_placeholder_label.setStyleSheet("""
            QLabel {
                color: #4ade80;
                font-weight: 600;
                border: none;
            }        
        """)

        ssl_remaining_days_label = QLabel("Days Left")
        ssl_remaining_days_label.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                border: none;
            }
        """)
        ssl_remaining_days_placeholder_label = QLabel(remaining_days)
        ssl_remaining_days_placeholder_label.setStyleSheet("""
            QLabel {
                color: #e5e7eb;
                font-weight: 600;
                border: none;
            }   
        """)

        ssl_issued_date_label = QLabel("Issued On")
        ssl_issued_date_label.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                border: none;
            }
        """)
        ssl_issued_date_placeholder_label = QLabel(cert_issued)
        ssl_issued_date_placeholder_label.setStyleSheet("""
            QLabel {
                color: #e5e7eb;
                font-weight: 600;
                border: none;
            } 
        """)

        ssl_expires_label = QLabel("Expires On")
        ssl_expires_label.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                border: none;
            }
        """)
        ssl_expires_placeholder_label = QLabel(expiry_date)
        ssl_expires_placeholder_label.setStyleSheet("""
            QLabel {
                color: #e5e7eb;
                font-weight: 600;
                border: none;
            }        
        """)

        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setFixedHeight(1)
        line1.setStyleSheet("""
            QFrame {
                border: 1px solid #1f2a44;
                border-radius: 8px;
            }
        """)

        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFixedHeight(1)
        line2.setStyleSheet("""
            QFrame {
                border: 1px solid #1f2a44;
                border-radius: 8px;
            }
        """)

        line3 = QFrame()
        line3.setFrameShape(QFrame.Shape.HLine)
        line3.setFixedHeight(1)
        line3.setStyleSheet("""
            QFrame {
                border: 1px solid #1f2a44;
                border-radius: 8px;
            }
        """)

        line4 = QFrame()
        line4.setFrameShape(QFrame.Shape.HLine)
        line4.setFixedHeight(1)
        line4.setStyleSheet("""
            QFrame {
                border: 1px solid #1f2a44;
                border-radius: 8px;
            }
        """)

        line5 = QFrame()
        line5.setFrameShape(QFrame.Shape.HLine)
        line5.setFixedHeight(1)
        line5.setStyleSheet("""
            QFrame {
                border: 1px solid #1f2a44;
                border-radius: 8px;
            }
        """)

        server_info_layout.addWidget(server_info_label, 0, 0)
        server_info_layout.addWidget(line1, 1, 0, 1, 2)
        server_info_layout.addWidget(port_label, 2, 0)
        server_info_layout.addWidget(port_placeholder_label, 2, 1, Qt.AlignmentFlag.AlignRight)
        server_info_layout.addWidget(line2, 3, 0, 1, 2)
        server_info_layout.addWidget(ssl_status_label, 4, 0)
        server_info_layout.addWidget(ssl_status_placeholder_label, 4, 1, Qt.AlignmentFlag.AlignRight)
        server_info_layout.addWidget(line3, 5, 0, 1, 2)
        server_info_layout.addWidget(ssl_remaining_days_label, 6, 0)
        server_info_layout.addWidget(ssl_remaining_days_placeholder_label, 6, 1, Qt.AlignmentFlag.AlignRight)
        server_info_layout.addWidget(line4, 7, 0, 1, 2)
        server_info_layout.addWidget(ssl_issued_date_label, 8, 0)
        server_info_layout.addWidget(ssl_issued_date_placeholder_label, 8, 1, Qt.AlignmentFlag.AlignRight)
        server_info_layout.addWidget(line5, 9, 0, 1, 2)
        server_info_layout.addWidget(ssl_expires_label, 10, 0)
        server_info_layout.addWidget(ssl_expires_placeholder_label, 10, 1, Qt.AlignmentFlag.AlignRight)

        server_resources = QWidget()
        server_resources_layout = QVBoxLayout(server_resources)
        cpu_and_ram_stats_layout = QHBoxLayout()
        incoming_and_outgoing_layout = QHBoxLayout()

        server_statistics_and_resources_container = QHBoxLayout()

        self.cpu_percentage_card = StatCard("CPU Usage", f"{self.cpu_usage}%", "#facc15")
        self.ram_usage_card = StatCard("RAM Usage", f"{self.ram_usage}MB", "#f472b6")
        self.incoming_card = StatCard("Incoming", f"{self.incoming}KB/s", "#4ade80")
        self.outgoing_card = StatCard("Outgoing", f"{self.outgoing}KB/s", "#fb923c")

        cpu_and_ram_stats_layout.addWidget(self.cpu_percentage_card)
        cpu_and_ram_stats_layout.addWidget(self.ram_usage_card)

        incoming_and_outgoing_layout.addWidget(self.incoming_card)
        incoming_and_outgoing_layout.addWidget(self.outgoing_card)

        server_resources_layout.addLayout(cpu_and_ram_stats_layout)
        server_resources_layout.addLayout(incoming_and_outgoing_layout)

        server_statistics_and_resources_container.addWidget(server_resources)
        server_statistics_and_resources_container.addWidget(server_info)

        recent_logs_and_active_clients_container = QHBoxLayout()

        recent_logs_card = QFrame()
        recent_logs_card.setObjectName("recent_logs_card")
        recent_logs_card.setFixedHeight(200)
        recent_logs_card.setStyleSheet("""
            QFrame#recent_logs_card {
                background-color: #111827;
                border: 1px solid #23304a;
                border-radius: 7px;
            }
        """)
        recent_logs_card_layout = QVBoxLayout(recent_logs_card)
        recent_logs_card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        recent_logs_card_header_layout = QHBoxLayout()

        recent_logs_label = QLabel("Recent Logs")

        view_all_logs_label = QLabel("View all logs >")
        view_all_logs_label.setToolTip("Currently not available")

        recent_logs_card_header_layout.addWidget(recent_logs_label)
        recent_logs_card_header_layout.addStretch()
        recent_logs_card_header_layout.addWidget(view_all_logs_label)

        recent_logs_card_layout.addLayout(recent_logs_card_header_layout)

        active_clients_card = QFrame()
        active_clients_card.setObjectName("active_clients_card")
        active_clients_card.setFixedHeight(200)
        active_clients_card.setStyleSheet("""
            QFrame#active_clients_card {
                background-color: #111827;
                border: 1px solid #23304a;
                border-radius: 7px;
            }
        """)
        active_clients_card_layout = QVBoxLayout(active_clients_card)
        active_clients_card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.active_clients_card_first_clients_layout = QVBoxLayout()

        active_clients_card_header_layout = QHBoxLayout()

        self.active_users_label = QLabel("Active users (0)")

        view_all_users_label = QLabel("View all users >")
        view_all_users_label.setToolTip("Currently not available")

        active_clients_card_header_layout.addWidget(self.active_users_label)
        active_clients_card_header_layout.addStretch()
        active_clients_card_header_layout.addWidget(view_all_users_label)

        active_clients_card_layout.addLayout(active_clients_card_header_layout)
        active_clients_card_layout.addLayout(self.active_clients_card_first_clients_layout)

        recent_logs_and_active_clients_container.addWidget(recent_logs_card)
        recent_logs_and_active_clients_container.addSpacing(5)
        recent_logs_and_active_clients_container.addWidget(active_clients_card)

        server_control_box = QFrame()
        server_buttons_layout = QHBoxLayout(server_control_box)

        self.start_server_button = QPushButton("Start")
        self.start_server_button.setFixedSize(80, 30)
        self.start_server_button.setStyleSheet("""
            QPushButton {
                border-radius: 3px;
                font-size: 13px;
                font-weight: 600;
                background-color: #1d64d6;
            }
        """)
        self.start_server_button.clicked.connect(self.start_server)
        self.stop_server_button = QPushButton("Stop")
        self.stop_server_button.setFixedSize(80, 30)
        self.stop_server_button.setStyleSheet("""
            QPushButton {
                border-radius: 3px;
                font-size: 13px;
                font-weight: 600;
                background-color: gray;
            }
        """)
        self.stop_server_button.clicked.connect(self.stop_server)
        self.stop_server_button.setEnabled(False)

        server_buttons_layout.addWidget(self.start_server_button)
        server_buttons_layout.addSpacing(5)
        server_buttons_layout.addWidget(self.stop_server_button)
        server_buttons_layout.addStretch()

        main_screen_layout.addLayout(cards_layout)
        main_screen_layout.addSpacing(10)
        main_screen_layout.addLayout(server_statistics_and_resources_container)
        main_screen_layout.addSpacing(10)
        main_screen_layout.addLayout(recent_logs_and_active_clients_container)
        main_screen_layout.addStretch()
        main_screen_layout.addWidget(server_control_box)

        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
        QFrame{
            background-color: #111827;
            border-right: 1px solid #23304a;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(5, 10, 5, 10)
        sidebar_layout.setSpacing(5)

        sidebar_layout.addWidget(dashboard_button)
        sidebar_layout.addWidget(users_button)
        sidebar_layout.addWidget(logs_button)
        sidebar_layout.addWidget(settings_button)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(about_button)

        self.stack.addWidget(main_screen)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.users_page)
        self.stack.setCurrentWidget(main_screen)

        layout.addWidget(sidebar)
        layout.addLayout(self.stack)

    def start_server(self):
        if not self.settings_page.check_required_files():
            return

        threading.Thread(target = self.chat_server.start, daemon = True).start()

        self.server_status_card.set_value("Running")
        self.start_server_button.setEnabled(False)
        QTimer.singleShot(2000, lambda: self.stop_server_button.setEnabled(True))

        self.tray.set_server_status("Running")

    def stop_server(self):
        self.chat_server.stop()
        self.server_status_card.set_value("Stopped")
        self.stop_server_button.setEnabled(False)
        QTimer.singleShot(2000, lambda: self.start_server_button.setEnabled(True))

        self.tray.set_server_status("Stopped")

        self.update_timer(0, 0, 0)

    def update_timer(self, hours, minutes, seconds):
        self.server_uptime_card.set_value(f"{hours:02}:{minutes:02}:{seconds:02}")
        self.tray.set_server_uptime(hours, minutes, seconds)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def open_server_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.local_file))

    def update_server_resource_values(self):
        self.cpu_usage, self.ram_usage = resouce_statistic()
        self.incoming, self.outgoing = self.chat_server.update_network_statistics()

        self.cpu_percentage_card.set_value(f"{self.cpu_usage}%")
        self.ram_usage_card.set_value(f"{self.ram_usage}MB")
        self.incoming_card.set_value(f"{self.incoming}KB/s")
        self.outgoing_card.set_value(f"{self.outgoing}KB/s")

    def refresh_first_clients(self, clients):
        while self.active_clients_card_first_clients_layout.count():
            item = self.active_clients_card_first_clients_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for client in clients:
            row = ActiveClient(client)
            self.active_clients_card_first_clients_layout.addWidget(row)

    def refresh_active_clients_count(self, clients_count):
        self.active_clients_label.setText(f"Active users ({clients_count})")

class StatCard(QFrame):
    def __init__(self, title, value, text_color):
        super().__init__()

        self.setObjectName("statcard")
        self.setStyleSheet("""
            QFrame#statcard {
                background-color: #111827;
                border: 1px solid #23304a;
                border-radius: 7px;
            }
        """)
        self.setFixedHeight(80)


        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #d1d5db;
                font-size: 12px;
            }
        """)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                font-size: 17px;
                font-weight: 700px;
            }}
        """)

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()

    def set_value(self, value):
        self.value_label.setText(value)

class ActiveClient(QWidget):
    def __init__(self, username):
        super().__init__()

        layout = QHBoxLayout(self)

        username_label = QLabel(username)

        layout.addWidget(username_label)
        layout.addStretch()

class SideButtons(QPushButton):
    def __init__(self, text, icon):
        super().__init__()

        self.icon = icon
        self.text = text

        self.setFixedHeight(40)

        self.setStyleSheet("""
        QWidget {
            background: transparent;
            border: 3px solid transparent;
            border-radius: 10px;
            color: #9ca3af;
            }
            
        QWidget:hover {
            background: #1b2535;
            color: white;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 0, 10, 0)

        icon = QLabel()
        icon.setPixmap(QPixmap(self.icon).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
        icon.setFixedSize(30, 30)

        label = QLabel(self.text)
        label.setStyleSheet("""
        QLabel {
            color: #d1d5db;
            font-size: 14px;
            font-weight: 500;
            }
        """)

        layout.addWidget(icon)
        layout.addWidget(label)

class SettingsPage(QWidget):
    def __init__(self, local_files, image_path):
        super().__init__()

        self.directory_watcher = QFileSystemWatcher(self)
        self.directory_watcher.addPath(local_files)
        self.directory_watcher.directoryChanged.connect(lambda: self.fill_inputs(files_check()))

        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()

        layout.addLayout(header_layout)
        layout.addSpacing(10)

        frame = QFrame()
        frame.setObjectName("frame")
        frame.setStyleSheet("""
        QFrame#frame {
            background: #161b22;
            border: 1px solid #2b3442;
            border-radius: 12px;
            }
        """)

        frame_layout = QVBoxLayout(frame)

        files_grid_layout = QGridLayout()
        files_grid_layout.setSpacing(20)
        files_grid_layout.setHorizontalSpacing(10)

        server_files_label = QLabel("Server Files")
        server_files_label.setStyleSheet("""
        QLabel {
            color: #d1d5db;
            font-size: 20px;
            font-weight: 500;
            }
        """)

        server_files_icon = QLabel()
        server_files_icon.setPixmap(QPixmap(f"{image_path}/folder.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        server_files_icon.setFixedSize(40, 40)
        server_files_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        server_files_icon.setStyleSheet("""
        QLabel {
            background-color: #1e3a8a;
            border-radius: 20px;
            border: 1px solid transparent;
            } 
        """)

        header_layout.addWidget(server_files_icon)
        header_layout.addWidget(server_files_label)

        certificate_file_icon = QLabel()
        certificate_file_icon.setPixmap(QPixmap(f"{image_path}/certificate.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        certificate_file_icon.setFixedSize(50, 50)
        certificate_file_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        certificate_file_icon.setStyleSheet("""
        QLabel {
            background-color: #15161c;
            border: 1px solid #282b33;
            border-radius: 10px;
            }
        """)
        certificate_file_label = QLabel("Certificate file")
        certificate_file_label.setStyleSheet("""
        QLabel {
            font-weight: 500;
            } 
        """)
        self.certificate_file_input = QLineEdit()
        self.certificate_file_input.setStyleSheet("""
        QLineEdit {
            background-color: #1d212a;
            border: 1px solid #282c35;
            border-radius: 8px;
            color: #d1d5db;
            padding: 8px;     
            }
        """)
        self.certificate_file_input.setEnabled(False)

        key_file_icon = QLabel()
        key_file_icon.setPixmap(QPixmap(f"{image_path}/key.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        key_file_icon.setFixedSize(50, 50)
        key_file_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        key_file_icon.setStyleSheet("""
        QLabel {
            background-color: #15161c;
            border: 1px solid #282b33;
            border-radius: 10px;
            }
        """)
        key_file_label = QLabel("Key file")
        key_file_label.setStyleSheet("""
        QLabel {
            font-weight: 500;
            } 
        """)
        self.key_file_input = QLineEdit()
        self.key_file_input.setStyleSheet("""
        QLineEdit {
            background-color: #1d212a;
            border: 1px solid #282c35;
            border-radius: 8px;
            color: #d1d5db;
            padding: 8px;     
            }
        """)
        self.key_file_input.setEnabled(False)

        users_database_file_icon = QLabel()
        users_database_file_icon.setPixmap(QPixmap(f"{image_path}/user_database.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        users_database_file_icon.setFixedSize(50, 50)
        users_database_file_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        users_database_file_icon.setStyleSheet("""
        QLabel {
            background-color: #15161c;
            border: 1px solid #282b33;
            border-radius: 10px;
            }
        """)
        users_database_file_label = QLabel("Users database file")
        users_database_file_label.setStyleSheet("""
        QLabel {
            font-weight: 500;
            } 
        """)
        self.users_database_file_input = QLineEdit()
        self.users_database_file_input.setStyleSheet("""
        QLineEdit {
            background-color: #1d212a;
            border: 1px solid #282c35;
            border-radius: 8px;
            color: #d1d5db;
            padding: 8px;     
            }
        """)
        self.users_database_file_input.setEnabled(False)

        messages_database_file_icon = QLabel()
        messages_database_file_icon.setPixmap(QPixmap(f"{image_path}/message_database.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        messages_database_file_icon.setFixedSize(50, 50)
        messages_database_file_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        messages_database_file_icon.setStyleSheet("""
        QLabel {
            background-color: #15161c;
            border: 1px solid #282b33;
            border-radius: 10px;
            }
        """)
        messages_database_file_label = QLabel("Messages database file")
        messages_database_file_label.setStyleSheet("""
        QLabel {
            font-weight: 500;
            } 
        """)
        self.messages_database_file_input = QLineEdit()
        self.messages_database_file_input.setStyleSheet("""
        QLineEdit {
            background-color: #1d212a;
            border: 1px solid #282c35;
            border-radius: 8px;
            color: #d1d5db;
            padding: 8px;     
            }
        """)
        self.messages_database_file_input.setEnabled(False)

        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(10)
        footer_layout.setContentsMargins(10, 10, 10, 10)

        info_icon = QLabel()
        info_icon.setPixmap(QPixmap(f"{image_path}/about.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        info_label = QLabel("Database files are generated automatically when server starts. if you already have existing database files, place them in the application directory.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
        QLabel {
            color: #dbeafe;
            font-size: 13px;
            }
        """)

        server_icon = QLabel()
        server_icon.setPixmap(QPixmap(f"{image_path}/server_icon.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        server_icon.setFixedSize(50, 50)
        server_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        server_icon.setStyleSheet("""
        QLabel {
            background-color: #15161c;
            border: 1px solid #282b33;
            border-radius: 10px;
            }
        """)
        server_icon_label = QLabel("Server icon")
        server_icon_label.setStyleSheet("""
        QLabel {
            font-weight: 500;
            }
        """)
        self.server_icon_input = QLineEdit()
        self.server_icon_input.setStyleSheet("""
        QLineEdit {
            background-color: #1d212a;
            border: 1px solid #282c35;
            border-radius: 8px;
            color: #d1d5db;
            padding: 8px;     
            }
        """)
        self.server_icon_input.setEnabled(False)

        browse_button = QPushButton("Browse...")
        browse_button.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border-radius: 5px;
                    padding: 8px 16px;
                    }

                QPushButton:hover {
                    background-color: #1d4ed8;
                    }

                QPushButton:pressed {
                    background-color: #1e40af;
                    }
                """)
        browse_button.setFixedWidth(100)
        browse_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(local_files)))

        footer_layout.addWidget(info_icon)
        footer_layout.addWidget(info_label)
        footer_layout.addStretch()
        footer_layout.addWidget(browse_button)

        files_grid_layout.addWidget(certificate_file_icon, 0, 0)
        files_grid_layout.addWidget(certificate_file_label, 0, 1)
        files_grid_layout.addWidget(self.certificate_file_input, 0, 2)
        files_grid_layout.addWidget(key_file_icon, 1, 0)
        files_grid_layout.addWidget(key_file_label, 1, 1)
        files_grid_layout.addWidget(self.key_file_input, 1, 2)
        files_grid_layout.addWidget(users_database_file_icon, 2, 0)
        files_grid_layout.addWidget(users_database_file_label, 2, 1)
        files_grid_layout.addWidget(self.users_database_file_input, 2, 2)
        files_grid_layout.addWidget(messages_database_file_icon, 3, 0)
        files_grid_layout.addWidget(messages_database_file_label, 3, 1)
        files_grid_layout.addWidget(self.messages_database_file_input, 3, 2)
        files_grid_layout.addWidget(server_icon, 4, 0)
        files_grid_layout.addWidget(server_icon_label, 4, 1)
        files_grid_layout.addWidget(self.server_icon_input, 4, 2)

        frame_layout.addLayout(files_grid_layout)
        frame_layout.addLayout(footer_layout)

        layout.addWidget(frame)
        layout.addStretch()

    def fill_inputs(self, files):
        self.certificate_file_input.clear()
        self.key_file_input.clear()
        self.users_database_file_input.clear()
        self.messages_database_file_input.clear()
        self.server_icon_input.clear()

        for file_path in files:
            if file_path.endswith(".crt"):
                self.certificate_file_input.setText(file_path)

            elif file_path.endswith(".key"):
                self.key_file_input.setText(file_path)

            elif file_path.endswith("users.db"):
                self.users_database_file_input.setText(file_path)

            elif file_path.endswith("messages.db"):
                self.messages_database_file_input.setText(file_path)

            elif file_path.endswith(".png") or file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                self.server_icon_input.setText(file_path)

    def check_required_files(self):
        return all([
            self.certificate_file_input.text(),
            self.key_file_input.text(),
            self.users_database_file_input.text(),
            self.messages_database_file_input.text(),
            self.server_icon_input.text()
        ])

class UsersPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()

        header_icon = QLabel()
        header_label = QLabel("All Users")
        header_label.setStyleSheet("""
        QLabel {
            color: #d1d5db;
            font-size: 14px;
            font-weight: 500;
            }
        """)
        search_user_box = QLineEdit()
        search_user_box.setPlaceholderText("Search...")
        search_user_box.setFixedWidth(220)
        search_user_box.setStyleSheet("""
        QLineEdit {
            background-color: #26263b;
            color: #d1d5db;
            border: 1px solid #3c3c52;
            border-radius: 5px;
            padding: 6px 10px;
            }
        
        QLineEdit:focus {
            border: 1px solid #4f8cff;
            }
        """)

        header_layout.addWidget(header_icon)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(search_user_box)

        data_bar_layout = QHBoxLayout()

        user_number_label = QLabel("#")
        username_label = QLabel("Username")
        status_label = QLabel("Status")
        actions_label = QLabel("Actions")

        data_bar_layout.addWidget(user_number_label)
        data_bar_layout.addWidget(username_label)
        data_bar_layout.addWidget(status_label)
        data_bar_layout.addWidget(actions_label)

        layout.addLayout(header_layout)
        layout.addLayout(data_bar_layout)
        layout.addStretch()