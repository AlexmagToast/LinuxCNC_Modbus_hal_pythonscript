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

for port in range(32):
    c.newpin("N4DIH32.{}".format(port), hal.HAL_BIT, hal.HAL_OUT)
    c.newparam("N4DIH32.{}-invert".format(port), hal.HAL_BIT, hal.HAL_RW)

c.newpin("SZGH.spindlecurrent", hal.HAL_FLOAT, hal.HAL_OUT)
    
N4DIH32 = minimalmodbus.Instrument('/dev/ttyUSB0',1)
N4DIH32.serial.baudrate = 9400
    
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
        
while True:
    time.sleep(0.1)
    
    try:
        readSZGH()
        readN4DIH32()

         
    except: 
        pass
    



