from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from client_modules.ui import MainUi

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(200, 250)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color : #0e1117;")

        self.value = 0

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        title = QLabel("BITWARE")
        title.setFont(QFont("Courier New", 20))
        title.setStyleSheet("color: #a5a8ad;")

        line = QLabel()
        line.setFixedSize(120, 2)
        line.setStyleSheet("background-color: #2554a1;")

        self.progress = QProgressBar()
        self.progress.setFixedSize(80, 5)
        self.progress.setRange(0, 100)
        self.progress.setStyleSheet("background-color: #1c1f26; border-radius: 4px;")

        self.label = QLabel("Loading...")
        self.label.setFont(QFont("Courier New", 10))
        self.label.setStyleSheet("color: #a5a8ad;")

        layout.addWidget(title, alignment = Qt.AlignCenter)
        layout.addWidget(line, alignment = Qt.AlignCenter)
        layout.addWidget(self.progress, alignment = Qt.AlignCenter)
        layout.addWidget(self.label, alignment = Qt.AlignCenter)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bar)
        self.timer.start(20)

    def update_progress_bar(self):
        if self.value < 100:
            self.value += 1
            self.progress.setValue(self.value)
        else:
            self.timer.stop()
            self.label.setText("Success!")
            self.close()
            self.MainUi = MainUi()
            self.MainUi.show()
            self.close()