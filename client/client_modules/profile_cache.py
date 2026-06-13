from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import base64

class ProfileCache(QObject):
    profile_picture = Signal(str)

    def __init__(self):
        super().__init__()
        self.cache = {}

    def save(self, data):
        for user_data in data:
            username = user_data['username']
            picture_bytes = user_data['image_bytes']

            decoded_bytes = base64.b64decode(picture_bytes)

            pixmap = QPixmap()
            pixmap.loadFromData(decoded_bytes)

            self.cache[username] = {
                "list_profile_picture": self.create_picture(pixmap, 30),
                "message_profile_picture": self.create_picture(pixmap, 35)
            }
            
            self.profile_picture.emit(username)

    def get(self, username, picture_type):
        user_cache = self.cache.get(username)

        if not user_cache:
            return None

        return user_cache.get(picture_type)

    def create_picture(self, pixmap, size):
        picture = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        icon = QPixmap(size, size)
        icon.fill(Qt.GlobalColor.transparent)

        painter = QPainter(icon)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, size, size)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, picture)
        painter.end()

        return icon