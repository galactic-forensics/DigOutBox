"""Class to communicate with device via serial."""

import serial


class DevComm:
    """Class to communicate with the Arduino.

    Example usage:
    - todo
    """

    def __init__(self, port: str, baudrate: int = 9600) -> None:
        """Initialize communication with the device.

        :param port: Port to communicate over.
        :param baudrate: Baud rate to communicate at.
        """
        self.dev = serial.Serial(port=port, baudrate=baudrate)
        self.terminator = "\n"

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


if __name__ == "__main__":
    dev = DevComm(port="/dev/ttyACM1")
    dev.sendcmd("DO0 0")
    print(dev.query("DO0?"))
