import RPi.GPIO as GPIO
import time

channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)



time.sleep(1)
print("Relay On")
GPIO.output(channel, True)
time.sleep(1)
print("Relay Off")
GPIO.output(channel, False)

time.sleep(1)
print("Relay On")
GPIO.output(channel, True)
time.sleep(1)
print("Relay Off")
GPIO.output(channel, False)



GPIO.cleanup()
