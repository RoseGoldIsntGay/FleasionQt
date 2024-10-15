import os
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QStackedWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import NavigationInterface, NavigationItemPosition, Theme, setTheme
from qframelesswindow import FramelessWindow, TitleBar

from fleasion.util.constants import RESOURCES_DIR
from fleasion.widgets.cache_settings import CacheSettings
from fleasion.widgets.presets import Presets
from fleasion.widgets.replace_assets import ReplaceAssets
from fleasion.widgets.settings import Settings

APP_NAME = "FleasionQt"
ICON_SIZE = QSize(22, 22)


class CustomTitleBar(TitleBar):
    """Title bar with icon and title"""

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(ICON_SIZE)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(
            1,
            self.iconLabel,
            0,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom,
        )
        self.window().windowIconChanged.connect(self.setIcon)  # type: ignore

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(
            2,
            self.titleLabel,
            0,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom,
        )
        self.titleLabel.setObjectName("titleLabel")
        self.window().windowTitleChanged.connect(self.setTitle)  # type: ignore

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon: QIcon) -> None:
        self.iconLabel.setPixmap(icon.pixmap(ICON_SIZE))


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        # use dark theme mode
        setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)

        self.replaceAssets = ReplaceAssets()
        self.presets = Presets()
        self.cacheSettings = CacheSettings()
        self.settings = Settings()

        self.initLayout()

        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.addSubInterface(
            self.replaceAssets,
            FIF.PALETTE,
            self.replaceAssets.NAME,
        )
        self.addSubInterface(self.presets, FIF.BOOK_SHELF, self.presets.NAME)
        self.addSubInterface(
            self.cacheSettings,
            FIF.DEVELOPER_TOOLS,
            self.cacheSettings.NAME,
        )

        self.navigationInterface.addSeparator()

        self.addSubInterface(
            self.settings,
            FIF.SETTING,
            self.settings.NAME,
            NavigationItemPosition.BOTTOM,
        )

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.navigationInterface.setCurrentItem(self.replaceAssets.objectName())

    def initWindow(self):
        self.resize(1000, 600)
        self.setWindowIcon(QIcon(os.path.join(RESOURCES_DIR, "icons/fleasion.ico")))
        self.setWindowTitle(APP_NAME)
        self.setQss()

    def addSubInterface(
        self,
        interface,
        icon,
        text: str,
        position=NavigationItemPosition.TOP,
    ):
        """add sub interface"""
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
        )

    def setQss(self):
        with open(
            os.path.join(RESOURCES_DIR, "dark_mode.qss"),
            encoding="utf-8",
        ) as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        if widget:
            self.navigationInterface.setCurrentItem(widget.objectName())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    w = Window()
    w.show()
    sys.exit(app.exec())
