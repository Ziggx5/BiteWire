from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class AddIdentityUi(QWidget):
    def __init__(self):
        super().__init__()

        #self.on_cancel = on_cancel

        self.setWindowTitle("BitWire")
        self.setStyleSheet("background-color: #161b22")
        self.setFixedSize(500, 300)

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

        main_title = """
        QLabel {
            color: #e6edf3;
            font-size: 20px;
            font-weight: 600;
        }
        """
        
        add_identity_layout = QHBoxLayout(self)
        add_identity_layout.setSpacing(0)

        add_identity_left_layout = QVBoxLayout()
        add_identity_right_layout = QVBoxLayout()


        self.add_avatar_button = QPushButton()
        self.add_avatar_button.setFixedSize(160, 160)
        self.add_avatar_button.setStyleSheet("background-color: blue")
        self.add_avatar_button.setText("Select photo")

        title = QLabel("Add identity")
        title.setStyleSheet(main_title)
        title.setFixedHeight(30)

        username_label = QLabel("Username")
        username_label.setFont(QFont("Courier New,", 12))
        username_label.setStyleSheet("color: #a5a8ad;")
        username_label.setFixedHeight(20)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(input_style)


        password_label = QLabel("Password")
        password_label.setFont(QFont("Courier New,", 12))
        password_label.setStyleSheet("color: #a5a8ad;")
        password_label.setFixedHeight(20)

        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(input_style)

        add_identity_left_layout.addWidget(self.add_avatar_button)
        add_identity_right_layout.addWidget(title)
        add_identity_right_layout.addWidget(username_label)
        add_identity_right_layout.addWidget(self.username_input)
        add_identity_right_layout.addWidget(password_label)
        add_identity_right_layout.addWidget(self.password_input)

        add_identity_layout.addLayout(add_identity_left_layout)
        add_identity_layout.addLayout(add_identity_right_layout)