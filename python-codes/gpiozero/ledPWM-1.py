# This code is to demonstrate a PWM signal generation
# With PWM, intensity of an LED is varied.
# LED is connected to pin 11 as usual (GPIO 17) 
# Setting the value to 0 sets ON time as zero so turning off the LED
# Similarly, a value of 1 turns on the LED in full intensity

from gpiozero import PWMLED
from time import sleep

led = PWMLED(17)

while 1:
    led.value=0		# LED is turned off
    sleep(1)

    led.value=0.5	# LED glows in half brightness
    sleep(1)

    led.value=(1)	# LED turns on in full intensity
    sleep(1)
