from device_comm import DigIOBoxComm

dev = DigIOBoxComm("/dev/ttyACM2")

print(dev.identify)

## Test all channels individually

nof_channels = 16

for chit in range(nof_channels):
    ch = dev.channel[chit]
    print(f"\nChannel {ch}")
    ch.state = True
    _ = input("> Press enter to turn off")
    ch.state=False
    _ = input("> Press enter to continue")

## Testing remote control

_ = input("turn some switches and press enter")

print(dev.states)

_ = input("press enter to turn all off")

dev.all_off()

_ = input("enter to quit program")