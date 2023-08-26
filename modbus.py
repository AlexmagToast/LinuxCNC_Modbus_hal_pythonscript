#!/usr/bin/env python3.9
import hal, minimalmodbus, time

# The baud rate is 9600, but it can be changed by writing an int number in the range of 0-4 to register 255, as follows:

#0 = 1200
#1 = 2400
#2 = 4800
#3 = 9600
#4 = 19200

#The state of the input pins is stored in registers 128 to 159 (32 registers, with one register for each input pin).

#There are also registers 192 and 193 that store the input values but in a slightly different format. For example:

#If input pin X00 = 1, then the register at address 192 = 1. Then, further:

#X01 = 1 (X00 = 0); register at address 192 = 2;
#X02 = 1 (X00; X01 = 0) register at address 192 = 4;
#X03 = 1 (X00; X01; X02 = 0) register at address 192 = 8
#Or for example, if X00 = 1 and X01 = 1, then the register at address 192 = 3, and so on for the first group of 16 pins where the maximum value of the register is 32768.
#The register at address 193 works the same, but for the next 16 input pins.

#The device address is changed using the "DIP switch," where address 1 has already been selected.
c = hal.component("modbus") 	#name that we will cal pins from in hal



"""SZGH_monitoring_adresses = [
    #[adress,name of Parameter,0=bit 1=int 2=float,0=IN, 1=Out 2=RW]
    [0x2404,"running_of_math",3,1],
    [0x2228,"motor_output_current",3,1],
    [0x2238,"motor_output_torque",3,1],
    [0x2408,"motor_command_frequency",3,1],
    [0x240A,"motor_output_frequency",3,1],
    [0x2276,"motor_speed",3,1],
    [0x2364,"digital_input_monitor",3,1],
    [0x23B0,"digital_output_monitor",3,1],
    [0x2316,"non-revised_analog_input_value",3,1],
    [0x2318,"corrected_analog_input_value",3,1],
    [0x2272,"motor_encoder_counter",3,1],
    [0x2274,"motor_axis_absolute_position",3,1],
    [0x2356,"external_pulse_counting",3,1],
    [0x2358,"external_pulse_frequency",3,1],
    [0x240C,"position_coding_pulse",3,1],
    [0x240E,"position_coding_frequency",3,1],
    [0x2410,"position_following_error",3,1],
    [0x2804,"motor_setting_speed(panel_control)",3,1],
    [0x2806,"motor_acceleration(panel_control)",3,1],
    [0x2808,"motor_deceleration(panel_control)",3,1],
    [0x280A,"motor_rotate_direction(panel_control)",3,1],
    [0x2800,"control_mode",3,1],
    [0x4102,"no.0_error",3,1],
    [0x4120,"no.1_error",3,1],
    [0x413E,"no.2_error",3,1],
    [0x415C,"no.3_error",3,1],
    [0x417A,"no.4_error",3,1],
    [0x4198,"no.5_error",3,1],
]"""

SZGH_parameter_adresses = [
    #[adress,name_of_Parameter,0=bit_1=int_2=float,0=IN,_1=Out_2=RW]
    #Seite_41
    [0x2100,"P01_00",2,1],
    [0x2102,"P01_01",2,1],
    [0x2104,"P01_02",2,1],
    [0x2106,"P01_03",2,1],
    [0x2108,"P01_04",2,1],
    [0x210A,"P01_05",2,1],
    [0x210C,"P01_06",2,1],
    [0x210E,"P01_07",2,1],
    [0x2110,"P01_08",2,1],
    [0x2112,"P01_09",2,1],
    [0x2114,"P01_10",2,1],
    [0x2116,"P01_11",2,1],
    [0x2118,"P01_12",2,1],
    [0x211A,"P01_13",2,1],
    [0x211C,"P01_14",2,1],
    [0x211E,"P01_15",2,1],
    [0x2120,"P01_16",2,1],
    [0x2122,"P01_17",2,1],
    [0x2140,"P02_00",2,1],
    [0x2142,"P02_01",2,1],
    [0x2144,"P02_02",2,1],
    [0x2146,"P02_03",2,1],
    [0x2148,"P02_04",2,1],
    [0x214A,"P02_05",2,1],
    [0x214C,"P02_06",2,1],
    [0x2150,"P02_08",2,1],
    [0x2152,"P02_09",2,1],
    [0x2154,"P02_10",2,1],
    [0x2156,"P02_11",2,1],
    [0x2158,"P02_12",2,1],
    [0x215C,"P02_14",2,1],
    [0x215E,"P02_15",2,1],
    [0x2160,"P02_16",2,1],
    [0x2162,"P02_17",2,1],
    [0x2180,"P03_00",2,1],
#Seite_51
    [0x28A8,"P53_20",2,1],
    [0x2900,"P54_00",2,1],
    [0x2902,"P54_01",2,1],
    [0x2904,"P54_02",2,1],
    [0x2906,"P54_03",2,1],
    [0x2908,"P54_04",2,1],
    [0x290E,"P54_07",2,1],
    [0x2914,"P54_10",2,1],
    [0x2918,"P54_12",2,1],
    [0x291A,"P54_13",2,1],
    [0x291C,"P54_14",2,1],
    [0x291E,"P54_15",2,1],
    [0x2980,"P55_00",2,1],
    [0x2982,"P55_01",2,1],
    [0x2984,"P55_02",2,1],
    [0x2986,"P55_03",2,1],
    [0x2988,"P55_04",2,1],
    [0x298A,"P55_05",2,1],
    [0x298C,"P55_06",2,1],
    [0x298E,"P55_07",2,1],
    [0x2990,"P55_08",2,1],
    [0x2992,"P55_09",2,1],
    [0x2994,"P55_10",2,1],
    [0x2996,"P55_11",2,1],
    [0x2998,"P55_12",2,1],

#Seite_52
    [0x299A,"P55_13",2,1],
    [0x299C,"P55_14",2,1],
    [0x299E,"P55_15",2,1],
    [0x29A4,"P55_18",2,1],
    [0x29A6,"P55_19",2,1],
    [0x29A8,"P55_20",2,1],
    [0x29AA,"P55_21",2,1],
    [0x29AC,"P55_22",2,1],
    [0x29AE,"P55_23",2,1],
    [0x29B0,"P55_24",2,1],
    [0x29B2,"P55_25",2,1],
    [0x29B4,"P55_26",2,1],
    [0x29B6,"P55_27",2,1],
    [0x29B8,"P55_28",2,1],
    [0x29BA,"P55_30",2,1],
    [0x29BC,"P55_31",2,1],
    [0x29BE,"P55_32",2,1],
    [0x29C0,"P55_33",2,1],
    [0x29C2,"P55_34",2,1],
    [0x29C4,"P55_35",2,1],
    [0x29C6,"P55_36",2,1],
    [0x29C8,"P55_37",2,1],
    [0x2A00,"P56_00",2,1],
    [0x2A02,"P56_01",2,1],
    [0x2A04,"P56_02",2,1],
    [0x2A06,"P56_03",2,1],
    [0x2A08,"P56_04",2,1],
]


SZGH_monitoring_adresses = [
    #[adress,code,0=bit 1=int 2=float,0=IN, 1=Out 2=RW]
    [0x2404,"RUN",1,1],
    [0x2228,"Ao",2,1],
    [0x2238,"To",2,1],
    [0x2408,"FI",2,1],
    [0x240A,"Fo",2,1],
    [0x2276,"Fr",2,1],
    [0x2364,"d1-d8",1,1],
    [0x23B0,"o1-o4",1,1],
    [0x2316,"A0",2,1],
    [0x2318,"A1",2,1],
    [0x2272,"P",2,1],
    [0x2274,"H",1,1],
    [0x2356,"E",2,1],
    [0x2358,"F",2,1],
    [0x240C,"C",2,1],
    [0x240E,"L",2,1],
    [0x2410,"U",2,1],
    [0x2804,"nc",2,1],
    [0x2806,"Ac",2,1],
    [0x2808,"dc",2,1],
    [0x280A,"FE",2,1],
    [0x2800,"oP",2,1],
    [0x4102,"Er0",0,1],
    [0x4120,"Er1",0,1],
    [0x413E,"Er2",0,1],
    [0x415C,"Er3",0,1],
    [0x417A,"Er4",0,1],
    [0x4198,"Er5",0,1],
]

def setup_SZGH_monitoring_adresses():
    for entry in range(len(SZGH_monitoring_adresses)):
        if SZGH_monitoring_adresses[entry][2] == 0:
            c.newpin("SZGH.mon.{}".format(SZGH_monitoring_adresses[entry][1]), hal.HAL_BIT, hal.HAL_OUT)
        if SZGH_monitoring_adresses[entry][2] == 1:
            c.newpin("SZGH.mon.{}".format(SZGH_monitoring_adresses[entry][1]), hal.HAL_S32, hal.HAL_OUT)
        if SZGH_monitoring_adresses[entry][2] == 2:
            c.newpin("SZGH.mon.{}".format(SZGH_monitoring_adresses[entry][1]), hal.HAL_FLOAT, hal.HAL_OUT)
        
def setup_SZGH_parameter_adresses():
    for entry in range(len(SZGH_parameter_adresses)):
        if SZGH_parameter_adresses[entry][2] == 0:
            c.newpin("SZGH.par.{}".format(SZGH_parameter_adresses[entry][1]), hal.HAL_BIT, hal.HAL_OUT)
        if SZGH_parameter_adresses[entry][2] == 1:
            c.newpin("SZGH.par.{}".format(SZGH_parameter_adresses[entry][1]), hal.HAL_S32, hal.HAL_OUT)
        if SZGH_parameter_adresses[entry][2] == 2:
            c.newpin("SZGH.par.{}".format(SZGH_parameter_adresses[entry][1]), hal.HAL_FLOAT, hal.HAL_OUT)
        


def read_SZGH_monitoring_adresses():
    for entry in range(len(SZGH_monitoring_adresses)):  
        time.sleep(0.1)
        try:
            registry = SZGH_monitoring_adresses[entry][0]                
            if SZGH_monitoring_adresses[entry][2] == 0:
                data = SZGH.read_bit(registry)
                c["SZGH.mon.{}".format(SZGH_monitoring_adresses[entry][1])] = data
            if SZGH_monitoring_adresses[entry][2] == 1:
                data = SZGH.read_register(registry)
                c["SZGH.mon.{}".format(SZGH_monitoring_adresses[entry][1])] = data
            if SZGH_monitoring_adresses[entry][2] == 2:
                data = SZGH.read_float(registry)
                c["SZGH.mon.{}".format(SZGH_monitoring_adresses[entry][1])] = data    
            
        except:
            c["SZGH.mon.{}".format(SZGH_monitoring_adresses[entry][1])] = 5


def read_SZGH_paramter_adresses():
    for entry in range(len(SZGH_monitoring_adresses)):  
        time.sleep(0.1)
        try:
            registry = SZGH_monitoring_adresses[entry][0]                
            if SZGH_monitoring_adresses[entry][2] == 0:
                data = SZGH.read_bit(registry)
                c["SZGH.par.{}".format(SZGH_monitoring_adresses[entry][1])] = data
            if SZGH_monitoring_adresses[entry][2] == 1:
                data = SZGH.read_register(registry)
                c["SZGH.par.{}".format(SZGH_monitoring_adresses[entry][1])] = data
            if SZGH_monitoring_adresses[entry][2] == 2:
                data = SZGH.read_float(registry)
                c["SZGH.par.{}".format(SZGH_monitoring_adresses[entry][1])] = data    
            
        except:
            c["SZGH.par.{}".format(SZGH_monitoring_adresses[entry][1])] = 5
            

def read_SZGH_parameter_adresses():
    time.sleep(0.1)
    for entry in range(len(SZGH_parameter_adresses)):  
        try:
            registry = SZGH_parameter_adresses[entry][0]
            #data = SZGH.read_float(registry,3)
            #c[SZGH_monitoring_adresses[entry][1]] = data
            print(registry)
        except:
            #c["SZGH.spindlecurrent"] = 0
            pass
            



for port in range(32):
    c.newpin("N4DIH32.{}".format(port), hal.HAL_BIT, hal.HAL_OUT)
    c.newparam("N4DIH32.{}-invert".format(port), hal.HAL_BIT, hal.HAL_RW)


N4DIH32 = minimalmodbus.Instrument('/dev/ttyUSB0',1)
N4DIH32.serial.baudrate = 9600
    
SZGH = minimalmodbus.Instrument('/dev/ttyUSB0',48)
        

def readN4DIH32():
    data = N4DIH32.read_register(192)
    for pin_number in range(16):
        state = bool((data >> pin_number) & 1)
        c["N4DIH32.{}".format(pin_number)] = state
    time.sleep(0.1)
    data = N4DIH32.read_register(193)
    for pin_number in range(16):
        state = bool((data >> pin_number) & 1)
        c["N4DIH32.{}".format(pin_number+16)] = state


def readSZGH():
    try:
        pin_number = 0x2228
        data = SZGH.read_float(pin_number,3)
        c["SZGH.spindlecurrent"] = data    
    except:
        c["SZGH.spindlecurrent"] = 0

setup_SZGH_monitoring_adresses()


while True:
    time.sleep(0.1)
    
    try:
        readN4DIH32()
        #read_SZGH_parameter_adresses()
        read_SZGH_monitoring_adresses()
        
         
    except KeyboardInterrupt:
        exit()

    except: 
        pass


