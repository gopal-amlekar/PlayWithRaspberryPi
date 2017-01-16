import smbus
import time
import datetime

address = 0x68

# Define all the registers
SECONDS = 0x00
MINUTES = 0x01
HOURS = 0x02
DAY = 0x03
DATE = 0x04
MONTH = 0x05
YEAR = 0x06

CONTROL = 0x0E
STATUS = 0x0F

bus = smbus.SMBus(0) # Change to 0 for revision 1 Raspberry Pi

now = datetime.datetime.now()
prevsec = 255

sec_10 = now.second/10
sec_1 = now.second%10

min_10 = now.minute/10
min_1 = now.minute%10

#print now.minute
#print min_10, min_1

sec_to_write = (sec_10 << 4) | sec_1
min_to_write = (min_10 << 4) | min_1

print now.hour

if (now.hour > 12):
    ampm = 1
    hrs = now.hour - 12
else:
    ampm = 0
    hrs = now.hour
    
hrs_10 = hrs/10
hrs_1 = hrs%10

hrs_to_write = (hrs_10 << 4) | hrs_1

print hrs_to_write

if (ampm):
    hrs_to_write |= 0x20

hrs_to_write |= 0x40

print hrs_to_write

bus.write_byte_data(address, SECONDS, sec_to_write)
bus.write_byte_data(address, MINUTES, min_to_write)
bus.write_byte_data(address, HOURS, hrs_to_write)

while True:
    sec = bus.read_byte_data(address, SECONDS)
    mints = bus.read_byte_data(address, MINUTES)
    hrs = bus.read_byte_data(address, HOURS)
    
    sec_data = ( ( (sec & 0xF0) >> 4 )*10) + (sec & 0x0F)
    min_data = ( ( (mints & 0xF0) >> 4 )*10) + (mints & 0x0F)
    hrs_data = ( ( (hrs & 0x10) >> 4 ) *10) + (hrs & 0x0F)
    
    if (sec_data != prevsec):
        print str(hrs_data) + ":" + str(min_data) + ":" + str(sec_data)
        prevsec = sec_data


# Set IODIR as OUTPUT
#bus.write_byte_data(address, IODIR, 0b00000000)

# Reset all the other registers
#for reg in [IPOL,GPINTEN,DEFVAL,INTCON,IOCON,GPPU,INTF,INTCAP,GPIO,OLAT]:
#    bus.write_byte_data(address, reg, 0b00000000)

#while True:
#    bus.write_byte_data(address, GPIO, 0xFF)
#    time.sleep(1)
#    bus.write_byte_data(address, GPIO, 0x00)
#    time.sleep(1)

