"""Init file for tests."""

import contextlib
from typing import List
from unittest import mock

from mock_serial import MockSerial

from controller_cli import DigIOBoxComm


@contextlib.contextmanager
def expected_communication(command: List = [], response: List = []):  # noqa: B006
    """Expect a command and response from the device.

    :param mock_serial: Mocked serial.Serial object.
    :param command: List of commands expected to be sent to device.
    :param response: List of responses from device. If a command sends no response,
        the response list should contain `None` for that command.
    """
    terminator = "\n"

    mock_dev = MockSerial()
    mock_dev.open()

    dev = DigIOBoxComm(mock_dev.port)

    dev.dev.write = mock.MagicMock()

    encoded_response = [bytes(resp + terminator, "utf-8") for resp in response]
    dev.dev.readline = mock.MagicMock(side_effect=encoded_response)

    try:
        yield dev
    finally:
        # check that all sendcommands were sent in order
        calls = [mock.call(bytes(cmd + terminator, "utf-8")) for cmd in command]
        dev.dev.write.assert_has_calls(calls, any_order=False)
