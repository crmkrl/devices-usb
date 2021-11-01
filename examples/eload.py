import time
import sys
sys.path.append("../")
from DL3031 import *

flag=True
serial_num='DL3C211800028'
delay=0.3

mode="CC"
current=0.5000

if __name__ == '__main__':
    e_load = DL3031(serial_num)
    e_load.set_off()
    e_load.set_mode(mode)
    e_load.set_cc_curr(current)
    
    while(flag==True):
        print("Voltage: " + e_load.measure_voltage())
        print("Current: " + e_load.measure_current())
        print("Power: " + e_load.measure_power())
        print("Resistance: " + e_load.measure_resistance())
        print("*************************")
        time.sleep(delay)
