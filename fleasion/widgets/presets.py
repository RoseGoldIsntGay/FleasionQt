from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class Presets(QWidget):
    NAME = "Presets"

    def __init__(self):
        super().__init__()

        self.setObjectName(Presets.NAME)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
