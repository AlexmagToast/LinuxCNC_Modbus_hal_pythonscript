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
def print_pins_states(binary_data):
    if len(binary_data) != 16:
        raise ValueError("Binary data length must be 16 bits.")

    for pin_number, state_char in enumerate(binary_data, start=1):
        state = int(state_char)
        print(f"Pin Number: {pin_number:2d}  State: {state}")



while True:
    time.sleep(0.1)
    try:
        #N4DIH32
        N4DIH32 = minimalmodbus.Instrument('/dev/ttyUSB0',1)
        N4DIH32.serial.baudrate = 9400

        data = N4DIH32.read_register(192,1)
        print(print_pins_states(data))
        time.sleep(0.1)
        data = N4DIH32.read_register(193,1)
        print(print_pins_states(data))
    except: 
        pass



