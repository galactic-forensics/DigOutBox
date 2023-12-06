"""Provide the control Qt widget for a single channel."""

from typing import Union

from qtpy import QtCore, QtGui, QtWidgets

from statusindicator import StatusIndicator


class ChannelWidget(QtWidgets.QWidget):
    """Channel widget that allows to turn an individual channel on or off."""

    def __init__(
        self,
        channel: str,
        cmd_on: str,
        cmd_off: str,
        parent=None,
        inverted: bool = False,
        is_on: bool = None,
    ):
        """Initialize the channel widget.

        If the channel is inverted, the `cmd_off` will be sent for in the turn on button
        and vice versa.

        :param channel: Channel name.
        :param cmd_on: Command to turn the channel on.
        :param cmd_off: Command to turn the channel off.
        :param parent: Parent widget.
        :param inverted: Whether the channel is inverted.
        :param is_on: Whether the channel is currently on.
        """
        super().__init__(parent=parent)

        self.channel = channel
        self.cmd_on = cmd_on
        self.cmd_off = cmd_off
        self.inverted = inverted

        self.init_ui()

        self.is_on = is_on

    @property
    def is_on(self) -> Union[bool, None]:
        """Return whether the channel is currently on.

        If no known status is available, return None.
        """
        return self._is_on

    @is_on.setter
    def is_on(self, value: Union[bool, None]):
        self._is_on = value
        self.set_status()

    def init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle(self.channel)

        # name label
        self.name_label = QtWidgets.QLabel(self.channel)
        # make label bold
        self.name_label_font = QtGui.QFont()
        self.name_label_font.setBold(True)
        self.name_label.setFont(self.name_label_font)

        # status indicator
        self.status_indicator = StatusIndicator()

        # buttons
        self.on_button = QtWidgets.QPushButton("On")
        self.on_button.clicked.connect(self.on_button_clicked)
        self.off_button = QtWidgets.QPushButton("Off")
        self.off_button.clicked.connect(self.off_button_clicked)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.status_indicator)
        layout.addStretch()
        layout.addWidget(self.on_button)
        layout.addWidget(self.off_button)
        self.setLayout(layout)

    def on_button_clicked(self):
        """Handle the on button click."""
        self.send_cmd(True)
        self.is_on = True

    def off_button_clicked(self):
        """Handle the off button click."""
        self.send_cmd(False)
        self.is_on = False

    def send_cmd(self, state: bool):
        """Send the command to the controller.

        :param state: Whether to turn the channel on or off.
        """
        if state:  # turn on
            cmd = self.cmd_on if not self.inverted else self.cmd_off
        else:  # turn off
            cmd = self.cmd_off if not self.inverted else self.cmd_on

        # todo send command to parent
        print(cmd)

    def set_status(self):
        """Set the font color depending on the channel status."""
        self.status_indicator.set_status(self.is_on)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ChannelWidget("test", "cmd_on", "cmd_off", is_on=True)
    window.show()
    sys.exit(app.exec())
