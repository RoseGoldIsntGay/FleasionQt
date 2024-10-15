from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class Settings(QWidget):
    NAME = "Settings"

    def __init__(self):
        super().__init__()

        self.setObjectName(Settings.NAME)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
