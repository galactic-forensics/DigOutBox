"""Dialogs for the controller_gui application."""

from qtpy import QtWidgets
from serial.tools import list_ports


class PortDialog(QtWidgets.QDialog):
    """Dialog to select COM port."""

    def __init__(self, parent=None):
        """Initialize the dialog."""
        super().__init__(parent=parent)

        self.parent = parent

        # get available ports
        self.av_ports = [port.device for port in list_ports.comports()]

        # layout
        layout = QtWidgets.QVBoxLayout()

        # list widget with available ports to select from, sorted alphabetically
        self.port_list = QtWidgets.QListWidget()
        self.port_list.addItems(sorted(self.av_ports))
        self.port_list.setCurrentRow(0)

        layout.addWidget(self.port_list)

        # button box

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
            | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)

    def accept(self):
        """Accept the dialog."""
        selected_port = self.port_list.currentItem().text()
        self.parent.settings.set("Port", selected_port)
        super().accept()
