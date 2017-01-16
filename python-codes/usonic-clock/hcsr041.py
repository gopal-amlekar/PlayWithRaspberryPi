import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 18 
ECHO = 17
TEMP_LED = 27

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(TEMP_LED, GPIO.OUT)

GPIO.output(TEMP_LED, False)
time.sleep(2)

while True:
    GPIO.output(TRIG, False)
    print "Waiting For Sensor To Settle"
    time.sleep(0.5)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print "Distance:",distance,"cm"

    if distance < 10:
        print "Approaching me, be careful"
        GPIO.output(TEMP_LED, True)
    else:
        GPIO.output(TEMP_LED, False)
        

GPIO.cleanup()
