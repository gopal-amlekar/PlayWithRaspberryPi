# Python code to control the ultrasonic digitcal clock based on Raspberry Pi
# TODO:
# 1. Make it modular
# 2. Add error handling (like, handle signals for kill, interrupt etc.)
# 3. Spawn / fork a process for usonic sensor and keep only I2C in this module (or the other way round)



import smbus            # Required to communicate to I2C devices
import time             # Required to measure time lapse between trigger and echo of HC-SR04 sensor
import RPi.GPIO as GPIO # Required to control the trigger and echo pins of HC-SR04 sensor
import syslog           # Required to print any messages to system log instead of console when we run this code in background


GPIO.setmode(GPIO.BCM)  # We are using BCM mode i.e. refer the Pi pins as GPIO pin numbers instead of physical pin numbers
GPIO.setwarnings(False) # Just so it doesn't clutter the console / system log
TRIG = 18               # HC-SR04 trigger pin connected to GPIO 18 which is board pin 12
ECHO = 17               # HC-SR04 echo pin connected to GPIO 17 which is board pin 11

# I2C addresses of the 4 I/O expanders used. 0x20 represnts the rightmost display showing minutes (unit digit)
mcp_address1 = 0x20
mcp_address2 = 0x21
mcp_address3 = 0x22
mcp_address4 = 0x23

# I2C address of DS1307
address_rtc = 0x68

# This look-up table is used to take care of the wierd connections of MCP23008 ICs to the displays
# A dictionary is used with key-value pairs. 'dig' key is only for reference and not used in code
# IC1-DISP1 key corresponds to the data to be sent to MCP23008 (0x20) to display part of the 'dig' digit on it.
# Similarly, IC2-DISP1 value should be sent to MCP23008 (0x21) at the same time to display the remaining part of 'dig' digit on it


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

# Similar array as above for the hours digits.
# Here IC1 actually corresponds to MCP23008 (0x22) and IC2 is MCP23008 (0x23)
# Last two entries for digit 0 were 0xe0 and 0x0d. Made them 0x00 for leading zero blanking on the hours display
hrs_data = (
    {'dig': 0, 'IC1-DISP1': 0x0E, 'IC2-DISP1': 0xE0, 'IC1-DISP2': 0x00, 'IC2-DISP2': 0x00},
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

# Deine all the registers of MCP23008. Refer datasheet for details
IODIR = 0x00
IPOL = 0x01
GPINTEN = 0x02
DEFVAL = 0x03
INTCON = 0x04
IOCON = 0x05
GPPU = 0x06
INTF = 0x07
INTCAP = 0x08
GPIOMCP = 0x09
OLAT = 0x0A


# Define all the registers for DS1307. Refer datasheet for details
SECONDS = 0x00
MINUTES = 0x01
HOURS = 0x02
DAY = 0x03
DATE = 0x04
MONTH = 0x05
YEAR = 0x06

CONTROL = 0x0E
STATUS = 0x0F


#########################################

# Trigger is input to HC-SR04 so output from Pi
GPIO.setup(TRIG,GPIO.OUT)
# Echo is output from HC-SR04 so input to Pi
GPIO.setup(ECHO,GPIO.IN)

# Just an arbitrary delay for HC-SR04 to be stable, may not be required..
time.sleep(2)

bus = smbus.SMBus(0) # Change to 1 for newer Raspberry Pi (Post Oct-2012)

# Set IODIR as OUTPUT
bus.write_byte_data(mcp_address1, IODIR, 0b00000000)
bus.write_byte_data(mcp_address2, IODIR, 0b00000000)
bus.write_byte_data(mcp_address3, IODIR, 0b00000000)
bus.write_byte_data(mcp_address4, IODIR, 0b00000000)

# Reset all the other registers, though their default values are already 0x00.
# It also ensures that at power on, all LEDs are off unless explicitly controlled (Register DEFVAL)

for reg in [IPOL,GPINTEN,DEFVAL,INTCON,IOCON,GPPU,INTF,INTCAP,GPIOMCP,OLAT]:
    bus.write_byte_data(address, reg, 0b00000000)
    bus.write_byte_data(address2, reg, 0b00000000)
    bus.write_byte_data(address3, reg, 0b00000000)
    bus.write_byte_data(address4, reg, 0b00000000)
    bus.write_byte_data(address, GPIOMCP, 0x00)
    bus.write_byte_data(address2, GPIOMCP, 0x00)
    bus.write_byte_data(address3, GPIOMCP, 0x00)
    bus.write_byte_data(address4, GPIOMCP, 0x00)

# Serves as a kind of display test. It will show sequence 0000, 1111, 2222 and so on up to 9999 on the display with a 200msec delay
for index in range(0,10):
    bus.write_byte_data(address, GPIOMCP, min_data[index]['IC1-DISP1'] | min_data[index]['IC1-DISP2'])
    bus.write_byte_data(address2, GPIOMCP, min_data[index]['IC2-DISP1'] | min_data[index]['IC2-DISP2'])

    bus.write_byte_data(address3, GPIOMCP, hrs_data[index]['IC1-DISP1'] | hrs_data[index]['IC1-DISP2'])
    bus.write_byte_data(address4, GPIOMCP, hrs_data[index]['IC2-DISP1'] | hrs_data[index]['IC2-DISP2'])
    
    time.sleep(0.2)

# Turn of all displays after display test is done
bus.write_byte_data(address, GPIOMCP, 0x00)
bus.write_byte_data(address2, GPIOMCP, 0x00)
bus.write_byte_data(address3, GPIOMCP, 0x00)
bus.write_byte_data(address4, GPIOMCP, 0x00)

#print "display test done"

# Initialize variables used later
showtime = False
nowtime = futuretime = time.time()

# Continuous loop starts
# All the print statements are left for debugging later if required
while True:
    # Start with setting the trigger pin to LOW. Wait for a second to help sensor be stable.
    # This delay of 1 second may be reduced but may affect performance sometimes.
    GPIO.output(TRIG, False)
#    print "Waiting For Sensor To Settle"
    time.sleep(1)

    # Now send a pulse of 10usec (as per datasheet) on the trigger pin
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # After the pulse is sent, wait for a rising signal on the ECHO pin.
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    # The time duration from sending trigger to getting a rising pulse on echo pin corresponds to distance
    # Note that the obtained value is in seconds
    pulse_duration = pulse_end - pulse_start

    # Multiply the duration by a constant. This constant is based on speed of sound but also corresponds to datasheet.
    # Sparkfun datasheet says to divide the duration (in usec) by 58 which corresponds to multiplying the seconds value by 17241
    # Based on speed of sound as 343m/sec, the distance can be calculated as time required / 2 (send and receive time)
    # Thus (time/2 * 343 * 100) = Distance. Since the speed is in meters, we convert it to cm by multiplying by 100
    # This comes to Distance = 17150 * time duration which is used in the following formula
    # This has not been calibrated though but roughly verified to see that the distance is approximately correct.
    distance = pulse_duration * 17150

    # Round off
    distance = round(distance, 2)

#    print "Distance:",distance,"cm"

    # If the obstacle is within 10 cm of the sensor, we start reading the RTC and displaying it on display
    # We also start a timer of 30 seconds to display the time and then the display is switched off.
    # Within these 30 seconds, if any object is again in vicinity (10cm), the timer is restarted. 
    if distance < 10:
        #print "Object found in vicinity, show time"
        syslog.syslog("USONIC distance: " + str(distance))
        nowtime = time.time()
        futuretime = nowtime + 30
        showtime = True


    if showtime:
        if time.time() < futuretime:
            # We only need hours and minutes
            mints = bus.read_byte_data(address_rtc, MINUTES)
            hrs = bus.read_byte_data(address_rtc, HOURS)
            
            # Convert the BCD data masking off any unwanted bits from the data read
            min_data_2 = (mints & 0xF0) >> 4
            min_data_1 = (mints & 0x0F)
            
            # Hours data contains a few more bits, mask them off as we don't need them
            hrs_data_2 = (hrs & 0x10) >> 4
            hrs_data_1 = (hrs & 0x0F)

            # Corresponding to the data to be displayed, pull out the GPIO data to be sent.
            # It also needs to be ORed because we are going to control two different digits from the same IC
            # The data for these 2 digits is ORed for an IC and sent to it.
            bus.write_byte_data(mcp_address1, GPIOMCP, min_data[min_data_1]['IC1-DISP1'] | min_data[min_data_2]['IC1-DISP2'])
            bus.write_byte_data(mcp_address2, GPIOMCP, min_data[min_data_1]['IC2-DISP1'] | min_data[min_data_2]['IC2-DISP2'])

            bus.write_byte_data(mcp_address3, GPIOMCP, hrs_data[hrs_data_1]['IC1-DISP1'] | hrs_data[hrs_data_2]['IC1-DISP2'] | 0x01)
            bus.write_byte_data(mcp_address4, GPIOMCP, hrs_data[hrs_data_1]['IC2-DISP1'] | hrs_data[hrs_data_2]['IC2-DISP2'])
    
        else:
            #print "Time over"
            # Switch off the display
            showtime = False
            bus.write_byte_data(address, GPIOMCP, 0x00)
            bus.write_byte_data(address2, GPIOMCP, 0x00)
            bus.write_byte_data(address3, GPIOMCP, 0x00)
            bus.write_byte_data(address4, GPIOMCP, 0x00)
    
    # Following else section is not used.
    #else:
        #bus.write_byte_data(address, GPIOMCP, 0x00)
        #bus.write_byte_data(address2, GPIOMCP, 0x00)
        #bus.write_byte_data(address3, GPIOMCP, 0x00)
        #bus.write_byte_data(address4, GPIOMCP, 0x00)
        #showtime = False

# The program won't come here in normal flow        
GPIO.cleanup()
