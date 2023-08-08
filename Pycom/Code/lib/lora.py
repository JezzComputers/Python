"""
Lora library for MicroPython
"""
import config
import utime
import time
from network import LoRa
import socket
import binascii
import struct
import machine

class LoraAU915: #Australia AU915
    # https://stackoverflow.com/questions/5690888/variable-scopes-in-python-classes
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915)

    def setupLora():
        #lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915)
        # Initialise LoRa in LORAWAN mode.

        # create an OTAA authentication parameters, change them to the provided credentials
        # tech-school-temp-1
        # Edmond - temperature sensor demonstration

        app_eui = binascii.unhexlify('YOUR_APP_EUI_HERE') - keep secret
        app_key = binascii.unhexlify('YOUR_APP_KEY_HERE') - keep secret

        #Limit channels for AU915
        for i in range(0,8):
            LoraAU915.lora.remove_channel(i)
        for i in range(16,65):
            LoraAU915.lora.remove_channel(i)
        for i in range(66,72):
            LoraAU915.lora.remove_channel(i)

        # join a network using OTAA (Over the Air Activation)
        #uncomment below to use LoRaWAN application provided dev_eui
        #https://docs.pycom.io/tutorials/networks/lora/nvram/
        new_connection = True
        LoraAU915.lora.nvram_restore()

        if(LoraAU915.lora.has_joined() == False):
            print("LoRa memory restored but need to join LoRa")
            LoraAU915.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
        else:
            print("Memory restored and have rejoined LoRa with previous Dev Add")
            new_connection = False

        # wait until the module has joined the network
        while not LoraAU915.lora.has_joined():
            utime.sleep(1)
            if utime.time() > 15:
                print("possible timeout")
                machine.reset()
            pass

        print('Joined')
        # create a LoRa socket
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        if new_connection:
            # set the LoRaWAN data rate
            s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)  # dr0 equiv to SF12

        # make the socket non-blocking
        s.setblocking(False)

        print("LoRa connection set up")
        utime.sleep_ms(5)
        return s

    def saveLora():
        LoraAU915.lora.nvram_save()
        print("LoRa setting saved to memory")
