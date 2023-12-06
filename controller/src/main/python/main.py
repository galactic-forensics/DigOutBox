"""Main interface for DigOutBoxController."""

# Detect if PyQt6 or PySide6 are installed
try:
    from PyQt6.QtWidgets import QMainWindow
    from fbs_runtime.application_context.PyQt6 import ApplicationContext
except ImportError:
    try:
        from PySide6.QtWidgets import QMainWindow
        from fbs_runtime.application_context.PySide6 import ApplicationContext
    except ImportError as e:
        raise ImportError("Please install either PyQt6 or PySide6.") from e

# Detect if fbs is installed
try:
    from fbs_runtime import PUBLIC_SETTINGS as fbsrt_public_settings
    from fbs_runtime.application_context.PyQt6 import ApplicationContext
    import fbs_runtime.platform as fbsrt_platform
except ImportError:
    fbsrt_public_settings = {"version": "Unknown"}
    ApplicationContext = None
    fbsrt_platform = None

import json
from pathlib import Path
import sys
import warnings

from qtpy import QtGui, QtWidgets, QtCore

from channel_setup import ChannelSetup
from widgets import ChannelAndGroupWidget


class DigOutBoxController(QtWidgets.QMainWindow):
    def __init__(self, is_windows=False) -> None:
        """Initialize the main window.

        :param is_windows: Whether the current platform is windows.
        """
        super().__init__(parent=None)

        self.setWindowTitle("DigOutBoxController")
        self.resize(250, 150)

        self.is_windows = is_windows

        self.app_local_path = None
        self.init_local_profile()

        # statusbar
        self.statusbar = self.statusBar()
        self.statusbartime = 3000  # time in ms to display messages
        self.setStatusBar(self.statusbar)

        # init GUI
        self.init_menubar()

        # load config and settings
        self._channels = {}
        self.channel_widgets_individual = None
        self.channel_widgets_grouped = None
        self.load_file()

    def init_local_profile(self):
        """Initialize a user's local profile, platform dependent."""
        if self.is_windows:
            app_local_path = Path.home().joinpath("AppData/Roaming/DigOutBox/")
        else:
            app_local_path = Path.home().joinpath(".config/DigOutBox/")
        app_local_path.mkdir(parents=True, exist_ok=True)
        self.app_local_path = app_local_path

    def init_menubar(self):
        """Initialize the menu bar."""
        menubar = self.menuBar()

        # file menu

        file_menu = menubar.addMenu("&File")

        load_action = QtWidgets.QAction(QtGui.QIcon(None), "&Load", self)
        load_action.setStatusTip("Load a saved configuration")
        load_action.triggered.connect(lambda: self.load_file(ask_fname=True))

        save_action = QtWidgets.QAction(QtGui.QIcon(None), "&Save", self)
        save_action.setStatusTip("Save current settings and configuration")
        save_action.triggered.connect(self.save)

        save_as_action = QtWidgets.QAction(QtGui.QIcon(None), "Save &As", self)
        save_as_action.setStatusTip("Save current configuration as...")
        save_as_action.triggered.connect(lambda: self.save(ask_fname=True))

        quit_action = QtWidgets.QAction(QtGui.QIcon(None), "&Quit", self)
        quit_action.setStatusTip("Quit DigOutBoxController")
        quit_action.triggered.connect(self.close)

        file_menu.addAction(load_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(quit_action)

        # config menu

        file_menu = menubar.addMenu("&Config")

        channel_config_action = QtWidgets.QAction(QtGui.QIcon(None), "&Channels", self)
        channel_config_action.setStatusTip("Configure channels")
        channel_config_action.triggered.connect(self.config_channels)

        group_config_action = QtWidgets.QAction(QtGui.QIcon(None), "&Groups", self)
        group_config_action.setStatusTip("Configure channel groups")
        group_config_action.triggered.connect(self.config_groups)

        settings_action = QtWidgets.QAction(QtGui.QIcon(None), "&Settings", self)
        settings_action.setStatusTip("Configure settings")
        settings_action.triggered.connect(self.settings)

        file_menu.addAction(channel_config_action)
        file_menu.addAction(group_config_action)
        file_menu.addSeparator()
        file_menu.addAction(settings_action)

        # help menu

        help_menu = menubar.addMenu("&Help")

        about_action = QtWidgets.QAction(QtGui.QIcon(None), "&About", self)
        about_action.setStatusTip("About DigOutBoxController")
        about_action.triggered.connect(self.about)

        help_menu.addAction(about_action)

    def build_ui(self):
        """Setup the UI with all the channels.

        This sets up the main widget from scratch and can be called while the GUI is
        running.
        """
        outer_layout = QtWidgets.QVBoxLayout()

        individual_channels_layout = QtWidgets.QVBoxLayout()
        for channel_widget in self.channel_widgets_individual:
            individual_channels_layout.addWidget(channel_widget)
        individual_channels_layout.addStretch()

        grouped_channels_layout = QtWidgets.QVBoxLayout()
        for channel_widget in self.channel_widgets_grouped:
            grouped_channels_layout.addWidget(channel_widget)
        grouped_channels_layout.addStretch()

        channels_layout = QtWidgets.QHBoxLayout()
        if len(self.channel_widgets_individual) > 0:
            channels_layout.addLayout(individual_channels_layout)
        if (
            len(self.channel_widgets_individual) > 0
            and len(self.channel_widgets_grouped) > 0
        ):
            channels_layout.addStretch()
        if len(self.channel_widgets_grouped) > 0:
            channels_layout.addLayout(grouped_channels_layout)

        outer_layout.addLayout(channels_layout)

        # "All On" and "All Off" buttons at the bottom of the window
        all_on_off_layout = QtWidgets.QHBoxLayout()
        all_on_off_layout.addStretch()

        all_on_button = QtWidgets.QPushButton("All On")
        all_on_button.setToolTip("Turn all channels on")
        all_on_button.clicked.connect(lambda: self.set_all_channels(state=True))

        all_off_button = QtWidgets.QPushButton("All Off")
        all_off_button.setToolTip("Turn all channels off")
        all_off_button.clicked.connect(lambda: self.set_all_channels(state=False))

        all_on_off_layout.addWidget(all_on_button)
        all_on_off_layout.addWidget(all_off_button)

        outer_layout.addLayout(all_on_off_layout)

        # create a new main widget and set it as the central widget
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(outer_layout)
        self.setCentralWidget(self.main_widget)

    def about(self):
        """Show the about dialog."""
        QtWidgets.QMessageBox.about(
            self,
            "About DigOutBoxController",
            "DigOutBoxController is a GUI for the DigOutBox.\n\n"
            "Help can be found on GitHub:\n"
            "https://github.com/galactic-forensics/DigOutBox\n\n"
            "If you have issues, please report them on GitHub.\n",
        )

    def config_channels(self):
        """Configure the channels."""
        dialog = ChannelSetup(self, channels=self._channels)
        if dialog.exec():
            self._channels = dialog.channels
            self.load_channels()
            self.save()
        else:
            print("None")

    def config_groups(self):
        """Configure the groups."""
        # todo
        pass

    def load_channels(self):
        """Load the channels into the GUI."""
        # fill channel widgets
        self.channel_widgets_individual = []
        self.channel_widgets_grouped = []
        for key in self._channels.keys():
            if self._channels[key]["section"] == "individual":
                self.channel_widgets_individual.append(
                    ChannelAndGroupWidget(
                        channel=key,
                        cmd_on=f"{key} on",  # fixme
                        cmd_off=f"{key} off",  # fixme
                        controller=self,
                    )
                )
            elif self._channels[key]["section"] == "grouped":
                self.channel_widgets_grouped.append(
                    ChannelAndGroupWidget(
                        channel=key,
                        cmd_on=f"{key} on",  # fixme
                        cmd_off=f"{key} off",  # fixme
                        controller=self,
                    )
                )
        self.build_ui()

    def load_file(self, ask_fname: bool = False):
        """Load a configuration file and set the GUI accordingly.

        :param ask_fname: Whether to ask for a filename or not.
        """
        if ask_fname:
            # todo
            pass
        else:  # load default configuration file
            fin = self.app_local_path.joinpath("config.json")
            if fin.exists():
                with open(fin) as f:
                    self._channels = json.load(f)
            else:
                self.statusbar.showMessage(
                    f"Could not find {fin}. Starting with empty configuration.",
                    self.statusbartime,
                )
        self.load_channels()

    def save(self, ask_fname: bool = False):
        """Save the current configuration to default json file.

        :param ask_fname: Whether to ask for a filename or not.
        """
        fout = self.app_local_path.joinpath("config.json")

        with open(fout, "w") as f:
            json.dump(self._channels, f, indent=4)

        self.statusbar.showMessage(f"Saved configuration to {fout}", self.statusbartime)

    def send_command(self, cmd: str):
        """Send a command to the DigOutBox.

        Command will automatically be terminated with `\n` if not already present.

        :param cmd: Command to send.
        """
        # todo
        print(cmd)

    def settings(self):
        """Configure the settings."""
        # todo
        pass

    def set_all_channels(self, state: bool):
        """Turn all channels on or off."""
        for ch in self.channel_widgets_individual:
            ch.is_on = state
        for ch in self.channel_widgets_grouped:
            ch.is_on = state
        # todo: send command


if __name__ == "__main__":
    # fbs installed
    if ApplicationContext is not None:
        appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
        window = DigOutBoxController(is_windows=fbsrt_platform.is_windows())
        window.show()
        exit_code = appctxt.app.exec()  # 2. Invoke appctxt.app.exec()
        sys.exit(exit_code)
    # fbs not installed
    else:
        current_platform = sys.platform
        if current_platform == "win32" or current_platform == "cygwin":
            is_windows = True
        elif current_platform == "linux" or current_platform == "darwin":
            is_windows = False
        else:
            is_windows = False
            warnings.warn(
                f"Current platform {current_platform} is not recognized. "
                f"Assuming this is not windows."
            )

        # run the app
        app = QtWidgets.QApplication(sys.argv)
        window = DigOutBoxController(is_windows=is_windows)
        window.show()

        app.exec()
