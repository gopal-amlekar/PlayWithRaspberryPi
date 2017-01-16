from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=17, trigger=18)
while True:
    print('Distance: ', sensor.distance * 100)
    sleep(1)
