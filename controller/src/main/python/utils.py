"""Utilities and checks."""


def check_channels(channels: dict) -> bool:
    """Check if channels dictionary is valid."""
    try:
        if not isinstance(channels, dict):
            return False
        for channel in channels:
            if not isinstance(channel, str):
                return False
            if not isinstance(channels[channel]["hw_channel"], str):
                return False
            if not isinstance(channels[channel]["section"], str):
                return False
    except KeyError or IndexError:
        return False

    return True
