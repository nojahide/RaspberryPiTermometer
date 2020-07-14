# -*- cording:utf-8 -*-
#
# RaspberryPi LED 
# --- main ---
#

import RPi.GPIO as GPIO
import sys
import threading
from gpiozero import LED
from time import sleep

#--- GPIO ZERO reference -------
#https://www.raspberrypi.org/documentation/usage/gpio/python/README.md
#https://gpiozero.readthedocs.io/en/stable/


LED_RED_BCM   = 0
LED_GREEN_BCM = 1
LED_BLUE_BCM  = 2

class ThermoLED:
    #===============================
    # set_mode
    # target: 'R' or 'G' or 'B'
    # mode: 0=off, 1=on, 2=toggle, 3=blink
    #===============================
    def set_mode(self, target, mode):
        
        targetBCM = LED_RED_BCM
        
        if target == 'R':
            targetBCM = LED_RED_BCM
        elif target == 'G':
            targetBCM = LED_GREEN_BCM
        elif target == 'B':
            targetBCM = LED_BLUE_BCM
        else:
            return
        
        led = LED(targetBCM)
        #gpiozero LED methods include on(), off(), toggle(), and blink().
        if mode == 1:
            led.on()
        elif mode == 2:
            led.toggle()
        elif mode == 3:
            led.blink()
        else:
            led.off()
        
        return

# ------------------ end of class ------------------

#===============================
# main program
#===============================
def main():
    argcount = len(sys.argv)
    if argcount < 2:
        return
    
    tar = sys.arg[0]
    stmos = str(sys.arg[1])
    if stmos.isdecimal() == True:
        mos = int(sys.arg[1])
        led = ThermoLED()
        led.set_mode(tar, mos)
    
    print("end. hit any key.")
    s = input()
    
if __name__ == '__main__':
    main()
