import requests
import os
from packaging import version
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import platform
from client_modules.path_finder import updater_executable_path, bitewire_executable_path

class UpdateChecker(QWidget):
    update_found = Signal(str)

    def __init__(self, parent, file_root, on_cancel):
        super().__init__()
        self.current_release = "2.1.0"
        self.latest_release = None
        self.url = "https://api.github.com/repos/Ziggx5/BiteWire/releases"
        self.on_cancel = on_cancel
        self.download_link = None
        self.system = None
        self.file_root = file_root
        self.parent = parent
        self.sha256 = None

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
        update_image.setPixmap(QPixmap(f"{self.file_root}/client_pictures/update_wheel.png").scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))

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

        self.note_label = QLabel()
        self.note_label.setWordWrap(True)
        self.note_label.setFixedWidth(350)
        self.note_label.setStyleSheet("""
        QLabel {
            color: #8b949e;
            font-size: 10px;
        }
        """)

        self.update_button = QPushButton("Download")
        self.update_button.setFixedSize(110, 35)
        self.update_button.setIcon(QIcon(f"{self.file_root}/client_pictures/update_white.png"))
        self.update_button.setIconSize(QSize(18, 18))
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_button.clicked.connect(lambda: self.open_updater())
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

        update_button_layout.addWidget(self.note_label)
        update_button_layout.addStretch()
        update_button_layout.addWidget(self.later_button)
        update_button_layout.addSpacing(8)
        update_button_layout.addWidget(self.update_button)

        update_page_layout.addLayout(header_page_horizontal_layout)
        update_page_layout.addWidget(upper_line)
        update_page_layout.addSpacing(10)
        update_page_layout.addWidget(scroll)
        update_page_layout.addSpacing(10)
        update_page_layout.addWidget(bottom_line)
        update_page_layout.addLayout(update_button_layout)

    def detect_os(self):
        if platform.system() == "Windows":
            self.system = "windows"
            self.note_label.setText("NOTE: Windows may block the updater because it is not yet recognized or digitally signed."
                                    " Make sure the app was downloaded from official BiteWire source and allow it through the Windows security prompt.")

            return "update.zip"
        else:
            self.system = "linux"
            self.note_label.setText("NOTE: Linux may ask for your password during the update.")

            if os.path.exists("/usr/bin/apt"):
                return ".deb"
            else:
                return ".rpm"

    def check_update(self):
        try:
            file_type = self.detect_os()
            response = requests.get(self.url, timeout = 2)
            data = response.json()

            if response.status_code != 200:
                return None

            for release in data:
                tag = release["tag_name"]
                if tag.startswith("c"):
                    for asset in release["assets"]:
                        self.download_link = asset["browser_download_url"]
                        self.sha256 = asset['digest'].split(":")[1]
                        self.file_size.setText(f"{asset['size'] / 1024 / 1024:.2f} MB")
                        if self.download_link.endswith(file_type):
                            break
                    split_release = tag[1:]
                    if version.parse(split_release) > version.parse(self.current_release):
                        self.latest_release = split_release
                        self.update_found.emit(self.latest_release)
                        self.new_version_label.setText(f"Version {self.latest_release}")
                        self.description.setMarkdown(release["body"])
                        break
            return None

        except:
            return None

    def open_updater(self):
        if self.system == "windows":
            updater_executable = "release/BiteWireUpdater.exe"
            bitewire_executable = "BiteWire.exe"
        else:
            updater_executable = "BiteWireUpdater"
            bitewire_executable = "bitewire"

        updater_path = os.path.join(updater_executable_path(), updater_executable)
        bitewire_path = os.path.join(bitewire_executable_path(), bitewire_executable)

        qt_library_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.LibrariesPath)
        qt_plugin_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)

        process = QProcess()

        env = QProcessEnvironment.systemEnvironment()
        env.remove("LD_LIBRARY_PATH")
        env.remove("QT_PLUGIN_PATH")

        process.setProcessEnvironment(env)
        process.setProgram(updater_path)
        process.setArguments(["--url", self.download_link,
                              "--current_version", self.current_release,
                              "--new_version", self.latest_release,
                              "--system", self.system,
                              "--bitewire_path", bitewire_path,
                              "--sha256", self.sha256,
                              "--qt_library_path", qt_library_path,
                              "--qt_plugin_path", qt_plugin_path])

        started = process.startDetached()

        if started:
            self.parent.hide()
            QTimer.singleShot(100, QApplication.quit)