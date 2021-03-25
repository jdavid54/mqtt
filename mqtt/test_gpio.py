import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(15, GPIO.OUT)
#print('high')
#GPIO.output(15, GPIO.HIGH)

print('low')
GPIO.output(15, GPIO.LOW)