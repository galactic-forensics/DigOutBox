from time import sleep

from device_comm import DigIOBoxComm

dev = DigIOBoxComm("/dev/ttyACM2")

sleep(1)

# nof_channels = 16

# for chit in range(nof_channels):
#     ch = dev.channel[chit]
#     print(f"\nChannel {ch}")
#     ch.state = True
#     _ = input("> Press enter to turn off")
#     ch.state=False
#     _ = input("> Press enter to continue")

print(dev.identify)

_ = input("turn some switches and press enter")

print(dev.states)

_ = input("press enter to turn all off")

dev.all_off()

_ = input("enter to quit program")