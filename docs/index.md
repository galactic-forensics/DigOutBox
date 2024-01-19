# DigOutBox Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/digoutbox/badge/?version=latest)](https://digoutbox.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/galactic-forensics/DigOutBox/graph/badge.svg?token=R4VQOKG1IR)](https://codecov.io/gh/galactic-forensics/DigOutBox)
[![tests](https://github.com/galactic-forensics/DigOutBox/actions/workflows/package_testing.yml/badge.svg)](https://github.com/galactic-forensics/DigOutBox/actions/workflows/package_testing.yml)

## Welcome!
This project provides instrument builders with an easy interface
to control digital output pins to control other devices,
e.g., laser shutters.
The project makes use of an
[Arduino Mega](https://store.arduino.cc/products/arduino-mega-2560-rev3)
in order to have digital output pins available via
DSub-9 and BNC connectors.
Each channel will have its own LED as an indication status
if the channel is high (LED on) or low (LED off).
The Arduino can be controlled via a serial using a standard set of
[SCPI commands](https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments)
in order to control the device.
Furthermore,
a Python communications class
and a Python GUI (making use of this class)
are provided for easy control of the DigOutBox.
Finally,
the Arduino can also take commands from an RF control at 433 MHz,
which puts it in the allowable range in the US and in Europe,
to drive digital outputs.
The idea of the remote is to give the user direct control
when attending to, e.g., a laser on the table.
Depending on the number of channels the control has
(the default is 8),
multiple channels can be controlled.

## Some images

More images can be found [here](images.md).

| [<img src="img/boxes/gfl002_setup_small.jpeg" width="600">](img/boxes/gfl002_setup.jpeg) | [<img src="img/boxes/gfl002_back_top.jpeg" width="600">](img/boxes/gfl002_back_top.jpeg) |
|:----------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------:|
|                           Front of the box and remote control                            |                             Back of the box with connections                             |



## Source code, issues, contributions

All source code is available on
[GitHub](https://github.com/galactic-forensics/DigOutBox).
If you encounter any problems,
would like to contribute,
have feature requests,
please get in contact by filing an
[issue on GitHub](https://github.com/galactic-forensics/DigOutBox/issues).
