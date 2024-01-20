"""Provide some home-made Qt widgets."""

import itertools
from typing import Union

from qtpy import QtCore, QtGui, QtWidgets

from controller_cli import DigIOBoxComm


class ChannelWidget(QtWidgets.QWidget):
    """Channel and group widget that allows to turn an individual channel on or off."""

    def __init__(
        self,
        channel: str,
        hw_channel: list[str],
        comm: DigIOBoxComm,
        parent=None,
        controller=None,
        is_on: bool = None,
        channel_names: list[str] = None,
    ):
        """Initialize the channel widget.

        :param channel: Channel name.
        :param hw_channel: List of hardware channels, e.g. ["7", "10"] or ["3"] for a
            single channel.
        :param comm: Communication object.
        :param parent: Parent widget.
        :param controller: Controller object.
        :param is_on: Whether the channel is currently on.
        :channel_names: List of channel names, e.g. ["laser1", "laser2"]. Must be
            provided if hw_channel is a list of length > 1.
        """
        super().__init__(parent=parent)

        self.channel = channel

        if len(hw_channel) > 1:
            if channel_names is None:
                raise ValueError(
                    "Must provide channel names if hw_channel is a list of length > 1."
                )
            self.channel_names = channel_names
        else:
            self.channel_names = [channel]

        self.hw_channel = hw_channel
        self.comm = comm
        self.controller = controller

        # status indicator
        self.status_indicator = StatusIndicator()

        # UI
        self.on_button = None
        self.off_button = None
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
        # name label
        name_label = QtWidgets.QLabel(self.channel)
        if len(self.hw_channel) > 1:
            tooltip = f"Channels: {', '.join(self.channel_names)}"
        else:
            tooltip = (
                f"Physical output channel: "
                f"{self.controller.hw_config[self.hw_channel[0]]}"
            )
        name_label.setToolTip(tooltip)
        # make label bold
        name_label_font = QtGui.QFont()
        name_label_font.setBold(True)
        name_label.setFont(name_label_font)

        # buttons
        self.on_button = QtWidgets.QPushButton("On")
        self.on_button.setToolTip(f"Turn {self.channel} on")
        self.on_button.clicked.connect(self.on_button_clicked)
        self.off_button = QtWidgets.QPushButton("Off")
        self.off_button.setToolTip(f"Turn {self.channel} off")
        self.off_button.clicked.connect(self.off_button_clicked)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.status_indicator)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(self.on_button)
        layout.addWidget(self.off_button)
        self.setLayout(layout)

    def on_button_clicked(self):
        """Handle the on button click."""
        self.is_on = True

    def off_button_clicked(self):
        """Handle the off button click."""
        self.is_on = False

    def set_status(self):
        """Set the font color depending on the channel status."""
        self.status_indicator.set_status(self.is_on)

        # send command
        if self.is_on is not None:
            for it in self.hw_channel:
                ch = self.comm.channel[it]
                ch.state = self.is_on

        # update the status of the channels if a group of lasers was changed in state
        if len(self.hw_channel) > 1:
            for other_channel in itertools.chain(
                self.controller.channel_widgets_individual,
                self.controller.channel_widgets_grouped,
            ):
                other_channel.set_status_custom(self.is_on, self.channel_names)

        # update grouped channels
        for other_channel in self.controller.group_widgets:
            other_channel.set_status_group()

    def set_status_custom(self, state: Union[bool, str], ch_check: list[str] = None):
        """Set the status light without sending any commands.

        :param state: State to set the status to. Can be True, False, None, or "mixed".
        :param ch_check: If set, only sets the indicator if the ch_check list contains
            this channel's name.
        """
        if ch_check is not None:
            if self.channel not in ch_check:
                return
        self.status_indicator.set_status(state)
        self._is_on = state

    def set_status_group(self):
        """Automatically check group status in comparison with individual channels."""
        if len(self.hw_channel) > 1:
            states = []
            for other_ch in itertools.chain(
                self.controller.channel_widgets_individual,
                self.controller.channel_widgets_grouped,
            ):
                if other_ch.channel in self.channel_names:
                    states.append(other_ch.is_on)

            if all(states):
                state = True
            elif not any(states):
                state = False
            else:
                state = "mixed"

            self.set_status_custom(state)

    def set_status_from_read(self, all_states: list[int]):
        """Set the status from the read all list of values.

        :param all_states: List of the states of all channels as integers.
        """
        try:
            states = [bool(all_states[int(it)]) for it in self.hw_channel]
            if all(states):
                state = True
            elif not any(states):
                state = False
            else:
                state = "mixed"
        except IndexError:
            return

        self.set_status_custom(state)
        pass


class TimerSpinBox(QtWidgets.QSpinBox):
    """QSpinBox for timer with min 1, max of 999."""

    def __init__(self, parent=None):
        """Initialize the spin box with new settings."""
        super().__init__(parent)
        self.setMinimum(1)
        self.setMaximum(999)


class StatusIndicator(QtWidgets.QWidget):
    """Status indicator widget."""

    def __init__(self, parent=None, size=20, margin=5):
        """Initialize the status indicator."""
        super().__init__(parent=parent)
        # for statuses: True (green), "mixed" (yellow), None (gray), False (red)
        self.status = None

        # dictionary for the status color, status call
        self.status_color = {
            None: QtCore.Qt.GlobalColor.gray,
            True: QtCore.Qt.GlobalColor.green,
            False: QtCore.Qt.GlobalColor.red,
            "mixed": QtGui.QColor(255, 128, 0),  # orange
        }
        self.setToolTip("green:\ton\nred:\toff\norange:\tmixed\ngray:\tunknown status")

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
        """Paints the status indicator with the defined width if an event is triggered.

        :param event:  <QPaintEvent>   Event that triggers the paint
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
        """Set the color of the status  indicator.

        When done, emits a signal to trigger the event painter.

        :param color:   <QColor>    Color to change it to
        :return:
        """
        self.color = color
        self.update()  # updates the widget -> sends the event to trigger the painter

    def set_status(self, status: Union[bool, None]):
        """Set the color of the LED according to the status.

        See the dictionary self.status_color

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
