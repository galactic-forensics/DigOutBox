# Firmware

Once your assembly is finished,
you will need to configure the firmware
and flash it to the Arduino.
If you followed the instructions
and used an existing pinout mapping,
this should be fairly straightforward.
However,
you might need to detect and register new remotes.

The firmware is written in `C` and uses the Arduino framework.
You can find the current version `v0.2.0`
[on GitHub](https://github.com/galactic-forensics/DigOutBox/tree/main/firmware).

The firmware consists of two files:
- `DigOutBox_fw_v*.ino`: This is the main file that contains the firmware.
- `config.h`: This file contains the configuration of the firmware.
  You can find the configuration for the existing setups in the folder `configs` on GitHub.
  If you want to use a new setup,
  you will need to create a new configuration file.

Please read the following sections
for details on configuration, registering remotes,
flashing the firmware, and communicating with the Arduino via serial.

Once finished with this section,
your box can be used with the remote.
You can also use our [GUI](gui.md)
or [Python Interface](cli.md)
for computer control.

## Overview of the configuration

The important file to understand, assuming you use the existing setups, is `config.h`.
This file contains the configuration of the firmware.
It has three sections:

### DigOutBox HW configuration

This section contains the configuration of the DigOutBox hardware.
It contains the following variables:

- `numOfChannels`: The number of channels that are available.
- `numOfRemoteButtons`: The number of buttons on the remote control.
- `fw_version`: The firmware version.
- `hw_version`: The hardware version.

### User setup

This section contains the user setup.
If you have a box with an existing setup,
this section is likely the one you might want to tweak.
The section contains the following variables:

- `debug`: If set to `true`, the Arduino will print debug messages to the serial port.
  This is mainly used to set up new remotes (see below).
- `rf_delay`: Set the delay time after accepting a second remote control command in ms.
- `InterlockPin`:
  The number of the digital input pin that is connected to the interlock/trigger channel.
  If this pin is open or at 5V, all channels are off and cannot be turned on.
  Note that the channel must be an interrupt pin (default: `3`).
- `EnableInterlock`: If set to `true`, the interlock is enabled.
  If set to `false`, the interlock is disabled and `InterlockPin` functionality has no meaning.
- `SoftwareLockoutDoubleClickTime`: Sets the time in ms on how fast a double click on the remote
  has to take place in order to deactivate the software lockout.
  Note that the second click has to come after the `rf_delay` time window!
- `RFChannels`: Array that maps the buttons of the remote control to the channels of the DigOut Box.
  This array has `numOfRemoteButtons` elements.
  Each element is an integer that maps the button to a channel.
  "Channel" `-1` means that this button will turn all channels off.
  "Channel" `-2` means that this button will be used to toggle the software lockout.
  "Channel" `-3` means that this button is unused.
- `DOutInvert`: Array that defines the "off-state" of a channel.
  This array has `numOfChannels` elements.
  Each element is either `0` or `1` and defines the "off-state" of a channel.
  If `1`, the pin output is high when the channel is off.
  If `0`, the pin output is low when the channel is off.

### Board and Remote specific setup

This is the setup of the board (i.e., what is connected to what)
and the remote control codes (what button sends what signal).
This section contains the following variables:

- `DOut`: Array that defines the numbers of the digital output pins.
  This array has `numOfChannels` elements.
  Each element is an integer that defines the number of the digital output pin.
- `LedPins`: Array that defines the numbers of the LED output pins.
  This array has `numOfChannels` elements.
  Each element is an integer that defines the number of the LED output pin.
- `RFInterrupt`: The interrupt number of the pin the RF receiver is connected to.
  Note that this is not the pin, but the interrupt number.
- `numOfRemotes`: The number of remote controls that are registered.
  These remote controls are redundant and can be used to control the DigOutBox.
  If your remote controls have the same codes (see below), only one has to be setup.
- `RFRemoteCodes`: Array that defines the codes of the remote controls.
  This array has `numOfRemoteButtons` rows and `numOfRemotes` columns.
  Each element is an integer that defines the code of the remote control.

## Register remotes

To set up a new remote,
set `debug = true;` in the configuration file
and flash the firmware to the Arduino.
Leave the Arduino plugged into the computer
and open the `Serial Terminal`.
If you press a remote control button,
the serial terminal will print out a message like:

```Valid RF Remote code received: 4543804 / Channel associated: -2```

If the code has not been set up, the associated channel will be `-2` (i.e., do nothing).
For every button on your remote, write down the code that is received by the Arduino.
Do this for every remote that you would like to add to the instrument.

After you have recorded the remote codes,
enter them into the configuration file.

1. Ensure that you set up the correct `numOfRemotes` value.
2. Set up the `RFRemoteCodes` array as shown in the example below.
3. Flash the firmware and try it out!

!!! example

    ```
    RFRemoteCodes[numOfRemoteButtons][numOfRemotes]{
      {rm1_b1, rm2_b1, ...},
      {rm1_b2, rm2_b2, ...},
      ...
      {rm1_bn, rm2_bn, ...}
    }
    ```

    Here, `rm1` and `rm2` stand for remote 1 and remote 2, respectively, and
    `b1`, `b2`, ..., `bn` for buttons 1 through `n` of the remote.

### Already mapped remotes

If you bought the Bestten remotes that are linked in the BOM,
we might already have mapped out certain codes.
These remotes have, in the back, a sticker with a frequency code.
Below is a table with frequency codes that we have mapped already:


| Button  | Code 301  | Code 302 | Code 303 | Code 304  |
|---------|-----------|----------|----------|-----------|
| 1 left  | 1398067   | 4543795  | 349491   | 5330227   |
| 1 right | 1398076   | 4543804  | 349500   | 5330236   |
| 2 left  | 1398211   | 4543939  | 349635   | 5330691   |
| 2 right | 1398220   | 4543948  | 349644   | 5330380   |
| 3 left  | 1398531   | 4544259  | 349955   | 5330691   |
| 3 right | 1398540   | 4544268  | 349964   | 5330700   |
| 4 left  | 1400067   | 4545795  | 351491   | 5332227   |
| 4 right | 1400076   | 4545804  | 351500   | 5332236   |
| 5 left  | 1406211   | 4551939  | 357635   | 5338371   |
| 5 right | 1406220   | 4551948  | 357644   | 5338380   |




## Flash firmware

**Important: Make sure that the jumper on the board connecting the reset pin via the capacitor to ground is open!
Otherwise, you will not be able to flash firmware.
After you are done flashing firmware, close the connection with a jumper again.**

The following libraries are required to compile the firmware:

- `RCSwitch`
- `Vrekrer_scpi_parser`

These libraries can be installed from the Arduino IDE library manager.

Many tutorials are out there on how to flash the firmware to the Arduino.
You will need to install the [Arduino IDE](https://www.arduino.cc/en/Main/Software).
You can find help with the IDEs, e.g., here [Arduino website](https://docs.arduino.cc/software/ide-v2).

## SCPI commands

We use the `Vrekrer_scpi_parser.h` library to enable SCPI communication
with the DigOutBox. The following commands can be sent to set/query the device:

| Command       | Parameters                                                   | Description                                                                                               | Example                                                                                                         |
|---------------|--------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| `*IDN?`       | None                                                         | Query identity of device                                                                                  | `>>> *IDN?`<br/>`DigIOBox, Hardware v0.1.0, Firmware v0.1.0`                                                    |
| `DO#?`        | - `#`: Number of channel                                     | Query status of channel.<br/>Returns:<br/>- `0`: Channel off<br/>- `1`: Channel on                        | Status of channel 5 (on):<br/>`>>> DO5?`<br/>`1`                                                                |
| `DO# S`       | - `#`: Number of channel<br/>- `S`: Status (`0` off, `1` on) | Set status of channel.                                                                                    | Turn channel 3 off:<br/>`>>> DO3 0`                                                                             |
| `ALLDO?`      | None                                                         | Query status of all channels.                                                                             | `>>> ALLDO?`<br/>`1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0`<br/>Here, channel 1 reports as being on, all others are off. |
| `ALLOFF`      | None                                                         | Turn off all channels.                                                                                    | `>>> ALLOFF`                                                                                                    |
| `INTERLOCKS?` | None                                                         | Query the interlock state.<br/>- `1`: Interlocked<br/>- `0`: Not interlocked                              | `>>> INTERLOCKS?`<br/>`1`<br/>                                                                                  |
| `SWL?`        | None                                                         | Query the software lockout state.<br/>- `1`: Software lockout active<br/>- `0`: Software lockout inactive | `>>> SWL?`<br/>`1`<br/>                                                                                         |

Command sending is indicated with `>>>`.
Note that all commands must be terminated with a newline character (`\n`).

## Testing

If all works, you can send SCPI commands to the device and see the LEDs turn on and off,
but also see the voltage output assume the desired value.
A simple testing script that allows you to measure each channel individually
and to test the remote and SCPI commands is provided with the python software
in the
[`controller_cli/examples`](https://github.com/galactic-forensics/DigOutBox/tree/main/controller_cli/examples)
folder.
