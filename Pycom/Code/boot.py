# boot.py -- run on boot-up

import pycom
from machine import UART
import machine
import os
from network import Bluetooth
from network import WLAN
# test
if pycom.heartbeat() == True:
    pycom.heartbeat(False)

if pycom.wifi_on_boot() == True:
  pycom.wifi_on_boot(False)

#wlan = WLAN()
#wlan.deinit()

bluetooth = Bluetooth()
bluetooth.deinit()

uart = UART(0, baudrate=115200)
os.dupterm(uart)

machine.main('main.py')
