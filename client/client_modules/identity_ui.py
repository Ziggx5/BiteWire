from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class AddIdentityUi(QWidget):
    def __init__(self):
        super().__init__()

        self.on_cancel = on_cancel

        self.setWindowTitle("BitWire")
        self.setStyleSheet("background-color: #161b22")
        self.setFixedSize(500, 300)

        

