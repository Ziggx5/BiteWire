import requests
import os
from packaging import version
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import markdown

class UpdateChecker(QWidget):
    update_found = Signal(str)

    def __init__(self, image_path, on_cancel):
        super().__init__()
        self.current_release = "2.0.0"
        self.url = "https://api.github.com/repos/Ziggx5/BiteWire/releases"
        self.on_cancel = on_cancel

        self.setFixedSize(650, 550)
        self.setStyleSheet("background-color: transparent;")

        update_page_layout = QVBoxLayout(self)
        header_page_horizontal_layout = QHBoxLayout()
        header_page_vertical_layout = QVBoxLayout()
        update_button_layout = QHBoxLayout()

        update_image_widget = QWidget()
        update_image_widget.setObjectName("update_image_widget")
        update_image_widget.setFixedSize(100, 100)
        update_image_widget.setStyleSheet("""
            QWidget#update_image_widget {
                background-color: rgba(255, 255, 255, 0.04);
                border-radius: 50px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)

        update_image_layout = QVBoxLayout(update_image_widget)

        update_image = QLabel()
        update_image.setFixedSize(60, 60)
        update_image.setPixmap(QPixmap(f"{image_path}/update_wheel.png").scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))

        update_image_layout.addWidget(update_image, alignment = Qt.AlignmentFlag.AlignCenter)

        update_label = QLabel("Update available")
        update_label.setStyleSheet("font-size: 22px; font-weight: 600;")

        subtitle_label = QLabel("A new version of BiteWire is ready to install.")
        subtitle_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #b3b3b3;")

        version_widget = QWidget()
        version_widget.setFixedSize(110, 35)
        version_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(59, 130, 246, 0.15);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 3px;
            }    
        """)

        version_widget_layout = QHBoxLayout(version_widget)
        version_widget_layout.setContentsMargins(10, 0, 10, 0)

        self.new_version_label = QLabel("version")
        self.new_version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.new_version_label.setStyleSheet("""
            QLabel {
                color: #60a5fa;
                font-size: 14px;
                font-weight: 600;
                background: transparent;
                border: none;
            }
        """)

        version_widget_layout.addWidget(self.new_version_label)

        header_page_vertical_layout.addWidget(update_label)
        header_page_vertical_layout.addWidget(subtitle_label)
        header_page_vertical_layout.addWidget(version_widget)

        header_page_horizontal_layout.addWidget(update_image_widget, alignment = Qt.AlignmentFlag.AlignLeft)
        header_page_horizontal_layout.addSpacing(10)
        header_page_horizontal_layout.addLayout(header_page_vertical_layout)
        header_page_horizontal_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #30363d;
                background: #0d1117;
                border-radius: 10px;
            }
        """)

        scroll_content = QWidget()

        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setContentsMargins(0, 0, 0, 0)
        self.description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.description.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: #c9d1d9;
                padding: 10px;
                line-height: 22px;
            }
        """)

        scroll_layout.addWidget(self.description)
        scroll.setWidget(scroll_content)

        upper_line = QFrame()
        upper_line.setFrameShape(QFrame.Shape.HLine)
        upper_line.setStyleSheet("color: #30363d;")

        bottom_line = QFrame()
        bottom_line.setFrameShape(QFrame.Shape.HLine)
        bottom_line.setStyleSheet("color: #30363d;")

        update_button = QPushButton("Download")
        update_button.setFixedSize(110, 35)
        update_button.setIcon(QIcon(f"{image_path}/update_white.png"))
        update_button.setIconSize(QSize(18, 18))
        update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        update_button.setStyleSheet("""
            QPushButton {
                background-color: #1f6feb;
                border-radius: 4px;
                padding: 8px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #388bfd; 
            }
        """)

        later_button = QPushButton("Later")
        later_button.setFixedSize(110, 35)
        later_button.setCursor(Qt.CursorShape.PointingHandCursor)
        later_button.clicked.connect(self.on_cancel)
        later_button.setStyleSheet("""
            QPushButton {
                background-color: #21262d;
                color: #c9d1d9;
                border-radius: 4px;
                padding: 8px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #30363d; 
            }
        """)

        update_button_layout.addStretch()
        update_button_layout.addWidget(later_button)
        update_button_layout.addSpacing(8)
        update_button_layout.addWidget(update_button)

        update_page_layout.addLayout(header_page_horizontal_layout)
        update_page_layout.addWidget(upper_line)
        update_page_layout.addSpacing(10)
        update_page_layout.addWidget(scroll)
        update_page_layout.addSpacing(10)
        update_page_layout.addWidget(bottom_line)
        update_page_layout.addLayout(update_button_layout)

    def check_update(self):
        try:
            response = requests.get(self.url, timeout = 2)
            data = response.json()

            if response.status_code != 200:
                return None

            for release in data:
                tag = release["tag_name"]
                if tag.startswith("c"):
                    split_release = tag[1:]
                    if version.parse(split_release) > version.parse(self.current_release):
                        latest_release = split_release
                        self.update_found.emit(latest_release)
                        self.new_version_label.setText(f"Version {latest_release}")
                        html = markdown.markdown(release["body"])
                        self.description.setText(html)
                        break
            return None

        except:
            return None