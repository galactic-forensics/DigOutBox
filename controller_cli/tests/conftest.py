"""Fixtures for controller_cli tests."""

import time
import pytest


@pytest.fixture(autouse=True)
def mock_time(mocker):
    """Mock `time.sleep` for and set to zero as autouse fixture."""
    return mocker.patch.object(time, "sleep", return_value=None)
