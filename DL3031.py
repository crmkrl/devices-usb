# Reference:
# https://www.batronix.com/files/Rigol/Elektronische-Lasten/DL3000/DL3000_ProgrammingManual_EN.pdf

from visa import *
import time

_delay = 0.3  # in seconds

class DL3031:
    def __init__(self, serial='XXX'):
        try:
            self.rm = ResourceManager()
            self.instrument_list = self.rm.list_resources()

            self.address = [elem for elem in self.instrument_list if (elem.find('USB0') != -1 and elem.find(
                serial) != -1)] 

            if self.address.__len__() == 0:
                self.status = "Not Connected"
                print("Could not connect to device")
            else:
                self.address = self.address[0]
                self.device = self.rm.open_resource(self.address)
                self.status = "Connected"
                self.connected_with = 'USB'
                print("Connected to " + self.address)

        except VisaIOError:
            self.status = "Not Connected"
            print("PyVISA is not able to find any devices")

    # 
    # DEVICE STATUS
    # 
    def query_error(self, value, mode='DEF'):                      
        command=':SYSTem:ERRor?'
        sys_error=self.device.query(command)
        time.sleep(_delay)
        return sys_error

    # 
    # MEASURE
    # 
    # Reads the input voltage of the instrument
    def measure_voltage(self, opt=True, mode=True):
        command=''
        if opt:
            command=':MEAS:VOLT?'
        else:
            if(mode==True):
                command=':MEAS:VOLT:MAX?'   #reads max
            else:
                command=':MEAS:VOLT:MIN?'   #reads min
        volt = self.device.query(command)
        time.sleep(_delay)
        return volt

    # Reads the input current of the instrument
    def measure_current(self, opt=True, mode=True):
        command=''
        if opt:
            command=':MEAS:CURR?'
        else:
            if(mode==True):
                command=':MEAS:CURR:MAX?'   #reads max
            else:
                command=':MEAS:CURR:MIN?'   #reads min
        curr = self.device.query(command)
        time.sleep(_delay)
        return curr

    # Reads the resistance of the instrument
    def measure_resistance(self):
        command=':MEAS:RES?'
        res = self.device.query(command)
        time.sleep(_delay)
        return res

    # Reads the power of the instrument
    def measure_power(self):
        command=':MEAS:POW?'
        power = self.device.query(command)
        time.sleep(_delay)
        return power

    # Reads the battery capacity
    def measure_cap(self):
        command=':MEAS:CAP?'
        cap = self.device.query(command)
        time.sleep(_delay)
        return cap

    # Reads the battery capacity
    def measure_cap(self):
        command=':MEAS:CAP?'
        cap = self.device.query(command)
        time.sleep(_delay)
        return cap

    # Queries whether the input of the electronic load is on or off
    def instr_stat(self):
        command=':SOUR:INP:STAT?'
        stat = self.device.query(command)
        time.sleep(_delay)
        return stat

    # Sets the input of the electronic load to be on (1) and off (0)
    def set_on(self):
        command=':SOUR:INP:STAT 1' 
        self.device.write(command)
        time.sleep(_delay)
    def set_off(self):
        command=':SOUR:INP:STAT 0' 
        self.device.write(command)
        time.sleep(_delay)

    # Sets the static operation mode of the electronic load to be CR mode.
    def set_mode(self, mode):   #CC,CR,CV,CP
        command =''
        if (mode=='CC'):
            command=':SOUR:FUNC CURR'
        elif (mode=='CV'):
            command=':SOUR:FUNC VOLT'
        elif (mode=='CR'):
            command=':SOUR:FUNC RES'
        elif (mode=='CP'):
            command=':SOUR:FUNC POW'
        else:
            command=''
        self.device.write(command)
        time.sleep(_delay)
        mode = self.device.query(':SOUR:FUNC?')
        time.sleep(_delay)
        return mode

    # The input regulation mode setting is controlled by the FUNCtion command, the list value,
    # the waveform display command, or the battery discharge command.
    def func_mode(self, mode):          
        command=':SOUR:FUNC:MODE %s' % mode                 # FIX, BATT
        self.device.write(command)
        func = self.device.query(':SOUR:FUNC:MODE?')        # Queries what controls the input regulation mode
        time.sleep(_delay)
        return func

    # 
    # CC MODE
    # 
    # Sets the load's regulated current in CC mode.
    def set_cc_curr(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:CURR:LEV:IMM %s' % value
        if mode!='DEF':                                               
            command=':SOUR:CURR:LEV:IMM %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        reg_curr_set=self.device.query(':SOUR:CURR:LEV:IMM?')       # Queries the load's regulated current set in CC mode
        time.sleep(_delay)
        return reg_curr_set

    # Sets the current range in CC mode and transient operation mode to be a high range or a low one.
    # The default range is a high range.
    def set_cc_curr_range(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT        
        command=':SOUR:CURR:RANG %s' % value                       
        if mode!='DEF':
            command=':SOUR:CURR:LEV:IMM %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        curr_range=self.device.query(':SOUR:CURR:RANG?')          # Queries the load's regulated current set in CC mode
        time.sleep(_delay)
        return curr_range

    # Sets the rising and falling slew rate in CC mode
    def set_cc_slew(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT     
        command=':SOUR:CURR:SLEW:BOTH %s' % value                    
        if mode!='DEF':
            command=':SOUR:CURR:SLEW:BOTH %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        slew_rate=self.device.query(':SOUR:CURR:SLEW:BOTH?')        # Queries the slew rate set in CC mode.
        time.sleep(_delay)
        return slew_rate

    # Sets the rising rate in transient operation mode
    def set_cc_slewPos(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT     
        command=':SOUR:CURR:SLEW:POS %s' % value                 # Sets the rising rate in continuous mode to be
        if mode!='DEF':
            command=':SOUR:CURR:SLEW:POS %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        slew_pos=self.device.query(':SOUR:CURR:SLEW:POS?')        # Queries the rising rate in continuous mode
        time.sleep(_delay)
        return slew_pos

    # Sets the falling rate in transient operation mode
    def set_cc_slewNeg(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT     
        command=':SOUR:CURR:SLEW:NEG %s' % value                 # Sets the falling rate in continuous mode to be
        if mode!='DEF':
            command=':SOUR:CURR:SLEW:NEG %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        slew_neg=self.device.query(':SOUR:CURR:SLEW:NEG?')        # Queries the falling rate in continuous mode
        time.sleep(_delay)
        return slew_neg

    # Sets the starting voltage in CC mode; The unit is V
    def set_cc_von(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT     
        command=':SOUR:CURR:VON %s' % value                 # Sets the starting voltage (Von) in CC mode to be
        if mode!='DEF':
            command=':SOUR:CURR:VON %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        Von=self.device.query(':SOUR:CURR:VON?')        # Queries the starting voltage (Von) set in CC mode
        time.sleep(_delay)
        return Von

    # Sets the voltage limit in CC mode; The unit is V
    def set_cc_vlim(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT     
        command=':SOUR:CURR:VLIM %s' % value                 # *Sets the voltage limit in CC mode to be
        if mode!='DEF':
            command=':SOUR:CURR:VLIM %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        Von=self.device.query(':SOUR:CURR:VLIM?')        # Queries the voltage limit set in CC mode
        time.sleep(_delay)
        return Von

    # Sets the current limit in CC mode; The unit is A
    # The current limit refers to the upper limit of the current working in CC mode
    def set_cc_ilim(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT     
        command=':SOUR:CURR:ILIM %s' % value                 # Sets the current limit in CC mode to be
        if mode!='DEF':
            command=':SOUR:CURR:ILIM %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        Ilim=self.device.query(':SOUR:CURR:ILIM?')        # Queries the current limit set in CC mode
        time.sleep(_delay)
        return Ilim

    # Sets the frequency in continuous mode; The unit of frequency is kHz.
    def set_cc_freq(self, value, mode='DEF'):                   # MIN, MAX, DEFAULT   
        command=':SOUR:CURR:TRAN:FREQ %s' % value                 # Sets the frequency in continuous mode to be value kHz
        if mode!='DEF':
            command=':SOUR:CURR:TRAN:FREQ %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        mode=self.device.query(':SOUR:CURR:TRAN:FREQ?')        # Queries the frequency set in continuous mode
        time.sleep(_delay)
        return mode

    # Sets the period in continuous mode; The unit for the period is ms.
    def set_cc_per(self, value, mode='DEF'):                   # MIN, MAX, DEFAULT   
        command=':SOUR:CURR:TRAN:PER %s' % value                 # Sets the period in continuous mode to be value ms
        if mode!='DEF':
            command=':SOUR:CURR:TRAN:PER %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        mode=self.device.query(':SOUR:CURR:TRAN:PER?')        # Queries the period set in continuous mode
        time.sleep(_delay)
        return mode
    # 
    # CV MODE
    # 
    # Sets the load voltage in CV mode; The unit is V
    # In CV mode, when the set load voltage is greater than the voltage output from the
    # DUT, open circuit occurs to the DUT
    def set_cv_volt(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:VOLT:LEV:IMM %s' % value
        if mode!='DEF':                                               
            command=':SOUR:VOLT:LEV:IMM %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        reg_volt=self.device.query(':SOUR:VOLT:LEV:IMM?')       # Queries the load voltage set in CV mode
        time.sleep(_delay)
        return reg_volt

    # Sets the voltage range in CV mode to be a high range or a low one; The default range is a high range.
    def set_cv_range(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:VOLT:RANG %s' % value
        if mode!='DEF':                                               
            command=':SOUR:VOLT:RANG %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        range_volt=self.device.query(':SOUR:VOLT:RANG?')       # Queries the voltage range set in CV mode
        time.sleep(_delay)
        return range_volt

    # Sets the voltage limit in CV mode
    # The voltage limit refers to the upper limit of the voltage working in CV mode; The unit is V
    def set_cv_vlim(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:VOLT:VLIM %s' % value
        if mode!='DEF':                                               
            command=':SOUR:VOLT:VLIM %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        vlim=self.device.query(':SOUR:VOLT:VLIM?')       # Queries the voltage limit set in CV mode
        time.sleep(_delay)
        return vlim

    # Sets the current limit in CV mode
    # The current limit refers to the upper limit of the current working in CV mode; Its unit is A
    def set_cv_ilim(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:VOLT:ILIM %s' % value
        if mode!='DEF':                                               
            command=':SOUR:VOLT:ILIM %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        ilim=self.device.query(':SOUR:VOLT:ILIM?')       # Queries the current limit set in CV mode
        time.sleep(_delay)
        return ilim

    # 
    # CR MODE
    # 
    # Sets the load resistance in CR mode
    # The load resistance refers to the constant resistance in CR mode. Its unit is Ω
    def set_cr_res(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:RES:LEV:IMM %s' % value
        if mode!='DEF':                                               
            command=':SOUR:RES:LEV:IMM %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        res=self.device.query(':SOUR:RES:LEV:IMM?')       # Queries the load resistance set in CR mode
        time.sleep(_delay)
        return res

    # Sets the resistance range in CR mode to be a high range or a low one; The default range is a high range
    def set_cr_range(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:RES:RANG %s' % value
        if mode!='DEF':                                               
            command=':SOUR:RES:RANG %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        res_range=self.device.query(':SOUR:RES:RANG?')       # Queries the resistance range set in CR mode
        return res_range

    # Sets the voltage limit in CR mode; The unit is V
    def set_cr_vlim(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:RES:VLIM %s' % value
        if mode!='DEF':                                               
            command=':SOUR:RES:VLIM %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        res_range=self.device.query(':SOUR:RES:VLIM?')       # Queries the voltage limit set in CR mode
        time.sleep(_delay)
        return res_range
    
    # Sets the current limit in CR mode; Its unit is A
    def set_cr_ilim(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:RES:ILIM %s' % value
        if mode!='DEF':                                               
            command=':SOUR:RES:ILIM %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        ilim=self.device.query(':SOUR:RES:ILIM?')       # Queries the current limit set in CR mode
        time.sleep(_delay)
        return ilim

    # 
    # CP MODE
    # 
    # Sets the load power in CP mode
    # The load power refers to the constant power value in CP mode. The unit of power is W
    def set_cp_pow(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:POW:LEV:IMM %s' % value
        if mode!='DEF':                                               
            command=':SOUR:POW:LEV:IMM %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        ilim=self.device.query(':SOUR:POW:LEV:IMM?')       # Queries the load resistance set in CP mode
        time.sleep(_delay)
        return ilim
    
    # Sets the voltage limit in CP mode; The unit is V
    def set_cp_vlim(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:POW:VLIM %s' % value
        if mode!='DEF':                                               
            command=':SOUR:POW:VLIM %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        vlim=self.device.query(':SOUR:POW:VLIM?')       # Queries the voltage limit set in CP mode
        time.sleep(_delay)
        return vlim

    # Sets the current limit in CP mode; Its unit is A
    def set_cp_ilim(self, value, mode='DEF'):                       # MIN, MAX, DEFAULT  
        command=':SOUR:POW:ILIM %s' % value
        if mode!='DEF':                                               
            command=':SOUR:POW:ILIM %s|%s' % value %mode        
        self.device.write(command)
        time.sleep(_delay)
        ilim=self.device.query(':SOUR:POW:ILIM?')       # Queries the current limit set in CP mode
        time.sleep(_delay)
        return ilim

    # 
    # TRANSIENT MODE
    # 
    # Sets the trigger function to be on or off
    # Running this command produces the same effect as pressing the TRAN key
    def trans_on(self):
        command=':SOUR:TRAN:STAT 1'  
        self.device.write(command)
        time.sleep(_delay)
    def trans_off(self):
        command=':SOUR:TRAN:STAT 0'  
        self.device.write(command)
        time.sleep(_delay)

    # Sets the transient operation mode in CC mode
    def set_cc_transmode(self, mode='CONT'):                    # CONTinuous | PULSe | TOGGle   
        command=':SOUR:CURR:TRAN:MODE %s' % mode       
        self.device.write(command)
        time.sleep(_delay)
        mode=self.device.query(':SOUR:CURR:TRAN:MODE?')        # Queries the transient operation mode in CC mode
        time.sleep(_delay)
        return mode
    
    # Sets Level A in transient operation mode
    # In transient operation, the sink current toggles between a high value and a low value.
    # Level A indicates a high value. The unit is A
    def set_trans_alevel(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT        
        command=':SOUR:CURR:TRAN:ALEV %s' % value                       
        if mode!='DEF':
            command=':SOUR:CURR:TRAN:ALEV %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        alevel=self.device.query(':SOUR:CURR:TRAN:ALEV?')          # Queries Level A set in transient operation mode
        time.sleep(_delay)
        return alevel

    # Sets the width of Level A in continuous and pulsed transient operation
    def set_trans_awidth(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT        
        command=':SOUR:CURR:TRAN:AWID %s' % value                       
        if mode!='DEF':
            command=':SOUR:CURR:TRAN:AWID %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        awidth=self.device.query(':SOUR:CURR:TRAN:AWID?')          # Queries the width of Level A in continuous or pulsed transient operation
        time.sleep(_delay)
        return awidth

    # Sets the duty cycle in continuous mode
    # Duty cycle refers to the ratio of duration of Level A to the period when the sink current switches to Level A in continuous mode
    def set_trans_aduty(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT        
        command=':SOUR:CURR:TRAN:ADUT %s' % value                       
        if mode!='DEF':
            command=':SOUR:CURR:TRAN:ADUT %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        aduty=self.device.query(':SOUR:CURR:TRAN:ADUT?')          # Queries the duty cycle set in continuous mode
        time.sleep(_delay)
        return aduty

    # Sets Level B in transient operation mode
    # In transient operation, the sink current toggles between a high value and a low value.
    # Level B indicates a low value
    def set_trans_blevel(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT        
        command=':SOUR:CURR:TRAN:BLEV %s' % value                       
        if mode!='DEF':
            command=':SOUR:CURR:TRAN:BLEV %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        blevel=self.device.query(':SOUR:CURR:TRAN:BLEV?')          # Queries Level B set in transient operation mode
        time.sleep(_delay)
        return blevel

    # Sets the width of Level B in continuous and pulsed transient operation
    def set_trans_bwidth(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT        
        command=':SOUR:CURR:TRAN:BWID %s' % value                       
        if mode!='DEF':
            command=':SOUR:CURR:TRAN:BWID %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        bwidth=self.device.query(':SOUR:CURR:TRAN:BWID?')          # Queries the width of Level B in continuous or pulsed transient operation
        time.sleep(_delay)
        return bwidth

    # Sets the frequency in continuous mode
    def set_trans_freq(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT        
        command=':SOUR:CURR:TRAN:FREQ %s' % value                       
        if mode!='DEF':
            command=':SOUR:CURR:TRAN:FREQ %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        freq=self.device.query(':SOUR:CURR:TRAN:FREQ?')          # Queries the frequency set in continuous mode
        time.sleep(_delay)
        return freq

    # Sets the period in continuous mode
    def set_trans_period(self, value, mode='DEF'):                 # MIN, MAX, DEFAULT        
        command=':SOUR:CURR:TRAN:PER %s' % value                       
        if mode!='DEF':
            command=':SOUR:CURR:TRAN:PER %s|%s' % value %mode       
        self.device.write(command)
        time.sleep(_delay)
        period=self.device.query(':SOUR:CURR:TRAN:PER?')          # Queries the period set in continuous mode
        time.sleep(_delay)
        return period