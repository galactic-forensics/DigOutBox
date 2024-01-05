"""Main interface for DigOutBoxController."""
import importlib.util
import itertools
import json
import os
from pathlib import Path
import sys
import warnings

if importlib.util.find_spec("PyQt6") is not None:
    os.environ["QT_API"] = "pyqt6"
elif importlib.util.find_spec("PySide6") is not None:
    os.environ["QT_API"] = "pyside6"
else:
    raise ImportError("Neither PyQt6 nor PySide6 are installed.")

# Detect if fbs is installed
try:
    from fbs_runtime import PUBLIC_SETTINGS as FBSRT_PUBLIC_SETTINGS
    import fbs_runtime.platform as fbsrt_platform

    if os.environ["QT_API"] == "pyqt6":
        from fbs_runtime.application_context.PyQt6 import ApplicationContext
    else:
        from fbs_runtime.application_context.PySide6 import ApplicationContext
except ImportError:
    FBSRT_PUBLIC_SETTINGS = {"version": "Unknown"}
    ApplicationContext = None
    fbsrt_platform = None


from qtpy import QtGui, QtWidgets, QtCore
from pyqtconfig import ConfigDialog, ConfigManager

import controller_cli
from controller_cli import DigIOBoxComm
from channel_setup import ChannelSetup
import dialogs
from group_setup import GroupSetup
import utils
from widgets import ChannelWidget, TimerSpinBox


class DigOutBoxController(QtWidgets.QMainWindow):
    def __init__(self, is_windows=False) -> None:
        """Initialize the main window.

        :param is_windows: Whether the current platform is windows.
        """
        super().__init__(parent=None)

        self.dummy = (
            False  # dummy mode - do not communicate over serial and "simulate" a device
        )
        self.debug = False  # debug mode - additional functionality and a debug button

        self.version = FBSRT_PUBLIC_SETTINGS["version"]

        # set window properties
        self.window_title = "DigOutBox Controller"
        self.setWindowTitle(self.window_title)
        self.resize(250, 150)

        self.is_windows = is_windows

        # local profile
        self.user_folder = None
        self.app_local_path = None
        self.settings = None
        self.init_local_profile()

        # communication handler
        self.comm = None

        # statusbar
        self.statusbar = self.statusBar()
        self.statusbartime = 3000  # time in ms to display messages
        self.setStatusBar(self.statusbar)

        # read hardware configuration
        self.hw_config = None
        self.init_hw_config()

        # init GUI
        self.main_widget = None
        self.init_menubar()

        # init settings manager
        self.init_settings_manager()

        # init communication
        self.init_comm()

        # load config and settings
        self.channels = {}
        self.channel_groups = {}

        self.channel_widgets_individual = []
        self.channel_widgets_grouped = []
        self.group_widgets = []
        self.load_file()

        # automatic read
        self.read_timer = QtCore.QTimer(self)
        self.automatic_read()

    def init_comm(self):
        """Initiate communication with the DigOutBox.

        When the software is opened, a dialog will be shown in order to
        """
        if self.settings.get("Port") is None and self.dummy is not True:
            diag = dialogs.PortDialog(self)
            if not diag.exec():  # Cancel pressed
                QtWidgets.QMessageBox.warning(
                    self,
                    "No device selected",
                    "No device selected. Using a dummy device for demo purposes.",
                )
                self.dummy = True
                self.setWindowTitle(f"{self.window_title} (DEMO MODE)")
                self.comm = DigIOBoxComm("dummy", dummy=True)
                return

        # open connection and check for correct device
        try:
            self.comm = DigIOBoxComm(self.settings.get("Port"), dummy=self.dummy)
            identity = self.comm.identify
            if "DigIOBox" not in identity:
                raise OSError
            self.comm.num_channels = len(self.hw_config)
        except:  # noqa
            QtWidgets.QMessageBox.warning(
                self,
                "Device not responding",
                f"The device on port {self.settings.get('Port')} is not responding "
                f"correctly. "
                f"Please check that you selected the correct port and try again.",
            )
            self.settings.set("Port", None)
            self.settings.save()
            self.init_comm()

        # save the port
        self.settings.save()

    def init_hw_config(self):
        """Initialize the hardware configuration from file.

        If no file available, read the standard configuration and save it out.
        """
        fname = self.app_local_path.joinpath("hw_config.txt")
        terminator = "\r\n" if self.is_windows else "\n"

        if fname.exists():
            hw_config = []
            with open(fname) as f:
                for line in f:
                    hw_config.append(line.strip())
            self.hw_config = hw_config
        else:
            self.hw_config = utils.HW_CONFIG
            with open(fname, "w") as f:
                for line in self.hw_config:
                    f.write(f"{line}{terminator}")

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

    def init_settings_manager(self):
        """Initialize the configuration manager and load the default configuration."""
        default_values = {
            "Activate automatic read": True,
            "Time between reads (s)": 1,
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

        if len(self.channel_widgets_grouped) > 0:
            grouped_channels_layout.addStretch()

        for channel_widget in self.group_widgets:
            grouped_channels_layout.addWidget(channel_widget)
        if len(self.channel_widgets_grouped) == 0:
            grouped_channels_layout.addStretch()

        channels_layout = QtWidgets.QHBoxLayout()
        if len(self.channel_widgets_individual) > 0:
            channels_layout.addLayout(individual_channels_layout)
        if (
            len(self.channel_widgets_individual) > 0
            and len(self.channel_widgets_grouped) + len(self.channel_groups) > 0
        ):
            channels_layout.addStretch()
        if len(self.channel_widgets_grouped) + len(self.group_widgets) > 0:
            channels_layout.addLayout(grouped_channels_layout)

        outer_layout.addLayout(channels_layout)

        # "All On" and "All Off" buttons at the bottom of the window
        all_on_off_layout = QtWidgets.QHBoxLayout()
        all_on_off_layout.addStretch()

        # debug button
        if self.debug:
            debug_button = QtWidgets.QPushButton("Debug")
            debug_button.clicked.connect(self.debug_function)
            all_on_off_layout.addWidget(debug_button)

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
            "About DigOutBoxController",
            f"DigOutBoxController is a GUI for the DigOutBox.\n\n"
            f"Help can be found on GitHub:\n"
            f"https://github.com/galactic-forensics/DigOutBox\n\n"
            f"If you have issues, please report them on GitHub.\n\n"
            f"{self.comm.identify}\n"
            f"GUI version: {self.version}\n"
            f"CLI version: {controller_cli.__version__}",
        )

    def automatic_read(self):
        """Thread out a timer to read the status of all channels and set statuses."""
        self.read_all()
        if self.settings.get("Activate automatic read"):
            self.read_timer.timeout.connect(self.read_all)
            self.read_timer.start(self.settings.get("Time between reads (s)") * 1000)
        else:
            self.read_timer.stop()

    def clean_up_groups(self):
        """Clean up groups to make sure that all channels that are in groupsexist.

        Groups that have undefined/dangling channels will be deleted. Note that the UI
        will not be updated and an update must be triggered manually!
        """
        to_del = []
        for group in self.channel_groups:
            for channel in self.channel_groups[group]:
                if channel not in self.channels:
                    to_del.append(group)

        for group in to_del:
            del self.channel_groups[group]

    def config_channels(self):
        """Configure the channels."""
        dialog = ChannelSetup(
            self, channels=self.channels, possible_hw_channels=self.hw_config
        )
        if dialog.exec():
            self.channels = dialog.channels
            self.clean_up_groups()
            self.load_channels()
            self.save()
            self.automatic_read()

    def config_groups(self):
        """Configure the groups."""
        dialog = GroupSetup(self, channels=self.channels, groups=self.channel_groups)
        if dialog.exec():
            self.load_channels()
            self.save()
            self.automatic_read()

    def debug_function(self):
        """Debug function.

        Connected to the debug button, when debug mode is activated.
        """
        pass

    def load_channels(self):
        """Load the channels into the GUI."""
        # fill channel widgets
        self.channel_widgets_individual = []
        self.channel_widgets_grouped = []
        for key in self.channels.keys():
            if self.channels[key]["section"] == "individual":
                self.channel_widgets_individual.append(
                    ChannelWidget(
                        channel=key,
                        hw_channel=[self.channels[key]["hw_channel"]],
                        comm=self.comm,
                        controller=self,
                    )
                )
            elif self.channels[key]["section"] == "grouped":
                self.channel_widgets_grouped.append(
                    ChannelWidget(
                        channel=key,
                        hw_channel=[self.channels[key]["hw_channel"]],
                        comm=self.comm,
                        controller=self,
                    )
                )

        self.group_widgets = []
        for key in self.channel_groups.keys():
            hw_channel = [
                self.channels[ch]["hw_channel"] for ch in self.channel_groups[key]
            ]

            self.group_widgets.append(
                ChannelWidget(
                    channel=key,
                    hw_channel=hw_channel,
                    comm=self.comm,
                    controller=self,
                    channel_names=self.channel_groups[key],
                )
            )
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
                in_dict = json.load(f)

                try:
                    self.channels = in_dict["channels"]
                except KeyError:
                    pass
                try:
                    self.channel_groups = in_dict["groups"]
                except KeyError:
                    pass
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
        for ch in itertools.chain(
            self.channel_widgets_individual,
            self.channel_widgets_grouped,
            self.group_widgets,
        ):
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
                return
        else:
            fout = self.app_local_path.joinpath("config.json")

        # create compound dictionary
        out_dict = {"channels": self.channels, "groups": self.channel_groups}

        # now save the file
        with open(fout, "w") as f:
            json.dump(out_dict, f, indent=4)

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
            for ch in itertools.chain(
                self.channel_widgets_individual, self.channel_widgets_grouped
            ):
                ch.is_on = state
        else:
            self.comm.all_off()
            for ch in itertools.chain(
                self.channel_widgets_individual,
                self.channel_widgets_grouped,
                self.group_widgets,
            ):
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
