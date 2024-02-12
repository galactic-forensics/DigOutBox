# DigOutBox Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mitsuhiko/rye/main/artwork/badge.json)](https://rye-up.com)
[![Documentation Status](https://readthedocs.org/projects/digoutbox/badge/?version=latest)](https://digoutbox.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/galactic-forensics/DigOutBox/graph/badge.svg?token=R4VQOKG1IR)](https://codecov.io/gh/galactic-forensics/DigOutBox)
[![tests](https://github.com/galactic-forensics/DigOutBox/actions/workflows/package_testing.yml/badge.svg)](https://github.com/galactic-forensics/DigOutBox/actions/workflows/package_testing.yml)

## Welcome!
The Digital Output Box (DigOutBox) provides instrument builders with a simple hard- and software interface
to generate output signals for controlling instruments,
e.g., to open/close laser shutters.
The project makes use of an
[Arduino Mega](https://store.arduino.cc/products/arduino-mega-2560-rev3)
and makes 16 digital output pins (channels) available via
DSub-9 and BNC connectors.
Each channel has its own LED on the front of the box
to display the status of the channel (high/low).

The Arduino can be controlled via a serial interface using a standard set of
[SCPI commands](https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments).
Furthermore,
a Python interface
and a GUI (making use of this interface)
are provided for easy computer control of the DigOutBox.
Finally,
the box can also take commands from an RF control at 433 MHz
to activate/deactivate channels.
The selected frequency
is in the allowable range in the US and in Europe.
The idea of the remote is to give the user direct control
when attending to, e.g., a laser on the table.
Depending on the number channels/buttons the control has
(the remote chosen here has 8 buttons)
and depending on the configuration,
multiple channels can be controlled.

## Use cases and safety features

The DigOutBox can be used in a variety of applications,
however,
it's originally intended use is to control laser shutters.
For this reason,
two safety features are implemented into the firmware:

- Interlock via the external line labeled `TRIG`
- Software lockout that can be triggered from a remote

The interlock feature,
if activated in the firmware,
requires a TTL signal to be present on the `TRIG` line.
If the signal is not present or is low,
all digital outputs will be set to their `off` positions
and cannot be turned on again
until the interlock signal is present/high again.

The software lockout can be set/unset from the remote
and will prevent any computer connection
to set digital outputs to `on`.
The computer can still read the states and turn all outputs `off`.

More details can be found in the
[firmware documentation](firmware.md).

## Some images

Here are two images of a completed DigOutBox.
The left image shows the status LEDs,
the right image the connections in the back.
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

## License

All software in this project is licensed under [MIT](LICENSE).
All hardware designs, images, and documentation are licensed under [CC-BY-4.0](LICENSE_CC-BY-4.0).
Copyright: 2021-2024, Reto Trappitsch
