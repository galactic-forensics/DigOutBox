"""Class to communicate with device via serial."""

import time

import serial


class DevComm:
    """Class to communicate with the Arduino."""

    def __init__(
        self, port: str, baudrate: int = 9600, timeout: int = 3, dummy: bool = False
    ) -> None:
        """Initialize communication with the device.

        :param port: Port to communicate over.
        :param baudrate: Baud rate to communicate at.
        :param timeout: Timeout in seconds.
        :param dummy: Do not communicate over serial but print send and use dummy values for receive.
        """
        self.terminator = "\n"
        self.dummy = dummy

        if not dummy:
            self.dev = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

        time.sleep(1)

    def query(self, cmd: str) -> str:
        """Query the device by sending a given command and returning the answer.

        :param cmd: Command to start querying.

        :return: Decoded answer.
        """
        self.sendcmd(cmd)
        if self.dummy:
            return "0"
        else:
            return self.dev.readline().decode("utf-8").rstrip()

    def sendcmd(self, cmd: str) -> None:
        """Send a command string to the device.

        :param cmd: Command to send.
        """
        if self.dummy:
            print(f"Sending: {cmd}")
        else:
            self.dev.write(f"{cmd}{self.terminator}".encode())
