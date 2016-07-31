# This is an alternative for blinking an LED
# Instead of calling ON/OFF with a delay,
# this program generated the blinking on/off cycle
# with just a single function call
# Blinking interval is hard-coded to 1 second
# in the library. That is 1 sec on, 1 sec off
 
from gpiozero import LED
from signal import pause

green=LED(17)

green.blink()

pause()
