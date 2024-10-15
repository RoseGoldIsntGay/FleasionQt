from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QStackedWidget, QVBoxLayout, QWidget
from qfluentwidgets import LineEdit, Pivot, PrimaryPushButton

from fleasion.util.files import replace_files


class CustomInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self)

        self.vBoxLayout.setSpacing(4)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addLayout(self.hBoxLayout)

        self.originalAssetLineEdit = LineEdit()
        self.originalAssetLineEdit.setPlaceholderText("Original Asset Id")
        self.originalAssetLineEdit.setMaximumWidth(256)
        self.hBoxLayout.addWidget(self.originalAssetLineEdit)

        self.newAssetLineEdit = LineEdit()
        self.newAssetLineEdit.setPlaceholderText("New Asset Id")
        self.newAssetLineEdit.setMaximumWidth(256)
        self.hBoxLayout.addWidget(self.newAssetLineEdit)

        self.saveButton = PrimaryPushButton("Save")
        self.saveButton.setMaximumWidth(68)
        self.saveButton.clicked.connect(self.save)
        self.vBoxLayout.addWidget(
            self.saveButton,
            0,
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight,
        )

        self.setLayout(self.vBoxLayout)

    def save(self):
        file_to_copy = self.newAssetLineEdit.text()
        files_to_replace = [self.originalAssetLineEdit.text()]

        if file_to_copy and files_to_replace:
            replace_files(file_to_copy=file_to_copy, files_to_replace=files_to_replace)


class ReplaceAssets(QWidget):
    NAME = "Replace Assets"

    def __init__(self):
        super().__init__()

        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.customInterface = CustomInterface(self)
        self.sightsInterface = QLabel("Sights Interface", self)
        self.armModelsInterface = QLabel("Arm Models Interface", self)
        self.sleevesInterface = QLabel("Sleeves Interface", self)

        self.addSubInterface(self.customInterface, "customInterface", "Custom")
        self.addSubInterface(self.sightsInterface, "sightsInterface", "Sights")
        self.addSubInterface(
            self.armModelsInterface, "armModelsInterface", "Arm Models"
        )
        self.addSubInterface(self.sleevesInterface, "sleevesInterface", "Sleeves")

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.customInterface)
        self.pivot.setCurrentItem(self.customInterface.objectName())

        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.resize(400, 400)

    def addSubInterface(self, widget: QWidget, objectName: str, text: str):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)

        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)

        if widget:
            self.pivot.setCurrentItem(widget.objectName())
