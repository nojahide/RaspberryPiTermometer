# -*- cording:utf-8 -*-
#
# RaspberryPi Thermometer with TMP006 and 7-Segment-Display
# --- main ---
#

import threading
import Thermometer
import SevenSegmentDisplay
from time import sleep

temparature_data = 0.0    # extern parameter

# ============================
# thread for show temparature to 7 segment display
# ============================
def ShowTemparatureThead():
    display = SevenSegmentDisplay.SevenSegmentDisplay()
    display.dispReset()
    while True:
        display.ShowDigitalValue(temparature_data)



#===============================
# main program
#===============================
try:
    
    thermo = Thermometer.Thermometer()
    thread_1 = threading.Thread(target=ShowTemparatureThead)
    thread_1.start()
    
    while True:
        
        temp = thermo.ReadTemperature()
        temparature_data = temp
        sleep(2)
        
except KeyboardInterrupt:
    pass

