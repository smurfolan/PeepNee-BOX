#import RPi.GPIO as GPIO

#from buzzerSensorManager import BuzzerSensorManager
#from proximitySensorManager import ProximitySensorManager

#proximitySensor = ProximitySensorManager()
#buzzerSensor = BuzzerSensorManager()

     
#if(proximitySensor.object_in_front()):
    #print("in front")
    #buzzerSensor.ring_the_alarm(2)
     
#GPIO.cleanup()
#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

Buzzer = 11    # pin11

def setup(pin):
	global BuzzerPin
	BuzzerPin = pin
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(BuzzerPin, GPIO.OUT)
	GPIO.output(BuzzerPin, GPIO.HIGH)

def on():
	GPIO.output(BuzzerPin, GPIO.LOW)

def off():
	GPIO.output(BuzzerPin, GPIO.HIGH)

def beep(x):
	on()
	time.sleep(x)
	off()
	time.sleep(x)

def loop():
    timeout = time.time() + 1
    while True:
        if time.time() > timeout:
           destroy()
           
        beep(0.5)

def destroy():
	GPIO.output(BuzzerPin, GPIO.HIGH)
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup(Buzzer)
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()