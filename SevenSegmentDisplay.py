# -*- cording:utf-8 -*-
#
# Display digits to 7 Segment display
#

import RPi.GPIO as GPIO
from time import sleep

#GPIO pin number(BCM) with each segment dispaly
#             0, 1,  2,  3
index2gpio = [13, 6, 5, 24]

class SevenSegmentDisplay:
    
    # ========================
    # initialize
    # ========================
    def __init__(self):
        GPIO.setmode(GPIO.BCM)    # BCM Mode
        GPIO.setwarnings(False)
        pass


    # ========================
    # for Pin check
    # ========================
    def test(self, targetPin, HighLow):
        
        #セグメントディスプレイのピンとgpioの指した場所
        #31   4 blue  -> BCM-6
        #33 上3 purple-> BCM-13 4桁のうちの左端桁指定フラグ
        #35 上2 gray -> BCM-19 （抵抗あり） > 左上！
        #37 上1 white -> BCM-26 （抵抗あり） > 真上！

        #-----------------
        #18 12 下 blue   -> BCM-24 　>4桁のうちの右端桁指定フラグ
        #20  0v
        #22 10 下 green  -> BCM-25 （抵抗あり）>右下
        #24  CE0
        #26  CE1
        #28 6 グレイ     -> BCM-1 （抵抗あり）->右上
        #30     0v
        #32 8 下yellow  -> BCM-12 （抵抗あり）-> 真下！
        #34     0v
        #36 9 下 orange ->  BCM-16 （抵抗あり）->ピリオド
        #38 11下 white  -> BCM-20 （抵抗あり） -> 真中！
        #40 7 下red     -> BCM-21 （抵抗あり） -> 左下！
        GPIO.setup(int(targetPin), GPIO.OUT)   # 出力指定
        GPIO.output(int(targetPin), int(HighLow))

        #    wh gy pu bl gn  グ
        #    1  2  3  4  5  6
        #    |  |  |  |  |  |
        # --------------------------
        #     []  []  []  []
        #     []. []. []. [].
        # --------------------------
        #    |  |  |  |  |  |
        #    7  8  9  10 11 12
        #    rd yl or gn wh bl
        
        
        #       ___1
        #     2/   / 6
        #    11___ 
        #   7/   / 10
        #    ___  .
        #     8   9
        # 3pinを0　->4桁のうちの左から1番目桁指定フラグ
        # 4pinを0　->4桁のうちの左から2番目桁指定フラグ
        # 5       -> 3
        # 12pinを0-> 4桁のうちの左から4番目桁指定フラグ
        return
        
    # ========================
    # digit:value for display
    # ========================
    def displayOneDigit(self, digit):
        #                  1   2   3   4 5  6   7   8   9  10  11  12
        #LEDpin_vs_gpio = [26, 19, 13, 6, 5, 1, 21, 12, 16, 25, 20, 24]

        segmentON = [[]]
        #                 1  2  7  6 10 11  8  9
        segmentON.append([1, 1, 1, 1, 1, 0, 1, 0])  #0
        segmentON.append([0, 0, 0, 1, 1, 0, 0, 0])  #1
        segmentON.append([1, 0, 1, 1, 0, 1, 1, 0])  #2
        segmentON.append([1, 0, 0, 1, 1, 1, 1, 0])  #3
        segmentON.append([0, 1, 0, 1, 1, 1, 0, 0])  #4
        segmentON.append([1, 1, 0, 0, 1, 1, 1, 0])  #5
        segmentON.append([1, 1, 1, 0, 1, 1, 1, 0])  #6
        segmentON.append([1, 0, 0, 1, 1, 0, 0, 0])  #7
        segmentON.append([1, 1, 1, 1, 1, 1, 1, 0])  #8
        segmentON.append([1, 1, 0, 1, 1, 1, 1, 0])  #9
        
        segmentON.append([0, 0, 0, 0, 0, 0, 0, 1])  #.
        
        #all segment LED Call
        #                   1  2  7 6 10 11  8  9
        segment_vs_gpio = [26,19,21,1,25,20,12,16]
        for i in range(8):
            GPIO.setup(segment_vs_gpio[i], GPIO.OUT)   # 出力指定
            GPIO.output(segment_vs_gpio[i], segmentON[digit + 1][i])
        return


    # ========================
    # clear display all
    # ========================
    def dispReset(self):
        for i in range(4):
            GPIO.setup(index2gpio[i], GPIO.OUT)   # output mode
            GPIO.output(index2gpio[i], 0)         # LOW
            
        #                   1  2  7 6 10 11  8  9
        segment_vs_gpio = [26,19,21,1,25,20,12,16]
        for i in range(8):
            GPIO.setup(segment_vs_gpio[i], GPIO.OUT)   # output mode
            GPIO.output(segment_vs_gpio[i], 0)         # LOW
            
    # ========================
    # change the target segment dispaly in 4 one
    # index : from left 0 to 3
    # ========================
    def changeTarget(self, index):
        for i in range(4):
            GPIO.setup(index2gpio[i], GPIO.OUT)   # output mode
            GPIO.output(index2gpio[i], 1)         # target off
            
        GPIO.setup(index2gpio[index], GPIO.OUT)   # output mode
        GPIO.output(index2gpio[index], 0)         # target ON

    # ========================
    # only supprt 0-99.99
    # if over 3 decimal place, round to the second decimal place (by format())
    # ========================
    def ShowDigitalValue(self,value):

        if (value > 99.995):
            print("not supprt the value for display: %s" %(value))
            return
        elif (value < 0):
            print("not supprt the value for display: %s" %(value))
            return
        
        
        s = "{:.2f}".format(value)   # to string
        slen = len(s)
        digit_list = list(s)     # devide character
        
        i = 0
        if (slen != 5):
            i = 5 - slen        # case of value < 10
            
        for c in digit_list:
            if c == '.':
                self.changeTarget(1)      # period position is 1
                self.displayOneDigit(10)  #. = 10 is rule of this method
                sleep(0.004)
            else:
                self.changeTarget(i)
                self.displayOneDigit(int(c))
                sleep(0.004)
                i += 1

# ------------------ end of class ------------------

def main():
    display = SevenSegmentDisplay()
    display.dispReset()

    while True:
        print("please input float 0-99.99")
        x = input()
        i = 0
        while i < 1000:
            display.ShowDigitalValue(float(x))
            i += 1

        display.dispReset()
        print("show finish.")

#all segment ON by turns
def disp_all_pattern():
    display = SevenSegmentDisplay()
    display.dispReset()
    for i in range(4):
        display.changeTarget(i)
        
        for j in range(10):
            display.changeTarget(j)
            sleep(0.5)
            
        
    display.dispReset()
    print("disp_all_pattern finish.")
    #x = input()

def set_signal():
    display = SevenSegmentDisplay()
    while True:
        print("Input the target BCM")
        x = input()
        if str.isdecimal(x):
            print( "if " + x + " set High , input 1, else input other")
            y = input()
            if (y == "1"):
                y = int(1)
            else:
                y = int(0)
            display.test(x,y)
        else:
            print("invalid input :" + x)


if __name__ == '__main__':
    main()