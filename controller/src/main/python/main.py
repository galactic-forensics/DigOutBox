try:
    from PyQt6.QtWidgets import QMainWindow
    from fbs_runtime.application_context.PyQt6 import ApplicationContext
except ImportError:
    try:
        from PySide6.QtWidgets import QMainWindow
        from fbs_runtime.application_context.PySide6 import ApplicationContext
    except ImportError as e:
        raise ImportError("Please install either PyQt6 or PySide6.") from e


from qtpy import QtGui, QtWidgets

import sys


class DigOutBoxController(QtWidgets.QMainWindow):
    def __init__(self, appctxt: ApplicationContext) -> None:
        """Initialize the main window.

        :param appctxt: ApplicationContext object (fbs).
        """
        super().__init__(parent=None)
        self.setWindowTitle("DigOutBoxController")
        self.appctxt = appctxt

        self.resize(250, 150)

        # init GUI
        self.init_menubar()

    def init_menubar(self):
        """Initialize the menu bar."""
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        quit_action = QtWidgets.QAction(QtGui.QIcon(None), "&Quit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)


if __name__ == "__main__":
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    window = DigOutBoxController(appctxt)
    window.show()
    exit_code = appctxt.app.exec()  # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)
