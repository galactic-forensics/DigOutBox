========================
DigOut Box Documentation
========================

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
   :alt: MIT License
   :target: https://github.com/galactic-forensics/digoutbox/blob/master/LICENSE

.. image:: https://readthedocs.org/projects/digoutbox/badge/?version=latest
    :target: https://digoutbox.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/galactic-forensics/DigOutBox/graph/badge.svg?token=R4VQOKG1IR
    :alt: Code Coverage
    :target: https://codecov.io/gh/galactic-forensics/DigOutBox

.. image:: https://github.com/galactic-forensics/DigOutBox/actions/workflows/package_testing.yml/badge.svg?branch=main
   :alt: tests
   :target: https://github.com/galactic-forensics/DigOutBox/actions/workflows/package_testing.yml


--------
Welcome!
--------

This project provides instrument builders with an easy interface
to control digital output pins to control other devices,
e.g., laser shutters.
The project makes use of an
`Arduino Mega <https://store.arduino.cc/products/arduino-mega-2560-rev3>`_
in order to have digital output pins available via
DSub-9 and BNC connectors.
Each channel will have its own LED as an indication status
if the channel is high (LED on) or low (LED off).
The Arduino can be controlled via a serial using a standard set of
`SCPI commands <https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments>`_
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


+--------------------------------------------------------+------------------------------------------------------+
| .. image:: graphics/boxes/gfl002_setup_small.jpeg      | .. image:: graphics/boxes/gfl002_back_top_small.jpeg |
|   :alt: Image 1                                        |   :alt: Image 2                                      |
+--------------------------------------------------------+------------------------------------------------------+


--------
Contents
--------

.. toctree::
    :maxdepth: 1

    license

++++++
Manual
++++++

.. toctree::
    :maxdepth: 1

    digoutbox/images
    digoutbox/versioning
    digoutbox/hardware
    digoutbox/firmware
    digoutbox/cli
    digoutbox/gui

+++++++++++++
API Reference
+++++++++++++

.. toctree::
    :maxdepth: 1
