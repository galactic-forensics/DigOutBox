# Controller GUI

This is the folder for the controller GUI,
which uses the `controller_cli` to interface with the hardware.

## Requirements

You need to have either `PyQt6` or `PySide6` installed.
Further requirements are listed in `src/requirements/base.txt`.

If you want to compile the GUI to a standalone executable,
you must have `fbs-pro` installed,
see [here](https://build-system.fman.io/).

### Arduino on Windows

If you are using Windows,
you need to install the Arduino IDE from
[here](https://www.arduino.cc/en/software).
Unplug and replug the Arduino after installation.

If it still does not work,
open the device manager,
look for the COM port of the Arduino.
The properties of the device, in extras,
will mention that the device needs further installation.
Update the driver by searching the local computer for drivers
where you installed the Arduino IDE.
This path is most likely:
```bash
C:\Users\<USERNAME>\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.3\drivers
```


## Usage

The easiest usage is to download an installer.
We provide installers for Windows.
This is especially recommended for air-gapped systems,
since no internet connection is required.
Install the program as you would any other windows program.

You can also run the program directly from source.
To do so, first install the requirements.
Then run the following command from the `src` directory:

```bash
python -m main.py
```

## Controller configuration and settings files

The settings and configuration files are by default saved to the following locations:

- Windows: `%APPDATA%\Roaming\DigOutBox`
- Linux/macOS: `$HOME/.config/DigOutBox`

If you encounter issues with the software,
it might be worth deleting these files and restarting the program.
Note that you will lose your configuration and settings if you do so!
