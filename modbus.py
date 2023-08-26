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
    [0x2100,"serial_number_of_motor_type",3,1],
    [0x2102,"poles_number_of_motor",3,1],
    [0x2104,"rated_frequency_of_motor",3,1],
    [0x2106,"max_frequency_of_motor",3,1],
    [0x2108,"motor_rated_voltage",3,1],
    [0x210A,"motor_rated_current",3,1],
    [0x210C,"motor_rated_torque",3,1],
    [0x210E,"rated_excitation_current_of_motor",3,1],
    [0x2110,"excitation_current_coefficient_of_motor",3,1],
    [0x2112,"weak_magnetic_coefficient_of_motor",3,1],
    [0x2114,"motor_monent_of_inertia",3,1],
    [0x2116,"motor_zero_speed_torque_multiple",3,1],
    [0x2118,"motor_rated_torque_multiple",3,1],
    [0x211A,"motor_constat_power_max_speed",3,1],
    [0x211C,"motor_zero_slip_compensate_coef",3,1],
    [0x211E,"motor_rated_slip_compensate_coef",3,1],
    [0x2120,"motor_max_slip_compensate_coef",3,1],
    [0x2122,"motor_zero_slip_compensate_coef_speed",3,1],
    [0x2140,"hi_motor_sn",3,1],
    [0x2142,"motor_pole_number(H)",3,1],
    [0x2144,"motor_rated_frequency(H)",3,1],
    [0x2146,"motor_max_frequency(H)",3,1],
    [0x2148,"motor_rated_voltage(H)",3,1],
    [0x214A,"motor_rated_current(H)",3,1],
    [0x214C,"motor_rated_torque(H)",3,1],
    [0x2150,"motor_flux_current_coff(H)",3,1],
    [0x2152,"motor_rated_flux_weak_coff",3,1],
    [0x2154,"motor_monent_of_inertia",3,1],
    [0x2156,"motor_zero_speed_torque_multiple",3,1],
    [0x2158,"motor_rated_speed_torque_multiple",3,1],
    [0x215C,"motor_zero_slip_compensate_coff",3,1],
    [0x215E,"motor_rated_slip_compensate_coff",3,1],
    [0x2160,"motor_max_slip_compensate_coff",3,1],
    [0x2162,"motor_zero_slip_compensate_coff_speed",3,1],
    [0x2180,"double_switch_state",3,1],
#Seite_51
    [0x2900,"accurate_stop_control_type",3,1],
    [0x2902,"accurate_stop_feedback_source",3,1],
    [0x2904,"accureate_stop_dec",3,1],
    [0x2906,"accurate_stop_search_z-speed",3,1],
    [0x2908,"accurate_stop_pos_max_speed",3,1],
    [0x290E,"accurate_stop_stiff",3,1],
    [0x2914,"accurate_stop_precision",3,1],
    [0x2918,"accurate_stop_position_1",3,1],
    [0x291A,"accurate_stop_position_2",3,1],
    [0x291C,"accurate_stop_position_3",3,1],
    [0x291E,"accurate_stop_position_4",3,1],
    [0x2980,"speed_algorithm_type",3,1],
    [0x2982,"speed_feedback_source",3,1],
    [0x2984,"speed_ins_type",3,1],
    [0x2986,"speed_zero_lock_time_delay",3,1],
    [0x2988,"speed_control_s-curve_time",3,1],
    [0x298A,"speed_control_max_speed",3,1],
    [0x298C,"speed_control_min_speed",3,1],
    [0x298E,"speed_control_low_speed_acc",3,1],
    [0x2990,"speed_control_low_speed_dec",3,1],
    [0x2992,"speed_control_adj_speed_sw_point",3,1],
    [0x2994,"speed_control_hi_speed_acc",3,1],
    [0x2996,"speed_control_hi_speed_dec",3,1],
    [0x2998,"speed_control_reach_field",3,1],

#Seite_52
    [0x299A,"speed_control_ins_gear_ratio",3,1],
    [0x299C,"speed_control_speed_ins_dir",3,1],
    [0x299E,"speed_control_speed_inv_disable",3,1],
    [0x29A4,"speed_control_speed_ins_resolution",3,1],
    [0x29A6,"speed_control_mbus_target_speed",3,1],
    [0x29A8,"gear_speed_0",3,1],
    [0x29AA,"gear_speed_1",3,1],
    [0x29AC,"gear_speed_2",3,1],
    [0x29AE,"gear_speed_3",3,1],
    [0x29B0,"gear_speed_4",3,1],
    [0x29B2,"gear_speed_5",3,1],
    [0x29B4,"gear_speed_6",3,1],
    [0x29B6,"gear_speed_7",3,1],
    [0x29B8,"gear_speed_8",3,1],
    [0x29BA,"gear_speed_9",3,1],
    [0x29BC,"gear_speed_10",3,1],
    [0x29BE,"gear_speed_11",3,1],
    [0x29C0,"gear_speed_12",3,1],
    [0x29C2,"gear_speed_13",3,1],
    [0x29C4,"gear_speed_14",3,1],
    [0x29C6,"gear_speed_15",3,1],
    [0x29C8,"zero_speed_no_output_range",3,1],
    [0x2A00,"torque_ins_type",3,1],
    [0x2A02,"max_torque",3,1],
    [0x2A04,"torque_acc",3,1],
    [0x2A06,"torque_dec",3,1],
    [0x2A08,"torque_ins_dir",3,1],
]

"""
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
"""
def setup_SZGH_monitoring_adresses():
    for entry in range(len(SZGH_monitoring_adresses)):
        if SZGH_monitoring_adresses[entry][2] == 0:
            c.newpin("SZGH.mon.{}".format(SZGH_monitoring_adresses[entry][1]), hal.HAL_BIT, hal.HAL_OUT)
        if SZGH_monitoring_adresses[entry][2] == 1:
            c.newpin("SZGH.mon.{}".format(SZGH_monitoring_adresses[entry][1]), hal.HAL_S32, hal.HAL_OUT)
        if SZGH_monitoring_adresses[entry][2] == 2:
            c.newpin("SZGH.mon.{}".format(SZGH_monitoring_adresses[entry][1]), hal.HAL_FLOAT, hal.HAL_OUT)
        

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


