#############################################################
# Controller Class for Managing Serial Communcation w/
# the Arduino Uno
#############################################################

import serial
import time

class LightTable():
    def __init__(self, config:dict):
        self.config = config
        pass

    def turn_arduino_leds_on(self):
        try:
            ser=serial.Serial(self.config['server']['usb_port_id'],9800)
            #not sure why but the sleep is required.
            time.sleep(2)
            ser.write(b'H')
            ser.close()
        finally:
            pass
        
    def turn_arduino_leds_off(self):
        try:
            ser=serial.Serial(self.config['server']['usb_port_id'],9800)
            time.sleep(2)
            ser.write(b'L')
            ser.close()
        finally:
            pass

