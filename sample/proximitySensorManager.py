import RPi.GPIO as GPIO
from time import sleep
from patternImplementations import Singleton

class ProximitySensorManager():
    __metaclass__ = Singleton
    
    __INPUT_GPIO_PIN_NUMBER = 40
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__INPUT_GPIO_PIN_NUMBER, GPIO.IN)
        
    def object_in_front(self):
        sensor = GPIO.input(self.__INPUT_GPIO_PIN_NUMBER)
        return sensor == 0