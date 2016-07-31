# This code demonstrates use of Button functionality of gpiozero
# The button object has got a number of functions associated with it
# Most basic are the ways to find out if the button is pressed
# button.is_pressed returns true if the button is pressed
# The button is connected to GPIO 17 (pin 11) with the other end to Ground

from gpiozero import Button

button=Button(2)

while 1:
    if button.is_pressed:
        print("Button is pressed")  	# Printed when button is pressed
    else:
        print("Button is not pressed")	# It will keep printing this normally
        
