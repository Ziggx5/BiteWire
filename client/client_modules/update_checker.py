from operator import truediv

import requests
import os
from packaging import version
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import platform
import threading

class UpdateChecker(QWidget):
    update_found = Signal(str)
    download_percent_signal = Signal(str)

    def __init__(self, image_path, on_cancel):
        super().__init__()
        self.current_release = "2.2.0"
        self.url = "https://api.github.com/repos/Ziggx5/BiteWire/releases"
        self.on_cancel = on_cancel
        self.download_link = None
        self.system = None
        self.download_percent_signal.connect(lambda p: self.download_percent.setText(p))
        self.stop_download_event = threading.Event()

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

        file_size_widget = QWidget()
        file_size_widget.setFixedSize(110, 35)
        file_size_widget.setStyleSheet("""
        QWidget {
            background-color: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 3px;
            }    
        """)

        file_size_layout = QHBoxLayout(file_size_widget)
        file_size_layout.setContentsMargins(10, 0, 10, 0)

        self.file_size = QLabel("size")
        self.file_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_size.setStyleSheet("""
        QLabel {
            color: #60a5fa;
            font-size: 14px;
            font-weight: 600;
            background: transparent;
            border: none;
            }
        """)

        file_size_layout.addWidget(self.file_size)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(10)
        cards_layout.addWidget(version_widget)
        cards_layout.addWidget(file_size_widget)
        cards_layout.addStretch()

        header_page_vertical_layout.addWidget(update_label)
        header_page_vertical_layout.addWidget(subtitle_label)
        header_page_vertical_layout.addSpacing(10)
        header_page_vertical_layout.addLayout(cards_layout)

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

        self.description = QTextBrowser()
        self.description.setReadOnly(True)
        self.description.setContentsMargins(0, 0, 0, 0)
        self.description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.description.setStyleSheet("""
            QTextBrowser {
                font-size: 15px;
                color: #c9d1d9;
                padding: 10px;
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

        self.update_button = QPushButton("Download")
        self.update_button.setFixedSize(110, 35)
        self.update_button.setIcon(QIcon(f"{image_path}/update_white.png"))
        self.update_button.setIconSize(QSize(18, 18))
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_button.clicked.connect(lambda: self.start_download())
        self.update_button.setStyleSheet("""
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

        self.later_button = QPushButton("Later")
        self.later_button.setFixedSize(110, 35)
        self.later_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.later_button.clicked.connect(self.on_cancel)
        self.later_button.setStyleSheet("""
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

        download_path_frame = QFrame()
        download_path_frame.setStyleSheet("""
        QFrame {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
            }
        """)
        download_path_frame_layout = QHBoxLayout(download_path_frame)

        self.download_path_label = QLabel(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation))
        self.download_path_label.setStyleSheet("""
        QLabel {
            color: #8b949e;
            font-size: 13px;
            border: None;
            }
        """)

        self.edit_download_path_button = QPushButton("Browse...")
        self.edit_download_path_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_download_path_button.setFixedSize(60, 30)
        self.edit_download_path_button.clicked.connect(lambda: self.select_download_folder())
        self.edit_download_path_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: None;
            border-radius: 6px;
            }
        
        QPushButton:hover {
            background-color: #30363d;
            }
        """)

        download_path_frame_layout.addWidget(self.download_path_label)
        download_path_frame_layout.addWidget(self.edit_download_path_button)

        self.download_percent = QLabel()
        self.download_percent.setVisible(False)

        self.cancel_download_button = QPushButton("Cancel")
        self.cancel_download_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_download_button.setFixedSize(60, 30)
        self.cancel_download_button.setVisible(False)
        self.cancel_download_button.clicked.connect(lambda: self.stop_download())

        update_button_layout.addWidget(download_path_frame)
        update_button_layout.addStretch()
        update_button_layout.addWidget(self.later_button)
        update_button_layout.addSpacing(8)
        update_button_layout.addWidget(self.update_button)
        update_button_layout.addWidget(self.cancel_download_button)
        update_button_layout.addWidget(self.download_percent)

        update_page_layout.addLayout(header_page_horizontal_layout)
        update_page_layout.addWidget(upper_line)
        update_page_layout.addSpacing(10)
        update_page_layout.addWidget(scroll)
        update_page_layout.addSpacing(10)
        update_page_layout.addWidget(bottom_line)
        update_page_layout.addLayout(update_button_layout)

    def detect_os(self):
        if platform.system() == "Windows":
            return ".exe"
        else:
            if os.path.exists("/usr/bin/apt"):
                return ".deb"
            else:
                return ".rpm"

    def check_update(self):
        try:
            self.system = self.detect_os()
            response = requests.get(self.url, timeout = 2)
            data = response.json()

            if response.status_code != 200:
                return None

            for release in data:
                tag = release["tag_name"]
                if tag.startswith("c"):
                    for asset in release["assets"]:
                        self.download_link = asset["browser_download_url"]
                        self.file_size.setText(f"{asset['size'] / 1024 / 1024:.2f} MB")
                        if self.download_link.endswith(self.system):
                            break
                    split_release = tag[1:]
                    if version.parse(split_release) > version.parse(self.current_release):
                        latest_release = split_release
                        self.update_found.emit(latest_release)
                        self.new_version_label.setText(f"Version {latest_release}")
                        self.description.setMarkdown(release["body"])
                        break
            return None

        except:
            return None

    def download_file(self):
        self.stop_download_event.clear()
        response = requests.get(self.download_link, stream = True)
        total = int(response.headers.get('content-length'))
        file_name = response.headers.get('content-disposition').split("filename=")[1]
        downloaded = 0

        with open (f"{self.download_path_label.text()}/{file_name}", "wb") as f:
            for chunk in response.iter_content(8192):
                if self.stop_download_event.is_set():
                    f.close()
                    os.remove(f"{self.download_path_label.text()}/{file_name}")
                    return
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    percent = downloaded / total * 100
                    self.download_percent_signal.emit(f"{int(percent)}%")

            self.download_percent_signal.emit("New app version downloaded successfully! Close the app now.")

    def start_download(self):
        self.download_percent.setVisible(True)
        self.cancel_download_button.setVisible(True)
        self.update_button.setVisible(False)
        self.later_button.setVisible(False)
        self.edit_download_path_button.setEnabled(False)
        threading.Thread(target=self.download_file, daemon=True).start()

    def select_download_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", self.download_path_label.text())
        if folder:
            self.download_path_label.setText(folder)

    def stop_download(self):
        self.stop_download_event.set()
        self.download_percent.setVisible(False)
        self.cancel_download_button.setVisible(False)

        self.update_button.setVisible(True)
        self.later_button.setVisible(True)
        self.edit_download_path_button.setEnabled(True)