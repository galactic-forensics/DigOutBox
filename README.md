# DigOutBox

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
Furhtermore, 
a Python communications class 
and a Python GUI (making use of this class)
are provided for easy control of the DigOutBox.
Finally,
the Arduino can also take commands from an RF control at 433MHz,
which puts it in the allowable range in the US and in Europe,
to drive digital outputs. 
The idea of the remote is to give the user direct control
when attending to, e.g., a laser on the table.
Depending on the number of channels the control has
(the default is 8),
multiple channels can be controlled.


## Documentation


## Hardware design


## Firmware


## Python driver


## Python GUI


## Contribution

If you would like to contribute, 
please get in touch with us.
If you have a specific issue with the software you would like to discuss,
please feel free to raise an issue and mention
that you would like to contribute.


## Acknowledgement

- [Vreker SCPI Parser](https://github.com/Vrekrer/Vrekrer_scpi_parser) (MIT):
  Used to create the SCPI interface on the Arduino.
- [InstrumentKit](https://github.com/Galvant/InstrumentKit) (AGPL-v3):
  Several parts of the python driver (code and conceptual idea)
  were adopted from this fanastic driver suite.


## License

This project is licensed under [MIT](LICENSE). 
Copyright: 2021, Galactic Forensics Laboratory.
