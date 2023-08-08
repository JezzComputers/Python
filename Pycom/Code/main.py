# main.py

import binascii #module that makes conversion between binary and Ascii
import config
from dth import DTH
import gc # garbage collection
from lora import LoraAU915
import machine
from machine import Pin
from machine import ADC
from onewire import DS18X20
from onewire import OneWire
import pycom
import network
import socket
import time
import ustruct
import utime

#INIT EVERYTHING test
sleep_duration = 600  # in seconds (10 minutes)
pycom.rgbled(config.GREEN)

# power up sensors
sensor_power = Pin(config.POWER_PIN, mode=Pin.OUT)  # power for all sensors
sensor_power.value(1)  # power up
time.sleep(2)   # wait 2 seconds to stabilise

print("starting main")
pycom.rgbled(config.OFF)

# voltage divider setup to monitor battery voltage
adc = ADC()
time.sleep(2)   # wait 2 seconds to stabilise

# garbage collection enabled
gc.enable()

# config LoRa communications
s = LoraAU915.setupLora()

####################################
### LOOP IF NO NEED TO SLEEP #######
####################################

while True:
    sensor_power.value(1)  # power up
    time.sleep(1)
    pycom.rgbled(config.ORANGE)
    time.sleep(1)
    pycom.rgbled(config.OFF)


    # TEMPERATURE AND HUMIDITY OF AMBIENT AIR
    j=0
    th = DTH(config.DHT22_DATA,1)
    time.sleep(1)
    while j < 5:
        result = th.read()
        if result.temperature != 0:
            print("temperature is not zero - breaking from while loop")
            break
        time.sleep(1)
        j += 1
        print("Error code %d" % result.error_code)
        print(j)
    print("Temperature = = %.2f C" % result.temperature)
    print("Humidity = %.2f %%" % result.humidity)
    print("Error code final %d" % result.error_code)

    # BATTERY
    meanbatt=0
    j=0
    while j < 5:
        utime.sleep(0.2)
        batt = adc.channel(attn=3, pin=config.VOLTMETER)
        meanbatt += batt.voltage()/1000
        j += 1
    batt_volt = (meanbatt/j)*config.BATCOEFF #multiplcator coef to adjust the real value of the battery voltage
    print("Battery voltage = %.2f V" % batt_volt)

    #DS18B20 TEMPERATURE SENSOR
    #https://docs.pycom.io/tutorials/hardware/owd/#app

    #Also note - needed to add a 10k resistor pull up on the board
    #Internal pull up resistor was not sufficient
    #used this reference for Raspberry Pi circuit which includes 5k to 10k pull up resistor
    #https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/

    ow = OneWire(Pin(config.DS18B20_DATA))
    temp = DS18X20(ow)

    onewire_temp = temp.start_conversion()
    time.sleep(1)
    onewire_temp = temp.read_temp_async()
    time.sleep(1)


    if onewire_temp != None:
        print("Onewire temperature = %.2f C" % onewire_temp)
    else:
        print("No data received from onewire temp probe")
        pycom.rgbled(config.RED)
        time.sleep(1)
        pycom.rgbled(config.OFF)
        onewire_temp = 0.0

    onewire_temp_t = int(onewire_temp*100)
    print(onewire_temp_t)
    batt_volt_t = int(batt_volt*100)
    print(batt_volt_t)
    sens_temp = int(result.temperature*100)
    print(sens_temp)
    sens_humi = int(result.humidity*100)
    print(sens_humi)

    # converting 2 byte values into single bytes for transmission
    onewire1 = int(onewire_temp_t//256)
    onewire2 = int(onewire_temp_t%256)
    batt1 = int(batt_volt_t//256)
    batt2 = int(batt_volt_t%256)
    temp1 = int(sens_temp//256)
    temp2 = int(sens_temp%256)
    humi1 = int(sens_humi//256)
    humi2 = int(sens_humi%256)

    print("sending to TTN")
    s.setblocking(True)
    print(onewire1,onewire2,batt1,batt2,temp1,temp2,humi1,humi2)
    s.send(bytes([onewire1,onewire2,batt1,batt2,temp1,temp2,humi1,humi2]))
    s.setblocking(False)

    # Save LoRa settings before deep sleep
    LoraAU915.saveLora()
    print("going to sleep")
    sensor_power.value(0)  # power down

    # note that batt_volt has been multiplied by 100 for transmission
    if (batt_volt > 4.0):
        # to minimise writes to onboard memory and for teaching
        sleep_duration = 600  # sleep for 10 minutes
        print("Time delay sleep only")
        time.sleep(sleep_duration) # sleep in seconds
    else:
        sleep_duration = 3600  # sleep for 60 minutes
        print("Sleep using deepsleep")
        machine.deepsleep(1000 * sleep_duration)   # deepsleep in ms
