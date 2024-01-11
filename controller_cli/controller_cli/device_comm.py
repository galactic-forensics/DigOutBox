"""Class to communicate with the DigIOBox."""

from .serial_comm import DevComm
from .util_fns import ProxyList


class DigIOBoxComm(DevComm):
    """Communicate with the DigIO Box.

    Example for setting and checking state of channel zero:
        >>> device = DigIOBoxComm("/dev/ttyACM0")
        >>> ch = device.channel[0]
        >>> ch.state = True
        >>> ch.state
        True
    """

    class Channel:
        """Channel instance."""

        def __init__(self, parent, idx: int) -> None:
            """Initialize a channel.

            :param parent: Parent class, must be DigIOBoxComm.
            :param idx: ID of channel.

            :raises TypeError: If parent is not DigIOBoxComm.
            """
            if not isinstance(parent, DigIOBoxComm):
                raise TypeError("Channel must be instantiated with class DigIOBoxComm.")

            self._parent = parent
            self._idx = idx

        @property
        def state(self) -> bool:
            """Get / Set the state of a channel.

            :return: State of channel.

            Example:
                >>> device = DigIOBox("/dev/ttyACM0")
                >>> ch = device.channel[1]
                >>> ch.state
                >>> ch.state = True
                >>> ch.state
                True
            """
            return bool(int(self._parent.query(f"DO{self._idx}?")))

        @state.setter
        def state(self, value: bool) -> None:
            self._parent.sendcmd(f"DO{self._idx} {int(value)}")

    def __init__(
        self, port: str, baudrate: int = 9600, timeout: int = 3, dummy: bool = False
    ):
        """Initialize the class.

        :param port: Port to find device on.
        :param baudrate: Baud rate to connect with.
        :param timeout: Timeout in seconds.
        :param dummy: Do not communicate over serial but print send and use dummy
            values for receive.
        """
        self.dummy = dummy
        self._num_channels = 16

        super().__init__(port, baudrate=baudrate, timeout=timeout, dummy=dummy)

    # PROPERTIES #

    @property
    def channel(self):
        """Return a given channel as an object.

        :return: Channel object.

        Example:
            >>> device = DigIOBoxComm("/dev/ttyACM0")
            >>> ch = device.channel[0]
        """
        return ProxyList(self, self.Channel, range(self._num_channels))

    @property
    def identify(self):
        """Get firmware version of box."""
        if self.dummy:
            return "DigIOBox Dummy"
        return self.query("*IDN?")

    @property
    def interlock_state(self) -> bool:
        """Read if software lockout is on."""
        return bool(int(self.query("INTERLOCKState?")))

    @property
    def num_channels(self) -> int:
        """Get / Set number of available channels.

        :return: Number of channels
        """
        return self._num_channels

    @num_channels.setter
    def num_channels(self, value: int):
        self._num_channels = int(value)

    @property
    def software_lockout(self) -> bool:
        """Read if software lockout is on."""
        return bool(int(self.query("SWLockout?")))

    @property
    def states(self):
        """Read the states of all channels and return as a boolean array."""
        retval = self.query("ALLDOut?")
        return [bool(int(x)) for x in retval.split(",")]

    # METHODS #

    def all_off(self):
        """Turn all channels off."""
        self.sendcmd("ALLOFF")
