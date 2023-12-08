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

from pyqtconfig import ConfigDialog, ConfigManager
from qtpy import QtGui, QtWidgets, QtCore

from controller_cli import DigIOBoxComm
from channel_setup import ChannelSetup
import dialogs
from widgets import ChannelAndGroupWidget, TimerSpinBox


class DigOutBoxController(QtWidgets.QMainWindow):
    def __init__(self, is_windows=False) -> None:
        """Initialize the main window.

        :param is_windows: Whether the current platform is windows.
        """
        super().__init__(parent=None)

        self.dummy = False

        # set window properties
        self.window_title = "DigOutBox Controller"
        self.setWindowTitle("DigOutBox Controller")
        self.resize(250, 150)

        self.is_windows = is_windows

        self.app_local_path = None
        self.settings = None
        self.init_local_profile()

        # communication handler
        self.comm = None

        # statusbar
        self.statusbar = self.statusBar()
        self.statusbartime = 3000  # time in ms to display messages
        self.setStatusBar(self.statusbar)

        # init GUI
        self.init_menubar()

        # init settings manager
        self.init_settings_manager()

        # init communication
        self.init_comm()

        # load config and settings
        self._channels = {}
        self.channel_widgets_individual = None
        self.channel_widgets_grouped = None
        self.load_file()

        # automatic read
        self.read_timer = QtCore.QTimer(self)
        self.automatic_read()

    def init_comm(self):
        """Initiate communication with the DigOutBox.

        When the software is opened, a dialog will be shown in order to
        """
        if self.settings.get("Port") is None:
            diag = dialogs.PortDialog(self)
            if not diag.exec():  # Cancel pressed
                QtWidgets.QMessageBox.warning(
                    self,
                    "No device selected",
                    "No device selected. Using a dummy device for demo purposes.",
                )
                self.dummy = True
                self.comm = DigIOBoxComm("dummy", dummy=True)
                self.setWindowTitle(self.window_title + " (DEMO MODE)")
                return

        # open connection and check for correct device
        try:
            self.comm = DigIOBoxComm(self.settings.get("Port"), dummy=self.dummy)
            id = self.comm.identify
            if "DigIOBox" not in id:
                raise OSError
        except:
            QtWidgets.QMessageBox.warning(
                self,
                "Device not responding",
                f"The device on port {self.settings.get('Port')} is not responding correctly. "
                f"Please check that you selected the correct port and try again.",
            )
            self.settings.set("Port", None)
            self.settings.save()
            self.init_comm()

        # save the port
        self.settings.save()

        # set window title
        self.setWindowTitle(self.window_title)

    def init_settings_manager(self):
        """Initialize the configuration manager and load the default configuration."""
        default_values = {
            "Activate automatic read": True,
            "Time between reads (s)": 10,
            "Port": None,
            "User folder": str(Path.home()),
        }

        default_settings_metadata = {
            "Time between reads (s)": {
                "preferred_handler": TimerSpinBox,
            },
            "Port": {"prefer_hidden": True},
            "User folder": {"prefer_hidden": True},
        }

        try:
            self.settings = ConfigManager(
                default_values, filename=self.app_local_path.joinpath("settings.json")
            )
        except json.decoder.JSONDecodeError as err:
            QtWidgets.QMessageBox.warning(
                self,
                "Settings error",
                f"Your settings file seems to be corrupt. "
                f"Deleting it and starting with the default config. "
                f"Plese check your settings for correctness."
                f"\n\n{err.args[0]}",
            )
            self.app_local_path.joinpath("settings.json").unlink()
            self.settings = ConfigManager(
                default_values, filename=self.app_local_path.joinpath("settings.json")
            )

        self.settings.set_many_metadata(default_settings_metadata)
        self.user_folder = Path(self.settings.get("User folder"))

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
        settings_action.triggered.connect(self.settings_window)

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

        all_read_button = QtWidgets.QPushButton("Read All")
        all_read_button.setToolTip("Read the status of all channels")
        all_read_button.clicked.connect(self.read_all)

        all_on_button = QtWidgets.QPushButton("All On")
        all_on_button.setToolTip("Turn all channels on")
        all_on_button.clicked.connect(lambda: self.set_all_channels(state=True))

        all_off_button = QtWidgets.QPushButton("All Off")
        all_off_button.setToolTip("Turn all channels off")
        all_off_button.clicked.connect(lambda: self.set_all_channels(state=False))

        all_on_off_layout.addWidget(all_read_button)
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
            f"About DigOutBoxController",
            f"DigOutBoxController is a GUI for the DigOutBox.\n\n"
            f"Help can be found on GitHub:\n"
            f"https://github.com/galactic-forensics/DigOutBox\n\n"
            f"If you have issues, please report them on GitHub.\n\n"
            f"{self.comm.identify}",
        )

    def automatic_read(self):
        """Thread out a timer to automatically read the status of all channels and set statuses."""
        self.read_all()
        if self.settings.get("Activate automatic read"):
            self.read_timer.timeout.connect(self.read_all)
            self.read_timer.start(self.settings.get("Time between reads (s)") * 1000)
        else:
            self.read_timer.stop()

    def config_channels(self):
        """Configure the channels."""
        dialog = ChannelSetup(self, channels=self._channels)
        if dialog.exec():
            self._channels = dialog.channels
            self.load_channels()
            self.save()
            self.automatic_read()

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
                        hw_channel=[self._channels[key]["hw_channel"]],
                        comm=self.comm,
                        controller=self,
                    )
                )
            elif self._channels[key]["section"] == "grouped":
                self.channel_widgets_grouped.append(
                    ChannelAndGroupWidget(
                        channel=key,
                        hw_channel=[self._channels[key]["hw_channel"]],
                        comm=self.comm,
                        controller=self,
                    )
                )
            # todo: routine to define groups of channels
        self.build_ui()

    def load_file(self, ask_fname: bool = False):
        """Load a configuration file and set the GUI accordingly.

        :param ask_fname: Whether to ask for a filename or not.
        """
        if ask_fname:
            query = QtWidgets.QFileDialog.getOpenFileName(
                self,
                "Open Configuration File",
                str(self.user_folder),
                "JSON Files (*.json)",
            )[0]
            if query == "":
                return
            fin = Path(query)
        else:  # load default configuration file
            fin = self.app_local_path.joinpath("config.json")

        # load the file
        if fin.exists():
            with open(fin) as f:
                self._channels = json.load(f)
        else:
            self.statusbar.showMessage(
                f"Could not find {fin}. Starting with empty configuration.",
                self.statusbartime,
            )
        self.load_channels()

        if ask_fname:
            self.automatic_read()
            self.save()

    def read_all(self):
        """Read the status of all channels and set the status indicators accordingly."""
        if self.dummy:
            read = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        else:
            read = self.comm.states

        # now set the status indicators for each channel
        for ch in self.channel_widgets_individual:
            ch.set_status_from_read(read)
        for ch in self.channel_widgets_grouped:
            ch.set_status_from_read(read)

    def save(self, ask_fname: bool = False):
        """Save the current configuration to default json file.

        :param ask_fname: Whether to ask for a filename or not.
        """
        if ask_fname:
            query = QtWidgets.QFileDialog.getSaveFileName(
                self,
                caption="Save configuration file as",
                directory=str(self.user_folder),
                filter="JSON Files (*.json)",
            )
            if query[0]:
                fout = Path(query[0]).with_suffix(".json")
        else:
            fout = self.app_local_path.joinpath("config.json")

        # now save the file

        with open(fout, "w") as f:
            json.dump(self._channels, f, indent=4)

        self.statusbar.showMessage(f"Saved configuration to {fout}", self.statusbartime)

    def settings_update(self, update):
        """Update the settings."""
        self.settings.set_many(update.as_dict())
        self.settings.save()
        self.automatic_read()

    def settings_window(self):
        """Bring up dialog with the settings window."""
        settings_dialog = ConfigDialog(self.settings, self, cols=1)
        settings_dialog.setWindowTitle("Settings")
        settings_dialog.accepted.connect(
            lambda: self.settings_update(settings_dialog.config)
        )
        settings_dialog.exec()

    def set_all_channels(self, state: bool):
        """Turn all channels on or off."""
        if state:
            for ch in self.channel_widgets_individual:
                ch.is_on = state
            for ch in self.channel_widgets_grouped:
                ch.is_on = state
        else:
            self.comm.all_off()
            for ch in self.channel_widgets_individual:
                ch.set_status_custom(False)
            for ch in self.channel_widgets_grouped:
                ch.set_status_custom(False)


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
