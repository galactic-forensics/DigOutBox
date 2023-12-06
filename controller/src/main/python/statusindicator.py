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
