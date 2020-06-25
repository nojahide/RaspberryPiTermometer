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

class Thermometer:

    # read data from device
    def read_data(self):
        
        # vaotage(V) = rowdata * 1.5625E-07 
        word_data = smbus.SMBus(1).read_word_data(address_temp006, register_voltage)
        data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
        if data & 0x8000 == 0:  # equal or over 0
            voltage = float(data) * 1.5625 * math.pow(10, -7)
        else: # under 0
            voltage = ((~data&0x8fff) + 1) * -1.5625 * math.pow(10, -7)

        print ('--------')
        print('data:0x{0:x}, bin:{0:b}, dec:{0}'.format(data))
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
    def calc_data(self, Vobj, Tdie, S0):
        Tdie = Tdie + 273.15 #Kelvin
        # S0 Calibration factor 5x10^-14 ~ 7x10^-14
        
        print ('--------calc data')
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
        
        return Tobj


    #S0 calibration
    def calib_param(self, arg):
        Vobj = arg[0]
        Tdie = arg[1] + 273.15 #Kelvin

        Tref = 298.15
        Twork = Tdie - Tref

        b0 = -2.94 * math.pow(10, -5)
        b1 = -5.7 * math.pow(10, -7)
        b2 = 4.63 * math.pow(10, -9)
        Vos = b0 + b1*Twork + b2*(Twork**2)

        c2 = 13.4
        FVobj = (Vobj - Vos) + c2*((Vobj - Vos)**2)

        a1 = 1.75 * math.pow(10, -3)
        a2 =  -1.678 * math.pow(10, -5)
        S = 1 + a1*Twork + a2*(Twork**2)
        CalibFunc = FVobj / S

        print ('--------calibration function')
        print("Vol : {:e}, Tdie : {:.3f}".format(arg[0], arg[1]))

        Tobj = 24.0 + 273.15
        T4subtra = math.pow(Tobj,4) - math.pow(Tdie,4)

        str1 = "Tobj : {:.3f}, ".format(Tobj)
        str2 = "To^4-Td^4 : {:e}, ".format(T4subtra)
        str3 = "CalibFunc : {:e}".format(CalibFunc)
        print (str1 + str2 + str3)
        
        '''
        S = FVobj / (math.pow(Tobj,4) - math.pow(Tdie,4))
        print("S : %s"%S)

        S0 = S / (1 + a1*Twork + a2*(Twork**2))
        print("S0", end = ":")
        print(S0)
        '''
        return S

    # for public call
    def ReadTemperature(self):
        try:
            result = self.read_data()
            #S0 = calib_param(result)
            S0 = 6 * math.pow(10, -14)
            ondo = self.calc_data(result[0], result[1], S0)
            return ondo
        
        except:
            print('--------Exception occurred--------')
            print(traceback.format_exc(sys.exc_info()[2]))
            print('----------------------------------')

#------------ end of class ----------------


def main():
    try:
        thermo = Thermometer()
        while True:
            temp = thermo.ReadTemperature()
            print("target temparature", end = ":")
            print(temp)
            sleep(1)
            print(".")
            sleep(1)
            print(".")
            sleep(1)
            print(".")
            sleep(1)
            
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()