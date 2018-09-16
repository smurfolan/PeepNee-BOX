import time
import RPi.GPIO as GPIO
from patternImplementations import Singleton

class BuzzerSensorManager():
    __metaclass__ = Singleton
    
    __OUTPUT_GPIO_PIN_NUMBER = 11
    
    def __init__(self):
            GPIO.setmode(GPIO.BOARD)#Numbers GPIOs by physical location
    
    def start_alarm(self, seconds):
        self.__setup()
        
        timeout = time.time() + seconds
        while True:
            if time.time() > timeout:
                self.__destroy()
                break
            else:
                self.__beep(0.5)
    
    def __setup(self):
            GPIO.setup(self.__OUTPUT_GPIO_PIN_NUMBER, GPIO.OUT)
            GPIO.output(self.__OUTPUT_GPIO_PIN_NUMBER, GPIO.LOW)
	
    def __beep(self, x):
            GPIO.output(self.__OUTPUT_GPIO_PIN_NUMBER,GPIO.LOW)
            time.sleep(x)
            GPIO.output(self.__OUTPUT_GPIO_PIN_NUMBER,GPIO.HIGH)
            time.sleep(x)
    
    def __destroy(self):
            GPIO.output(self.__OUTPUT_GPIO_PIN_NUMBER, GPIO.HIGH)
            GPIO.cleanup(self.__OUTPUT_GPIO_PIN_NUMBER)