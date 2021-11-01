import sys
sys.path.append("../")
from DP832 import *
from DL3031 import *
from DMM6500 import *

serial_num=[    'DP8C221801417',    #ps
                'DL3C211800028',    #eload
                '04458739'          #dmm
            ]
PS_CH=3
voltage=3.0
current=0.5

mode="CC"
current=0.5000

flag=True
delay = 0.3

if __name__ == '__main__':
    ps = DP832(serial_num[0])
    # eload = DL3031(serial_num[1])
    dmm = DMM6500(serial=serial_num[2])
    dmm.init()
    
    print("*****Power Supply*******")
    ps.set_off(PS_CH)
    ps.set_voltage(PS_CH, voltage)
    ps.set_current(PS_CH, current)
    time.sleep(1)
    print(ps.measure_voltage(PS_CH))
    print(ps.measure_current(PS_CH))
    time.sleep(1)

    # print("***** ELOAD *******")
    # eload.set_off()
    # eload.set_mode(mode)
    # eload.set_cc_curr(current)

    # print(eload.measure_voltage())
    # print(eload.measure_current())
    # print(eload.measure_resistance())
    # print(eload.measure_power())
    # time.sleep(1)

    print("***** DMM *******")
    dmm.setMeasure_voltage()
    print(dmm.measure_voltage())
    
    time.sleep(2)
    dmm.setMeasure_resistance()
    print(dmm.measure_resistance())

    # while(flag==True):
    #     print(ps.measure_voltage(PS_CH))
    #     # print(ps.measure_current())

    #     print("*************")
