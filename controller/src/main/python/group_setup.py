"""Combine multiple channels into individual groups."""

import sys

from qtpy import QtWidgets


class GroupSetup(QtWidgets.QDialog):
    """Provide a dialog for setting up groups of channels."""

    def __init__(self, parent=None, channels=None, groups=None):
        """Initialize the GroupSetup dialog.

        :param parent: Parent widget.
        :param channels: Dictionary of channels.
        :param groups: Dictionary of groups.
        """
        super().__init__(parent=parent)

        self.parent = parent
        self.channels = channels

        self.groups = groups if groups is not None else {}

        # raise warning message box if no channels are defined and exit dialog
        if self.channels is {} or channels is None:
            QtWidgets.QMessageBox.warning(
                self,
                "No channels defined",
                "No channels are defined. Please define channels first.",
            )
            self.close()

        self.init_ui()

    def init_ui(self):
        """Initialize the UI."""
        # set window title
        self.setWindowTitle("Group Setup")

        # layout
        layout = QtWidgets.QVBoxLayout()

        # set up a list widget with the group names
        self.group_list = QtWidgets.QListWidget()
        self.group_list.addItems(self.groups.keys())

        layout.addWidget(self.group_list)

        # add a few buttons to add, remove groups, and to close the dialog
        self.add_group_button = QtWidgets.QPushButton("Add Group")
        self.add_group_button.setToolTip("Add a new group.")
        self.add_group_button.clicked.connect(self.add_group)

        self.remove_group_button = QtWidgets.QPushButton("Remove Group")
        self.remove_group_button.setToolTip("Remove the selected group.")
        self.remove_group_button.clicked.connect(self.remove_group)

        self.close_button = QtWidgets.QPushButton("Close")
        self.close_button.setToolTip("Close the dialog.")

        # button box with ok and cancel buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_group_button)
        button_layout.addWidget(self.remove_group_button)
        button_layout.addStretch()
        button_layout.addWidget(button_box)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        """Set the groups to the parent and close the dialog."""
        self.groups = dict(sorted(self.groups.items()))
        self.parent.channel_groups = self.groups
        super().accept()

    def add_group(self):
        """Add a new group.

        Open a dialog to enter the group name, and select from a list widget the channels to add to the group.
        The channel names are taken from the keys of the channels dictionary.
        """
        # open a dialog to enter the group name and select channels
        dialog = GroupSetupIndividual(parent=self)
        if dialog.exec_():
            # update the group list widget
            self.group_list.clear()
            self.group_list.addItems(self.groups.keys())

    def remove_group(self):
        """Remove the selected group."""
        # get the selected group name
        group_name = self.group_list.currentItem().text()

        # remove the group from the list
        del self.groups[group_name]
        self.group_list.takeItem(self.group_list.currentRow())


class GroupSetupIndividual(QtWidgets.QDialog):
    """Provide a dialog for setting up groups of channels."""

    def __init__(self, parent: GroupSetup):
        """Initialize the GroupSetup dialog.

        :param parent: Parent widget.
        """
        super().__init__(parent=parent)

        self.parent = parent
        self.channels = self.parent.channels

        self.init_ui()

    def init_ui(self):
        """Initialize the UI."""
        layout = QtWidgets.QVBoxLayout()

        # label and entry box for group name
        group_name_layout = QtWidgets.QHBoxLayout()
        self.group_name_label = QtWidgets.QLabel("Group name:")
        self.group_name_entry = QtWidgets.QLineEdit()
        group_name_layout.addWidget(self.group_name_label)
        group_name_layout.addStretch()
        group_name_layout.addWidget(self.group_name_entry)

        # list widget with available channels to select from, sorted alphabetically, allowing multiple selections
        self.channel_list = QtWidgets.QListWidget()
        self.channel_list.addItems(sorted(self.channels.keys()))
        self.channel_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        # cancel and ok buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(group_name_layout)
        layout.addWidget(self.channel_list)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def accept(self):
        """Verify input and accept."""
        # check that group name is not empty and that at least one channel is selected
        if self.group_name_entry.text() == "":
            QtWidgets.QMessageBox.warning(
                self,
                "Empty group name",
                "Please enter a group name.",
            )
            return
        if len(self.channel_list.selectedItems()) == 0:
            QtWidgets.QMessageBox.warning(
                self,
                "No channels selected",
                "Please select at least one channel.",
            )
            return

        # add group to parent
        self.parent.groups[self.group_name_entry.text()] = [
            item.text() for item in self.channel_list.selectedItems()
        ]

        super().accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])  # 1. Instantiate ApplicationContext
    channel_dict = {
        "Alfred": {"hw_channel": 0, "section": "individual"},
        "Bob": {"hw_channel": 1, "section": "grouped"},
    }
    groups = {"group1": ["Alfred", "Bob"]}
    window = GroupSetup(channels=channel_dict, groups=groups)
    window.show()
    sys.exit(app.exec_())