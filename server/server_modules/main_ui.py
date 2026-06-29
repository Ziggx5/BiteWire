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
        self.setFixedSize(700, 700)
        self.tray = TrayManager(self)
        self.chat_server = ChatServer()
        self.chat_server.uptime_signal.connect(self.update_timer)
        self.chat_server.first_clients_signal.connect(self.refresh_first_clients)
        self.local_file = local_data_file()
        image_path = file_root()
        self.files = files_check()
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

        self.server_status_card = StatCard("Server Status", "Stopped")
        self.connected_clients_card = StatCard("Connected Clients", "0")
        self.total_messages_card = StatCard("Total Messages", "0")
        self.server_uptime_card = StatCard("Uptime", "00:00:00")

        self.chat_server.client_count_signal.connect(self.connected_clients_card.set_value)
        self.chat_server.message_count_signal.connect(self.total_messages_card.set_value)

        self.chat_server.get_message_count()

        layout = QVBoxLayout(self)

        cards_layout = QHBoxLayout()

        cards_layout.addWidget(self.server_status_card)
        cards_layout.addSpacing(5)
        cards_layout.addWidget(self.connected_clients_card)
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
        server_resouces_layout = QVBoxLayout(server_resources)
        cpu_and_ram_stats_layout = QHBoxLayout()
        incoming_and_outgoing_layout = QHBoxLayout()

        server_statistics_and_resources_container = QHBoxLayout()

        self.cpu_percentage_card = StatCard("CPU Usage", f"{self.cpu_usage}%")
        self.ram_usage_card = StatCard("RAM Usage", f"{self.ram_usage}MB")
        self.incoming_card = StatCard("Incoming", f"{self.incoming}KB/s")
        self.outgoing_card = StatCard("Outgoing", f"{self.outgoing}KB/s")

        cpu_and_ram_stats_layout.addWidget(self.cpu_percentage_card)
        cpu_and_ram_stats_layout.addWidget(self.ram_usage_card)

        incoming_and_outgoing_layout.addWidget(self.incoming_card)
        incoming_and_outgoing_layout.addWidget(self.outgoing_card)

        server_resouces_layout.addLayout(cpu_and_ram_stats_layout)
        server_resouces_layout.addLayout(incoming_and_outgoing_layout)

        server_statistics_and_resources_container.addWidget(server_resources)
        server_statistics_and_resources_container.addWidget(server_info)

        recent_logs_and_active_clients_container = QHBoxLayout()

        recent_logs_card = QFrame()
        recent_logs_card.setObjectName("recent_logs_card")
        recent_logs_card.setStyleSheet("""
            QFrame#recent_logs_card {
                background-color: #111827;
                border: 1px solid #23304a;
                border-radius: 7px;
            }
        """)
        recent_logs_card_layout = QVBoxLayout(recent_logs_card)

        recent_logs_card_header_layout = QHBoxLayout()

        recent_logs_label = QLabel("Recent Logs")

        view_all_logs_label = QLabel("View all logs >")

        recent_logs_card_header_layout.addWidget(recent_logs_label)
        recent_logs_card_header_layout.addStretch()
        recent_logs_card_header_layout.addWidget(view_all_logs_label)

        recent_logs_card_layout.addLayout(recent_logs_card_header_layout)
        
        recent_logs_and_active_clients_container.addWidget(recent_logs_card)

        active_clients_card = QFrame()
        active_clients_card.setObjectName("active_clients_card")
        active_clients_card.setStyleSheet("""
            QFrame#active_clients_card {
                background-color: #111827;
                border: 1px solid #23304a;
                border-radius: 7px;
            }
        """)
        active_clients_card_layout = QVBoxLayout(active_clients_card)

        self.active_clients_card_first_clients_layout = QVBoxLayout()

        active_clients_card_header_layout = QHBoxLayout()

        active_clients_label = QLabel("Active Clients")

        view_all_clients_label = QLabel("View all clients >")

        active_clients_card_header_layout.addWidget(active_clients_label)
        active_clients_card_header_layout.addStretch()
        active_clients_card_header_layout.addWidget(view_all_clients_label)

        active_clients_card_layout.addLayout(active_clients_card_header_layout)
        active_clients_card_layout.addLayout(self.active_clients_card_first_clients_layout)

        recent_logs_and_active_clients_container.addWidget(active_clients_card)

        ssl_box = QGroupBox("SSL Certificate Files")
        ssl_box_layout = QVBoxLayout()
        certificate_file_layout = QHBoxLayout()
        key_file_layout = QHBoxLayout()

        databases_box = QGroupBox("Database files")
        database_files_layout = QVBoxLayout()
        users_database_layout = QHBoxLayout()
        messages_database_layout = QHBoxLayout()

        server_control_box = QGroupBox()
        server_control_box_layout = QVBoxLayout()
        server_buttons_layout = QHBoxLayout()

        server_folder_layout = QHBoxLayout()

        certificate_file_label = QLabel("Certificate file:")
        self.certificate_file_input = QLineEdit()

        key_file_label = QLabel("Key file:")
        self.key_file_input = QLineEdit()

        users_database_file_label = QLabel("Users database file:")
        self.users_database_file_input = QLineEdit()

        messages_database_file_label = QLabel("Messages database file:")
        self.messages_database_file_input = QLineEdit()

        self.start_server_button = QPushButton("Start Server")
        self.start_server_button.clicked.connect(self.start_server)
        self.stop_server_button = QPushButton("Stop Server")
        self.stop_server_button.clicked.connect(self.stop_server)
        self.stop_server_button.setEnabled(False)

        server_status_label = QLabel("Server Status:")
        self.server_status_state = QLabel("Stopped")

        server_uptime_label = QLabel("Server Uptime")
        self.server_uptime_time = QLabel("Time")

        server_folder_button = QPushButton()
        server_folder_button.setIcon(QIcon(f"{image_path}/folder.png"))
        server_folder_button.setIconSize(QSize(15, 15))
        server_folder_button.setFixedSize(35, 35)
        server_folder_button.clicked.connect(self.open_server_folder)

        certificate_file_layout.addWidget(certificate_file_label)
        certificate_file_layout.addWidget(self.certificate_file_input)

        key_file_layout.addWidget(key_file_label)
        key_file_layout.addWidget(self.key_file_input)

        ssl_box_layout.addLayout(certificate_file_layout)
        ssl_box_layout.addLayout(key_file_layout)

        ssl_box.setLayout(ssl_box_layout)

        users_database_layout.addWidget(users_database_file_label)
        users_database_layout.addWidget(self.users_database_file_input)

        messages_database_layout.addWidget(messages_database_file_label)
        messages_database_layout.addWidget(self.messages_database_file_input)

        database_files_layout.addLayout(users_database_layout)
        database_files_layout.addLayout(messages_database_layout)

        databases_box.setLayout(database_files_layout)

        server_buttons_layout.addWidget(self.start_server_button)
        server_buttons_layout.addWidget(self.stop_server_button)

        server_control_box_layout.addLayout(server_buttons_layout)

        server_folder_layout.addStretch()
        server_folder_layout.addWidget(server_folder_button)

        server_control_box.setLayout(server_control_box_layout)

        layout.addLayout(cards_layout)
        layout.addLayout(server_statistics_and_resources_container)
        layout.addLayout(recent_logs_and_active_clients_container)
        layout.addWidget(ssl_box)
        layout.addWidget(databases_box)
        layout.addWidget(server_control_box)
        layout.addLayout(server_folder_layout)

        self.certificate_file_input.setEnabled(False)
        self.key_file_input.setEnabled(False)
        self.users_database_file_input.setEnabled(False)
        self.messages_database_file_input.setEnabled(False)

        self.fill_inputs(self.files)

    def fill_inputs(self, files):
        for file_path in files:
            if file_path.endswith(".crt"):
                self.certificate_file_input.setText(file_path)

            elif file_path.endswith(".key"):
                self.key_file_input.setText(file_path)

            elif file_path.endswith("users.db"):
                self.users_database_file_input.setText(file_path)
                
            elif file_path.endswith("messages.db"):
                self.messages_database_file_input.setText(file_path)

    def start_server(self):
        if not self.certificate_file_input.text() or not self.key_file_input.text():
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

class StatCard(QFrame):
    def __init__(self, title, value):
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
        self.value_label.setStyleSheet("""
            QLabel {
                color: #4ade80;
                font-size: 17px;
                font-weight: 700px;
            }
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