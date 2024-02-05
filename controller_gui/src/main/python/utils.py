"""Utilities and checks."""

# Initial hardcoded hardware configuration to write out.
HW_CONFIG = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
]


def check_channels(channels: dict) -> bool:
    """Check if channels dictionary is valid."""
    try:
        if not isinstance(channels, dict):
            return False
        for channel in channels:
            if not isinstance(channel, str):
                return False
            if not isinstance(channels[channel]["hw_channel"], int):
                return False
            if not isinstance(channels[channel]["section"], str):
                return False
    except (KeyError, IndexError):
        return False

    return True
