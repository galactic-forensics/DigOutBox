"""Communication package to talk to the DigOutBox via Serial."""

from .device_comm import DigIOBoxComm

__all__ = ["DigIOBoxComm"]

# Package information
__version__ = "0.2.0"

__title__ = "controller"
__description__ = """Communication package to talk to the DigOutBox via Serial."""

__uri__ = "https://github.com/galactic-forensics/DigOutBox"
__author__ = "Reto Trappitsch"
__email__ = "reto@galactic-forensics.space"

__license__ = "MIT"
__copyright__ = "Copyright (c) 2021-2024, Reto Trappitsch"
