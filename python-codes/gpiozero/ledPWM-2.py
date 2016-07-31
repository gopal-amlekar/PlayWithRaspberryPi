# This uses the PWM pulse functionality
# It causes the LED to fade in and fade out
# The LED starts in OFF condition and gradually glows to full intesnsity
# After a while, it then diminishes to full off condition
# The cycle repeats
# LED on GPIO 17 (Pin 11)

from gpiozero import PWMLED
from signal import pause

pro=PWMLED(17)

pro.pulse()

pause()




