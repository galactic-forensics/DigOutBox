"""Provide some home-made Qt widgets."""

from typing import Union

from qtpy import QtCore, QtGui, QtWidgets


class ChannelAndGroupWidget(QtWidgets.QWidget):
    """Channel and group widget that allows to turn an individual channel on or off."""

    def __init__(
        self,
        channel: str,
        cmd_on: str,
        cmd_off: str,
        parent=None,
        controller=None,
        is_on: bool = None,
    ):
        """Initialize the channel widget.

        :param channel: Channel name.
        :param cmd_on: Command to turn the channel on.
        :param cmd_off: Command to turn the channel off.
        :param parent: Parent widget.
        :param is_on: Whether the channel is currently on.
        """
        super().__init__(parent=parent)

        self.channel = channel
        self.cmd_on = cmd_on
        self.cmd_off = cmd_off
        self.controller = controller

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
        layout.addWidget(self.status_indicator)
        layout.addWidget(self.name_label)
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
            cmd = self.cmd_on
        else:  # turn off
            cmd = self.cmd_off

        self.controller.send_command(cmd)

    def set_status(self):
        """Set the font color depending on the channel status."""
        self.status_indicator.set_status(self.is_on)


class StatusIndicator(QtWidgets.QWidget):
    def __init__(self, parent=None, size=20, margin=5):
        super().__init__(parent=parent)
        # for statuses: on (green), busy (yellow), off (dark gray), error (red)
        self.status = None

        # dictionary for the status color, status call
        self.status_color = {
            None: QtCore.Qt.GlobalColor.gray,
            True: QtCore.Qt.GlobalColor.green,
            False: QtCore.Qt.GlobalColor.red,
        }

        # color
        self.color = self.status_color[self.status]

        # implement the line color around the indicator
        self.linecolor = QtCore.Qt.GlobalColor.darkGray

        # set the size of the object in px
        self.margin = margin
        self.size = size
        self.linewidth = self.size // 10

        # set the widget width and height
        self.setFixedWidth(self.size + 2 * self.margin)
        self.setFixedHeight(self.size + 2 * self.margin)

    def paintEvent(self, event):
        """
        Paints the status indicator with the defined width if an event is triggered.
        :param event:
        :return:
        """
        # this will paint automatically when called (calling is an event apparently)
        painter = QtGui.QPainter(self)
        # draw the line around the LED
        painter.setPen(
            QtGui.QPen(self.linecolor, self.linewidth, QtCore.Qt.PenStyle.SolidLine)
        )
        painter.drawEllipse(self.margin, self.margin, self.size, self.size)
        # fill the circle
        painter.setBrush(QtGui.QBrush(self.color, QtCore.Qt.BrushStyle.SolidPattern))
        painter.drawEllipse(self.margin, self.margin, self.size, self.size)

    def set_color(self, color):
        """
        Sets the color of the status  indicator. Then emits a signal to trigger the
        event painter.

        :param color:   <QColor>    Color to change it to
        :return:
        """
        self.color = color
        self.update()  # updates the widget -> sends the event to trigger the painter

    def set_status(self, status: Union[bool, None]):
        """
        Sets the color of the LED according to the status. See the dictionary
        self.status_color

        :param status: See class docstring for allowed statuses
        :return:
        """
        # check for appropriate status
        if status in self.status_color:
            color = self.status_color[status]
            self.set_color(color)
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Unallowed Status",
                "The selected status is not available for the indicator.",
            )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ChannelAndGroupWidget("test", "cmd_on", "cmd_off", is_on=True)
    window.show()
    sys.exit(app.exec())
