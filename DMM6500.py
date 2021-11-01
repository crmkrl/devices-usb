# Reference:
# https://download.tek.com/manual/DMM6500-901-01_A_April_2018_Ref_DMM6500-901-01A.pdf
# https://assets.testequity.com/te1/Documents/pdf/keithley/2000-SCAN-Manual.pdf

from visa import *
import time

_delay = 0.3  # in seconds
_timeout = 5000     # in seconds

class DMM6500:
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
                self.device.timeout = _timeout
                self.status = "Connected"
                self.connected_with = 'USB'
                print("Connected to " + self.address)

        except VisaIOError:
            self.status = "Not Connected"
            print("PyVISA is not able to find any devices")

    def close(self):
        self.device.close()
        return

    def write(self, cmd):
        self.device.write(cmd)
        time.sleep(_delay)
        return

    def reset(self):
        self.write('*RST')
        return

    def init(self):
        self.write('*RST')
        self.write('SYST:ACC FULL')
        return

    def setMeasure_voltage(self, range=10, average_count=20, numReadings=5):
        self.write(':TRAC:CLE')
        self.write(':SENS:FUNC "VOLT:DC"')
        self.write(':SENS:VOLT:RANG {range}')
        self.write(':SENS:VOLT:NPLC 1')
        self.write(':SENS:VOLT:AZER ON')
        
        self.write(':VOLT:INP AUTO')
        self.write(':VOLT:AVER:TCON REP')
        self.write(':VOLT:AVER:COUN {average_count}}')
        self.write(':VOLT:AVER ON')

        self.write(':SENS:COUN {numReadings}')
        return

    def measure_voltage(self):
        # time.sleep(1)
        self.write('INIT')
        self.write('*WAI')
        return self.device.query(':READ? "defbuffer1"')
        # return self.device.query(':TRAC:DATA? 1,10, "defbuffer1"')

    def setMeasure_current(self, range=10, average_count=20, numReadings=5):
        self.write(':TRAC:CLE')
        self.write(':SENS:FUNC "CURR:DC"')
        self.write(':SENS:CURR:RANG {range}')
        self.write(':SENS:CURR:NPLC 1')
        self.write(':SENS:CURR:AZER ON')
        
        self.write(':CURR:INP AUTO')
        self.write(':CURR:AVER:TCON REP')
        self.write(':CURR:AVER:COUN {average_count}}')
        self.write(':CURR:AVER ON')

        self.write(':SENS:COUN {numReadings}')
        return

    def measure_current(self):
        # time.sleep(1)
        self.write('INIT')
        self.write('*WAI')
        return self.device.query(':READ? "defbuffer1"')
        # return self.device.query(':TRAC:DATA? 1,10, "defbuffer1"')

    def setMeasure_resistance(self, range=1000, average_count=20, numReadings=5):
        self.write(':TRAC:CLE')
        self.write(':SENS:FUNC "RES"')
        self.write(':SENS:RES:RANG {range}')
        self.write(':SENS:RES:NPLC 1')
        self.write(':SENS:RES:AZER ON')
        
        self.write(':RES:AVER:TCON REP')
        self.write(':RES:AVER:COUN {average_count}}')
        self.write(':RES:AVER ON')

        self.write(':SENS:COUN {numReadings}')
        return

    def measure_resistance(self):
        # time.sleep(1)
        self.write('INIT')
        self.write('*WAI')
        return self.device.query(':READ? "defbuffer1"')
        # return self.device.query(':TRAC:DATA? 1,10, "defbuffer1"')

    # Create multiple channel 
# *RST
# TRAC:CLE
# TRACe:POINts 100, "defbuffer1"
# ROUT:SCAN (@1:9)
# SENS:FUNC "VOLT",(@1:9)
# SENS:VOLT:RANG 10, (@1:9)
# SENS:VOLT:NPLC 0.1, (@1:9)
# DISP:VOLT:DIG 5, (@1:9)
# ROUT:SCAN:CRE (@1:9)
# ROUTe:SCAN:COUN:SCAN 10
# ROUTe:SCAN:INT 1.0
# INIT 
# *WAI
# READ? "defbuffer1"
# TRAC:DATA? 1, 91, "defbuffer1", READ
















    # def measure_current_s(self, signal='DC', range=5, nplc=0.5, azero='ON', ave_filter_type='MOV', filter_cnt=100, en_filter='ON'):      
    #     self.write('SENS:FUNC "CURR:%s"') % signal
    #     self.write('SENS:CURR:RANG %s') % range
    #     if (signal=='DC'):
    #         self.write('SENS:CURR:NPLC %s') % nplc
    #         self.write('SENS:VOLT:AZER %s') % azero
    #     self.write('SENS:CURR:AVER:TCON %s') % ave_filter_type
    #     self.write('SENS:CURR:AVER:COUN %s') % filter_cnt
    #     self.write('SENS:CURR:AVER %s') % en_filter
    #     return self.read()

    # def measure_res_s(self, range=5, nplc=10, azero='ON', ave_filter_type='REP', filter_cnt=10, en_filter='ON'):
    #     self.write('SENS:FUNC "RES"')
    #     self.write('SENS:RES:RANG %s') % range
    #     self.write('SENS:RES:NPLC %s') % nplc
    #     self.write('SENS:RES:AZER %s') % azero
            
    #     self.write('SENS:RES:AVER:TCON %s') % ave_filter_type
    #     self.write('SENS:RES:AVER:COUN %s') % filter_cnt
    #     self.write('SENS:RES:AVER %s') % en_filter

    #     return self.query('READ?')

    # def measure_voltage_m(self, signal='DC', readings=100, debuf_name='debuffer1', cha=1, chb=9, 
    #                             volt_range=10, nplc=0.1, volt_digit=5, display_volt=5,
    #                             count=10, delay=1.0,
    #                             num_readings_a=1, num_readings_b=99):
        
    #     self.query('TRAC:CLE?')                                     #clearing debuffer1
    #     self.write('TRAC:POIN %s, "%s"' % readings % debuf_name)    #set debuffer1 to 100 readings
    #     self.write('ROUT:SCAN (@%s:%s)' % cha % chb)                #Set channels 1 to 9 on slot 1 to make DC voltage

    #     self.write('SENS:FUNC "VOLT"%s",(@%s:%s)' % signal % cha % chb)    
    #     self.write('SENS:VOLT:RANG %s, (@%s:%s)' % volt_range % cha % chb)    
    #     self.write('SENS:VOLT:NPLC %s, (@%s:%s)' % nplc % cha % chb)    
    #     self.write('SENS:VOLT:DIG %s, (@%s:%s)' % volt_digit % cha % chb)    

    #     self.write('DISP:VOLT:DIG %s, (@%s:%s)' % display_volt % cha % chb)  
    #     self.write('ROUT:SCAN:CRE (@a:b)')  
    #     self.write('ROUT:SCAN:COUN:SCAN %s' % count)  
    #     self.write('ROUT:SCAN:INT %s' % delay)  
        
    #     self.init()
    #     self.wait()

    #     read = self.read_buffer()
    #     self.query('TRAC:DATA? %s, %s, "%s", READ' % num_readings_a % num_readings_b % debuf_name)  
    #     return read

    # def measure_current_m(self, readings=100, debuf_name='debuffer2', cha=1, chb=9,
    #                             signal='DC', range=5, nplc=0.5, azero='ON', ave_filter_type='MOV', 
    #                             filter_cnt=100, en_filter='ON', 
    #                             count=10, delay=1.0,
    #                             num_readings_a=1, num_readings_b=99):     

    #     self.query('TRAC:CLE?')                                     #clearing debuffer1
    #     self.write('TRAC:POIN %s, "%s"' % readings % debuf_name)    #set debuffer1 to 100 readings

    #     self.write('ROUT:SCAN (@%s:%s)' % cha % chb)                #Set channels 1 to 9 on slot 1 to make DC voltage

    #     self.write('SENS:FUNC "CURR:%s", (@%s:%s)' % signal % cha %chb)
    #     self.write('SENS:CURR:RANG %s, (@%s:%s)' % range % cha %chb)
    #     if (signal=='DC'):
    #         self.write('SENS:CURR:NPLC %s, (@%s:%s)' % nplc % cha %chb)
    #         self.write('SENS:VOLT:AZER %s, (@%s:%s)' % azero % cha %chb)
    #     self.write('SENS:CURR:AVER:TCON %s, (@%s:%s)' % ave_filter_type % cha %chb) 
    #     self.write('SENS:CURR:AVER:COUN %s, (@%s:%s)' % filter_cnt % cha %chb)
    #     self.write('SENS:CURR:AVER %s, (@%s:%s)' % en_filter % cha %chb)
    #     self.write('ROUT:SCAN:CRE (@a:b)')  
    #     self.write('ROUT:SCAN:COUN:SCAN %s' % count)  
    #     self.write('ROUT:SCAN:INT %s' % delay)   
    #     self.init()
    #     self.wait()

    #     read = self.read_buffer()
    #     self.query('TRAC:DATA? %s, %s, "%s", READ' % num_readings_a % num_readings_b % debuf_name)          
    #     return read

    # def measure_res_m(self, readings=100, debuf_name='debuffer3', cha=1, chb=9, 
    #                         res_range=5, nplc=10, azero='ON', ave_filter_type='REP',
    #                         filter_cnt=10, en_filter='ON', count=10, delay=1.0,
    #                         num_readings_a=1, num_readings_b=99):

    #     self.query('TRAC:CLE?')                                     #clearing debuffer1
    #     self.write('TRAC:POIN %s, "%s"' % readings % debuf_name)    #set debuffer1 to 100 readings
    #     self.write('ROUT:SCAN (@%s:%s)' % cha % chb)                #Set channels 1 to 9 on slot 1 to make DC voltage

    #     self.write('SENS:FUNC "RES",(@%s:%s)' % cha % chb)    
    #     self.write('SENS:RES:RANG %s, (@%s:%s)' % res_range % cha % chb)    
    #     self.write('SENS:RES:NPLC %s, (@%s:%s)' % nplc % cha % chb)    
    #     self.write('SENS:RES:AZER %s, (@%s:%s)' % azero % cha % chb)

    #     self.write('SENS:RES:AVER:TCON %s, (@%s:%s)' % ave_filter_type % cha %chb)
    #     self.write('SENS:RES:AVER:COUN %s, (@%s:%s)' % filter_cnt % cha % chb)
    #     self.write('SENS:RES:AVER %s, (@%s:%s)' % en_filter)

    #     self.write('ROUT:SCAN:CRE (@a:b)')  
    #     self.write('ROUT:SCAN:COUN:SCAN %s' % count)  
    #     self.write('ROUT:SCAN:INT %s' % delay)  
    #     self.init()
    #     self.wait()

    #     read = self.read_buffer()
    #     self.query('TRAC:DATA? %s, %s, "%s", READ' % num_readings_a % num_readings_b % debuf_name)          
    #     return read

# class DMM6500_M:
#     def __init__(self, tcp_ip_or_serial='XXX'):
#         try:
#             self.rm = ResourceManager()
#             self.instrument_list = self.rm.list_resources()

#             self.address = [elem for elem in self.instrument_list if (elem.find('TCPIP') != -1 and elem.find(
#                 tcp_ip_or_serial) != -1)] 

#             if self.address.__len__() == 0:
#                 self.status = "Not Connected"
#                 print("Could not connect to device")
#             else:
#                 self.address = self.address[0]
#                 self.device = self.rm.open_resource(self.address)
#                 self.status = "Connected"
#                 self.connected_with = 'TCP'
#                 print("Connected to " + self.address)

#         except VisaIOError:
#             self.status = "Not Connected"
#             print("PyVISA is not able to find any devices")
        
#     def write(self, cmd):
#         self.device.write(cmd)
#         time.sleep(_delay)
#         return
    
#     def query(self, cmd):
#         self.device.query(cmd)
#         time.sleep(_delay)
#         return

#     def reset(self):
#         command = '*RST'
#         self.write(command)

#     # Measure Voltage
#     def measure_voltage(self, signal='DC'):   
#         command = ':MEAS:VOLT:%s?' % signal
#         self.query(command)

#     def measure_current(self, signal='DC'):    
#         command = ':MEAS:CURR:%s?' % signal
#         self.query(command)

#     def measure_res(self):   
#         command = ':MEAS:RES?'
#         self.query(command)

#     def measure_diode(self):   
#         command = ':MEAS:DIOD?'
#         self.query(command)

#     def measure_capacitance(self):   
#         command = ':MEAS:CAP?'
#         self.query(command)
    
#     def measure_temp(self):   
#         command = ':MEAS:TEMP?'
#         self.query(command)
    
#     def measure_freq(self):   
#         command = ':MEAS:FREQ?'
#         self.query(command)

#     def measure_period(self):   
#         command = ':MEAS:PER?'
#         self.query(command)

#     # Sense
#     # The SENSe1 subsystem commands configure and control the measurement functions of the instrument.
#     # Scan channels from a to b, sign=DC or AC
#     def sense_voltage(self, sign, a, b):   
#         command = 'SENS:FUNC "VOLT"%s",(@%s:%s)' % sign % a % b
#         self.query(command)

#     def sense_curr(self, sign, a, b):   
#         command = 'SENS:FUNC "CURR"%s",(@%s:%s)' % sign % a % b
#         self.query(command)

#     def sense_volt_range(self, val, a, b):   
#         command = 'SENS:VOLT:RANG %s, (@%s:%s)' % val % a % b
#         self.query(command)

#     #Measurement resolution
#     def sense_volt_nplc(self, val, a, b):   
#         command = 'SENS:VOLT:NPLC %s, (@%s:%s)' % val % a % b
#         self.query(command)

#     def sense_volt_dig(self, val, a, b):   
#         command = 'SENS:VOLT:DIG %s, (@%s:%s)' % val % a % b
#         self.query(command)

#     # Clears debuffer1
#     def trace_clear(self):   
#         command = 'TRAC:CLE?'
#         self.query(command)

#     # Set it to <value> readings.
#     def trace_setpoints(self, value, buf_name):   
#         command = 'TRACe:POINts %s, "%s"' % value % buf_name
#         self.query(command)

#     #output data from j to k stored in buf_name
#     def trace_show_data(self, j, k, buf_name):   
#         command = 'TRAC:DATA? %s, %s, "%s", READ' % j % k % buf_name
#         self.query(command)

#     # Scan channels from a to b
#     def route_scan(self, a, b):   
#         command = 'ROUT:SCAN (@%s:%s)' % a % b
#         self.query(command)

#     # Create scan channels
#     def route_scan_create(self, a, b):   
#         command = 'ROUT:SCAN:CRE (@a:b)'
#         self.query(command)

#     #Set the scan count
#     def route_scan_count(self, count):   
#         command = 'ROUT:SCAN:COUN:SCAN %s' % count
#         self.query(command)

#     # specifies the interval time between scan
#     def route_scan_delay(self, delay):   
#         command = 'ROUTe:SCAN:INT %s' % delay
#         self.query(command)

#     # Display n digits
#     def disp_volt(self, n, a, b):   
#         command = 'DISP:VOLT:DIG %s, (@%s:%s)' % n % a % b
#         self.query(command)


    


        


        

        