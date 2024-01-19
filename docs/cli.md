# Python Interface ("CLI")

[![tests](https://github.com/galactic-forensics/DigOutBox/actions/workflows/package_testing.yml/badge.svg)](https://github.com/galactic-forensics/DigOutBox/actions/workflows/package_testing.yml)
[![codecov](https://codecov.io/github/galactic-forensics/DigOutBox/branch/main/graph/badge.svg?token=R4VQOKG1IR)](https://codecov.io/github/galactic-forensics/DigOutBox)

Here we provide a python interface
to communicate with the DigOutBox.
The interface is currently tested on python 3.8-3.12.

## Installation

We currently do not provide a package hosted on PyPI for this interface.
However,
you can directly install the latest version of the interface from GitHub
via `pip` using the following command:

```bash
pip install git+https://github.com/galactic-forensics/DigOutBox.git#subdirecto
ry=controller_cli
```

## Usage

To use the package after installation,
you can import it as following and connect to a new device
connected on a given `port`:

```python
from controller_cli import DigIOBoxComm

port = "/dev/ttyACM"  # com port the box is connected to
dev = DigIOBoxComm(port)
```

!!! note
    If you are on Linux and get a `Permission denied` error when connecting to the box,
    your user might not be part of the `dialout` group.
    See the
    [Arduino docs](https://docs.arduino.cc/software/ide-v1/tutorials/Linux/#please-read)
    for more information on how to add your user to this group.

### Working with individual channels

You can define your own channel name,
e.g., let's name the first channel "Frida"
and set the status to on.

```python
frida = dev.channel[0]
frida.state = True
```

Note that all channels are zero-indexed.
You could also query the state of the channel by printing out `frida.state`.

### Commands for all channels

You can query the state as well as turn all the channels off at ones
All current states are set in the property `dev.states`.
This contains a list of as many booleans as you have channels defined.

To turn all channels to the off state, you can call
`dev.all_off()`.

### Number of channels

By default, the number of channels is set to 15.
You could change this if your hardware is different using
the `num_channels` property, e.g., to set it to 7, use:

```python
dev.num_channels = 8
```

### Safety states

You can use the interface to query the interlock and software lockout state.
The two respective properties are `dev.interlock_state` and `dev.software_lockout`.
They return boolean values.
If they return `True`,
the interlock or software lockout is active.

!!! note
    You can learn more on these safety features
    in the
    [firmware documentation](../firmware#user-setup).

### Identity

Finally, to query the hardware and firmware version of the DigOutBox,
you can check out the property: `dev.identify`.
This will tell you what is currently running on the box.

## Testing your hardware

A very simple script to test your hardware is provided
[here](https://github.com/galactic-forensics/DigOutBox/blob/main/controller_cli/examples/hw_check.py).
Read the documentation in the script for more information.
