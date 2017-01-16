import smbus
import time
address = 0x20
address2 = 0x21
address3 = 0x22
address4 = 0x23

#Seg_Test = 0x01

disp1 = 0xD0
disp2 = 0x30

disp1_1 = 0x00
disp2_1 = 0x00


# Define all the registers
IODIR = 0x00
IPOL = 0x01
GPINTEN = 0x02
DEFVAL = 0x03
INTCON = 0x04
IOCON = 0x05
GPPU = 0x06
INTF = 0x07
INTCAP = 0x08
GPIO = 0x09
OLAT = 0x0A


bus = smbus.SMBus(0) # Change to 0 for revision 1 Raspberry Pi

# Set IODIR as OUTPUT
bus.write_byte_data(address, IODIR, 0b00000000)
bus.write_byte_data(address2, IODIR, 0b00000000)
bus.write_byte_data(address3, IODIR, 0b00000000)
bus.write_byte_data(address4, IODIR, 0b00000000)

# Reset all the other registers
for reg in [IPOL,GPINTEN,DEFVAL,INTCON,IOCON,GPPU,INTF,INTCAP,GPIO,OLAT]:
    bus.write_byte_data(address, reg, 0b00000000)
    bus.write_byte_data(address2, reg, 0b00000000)
    bus.write_byte_data(address3, reg, 0b00000000)
    bus.write_byte_data(address4, reg, 0b00000000)
    bus.write_byte_data(address, GPIO, 0x00)
    bus.write_byte_data(address2, GPIO, 0x00)
    bus.write_byte_data(address3, GPIO, 0x00)
    bus.write_byte_data(address4, GPIO, 0x00)
while True:
    #Seg_Input = raw_input("\nEnter a bit number 0 to 7:  ")
    #Seg_Test = 0x01 << int(Seg_Input)
    bus.write_byte_data(address, GPIO, disp1 | disp1_1)
    bus.write_byte_data(address2, GPIO, disp2 | disp2_1)
    #bus.write_byte_data(address3, GPIO, Seg_Test)
    #bus.write_byte_data(address4, GPIO, Seg_Test)
    #time.sleep(1)
    #bus.write_byte_data(address, GPIO, 0x00)
    #bus.write_byte_data(address2, GPIO, 0x00)
    #bus.write_byte_data(address3, GPIO, 0x00)
    #bus.write_byte_data(address4, GPIO, 0x00)
    #time.sleep(1)

