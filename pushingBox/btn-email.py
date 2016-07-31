# This code demonstrates use of Button functionality of gpiozero
# The button object has got a number of functions associated with it
# Most basic are the ways to find out if the button is pressed
# button.is_pressed returns true if the button is pressed
# The button is connected to GPIO 17 (pin 11) with the other end to Ground

# When the button is pressed, it calls a http api from pushingbox
# This API then carries out a service configured there (to send out an email)

from gpiozero import Button
from gpiozero impor LED
import requests

button = Button(2)
led = LED(17)
led.off()

while 1:
    if button.is_pressed:
        print("Button is pressed")  	# Printed when button is pressed
        r = requests.post('http://api.pushingbox.com/pushingbox', {'devid':'v39A2FC4A283D8C6'})
        print r
        r = requests.post('http://api.pushingbox.com/pushingbox', {'devid':'v93D86A3CF2DD136'})
        print r
        led.blink(0.5,0.5,5)
        exit (0)
    #else:
    #    print("Button is not pressed")	# It will keep printing this normally
        
