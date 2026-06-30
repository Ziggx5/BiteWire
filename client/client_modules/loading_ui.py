from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from client_modules.main_ui import MainUi

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(200, 250)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("root")
        self.setStyleSheet("""
            QWidget#root {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0e1117,
                    stop:0.5 #151a22,
                    stop:1 #1a1f2b
                );
            }
        """)

        self.value = 0
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        lower_layout = QHBoxLayout()

        version_label = QLabel("Version 2.1.0")
        version_label.setStyleSheet("color: #a5a8ad; font: 10px;")
        creator_label = QLabel("Created by Ziggx5")
        creator_label.setStyleSheet("color: #a5a8ad; font: 10px;")

        lower_layout.addWidget(version_label)
        lower_layout.addStretch()
        lower_layout.addWidget(creator_label)

        title = QLabel("BiteWire")
        title.setStyleSheet("""
            QLabel {
                color: #e6edf3;
                font-size: 28px;
                font-weight: 600;
                letter-spacing: 1px;
            }
        """)

        line = QLabel()
        line.setFixedSize(120, 2)
        line.setStyleSheet("background-color: #3b82f6; border-radius: 1px;")

        self.progress = QProgressBar()
        self.progress.setFixedSize(80, 5)
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #1c1f26;
                border-radius: 2px;
            }

            QProgressBar::chunk {
                background-color: #3b82f6;
                border-radius: 2px;
            }
        """)

        self.label = QLabel("Loading...")
        self.label.setStyleSheet("color: #a5a8ad; font: 12px;")

        layout.addStretch()
        layout.addWidget(title, alignment = Qt.AlignCenter)
        layout.addWidget(line, alignment = Qt.AlignCenter)
        layout.addWidget(self.progress, alignment = Qt.AlignCenter)
        layout.addWidget(self.label, alignment = Qt.AlignCenter)
        layout.addStretch()
        layout.addLayout(lower_layout)
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
            QTimer.singleShot(1000, self.open_main_ui)

    def open_main_ui(self):
        self.close()
        self.MainUi = MainUi()
        self.MainUi.show()