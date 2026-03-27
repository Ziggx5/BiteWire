from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QPainter, QPainterPath
import os
from client_modules.path_finder import file_root
from client_modules.data_manipulation import save_identity_data, pictures_file

class AddIdentityUi(QWidget):
    def __init__(self, on_cancel):
        super().__init__()

        self.on_cancel = on_cancel
        self.rounded = None
        self.picture_path = file_root()

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

        main_page = QWidget(self)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_page)
        add_identity_layout = QVBoxLayout(main_page)
        add_identity_layout.setContentsMargins(10, 10, 10, 10)
        add_identity_layout.setSpacing(0)

        add_identity_upper_layout = QHBoxLayout()
        add_identity_left_layout = QVBoxLayout()
        add_identity_right_layout = QVBoxLayout()
        add_identity_right_layout.setSpacing(8)
        add_identity_lower_layout = QHBoxLayout()

        bot_line = QFrame()
        bot_line.setFrameShape(QFrame.HLine)
        bot_line.setStyleSheet("color: #30363d;")

        self.profile_picture_widget = QWidget()
        self.profile_picture_widget.setFixedSize(160, 160)
        self.profile_picture_widget.mousePressEvent = self.select_picture
        self.profile_picture_widget.setStyleSheet("""
            QWidget { 
                background-color: #0d1117;
                border: 2px dashed #30363d;
                border-radius: 80px;
                color: #8b949e;
            }

            QWidget:hover {
            border: 2px solid #58a6ff;
            background-color: #0f141a;
            }
        """)
        profile_picture_layout = QVBoxLayout(self.profile_picture_widget)

        self.profile_picture = QLabel()
        self.profile_picture.setPixmap(QPixmap(f"{self.picture_path}/camera.png").scaled(80, 80))
        self.profile_picture.setStyleSheet("border: None; background-color: transparent;")

        self.profile_picture_subtitle = QLabel("Select photo")
        self.profile_picture_subtitle.setStyleSheet("border: None; background-color: transparent;")

        profile_picture_layout.setAlignment(Qt.AlignCenter)
        profile_picture_layout.addWidget(self.profile_picture)
        profile_picture_layout.addWidget(self.profile_picture_subtitle)

        title = QLabel("Add new identity")
        title.setStyleSheet("""
            QLabel {
                color: #e6edf3;
                font-size: 20px;
                font-weight: 600;
            }
        """)
        title.setFixedHeight(30)

        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #a5a8ad; font-size: 15px;")
        username_label.setFixedHeight(20)

        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(input_style)
        self.username_input.setPlaceholderText("Enter username")

        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #a5a8ad; font-size: 15px;")
        password_label.setFixedHeight(20)
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(input_style)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(110, 35)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6e6e6e;
                font-weight: 600;
                border-radius: 5px;
                border: 1px solid #30363d;
            }
            QPushButton:hover {
                background-color: #878787;
            }
        """)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setFixedSize(110, 35)
        self.confirm_button.setCursor(Qt.PointingHandCursor)
        self.confirm_button.clicked.connect(self.save_identity)
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #175723;
                font-weight: 600;
                border-radius: 5px;
                border: 1px solid #30363d;
            }

            QPushButton:hover {
                background-color: #1e732e;
            }
        """)

        self.all_identities_button = QPushButton("Identities")
        self.all_identities_button.setFixedSize(110, 35)
        self.all_identities_button.setCursor(Qt.PointingHandCursor)
        self.all_identities_button.setStyleSheet("""
            QPushButton {
            background-color: #1f6feb;
            font-weight: 600;
            border-radius: 5px;
            border: 1px solid #30363d;
            }

            QPushButton:hover {
            background-color: #388bfd;
            }
        """)

        add_identity_left_layout.addWidget(self.profile_picture_widget)

        add_identity_right_layout.addWidget(title)
        add_identity_right_layout.addWidget(username_label)
        add_identity_right_layout.addWidget(self.username_input)
        add_identity_right_layout.addWidget(password_label)
        add_identity_right_layout.addWidget(self.password_input)

        add_identity_upper_layout.addLayout(add_identity_left_layout)
        add_identity_upper_layout.addSpacing(30)
        add_identity_upper_layout.addLayout(add_identity_right_layout)

        add_identity_lower_layout.addStretch()
        add_identity_lower_layout.addWidget(self.all_identities_button)
        add_identity_lower_layout.addSpacing(10)
        add_identity_lower_layout.addWidget(self.cancel_button)
        add_identity_lower_layout.addSpacing(10)
        add_identity_lower_layout.addWidget(self.confirm_button)

        add_identity_layout.addLayout(add_identity_upper_layout)
        add_identity_layout.addStretch()
        add_identity_layout.addWidget(bot_line)
        add_identity_layout.addSpacing(10)
        add_identity_layout.addLayout(add_identity_lower_layout)

        main_page.setLayout(add_identity_layout)

    def select_picture(self, event):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select profile picture", "", "Images (*.png *.jpg *.jpeg)")
        
        if file_path:
            pixmap = QPixmap(file_path).scaled(160, 160, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.rounded = QPixmap(160, 160)
            self.rounded.fill(Qt.transparent)

            painter = QPainter(self.rounded)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)

            path = QPainterPath()
            path.addEllipse(0, 0, 160, 160)
            
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()

            self.profile_picture.setPixmap(self.rounded)
            self.profile_picture.setScaledContents(True)
            self.profile_picture_subtitle.hide()

    def save_identity(self):
        profile_pictures_folder_path = pictures_file()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        profile_picture = self.rounded
        
        if username and password and profile_picture:
            profile_picture_path = os.path.join(profile_pictures_folder_path, f"{username}.png")
            profile_picture.save(profile_picture_path)
            save_identity_data(username, password, profile_picture_path)
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Please enter username, password and profile picture."
            )