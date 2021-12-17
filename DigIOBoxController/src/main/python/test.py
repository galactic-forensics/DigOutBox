from time import sleep

from device_comm import DigIOBoxComm

dev = DigIOBoxComm("/dev/ttyACM0")
print(dev.identify)

ch = dev.channel[0]
print(ch.state)
ch.state = True

sleep(1)

print(ch.state)
ch.state = False
