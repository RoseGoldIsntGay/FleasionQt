from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class Home(QWidget):
    NAME = "Home"

    def __init__(self):
        super().__init__()

        self.setObjectName(Home.NAME)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
