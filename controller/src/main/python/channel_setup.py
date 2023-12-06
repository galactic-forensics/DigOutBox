"""Main window for channel setup and editing."""

import sys

from qtpy import QtWidgets

from utils import check_channels


class ChannelSetup(QtWidgets.QDialog):
    """Channel setup.

    This window is used to set up channels for the DigOutBox Controller.
    It will also pre-populate already configured channels for editing.

    The window consists of a tab widget with a tab for each channel.
    Each tab has a name, a hardware channel, and an display section.

    If cancel is hit, the window is simply closed and nothing is returned.
    If save is hit, the dictionary of all channels is checked for consistency and
    returned and the window is closed.

    Checks implemented:
    - No duplicated channel names.
    - No duplicated hardware channels.
    - No empty channel names.
    - Valid channel file.
    - Valid hardware channel configuration.
    """

    def __init__(self, parent=None, **kwargs):
        """Initialize the ChannelSetup window.

        :param parent: Parent widget.
        :param kwargs: Keyword arguments.
            - channels: A dictionary with channel names as keys and channel
                        objects as values.
            - possible_hw_channels: A list of strings with possible channels.
        """
        super().__init__(parent=parent)

        self.setWindowTitle("Channel Setup")

        self.channels = kwargs.get("channels", {})
        self._check_channels()

        self.kwargs = kwargs

        # layout for central widget
        central_layout = QtWidgets.QVBoxLayout()

        # tab widget
        self.tab_widget = QtWidgets.QTabWidget()
        central_layout.addWidget(self.tab_widget)

        # "Add", "Delete", "Cancel", "Save" buttons for bottom row of central_widget
        bottom_layout = QtWidgets.QHBoxLayout()

        add_button = QtWidgets.QPushButton("Add")
        add_button.setToolTip("Add a new channel.")
        add_button.clicked.connect(lambda: self.add_tab())
        delete_button = QtWidgets.QPushButton("Delete")
        delete_button.setToolTip("Delete the current channel.")
        delete_button.clicked.connect(self.delete_tab)
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.setToolTip("Cancel, do not save, and close the window.")
        cancel_button.clicked.connect(self.close)
        save_button = QtWidgets.QPushButton("Save")
        save_button.setToolTip("Save and close the window.")
        save_button.clicked.connect(self.save)

        bottom_layout.addStretch()
        bottom_layout.addWidget(add_button)
        bottom_layout.addWidget(delete_button)
        bottom_layout.addWidget(cancel_button)
        bottom_layout.addWidget(save_button)

        central_layout.addLayout(bottom_layout)

        self.setLayout(central_layout)

        if self.channels == {}:
            self.add_tab()
        else:
            for channel in self.channels:
                self.add_tab(name=channel, values=self.channels[channel])

        # geometry
        self.resize(550, 10)

    @property
    def num_channels(self):
        """Return the number of channels."""
        return len(self.channels)

    def add_tab(self, name=None, values=None):
        """Add a new tab to the tab widget.

        This function adds a new tab to the tab widget named "New Channel" and
        refreshes the tab widget itself.
        """
        if name is None:
            name = "New"
        possible_hw_channels = self.kwargs.get("possible_hw_channels", None)

        self.tab_widget.addTab(
            ChannelWidget(
                self, name=name, values=values, possible_hw_channel=possible_hw_channels
            ),
            "",
        )
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)

        self._change_tab_name(name)

    def delete_tab(self):
        """Delete the current tab from the tab widget."""
        self.tab_widget.removeTab(self.tab_widget.currentIndex())

    def save(self):
        """Save the channel state.

        Loop through all the tabs, get the data, and create a dictionary in the style:
        {
            "channel_name": {
                "hw_channel": "A",
                "section": "individual"
            }
        }

        If a channel name is duplicated, print a QMessageBox warning and return None.
        If a hardware channel is duplicated, print a QMessageBox warning and return
        None.
        If a channel name is empty, print a QMessagebox warning and return None

        If no warnings are encountered, return the dictionary and close the window.
        """
        channel_dict = {}
        for i in range(self.tab_widget.count()):
            channel_data = self.tab_widget.widget(i).data
            channel_name = channel_data["name"]
            channel_hw_channel = channel_data["hw_channel"]
            channel_section = channel_data["section"]

            # check if channel name is empty
            if channel_name == "":
                QtWidgets.QMessageBox.warning(
                    self,
                    "Empty Channel Name",
                    "One or more of the channel names is empty.",
                )
                return None

            # check if channel name is duplicated
            if channel_name in channel_dict.keys():
                QtWidgets.QMessageBox.warning(
                    self,
                    "Duplicated Channel Name",
                    f'The channel name "{channel_name}" occurs more than once.',
                )
                return None

            channel_dict[channel_name] = {
                "hw_channel": channel_hw_channel,
            }

            channel_dict[channel_name]["section"] = channel_section

        # check if hardware channel is duplicated
        hw_channels = [channel_dict[channel]["hw_channel"] for channel in channel_dict]
        if len(hw_channels) != len(set(hw_channels)):
            QtWidgets.QMessageBox.warning(
                self,
                "Duplicated Hardware Channel",
                f"Two or more channels have the same hardware channel.",
            )
            return None

        # sort the dictionary alphabetically by key
        channel_dict = dict(sorted(channel_dict.items()))

        self.channels = channel_dict
        super().accept()

    def _change_tab_name(self, name: str = None) -> None:
        """Change the name of the current tab to the given name."""
        if name is not None:
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), name)

    def _check_channels(self):
        """Check if channels are valid, if not raise a warning."""
        if not check_channels(self.channels):
            QtWidgets.QMessageBox.warning(
                self,
                "Invalid Channels",
                "The given channel configuration is invalid. "
                + "The setup file might be corrupt. "
                + "I'm setting up an empty channel list. "
                + "To manually fix the issue in the initialization file, "
                + "hit cancel, close the program, and edit the file.",
            )
            self.channels = {}


class ChannelWidget(QtWidgets.QWidget):
    """Channel widget with a given name."""

    def __init__(self, parent=None, name: str = None, values=None, **kwargs):
        """Initialize the ChannelWidget.

        :param parent: Parent widget.
        :param name: Name of the channel.
        :param values: Dictionary with values for the channel.

        :param kwargs: Keyword arguments.
            - possible_hw_channels: A list of strings with possible channels.
        """
        super().__init__(parent=parent)
        self.parent = parent
        self.possible_hw_channels = kwargs.get(
            "possible_hw_channels", self.hardcoded_channels
        )

        # layout for central widget
        central_layout = QtWidgets.QVBoxLayout()

        # "Name" label and line edit
        name_layout = QtWidgets.QHBoxLayout()
        name_label = QtWidgets.QLabel("Name")
        self.name_line_edit = QtWidgets.QLineEdit()
        self.name_line_edit.setToolTip("Name of the channel.")
        self.name_line_edit.setText(name)
        self.name_line_edit.textChanged.connect(self.name_edited)
        name_layout.addWidget(name_label)
        name_layout.addStretch()
        name_layout.addWidget(self.name_line_edit)
        central_layout.addLayout(name_layout)

        # "Hardware Channel" label and combo box
        hw_channel_layout = QtWidgets.QHBoxLayout()
        hw_channel_label = QtWidgets.QLabel("Hardware Channel")
        self.hw_channel_combo_box = QtWidgets.QComboBox()
        self.hw_channel_combo_box.addItems(self.possible_hw_channels)
        self.hw_channel_combo_box.setToolTip("Hardware channel on DigOutBox.")
        hw_channel_layout.addWidget(hw_channel_label)
        hw_channel_layout.addStretch()
        hw_channel_layout.addWidget(self.hw_channel_combo_box)
        central_layout.addLayout(hw_channel_layout)

        # Radio button group for Display Section with entries "individual" and "grouped"
        display_section_layout = QtWidgets.QHBoxLayout()
        display_section_label = QtWidgets.QLabel("Display Section")
        display_section_label.setToolTip(
            "Which section of the GUI should this channel be displayed in?\n"
            "Individual: Display channel on the left\n"
            "Grouped: Display channel on the right"
        )
        self.display_section_radio_button_group = QtWidgets.QButtonGroup()
        self.display_section_radio_button_individual = QtWidgets.QRadioButton(
            "individual"
        )
        self.display_section_radio_button_individual.setToolTip(
            "Display channel on the left"
        )
        self.display_section_radio_button_grouped = QtWidgets.QRadioButton("grouped")
        self.display_section_radio_button_grouped.setToolTip(
            "Display channel on the right"
        )
        self.display_section_radio_button_group.addButton(
            self.display_section_radio_button_individual
        )
        self.display_section_radio_button_individual.setChecked(True)
        self.display_section_radio_button_group.setId(
            self.display_section_radio_button_individual, 0
        )
        self.display_section_radio_button_group.addButton(
            self.display_section_radio_button_grouped
        )
        self.display_section_radio_button_group.setId(
            self.display_section_radio_button_grouped, 1
        )
        display_section_layout.addWidget(display_section_label)
        display_section_layout.addStretch()
        display_section_layout.addWidget(self.display_section_radio_button_individual)
        display_section_layout.addWidget(self.display_section_radio_button_grouped)
        central_layout.addLayout(display_section_layout)

        self.setLayout(central_layout)

        if values is not None:
            self.value_setter(values)

    @property
    def data(self) -> dict:
        """Return the data of the channel."""
        return {
            "name": self.name,
            "hw_channel": self.hw_channel,
            "section": self.section,
        }

    @property
    def hardcoded_channels(self) -> list:
        """Return a list of hardcoded hardware channels."""
        return [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
        ]

    @property
    def name(self) -> str:
        """Get the name of the channel."""
        return self.name_line_edit.text()

    @name.setter
    def name(self, value):
        """Set the name of the channel."""
        self.name_line_edit.setText(value)

    @property
    def hw_channel(self) -> str:
        """Get the hardware channel of the channel."""
        return self.hw_channel_combo_box.currentText()

    @hw_channel.setter
    def hw_channel(self, value):
        """Set the hardware channel of the channel."""
        self.hw_channel_combo_box.setCurrentText(value)

    @property
    def section(self) -> str:
        """Get the display section of the channel."""
        return (
            "individual"
            if self.display_section_radio_button_individual.isChecked()
            else "grouped"
        )

    @section.setter
    def section(self, value):
        if value == "grouped":
            self.display_section_radio_button_grouped.setChecked(True)
        else:
            self.display_section_radio_button_individual.setChecked(True)

    def name_edited(self):
        """Update the name of the channel and send out a signal to update tab name."""
        name = self.name_line_edit.text()
        self.parent._change_tab_name(name)

    def value_setter(self, values: dict):
        """Set current tab to these values.

        A warning is emitted if the hardware channel is not in the list of hw channels.
        """
        hw_channel = values["hw_channel"]
        self.hw_channel = values["hw_channel"]
        self.section = values["section"]

        if hw_channel not in self.possible_hw_channels:
            QtWidgets.QMessageBox.warning(
                self,
                "Hardware Channel not in List",
                f"The hardware channel {hw_channel} is not in the list of possible "
                f"hardware channels for output {self.name}.",
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication([])  # 1. Instantiate ApplicationContext
    channel_dict = {
        "Alfred": {"hw_channel": "A", "section": "individual"},
        "Bob": {"hw_channel": "B", "section": "grouped"},
    }
    window = ChannelSetup(channels=channel_dict)
    window.show()
    sys.exit(app.exec_())
