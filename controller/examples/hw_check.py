"""Test your DigOutBox hardware.

This simple script allows you to test your DigOutBox hardware.
After installing the `controller`, you can use this script to test your hardware.
Set the `PORT` variable below to the correct port and run the script by typing

`python hw_check.py`

The script will guide you through turning each channel on and off by pressing enter.
This allows you to check the LED as well as the actual output using a multimeter.
Finally, you will be asked to turn on some channels using the remote control.
These will be turned off automatically before ending the script.
"""

from controller import DigIOBoxComm

PORT = "/dev/ttyACM0"


dev = DigIOBoxComm(PORT)

print(dev.identify)

## Test all channels individually

nof_channels = 16

for chit in range(nof_channels):
    ch = dev.channel[chit]
    print(f"\nChannel {chit}")
    ch.state = True
    _ = input("> Press enter to turn off")
    ch.state = False
    _ = input("> Press enter to continue")

## Testing remote control

_ = input("turn some switches on with the remote and press enter")

print(dev.states)

_ = input("press enter to turn all off")

dev.all_off()

_ = input("enter to quit program")

print("Bye!")
