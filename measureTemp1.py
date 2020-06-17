# -*- cording:utf-8 -*-
#
# Read and calcution temparature of TMP006
#

import smbus
import math
from time import sleep

address_temp006 = 0x40
register_voltage = 0x00
register_tempDie = 0x01

# read data from device
def read_data():
    
    # vaotage(V) = rowdata * 1.5625E-07 
    word_data = smbus.SMBus(1).read_word_data(address_temp006, register_voltage)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
    if data & 0x8000 == 0:  # equal or over 0
        voltage = float(data) * 1.5625 * math.pow(10, -7)
    else: # under 0
        voltage = ((~data&0x8fff) + 1) * -1.5625 * math.pow(10, -7)

    print ('--------')
    print('d ata:0x{0:x}, bin:{0:b}, dec:{0}'.format(data))
    print('~data:0x{0:x}, bin:{0:b}, dec:{0}'.format(((~data&0x8fff) + 1)))
    print('rowdata:0x{:x}, data:0x{:x}, voltage:{}'.format(word_data,data,voltage))
    
    # temparature in TMP006(centigrate) = rowdata(14bit) * 0.03125 22
    word_data = smbus.SMBus(1).read_word_data(address_temp006, register_tempDie)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
    data = data >>2
    if data & 0x3000 == 0:  # equal or over 0
        tempDie = float(data) * 0.03125
    else: # under 0
        tempDie = ((~data&0x3fff) + 1) * -0.03125
        
    print('rowdata:%s, bitConv:%s, tempInDevice:%s' %(word_data, data, tempDie))
    
    return voltage,tempDie

#caculation target temparature
def calc_data(arg):
    Vobj = arg[0]
    Tdie = arg[1] + 273.15 #Kelvin
    
    print ('--------calc data')
    S0 = 6 * math.pow(10, -14)  # Calibration factor 5x10^-14 ~ 7x10^-14
    a1 = 1.75 * math.pow(10, -3)
    a2 =  -1.678 * math.pow(10, -5)
    Tref = 298.15
    Twork = Tdie - Tref
    S = S0 * (1 + a1*Twork + a2*(Twork**2))
    
    b0 = -2.94 * math.pow(10, -5)
    b1 = -5.7 * math.pow(10, -7)
    b2 = 4.63 * math.pow(10, -9)
    Vos = b0 + b1*Twork + b2*(Twork**2)
    
    c2 = 13.4
    FVobj = (Vobj - Vos) + c2*((Vobj - Vos)**2)
    
    Tobj = math.pow(math.pow(Tdie,4) + FVobj / S, 0.25)
    Tobj -= 273.15
    print("target temparature", end = ":")
    print(Tobj)
    
    return Tobj

#S0 calibration
def calib_param(arg, times):
    Vobj = arg[0]
    Tdie = arg[1] + 273.15 #Kelvin

    Tref = 298.15
    Twork = Tdie - Tref

    b0 = -2.94 * math.pow(10, -5)
    b1 = -5.7 * math.pow(10, -7)
    b2 = 4.63 * math.pow(10, -9)
    Vos = b0 + b1*Twork + b2*(Twork**2)
    print("Vos : %s"%Vos)

    c2 = 13.4
    FVobj = (Vobj - Vos) + c2*((Vobj - Vos)**2)
    print("FVobj : %s"%FVobj)

    #******************
    #  sample for calcration
    #******************
    #Tobj = 25.5 + 0.05*times
    Tobj = arg[1] + 0.1
    print("Tobj : %s"%Tobj)
    Tobj = Tobj + 273.15

    S = FVobj / (math.pow(Tobj,4) - math.pow(Tdie,4))
    print("S : %s"%S)

    a1 = 1.75 * math.pow(10, -3)
    a2 =  -1.678 * math.pow(10, -5)
    S0 = S / (1 + a1*Twork + a2*(Twork**2))

    print("S0", end = ":")
    print(S0)
    
    return S0


#===============================
try:
    times = 0
    while True:
        result = read_data()
        S0 = calib_param(result, times)
        ondo = calc_data(result)
        times += 1
        sleep(1)
        print(".")
        sleep(1)
        print(".")
        sleep(1)
        print(".")
        sleep(1)
        
except KeyboardInterrupt:
    pass
