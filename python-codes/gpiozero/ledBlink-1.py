# Basic program to blink an LED using gpiozero library
# The LED is connected to pin 11 on board
# Pin 11 is GPIO 17 on the raspi in BCM mode
# Default pinmode is always BCM mode in gpioZero

from gpiozero import LED
from time import sleep


led = LED(17)	# LED anode at pin 11 (GPIO 17) of the pi

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)

    
