import time
import sys
sys.path.append("../")
from DMM6500 import *

flag=True
serial_num='04458739'
delay=0.3

if __name__ == '__main__':
    dmm = DMM6500(serial_num)    
    dmm.init()
    dmm.setMeasure_voltage()

    while(flag==True):
        print("Voltage: " + dmm.measure_voltage())
        print("*************************")
        time.sleep(delay)
