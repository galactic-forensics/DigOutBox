"""Test communications with device."""

import pytest

from . import expected_communication


# PROPERTIES #


def test_num_channels():
    """Set/get num channels."""
    with expected_communication() as dev:
        dev.num_channels = 42
        assert dev.num_channels == 42


def test_num_channels_default():
    """Assert default num_channels is set to 16."""
    with expected_communication() as dev:
        assert dev.num_channels == 16


def test_identify():
    """Get firmware version."""
    with expected_communication(
        command=["*IDN?"],
        response=["DigIOBox,1.0"],
    ) as dev:
        assert dev.identify == "DigIOBox,1.0"


def test_states():
    """Get states of all channels."""
    with expected_communication(
        ["ALLDOut?"], ["1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0"]
    ) as dev:
        assert dev.states == [
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
        ]


# METHODS #


def test_all_off():
    """Turn all channels off."""
    with expected_communication(command=["ALLOFF"]) as dev:
        dev.all_off()


@pytest.mark.parametrize("state", [0, 1])
def test_interlock_state(state):
    """Read state of the interlock."""
    with expected_communication(
        command=["INTERLOCKState?"], response=[f"{state}"]
    ) as dev:
        assert dev.interlock_state == bool(state)


@pytest.mark.parametrize("state", [0, 1])
def test_software_lockout(state):
    """Read state of software lockout."""
    with expected_communication(command=["SWLockout?"], response=[f"{state}"]) as dev:
        assert dev.software_lockout == bool(state)


# CHANNEL PROPERTIES #


def test_channel_type_error():
    """Raise TypeError when channel is not initialized properly."""
    with expected_communication() as dev:
        with pytest.raises(TypeError):
            _ = dev.Channel("foo", 0)


@pytest.mark.parametrize("state", [True, False])
@pytest.mark.parametrize("channel", range(16))
def test_channel_state(state, channel):
    """Set/Get channel state."""
    with expected_communication(
        command=[f"DO{channel} {int(state)}", f"DO{channel}?"],
        response=[f"{int(state)}"],
    ) as dev:
        dev.channel[channel].state = state
        assert dev.channel[channel].state == state
