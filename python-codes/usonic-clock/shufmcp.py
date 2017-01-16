import smbus
import time
address = 0x20
address2 = 0x21
address3 = 0x22
address4 = 0x23

#Seg_Test = 0x01

min_data = (
    {'dig': 0, 'IC1-DISP1': 0xE0, 'IC2-DISP1': 0x38, 'IC1-DISP2': 0x0E, 'IC2-DISP2': 0x83},
    {'dig': 1, 'IC1-DISP1': 0x40, 'IC2-DISP1': 0x08, 'IC1-DISP2': 0x08, 'IC2-DISP2': 0x80},
    {'dig': 2, 'IC1-DISP1': 0xD0, 'IC2-DISP1': 0x30, 'IC1-DISP2': 0x0D, 'IC2-DISP2': 0x03},
    {'dig': 3, 'IC1-DISP1': 0xD0, 'IC2-DISP1': 0x18, 'IC1-DISP2': 0x0D, 'IC2-DISP2': 0x82},
    {'dig': 4, 'IC1-DISP1': 0x70, 'IC2-DISP1': 0x08, 'IC1-DISP2': 0x0B, 'IC2-DISP2': 0x80},
    {'dig': 5, 'IC1-DISP1': 0xB0, 'IC2-DISP1': 0x18, 'IC1-DISP2': 0x07, 'IC2-DISP2': 0x82},
    {'dig': 6, 'IC1-DISP1': 0xB0, 'IC2-DISP1': 0x38, 'IC1-DISP2': 0x07, 'IC2-DISP2': 0x83},
    {'dig': 7, 'IC1-DISP1': 0xC0, 'IC2-DISP1': 0x08, 'IC1-DISP2': 0x0C, 'IC2-DISP2': 0x80},
    {'dig': 8, 'IC1-DISP1': 0xF0, 'IC2-DISP1': 0x38, 'IC1-DISP2': 0x0F, 'IC2-DISP2': 0x83},
    {'dig': 9, 'IC1-DISP1': 0xF0, 'IC2-DISP1': 0x18, 'IC1-DISP2': 0x0F, 'IC2-DISP2': 0x82}
)

hrs_data = (
    {'dig': 0, 'IC1-DISP1': 0x0E, 'IC2-DISP1': 0xE0, 'IC1-DISP2': 0xE0, 'IC2-DISP2': 0x0D},
    {'dig': 1, 'IC1-DISP1': 0x02, 'IC2-DISP1': 0x80, 'IC1-DISP2': 0x20, 'IC2-DISP2': 0x08},
    {'dig': 2, 'IC1-DISP1': 0x0C, 'IC2-DISP1': 0xD0, 'IC1-DISP2': 0xC0, 'IC2-DISP2': 0x0E},
    {'dig': 3, 'IC1-DISP1': 0x06, 'IC2-DISP1': 0xD0, 'IC1-DISP2': 0x60, 'IC2-DISP2': 0x0E},
    {'dig': 4, 'IC1-DISP1': 0x02, 'IC2-DISP1': 0xB0, 'IC1-DISP2': 0x20, 'IC2-DISP2': 0x0B},
    {'dig': 5, 'IC1-DISP1': 0x06, 'IC2-DISP1': 0x70, 'IC1-DISP2': 0x60, 'IC2-DISP2': 0x07},
    {'dig': 6, 'IC1-DISP1': 0x0E, 'IC2-DISP1': 0x70, 'IC1-DISP2': 0xE0, 'IC2-DISP2': 0x07},
    {'dig': 7, 'IC1-DISP1': 0x02, 'IC2-DISP1': 0xC0, 'IC1-DISP2': 0x20, 'IC2-DISP2': 0x0C},
    {'dig': 8, 'IC1-DISP1': 0x0E, 'IC2-DISP1': 0xF0, 'IC1-DISP2': 0xE0, 'IC2-DISP2': 0x0F},
    {'dig': 9, 'IC1-DISP1': 0x06, 'IC2-DISP1': 0xF0, 'IC1-DISP2': 0x60, 'IC2-DISP2': 0x0F}
)

disp1   = 0x0E
disp2 = 0x83

disp1_1 = 0xE0
disp2_1 = 0x38


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
    #bus.write_byte_data(address, GPIO, disp1 | disp1_1)
    #bus.write_byte_data(address2, GPIO, disp2 | disp2_1)
    #bus.write_byte_data(address3, GPIO, Seg_Test)
    #bus.write_byte_data(address4, GPIO, Seg_Test)
    #time.sleep(1)
    #bus.write_byte_data(address, GPIO, 0x00)
    #bus.write_byte_data(address2, GPIO, 0x00)
    #bus.write_byte_data(address3, GPIO, 0x00)
    #bus.write_byte_data(address4, GPIO, 0x00)
    #time.sleep(1)

    for index in range(0,10):
   #index = int(Seg_Input)
   # print (min_data[index]),
    #print (format(min_data[index]['IC1-DISP1'], '#04X')),
    #print (format(min_data[index]['IC2-DISP1'], '#04X'))
    #bus.write_byte_data(address, GPIO, min_data[index]['IC1-DISP1'])
    #bus.write_byte_data(address2, GPIO, min_data[index]['IC2-DISP1'])

    #print (format(min_data[index]['IC1-DISP2'], '#04X')),
    #print (format(min_data[index]['IC2-DISP2'], '#04X'))
        bus.write_byte_data(address, GPIO, min_data[index]['IC1-DISP1'] | min_data[index]['IC1-DISP2'])
        bus.write_byte_data(address2, GPIO, min_data[index]['IC2-DISP1'] | min_data[index]['IC2-DISP2'])

        bus.write_byte_data(address3, GPIO, hrs_data[index]['IC1-DISP1'] | hrs_data[index]['IC1-DISP2'])
        bus.write_byte_data(address4, GPIO, hrs_data[index]['IC2-DISP1'] | hrs_data[index]['IC2-DISP2'])
    
        time.sleep(1)
