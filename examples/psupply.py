import time
import re
import sys
sys.path.append("../")
from DP832 import *

flag=True
serial_num='DP8C221801417'
delay=0.1

CH=1
on_=0
voltage=2.3000
current=1.0000

if __name__ == '__main__':
    psupply = DP832(serial_num)
    psupply.toggle_output(CH, on_)
    psupply.set_voltage(CH, voltage)
    psupply.set_current(CH, current)

    while(flag==True):
       print("Voltage: " + psupply.measure_voltage(CH))
       print("Current: " + psupply.measure_current(CH))
       print("Power: " + psupply.measure_power(CH))
       print("*********************************")
       time.sleep(delay)
