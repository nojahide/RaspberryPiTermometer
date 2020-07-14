# -*- cording:utf-8 -*-
#
# Display digits to 7 Segment display
#

import sys
import RPi.GPIO as GPIO
import time
import threading

#                   1   2   3   4   5   6   7   8   9  10  11  12


#LEDpin_vs_Board = [29, 32, 31, 33, 35, 37, 15, 16, 22, 36, 38, 40]
#LEDpin_vs_BCM   = [ 5, 12,  6, 13, 19, 26, 22, 23, 25, 16, 20, 21]

#GPIO pin number(BCM) with each segment dispaly
#               0, 1,  2,  3
index2gpio = [ 26, 6, 12, 22]

#                   1   2   7   6  10  11   8   9
segment_vs_gpio = [ 19, 13, 21, 25, 5, 23, 20, 16]

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
        for i in range(8):
            debug_print("displayOneDigit:GPIO.setup&Output: %s" %(segment_vs_gpio[i]))
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
            
        for i in range(8):
            GPIO.setup(segment_vs_gpio[i], GPIO.OUT)   # output mode
            GPIO.output(segment_vs_gpio[i], 0)         # LOW
            
    # ========================
    # change the target segment dispaly in 4 one
    # index : from left 0 to 3
    # ========================
    def changeTarget(self, index):
        for i in range(4):
            debug_print("changeTarget:clear:GPIO.setup&Output: %s" %(index2gpio[i]))
            GPIO.setup(index2gpio[i], GPIO.OUT)   # output mode
            GPIO.output(index2gpio[i], 1)         # target off
            
        debug_print("changeTarget:setTarget:GPIO.setup&Output: %s" %(index2gpio[index]))
        GPIO.setup(index2gpio[index], GPIO.OUT)   # output mode
        GPIO.output(index2gpio[index], 0)         # target ON

    def clearTarget(self):
        for i in range(4):
            GPIO.setup(index2gpio[i], GPIO.OUT)   # output mode
            GPIO.output(index2gpio[i], 1)         # target off
            
    def setTarget(self, index):
        debug_print("changeTarget:setTarget:GPIO.setup&Output: %s" %(index2gpio[index]))
        GPIO.setup(index2gpio[index], GPIO.OUT)   # output mode
        GPIO.output(index2gpio[index], 0)         # target ON

    def blinkAllZero(self):
        thread_1 = threading.Thread(target=self.blinkAllZeroThead)
        thread_1.start()        
    
    def blinkAllZeroThead(self):
        # 1sec ON, 1sec Off x 4times
        self.dispReset()
        
        for times in range(4):
            elapsedtime = 0.0
            starttime = time.monotonic()
            while elapsedtime < 1.0:
        
                #all zero
                for i in range(4):
                    self.changeTarget(i)
                    self.displayOneDigit(0)
                    time.sleep(0.004)

                    #period
                    self.changeTarget(1)      # period position is 1
                    self.displayOneDigit(10)  # '.' = 10 is rule of this method
                    time.sleep(0.004)
                
                elapsedtime = time.monotonic() - starttime
            
            time.sleep(1)

    # ========================
    # ShowDigitalValue()
    # only supprt 0-99.99
    # if over 3 decimal place, round to the second decimal place (by format())
    # ========================
    def ShowDigitalValue(self,value):
        #self.dispReset()
        #time.sleep(1)
        
        
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
                #self.changeTarget(1)      # period position is 1
                self.clearTarget()
                self.displayOneDigit(10)  # '.' = 10 is rule of this method
                self.setTarget(1)      # period position is 1
                time.sleep(0.003)
            else:
                #self.changeTarget(i)
                self.clearTarget()
                self.displayOneDigit(int(c))
                self.setTarget(i)
                time.sleep(0.003)
                i += 1


# ------------------ end of class ------------------

def debug_print(mes):
    #print(mes)
    pass


def continuous_show_digit_value(value, times):
    display = SevenSegmentDisplay()
    display.dispReset()
    
    starttime = time.monotonic()
    elapsedtime = 0.0
    
    while elapsedtime < times:
        display.ShowDigitalValue(value)
        elapsedtime = time.monotonic() - starttime


def main_disp_all():
    disp_all_pattern()
    print("all pattern finish. Hit any key.")
    x = input()


def main_manual_input():
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
            display.displayOneDigit(j)
            time.sleep(0.5)
            
        
    display.dispReset()
    print("disp_all_pattern finish.")
    #x = input()

def set_by_bcm():
    display = SevenSegmentDisplay()
    display.dispReset()
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

def blink_zerozero():
    display = SevenSegmentDisplay()
    display.dispReset()
    display.blinkAllZero()
    

def main():
    
    a = 'empty'            # default argument
    arglen = len(sys.argv)
    if arglen > 1:
        a = sys.argv[1]    # first argument. argv[0] is file or module name

    disptime = 5.0         # sec second argument, optional.
    if arglen > 2:
        if is_float_str(sys.argv[2]):
            disptime = float(sys.argv[2])

    if is_float_str(a):     #temparature or other numeric
        f = float(a)
        continuous_show_digit_value(f, disptime)
    elif a == 'all':
        main_disp_all()
    elif a == 'manual':
        main_manual_input()
    elif a == 'check':
        set_by_bcm()
    else:
        blink_zerozero()
        
    
def is_float_str(num_str):
    try:
        f = float(num_str)
        return True
    except ValueError:
        return False


def all_gpio_set_at_once():
    
    GPIO.setmode(GPIO.BCM)    # BCM Mode
    GPIO.setwarnings(False)
    
    print("all gpio set signal at once, please input 0 or 1.")
    x = input()
    y = 0
    if x == "1":
        y = 1

    for i in range(28):
        GPIO.setup(i, GPIO.OUT)   # output mode
        GPIO.output(i, y)         # target ON
        time.sleep(0.004)
    print("finished all gpio set signal.")

def all_gpio_set_one_by_one():
    
    GPIO.setmode(GPIO.BCM)    # BCM Mode
    GPIO.setwarnings(False)
    
    print("all gpio set on one by one each 1 sec.")

    for i in range(28):
        GPIO.setup(i, GPIO.OUT)   # output mode
        GPIO.output(i, 3)         # target ON
        print("GPIO %s" %(i))
        time.sleep(1)
        input()
        #GPIO.output(i, 0)         # target ON
        
    print("o wa ri.")

if __name__ == '__main__':
    main()
    #all_gpio_set_at_once()
    #all_gpio_set_one_by_one()
    