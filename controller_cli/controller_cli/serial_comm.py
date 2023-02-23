"""Class to communicate with device via serial."""

import serial
import time


class DevComm:
    """Class to communicate with the Arduino."""

    def __init__(self, port: str, baudrate: int = 9600, timeout: int = 3) -> None:
        """Initialize communication with the device.

        :param port: Port to communicate over.
        :param baudrate: Baud rate to communicate at.
        :param timeout: Timeout in seconds.
        """
        self.dev = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.terminator = "\n"
        time.sleep(1)

    def query(self, cmd: str) -> str:
        """Query the device by sending a given command and returning the answer.

        :param cmd: Command to start querying.

        :return: Decoded answer.
        """
        self.sendcmd(cmd)
        return self.dev.readline().decode("utf-8").rstrip()

    def sendcmd(self, cmd: str) -> None:
        """Send a command string to the device.

        :param cmd: Command to send.
        """
        self.dev.write(f"{cmd}{self.terminator}".encode())
