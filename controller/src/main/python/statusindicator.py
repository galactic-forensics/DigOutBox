"""PyQt Widget - Statusindicator

PyQt class to implement a Status Indicator function as an object. The status indicator
inherits all attributes from QWidget and can be used like a regular widget.

Example in a given PyQt6 program:

    from statusindicator import StatusIndicator

    led = StatusIndicator()
    led.set_status(True)

Possible statuses are:
    None:   gray
    False:  red
    True:   green
"""

from typing import Union

from qtpy import QtCore, QtGui, QtWidgets


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
